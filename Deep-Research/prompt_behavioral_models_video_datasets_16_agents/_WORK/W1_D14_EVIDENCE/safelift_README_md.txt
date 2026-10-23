[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]
<a href="https://zenodo.org/records/18243098"><img src="https://img.shields.io/badge/Dataset-Zenodo-darkgreen"/></a>
<a href="pdf/paper.pdf"><img src="https://img.shields.io/badge/Paper-PDF-blue"/></a>
<!-- <a href="pdf/poster.pdf"><img src="https://img.shields.io/badge/Poster-PDF-red"/></a> -->

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

# 🏋️ SAFELIFT: Safety-Aware Feedback for Ergonomic Lifting & Injury-Free Tasks

This repository contains the official implementation of our paper **"SAFELIFT: Safety-Aware Feedback for Ergonomic Lifting & Injury-Free Tasks"**, a system designed to assess and improve lifting posture using ergonomic principles and computer vision.

> ✅ **Tested with Python 3.11**  
> ⚠️ Can be adapted to other Python versions with minor changes (modifications are up to the user)

<div style="text-align:center"><img src="media/A. CARRIOLA-TERRA LAT 3.gif" width="300" alt=""></div>

---
## 📦 Dataset

- The dataset has undergone a privacy and ethics review and was approved by TU Delft institutional review board.
- The dataset is published on [ZENODO](https://zenodo.org/records/18243098).
- After downloading, place all dataset archives inside the `archives_data/` folder and extract them in place. After extraction, the folder structure should look like this:
```
└── archives_data/
    ├── annotations.json                
    │
    └── anonymized/
        ├── video_env_1_anonymized/            
        │   ├── xx_0013.mp4
        │   ├── xy_0017.mp4
        │   └── ...
        │
        ├── video_env_1_oblique_anonymized/    
        │   ├── xx_0020.mp4
        │   ├── xy_0013.mp4
        │   └── ...
        │
        ├── video_env_3_anonymized/            
        │   ├── zz_0006_dg.mp4
        │   ├── ff_0003_gd.mp4
        │   └── ...
        │
        └── video_env_3_oblique_anonymized/    
            ├── ...
```
---

## 📚 Background: Ergonomic Principles

Our system is grounded in the **Revised NIOSH Lifting Equation (RNLE)**, a widely accepted standard in ergonomics for evaluating lifting safety.

### Lifting Index (LI)

The **Lifting Index (LI)** is used to assess the risk associated with a lifting task:

$$
LI = \frac{\text{Load Weight}}{\text{RWL}}
$$

Where:
- **Load Weight** is the actual weight lifted.
- **RWL** is the **Recommended Weight Limit**, a value that varies depending on posture.

### Recommended Weight Limit (RWL)

RWL is calculated as:

```
RWL = LC × HM × VM × DM × AM × FM × CM
```

Each multiplier adjusts the baseline weight limit (LC) according to posture.

### RWL Multipliers

| Symbol | Multiplier Description | Formula or Source |
|--------|-------------------------|-------------------|
| `LC`   | Load Constant – the maximum recommended weight under ideal conditions | Based on age and gender (see below) |
| `HM`   | Horizontal Multiplier – based on hand distance from ankles | $$\frac{25}{H}$$ |
| `VM`   | Vertical Multiplier – based on hand height from the floor | $$1 - (0.003 \times \left\lvert V - 75 \right\lvert)$$ |
| `DM`   | Distance Multiplier – based on hand vertical travel distance | $$0.82 + \frac{4.5}{D}$$ |
| `AM`   | Asymmetric Multiplier – based on torso rotation angle | $$1 - (0.0032 \times A)$$ |
| `FM`   | Frequency Multiplier – based on number of lifts per minute | See Table 5 - Chapter 3 in [RNLE guide](https://www.cdc.gov/niosh/docs/94-110/) |
| `CM`   | Coupling Multiplier – based on grip quality |  See Table 7 - Chapter 3 in [RNLE guide](https://www.cdc.gov/niosh/docs/94-110/) |

Where:
- `H` is horizontal reach (cm)
- `V` is vertical height (cm)
- `D` is vertical distance traveled (cm)
- `A` is asymmetry angle (degrees)


#### 🔢 Load Constant (LC)

From the [RNLE guide](https://www.cdc.gov/niosh/docs/94-110/), the default Load Constant is **23 kg**.  
However, we adopt the approach from [ISO 11228](https://www.iso.org/standard/76820.html), which introduces personalization based on the subject’s **age** and **gender**:

```python
if gender == "M":
    LC = 25 if 20 <= age <= 45 else 20
elif gender == "W":
    LC = 20 if 20 <= age <= 45 else 15
```

---
## 📢 Recommendations

Our system provides **visual** and **textual** lifting posture recommendations aimed at reducing the Lifting Index (**LI**) below a safety threshold.

### 🔍 How It Works

* The system analyzes two key frames of the lifting motion: the **start** and **end** of the lift.
* For each frame, it computes three posture-dependent parameters:

  * `H`: horizontal distance of the hands from the ankles  
  * `V`: vertical height of the hands from the floor  
  * `D`: vertical travel distance between the start and end points  

By gradually adjusting the **hand position** — the main factor influencing the LI — the system identifies posture corrections that reduce LI below a configurable threshold (`τ = 0.7` for evaluation, assuming a 10 kg load).

### 🧠 Graphical Recommendation

When the hands move, **surrounding joints** such as the shoulders, elbows, and hips are also displaced **proportionally** to maintain anatomical plausibility.

<figure style="text-align:center">
  <img src="media/overlap_poses.jpg" alt="Overlay of original and recommended poses">
  <figcaption>Overlay of start and end poses (original vs. recommended).</figcaption>
</figure>

To create smooth transitions, intermediate poses are generated using **linear interpolation** between key poses:

$$
\text{pose}_{\alpha} = (1 - \alpha_k)\,\text{pose}_1 + \alpha_k\,\text{pose}_2,\quad \alpha_k \in [0, 1]
$$

where \( k \) indexes the interpolation step. This produces **smooth**, **kinematically coherent** animations.

We generate two types of animations:
- **Correction animation** – shows the transition from the original to the recommended posture at each key moment.  
- **Movement animation** – depicts the full lifting motion for both the original and recommended poses.

<div style="display:flex; gap:16px; align-items:flex-start">
  <figure style="flex:1; text-align:center">
    <img src="media/gif_correction.gif" alt="Correction animation">
    <figcaption>Animation: correction per key moment.</figcaption>
  </figure>
  <figure style="flex:1; text-align:center">
    <img src="media/gif_movement.gif" alt="Movement animation">
    <figcaption>Animation: full movement (original vs. recommended).</figcaption>
  </figure>
</div>

### 📝 Textual Recommendation

Following the [RNLE guide](https://www.cdc.gov/niosh/docs/94-110/) guide’s case study examples, we generate textual feedback by comparing joint positions between the original and adjusted poses.
A **rule-based approach** produces clear, body-part-specific instructions:

* If the hands move, a corresponding description of that displacement is generated.  
* If nearby joints (shoulders, elbows, hips) move proportionally, these are also mentioned.  
* For the knees, the system reports changes in flexion angles between the original and adjusted poses.

This structured feedback helps users understand **what to change** and **how those changes affect** their overall posture.

```text
Lifting Index (Original Pose): 1.03
Lifting Index (Recommended Pose): 0.67

At the start of the lift:
• Move your hands at least 14 cm closer to your body.
• This adjustment will also move your shoulders (6 cm) and elbows (11 cm) closer.
• You should actively shift your hips approximately 4–8 cm in the same direction.
• This posture change leads to a decrease in knee flexion of about 3.5°.

At the end of the lift:
• Move your hands at least 29 cm up.
• This adjustment will also move your shoulders (12 cm) and elbows (23 cm) up.
• You should actively shift your hips approximately 10–14 cm in the same direction.
• This posture change leads to an increase in knee flexion of about 8.6°.
```

---

## 📊 Evaluation
We conducted a multi-method evaluation of the system, combining technical, expert, and lay-user studies to assess performance, usability, and interpretability.

For detailed results, statistical analyses, and discussion, see our paper.

### Technical Validation
A custom lifting dataset was collected in 4 real-world environments (lab, office, classroom, and outdoor vineyard).
Each video includes annotated lifting actions with physical measurements for RNLE (Revised NIOSH Lifting Equation) parameters.

### Expert Evaluation
Participants: 11 ergonomics and occupational health professionals (6 retained for full analysis based on completion timestamps and on an attention-check question, which is set to appear in a shuffled position for 33% of each participant’s samples).
Average completion time: 44 minutes per expert, covering four feedback formats and a preference section. Each format was evaluated using a different video sample.

**Tested feedback formats:**

1. Textual recommendation
2. Static graphical overlay
3. Animated correction (key moments)
4. Animated movement (continuous)

<details>
<summary> <b>Expert Evaluation Interface</b></summary>

The source code for this interface is available in the [`web_app_experts`](web_app_experts) directory.

<figure style="text-align:center">
<img src="media/expert1.png" alt="expert1">
<figcaption>Expert Evaluation Interface, part 1.</figcaption>
</figure>

<figure style="text-align:center">
<img src="media/expert2.png" alt="expert2">
<figcaption>Expert Evaluation Interface, part 2.</figcaption>
</figure>

<figure style="text-align:center">
<img src="media/expert3.png" alt="expert3">
<figcaption>Expert Evaluation Interface, part 3.</figcaption>
</figure>  

<figure style="text-align:center">
<img src="media/expert4.png" alt="expert4">
<figcaption>AnExpert Evaluation Interface, part 4.</figcaption>
</figure>  

<figure style="text-align:center">
<img src="media/expert5.png" alt="expert5">
<figcaption>Expert Evaluation Interface, part 5.</figcaption>
</figure>  

</details>

### Lay-User Study

**Participants:** 32 lay users (22–42 yrs).

Compared formats:

* **Animation + Text**
* **Image + Text**

<details>
<summary> <b>Layperson Evaluation Interface</b></summary>

The source code for this interface is available in the [`web_app_laypeople`](web_app_laypeople) directory.

<figure style="text-align:center">
<img src="media/layperson1.png" alt="layperson1">
<figcaption>Layperson Evaluation Interface, part 1.</figcaption>
</figure>
<figure style="text-align:center">
<img src="media/layperson2.png" alt="layperson2">
<figcaption>Layperson Evaluation Interface, part 2.</figcaption>
</figure>
<figure style="text-align:center">
<img src="media/layperson3.png" alt="layperson3">
<figcaption>Layperson Evaluation Interface, part 3.</figcaption>
</figure>  
<figure style="text-align:center">
<img src="media/layperson4.png" alt="layperson4">
<figcaption>Layperson Evaluation Interface, part 4.</figcaption>
</figure>  
</details>

---

## Human Inclusion and Ethics
All procedures involving human participants were conducted in accordance with the ethical and privacy regulations of our institutions. During the data collection phases, we underwent formal ethical review and approval processes to ensure compliance with institutional and legal requirements. Each participant provided informed consent prior to participation, acknowledging the purpose, procedures, and use of their data.

For the expert evaluation phase, additional ethical clearance was obtained, and a compensation of €30 per participant was provided through Amazon voucher. This evaluation adhered to the same standards of transparency, confidentiality, and voluntary participation as the earlier data collection stage.

Both experts and lay participants provided informed consent before taking part in the evaluation. No personally identifiable information or signed consent forms were collected, as the study was conducted anonymously.

---

## ⚙️ Installation

### 1. Clone the repository:

```bash
git clone https://github.com/GaetanoDibenedetto/IUI26.git
```

### 2. Install dependencies

This project relies on [ViTPose](https://github.com/JunkyByte/easy_ViTPose.git) and [Ultralytics YOLO](https://github.com/ultralytics). All other required packages are listed in:

📄 [`requirements-python3_11.txt`](requirements-python3_11.txt)

Install with:

```bash
pip install -r requirements-python3_11.txt
```

Run with:

```bash
python main.py --if 'path_to_video_or_folder', -o 'path_to_output_folder'
```
## 📬 Contact

For questions, issues, or collaboration opportunities, contact:

- Gaetano Dibenedetto – gaetano.dibenedetto@uniba.it
- [Personal Web Page](https://gaetanodibenedetto.github.io/) - [Linkedin](https://www.linkedin.com/in/gaetano-dibenedetto/)

## Citing Us

BibTeX format:

```
@inproceedings{Dibenedetto26IUI,
  author       = {Gaetano Dibenedetto and Pasquale Lops and Piero Lovreglio and Marco Polignano and Roberto Ravallese and Helma Torkamaan},
  title        = {SAFELIFT: Safety-Aware Feedback for Ergonomic Lifting \& Injury-Free Tasks},
  booktitle    = {Proceedings of the 31th International Conference on Intelligent User Interfaces, {IUI} 2026, Paphos, Cyprus, March 23-26, 2026},
  publisher    = {{ACM}},
  year         = {2026},
  url          = {https://doi.org/10.1145/3742413.3789143},
  doi          = {10.1145/3742413.3789143}
}
```


ACM Reference Format:
```
Gaetano Dibenedetto, Pasquale Lops, Piero Lovreglio, Marco Polignano, Roberto Ravallese, and Helma Torkamaan. 2026. SAFELIFT: Safety-Aware Feedback for Ergonomic Lifting & Injury-Free Tasks. In 31st International Conference on Intelligent User Interfaces (IUI ’26), March 23–26, 2026, Paphos, Cyprus. ACM, New York, NY, USA, 16 pages. https://doi.org/10.1145/3742413.3789143
```
