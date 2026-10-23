---
license: cc-by-nc-4.0
task_categories:
- video-classification
language:
- en
tags:
- medical
- fall-detection
- activity-recognition
- synthetic
pretty_name: 'OmniFall: A Unified Benchmark for Staged-to-Wild Fall Detection'
size_categories:
- 10K<n<100K
configs:
- config_name: labels
  data_files:
  - split: train
    path: parquet/labels/train-*.parquet
  default: true
- config_name: labels-syn
  data_files:
  - split: train
    path: parquet/labels-syn/train-*.parquet
- config_name: metadata-syn
  data_files:
  - split: train
    path: parquet/metadata-syn/train-*.parquet
- config_name: framewise-syn
  data_files:
  - split: train
    path: parquet/framewise-syn/train-*.parquet
- config_name: of-sta-cs
  data_files:
  - split: train
    path: parquet/of-sta-cs/train-*.parquet
  - split: validation
    path: parquet/of-sta-cs/validation-*.parquet
  - split: test
    path: parquet/of-sta-cs/test-*.parquet
- config_name: of-sta-cv
  data_files:
  - split: train
    path: parquet/of-sta-cv/train-*.parquet
  - split: validation
    path: parquet/of-sta-cv/validation-*.parquet
  - split: test
    path: parquet/of-sta-cv/test-*.parquet
- config_name: of-itw
  data_files:
  - split: train
    path: parquet/of-itw/train-*.parquet
  - split: validation
    path: parquet/of-itw/validation-*.parquet
  - split: test
    path: parquet/of-itw/test-*.parquet
- config_name: of-syn
  data_files:
  - split: train
    path: parquet/of-syn/train-*.parquet
  - split: validation
    path: parquet/of-syn/validation-*.parquet
  - split: test
    path: parquet/of-syn/test-*.parquet
- config_name: of-syn-cross-age
  data_files:
  - split: train
    path: parquet/of-syn-cross-age/train-*.parquet
  - split: validation
    path: parquet/of-syn-cross-age/validation-*.parquet
  - split: test
    path: parquet/of-syn-cross-age/test-*.parquet
- config_name: of-syn-cross-ethnicity
  data_files:
  - split: train
    path: parquet/of-syn-cross-ethnicity/train-*.parquet
  - split: validation
    path: parquet/of-syn-cross-ethnicity/validation-*.parquet
  - split: test
    path: parquet/of-syn-cross-ethnicity/test-*.parquet
- config_name: of-syn-cross-bmi
  data_files:
  - split: train
    path: parquet/of-syn-cross-bmi/train-*.parquet
  - split: validation
    path: parquet/of-syn-cross-bmi/validation-*.parquet
  - split: test
    path: parquet/of-syn-cross-bmi/test-*.parquet
- config_name: caucafall-to-all-cs
  data_files:
  - split: train
    path: parquet/caucafall-to-all-cs/train-*.parquet
  - split: validation
    path: parquet/caucafall-to-all-cs/validation-*.parquet
  - split: test
    path: parquet/caucafall-to-all-cs/test-*.parquet
- config_name: caucafall-to-all-cv
  data_files:
  - split: train
    path: parquet/caucafall-to-all-cv/train-*.parquet
  - split: test
    path: parquet/caucafall-to-all-cv/test-*.parquet
- config_name: cmdfall-to-all-cs
  data_files:
  - split: train
    path: parquet/cmdfall-to-all-cs/train-*.parquet
  - split: validation
    path: parquet/cmdfall-to-all-cs/validation-*.parquet
  - split: test
    path: parquet/cmdfall-to-all-cs/test-*.parquet
- config_name: cmdfall-to-all-cv
  data_files:
  - split: train
    path: parquet/cmdfall-to-all-cv/train-*.parquet
  - split: validation
    path: parquet/cmdfall-to-all-cv/validation-*.parquet
  - split: test
    path: parquet/cmdfall-to-all-cv/test-*.parquet
- config_name: edf-to-all-cs
  data_files:
  - split: train
    path: parquet/edf-to-all-cs/train-*.parquet
  - split: validation
    path: parquet/edf-to-all-cs/validation-*.parquet
  - split: test
    path: parquet/edf-to-all-cs/test-*.parquet
- config_name: edf-to-all-cv
  data_files:
  - split: train
    path: parquet/edf-to-all-cv/train-*.parquet
  - split: validation
    path: parquet/edf-to-all-cv/validation-*.parquet
  - split: test
    path: parquet/edf-to-all-cv/test-*.parquet
- config_name: gmdcsa24-to-all-cs
  data_files:
  - split: train
    path: parquet/gmdcsa24-to-all-cs/train-*.parquet
  - split: validation
    path: parquet/gmdcsa24-to-all-cs/validation-*.parquet
  - split: test
    path: parquet/gmdcsa24-to-all-cs/test-*.parquet
- config_name: gmdcsa24-to-all-cv
  data_files:
  - split: train
    path: parquet/gmdcsa24-to-all-cv/train-*.parquet
  - split: validation
    path: parquet/gmdcsa24-to-all-cv/validation-*.parquet
  - split: test
    path: parquet/gmdcsa24-to-all-cv/test-*.parquet
- config_name: le2i-to-all-cs
  data_files:
  - split: train
    path: parquet/le2i-to-all-cs/train-*.parquet
  - split: validation
    path: parquet/le2i-to-all-cs/validation-*.parquet
  - split: test
    path: parquet/le2i-to-all-cs/test-*.parquet
- config_name: le2i-to-all-cv
  data_files:
  - split: train
    path: parquet/le2i-to-all-cv/train-*.parquet
  - split: validation
    path: parquet/le2i-to-all-cv/validation-*.parquet
  - split: test
    path: parquet/le2i-to-all-cv/test-*.parquet
- config_name: mcfd-to-all-cs
  data_files:
  - split: train
    path: parquet/mcfd-to-all-cs/train-*.parquet
  - split: test
    path: parquet/mcfd-to-all-cs/test-*.parquet
- config_name: mcfd-to-all-cv
  data_files:
  - split: train
    path: parquet/mcfd-to-all-cv/train-*.parquet
  - split: validation
    path: parquet/mcfd-to-all-cv/validation-*.parquet
  - split: test
    path: parquet/mcfd-to-all-cv/test-*.parquet
- config_name: occu-to-all-cs
  data_files:
  - split: train
    path: parquet/occu-to-all-cs/train-*.parquet
  - split: validation
    path: parquet/occu-to-all-cs/validation-*.parquet
  - split: test
    path: parquet/occu-to-all-cs/test-*.parquet
