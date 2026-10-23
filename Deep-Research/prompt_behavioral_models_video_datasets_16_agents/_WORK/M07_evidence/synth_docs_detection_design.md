# Zero-Shot Detection & Distance Estimation — Technical Reference

> **Scope:** Grounding DINO-based detection of two safety events (worker-near-machinery, lifted-load) with proximity estimation from fixed-angle CCTV.
> **Last updated:** 2026-02-25

---

## 1. Detection: Grounding DINO

### What it is

Grounding DINO is an **open-vocabulary object detector**. Unlike YOLO (which only finds the 80 COCO classes it was trained on), Grounding DINO accepts a free-text prompt describing what to find and detects matching objects in the image — zero-shot, no fine-tuning.

Architecture: Swin Transformer (vision) + BERT (text) + cross-modal decoder with deformable attention. The model learns to ground language in visual regions.

### Why it fits this task

- We need to detect **domain-specific objects** ("excavator", "suspended load", "crane hook") that YOLO doesn't natively recognize.
- No labeled construction-safety dataset required.
- We run two separate detection calls per frame:
  - **Targets**: `"person . worker . construction worker"`
  - **Hazards**: varies by event type (see Section 3)

### Current implementation

- Model: `IDEA-Research/grounding-dino-base` via HuggingFace transformers 5.x
- Runs on RTX 5090 (Blackwell sm_120) via PyTorch nightly cu130
- No CUDA compilation needed (pure Python, unlike the original DINO source)
- Fallback: YOLO-World (`yolov8x-worldv2`) with the same interface

### API notes (transformers 5.x)

```python
processor.post_process_grounded_object_detection(
    outputs, input_ids,
    threshold=0.3,          # NOT box_threshold
    text_threshold=0.25,
    target_sizes=[(h, w)],
)
# Returns: boxes, scores, text_labels (NOT labels)
```

---

## 2. Two Event Types

### Event 1: Worker Near Machinery

**Definition:** A worker is within the danger zone of operational heavy machinery.

**Detection prompts:**
- Targets: `"person . worker . construction worker"`
- Hazards: `"excavator . crane . bulldozer . forklift . truck . heavy machinery . vehicle"`

**Spatial rule:** Pixel-based proximity heuristic (see Section 4) between worker foot-point and machinery foot-point.

**Additional condition:** The machine must be **active** — either visibly moving or showing signs of being operational (see Section 6). A parked, fully shut-down machine near a worker is not a violation.

### Event 2: Lifted Load

**Definition:** A worker is beneath or dangerously close to a suspended load.

**Detection prompts:**
- Targets: `"person . worker . construction worker"`
- Hazards: `"chain hoist . concrete bucket . concrete skip . lifted container . hanging bucket . steel beam"`

Note: We detect the **hoist/rigging point** and the **payload** — not the crane itself. The crane is the lifting equipment, not the hazard. The hazard is what's hanging from it. Grounding DINO reliably detects `chain hoist` (the hook/rigging assembly, scores 0.35–0.53) and `concrete bucket`/`concrete skip` (the payload, scores 0.28–0.46). Lower detection thresholds are used for this event (box=0.2, text=0.15).

**Spatial rule — five-stage filter cascade** (see `notes/parameters.md` Section 3 for full detail):
1. **Confidence gate:** Hazard score ≥ 0.30 (detection runs at 0.20 for discovery; only high-confidence detections trigger violations).
2. **Max height:** Box height < 35% of frame — rejects crane-structure misdetections.
3. **Min area:** Box area ≥ 0.4% of frame — rejects tiny phantom detections.
4. **Suspension check:** Load's **bottom edge** must be above the worker's **top edge** in image coordinates. This is the strictest 2D test: it only fires when the load visually floats above the worker's head. Designed to be perspective-safe — avoids y-comparisons that break across different depths.
5. **Proximity:** Centroid-to-centroid distance ≤ 0.40 (normalised). Generous because OSHA defines the fall zone as extending beyond the vertical projection (pendulum/swing effect).

**No motion condition.** Any suspended load — even if static — poses a risk. The hazard is the potential energy of the load, not its kinetic state.

---

## 3. Regulatory and Literature Review: Distance Thresholds

### 3.1 Worker Near Machinery — Regulations

