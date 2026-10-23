# Suspended-Load Hazard Detection — Results Analysis

**Dataset:** ACM MM 2026 synthetic video corpus
**Date:** 2026-04-01
**Videos:** 227 (115 True Positive / 112 False Positive)
**Generators:** Veo 3.1 (124), Wan 2.2-14b (77), Wan 2.6 (20), Sora-2-Pro (6)
**Labeling:** Human-resolved labels from 2–3 reviewers; Tier 1 = unanimous (150), Tier 2 = majority vote (77)

---

## 1. Overall Results

| Metric | YOLO World | Grounding DINO |
|--------|:---:|:---:|
| **F2 (primary)** | **0.812** [0.753, 0.864] | 0.372 [0.283, 0.462] |
| F1 | 0.729 | 0.458 |
| Precision | 0.624 | 0.745 |
| Recall | 0.878 | 0.330 |
| Specificity | 0.455 | 0.884 |
| TP / FP / FN / TN | 101 / 61 / 14 / 51 | 38 / 13 / 77 / 99 |

**YOLO World is the clear winner on F2**, driven by much higher recall (87.8% vs 33.0%).
Grounding DINO has higher precision (74.5%) but misses 67% of actual hazards.

---

## 2. Per-Tier Breakdown

### YOLO World

| Tier | N | F2 [95% CI] | P | R | TP | FP | FN | TN |
|------|---|---|---|---|---|---|---|---|
| 1 (unanimous) | 150 | 0.815 [0.745, 0.874] | 0.653 | 0.868 | 66 | 35 | 10 | 39 |
| 2 (majority) | 77 | 0.806 [0.711, 0.884] | 0.574 | 0.897 | 35 | 26 | 4 | 12 |

### Grounding DINO

| Tier | N | F2 [95% CI] | P | R | TP | FP | FN | TN |
|------|---|---|---|---|---|---|---|---|
| 1 (unanimous) | 150 | 0.428 [0.317, 0.541] | 0.829 | 0.382 | 29 | 6 | 47 | 68 |
| 2 (majority) | 77 | 0.262 [0.128, 0.411] | 0.562 | 0.231 | 9 | 7 | 30 | 31 |

**Observations:**
- YOLO World is remarkably stable across tiers (F2 ~0.81 for both).
- Grounding DINO degrades significantly on Tier 2 (F2 drops from 0.43 to 0.26). Tier 2 videos required a third labeler to break ties, suggesting they depict more ambiguous or visually challenging scenes — exactly where Grounding DINO's rigid spatial rules fail.
- YOLO World's recall is actually *higher* on Tier 2 (0.897 vs 0.868), suggesting its temporal smoothing and physics-based hazard zones handle ambiguous cases better.

---

## 3. Per-Generator Breakdown

### YOLO World

| Generator | N | F2 | P | R | TP | FP | FN | TN |
|-----------|---|---|---|---|---|---|---|---|
| Sora-2-Pro | 6 | 0.938 | 0.750 | 1.000 | 3 | 1 | 0 | 2 |
| Veo 3.1 | 124 | 0.857 | 0.664 | 0.924 | 73 | 37 | 6 | 8 |
| Wan 2.6 | 20 | 0.769 | 0.769 | 0.769 | 10 | 3 | 3 | 4 |
| Wan 2.2-14b | 77 | 0.652 | 0.429 | 0.750 | 15 | 20 | 5 | 37 |

### Grounding DINO

| Generator | N | F2 | P | R | TP | FP | FN | TN |
|-----------|---|---|---|---|---|---|---|---|
| Sora-2-Pro | 6 | 0.625 | 0.500 | 0.667 | 2 | 2 | 1 | 1 |
| Veo 3.1 | 124 | 0.388 | 0.844 | 0.342 | 27 | 5 | 52 | 40 |
| Wan 2.6 | 20 | 0.351 | 0.800 | 0.308 | 4 | 1 | 9 | 6 |
| Wan 2.2-14b | 77 | 0.278 | 0.500 | 0.250 | 5 | 5 | 15 | 52 |

**Observations:**
- YOLO World performs best on Veo 3.1 (F2=0.857) and worst on Wan 2.2-14b (F2=0.652). Wan 2.2-14b has both the worst precision (0.429, 20 FP out of 57 negatives) and lowest recall.
- Grounding DINO's recall is catastrophically low across all generators (23–34%), with the worst on Wan 2.2-14b (25%).
- Veo 3.1 is problematic for YOLO World's FP rate: 37 of 45 negative Veo 3.1 videos are false positives (82%). Veo 3.1 appears to generate visually convincing scenes where objects are misidentified as suspended loads.