- config_name: occu-to-all-cv
  data_files:
  - split: train
    path: parquet/occu-to-all-cv/train-*.parquet
  - split: validation
    path: parquet/occu-to-all-cv/validation-*.parquet
  - split: test
    path: parquet/occu-to-all-cv/test-*.parquet
- config_name: up_fall-to-all-cs
  data_files:
  - split: train
    path: parquet/up_fall-to-all-cs/train-*.parquet
  - split: validation
    path: parquet/up_fall-to-all-cs/validation-*.parquet
  - split: test
    path: parquet/up_fall-to-all-cs/test-*.parquet
- config_name: up_fall-to-all-cv
  data_files:
  - split: train
    path: parquet/up_fall-to-all-cv/train-*.parquet
  - split: validation
    path: parquet/up_fall-to-all-cv/validation-*.parquet
  - split: test
    path: parquet/up_fall-to-all-cv/test-*.parquet
- config_name: of-sta-to-all-cs
  data_files:
  - split: train
    path: parquet/of-sta-to-all-cs/train-*.parquet
  - split: validation
    path: parquet/of-sta-to-all-cs/validation-*.parquet
  - split: test
    path: parquet/of-sta-to-all-cs/test-*.parquet
- config_name: of-sta-to-all-cv
  data_files:
  - split: train
    path: parquet/of-sta-to-all-cv/train-*.parquet
  - split: validation
    path: parquet/of-sta-to-all-cv/validation-*.parquet
  - split: test
    path: parquet/of-sta-to-all-cv/test-*.parquet
- config_name: of-syn-to-all-cs
  data_files:
  - split: train
    path: parquet/of-syn-to-all-cs/train-*.parquet
  - split: validation
    path: parquet/of-syn-to-all-cs/validation-*.parquet
  - split: test
    path: parquet/of-syn-to-all-cs/test-*.parquet
- config_name: of-syn-to-all-cv
  data_files:
  - split: train
    path: parquet/of-syn-to-all-cv/train-*.parquet
  - split: validation
    path: parquet/of-syn-to-all-cv/validation-*.parquet
  - split: test
    path: parquet/of-syn-to-all-cv/test-*.parquet
- config_name: of-sta-syn-to-all-cs
  data_files:
  - split: train
    path: parquet/of-sta-syn-to-all-cs/train-*.parquet
  - split: validation
    path: parquet/of-sta-syn-to-all-cs/validation-*.parquet
  - split: test
    path: parquet/of-sta-syn-to-all-cs/test-*.parquet
- config_name: of-sta-syn-to-all-cv
  data_files:
  - split: train
    path: parquet/of-sta-syn-to-all-cv/train-*.parquet
  - split: validation
    path: parquet/of-sta-syn-to-all-cv/validation-*.parquet
  - split: test
    path: parquet/of-sta-syn-to-all-cv/test-*.parquet
- config_name: of-sta-to-itw-cs
  data_files:
  - split: train
    path: parquet/of-sta-to-itw-cs/train-*.parquet
  - split: validation
    path: parquet/of-sta-to-itw-cs/validation-*.parquet
  - split: test
    path: parquet/of-sta-to-itw-cs/test-*.parquet
- config_name: of-sta-to-itw-cv
  data_files:
  - split: train
    path: parquet/of-sta-to-itw-cv/train-*.parquet
  - split: validation
    path: parquet/of-sta-to-itw-cv/validation-*.parquet
  - split: test
    path: parquet/of-sta-to-itw-cv/test-*.parquet
- config_name: of-syn-to-itw
  data_files:
  - split: train
    path: parquet/of-syn-to-itw/train-*.parquet
  - split: validation
    path: parquet/of-syn-to-itw/validation-*.parquet
  - split: test
    path: parquet/of-syn-to-itw/test-*.parquet
- config_name: of-sta-syn-to-itw-cs
  data_files:
  - split: train
    path: parquet/of-sta-syn-to-itw-cs/train-*.parquet
  - split: validation
    path: parquet/of-sta-syn-to-itw-cs/validation-*.parquet
  - split: test
    path: parquet/of-sta-syn-to-itw-cs/test-*.parquet
- config_name: of-sta-syn-to-itw-cv
  data_files:
  - split: train
    path: parquet/of-sta-syn-to-itw-cv/train-*.parquet
  - split: validation
    path: parquet/of-sta-syn-to-itw-cv/validation-*.parquet
  - split: test
    path: parquet/of-sta-syn-to-itw-cv/test-*.parquet
- config_name: of-sta-itw-cs
  data_files:
  - split: train
    path: parquet/of-sta-itw-cs/train-*.parquet
  - split: validation
    path: parquet/of-sta-itw-cs/validation-*.parquet
  - split: test
    path: parquet/of-sta-itw-cs/test-*.parquet
- config_name: of-sta-itw-cv
  data_files:
  - split: train
    path: parquet/of-sta-itw-cv/train-*.parquet
  - split: validation
    path: parquet/of-sta-itw-cv/validation-*.parquet
  - split: test
    path: parquet/of-sta-itw-cv/test-*.parquet
- config_name: of-syn-itw
  data_files:
  - split: train
    path: parquet/of-syn-itw/train-*.parquet
  - split: validation
    path: parquet/of-syn-itw/validation-*.parquet
  - split: test
    path: parquet/of-syn-itw/test-*.parquet
- config_name: cs
  data_files:
  - split: train
    path: parquet/cs/train-*.parquet
  - split: validation
    path: parquet/cs/validation-*.parquet
  - split: test
    path: parquet/cs/test-*.parquet
- config_name: cv
  data_files:
  - split: train
    path: parquet/cv/train-*.parquet
  - split: validation
    path: parquet/cv/validation-*.parquet
  - split: test
    path: parquet/cv/test-*.parquet
- config_name: caucafall-cs
  data_files:
  - split: train
    path: parquet/caucafall-cs/train-*.parquet
  - split: validation
    path: parquet/caucafall-cs/validation-*.parquet
  - split: test
    path: parquet/caucafall-cs/test-*.parquet
- config_name: caucafall-cv
  data_files:
  - split: train
    path: parquet/caucafall-cv/train-*.parquet
- config_name: cmdfall-cs
  data_files:
  - split: train
    path: parquet/cmdfall-cs/train-*.parquet
  - split: validation
    path: parquet/cmdfall-cs/validation-*.parquet
  - split: test
    path: parquet/cmdfall-cs/test-*.parquet
- config_name: cmdfall-cv
  data_files:
  - split: train
    path: parquet/cmdfall-cv/train-*.parquet
  - split: validation
    path: parquet/cmdfall-cv/validation-*.parquet
  - split: test
    path: parquet/cmdfall-cv/test-*.parquet
