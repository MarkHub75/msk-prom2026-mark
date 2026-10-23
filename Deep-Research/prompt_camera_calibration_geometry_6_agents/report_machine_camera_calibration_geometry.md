---
topic: camera_calibration_geometry
scope: "Single fixed industrial RGB camera: surveyed floor-plane geometry, calibration workflows and lifecycle, contact localization, timestamped speed, operational proximity, limits of complex 3D scenarios, tools and proposed validation."
not_covered:
  - "Full case specification and actual LinQ SDK/device audit: linq_platform."
  - "Exhaustive behavioral-model or dataset catalog: behavioral_models + datasets, model_stack, datasets."
  - "Training, Vast.ai runs and HPO: cv_accuracy_vast, training_strategy."
  - "Compiler/quantization operator audit or verified model export: quantization/export."
  - "Application implementation, production deployment, safety certification or Russian legal compliance assessment."
answers:
  - "What inputs make metric floor mapping identifiable, and how should OpenCV H fitting be performed and checked?"
  - "Which camera-calibration steps can be automated, and what must an integrator verify?"
  - "How do reference point, lens distortion, scene planes and calibration drift affect measurement and abstention?"
  - "What can track-based speed establish, how does it differ from running, and what does 1 FPS lose?"
  - "How should static intrusion, moving-footprint gap and predictive conflict be distinguished?"
  - "Which height, conveyor, suspended-load, fall and harness claims need additional observations?"
  - "Which inspected tools, licenses and dependency constraints matter for an MVP?"
  - "How should independent geometry, speed and event validation and actual LinQ execution be demonstrated?"
keywords:
  - homography
  - ground plane
  - floor calibration
  - camera intrinsics
  - undistortPoints
  - findHomography
  - RANSAC threshold units
  - footpoint
  - bbox bottom center
  - ChArUco
  - AprilTag
  - fSpy
  - Calibmar
  - GeoCalib
  - PTS
  - time_base
  - VFR
  - fast motion
  - running gait
  - PoseC3D
  - SlowFast
  - forklift footprint
  - TTC
  - TCA
  - suspended load
  - single view metrology
  - OpenPose
  - RTMPose
  - Depth Anything V2
  - Metric3D
  - Shapely
  - Norfair
  - ByteTrack
  - CVAT
  - LinQ
  - camera-hour
  - observability
  - indeterminate
entity_schema:
  method_decision:
    - scenario
    - observed_points
    - method
    - calibration_inputs
    - metric_distance
    - assumptions
    - failure_modes
    - compute_placement
    - validation
    - mvp_suitability
    - evidence
  library:
    - name
    - version_or_revision
    - license
    - role
    - limitations
    - evidence
takeaways:
  - "Prioritize configured-zone events, independently validated floor distances to surveyed static danger contours, and timestamped fast-motion rules; disable metric claims without measured scale."
  - "A floor H maps points on its plane only; bbox centers, shoulders, elevated loads and platform contacts cannot be treated as floor points."
  - "Four clicks require known metric XY and nondegenerate geometry; fit residuals and round-trip H checks do not replace physically separate hold-out controls."
  - "findHomography threshold units are dstPoint units: fit floor-to-undistorted-image with an explicit pixel budget, invert, then validate in meters when that noise model is appropriate."
  - "Speed is not gait; selected source FPS, inference throughput and alert latency are different, and brief events may vanish between 1 Hz samples."
  - "Current planar gap, closest approach and TTC are different; prediction needs shape, heading, synchronized tracks and an explicit motion horizon."
  - "Known scene geometry can enable conditional single-view height metrology; floor H alone does not recover arbitrary 3D or true under-load position."
  - "OpenCV wheel 4.13.0.92 and Norfair 2.3.0 have incompatible declared NumPy requirements on the relevant Python baseline; no installation was tested."
  - "Indeterminate is not safe; report all-event recall, observable-event recall, eligible/valid camera-hours and coverage together."
  - "No case-video benchmark, model inference/export or LinQ execution was performed; CPU postprocessing permission, exact SDK, scene accuracy and throughput remain unknown."
checked_at: "2026-10-23T20:03:09+03:00"
research_started_at: "2026-10-23T19:33:12+03:00"
context_version: mosprom-research-v1
case_status:
  available: "Two user-provided Markdown prompts, read in full."
  team_report: "Full case reportedly published and first checkpoint passed; server reportedly LinQ plus CPU without NVIDIA, uploaded videos preferred. These are team-reported facts."
  unavailable: "Official case PDF, actual videos, surveyed references, neighboring reports, SDK and device access."
checks_performed:
  - "Exactly six independent gpt-6.1-sol/medium researchers, fork_turns=none, one wave, maximum three researchers concurrently; orchestrator synthesis only."
  - "Primary documentation, papers, pinned source files, licenses and package metadata read through real Internet research."
  - "Source snapshots saved by branches A03, A05 and A06."
  - "A small standard-library Python pinhole/sampling arithmetic illustration executed locally; not a camera benchmark."
not_executed:
  - "Package installation/resolver/import tests, GUI demos, dataset archive retrieval, model inference/training/export/quantization, camera survey, video benchmarks or LinQ access."