---

## 4. Model Agreement & Disagreement

| Category | Count | Description |
|----------|------:|-------------|
| Both correct | 83 | Models agree and are right |
| Both wrong | 21 | Neither model gets it right |
| YOLO World only correct | 69 | YOLO World catches what GD misses |
| Grounding DINO only correct | 54 | GD avoids FPs that YOLO World makes |

The 21 videos where **both models fail** split into two patterns:

1. **Both predict SAFE on a True Positive (14 videos):** These include veo3.1_0091–0093, veo3.1_0100, wan2.6_0011/0012/0016, wan2.2-14b_0005/0013/0041/0044. Both models detect 0% hazard frames — the hazard is likely not visually represented in a way that either detector can recognise (e.g., the "load" may not look like a typical hoisted load, or no worker is nearby).

2. **Both predict UNSAFE on a False Positive (7 videos):** These include sora-2-pro_0002, veo3.1_0019/0025/0076/0113/0124, wan2.2-14b_0055/0068. High hazard frame percentages from both models suggest these videos genuinely *look like* hazard scenarios — they may be labeling edge cases or the video content is borderline. The fact that both independent detection approaches agree these look hazardous may warrant re-examining the labels.

---

## 5. Error Analysis

### YOLO World's Weakness: False Positives (61 FP)

YOLO World's primary failure mode is over-detection. The physics-based trapezoidal hazard zone, combined with temporal smoothing that latches once triggered, creates a recall-friendly but FP-prone system.

**Key FP patterns:**
- **Veo 3.1 negatives:** 37 of 45 negative Veo 3.1 videos are flagged as UNSAFE (82% FP rate). Veo 3.1 generates photorealistic construction scenes where objects (concrete structures, equipment parts) are confidently detected as `"hoisted load with crane hook"`.
- **Wan 2.2-14b negatives:** 20 of 57 flagged as UNSAFE (35% FP rate). Lower than Veo 3.1, likely because Wan 2.2 generates less photorealistic scenes where object detections are less confident.