- config_name: edf-cs
  data_files:
  - split: train
    path: parquet/edf-cs/train-*.parquet
  - split: validation
    path: parquet/edf-cs/validation-*.parquet
  - split: test
    path: parquet/edf-cs/test-*.parquet
- config_name: edf-cv
  data_files:
  - split: train
    path: parquet/edf-cv/train-*.parquet
  - split: validation
    path: parquet/edf-cv/validation-*.parquet
  - split: test
    path: parquet/edf-cv/test-*.parquet
- config_name: gmdcsa24-cs
  data_files:
  - split: train
    path: parquet/gmdcsa24-cs/train-*.parquet
  - split: validation
    path: parquet/gmdcsa24-cs/validation-*.parquet
  - split: test
    path: parquet/gmdcsa24-cs/test-*.parquet
- config_name: gmdcsa24-cv
  data_files:
  - split: train
    path: parquet/gmdcsa24-cv/train-*.parquet
  - split: validation
    path: parquet/gmdcsa24-cv/validation-*.parquet
  - split: test
    path: parquet/gmdcsa24-cv/test-*.parquet
- config_name: le2i-cs
  data_files:
  - split: train
    path: parquet/le2i-cs/train-*.parquet
  - split: validation
    path: parquet/le2i-cs/validation-*.parquet
  - split: test
    path: parquet/le2i-cs/test-*.parquet
- config_name: le2i-cv
  data_files:
  - split: train
    path: parquet/le2i-cv/train-*.parquet
  - split: validation
    path: parquet/le2i-cv/validation-*.parquet
  - split: test
    path: parquet/le2i-cv/test-*.parquet
- config_name: mcfd-cs
  data_files:
  - split: train
    path: parquet/mcfd-cs/train-*.parquet
- config_name: mcfd-cv
  data_files:
  - split: train
    path: parquet/mcfd-cv/train-*.parquet
  - split: validation
    path: parquet/mcfd-cv/validation-*.parquet
  - split: test
    path: parquet/mcfd-cv/test-*.parquet
- config_name: occu-cs
  data_files:
  - split: train
    path: parquet/occu-cs/train-*.parquet
  - split: validation
    path: parquet/occu-cs/validation-*.parquet
  - split: test
    path: parquet/occu-cs/test-*.parquet
- config_name: occu-cv
  data_files:
  - split: train
    path: parquet/occu-cv/train-*.parquet
  - split: validation
    path: parquet/occu-cv/validation-*.parquet
  - split: test
    path: parquet/occu-cv/test-*.parquet
- config_name: up_fall-cs
  data_files:
  - split: train
    path: parquet/up_fall-cs/train-*.parquet
  - split: validation
    path: parquet/up_fall-cs/validation-*.parquet
  - split: test
    path: parquet/up_fall-cs/test-*.parquet
- config_name: up_fall-cv
  data_files:
  - split: train
    path: parquet/up_fall-cv/train-*.parquet
  - split: validation
    path: parquet/up_fall-cv/validation-*.parquet
  - split: test
    path: parquet/up_fall-cv/test-*.parquet
- config_name: caucafall
  data_files:
  - split: train
    path: parquet/caucafall/train-*.parquet
  - split: validation
    path: parquet/caucafall/validation-*.parquet
  - split: test
    path: parquet/caucafall/test-*.parquet
- config_name: cmdfall
  data_files:
  - split: train
    path: parquet/cmdfall/train-*.parquet
  - split: validation
    path: parquet/cmdfall/validation-*.parquet
  - split: test
    path: parquet/cmdfall/test-*.parquet
- config_name: edf
  data_files:
  - split: train
    path: parquet/edf/train-*.parquet
  - split: validation
    path: parquet/edf/validation-*.parquet
  - split: test
    path: parquet/edf/test-*.parquet
- config_name: gmdcsa24
  data_files:
  - split: train
    path: parquet/gmdcsa24/train-*.parquet
  - split: validation
    path: parquet/gmdcsa24/validation-*.parquet
  - split: test
    path: parquet/gmdcsa24/test-*.parquet
- config_name: le2i
  data_files:
  - split: train
    path: parquet/le2i/train-*.parquet
  - split: validation
    path: parquet/le2i/validation-*.parquet
  - split: test
    path: parquet/le2i/test-*.parquet
- config_name: mcfd
  data_files:
  - split: train
    path: parquet/mcfd/train-*.parquet
- config_name: occu
  data_files:
  - split: train
    path: parquet/occu/train-*.parquet
  - split: validation
    path: parquet/occu/validation-*.parquet
  - split: test
    path: parquet/occu/test-*.parquet
- config_name: up_fall
  data_files:
  - split: train
    path: parquet/up_fall/train-*.parquet
  - split: validation
    path: parquet/up_fall/validation-*.parquet
  - split: test
    path: parquet/up_fall/test-*.parquet
- config_name: cs-staged
  data_files:
  - split: train
    path: parquet/cs-staged/train-*.parquet
  - split: validation
    path: parquet/cs-staged/validation-*.parquet
  - split: test
    path: parquet/cs-staged/test-*.parquet
- config_name: cv-staged
  data_files:
  - split: train
    path: parquet/cv-staged/train-*.parquet
  - split: validation
    path: parquet/cv-staged/validation-*.parquet
  - split: test
    path: parquet/cv-staged/test-*.parquet
- config_name: cs-staged-wild
  data_files:
  - split: train
    path: parquet/of-sta-to-all-cs/train-*.parquet
  - split: validation
    path: parquet/of-sta-to-all-cs/validation-*.parquet
  - split: test
    path: parquet/of-sta-to-all-cs/test-*.parquet
- config_name: cv-staged-wild
  data_files:
  - split: train
    path: parquet/of-sta-to-all-cv/train-*.parquet
  - split: validation
    path: parquet/of-sta-to-all-cv/validation-*.parquet
  - split: test
    path: parquet/of-sta-to-all-cv/test-*.parquet
- config_name: OOPS
  data_files:
  - split: train
    path: parquet/OOPS/train-*.parquet
  - split: validation
    path: parquet/OOPS/validation-*.parquet
  - split: test
    path: parquet/OOPS/test-*.parquet
