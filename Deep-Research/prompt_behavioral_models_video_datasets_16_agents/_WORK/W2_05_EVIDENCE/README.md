---
license: cc-by-4.0
---
# Physical AI Smart Spaces Dataset

![Demo of MTMC_Tracking](./demo.gif)

## Overview
Comprehensive, annotated dataset for multi-camera tracking and 2D/3D object detection. This dataset is synthetically generated with Omniverse and Cosmos Transfer.

This dataset consists of over 280 hours of video from across nearly 1,800 cameras from indoor scenes in warehouses, hospitals, retail, and more. The dataset is time synchronized for tracking humans, forklifts, pallet trucks and Autonomous Mobile Robots (AMRs) across multiple cameras.

## Dataset Description

### Dataset Owner(s)
NVIDIA

### Dataset Creation Date
We started to create this dataset in December, 2023. First version was completed and released as part of 8th AI City Challenge in conjunction with CVPR 2024.

### Dataset Characterization
- Data Collection Method: Synthetic
- Labeling Method: Automatic with IsaacSim

### Video Format
- Video Standard: MP4 (H.264)
- Video Resolution: 1080p
- Video Frame rate: 30 FPS

### Ground Truth Format (MOTChallenge) for `MTMC_Tracking_2024`
Annotations are provided in the following text format per line:

```
<camera_id> <obj_id> <frame_id> <xmin> <ymin> <width> <height> <xworld> <yworld>
```

- `<camera_id>`: Numeric identifier for the camera.
- `<obj_id>`: Consistent numeric identifier for each object across cameras.
- `<frame_id>`: Frame index starting from 0.
- `<xmin> <ymin> <width> <height>`: Axis-aligned bounding box coordinates in pixels (top-left origin).
- `<xworld> <yworld>`: Global coordinates (projected bottom points of objects) based on provided camera matrices.

The video file and calibration (camera matrix and homography) are provided for each camera view.

Calibration and ground truth files in the updated 2025 JSON format are now also included for each scene. 

Notes:
- Some calibration fields—such as camera coordinates, camera directions, and scale factors—are not be available for the 2024 dataset due to original data limitations.
- Please be aware that the video identified as `scene_071/camera_0649` has encountered corruption issues. We advise you to exclude this video from your submissions.
- In the sequences ranging from scenes 071 to 080, you'll find a storage room distinct from the primary retail space. Although separate, individuals can access this area. We have ensured that these sequences are synchronized effectively, treating them as part of the same continuous space for analysis purposes.

### Directory Structure for `MTMC_Tracking_2025` and `MTMC_Tracking_2026`
- `videos/`: Video files.
- `depth_maps/`: Depth maps stored as PNG images and compressed within HDF5 files. These files are exceedingly large; you may choose to use RGB videos only if preferred.
- `ground_truth.json`: Detailed ground truth annotations (see below).
- `calibration.json`: Camera calibration and metadata.
- `map.png`: Visualization map in top-down view.

### Ground Truth Format (JSON) for `MTMC_Tracking_2025` and `MTMC_Tracking_2026`
Annotations per frame:

```json
{
  "<frame_id>": [
    {
      "object_type": "<class_name>",
      "object_id": <int>,
      "3d_location": [x, y, z],
      "3d_bounding_box_scale": [w, l, h],
      "3d_bounding_box_rotation": [pitch, roll, yaw],
      "2d_bounding_box_visible": {
        "<camera_id>": [xmin, ymin, xmax, ymax]
      }
    }
  ]
}
```

### Calibration Format (JSON) for `MTMC_Tracking_2025` and `MTMC_Tracking_2026`
Contains detailed calibration metadata per sensor:

```json
{
  "calibrationType": "cartesian",
  "sensors": [
    {
      "type": "camera",
      "id": "<sensor_id>",
      "coordinates": {"x": float, "y": float},
      "scaleFactor": float,
      "translationToGlobalCoordinates": {"x": float, "y": float},
      "attributes": [
        {"name": "fps", "value": float},
        {"name": "direction", "value": float},
        {"name": "direction3d", "value": "float,float,float"},
        {"name": "frameWidth", "value": int},
        {"name": "frameHeight", "value": int}
      ],
      "intrinsicMatrix": [[f_x, 0, c_x], [0, f_y, c_y], [0, 0, 1]],
      "extrinsicMatrix": [[3×4 matrix]],
      "cameraMatrix": [[3×4 matrix]],
      "homography": [[3×3 matrix]]
    }
  ]
}
```