**Possible mitigations (not applied):**
- Raise `YOLO_CONF` from 0.30 to 0.40–0.50 — would reduce FPs but may hurt recall.
- Add a secondary confidence gate (like Grounding DINO's `LOAD_MIN_HAZARD_SCORE = 0.30`).
- Require the load class specifically (`"hoisted load with crane hook"`) to exceed a higher threshold than the general 0.30.
- Shorten the temporal latching — once UNSAFE is triggered, it's permanent for the clip. A decay or re-evaluation could reduce FPs from brief false detections.

### Grounding DINO's Weakness: False Negatives (77 FN)

Grounding DINO misses 67% of true hazards. This is driven by:

1. **1 FPS sampling:** Processing at 1 frame/second means a ~10s clip yields only ~8–10 frames. A hazard may only be visible in a subset of frames, and sampling may miss the critical moments entirely.

2. **Strict spatial cascade:** The 5-stage filter is designed for precision, not recall:
   - Stage 4 (suspension check: load bottom must be *above* worker top) is very strict — in many camera angles, the load may overlap vertically with workers without the bottom edge being strictly above the head.
   - Stage 5 (proximity < 0.40 normalized) may reject valid hazards in wide-angle shots where both worker and load appear small.

3. **Text prompt mismatch:** The hazard prompt (`"chain hoist . concrete bucket . concrete skip . lifted container . hanging bucket . steel beam"`) is specific to certain load types. Synthetic generators may produce loads that look different (e.g., pallets, crates, generic boxes) that don't match these prompts.

4. **No temporal reasoning:** Each frame is evaluated independently. There's no tracking, no velocity estimation, and no gap-filling. A load may be detected in some frames but not others, and the simple aggregation (OR of ≥2 frames or ≥20%) requires a minimum density of positive frames.

---

## 6. Comparison with Previous Evaluation

### Previous Dataset (55 synthetic videos, synthetic_from_synthetic)

| Metric | YOLO World (prev) | YOLO World (now) |
|--------|:---:|:---:|
| N | 55 | 227 |
| F2 | — | 0.812 |
| F1 | 0.647 | 0.729 |
| Precision | 0.537 | 0.624 |
| Recall | 0.815 | 0.878 |
| TP / FP / FN / TN | 22 / 19 / 5 / 9 | 101 / 61 / 14 / 51 |

### Previous Dataset (6 real videos, Path A zero-shot)

| Metric | Grounding DINO (prev) | Grounding DINO (now) |
|--------|:---:|:---:|
| N | 6 | 227 |
| F2 | 1.000 | 0.372 |
| Precision | 1.000 | 0.745 |
| Recall | 1.000 | 0.330 |

**Key takeaway:** Grounding DINO's perfect performance on the original 6-video set was a severe overfitting artifact of an extremely small and easy dataset. On a 227-video corpus with diverse generators and challenging edge cases, its recall collapses to 33%. YOLO World actually *improved* on the larger dataset (F1 from 0.647 to 0.729), suggesting its approach generalizes better.

---

## 7. Design Decisions & Considerations

### Why F2 as primary metric
F2 weights recall twice as heavily as precision. For safety applications, missing a hazard (FN) is more dangerous than a false alarm (FP). A false alarm wastes inspection time; a missed hazard can result in injury or death.

### YOLO World pipeline design
- **Every-frame processing:** Unlike Grounding DINO's 1 FPS sampling, YOLO World processes all frames. This gives much denser temporal signal for the sliding window / gap-filling logic.
- **ByteTrack:** Persistent IDs enable velocity estimation and temporal continuity.
- **Physics-based hazard zone:** The trapezoidal zone grows with load height, accounting for lateral displacement during freefall. This is more principled than a fixed proximity threshold.
- **Temporal latching:** Once UNSAFE, stays UNSAFE for the clip. Appropriate for short clips (~10s) in a safety context — conservative by design.
- **Trade-off:** This design inherently favors recall over precision, which is why we see 87.8% recall but only 62.4% precision.

### Grounding DINO pipeline design
- **Text-guided zero-shot:** No training data needed. Detects objects described by natural language prompts.
- **5-stage spatial cascade:** Precision-oriented — each filter removes a class of false positives.
- **1 FPS sampling:** Dramatically reduces compute but sacrifices temporal resolution.
- **Trade-off:** High precision (74.5%) but recall is too low (33.0%) for a safety-critical application.

### Why the gap is so large
The fundamental architectural difference is **temporal reasoning**. YOLO World tracks objects across frames, estimates velocity, builds physics-based zones, and uses a sliding window with gap-filling. Grounding DINO treats each sampled frame independently. On a diverse synthetic dataset where hazards may be brief, visually ambiguous, or present only in certain frames, temporal reasoning is critical.

### Tier 2 interpretation
Tier 2 videos required a third labeler, meaning the first two disagreed. These are inherently ambiguous. YOLO World's stability across tiers (F2 ~0.81 for both) suggests it isn't thrown off by visual ambiguity. Grounding DINO's steep drop on Tier 2 (F2 from 0.43 to 0.26) confirms its rigid rules struggle with edge cases.

### Videos both models get wrong
The 14 true positives that both models miss (0% hazard frames from both) likely represent videos where the hazard is not visually detectable by either approach — the "load" may not resemble any trained/prompted load class, or the spatial relationship isn't captured in any sampled frame. These warrant manual inspection.

The 7 false positives that both models flag with high confidence may be labeling errors or genuinely borderline cases where the visual content is indistinguishable from a real hazard. Cross-referencing with the original labeler disagreements (Tier) could clarify.

---

## 8. Files Produced

| File | Description |
|------|-------------|
| `results_yolo_world_20260401_183730.csv` | Per-video YOLO World results (227 rows) |
| `results_grounding_dino_20260401_184439.csv` | Per-video Grounding DINO results (227 rows) |
| `confusion_matrix_yolo_world_20260401_183730.csv` | YOLO World confusion matrix (overall + per-tier) |
| `confusion_matrix_grounding_dino_20260401_184439.csv` | Grounding DINO confusion matrix (overall + per-tier) |
| `evaluate.py` | Self-contained evaluation script (supports `--model yolo_world/grounding_dino/both`, `--annotate`) |
| `ANALYSIS.md` | This file |

---

## 9. Reproducibility

```bash
# Activate environment
source .venv/bin/activate

# Run both models
python evaluate.py --model both

# Run individual models
python evaluate.py --model yolo_world
python evaluate.py --model grounding_dino

# Generate annotated output videos (YOLO World only, not yet implemented)
python evaluate.py --model yolo_world --annotate
```

All parameters are hardcoded in `evaluate.py` and match the original SafetyPrivacyPaper pipelines exactly. No configuration files are needed.
