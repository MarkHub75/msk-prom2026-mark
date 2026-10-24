# Object-dependent scenario prototypes:03,04,06,08

The official case page4 defines phone use while moving OR working with equipment,
smoking/open fire outside permitted places, height work without a harness, and
additional unsafe cargo carrying. These pure rules return internal Findings;
shared engine owns duration, dedup, candidate identity and evidence. They never
write pipeline state, call a model, or extend external EventMutation v1.

`evaluate(context, config)` uses the shared runtime contract and geometry in
`SCENARIO_RUNTIME_CONTRACT.md`. All objects, keypoints and zone polygons use the
original image grid. Every semantic fact below must be unique, sourced, finite,
score>=configured minimum, and exactly match frame/time/track through
`ml.scenarios.common.fact`; stale or duplicate facts do not establish evidence.
Coverage must explicitly be `complete` for required specialist classes. This is
a declared observation capability, not proven detector recall. Real specialist
models, video annotation, source rights, LinQ parity and accuracy remain gates.
Synthetic/manual facts do NOT establish any of those gates.

| Scenario | Required evidence and facts | Explicit site policy |
|---|---|---|
|03 `phone_use_during_activity` | `phone_object_key` identifies exactly one current phone, `phone_use_observed=true`, and `moving_observed=true` OR `operating_equipment=true`. Visible COCO wrists/head must support phone proximity. | Prototype distance thresholds relative to body diagonal; no temporal confirmation inside rule. |
|04 `open_fire_outside_allowed_zone` | Current flame plus `open_flame_observed=true` and `flame_not_steam_or_reflection=true`, facts keyed by flame object_key. Steam/smoke alone UNKNOWN. | `policy_declared`, nonempty `policy_source`, explicit `allowed_fire_zones`; empty declared list explicitly permits no location. |
|04 `smoking_outside_allowed_zone` | `smoking_observed=true`, `smoking_gesture_observed=true`, `cigarette_object_key` owns a current cigarette; visible feet locate activity. Cigarette presence alone UNKNOWN. | Same declaration and separate `allowed_smoking_zones`. |
|06 `work_at_height_without_harness` | Visible foot point inside declared elevated area, `working_observed=true`, `harness_area_visible=true`, and explicit `harness_state=absent` or `harness_absent=true`. `present` is a negative; conflicting/occluded evidence UNKNOWN. | `height_policy_declared`, nonempty `height_zone_source`, `elevated_work_zones` established by site survey. Pixel y/box height never implies physical elevation. |
|08 `unsafe_cargo_carrying` | `carrying_observed=true`, `carried_object_key` owns a current cargo object; violation of an explicit observable check. | `cargo_policy_declared`, nonempty `policy_source`, `forbidden_carry_zones` and/or `forbid_face_obstruction`. Face check requires `face_load_relation_observable=true` and typed `face_obstructed_by_load`; missing checks UNKNOWN. |

Configs03/04/06/08 are **unvalidated prototypes**. Height/cargo/fire policies are
undeclared by default, yielding BLOCKED. Missing specialist coverage also yields
BLOCKED; missing ownership/action/visibility yields UNKNOWN. Complete observed
negative activity or an explicitly compliant configured check may yield NEGATIVE.
No missing harness detection is mapped to harness absence; no weight, lifting
capacity, medical state or industrial camera layout is inferred. One proven
cargo check can be positive while another configured check remains unresolved;
attributes preserve that uncertainty. No opposite class or ownership is inferred
solely from object proximity.

Focused checks: `python -m unittest tests.test_scenarios_objects -v`. Explicit
synthetic fixtures exercise positive, negative, missing policy/coverage/visibility,
stale facts, conflicting harness facts, object presence alone, low confidence,
original geometry, exact Finding keys and purity. Passing them establishes rule
execution only; neural/video quality, deployment readiness and acceptance of
all eight industrial scenarios are not established by these tests.