No major regulatory body prescribes a single universal metre value. Instead, regulations require exclusion zones defined by the equipment's actual operating envelope (swing radius, travel path). The key regulations:

| Jurisdiction | Regulation | What it says |
|---|---|---|
| **US (OSHA)** | 29 CFR 1926.1424 | Barricade the swing radius of the rotating superstructure. No fixed distance — zone = actual swing envelope. |
| **US (OSHA)** | 29 CFR 1926.1408 Table A | Only prescriptive distance: 10 ft (3.05 m) clearance from power lines ≤50 kV. |
| **US (OSHA)** | Letter of Interpretation, 2003-01-16 | Being caught between rotating excavator superstructure and other objects is a "serious hazard." Barricade the full swing radius. |
| **UK (HSE)** | Excavators guidance | People must be kept away from areas of excavator operation via suitable barriers. No fixed metre figure. Industry practice: 3–6 m. |
| **Australia** | SafeWork NSW Code of Practice (2025) | Risk-assessment-based. Industry practice: 3–5 m for smaller machines (excavators, forklifts), 10 m for tipping trucks. |
| **EU** | EN 474-5:2022 | Hazard zone identification required but specific distances delegated to risk assessment. |

### 3.2 Worker Near Machinery — Literature and Industry

The academic literature and commercial systems span a range:

| Source | Threshold | Context |
|---|---|---|
| Shen et al. (2016), JCEM | 2 m initial safety boundary | Equipment-specific hazard zone design for excavators. The 2 m is a baseline buffer added beyond the operating radius. |
| Lee et al. (2017), MDPI Sustainability | 2 m / 6 m / 12 m | Three-tier model: high / medium / low hazard. |
| Sakhakarmi et al. (2023), Sensors | 2 m (Red zone buffer) | Five-zone model. Red = +2 m beyond operating radius = no personnel. |
| Park et al. (2019), Sensors | 4 m / 7 m / 10 m / 13 m | Four-tier crane operation zones (highest risk → awareness). |
| Chinese construction spec | 2–3 m (excavation), 6 m (percussion hammer), 10 m (asphalt lifting) | Activity-specific, more prescriptive. |
| Kim & Teizer (2014), RFID systems | 3–5 m | Minimum reliable detection threshold in field tests. |
| ZoneSafe (commercial) | 3–9 m | Configurable. Outer pre-warning + inner close-proximity alert. |
| Caterpillar Cat Detect | 9 m (270°), 16 m (rear) | Three tiers: Yellow / Amber / Red. |
| Australian industry practice | 3–5 m (small machines) | Excavators, forklifts. |

**Consensus:** The literature is not unified on a single value. The range of "danger zone" thresholds spans **2–5 m**, with 2 m being the absolute minimum buffer and 3–5 m being the most common primary alert threshold. Warning zones extend to 6–10 m. The tiered approach (2 m critical / 6 m warning / 12 m awareness) from Lee et al. is widely adopted.

### 3.3 What Happens at 1 m?

A 1 m threshold would be **insufficient by every standard reviewed**:

- No regulation, paper, or commercial system uses 1 m as an alert threshold.
- At 1 m, a worker is within arm's reach of moving machinery. At typical walking speed (1.4 m/s), this provides only **0.7 seconds of reaction time** — far below the 2-second minimum recommended by NIOSH.
- Even the tightest red-zone definitions (Sakhakarmi et al.) use 2 m as the buffer beyond the operating radius, not as the total distance.
- At 1 m, detection itself becomes unreliable: in a typical 1080p CCTV view, 1 m at 30 m depth corresponds to only ~36 pixels (~0.019 normalized) — borderline for bounding-box-based proximity detection.

**Practical implication for our system:** Using a 1 m threshold would dramatically reduce recall. Workers who are dangerously close (1.5 m from a moving excavator arm) would be classified as safe. If a tighter threshold is considered, **2 m is the defensible minimum** — it is the lower bound of the literature consensus and provides barely sufficient reaction time.

### 3.4 Lifted Load — Regulations and Fall Zone Geometry