review_mode: "orchestrator_synthesis_only; no_independent_critic; no_second_wave"
human_report: report_human_camera_calibration_geometry.md
evidence_files:
  - SOURCES.md
  - RAW_FACTS.md
  - CRITIC.md
open_questions_file: OPEN_QUESTIONS.md
---

# Camera calibration geometry: actionable contract

Evidence labels: **DOCUMENTED** primary documentation/paper; **CODE_INSPECTED** pinned code or manifest read; **REPORTED_EXPERIMENT** another author's result under its conditions; **LOCAL_OBSERVATION** actually done here; **INFERENCE** our derivation; **HYPOTHESIS** untested proposal; **UNKNOWN** not established. A code read is not a run. [F-ID](RAW_FACTS.md) resolves to detailed evidence and [S-ID](SOURCES.md) to original URL/version/locator. K issues are the orchestrator's own synthesis, not an independent review.

## MVP choice and missing case inputs

**INFERENCE:** implement (1) an explicitly defined observed-point/envelope intrusion event in a configured zone; (2) metric floor positions/distances to surveyed static danger contours only inside validated support; (3) fast motion from stable floor tracks and source timestamps. Without surveyed scale, retain image-zone events and disable meters/m/s. Moving-forklift prediction, learned calibration/depth and literal running recognition are extensions with separate validation requirements. [F021–F030](RAW_FACTS.md#f021), [F039](RAW_FACTS.md#f039), [F047–F052](RAW_FACTS.md#f047)

**UNKNOWN:** the official event definitions, physical thresholds, CPU-rule permission and actual LinQ outputs/resources. The two user prompts are available; the official PDF, videos, references and SDK are absent. The post-checkpoint hardware/accuracy statements are team reports, not independently read official specifications. Resolve Q001–Q007 before strengthening the claims. [F001–F003](RAW_FACTS.md#f001), [F078](RAW_FACTS.md#f078), [questions](OPEN_QUESTIONS.md)

## Metric floor H: identifiability, units and OpenCV API

**DOCUMENTED/INFERENCE:** after distortion correction, `lambda*p~=K[R|t](X,Y,Z,1)^T`. For plane `Z=0`, `lambda*p~=G*q~`, `G=K[r1 r2 t]`; define **G floor→image**, **H=G^-1 image→floor**. Metric XY references establish units; K/R/t need not be recovered separately for a directly fitted planar map. Known K alone does not establish scene scale. [F021](RAW_FACTS.md#f021)

```text
W=h31*u+h32*v+h33
X=(h11*u+h12*v+h13)/W
Y=(h21*u+h22*v+h23)/W
```

Four distinct image↔known-XY pairs form the general minimum; no three are collinear in either plane in the minimal projective frame. Use additional well-distributed near/far/two-direction references and **different physical hold-out controls**. An arbitrary quadrilateral, four clicks or one known segment without further constraints do not determine the general metric H. A measured rectangle supplies `(0,0),(L,0),(L,W),(0,W)` only when its dimensions and right angles are real. Near-collinearity, small support and wrong correspondences destabilize the result. In the inspected traditional OpenCV4.13.0 path, exactly four pairs go straight to the kernel; an all-inlier mask cannot establish that they are correct. [F022](RAW_FACTS.md#f022)

**DOCUMENTED/CODE_INSPECTED, fixed API baseline 4.13.0:**

- `calibrateCamera`: K/D plus board poses; moving-board poses do not automatically calibrate the installed floor.
- `undistort`: raster correction; `undistortPoints`: point correction. No P means normalized camera coordinates; `P=Knew` means corrected pixels. Fit H and process detections in one exact convention.
- `getPerspectiveTransform`: exactly four pairs, inspected wrapper expects four 2D CV_32F points, no robust rejection.
- `findHomography`: 4+ pairs, matrix/mask, possibly empty result. Default `ransacReprojThreshold=3`, `maxIters=2000`, `confidence=0.995` are not recommended scene budgets.
- `perspectiveTransform`: sparse floating-point points with homogeneous normalization. BEV raster generation through `warpPerspective` is optional for distance calculations.

[F023–F025](RAW_FACTS.md#f023), [OpenCV calib3d4.13.0](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)

**Critical threshold rule:** residual units follow **dstPoints**. With image→floor in meters, default 3 means **3 m**, not 3 px. If pixel-click noise dominates, fit G from floor meters to undistorted pixels using an explicit pixel threshold, invert and validate H in meters. This is an engineering estimator choice, not an optimal errors-in-variables solution when survey errors matter. RANSAC cannot repair incorrect dimensions, lens model, plane or footpoint. Its confidence is not event confidence. [F025](RAW_FACTS.md#f025)

Pseudocode only; not executed:

```python
uv_fit = cv.undistortPoints(raw_fit_points, K, D, P=Knew)
G, mask = cv.findHomography(
    fit_xy_metres, uv_fit, method=cv.RANSAC,
    ransacReprojThreshold=pixel_budget,
    maxIters=iteration_budget, confidence=sampling_confidence)
require_supported_invertible_mapping(G, mask)  # proposed gate
H = inverse(G)
uv_hold = cv.undistortPoints(raw_hold_points, K, D, P=Knew)
hold_xy_hat = cv.perspectiveTransform(uv_hold, H)
measure_errors(hold_xy_hat, independent_hold_xy_metres)
# Per frame: inverse detector resize/letterbox exactly once,
# correct contact point in the same pixel convention,
# gate current profile/plane/visibility/support/sensitivity, then apply H.
```

Prefer explicit `N×1×2` floating-point point arrays with API-appropriate dtype. Invalid contact must produce a reason/status, not a fake `(0,0)`. A finite mapped number near the horizon can still be unusable. [F024–F030](RAW_FACTS.md#f024)

## Contact point, planes and error propagation

**INFERENCE:** bbox bottom-center `((left+right)/2,bottom)` is a reference-point model, not direct physical truth. Visible-only boxes terminate at occluders; full-body predictions estimate hidden content. Ankles are above soles; ankle midpoint is not necessarily contact. Masks do not establish support during jumping/occlusion. Top-down torso/head may hide feet. Vehicle bbox bottom-center changes meaning with orientation, forks and loads. [F026](RAW_FACTS.md#f026)

**REPORTED_EXPERIMENT, limited:** Paik et al.2026 used Blender, exact keypoints/camera, 9 Mixamo pedestrians and 5 support-phase poses; CCTV heights3/5/7m and UAV30/50/70m. Toe midpoint was better on average but not universally. Real detector errors and the complete running flight phase were not tested. Do not infer that neural pose always beats bbox. [F026](RAW_FACTS.md#f026), [S023](SOURCES.md#s023)

For camera `C=(Cx,Cy,c)` and point `P=(X,Y,z)` above horizontal floor, inverse floor mapping returns

```text
q_hat=Cxy + c/(c-z)*(Pxy-Cxy)
q_hat-Pxy=z/(c-z)*(Pxy-Cxy)
```

This ray-floor intersection differs from the point's vertical ground projection. A ramp can have its own H; steps/platforms/multiple planes require correct plane selection and, for cross-plane distances, a common geometry. Validity is not guaranteed inside the fit convex hull or outside it. [F027](RAW_FACTS.md#f027)

**LOCAL_OBSERVATION, toy arithmetic only:** ideal horizontal-axis camera `c=4m,f=1000px`, no distortion: a point at `z=1m,Z=8m` falsely maps to floor depth `10.666667m`. A +1px vertical error for actual floor points gives depth errors `0.015968m` at8m, `0.099502m` at20m, `0.396040m` at40m. These are not real-camera accuracy numbers. [F004–F005](RAW_FACTS.md#f004)

**INFERENCE, first-order local uncertainty:**

```text
Jp=(1/W)*[[h11-X*h31,h12-X*h32],
          [h21-Y*h31,h22-Y*h32]]           # m/px
Sigma_q≈Jp*Sigma_p*Jp^T                    # fixed H only
```

For valid gauge h33=1 and `theta=(h11,h12,h13,h21,h22,h23,h31,h32)`:

```text
Jtheta=(1/W)*[[u,v,1,0,0,0,-X*u,-X*v],
              [0,0,0,u,v,1,-Y*u,-Y*v]]
Sigma_q≈Jp*Sigma_p*Jp^T+Jtheta*Sigma_theta*Jtheta^T
```

The second expression assumes independence of current point and fitted parameters; otherwise cross terms are needed. Chain the undistortion Jacobian for raw pixels. Large local sensitivity/horizon proximity invalidates naive linear bounds. Absolute `|W|` without a fixed H normalization is not scale-invariant. Wrong plane/contact/ID is not automatically Gaussian noise. [F028](RAW_FACTS.md#f028)

Shared calibration correlates errors: `Sigma_(q1-q2)=Sigma1+Sigma2-Sigma12-Sigma12^T`; for d>0, `Var(d)≈e^T Sigma_(q1-q2) e`, `e=(q1-q2)/d`. Near d=0 use another numerical/interval method. For `v=dq/dt`, independent dq/dt errors give `Sigma_v≈Sigma_dq/dt²+(dq*dq^T)*Var(dt)/dt⁴`; dependence adds terms. Common translation may cancel while scale bias remains. Empirical quantiles, deterministic bounds, detector scores and parameter covariance are different objects. [F016](RAW_FACTS.md#f016), [F029](RAW_FACTS.md#f029)

**HYPOTHESIS:** use independently measured spatial error budgets and boundary uncertainty bands. With signed inside-distance s and genuinely valid radial bound e, `s>e` inside, `s<−e` outside, otherwise ambiguous. For proximity r, `d_hat+e<r` supports closeness, `d_hat−e>r` supports separation; otherwise indeterminate. If e is an empirical quantile, the conclusion has empirical domain coverage, not a guarantee. Conservative candidate warnings may use envelope intersection but must not be labeled confirmed violations automatically. [F041](RAW_FACTS.md#f041)

## Calibration wizard and lifecycle

**HYPOTHESIS, proposed product workflow:**

1. **Image-zone MVP:** select immutable source frame/profile → draw zone and visibility mask → define footpoint/envelope/boundary semantics and active context → replay independent inside/outside/boundary/legitimate-work episodes → save version. No scale means no meters/m/s.
2. **Measured floor:** fix full coordinate chain → define plane/origin/axes/m → enter surveyed fit XY and image points → inspect G/H/grid/support → define world polygons → evaluate physically different near/far controls → accept region-specific mask or reject → save immutable calibration version.
3. **Assisted extension:** board/fiducials or VP/GeoCalib propose correspondences/intrinsics; integrator confirms target dimensions/plane/orthogonality/crop/scale and passes the same independent controls. Return to manual/image-only when inputs or controls fail.

[F031–F040](RAW_FACTS.md#f031)

Specific inspected building blocks: ChArUco requires exact squares/marker lengths/dictionary/IDs/axis convention (board Z changed after4.6). AprilTag pose requires known tag size and K; tagsize is between detection corners, not outer paper; planar pose can have two solutions. A wall tag is not floor calibration without known scene relation. fSpy uses an arbitrary default distance scale10 until referenceDistance rescales translation. GeoCalib estimates focal/gravity/distortion with assumptions and uncertainty, not floor scale/height/origin. Calibmar1.1.0 has a real intrinsics GUI/report, not an end-to-end safety-zone wizard. [F031–F036](RAW_FACTS.md#f031)

Bind calibration to camera/profile/preset, source resolution, crop/rotation/resize/letterbox/dewarping, lens/zoom/focus, K/D/Knew, plane and input-coordinate convention. Known pure resize can be transformed; unknown sensor mode/ISP warp cannot be assumed equivalent. PTZ/camera movement needs revalidation or separately validated presets. Scene rearrangement can invalidate zone semantics even when camera geometry stays fixed. Static anchors/fiducials/ECC can warn about drift, not certify scale or automatically restore H. Missing matches are unknown. [F037–F040](RAW_FACTS.md#f037)

Proposed config stores reference hashes/PTS, fit and **separate** controls/survey uncertainty, method/threshold **units**, actual residuals/budgets, validity mask, image vs metric zones, rule/context versions, drift outcomes/invalidation reasons and software lock. State `draft→proposed→controls_pending→validated→active`; change triggers `suspect/invalid` and a new accepted version. Events retain their original config/calibration/zone/model IDs, raw detections/points, source evidence and reason codes. [F013](RAW_FACTS.md#f013), [F040](RAW_FACTS.md#f040)

## Physical speed, gait and sampling

**INFERENCE:** `v=(q_j-q_i)/(t_j-t_i)`, `dt>0`, m/s; km/h=3.6*m/s. The norm is chord-displacement speed, not instantaneous peak or average path-length speed. Return motion can disappear; summing noisy short segments overestimates path. Use source time, e.g. `PTS*time_base`, not inference completion time. PTS is not automatically exposure UTC. Keep processing clocks separately, handle VFR/gaps/resets/stale/out-of-order results, and split track generations on identity/time/calibration discontinuity. Prediction is not a new observation. [F007–F016](RAW_FACTS.md#f007)

**HYPOTHESIS:** causal robust regression over valid same-ID floor positions in a seconds-based window, `q_i≈a+b(t_i-t0)`, speed `||b||`. Weighted least-squares slope is `sum(w_i*(t_i-tbar)*(q_i-qbar))/sum(w_i*(t_i-tbar)^2)`; detector score is not inverse metric variance. Require unique-frame count/span/max gap/residual gates. Long windows reduce jitter but smear bursts/add latency; offline future-looking filters cannot establish online latency. Tune W/T/dwell on development episodes, freeze before test. [F015–F019](RAW_FACTS.md#f015)

**Speed is not running:** slow running, fast walking and running in place require independently defined gait labels. Pose/gait, RGB temporal models and pose-temporal models are separate neural methods with separate export/domain tests. SlowFast's paper example and inspected config differ: config SHA `287ec0076846560f44a9327e931a5a2360240533` has `NUM_FRAMES=32`, `SAMPLING_RATE=2`, `ALPHA=4`; span is62/f seconds for uniform source frequency f. Pyskl PoseC3D SHA `f2bf3a6b08e2e8dec744692d64efdb187fd6719a` uses48 temporal positions; its sampler can repeat short-source indices modulo length. Tensor length does not establish unique observed phases. [F009–F012](RAW_FACTS.md#f009)

**1 FPS distinction:** slow processing of every dense archived frame retains temporal evidence but accumulates delay; choosing one source frame per second deletes evidence. Toy `x(t)=2t`, zone `(0.8,1.2)m`, t0..1s gives0.2s occupancy while both1Hz endpoints are outside. Segment crossing is an inference under a trajectory assumption, not directly observed occupancy. No universal minimum FPS was established. Sweep **frequency and phase**, report source/selected/inference rates and end-to-end latency separately. A missed trigger cannot necessarily start adaptive dense sampling. [F006](RAW_FACTS.md#f006), [F017](RAW_FACTS.md#f017)

## Operational proximity: zone, gap and prediction

**INFERENCE:** geometric proximity becomes a violation only under a defined threat, machine mode, guard and allowed operation. Legitimate work/signallers/maintenance/normal walk-under belong in hard negatives; authorization is not a universal risk suppressor. NIOSH magnetic action zones provide a conceptual uncertainty-set precedent, not CCTV accuracy or industrial threshold values. [F043–F044](RAW_FACTS.md#f043), [F055](RAW_FACTS.md#f055)

1. **Static danger zone:** `P_h(t) intersection Z(mode,t) != empty`; alternatively `covers(Z,p_h)` for footpoint. Point vs body-envelope vs hand reach are different rules. Image coordinates support named image-zone intrusion without metric offsets. [F046](RAW_FACTS.md#f046)
2. **Moving floor footprint:** `F_m=q_m+R(theta)*F0(mode,load)`; `g=dist(P_h,F_m)` in shared floor meters. Anchor, heading, forks/load/rear swing must be physically defined. Point-center distance and silhouette masks are not surface gap. `g=0` on overlap, not penetration depth. Unknown heading may yield a conservative union/circle, explicitly less precise. If Hausdorff/position bounds e_m/e_h genuinely hold, `|g_true-g_hat|<=e_m+e_h`; empirical quantiles remain empirical. [F047–F048](RAW_FACTS.md#f047)
3. **Predictive conflict:** synchronized trajectories, current age, heading/turn uncertainty and short horizon T are additional inputs, not consequences of current gap. [F049–F051](RAW_FACTS.md#f049)

```text
r=p_h-q_m; u=v_h-v_m
closing_speed=-(r dot u)/norm(r)             # r != 0
TCA=clip(-(r dot u)/(u dot u),0,T)          # u dot u > 0
d_CA=norm(r+u*TCA)
```

TCA is not TTC. For circles with summed radius R: `a=u·u`, `beta=r·u`, `c0=r·r-R²`, `D=beta²-a*c0`. If c0<=0, TTC=0. Otherwise when a>0,beta<0,D>=0, first root is `(-beta-sqrt(D))/a` if within[0,T]. Other cases predict no future contact **under the model**, not general safety. Handle numerical near-zero/tangency cases. `gap/||u||` is not general2D TTC. For shapes, require simultaneous intersection `P_h(t+tau)∩F_m(t+tau)`, not overlapping total swept areas at different times. Discrete prediction slices need a miss-error bound or continuous/conservative checking. [F049–F051](RAW_FACTS.md#f049)

Straight-line stopping model `s_stop=v*L+v²/(2*a_min)` needs a defined measured response chain L and guaranteed relevant deceleration a_min, including load/floor/turning constraints. No such inputs exist here. Offline replay and detector confidence cannot establish collision avoidance. [F052](RAW_FACTS.md#f052), Q019

**Counterevidence:** Shin–Kim2022 is a12-minute construction CCTV showcase on RTX2080Ti, not field safety proof. Section2.5 transforms person bbox center/shoulders with floor H, violating floor-point assumptions. Reuse the footprint concept only with a corrected anchor model. [F045](RAW_FACTS.md#f045)

## Complex 3D scenes, pose and depth

**Conditional single-view height is possible:** known reference plane, vanishing line/vertical direction and reference height can support special metrology. Floor H alone cannot. With known K/R/C and plane `n^T X+d=0`, ray `r=R^T K^-1[u,v,1]^T` gives `lambda=-(n^T C+d)/(n^T r)`, `X=C+lambda*r`, with valid forward intersection and coordinate conventions. Without extra constraints lambda remains free. Multiple local planes are not automatically one common3D frame. [F056–F057](RAW_FACTS.md#f056)

- **Suspended load:** floor H of elevated bbox center is not its vertical ground projection. Known load height/shape/pose or synchronized telemetry/extra view can constrain it; swing remains. A configured lifting-operation envelope is a valid separate target, not proof of actual current under-load occupancy. [F058](RAW_FACTS.md#f058)
- **Fence/conveyor:** crossing a configured side/access zone does not prove climbing or crawling under. Distinguish before/under/behind, authorized gates/passages, reachable nip points and occlusion. [F053](RAW_FACTS.md#f053), [F065](RAW_FACTS.md#f065)
- **Platform/edge:** calibrate the platform and visible edge separately; lower-floor H is wrong. Harness visible, connector visible, connected and correctly anchored are different relations. Hidden connector is unknown, not absent. [F065–F066](RAW_FACTS.md#f065)
- **Fall/immobility:** horizontal body can be normal floor work; fall needs transition/time. Fresh visible immobility does not diagnose unconsciousness; stale track/frame and hidden person are different failures. [F065](RAW_FACTS.md#f065)

OpenPose is bottom-up PAF with body/foot outputs and coordinate-scale options, under restrictive noncommercial-research conditions. RTMPose is detector/crop+SimCC, MMPose code Apache-2.0; checkpoint/skeleton terms separately. Neither has a verified LinQ path here. Relative Depth Anything V2 lacks absolute scale; metric weights are separate, with Hypersim `max_depth=20m` or VirtualKITTI80m settings, not a mere parameter switch. Metric3D uses focal length/canonicalization; inspected testing code has `.cuda()`. Do not use default focal or per-test GT scale/shift fit to claim absolute accuracy. Visible-surface depth does not reveal opaque occlusions or attachment topology. [F059–F063](RAW_FACTS.md#f059)

**License conflict UNKNOWN:** pinned V2 root README says Small Apache-2.0 and Base/Large/Giant CC-BY-NC-4.0; official Metric-Hypersim-Large card README revision7972080 says Apache-2.0, Small revision3bc65d4 also Apache. Resolve exact selected weights/inheritance with authoritative conditions; do not generalize either label to every variant. [F064](RAW_FACTS.md#f064), Q012

## Scenario decision records

All rows are **INFERENCE**; case-video quality is **NOT ESTABLISHED**. `L→C` means LinQ neural output followed by CPU geometry **conditional on Q005**, not demonstrated execution. Metric yes is limited to the specified validated plane; additional neural routes are UNKNOWN.

| scenario | observed_points | method | calibration_inputs | metric_distance | assumptions | failure_modes | compute_placement | validation | mvp_suitability | evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| Near fast motion | Visible contact, same-ID track, PTS | Floor displacement/causal regression | Surveyed H, controls, time GT | Yes floor/speed | Valid identity/plane/window | Jitter, switches, turn averaging | L→C | Position/speed error, event timing | High conditionally; not gait | F014–F019/F030 |
| Far running/fast motion | Small person/feet, unique temporal observations | Geometry; gait separately | Far controls/sensitivity, exact classifier | Only within accepted far mask | Detail/phases visible | Blur, hidden feet, aliasing | L→C; gait route UNKNOWN | Depth-stratified error/coverage, phase sweep | Conditional; running UNKNOWN | F009–F012/F026/F028 |
| Forbidden-area crossing | Defined point/envelope + polygon | Covers/intersection/episode | Fixed image profile; metric H optional | Image-only no; floor yes | Active zone semantics known | Shift, boundary/plane ambiguity | L→C | Onset/P/R/FAR/coverage | First priority | F039/F041/F046/F070 |
| Static machine proximity | Floor point + danger perimeter | Zone/planar gap | Surveyed perimeter or image zone | Floor contour only | Correct hazard/mode/side | Legitimate work, reach-in | L→C | Normal-work negatives, gap near threshold | High for configured zone | F043/F046/F053/F055 |
| Forklift/pedestrian | Anchors, shape/load/heading, PTS | Current gap; predictive extension | H, dimensions, anchor/time model | Horizontal gap conditionally | Same floor/correct shape | Reverse, rear swing, hidden forks | L→C; extra neural route UNKNOWN | Shape/heading/gap and event lead time | Extension; corridor simpler | F047–F052 |
| Under conveyor | Entrance/person/clearance/sequence | Access zone; action candidate | Floor/passage/mode,3D clearance if required | Floor yes; clearance UNKNOWN | Before/under/behind distinguishable | Occlusion, maintenance, allowed walk-under | L→C; action UNKNOWN | Context/visibility labels, event coverage | Zone feasible; literal under conditional | F053/F065/F066 |
| Under suspended load | Person floor point + load geometry | Operation envelope; conditional actual projection | Perimeter; calibrated height/shape/telemetry | To perimeter yes;3D UNKNOWN | Envelope meaning/time valid |2D overlap, swing, unknown volume | L→C zone;3D UNKNOWN | Actual projection GT vs envelope targets | Named operation zone only | F027/F057/F058 |
| Height/platform/edge/harness | Platform contact/edge; attachment details | Platform H/special metrology/relation | Platform XY/edge/height/references | Platform yes; arbitrary height no | Correct plane and visible relation | Wrong plane/hidden connector/bent body | L→C; extra model/sensor route separate | Edge error; worn/connected/unknown labels | Limited surveyed zone | F056/F059–F066 |
| Fall/immobility | Fresh visible body and sequence/time | Transition or visible inactivity | Scene occlusions; meters optional | Not main target | Transition/interval observable | Floor work/stale frame/hidden person | Temporal LinQ route UNKNOWN | Normal-work negatives, onset/phase recall | Validated candidate only; not diagnosis | F017/F065/F066 |

## Inspected tools and dependency constraints

Versions below are **inspected baselines**, not latest claims or tested installations. Geometry can run mathematically on CPU; actual server performance and permission remain unknown.

| name | version_or_revision | license | role | limitations | evidence |
|---|---|---|---|---|---|
| OpenCV | API/source4.13.0; wheel4.13.0.92 separately | Apache-2.0 plus notices | H/distortion/sparse points/overlay | `/4.x` redirected to4.13 but releases list newer; archive/GitHub dates disagree. Pin exact build/backend | F024/F042/F068 |
| Shapely |2.1.2 | BSD-3-Clause; GEOS LGPL-2.1 separately | Planar geometry | Python≥3.10, GEOS≥3.9, NumPy≥1.21; XY only; validate polygons/NaN | F054/F067/F070 |
| Norfair |2.3.0, `e517b4236f6b67a6ecf342f5df1fccb7788dbc54` | BSD-3-Clause | Detection/keypoint tracker | NumPy `^1.23.0` means<2; optional OpenCV<5 does not solve conflict with wheel4.13 | F068/F069 |
| Original ByteTrack | `d1bf0191adff59bc8fcfeaa0b33d3d1642552a99` | MIT original, not all ports | Box association | Torch import, `np.float`, legacy deps, rescaling and frame-based lifetime need adapter tests | F069 |
| CVAT Community |2.80.0; docs displayed develop | MIT community; other offerings separate | Offline reference annotation | Track XML frame≠PTS; interpolation≠observation; exact docs/release match not tested | F074 |
| Calibmar |1.1.0, `5c5a8200b42b22bac4e1ff62d066c1373a5ce57b` | BSD-3-Clause plus dependencies | Intrinsics GUI/report | GitHub mirror, binaries on GitLab; not a safety-zone wizard; not run | F035 |
| AprilTag |3.4.5 | BSD-2-Clause | Known fiducial detection/pose | Needs physical target specification/K; pose ambiguity and floor relation | F033 |
| fSpy |1.0.3 | GPL-3.0-or-later in code header | Interactive perspective/scale reference | Arbitrary scale without known distance; no field/OS validation | F034 |
| GeoCalib | `1dedb29f94fc11b896c5f572005978aeebccd67f` | Apache-2.0 code, CC-BY-4.0 weights | Optional camera/gravity proposals | Not metric floor scale; extra neural route and CPU latency UNKNOWN | F036 |

**CODE_INSPECTED incompatibility:** `opencv-python-headless==4.13.0.92` declares NumPy≥2 on Python≥3.9; Norfair2.3 declares NumPy<2. On the shared Shapely2.1.2 Python≥3.10 baseline, this is not a ready compatible lock. Resolve through another verified version/build, isolation/adapter or another tracker; bypassing dependencies is not proof. No resolver/install was run. [F068](RAW_FACTS.md#f068)

Shapely `contains` excludes a boundary point and `covers` includes it. Distance to a filled polygon is zero inside/overlap, not signed penetration depth. Z is ignored. Empty/None may produce NaN; explicitly gate finite/valid geometry to indeterminate, never safe. Automatic polygon repair can change the intended zone. Body radius, measurement uncertainty and protective margin must stay separate. [F044](RAW_FACTS.md#f044), [F054](RAW_FACTS.md#f054), [F070](RAW_FACTS.md#f070)

**Reusable examples/GT limits:** official `perspective_correction.py` is inspected image-to-image GUI demo, not a metric ground benchmark. EPFL provides calibrated views and discretized grid GT/research terms, not independent continuous speed truth. BrnoCompSpeed abstract describes18 approximately hour-long Full-HD videos at6 sites,20,865 vehicle instances, LiDAR gates and reference GPS; full paper/data not inspected. Its pinned README currently asks contact for download, uses a Python2 evaluator, and dataset/code license is UNKNOWN; an old tar URL does not establish access. Neither establishes factory person/forklift event quality. [F071–F073](RAW_FACTS.md#f071)

## Rule observability and event evaluation

**HYPOTHESIS:** per-rule observability gate requires valid camera/plane/support, required visible details, fresh source frames, adequate temporal coverage and identity. Harness attachment and footpoint intrusion require different evidence. Use `confirmed_danger` only for the specified rule with sufficient positive evidence/context; `no_detected_danger_with_adequate_observability` for observed absence; otherwise `indeterminate`. Missing detections behind an opaque obstacle do not establish absence. Preserve last positive evidence separately from current visibility; occlusion cannot retroactively make a hidden interval safe. [F041](RAW_FACTS.md#f041), [F065–F066](RAW_FACTS.md#f065)

Annotation must retain plane IDs, actual contact vs ankle, bbox semantics, visible/occluded/out-of-frame, unknown attachments, load-envelope meaning and time, machine mode/permissions, event onset/offset uncertainty and normal-work negatives. Do not fabricate precise hidden-foot GT. One camera-level confidence is insufficient. [F066](RAW_FACTS.md#f066)

**Proposed metrics; no results measured:**

- Position `e_i=||q_hat_i-q_GT_i||`: MAE/RMSE/median/upper quantiles/max, signed X/Y bias, N/raw errors and reference uncertainty, by near/far/direction/camera/occlusion/support.
- Distance `abs(d_hat-d_GT)` with identical point/footprint definition; speed `mean(abs(s_hat-s_GT))` on the **same interval and quantity**. Gate average cannot validate instantaneous peak. Evaluate H-only and contact/detector/tracker contributions separately.
- Freeze class/camera/zone/participant association and temporal-IoU or onset-tolerance matching before test. One-to-one events: unmatched predictions FP, unmatched GT FN; duplicates do not increase TP. `P=TP/(TP+FP)`, `R=TP/(TP+FN)`, zero denominators explicitly undefined.
- `FAR=FP/camera-hours`, not processing-wall-time/person-hours. Show all eligible hours, actual valid-monitoring hours, downtime/abstention and negative-only versus full-timeline denominators separately. Two cameras×one hour=two camera-hours.
- Coverage=`valid decision duration/eligible duration`; report all-GT recall and independently observable-GT conditional recall with counts/reasons. Abstained danger is not TN. Zero FP on a short clip does not establish zero deployed FAR.
- Source-time onset/offset error, sample/window delay, processing queue/infer/rule/display latency and offline replay rate are different measurements.

[F018](RAW_FACTS.md#f018), [F030](RAW_FACTS.md#f030), [F075–F077](RAW_FACTS.md#f075)

Use independent physical survey/time references. Labels produced using the same H cannot validate its scale. Separate calibration-fit, calibration-validation, rule-development and final-test episodes; once controls guide changes they become development data. Split whole trajectories/sessions/cameras according to the transfer claim; bootstrap independent episodes/sessions, not adjacent correlated frames. Small-sample P95 is unstable: retain N/max/raw residuals. Set budgets `B_pos(region)`, `B_dist(region)`, `B_speed(interval)`, recall/FAR/latency/minimum-coverage **before** test. No universal centimeters, m/s or FPS are justified here. [F030](RAW_FACTS.md#f030), [F077](RAW_FACTS.md#f077)

## Proposed experiments and decision branches

All E001–E010 are **NOT EXECUTED**; complete inputs, steps, evidence retention, pass/fail branches and non-proofs are in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md). The following is sufficient to select the next action.

1. **E001 environment/output contract:** actual OS/Python/SDK/manifests → resolver/lock/import/API/coordinate sample checks; save hashes/logs/cv2/GEOS build. Conflict triggers another verified build/adapter/isolation. Success does not establish model execution/accuracy.
2. **E002 metric hold-out:** surveyed fit and physically different near/far/directional controls → freeze G/H → spatial position/distance errors against predeclared budgets. Failure narrows mask or returns to image-only; changed H needs new hold-out. Success does not establish detector/contact/3D.
3. **E003 contact A/B:** same frozen H/frames with independent contact+visibility GT → compare bbox/pose/masks paired pixel/world errors and coverage. Hidden contact remains unknown. Success selects an observation model, not gait/attachment.
4. **E004 source time/speed:** original PTS and independent interval GT → oracle vs real tracks; processing-delay/drop/stale/reset/out-of-order perturbations → speed error/ID/window lag/coverage. Same q/t must not change speed with processing load. Success does not establish instantaneous peak or running.
5. **E005 events/normal work:** independent full sessions, expert labels/context, frozen matching/thresholds → one-to-one P/R/FAR/duplicates/onset/coverage. Semantic false alarms trigger rule/state revision on development and a new test, not test-set threshold tuning. Success is domain-limited.
6. **E006 sampling+phase:** same dense source; proposed sweep1/2/5/10FPS plus original and multiple phase offsets, selected by PTS; retain unique IDs/gaps → event recall/timing/speed/coverage/ID errors. Missing transient triggers denser selection or narrower claim. Success does not establish LinQ throughput.
7. **E007 drift/observability:** normal anchors/light/vibration and one-variable shifts/zoom/crop/resolution/occlusion/new plane → degradation, invalidation miss/delay/false invalidation, wrong-safe during blind intervals. Suspend/revalidate as needed. No universal auto-recalibration claim.
8. **E008 footprint/prediction:** physical shape/load/anchor/heading/time and safely archived maneuvers → gap/shape/orientation errors first, then TCA+d_CA/TTC/simultaneous shape conflict, reverse/turn/near-pass. Require measured L/a_min for stop claims. Failure returns to current gap/corridor/zone. No collision-prevention proof.
9. **E009 3D ambiguity/depth:** known platforms/load geometry and independent3D GT → before/under/behind, similar2D projections, hidden connector, floor-work counterexamples. Optional depth uses frozen calibration without per-test scale/shift fit; evaluate critical clearance/edges/events. Never create real danger for GT. Success does not establish hidden-object visibility or LinQ.
10. **E010 target execution/demo:** actual device/SDK/model and uploaded video → match real LinQ outputs to source frames/PTS, replay geometry, preserve model/runtime/device artifacts/config/annotation/raw outputs/hashes. Show independent floor controls, distance, motion, one explainable event, legitimate negative and indeterminate/camera-change failure. Record source/selected/inference rates and latency separately. Manual tracks only prove a labeled geometry layer, not end-to-end LinQ tracking.

## Conditional deployment and adjacent-topic handoff

**UNKNOWN/HYPOTHESIS:** if actual rules/SDK allow CPU postprocessing, use uploaded server video → decode/source PTS → agreed neural model on LinQ → inverse preprocessing exactly once → CPU tracker/floor mapping/polygon/time rules → versioned episode/evidence. Pose/depth/action/ReID are additional neural inference, not hidden CPU geometry. Do not invent SDK commands, paths, hardware configuration or graph support. Actual execution requires runtime/device/model artifacts, not an ONNX filename or NVIDIA success. [F078](RAW_FACTS.md#f078)

Priority unanswered inputs: official event ontology **Q001**; surveyed scale/controls **Q002**; image transforms **Q003**; timestamps/FPS/latency meaning **Q004**; CPU/SDK/device contract **Q005**; contact visibility/semantics **Q006**; machine state/allowed operations **Q007**. Footprint **Q008**, budgets **Q009**, drift **Q010**, complex-scene geometry **Q011**, exact depth license **Q012**, compatible lock **Q013**, dataset terms **Q014**, independent speed GT **Q015**, negative sessions **Q016**, checkpoint/device transfer **Q017**, indeterminate policy **Q018**, actual response/braking **Q019**, release-metadata history **Q020** remain scoped questions, not presumed facts. [Question registry](OPEN_QUESTIONS.md)

→ `model_stack`/`violation_methods`: contact/bbox/skeleton/visibility semantics, coordinate inverse and unique-frame/span contract. → `linq_platform`/`quantization/export`: permission, exact graph/weights/runtime and coordinate/temporal fidelity after export. → `video_architecture`: source PTS/epochs/stale age and separate processing clocks/profile versions. → `evaluation`: independent layered GT, event matching, FAR denominators and abstention coverage. → `datasets`/`behavioral_models + datasets`: gait/context hard negatives and EPFL/Brno terms/GT limits. → `operator_product`: rule-specific indeterminate reasons, latest confirmed evidence and immutable event versions. Neighbor reports were unavailable; no existence/content/paths are invented. [Detailed handoff](OPEN_QUESTIONS.md#адресная-передача-соседним-исследованиям)