dataset_info:
- config_name: labels
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 52618
- config_name: labels-syn
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  - name: age_group
    dtype:
      class_label:
        names:
          '0': toddlers_1_4
          '1': children_5_12
          '2': teenagers_13_17
          '3': young_adults_18_34
          '4': middle_aged_35_64
          '5': elderly_65_plus
  - name: gender_presentation
    dtype:
      class_label:
        names:
          '0': male
          '1': female
  - name: monk_skin_tone
    dtype:
      class_label:
        names:
          '0': mst1
          '1': mst2
          '2': mst3
          '3': mst4
          '4': mst5
          '5': mst6
          '6': mst7
          '7': mst8
          '8': mst9
          '9': mst10
  - name: race_ethnicity_omb
    dtype:
      class_label:
        names:
          '0': white
          '1': black
          '2': asian
          '3': hispanic_latino
          '4': aian
          '5': nhpi
          '6': mena
  - name: bmi_band
    dtype:
      class_label:
        names:
          '0': underweight
          '1': normal
          '2': overweight
          '3': obese
  - name: height_band
    dtype:
      class_label:
        names:
          '0': short
          '1': avg
          '2': tall
  - name: environment_category
    dtype:
      class_label:
        names:
          '0': indoor
          '1': outdoor
  - name: camera_shot
    dtype:
      class_label:
        names:
          '0': static_wide
          '1': static_medium_wide
  - name: speed
    dtype:
      class_label:
        names:
          '0': 24fps_rt
          '1': 25fps_rt
          '2': 30fps_rt
          '3': std_rt
  - name: camera_elevation
    dtype:
      class_label:
        names:
          '0': eye
          '1': low
          '2': high
          '3': top
  - name: camera_azimuth
    dtype:
      class_label:
        names:
          '0': front
          '1': rear
          '2': left
          '3': right
  - name: camera_distance
    dtype:
      class_label:
        names:
          '0': medium
          '1': far
  splits:
  - name: train
    num_bytes: 0
    num_examples: 19228
- config_name: metadata-syn
  features:
  - name: path
    dtype: string
  - name: dataset
    dtype: string
  - name: age_group
    dtype:
      class_label:
        names:
          '0': toddlers_1_4
          '1': children_5_12
          '2': teenagers_13_17
          '3': young_adults_18_34
          '4': middle_aged_35_64
          '5': elderly_65_plus
  - name: gender_presentation
    dtype:
      class_label:
        names:
          '0': male
          '1': female
  - name: monk_skin_tone
    dtype:
      class_label:
        names:
          '0': mst1
          '1': mst2
          '2': mst3
          '3': mst4
          '4': mst5
          '5': mst6
          '6': mst7
          '7': mst8
          '8': mst9
          '9': mst10
  - name: race_ethnicity_omb
    dtype:
      class_label:
        names:
          '0': white
          '1': black
          '2': asian
          '3': hispanic_latino
          '4': aian
          '5': nhpi
          '6': mena
  - name: bmi_band
    dtype:
      class_label:
        names:
          '0': underweight
          '1': normal
          '2': overweight
          '3': obese
  - name: height_band
    dtype:
      class_label:
        names:
          '0': short
          '1': avg
          '2': tall
  - name: environment_category
    dtype:
      class_label:
        names:
          '0': indoor
          '1': outdoor
  - name: camera_shot
    dtype:
      class_label:
        names:
          '0': static_wide
          '1': static_medium_wide
  - name: speed
    dtype:
      class_label:
        names:
          '0': 24fps_rt
          '1': 25fps_rt
          '2': 30fps_rt
          '3': std_rt
  - name: camera_elevation
    dtype:
      class_label:
        names:
          '0': eye
          '1': low
          '2': high
          '3': top
  - name: camera_azimuth
    dtype:
      class_label:
        names:
          '0': front
          '1': rear
          '2': left
          '3': right
  - name: camera_distance
    dtype:
      class_label:
        names:
          '0': medium
          '1': far
  splits:
  - name: train
    num_bytes: 0
    num_examples: 12000
- config_name: framewise-syn
  features:
  - name: path
    dtype: string
  - name: dataset
    dtype: string
  - name: frame_labels
    sequence:
      dtype:
        class_label:
          names:
            '0': walk
            '1': fall
            '2': fallen
            '3': sit_down
            '4': sitting
            '5': lie_down
            '6': lying
            '7': stand_up
            '8': standing
            '9': other
            '10': kneel_down
            '11': kneeling
            '12': squat_down
            '13': squatting
            '14': crawl
            '15': jump
      length: 81
  - name: age_group
    dtype:
      class_label:
        names:
          '0': toddlers_1_4
          '1': children_5_12
          '2': teenagers_13_17
          '3': young_adults_18_34
          '4': middle_aged_35_64
          '5': elderly_65_plus
  - name: gender_presentation
    dtype:
      class_label:
        names:
          '0': male
          '1': female
  - name: monk_skin_tone
    dtype:
      class_label:
        names:
          '0': mst1
          '1': mst2
          '2': mst3
          '3': mst4
          '4': mst5
          '5': mst6
          '6': mst7
          '7': mst8
          '8': mst9
          '9': mst10
  - name: race_ethnicity_omb
    dtype:
      class_label:
        names:
          '0': white
          '1': black
          '2': asian
          '3': hispanic_latino
          '4': aian
          '5': nhpi
          '6': mena
  - name: bmi_band
    dtype:
      class_label:
        names:
          '0': underweight
          '1': normal
          '2': overweight
          '3': obese
  - name: height_band
    dtype:
      class_label:
        names:
          '0': short
          '1': avg
          '2': tall
  - name: environment_category
    dtype:
      class_label:
        names:
          '0': indoor
          '1': outdoor
  - name: camera_shot
    dtype:
      class_label:
        names:
          '0': static_wide
          '1': static_medium_wide
  - name: speed
    dtype:
      class_label:
        names:
          '0': 24fps_rt
          '1': 25fps_rt
          '2': 30fps_rt
          '3': std_rt
  - name: camera_elevation
    dtype:
      class_label:
        names:
          '0': eye
          '1': low
          '2': high
          '3': top
  - name: camera_azimuth
    dtype:
      class_label:
        names:
          '0': front
          '1': rear
          '2': left
          '3': right
  - name: camera_distance
    dtype:
      class_label:
        names:
          '0': medium
          '1': far
  splits:
  - name: train
    num_bytes: 0
    num_examples: 12000
- config_name: of-sta-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 26036
  - name: validation
    num_bytes: 0
    num_examples: 4272
  - name: test
    num_bytes: 0
    num_examples: 18664
- config_name: of-sta-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 8888
  - name: validation
    num_bytes: 0
    num_examples: 8185
  - name: test
    num_bytes: 0
    num_examples: 27199
- config_name: of-itw
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 1023
  - name: validation
    num_bytes: 0
    num_examples: 482
  - name: test
    num_bytes: 0
    num_examples: 3673