| Jurisdiction | Regulation | What it says |
|---|---|---|
| **US (OSHA)** | 29 CFR 1926.1425 | No worker within the "fall zone" while a load is suspended. Fall zone = area where it is "reasonably foreseeable" that materials could fall — **explicitly includes area beyond the vertical projection**. |
| **US (OSHA)** | 29 CFR 1926.753 | Routes for suspended loads must be pre-planned so no worker is directly below. |
| **US (OSHA)** | 29 CFR 1926.651(e)(1) | No worker beneath loads handled by lifting or digging equipment. |
| **UK** | LOLER 1998 | Exclusion zone must be defined in the lift plan. Risk-assessment-based. |

The fall zone is **not purely vertical**. It accounts for:
- **Pendulum/swing effect:** A suspended load behaves as a pendulum. If the crane stops suddenly, the load swings.
- **Industry rule of thumb:** 10 ft (3.05 m) minimum radius from the vertical projection of the load.
- **Geometric model:** The fall zone is a cone — apex at the hook, base on the ground, radius = f(rope length, max swing angle, load dimensions).

For our vision-based system, the practical implementation is:
- Primary detection: is the worker **directly beneath** the load? (Horizontal overlap of bounding boxes with the load above.)
- Extended detection: is the worker within ~3 m horizontal distance of the load's vertical projection?
- No motion requirement — any suspended load is a hazard regardless of whether it is moving or static.

---

## 4. Distance Estimation: Why We Use a Pixel Heuristic

### 4.1 The Constraint: No Ground-Truth Measurements

We are processing **dozens of camera angles** from construction site CCTV. We do not have:
- Physical access to the sites to measure reference points
- Camera calibration matrices or intrinsic parameters
- Known ground-plane reference distances for any view

This rules out homography-based approaches as our primary method. We document the alternatives below and explain why the pixel heuristic is the pragmatic choice.

### 4.2 Approaches Considered

#### Approach A: Ground-Plane Homography (Not Selected)

**How it works:** Identify 4+ ground-plane reference points with known real-world positions per camera view. Compute a 3×3 homography matrix. Map foot-points to bird's-eye-view metric coordinates. Compute Euclidean distance in metres.

**Why not selected:**
- Requires **manual calibration per camera view**. With dozens of views and no site access, this does not scale.
- Even if we estimated reference points from visible objects (e.g., a standard 20-ft shipping container = 6.1 m, standard lane width = 3.5 m), these objects are not reliably present in every view.
- Estimation from visible objects introduces **±20–30% error** in the reference distances themselves, propagating into the homography and reducing the accuracy advantage over simpler methods.
- Assumes a flat ground plane — breaks for sloped terrain, scaffolding, multi-level sites.

**Accuracy if calibration were available:** ~0.3–0.5 m error (Shen et al. report 0.45 m for 3D proximity estimation from a single 2D camera).

**Verdict:** Gold standard for fixed installations with known geometry. Not viable for our zero-shot, multi-camera, no-access-to-site pipeline.

#### Approach B: Monocular Depth Estimation (Not Selected as Primary)

**How it works:** Run Depth Anything V2 Metric Outdoor (or similar) per frame. Extract metric depth at foot-points. Convert to 3D world coordinates. Compute Euclidean distance.

**Why not selected as primary:**
- Computational cost: ~220 ms/frame on GPU (Large model). For a paper processing many videos × multiple obfuscation levels, this adds significant overhead.
- Accuracy outdoors: ~0.45 m MAE (Depth Anything V2 benchmark). For a 2 m threshold, this means effective detection range of ~1.5–2.5 m — workable but introduces meaningful uncertainty near the threshold.
- May struggle with construction site conditions: dust, glare, reflective surfaces, unusual textures.

**Verdict:** Strong complementary signal. Could be added later for ablation or as a secondary validation method.

#### Approach C: Person-Height-Scaled Pixel Heuristic (Selected — Enhanced Version)

**How it works:**
1. Compute the **foot-point** of each bounding box: `(center_x, bottom_y)` — approximates ground contact point.
2. Compute Euclidean distance between foot-points in normalized [0,1] coordinates.
3. **Scale by local person height:** Use the detected person's bounding-box height as a proxy for depth. A person's pixel height is roughly proportional to `1/distance`. Dividing the pixel distance by the person's pixel height gives a **body-height-relative distance** that partially compensates for perspective.
4. Flag violation if distance < threshold (calibrated in body-height units ≈ 1.7 m).