### Evaluation
- **2024 Edition**: Evaluation based on 3D-location-based HOTA scores at the [2024 AI City Challenge Server](https://eval.aicitychallenge.org/aicity2024). The submission is currently disabled, as the ground truths of test set are provided with this release.
- **2025 Edition**: Evaluation based on 3D-bounding-box-based HOTA scores at the [2025 AI City Challenge Server](https://eval.aicitychallenge.org/aicity2025).
- **2026 Edition**: Evaluation based on 3D-bounding-box-based HOTA scores at the 2026 AI City Challenge Server (link to be announced).
- **Evaluation script**: An offline HOTA evaluator that reproduces the official AICity MTMC (3D-bounding-box HOTA) metric is provided in the [`spatialai-data-utils` evaluation tools](https://github.com/NVIDIA-AI-Blueprints/video-search-and-summarization/tree/develop/libs/analytics/spatialai-data-utils/tools/evaluation) — see `evaluate_aicity_mtmc.py`.

#### Scene ID Tables

<table>
<tr>
<th>MTMC_Tracking_2025</th>
<th>MTMC_Tracking_2026</th>
</tr>
<tr>
<td valign="top">

| Split | Scene ID | Scene Name     |
|-------|----------|----------------|
| Train | 0        | Warehouse_000  |
| Train | 1        | Warehouse_001  |
| Train | 2        | Warehouse_002  |
| Train | 3        | Warehouse_003  |
| Train | 4        | Warehouse_004  |
| Train | 5        | Warehouse_005  |
| Train | 6        | Warehouse_006  |
| Train | 7        | Warehouse_007  |
| Train | 8        | Warehouse_008  |
| Train | 9        | Warehouse_009  |
| Train | 10       | Warehouse_010  |
| Train | 11       | Warehouse_011  |
| Train | 12       | Warehouse_012  |
| Train | 13       | Warehouse_013  |
| Train | 14       | Warehouse_014  |
| Val   | 15       | Warehouse_015  |
| Val   | 16       | Warehouse_016  |
| Val   | 22       | Lab_000        |
| Val   | 23       | Hospital_000   |
| Test  | 17       | Warehouse_017  |
| Test  | 18       | Warehouse_018  |
| Test  | 19       | Warehouse_019  |
| Test  | 20       | Warehouse_020  |

</td>
<td valign="top">

| Split | Scene ID | Scene Name     |
|-------|----------|----------------|
| Train | 0        | Warehouse_000  |
| Train | 1        | Warehouse_001  |
| Train | 2        | Warehouse_002  |
| Train | 3        | Warehouse_003  |
| Train | 4        | Warehouse_004  |
| Train | 5        | Warehouse_005  |
| Train | 6        | Warehouse_006  |
| Train | 7        | Warehouse_007  |
| Train | 8        | Warehouse_008  |
| Train | 9        | Warehouse_009  |
| Train | 10       | Warehouse_010  |
| Train | 11       | Warehouse_011  |
| Train | 12       | Warehouse_012  |
| Train | 13       | Warehouse_013  |
| Train | 14       | Warehouse_014  |
| Train | 15       | Warehouse_015  |
| Train | 16       | Warehouse_016  |
| Train | 17       | Warehouse_017  |
| Train | 18       | Warehouse_018  |
| Train | 19       | Warehouse_019  |
| Val   | 20       | Warehouse_020  |
| Val   | 21       | Warehouse_021  |
| Val   | 22       | Warehouse_022  |
| Test  | 23       | Warehouse_023  |
| Test  | 24       | Warehouse_024  |
| Test  | 25       | Warehouse_025  |
| Test  | 26       | Warehouse_026  |
| Test  | 27       | Warehouse_027  |

*Scenes 001 / 003 / 005 / 007 / 021 / 024 are **Cosmos Transfer 2.5 (CT2.5)** augmented re-renderings of 000 / 002 / 004 / 006 / 020 / 023 respectively (same scene & cameras, augmented RGB).*<br>
*`Warehouse_026` and `Warehouse_027` are **real-world** test captures (4 and 7 cameras); the first 60 s (1800 frames) per camera is provided — videos + calibration only.*

</td>
</tr>
</table>

## Dataset Quantification
| Dataset                 | Annotation Type                                       | Scenes | Hours | Cameras | Object Classes & Counts                                       | No. 3D Boxes | No. 2D Boxes | Depth Maps | Total Size |
|-------------------------|-------------------------------------------------------|--------|-------|---------|---------------------------------------------------------------|--------------|--------------|------------|------------|
| **MTMC_Tracking_2024** | 2D bounding boxes, multi-camera tracking IDs | 90 | 212 | 953 | Person: 2,481 | 52M | 135M | No | 216.95 GB |
| **MTMC_Tracking_2025** | 2D & 3D bounding boxes, multi-camera tracking IDs | 23 | 42 | 504 | Person: 292<br>Forklift: 13<br>NovaCarter: 28<br>Transporter: 23<br>FourierGR1T2: 6<br>AgilityDigit: 1<br>**Overall:** 363 | 8.9M | 73M | Yes | 3.31 TB (~70 GB without depth maps) |
| **MTMC_Tracking_2026** | 2D & 3D bounding boxes, multi-camera tracking IDs | 28 | 28.7 | 353 | Person: 901<br>Forklift: 121<br>PalletTruck: 115 *(new)*<br>Transporter: 71<br>FourierGR1T2: 70<br>AgilityDigit: 69<br>NovaCarter: 32<br>**Overall:** 1,379 | 11.1M | 33.2M | Yes | 2.94 TB (~50 GB without depth maps) |

*`MTMC_Tracking_2026` scene / camera / camera-hour totals include the 2 real-world test scenes (`Warehouse_026`, `Warehouse_027`; first 60 s per camera). Their ground truth and depth maps are withheld, so the box counts and the "Depth Maps" column reflect the synthetic scenes only.*

## References
Please cite the following papers when using this dataset:

```bibtex
@InProceedings{Wang26PAISS,
author = {Yuxing Wang and Yizhou Wang and Anqi Li and Shuo Wang and Sameer Satish Pusegaonkar and Haoquan Liang and Jiajun Li and Shenxin Jiang and Jianhe Yuan and Shangru Li and Tongwei Dai and Zihao Chen and David C. Anastasiu and Sujit Biswas and Xunlei Wu and Zheng Tang},
title = {Physical {AI} {S}mart {S}paces: {A} large-scale benchmark for multi-camera {3D} perception in smart spaces},
booktitle = {Proc. NeurIPS},
address = {Atlanta, GA, USA},
note = {arXiv:2610.02580},
year = {2026}
}

@misc{Wang26Unified3DPerception,
author = {Yizhou Wang and Sameer Pusegaonkar and Yuxing Wang and Anqi Li and Vishal Kumar and Chetan Sethi and Ganapathy Aiyer and Yun He and Kartikay Thakkar and Swapnil Rathi and Bhushan Rupde and Zheng Tang and Sujit Biswas},
title = {A unified {3D} object perception framework for real-time outside-in multi-camera systems},
note = {arXiv:2601.10819},
year = {2026}
}

@InProceedings{Tang26AICity26,
author = {Zheng Tang and Shuo Wang and David C. Anastasiu and Ming-Ching Chang and Anuj Sharma and Quan Kong and Munkhjargal Gochoo and Jun-Wei Hsieh and Tomasz Kornuta and Zhedong Zheng and Renran Tian and Judah Goldfeder and Fulgencio Navarro and Yuxing Wang and Yizhou Wang and Sameer Satish Pusegaonkar and Anqi Li and Nalin Dadhich and Ridham Kachhadiya and Dhanishtha Patil and Haoquan Liang and Jiajun Li and Han Zhang and Yilin Zhao and Zaid Pervaiz Bhat and Shuyu Yang and Ashutosh Kumar and Rong Wang and Rafael Martin Nieto and Peter Christiansen and Ahmed Abduljawad and Mohanrasu Shanmugam and Nadeem Shaik and Sujit Biswas and Xunlei Wu and Vidya Murali and Rama Chellappa},
title = {The 10th {AI} {C}ity {C}hallenge},
booktitle = {Proc. ECCV Workshops},
address = {Malm\"o, Sweden},
year = {2026}
}

@InProceedings{Tang25AICity25,
author = {Zheng Tang and Shuo Wang and David C. Anastasiu and Ming-Ching Chang and Anuj Sharma and Quan Kong and Norimasa Kobori and Munkhjargal Gochoo and Ganzorig Batnasan and Munkh-Erdene Otgonbold and Fady Alnajjar and Jun-Wei Hsieh and Tomasz Kornuta and Xiaolong Li and Yilin Zhao and Han Zhang and Subhashree Radhakrishnan and Arihant Jain and Ratnesh Kumar and Vidya N. Murali and Yuxing Wang and Sameer Satish Pusegaonkar and Yizhou Wang and Sujit Biswas and Xunlei Wu and Zhedong Zheng and Pranamesh Chakraborty and Rama Chellappa},
title = {The 9th {AI} {C}ity {C}hallenge},
booktitle = {Proc. ICCV Workshops},
pages = {5526–-5535},
address = {Honolulu, HI, USA},
year = {2025}
}

@inproceedings{Wang24AICity24,
author = {Shuo Wang and David C. Anastasiu and Zheng Tang and Ming-Ching Chang and Yue Yao and Liang Zheng and Mohammed Shaiqur Rahman and Meenakshi S. Arya and Anuj Sharma and Pranamesh Chakraborty and Sanjita Prajapati and Quan Kong and Norimasa Kobori and Munkhjargal Gochoo and Munkh-Erdene Otgonbold and Ganzorig Batnasan and Fady Alnajjar and Ping-Yang Chen and Jun-Wei Hsieh and Xunlei Wu and Sameer Satish Pusegaonkar and Yizhou Wang and Sujit Biswas and Rama Chellappa},
title = {The 8th {AI} {C}ity {C}hallenge},
booktitle = {Proc. CVPR Workshops},
pages = {7261--7272},
address = {Seattle, WA, USA},
year = {2024}
}
```

## Ethical Considerations
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  When downloaded or used in accordance with our terms of service, developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.   

Please report security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## Changelog
- **2026-07-27**: Added complete [Croissant metadata](./croissant.json), including Responsible AI fields, and VGGT reprojection-error reports for the two real-world `MTMC_Tracking_2026` test scenes: [`Warehouse_026`](./MTMC_Tracking_2026/test/Warehouse_026/vggt_reprojection_error.txt) and [`Warehouse_027`](./MTMC_Tracking_2026/test/Warehouse_027/vggt_reprojection_error.txt).
- **2026-06-04**: Released 2 real-world test scenes for `MTMC_Tracking_2026` — `Warehouse_026` (4 cameras) and `Warehouse_027` (7 cameras), provided as 1080p / 30 FPS video covering the first 60 seconds (1800 frames) of each scene — the labeled evaluation window — with 2025-format `calibration.json`. An offline HOTA evaluator that reproduces the official AICity MTMC metric is available in the [`spatialai-data-utils` evaluation tools](https://github.com/NVIDIA-AI-Blueprints/video-search-and-summarization/tree/develop/libs/analytics/spatialai-data-utils/tools/evaluation) (`evaluate_aicity_mtmc.py`).
- **2026-05-15**: Released 3 synthetic test sets for `MTMC_Tracking_2026`. The remaining real-world test sets are scheduled for release at the end of May. The evaluation system for the 2026 AI City Challenge Track 1 has also been postponed to the end of May. In addition, the 2025 AI City Challenge Track 1 evaluation system has been temporarily disabled and will be re-opened after the conclusion of the 2026 AI City Challenge.
- **2026-04-29**: Initial release of `MTMC_Tracking_2026` — 26 scenes, 342 cameras, 28.5 camera-hours of 1080p video, 11.1M 3D boxes / 33.2M 2D boxes, with depth maps; calibration and GT aligned to the 2025 schema. 6 scenes (`Warehouse_001`, `_003`, `_005`, `_007`, `_021`, `_024`) are **Cosmos Transfer 2.5 (CT2.5) augmented** re-renderings of their source scenes (same scene/cameras/calibration/depth/GT, augmented RGB).
- **2025-07-14**: Provided evaluation tools for both 2024 and 2025 datasets.
- **2025-06-16**: Updated ground truth and calibration files, and removed misaligned videos and depth maps for train/val scenes in `MTMC_Tracking_2025`.
- **2025-05-28**: Added 4 test scenes of `MTMC_Tracking_2025` and provided scene ID table.
- **2025-05-19**: Updated corrupted files (videos and depth maps) in train/val scenes of `MTMC_Tracking_2025`.
- **2025-04-27**: Added depth maps to all `MTMC_Tracking_2025` scenes.
- **2025-04-23**: Added 2025-format calibration and ground truth JSON files to all `MTMC_Tracking_2024` scenes.