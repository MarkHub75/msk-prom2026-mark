---
license: other
license_name: govtech-singapore
license_link: LICENSE
language:
- en
tags:
- video
- safety
- construction
- synthetic
- benchmark
- computer-vision
---

# SynthSite

**SynthSite** is a curated benchmark of **227 synthetic construction site safety videos** (115 unsafe, 112 safe) generated using four text-to-video models: `Sora 2 Pro`, `Veo 3.1`, `Wan 2.2-14B`, and `Wan 2.6`. Each video was independently labeled by **2–3 human reviewers** for the presence of a **Worker Under Suspended Load** hazard, producing a binary classification: **unsafe** (`True_Positive` — worker remains in the suspended-load fall zone) or **safe** (`False_Positive` — no worker in fall zone or load not truly suspended).

All content is fully AI-generated — no real people or real incidents are depicted. The terms "lifted load" and "suspended load" are used interchangeably throughout this repo.

<!-- Paper link: TODO — update once preprint is available -->

---

## Sample Frames

Each video is a short clip (5–10 seconds, 1280×720, 16–30 FPS). Frames below are sampled from unsafe and safe videos.

### Unsafe — Worker Under Suspended Load

<table>
  <tr>
    <td align="center"><img src="assets/tp_sora_site.png" width="220"/></td>
    <td align="center"><img src="assets/tp_sora_steel.png" width="220"/></td>
    <td align="center"><img src="assets/tp_veo_night.png" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><img src="assets/tp_veo_rain.png" width="220"/></td>
    <td align="center"><img src="assets/tp_wan22_pipe.png" width="220"/></td>
    <td align="center"><img src="assets/tp_wan26_rebar.png" width="220"/></td>
  </tr>
</table>

### Safe — No Hazard Present

<table>
  <tr>
    <td align="center"><img src="assets/fp_sora_site.png" width="220"/></td>
    <td align="center"><img src="assets/fp_veo_day.png" width="220"/></td>
    <td align="center"><img src="assets/fp_veo_sunset.png" width="220"/></td>
  </tr>
  <tr>
    <td align="center"><img src="assets/fp_veo_night.png" width="220"/></td>
    <td align="center"><img src="assets/fp_wan22_quiet.png" width="220"/></td>
    <td align="center"><img src="assets/fp_wan26_tunnel.png" width="220"/></td>
  </tr>
</table>

---

## Generation

Videos were generated from four models:

| Model | Provider | Model License | Output Rights | Videos |
|-------|----------|---------------|---------------|--------|
| `Sora 2 Pro` | OpenAI | Proprietary (API ToS) | Assigned to user | 6 |
| `Veo 3.1` | Google | Proprietary (API ToS) | Not claimed by Google | 124 |
| `Wan 2.2-14B` | Alibaba / Wan-AI | Apache 2.0 | Not claimed by creators | 77 |
| `Wan 2.6` | Alibaba / Wan-AI | Apache 2.0 | Not claimed by creators | 20 |

All four models either assign output rights to the user or explicitly disclaim ownership of generated content, permitting redistribution under this dataset's license. The terms of service for each model were reviewed and confirmed to be compatible with open dataset release for academic and research use.

No real video footage is included. The generation process used text intermediaries that sufficiently abstract away details from any source material, preventing re-identification. Provenance metadata (C2PA for Sora, SynthID for Veo) has been preserved.

From an initial pool of **487** candidates, each video was manually screened before hazard annotation. Videos were excluded if they contained synthesis failures that prevented reliable hazard judgment — including severe artifacts, missing or fused workers/loads/machinery, abrupt appearance or disappearance of key entities, or major temporal corruption. Minor imperfections that did not hinder hazard interpretation (e.g., mild geometric distortion, low resolution, or corrupted text overlays) were retained. **227 videos (47%)** passed screening and form the final benchmark.

### Gemini 2.5 Flash Evaluation

Each video was assessed using a rubric-guided Gemini 2.5 Flash pipeline with schema-constrained structured outputs, characterizing diversity, complexity, and realism. The evaluation script, rubric, and per-video results are in `code/gemini_synthsite_eval.py` and `results/gemini_synthsite_eval/`.

### VBench Statistics

Scores are normalized to [0, 1], with higher values indicating better temporal stability.

| Metric | Mean | Median | Std |
|---|---|---|---|
| Subject consistency | 0.9770 | 0.9826 | 0.0191 |
| Background consistency | 0.9701 | 0.9769 | 0.0191 |
| Motion smoothness | 0.9952 | 0.9962 | 0.0024 |
| Temporal flickering | 0.9903 | 0.9935 | 0.0127 |