**Enhancement over raw pixel distance:** Using person height as a local scale factor means the effective threshold adapts to depth. A 2 m gap near the camera (where people are tall in pixels) and a 2 m gap far from the camera (where people are short in pixels) produce similar body-height-relative values.

**Expected error range:**
- With person-height scaling: **±30–40%** depending on camera angle, person pose (crouching reduces apparent height), and lateral vs depth separation.
- Without scaling (raw normalized distance): **±50–300%** depending on scene depth variation.
- The scaling partially corrects perspective but cannot handle depth differences between the two objects being compared (e.g., worker at 10 m, machine at 20 m from camera).

### 4.3 Why the Pixel Heuristic Is Defensible

1. **Precedent:** Multiple construction safety papers use pixel-space proximity (bounding box overlap, centroid distance, expanded boxes) without metric calibration. Son & Kim (2021, Automation in Construction) evaluate worker-in-swing-radius using bounding box overlap, not metric distances.

2. **Consistent with the zero-shot paradigm:** Our contribution is demonstrating that zero-shot detection (Grounding DINO, no training data) can identify safety violations from uncalibrated CCTV. Requiring per-camera calibration would contradict this.

3. **Conservative framing:** We frame the threshold as detecting "workers in the proximity zone of heavy equipment" (~3–7 m equivalent with our current threshold), consistent with the warning-zone range used by commercial proximity alert systems (ZoneSafe 3–9 m, Cat Detect 9 m). We do not claim to detect the precise 2 m critical boundary.

4. **Scalability:** Works identically across dozens of camera angles with no per-camera setup.

### 4.4 Pixel Distance vs Real-World Distance

For a typical construction CCTV (1080p, 6 m height, 4 mm lens, 45° tilt):

| Depth from camera | Approx. px/m | 2 m normalized | 1 m normalized | Person height (px) |
|---|---|---|---|---|
| 10 m | ~107 | 0.111 | 0.056 | ~182 |
| 15 m | ~71 | 0.074 | 0.037 | ~121 |
| 20 m | ~53 | 0.056 | 0.028 | ~91 |
| 30 m | ~36 | 0.037 | 0.019 | ~61 |

**Key observations:**
- A single normalized threshold of 0.25 corresponds to ~4.5 m at 20 m depth — firmly in the warning zone.
- At 1 m real-world distance, the pixel gap at 30 m depth is only ~36 px (0.019 normalized) — at the limit of what bounding-box precision can resolve.
- Person-height scaling reduces this variance: `2 m / 1.7 m ≈ 1.18 body heights` is roughly constant across depths if person height is correctly detected.

### 4.5 Threshold Selection

Our current threshold (0.25 normalized, unscaled) corresponds approximately to:
- ~2.2 m at 10 m depth (tight — close to critical zone)
- ~4.5 m at 20 m depth (warning zone)
- ~6.8 m at 30 m depth (extended warning zone)

This is a **recall-oriented** threshold: it will catch most true violations but will also flag workers in the broader warning zone. This is intentional given our F2 metric (which weights recall 4× over precision).

If tighter detection is needed (e.g., the 2 m critical zone), options are:
1. **Reduce threshold to ~0.07–0.10** — but this risks missing violations at far depths.
2. **Implement person-height scaling** — partially corrects for depth, allowing a tighter threshold.
3. **Add depth estimation as a secondary filter** — reject pixel-heuristic positives where the depth model places objects far apart.

---

## 5. Lifted Load: Spatial Rule Details

> **Full parameter table and calibration history:** see `notes/parameters.md` Section 3.

### 5.1 The Perspective Problem

Unlike worker-near-machinery (which compares foot-points at roughly the same ground plane), lifted-load detection must compare objects at **different elevations**. In a fixed CCTV view, perspective projection causes two systematic failures:

1. **Ground-level objects at distance appear "above" nearby workers.** An excavator bucket 30 m from the camera projects to a lower y-coordinate than a worker 10 m from the camera, even though both are at ground level.
2. **Suspended loads at distance appear "below" nearby workers' heads.** A concrete mixer suspended 10 m above the ground but 30 m from the camera may have its centroid at a higher y-coordinate (lower in image) than a nearby worker's head.

These failures invalidate any filter that compares the load's centroid or top edge against the worker's head or centroid across different depths. The only 2D comparison that remains perspective-safe is: **does the load's bottom edge appear above the worker's top edge?** This can only be true when the load is visually floating above the worker in the image, which is a strong (if conservative) indicator of suspension.