- config_name: of-syn
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  - name: age_group
    dtype:
      class_label:
        names:
          '0': toddlers_1_4
          '1': children_5_12
          '2': teenagers_13_17
          '3': young_adults_18_34
          '4': middle_aged_35_64
          '5': elderly_65_plus
  - name: gender_presentation
    dtype:
      class_label:
        names:
          '0': male
          '1': female
  - name: monk_skin_tone
    dtype:
      class_label:
        names:
          '0': mst1
          '1': mst2
          '2': mst3
          '3': mst4
          '4': mst5
          '5': mst6
          '6': mst7
          '7': mst8
          '8': mst9
          '9': mst10
  - name: race_ethnicity_omb
    dtype:
      class_label:
        names:
          '0': white
          '1': black
          '2': asian
          '3': hispanic_latino
          '4': aian
          '5': nhpi
          '6': mena
  - name: bmi_band
    dtype:
      class_label:
        names:
          '0': underweight
          '1': normal
          '2': overweight
          '3': obese
  - name: height_band
    dtype:
      class_label:
        names:
          '0': short
          '1': avg
          '2': tall
  - name: environment_category
    dtype:
      class_label:
        names:
          '0': indoor
          '1': outdoor
  - name: camera_shot
    dtype:
      class_label:
        names:
          '0': static_wide
          '1': static_medium_wide
  - name: speed
    dtype:
      class_label:
        names:
          '0': 24fps_rt
          '1': 25fps_rt
          '2': 30fps_rt
          '3': std_rt
  - name: camera_elevation
    dtype:
      class_label:
        names:
          '0': eye
          '1': low
          '2': high
          '3': top
  - name: camera_azimuth
    dtype:
      class_label:
        names:
          '0': front
          '1': rear
          '2': left
          '3': right
  - name: camera_distance
    dtype:
      class_label:
        names:
          '0': medium
          '1': far
  splits:
  - name: train
    num_bytes: 0
    num_examples: 15344
  - name: validation
    num_bytes: 0
    num_examples: 1956
  - name: test
    num_bytes: 0
    num_examples: 1928
- config_name: of-syn-cross-age
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  - name: age_group
    dtype:
      class_label:
        names:
          '0': toddlers_1_4
          '1': children_5_12
          '2': teenagers_13_17
          '3': young_adults_18_34
          '4': middle_aged_35_64
          '5': elderly_65_plus
  - name: gender_presentation
    dtype:
      class_label:
        names:
          '0': male
          '1': female
  - name: monk_skin_tone
    dtype:
      class_label:
        names:
          '0': mst1
          '1': mst2
          '2': mst3
          '3': mst4
          '4': mst5
          '5': mst6
          '6': mst7
          '7': mst8
          '8': mst9
          '9': mst10
  - name: race_ethnicity_omb
    dtype:
      class_label:
        names:
          '0': white
          '1': black
          '2': asian
          '3': hispanic_latino
          '4': aian
          '5': nhpi
          '6': mena
  - name: bmi_band
    dtype:
      class_label:
        names:
          '0': underweight
          '1': normal
          '2': overweight
          '3': obese
  - name: height_band
    dtype:
      class_label:
        names:
          '0': short
          '1': avg
          '2': tall
  - name: environment_category
    dtype:
      class_label:
        names:
          '0': indoor
          '1': outdoor
  - name: camera_shot
    dtype:
      class_label:
        names:
          '0': static_wide
          '1': static_medium_wide
  - name: speed
    dtype:
      class_label:
        names:
          '0': 24fps_rt
          '1': 25fps_rt
          '2': 30fps_rt
          '3': std_rt
  - name: camera_elevation
    dtype:
      class_label:
        names:
          '0': eye
          '1': low
          '2': high
          '3': top
  - name: camera_azimuth
    dtype:
      class_label:
        names:
          '0': front
          '1': rear
          '2': left
          '3': right
  - name: camera_distance
    dtype:
      class_label:
        names:
          '0': medium
          '1': far
  splits:
  - name: train
    num_bytes: 0
    num_examples: 6364
  - name: validation
    num_bytes: 0
    num_examples: 3183
  - name: test
    num_bytes: 0
    num_examples: 9681
- config_name: of-syn-cross-ethnicity
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  - name: age_group
    dtype:
      class_label:
        names:
          '0': toddlers_1_4
          '1': children_5_12
          '2': teenagers_13_17
          '3': young_adults_18_34
          '4': middle_aged_35_64
          '5': elderly_65_plus
  - name: gender_presentation
    dtype:
      class_label:
        names:
          '0': male
          '1': female
  - name: monk_skin_tone
    dtype:
      class_label:
        names:
          '0': mst1
          '1': mst2
          '2': mst3
          '3': mst4
          '4': mst5
          '5': mst6
          '6': mst7
          '7': mst8
          '8': mst9
          '9': mst10
  - name: race_ethnicity_omb
    dtype:
      class_label:
        names:
          '0': white
          '1': black
          '2': asian
          '3': hispanic_latino
          '4': aian
          '5': nhpi
          '6': mena
  - name: bmi_band
    dtype:
      class_label:
        names:
          '0': underweight
          '1': normal
          '2': overweight
          '3': obese
  - name: height_band
    dtype:
      class_label:
        names:
          '0': short
          '1': avg
          '2': tall
  - name: environment_category
    dtype:
      class_label:
        names:
          '0': indoor
          '1': outdoor
  - name: camera_shot
    dtype:
      class_label:
        names:
          '0': static_wide
          '1': static_medium_wide
  - name: speed
    dtype:
      class_label:
        names:
          '0': 24fps_rt
          '1': 25fps_rt
          '2': 30fps_rt
          '3': std_rt
  - name: camera_elevation
    dtype:
      class_label:
        names:
          '0': eye
          '1': low
          '2': high
          '3': top
  - name: camera_azimuth
    dtype:
      class_label:
        names:
          '0': front
          '1': rear
          '2': left
          '3': right
  - name: camera_distance
    dtype:
      class_label:
        names:
          '0': medium
          '1': far
  splits:
  - name: train
    num_bytes: 0
    num_examples: 8267
  - name: validation
    num_bytes: 0
    num_examples: 2762
  - name: test
    num_bytes: 0
    num_examples: 8199