---

## Inter-Annotator Agreement

| Scope | Videos | Weighted Avg Cohen's Kappa | Krippendorff's Alpha |
|-------|--------|---------------------------|----------------------|
| Global | 227 | 0.20 | 0.42 |
| Tier 1 | 150 | 1.00 | 1.00 |
| Tier 2 | 77 | -0.24 | -0.33 |

The low global Kappa (0.20) is expected — it is driven by the intentionally-included ambiguous Tier 2 videos. Tier 1 achieves perfect agreement (1.00), while Tier 2 is below chance, confirming these videos are genuinely ambiguous for human reviewers. Pairwise metrics available in `results/annotators_agreement/cohens_kappa.csv`.

---

## Tier System

Videos are assigned to tiers based on inter-annotator agreement:

| Tier | Condition | Count | Interpretation |
|------|-----------|-------|----------------|
| Tier 1 | All reviewers agree | **150** (66%) | High-confidence ground truth |
| Tier 2 | Reviewers disagree | **77** (34%) | Ambiguous — genuine disagreement |

Systems can be scored primarily on Tier 1 (reliable ground truth), with Tier 2 performance reported separately as the hard set.

---

## Dataset Structure

```
SynthSite/
├── LICENSE
├── README.md
├── synthetic_video_labels.csv
├── assets/                          — Sample frame images for README
├── videos/
│   └── *.mp4 (227 files)
├── results/
│   ├── annotators_agreement/
│   │   ├── cohens_kappa.csv
│   │   ├── krippendorffs_alpha.csv
│   │   └── summary.csv
│   ├── detector_outcome/
│   │   ├── confusion_matrix_grounding_dino.csv
│   │   ├── confusion_matrix_yolo_world.csv
│   │   ├── results_grounding_dino.csv
│   │   └── results_yolo_world.csv
│   ├── gemini_synthsite_eval/
│   │   └── *.json (227 files — Gemini 2.5 Flash per-video assessments)
│   └── vbench_eval/
│       ├── synthsite_eval_results.json
│       └── synthsite_scores.csv
├── code/
│   ├── gemini_synthsite_eval.py     — Gemini video evaluation pipeline
│   ├── gemini_agg_analysis.py       — Aggregate Gemini outputs into tables/figures
│   └── hazard_detector_eval.py      — YOLO World + Grounding DINO evaluation
└── docs/
    ├── detection_design.md           — Technical reference on detection approach
    ├── detection_parameters.md       — Filter cascade design and calibration
    ├── detector_scores.md            — Per-tier, per-generator detection results
    └── vbench_scores.md              — VBench quality metrics for synthetic videos
```

### Fields (`synthetic_video_labels.csv`)

| Field | Type | Description |
|-------|------|-------------|
| `filename` | string | Video filename (matches file in `videos/`) |
| `num_labelers` | int | Number of reviewers (2-3) |
| `tier` | int | Agreement tier: `1` (agreement) or `2` (disagreement) |
| `resolved_label` | string | Majority-vote label: `True_Positive` or `False_Positive` |
| `labeler_N_name` | string | Anonymized reviewer ID (`Reviewer_01` through `Reviewer_08`) |
| `labeler_N_label` | string | `True_Positive` or `False_Positive` |

Columns repeat for N = 1 to 3. A 3rd reviewer is present only when the first two disagreed (tiebreaker). Empty values indicate fewer reviewers.

---

## Intended Uses

- Benchmarking computer vision systems for construction site hazard detection
- Studying the effectiveness of synthetic data for safety-critical applications
- Evaluating inter-annotator agreement on ambiguous safety scenarios
- Comparing video generation models for domain-specific content creation

## Out-of-Scope Uses

- Misrepresenting synthetic content as real incident footage
- Training systems intended to cause harm or circumvent safety measures
- Substituting for real-world safety assessments or compliance evaluations

---

## Ethics

- **No real people** appear in any video — all content is AI-generated
- **No real incidents** are depicted — scenarios are synthetic constructions
- Source material was abstracted through text intermediaries, preventing re-identification
- Generative model terms of service were reviewed and complied with
- Provenance metadata (C2PA, SynthID) preserved for transparency
- Reviewer identities have been anonymized

---

## License

This dataset is released under a custom GovTech Singapore license. See [`LICENSE`](LICENSE) for full terms.

---

## Getting Started

This repository uses **Git LFS** for large files (videos, images). To clone with all assets:

```bash
git lfs install
git clone <repo-url>
```

Without Git LFS, video and image files will be downloaded as small pointer files.