### 5.2 Current Implementation: Five-Stage Filter Cascade

Applied per (hazard, target) pair:

| # | Filter | Threshold | Rejects |
|---|---|---|---|
| 1 | Confidence | score ≥ 0.30 | Low-confidence phantom detections from relaxed threshold |
| 2 | Max height | box_height < 0.35 | Crane-structure boxes spanning the frame |
| 3 | Min area | box_area ≥ 0.004 | Tiny phantom boxes on small scene features |
| 4 | Suspension | load_bottom_y < worker_top_y | Objects at or below worker head level (perspective-safe) |
| 5 | Proximity | centroid_dist ≤ 0.40 | Workers too far from load's fall zone |

### 5.3 Known Limitations

The strict suspension check (load bottom above worker top) sacrifices recall for perspective safety. It will miss:
- Loads suspended at distance whose bottom edge appears at the same y-level as a nearby worker's head.
- Extreme camera tilt angles where vertical ordering in the image does not correspond to 3D elevation ordering.

Monocular depth estimation (e.g., Depth Anything V2) could resolve these cases but adds computational cost and is not yet integrated.

---

## 6. Machine Activity Detection

### 6.1 Definition of "Active"

A machine is considered **active** (and therefore hazardous) if it meets **any** of the following conditions:

| State | Detection method | Description |
|---|---|---|
| **Moving** | Optical flow in machinery ROI | Arm swinging, wheels turning, tracks moving, boom rotating. Large, clearly visible motion. |
| **About to move** | Operator posture / cabin occupancy | Operator is in the cabin and appears to be at the controls. Detected via person detection within the machinery bounding box. |
| **Energised (on but stationary)** | Visual indicators | Warning lights/beacons flashing, exhaust visible, headlights on. Detectable via color change or periodic brightness variation in the ROI. |

The key insight: **machines that are on but momentarily stationary are just as dangerous as moving machines.** An excavator with its engine running and an operator at the controls can begin swinging at any moment. The reaction time for a nearby worker is the same whether the machine is currently moving or about to move.

### 6.2 Implementation: Tiered Detection

**Tier 1 — Visible motion (highest confidence):**
- Compute dense optical flow (Farnebäck) between consecutive frames within the machinery bounding box.
- Compute mean flow magnitude. Threshold for "moving": to be calibrated per scene (must exceed camera noise / wind-induced sway).
- This catches: arm movement, travel motion, boom rotation, load swinging.

**Tier 2 — Operator presence (medium confidence):**
- Run person detection (Grounding DINO with `"person . operator"`) within the machinery bounding box.
- If a person is detected in the cabin/seat area of the machine, flag as "operator present."
- An occupied machine is assumed active unless proven otherwise.

**Tier 3 — Visual indicators (lower confidence, secondary):**
- Detect periodic brightness changes in the ROI (flashing beacons / warning lights).
- Detect color anomalies consistent with exhaust plumes above the machine.
- These are supplementary signals, not primary detectors.

### 6.3 Integration with Event Detection

**Worker Near Machinery:**
```
frame_violation = worker_in_proximity AND machine_is_active
```
If the machine shows no signs of being active across the entire video, the video is classified as negative regardless of worker proximity.

**Lifted Load:**
```
frame_violation = worker_under_load
```
No activity check. Any suspended load is hazardous, whether moving or static. The hazard is the potential energy of the load, not its kinetic state.

### 6.4 Aggregation

Machine activity is assessed at the **video level**, not frame level. If the machine is active in any frames during the video, it is considered active for the entire video. Rationale: an excavator that moves in frames 1–10 and is stationary in frames 11–20 is still operational — the operator may have paused briefly.

---

## 7. Pipeline Architecture (Revised)