- config_name: of-syn-cross-bmi
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  - name: age_group
    dtype:
      class_label:
        names:
          '0': toddlers_1_4
          '1': children_5_12
          '2': teenagers_13_17
          '3': young_adults_18_34
          '4': middle_aged_35_64
          '5': elderly_65_plus
  - name: gender_presentation
    dtype:
      class_label:
        names:
          '0': male
          '1': female
  - name: monk_skin_tone
    dtype:
      class_label:
        names:
          '0': mst1
          '1': mst2
          '2': mst3
          '3': mst4
          '4': mst5
          '5': mst6
          '6': mst7
          '7': mst8
          '8': mst9
          '9': mst10
  - name: race_ethnicity_omb
    dtype:
      class_label:
        names:
          '0': white
          '1': black
          '2': asian
          '3': hispanic_latino
          '4': aian
          '5': nhpi
          '6': mena
  - name: bmi_band
    dtype:
      class_label:
        names:
          '0': underweight
          '1': normal
          '2': overweight
          '3': obese
  - name: height_band
    dtype:
      class_label:
        names:
          '0': short
          '1': avg
          '2': tall
  - name: environment_category
    dtype:
      class_label:
        names:
          '0': indoor
          '1': outdoor
  - name: camera_shot
    dtype:
      class_label:
        names:
          '0': static_wide
          '1': static_medium_wide
  - name: speed
    dtype:
      class_label:
        names:
          '0': 24fps_rt
          '1': 25fps_rt
          '2': 30fps_rt
          '3': std_rt
  - name: camera_elevation
    dtype:
      class_label:
        names:
          '0': eye
          '1': low
          '2': high
          '3': top
  - name: camera_azimuth
    dtype:
      class_label:
        names:
          '0': front
          '1': rear
          '2': left
          '3': right
  - name: camera_distance
    dtype:
      class_label:
        names:
          '0': medium
          '1': far
  splits:
  - name: train
    num_bytes: 0
    num_examples: 9675
  - name: validation
    num_bytes: 0
    num_examples: 4701
  - name: test
    num_bytes: 0
    num_examples: 4852
- config_name: caucafall-to-all-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 176
  - name: validation
    num_bytes: 0
    num_examples: 25
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: caucafall-to-all-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 254
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: cmdfall-to-all-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 20884
  - name: validation
    num_bytes: 0
    num_examples: 3689
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: cmdfall-to-all-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 5987
  - name: validation
    num_bytes: 0
    num_examples: 6026
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: edf-to-all-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 302
  - name: validation
    num_bytes: 0
    num_examples: 78
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: edf-to-all-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 254
  - name: validation
    num_bytes: 0
    num_examples: 254
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: gmdcsa24-to-all-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 213
  - name: validation
    num_bytes: 0
    num_examples: 152
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: gmdcsa24-to-all-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 276
  - name: validation
    num_bytes: 0
    num_examples: 89
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: le2i-to-all-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 670
  - name: validation
    num_bytes: 0
    num_examples: 94
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: le2i-to-all-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 490
  - name: validation
    num_bytes: 0
    num_examples: 195
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: mcfd-to-all-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 1352
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: mcfd-to-all-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 169
  - name: validation
    num_bytes: 0
    num_examples: 169
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: occu-to-all-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 289
  - name: validation
    num_bytes: 0
    num_examples: 94
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: occu-to-all-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 245
  - name: validation
    num_bytes: 0
    num_examples: 239
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: up_fall-to-all-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 2150
  - name: validation
    num_bytes: 0
    num_examples: 140
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: up_fall-to-all-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 1213
  - name: validation
    num_bytes: 0
    num_examples: 1213
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: of-sta-to-all-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 26036
  - name: validation
    num_bytes: 0
    num_examples: 4272
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: of-sta-to-all-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 8888
  - name: validation
    num_bytes: 0
    num_examples: 8185
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: of-syn-to-all-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 15344
  - name: validation
    num_bytes: 0
    num_examples: 1956
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: of-syn-to-all-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 15344
  - name: validation
    num_bytes: 0
    num_examples: 1956
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: of-sta-syn-to-all-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 41380
  - name: validation
    num_bytes: 0
    num_examples: 6228
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: of-sta-syn-to-all-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 24232
  - name: validation
    num_bytes: 0
    num_examples: 10141
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: of-sta-to-itw-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 26036
  - name: validation
    num_bytes: 0
    num_examples: 4272
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: of-sta-to-itw-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 8888
  - name: validation
    num_bytes: 0
    num_examples: 8185
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: of-syn-to-itw
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 15344
  - name: validation
    num_bytes: 0
    num_examples: 1956
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: of-sta-syn-to-itw-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 41380
  - name: validation
    num_bytes: 0
    num_examples: 6228
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: of-sta-syn-to-itw-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 24232
  - name: validation
    num_bytes: 0
    num_examples: 10141
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: of-sta-itw-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 26036
  - name: validation
    num_bytes: 0
    num_examples: 4272
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: of-sta-itw-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 8888
  - name: validation
    num_bytes: 0
    num_examples: 8185
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: of-syn-itw
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 15344
  - name: validation
    num_bytes: 0
    num_examples: 1956
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 27059
  - name: validation
    num_bytes: 0
    num_examples: 4754
  - name: test
    num_bytes: 0
    num_examples: 22337
- config_name: cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 9911
  - name: validation
    num_bytes: 0
    num_examples: 8667
  - name: test
    num_bytes: 0
    num_examples: 30872
- config_name: caucafall-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 176
  - name: validation
    num_bytes: 0
    num_examples: 25
  - name: test
    num_bytes: 0
    num_examples: 47
- config_name: caucafall-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 254
- config_name: cmdfall-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 20884
  - name: validation
    num_bytes: 0
    num_examples: 3689
  - name: test
    num_bytes: 0
    num_examples: 17570
- config_name: cmdfall-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 5987
  - name: validation
    num_bytes: 0
    num_examples: 6026
  - name: test
    num_bytes: 0
    num_examples: 24104
- config_name: edf-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 302
  - name: validation
    num_bytes: 0
    num_examples: 78
  - name: test
    num_bytes: 0
    num_examples: 128
- config_name: edf-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 254
  - name: validation
    num_bytes: 0
    num_examples: 254
  - name: test
    num_bytes: 0
    num_examples: 254
- config_name: gmdcsa24-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 213
  - name: validation
    num_bytes: 0
    num_examples: 152
  - name: test
    num_bytes: 0
    num_examples: 93
- config_name: gmdcsa24-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 276
  - name: validation
    num_bytes: 0
    num_examples: 89
  - name: test
    num_bytes: 0
    num_examples: 93
- config_name: le2i-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 670
  - name: validation
    num_bytes: 0
    num_examples: 94
  - name: test
    num_bytes: 0
    num_examples: 203
- config_name: le2i-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 490
  - name: validation
    num_bytes: 0
    num_examples: 195
  - name: test
    num_bytes: 0
    num_examples: 282
- config_name: mcfd-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 1352
- config_name: mcfd-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 169
  - name: validation
    num_bytes: 0
    num_examples: 169
  - name: test
    num_bytes: 0
    num_examples: 1014
- config_name: occu-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 289
  - name: validation
    num_bytes: 0
    num_examples: 94
  - name: test
    num_bytes: 0
    num_examples: 101
- config_name: occu-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 245
  - name: validation
    num_bytes: 0
    num_examples: 239
  - name: test
    num_bytes: 0
    num_examples: 239
