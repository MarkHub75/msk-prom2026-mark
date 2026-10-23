# OmniFall Repository Structure

## Directory Layout

```
parquet/                     Pre-built parquet files for all configs (used by load_dataset)
labels/                      CSV files containing temporal segment annotations
  caucafall.csv ... up_fall.csv   Staged dataset labels (7 columns)
  OOPS.csv                        OF-ItW labels (7 columns)
  of-syn.csv                      OF-Syn labels (19 columns: 7 core + 12 demographic)
splits/
  cs/                        Cross-subject splits (staged + OOPS)
  cv/                        Cross-view splits (staged + OOPS)
  syn/                       Synthetic splits (random, cross_age, cross_ethnicity, cross_bmi)
videos/metadata.csv          OF-Syn video-level metadata (12,000 videos)
data_files/
  omnifall-synthetic_av1.tar      OF-Syn video archive (12,000 AV1-encoded MP4s)
  syn_frame_wise_labels.tar.zst   OF-Syn frame-wise HDF5 labels
  oops_video_mapping.csv          Mapping from OOPS original filenames to OF-ItW names
prepare_oops_videos.py       Script to extract OOPS videos for OF-ItW
generate_parquet.py          Script to regenerate parquet files from labels + splits
```

## Label Format

Each label file in `labels/` contains temporal segment annotations:

```csv
path,label,start,end,subject,cam,dataset
path/to/clip,class_id,start_time,end_time,subject_id,camera_id,dataset_name
```

| Column | Type | Description |
|---|---|---|
| `path` | string | Video path, relative to its own dataset, **without file extension** |
| `label` | int | Class ID (0-15), see [LABELS.md](LABELS.md) |
| `start` | float | Segment start time in seconds |
| `end` | float | Segment end time in seconds |
| `subject` | int | Subject ID (-1 for OF-ItW and OF-Syn) |
| `cam` | int | Camera view ID (-1 for OF-ItW and OF-Syn) |
| `dataset` | string | Source dataset name |

### Resolving a row to a video file

A video is addressed by the pair `(dataset, path)`:

```
{root}/{dataset}/video/{path}.mp4
```

Every config carries a `dataset` column, so this works for all of them and never
needs to branch on the config name. `path` values are dataset-relative and carry
no extension, e.g. `Coffee_room_01/video_1`, `colors/S39P1K5`,
`falls/BestFailsofWeek2July2016_FailArmy9`.

Because `path` is only unique *within* a dataset, key any lookup or cache on the
`(dataset, path)` pair rather than on `path` alone.

The [`omnifall`](https://pypi.org/project/omnifall/) package does this for you:

```python
ds = omnifall.load("cs", split="test", video=True)
ds[0]["video"]   # absolute path to the file
```

### Video coverage

OmniFall annotates the continuous recordings of each component. With one
exception, every video file distributed for a component is annotated, and every
annotated path resolves to a file:

| Component | Videos annotated | Files distributed | Not annotated |
|---|---|---|---|
| cmdfall | 384 | 1,436 | 1,052 (see below) |
| up_fall | 1,118 | 1,118 | — |
| OOPS | 818 | 818 | — |
| le2i | 190 | 190 | — |
| mcfd | 192 | 192 | — |
| GMDCSA24 | 160 | 160 | — |
| caucafall | 100 | 100 | — |
| edf | 10 | 10 | — |
| occu | 10 | 10 | — |
| of-syn | 12,000 | 12,000 | — |

**cmdfall.** The release ships the same recordings in two forms.
`cmdfall/video/colors/` holds the 384 continuous multi-camera recordings
(7 Kinect views, roughly 400-540 s each); `cmdfall/video/clips/` holds 1,052
short pre-cut action clips (3-8 s) grouped into 58 recording sessions. OmniFall
annotates `colors/` only. The clips are the same footage already segmented, so
annotating them would be redundant and would hand a model the segment boundaries
it is supposed to predict. Files under `clips/` are therefore expected to be
present and unreferenced.

Check a local copy against the label file rather than against a file count:

```bash
omnifall verify cmdfall     # 384/384 annotated videos present
```

### Files you do not need to read

`data_files/oops_video_mapping.csv` maps original OOPS file names onto OF-ItW
`path` values. It exists for the video preparation step only --- `omnifall
prepare OOPS` extracts and renames the videos so that they land on the layout
above. Nothing downstream of preparation refers to it.

### OF-Syn Extended Labels

`labels/of-syn.csv` contains 12 additional demographic and scene metadata columns:

| Column | Values |
|---|---|
| `age_group` | toddlers_1_4, children_5_12, teenagers_13_17, young_adults_18_34, middle_aged_35_64, elderly_65_plus |
| `gender_presentation` | male, female |
| `monk_skin_tone` | mst1 through mst10 |
| `race_ethnicity_omb` | white, black, asian, hispanic_latino, aian, nhpi, mena |
| `bmi_band` | underweight, normal, overweight, obese |
| `height_band` | short, avg, tall |
| `environment_category` | indoor, outdoor |
| `camera_shot` | static_wide, static_medium_wide |
| `speed` | 24fps_rt, 25fps_rt, 30fps_rt, std_rt |
| `camera_elevation` | eye, low, high, top |
| `camera_azimuth` | front, rear, left, right |
| `camera_distance` | medium, far |

These fields are available in OF-Syn configs (`of-syn`, `of-syn-cross-*`, `labels-syn`, `metadata-syn`, `framewise-syn`). Cross-domain configs that mix sources use only the 7 core columns.

## Split Format

Split files in `splits/` list video paths included in each partition:

```csv
path
path/to/clip
```

Each video path maps to one or more temporal segments in the corresponding label file. The parquet configs contain the pre-merged result of joining split paths with labels.