```
Frame extraction (1 fps)
    │
    ├─→ Grounding DINO: detect targets (workers)
    ├─→ Grounding DINO: detect hazards (machinery / loads)
    │
    ▼
Foot-point extraction (bottom-center of each bbox)
    │
    ▼
Per-event spatial rule:
    │
    ├─→ worker_near_machinery:
    │       Pixel heuristic (foot-point distance, person-height-scaled)
    │       → within proximity zone?
    │
    ├─→ lifted_load:
    │       Vertical alignment + horizontal overlap check
    │       → worker under load?
    │
    ▼
Machine activity check:
    │
    ├─→ worker_near_machinery: optical flow + operator detection in machinery ROI
    │       Machine active? (any frame in video)
    │
    ├─→ lifted_load: SKIP (all suspended loads are hazardous)
    │
    ▼
Frame-level violation:
    • worker_near_machinery: proximity AND machine_active
    • lifted_load: worker_under_load (unconditional)
    │
    ▼
Video-level aggregation:
    • Positive if ≥2 violation frames OR ≥20% violation ratio
    • (OR = recall-friendly, aligned with F2 metric)
```

---

## 8. Summary of Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Detection backbone | Grounding DINO (HuggingFace) | Open-vocabulary, zero-shot, no CUDA compilation, works on Blackwell |
| Distance estimation | Person-height-scaled pixel heuristic | No ground-truth measurements available, must work across dozens of camera angles without per-camera calibration |
| Proximity threshold | ~0.25 normalized (≈3–7 m warning zone) | Recall-oriented, consistent with commercial PWS range. F2 metric prioritises catching violations. |
| Machine activity | Required for worker-near-machinery only | Inactive machines are not hazardous. Detected via optical flow + operator presence. |
| Lifted load activity | Not required | Any suspended load is hazardous regardless of motion state. |
| Video aggregation | OR of (≥2 frames, ≥20% ratio) | Recall-friendly. A violation in even a few frames is safety-relevant. |

---

## 9. References

### Regulations
- OSHA 29 CFR 1926.1424 — Work Area Control (swing radius exclusion)
- OSHA 29 CFR 1926.1425 — Keeping Clear of the Load (fall zone definition)
- OSHA 29 CFR 1926.1408 Table A — Power line clearance distances
- OSHA 29 CFR 1926.651 — Specific Excavation Requirements
- OSHA 29 CFR 1926.753 — Hoisting and Rigging (suspended loads in steel erection)
- OSHA Letter of Interpretation 2003-01-16 — Excavator swing radius hazard
- UK HSE — Excavators guidance; LOLER 1998 (Lifting Operations and Lifting Equipment Regulations)
- SafeWork NSW Code of Practice — Moving Plant on Construction Sites (2025)
- EN 474-5:2022 — Hydraulic Excavators Safety
- ISO 13857:2019 — Safety Distances to Prevent Hazard Zones Being Reached

### Distance thresholds and zone models
- Shen et al. (2016). "Hazardous Proximity Zone Design for Heavy Construction Excavation Equipment." JCEM. doi:10.1061/(ASCE)CO.1943-7862.0001108
- Lee et al. (2017). "Proximity Warning and Excavator Control System for Prevention of Collision Accidents." Sustainability. doi:10.3390/su9081488
- Sakhakarmi et al. (2023). "UWB-Based Proximity Warning System." Sensors. PMC10747065.
- Park et al. (2019). "Safety Distance for Crane Drivers." Sensors. PMC6631589.
- arXiv:2508.00862 — Survey on Proximity Monitoring in Construction (2025)

### Commercial proximity warning systems
- ZoneSafe (Avonwood Developments) — 3–9 m configurable zones
- Caterpillar Cat Detect — 9 m / 16 m tiered detection
- Reactec R-Link — configurable UWB-based exclusion zones

### Distance estimation methods
- Fei et al. (2021). "Single View Physical Distance Estimation Using Human Pose." ICCV 2021.
- Bochicchio et al. (2022). "Social Distancing with YOLOv4-tiny and Bird-Eye View." J. Real-Time Image Process.
- Yang et al. (2024). "Depth Anything V2." arXiv:2406.09414.
- Piccinelli et al. (2024). "UniDepth: Universal Monocular Metric Depth Estimation." CVPR 2024.
- ASCE (2023). "Real-Time Struck-By Hazards Detection from Far-Field Surveillance." JCCEE5.CPENG-5238.
- Son & Kim (2021). "Integrated Worker Detection and Tracking for Safe Interaction with Construction Machines." Automation in Construction, Vol. 126, 103670.

### Detection models
- Liu et al. (2023). "Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection." arXiv:2303.05499.
- Cheng et al. (2024). "YOLO-World: Real-Time Open-Vocabulary Object Detection." CVPR 2024.
