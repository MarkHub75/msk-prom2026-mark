# Parameter Registry (Living Document)

> **Purpose:** Track every tuneable parameter, its current value, rationale, and
> calibration history. When we write the paper's method section, this document
> becomes the single source of truth for reporting.
>
> **Last updated:** 2026-03-05
> **Config source:** `src/config.py`
> **Single event:** Lifted Load (only hazardous event under study)

---

## 1. Object Detection

### 1.1 Models

| Role | Model | Notes |
|---|---|---|
| Zero-shot (Path A) | Grounding DINO (`IDEA-Research/grounding-dino-base`) | Open-vocabulary, no training. HuggingFace transformers 5.x. |
| Fine-tuned (Path B) | YOLO26-N (`yolo26n.pt`) | Ultralytics YOLO26 Nano. NMS-free, optimised for edge/low-power. Pre-trained on COCO, fine-tuned on our labelled frames. |
| Framework | PyTorch nightly cu130 on RTX 5090 (Blackwell sm_120) | Required for Blackwell support. |

### 1.2 Detection Thresholds (Grounding DINO)

| Parameter | Config key | Value | Rationale |
|---|---|---|---|
| Box confidence (targets) | `BOX_CONFIDENCE` | 0.30 | Standard operating point for well-represented classes (person/worker). |
| Text threshold (targets) | `TEXT_THRESHOLD` | 0.25 | Balances precision/recall for person detection. |
| Box confidence (hazards) | `LIFTED_LOAD_BOX_CONFIDENCE` | 0.20 | Hoists, concrete buckets score lower (0.20-0.53). Lowered for discovery; the spatial rule applies a secondary confidence filter (see Section 2.2). |
| Text threshold (hazards) | `LIFTED_LOAD_TEXT_THRESHOLD` | 0.15 | Same reasoning. |

**Calibration history:**
- Initial: box=0.3, text=0.25 for both. Lifted-load payloads missed entirely.
- Tested on real footage: `chain hoist` (0.35-0.53), `concrete bucket` (0.28-0.46), `concrete skip` (0.23-0.45). Lowered to 0.20/0.15.
- Phantoms handled by spatial rule filters (Section 2.2).

### 1.3 Text Prompts (Grounding DINO)

| Role | Prompt |
|---|---|
| Target (workers) | `person . worker . construction worker` |
| Hazard (loads) | `chain hoist . concrete bucket . concrete skip . lifted container . hanging bucket . steel beam` |

**Key decision:** The hazard prompt targets the **payload and rigging**, not the crane itself. Earlier prompts (`suspended load . crane hook`) detected crane structures, producing systematic false positives.

### 1.4 YOLO26 Classes (Fine-tuned)

| Class ID | Name | Notes |
|---|---|---|
| 0 | `worker` | Any person on site |
| 1 | `suspended_load` | Concrete buckets, chain hoists, steel beams — specifically when hanging from a crane |

---

## 2. Spatial Rule: Lifted Load

### 2.1 Design Rationale

The central challenge is **perspective projection**: in a fixed CCTV view, a ground-level object far from the camera can appear at the same image y-coordinate as a nearby elevated object. Naive 2D filters fail because they conflate image-space y-position with real-world elevation.

Our approach uses a **strict cascade of five filters** designed to be perspective-safe.

### 2.2 Filter Cascade

| # | Filter | Config key | Value | What it rejects | Logic |
|---|---|---|---|---|---|
| 1 | **Confidence** | `LOAD_MIN_HAZARD_SCORE` | 0.30 | Low-confidence phantom detections from the relaxed threshold (0.20). | `hazard.score >= 0.30` |
| 2 | **Max height** | `LOAD_MAX_HEIGHT_RATIO` | 0.35 | Oversized boxes spanning the crane structure. | `box_height / frame_height < 0.35` |
| 3 | **Min area** | `LOAD_MIN_AREA` | 0.004 | Tiny phantom boxes (< 0.4% of frame area). | `box_width * box_height >= 0.004` |
| 4 | **Suspension** | *(hard-coded)* | load bottom < worker top | Objects whose bottom edge is at or below workers' heads. Only passes when the load **visually floats above** the worker. | `hazard.y2 < target.y1` |
| 5 | **Proximity** | `LOAD_PROXIMITY_THRESHOLD` | 0.40 | Workers too far from the load to be endangered. Generous because a swinging load's danger cone extends beyond its vertical projection. | `centroid_distance(hazard, target) <= 0.40` |