- config_name: up_fall-cs
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 2150
  - name: validation
    num_bytes: 0
    num_examples: 140
  - name: test
    num_bytes: 0
    num_examples: 522
- config_name: up_fall-cv
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 1213
  - name: validation
    num_bytes: 0
    num_examples: 1213
  - name: test
    num_bytes: 0
    num_examples: 1213
- config_name: cmdfall
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 20884
  - name: validation
    num_bytes: 0
    num_examples: 3689
  - name: test
    num_bytes: 0
    num_examples: 17570
- config_name: edf
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 302
  - name: validation
    num_bytes: 0
    num_examples: 78
  - name: test
    num_bytes: 0
    num_examples: 128
- config_name: gmdcsa24
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 213
  - name: validation
    num_bytes: 0
    num_examples: 152
  - name: test
    num_bytes: 0
    num_examples: 93
- config_name: le2i
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 670
  - name: validation
    num_bytes: 0
    num_examples: 94
  - name: test
    num_bytes: 0
    num_examples: 203
- config_name: mcfd
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 1352
- config_name: occu
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 289
  - name: validation
    num_bytes: 0
    num_examples: 94
  - name: test
    num_bytes: 0
    num_examples: 101
- config_name: up_fall
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 2150
  - name: validation
    num_bytes: 0
    num_examples: 140
  - name: test
    num_bytes: 0
    num_examples: 522
- config_name: caucafall
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 176
  - name: validation
    num_bytes: 0
    num_examples: 25
  - name: test
    num_bytes: 0
    num_examples: 47
- config_name: cs-staged
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 26036
  - name: validation
    num_bytes: 0
    num_examples: 4272
  - name: test
    num_bytes: 0
    num_examples: 18664
- config_name: cv-staged
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 8888
  - name: validation
    num_bytes: 0
    num_examples: 8185
  - name: test
    num_bytes: 0
    num_examples: 27199
- config_name: cs-staged-wild
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 26036
  - name: validation
    num_bytes: 0
    num_examples: 4272
  - name: test
    num_bytes: 0
    num_examples: 24265
- config_name: cv-staged-wild
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 8888
  - name: validation
    num_bytes: 0
    num_examples: 8185
  - name: test
    num_bytes: 0
    num_examples: 32800
- config_name: OOPS
  features:
  - name: path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': walk
          '1': fall
          '2': fallen
          '3': sit_down
          '4': sitting
          '5': lie_down
          '6': lying
          '7': stand_up
          '8': standing
          '9': other
          '10': kneel_down
          '11': kneeling
          '12': squat_down
          '13': squatting
          '14': crawl
          '15': jump
  - name: start
    dtype: float32
  - name: end
    dtype: float32
  - name: subject
    dtype: int32
  - name: cam
    dtype: int32
  - name: dataset
    dtype: string
  splits:
  - name: train
    num_bytes: 0
    num_examples: 1023
  - name: validation
    num_bytes: 0
    num_examples: 482
  - name: test
    num_bytes: 0
    num_examples: 3673
---
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
</br>
<a href="https://arxiv.org/abs/2505.19889">
  <img src="https://img.shields.io/badge/arXiv-2505.19889-b31b1b.svg?logo=arXiv" alt="arXiv" style="height:20px;">
</a>
</br>
<a href="https://simplexsigil.github.io/omnifall/">
  <img src="https://img.shields.io/badge/Omnifall-Project_Page-2FA7C9.svg" alt="Project Page" style="height:20px;">
</a>
</br>
<a href="https://pypi.org/project/omnifall/">
  <img src="https://img.shields.io/badge/Omnifall-Python_Package-006EAE.svg" alt="Python Package" style="height:20px;">
</a>


# OmniFall: A Unified Benchmark for Staged-to-Wild Fall Detection

OmniFall is a comprehensive fall detection benchmark with dense temporal segment annotations across three components: **OF-Staged** (8 public lab datasets), **OF-In-the-Wild** (genuine accidents from OOPS), and **OF-Synthetic** (12,000 diffusion-generated videos with demographic diversity). All components share a sixteen-class activity taxonomy.