### 2.3 Filters Considered and Rejected

| Filter | Why rejected |
|---|---|
| **Absolute elevation cutoff** | Failed on real footage — perspective foreshortening. |
| **Load centroid above worker centroid** | Too lenient — background objects naturally appear "higher" in the image. |
| **Load centroid above worker head** | Failed: distant suspended load's centroid projects below nearby worker's head. |
| **Ground rejection by foot_y comparison** | Unreliable across depths without depth information. |
| **Strict horizontal overlap** | Too strict for the fall-zone definition (OSHA 29 CFR 1926.1425). |

### 2.4 Calibration History

1. **V1:** Detected crane structures as hazards (wrong prompt). All videos flagged positive.
2. **V2:** Absolute elevation cutoff + above-head centroid. Rejected real suspended loads at mid-frame.
3. **V3:** Per-pair ground rejection + load-top-above-worker-centroid. Still let through excavator buckets.
4. **V4 (current):** 5-filter cascade. Correctly classifies all 6 test videos (2 real TP, 4 synthetic TN).

### 2.5 Known Limitations

- The suspension check (load bottom < worker top) sacrifices recall for perspective safety.
- Depth estimation (Depth Anything V2) could resolve edge cases but is not yet integrated.
- The prompt set may match excavator buckets in some views. Confidence + area filters mitigate this.

---

## 3. Video-Level Aggregation

| Parameter | Config key | Value | Rationale |
|---|---|---|---|
| Min violation frames | `MIN_VIOLATION_FRAMES` | 2 | Temporal consistency — single frames may be transient artefacts. |
| Violation ratio | `VIOLATION_RATIO` | 0.20 | At least 20% of frames show the violation. |
| Aggregation logic | — | `frames >= 2 OR ratio >= 0.20` | **OR** (recall-friendly, aligned with F2). |

---

## 4. Frame Extraction

| Parameter | Config key | Value | Rationale |
|---|---|---|---|
| Sample rate | `SAMPLE_FPS` | 1 fps | Construction activity is slow-moving. 1 fps captures all meaningful state changes. |

---

## 5. Evaluation Metrics

| Metric | Role | Notes |
|---|---|---|
| **F2 score** | Primary | Recall weighted 4x over precision. Missing a real violation is worse than a false alarm. |
| F1, Precision, Recall | Secondary | Reported for completeness. |
| Bootstrap 95% CI | Uncertainty | Resampling-based confidence interval on F2. |

---

## 6. Current Results (O0, 6 videos)

| Event | N | F2 | P | R | TP | FP | FN | TN |
|---|---|---|---|---|---|---|---|---|
| Lifted load | 6 | 1.000 | 1.000 | 1.000 | 2 | 0 | 0 | 4 |

**Dataset:** 2 real videos (LL positive), 4 synthetic Veo 3.1 videos (LL negative).

> Small validation set. Confirms pipeline is functional but not publishable
> as-is. Needs a larger, more diverse dataset.

---

## 7. Experimental Design

All 4 experiments evaluate **lifted_load only**.

| Experiment | Detection | Training data | Tests on | Question |
|---|---|---|---|---|
| **Exp 1** — Zero-shot baseline | Grounding DINO | None | O0–O3 | How much does obfuscation hurt out-of-the-box detection? |
| **Exp 2** — Fine-tuned by source | YOLO26-N | Real / Synthetic / Mixed | Real (O0) | Does synthetic data improve detection? |
| **Exp 3** — Privacy-utility tradeoff | YOLO26-N | Mixed (O0) | O0–O3 | How does performance degrade per obfuscation level? |
| **Exp 4** — Obfuscation-aware training | YOLO26-N | Obfuscated synthetic | Matching obfuscation real | Can training on obfuscated data recover lost performance? |