[[Paper]](https://arxiv.org/abs/2505.19889) [[Project Page]](https://simplexsigil.github.io/omnifall/)

## Quickstart

### Labels only (no video files needed)

```python
from datasets import load_dataset

# 8 staged datasets, cross-subject split
ds = load_dataset("simplexsigil2/omnifall", "of-sta-cs")
print(ds["train"][0])  # {'path': ..., 'label': 1, 'start': 0.0, 'end': 2.5, ...}

# Cross-domain: train on staged, test on all (staged + itw + syn)
ds = load_dataset("simplexsigil2/omnifall", "of-sta-to-all-cs")

# Synthetic data with demographic metadata (19 columns)
ds = load_dataset("simplexsigil2/omnifall", "of-syn")
```

### With video loading (`pip install omnifall`)

```python
import omnifall

# OF-Syn videos auto-download from HF Hub (~9.1GB, cached)
ds = omnifall.load("of-syn", video=True)

# OF-ItW requires one-time OOPS video preparation
omnifall.prepare_oops()  # streams ~45GB, extracts ~2.6GB
ds = omnifall.load("of-itw", video=True)

# The video column contains absolute file paths (strings)
print(ds["train"][0]["video"])
```

Video paths can also be added to an already-loaded dataset via `omnifall.add_video(ds, config="of-syn")`. OOPS preparation is also available via CLI: `omnifall prepare-oops`.

> **Loading the data directly?** [STRUCTURE.md](STRUCTURE.md) explains how a label row resolves to a video file and which videos each component contributes; [KNOWN_PITFALLS.md](KNOWN_PITFALLS.md) covers the two things that can catch you out. The `omnifall` package handles both for you.

## Overview

| | Videos | Segments (SV) | Duration (SV) |
|---|---|---|---|
| **OF-Staged** (8 datasets) | 2,164 | 9,590 | 13.81h |
| **OF-ItW** (OOPS) | 818 | 4,022 | 2.65h |
| **OF-Syn** | 12,000 | 19,228 | 16.88h |
| **Total** | **14,982** | **32,840** | **33.34h** |

| Dataset | Type | Videos | Segments (SV) | Duration (SV) | Avg Seg (s) |
|---|---|---|---|---|---|
| [CMDFall](https://www.mica.edu.vn/perso/Tran-Thi-Thanh-Hai/CMDFALL.html) | multi (7 views) | 384 | 6,026 | 7.12h | 4.25 |
| [UP-Fall](https://sites.google.com/up.edu.mx/har-up/) | multi (2 views) | 1,118 | 1,213 | 4.59h | 13.63 |
| [Le2i](https://search-data.ubfc.fr/imvia/FR-13002091000019-2024-04-09_Fall-Detection-Dataset.html) | single | 190 | 967 | 0.79h | 2.95 |
| [GMDCSA24](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos) | single | 160 | 458 | 0.36h | 2.80 |
| [CAUCAFall](https://data.mendeley.com/datasets/7w7fccy7ky/4) | single | 100 | 258 | 0.28h | 3.85 |
| [EDF](https://doi.org/10.5281/zenodo.15494102) | multi (2 views) | 10 | 254 | 0.22h | 3.14 |
| [OCCU](https://doi.org/10.5281/zenodo.15494102) | multi (2 views) | 10 | 245 | 0.25h | 3.54 |
| [MCFD](https://www.iro.umontreal.ca/~labimage/Dataset/) | multi (8 views) | 192 | 169 | 0.20h | 4.26 |
| [OOPS-Fall](https://oops.cs.columbia.edu/data/) | single | 818 | 4,022 | 2.65h | 2.38 |
| OF-Syn | single | 12,000 | 19,228 | 16.88h | 3.16 |

SV = single-view (one count per unique camera perspective). Multi-view datasets have additional synchronized views; see [statistics.md](statistics.md) for full multi-view counts and class distributions.

## Configs

Over 70 configurations are available. Each returns train/validation/test splits.

| Category | Examples | Description |
|---|---|---|
| **Same-domain** | `of-sta-cs`, `of-sta-cv`, `of-itw`, `of-syn` | Train and test from the same source |
| **Cross-domain (to-all)** | `of-sta-to-all-cs`, `of-syn-to-all-cs` | Train on one source, test on all (staged + ItW + Syn) |
| **Individual to-all** | `cmdfall-to-all-cs`, `edf-to-all-cv` | Train on single dataset, test on all |
| **OF-Syn demographic** | `of-syn-cross-age`, `of-syn-cross-bmi` | Cross-demographic generalization splits |
| **Aggregate** | `cs`, `cv` | All staged + OOPS combined |
| **Individual** | `cmdfall-cs`, `le2i-cv` | Single staged dataset |
| **Labels/metadata** | `labels`, `labels-syn`, `framewise-syn` | Raw annotations without splits |

See [CONFIGS.md](CONFIGS.md) for the complete configuration reference including deprecated names.

## Citation

If you use OmniFall in your research, please cite our paper as well as the sub-dataset papers:

```bibtex
@misc{omnifall,
      title={OmniFall: From Staged Through Synthetic to Wild, A Unified Multi-Domain Dataset for Robust Fall Detection},
      author={David Schneider and Zdravko Marinov and Rafael Baur and Zeyun Zhong and Rodi Düger and Rainer Stiefelhagen},
      year={2025},
      eprint={2505.19889},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2505.19889},
},

@inproceedings{omnifall_cmdfall,
  title={A multi-modal multi-view dataset for human fall analysis and preliminary investigation on modality},
  author={Tran, Thanh-Hai and Le, Thi-Lan and Pham, Dinh-Tan and Hoang, Van-Nam and Khong, Van-Minh and Tran, Quoc-Toan and Nguyen, Thai-Son and Pham, Cuong},
  booktitle={2018 24th International Conference on Pattern Recognition (ICPR)},
  pages={1947--1952},
  year={2018},
  organization={IEEE}
},

@article{omnifall_up-fall,
  title={UP-fall detection dataset: A multimodal approach},
  author={Mart{\'\i}nez-Villase{\~n}or, Lourdes and Ponce, Hiram and Brieva, Jorge and Moya-Albor, Ernesto and N{\'u}{\~n}ez-Mart{\'\i}nez, Jos{\'e} and Pe{\~n}afort-Asturiano, Carlos},
  journal={Sensors},
  volume={19},
  number={9},
  pages={1988},
  year={2019},
  publisher={MDPI}
},

@article{omnifall_le2i,
  title={Optimized spatio-temporal descriptors for real-time fall detection: comparison of support vector machine and Adaboost-based classification},
  author={Charfi, Imen and Miteran, Johel and Dubois, Julien and Atri, Mohamed and Tourki, Rached},
  journal={Journal of Electronic Imaging},
  volume={22},
  number={4},
  pages={041106--041106},
  year={2013},
  publisher={Society of Photo-Optical Instrumentation Engineers}
},

@article{omnifall_gmdcsa,
  title={GMDCSA-24: A dataset for human fall detection in videos},
  author={Alam, Ekram and Sufian, Abu and Dutta, Paramartha and Leo, Marco and Hameed, Ibrahim A},
  journal={Data in Brief},
  volume={57},
  pages={110892},
  year={2024},
  publisher={Elsevier}
},

@article{omnifall_cauca,
  title={Dataset CAUCAFall},
  author={Eraso, Jose Camilo and Mu{\~n}oz, Elena and Mu{\~n}oz, Mariela and Pinto, Jesus},
  journal={Mendeley Data},
  volume={4},
  year={2022}
},

@inproceedings{omnifall_edf_occu,
  title={Evaluating depth-based computer vision methods for fall detection under occlusions},
  author={Zhang, Zhong and Conly, Christopher and Athitsos, Vassilis},
  booktitle={International symposium on visual computing},
  pages={196--207},
  year={2014},
  organization={Springer}
},

@article{omnifall_mcfd,
  title={Multiple cameras fall dataset},
  author={Auvinet, Edouard and Rougier, Caroline and Meunier, Jean and St-Arnaud, Alain and Rousseau, Jacqueline},
  journal={DIRO-Universit{\'e} de Montr{\'e}al, Tech. Rep},
  volume={1350},
  pages={24},
  year={2010}
},

@inproceedings{omnifall_oops,
  title={Oops! predicting unintentional action in video},
  author={Epstein, Dave and Chen, Boyuan and Vondrick, Carl},
  booktitle={Proceedings of the IEEE/CVF conference on computer vision and pattern recognition},
  pages={919--929},
  year={2020}
}
```

## License

The annotations and split definitions are released under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). The original video data belongs to their respective owners and should be obtained from the original sources.

## Contact

For questions about the dataset, please contact [david.schneider@kit.edu].

## Documentation

- [statistics.md](statistics.md) - Full dataset statistics and class distributions
- [CONFIGS.md](CONFIGS.md) - Complete configuration reference and deprecated names
- [STRUCTURE.md](STRUCTURE.md) - Repository structure and data formats
- [LABELS.md](LABELS.md) - Label definitions and annotation guidelines
- [KNOWN_PITFALLS.md](KNOWN_PITFALLS.md) - Things that surprise people writing their own loader, and what to do about them
- [omnifall_dataset_examples.ipynb](omnifall_dataset_examples.ipynb) - Interactive examples with video loading and visualization
