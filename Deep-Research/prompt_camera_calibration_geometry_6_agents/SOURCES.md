# Источники camera_calibration_geometry

Реестр формируется оркестратором из одной волны шести исследователей. Время доступа, версия и реально выполненное действие указываются отдельно от даты публикации. Поисковые сниппеты не служат доказательством. Метки фактов определены в [RAW_FACTS.md](RAW_FACTS.md).

<a id="s001"></a>
## S001 — Общий договор исследования

- Происхождение: пользователь; [Context-prompt.md](Context-prompt.md), версия `mosprom-research-v1`.
- Тип: локальный входной документ, полностью прочитан. Дата публикации файла не установлена; доступ 2026-10-23, Europe/Moscow.
- Локатор: разделы 2–4 (команда, соревнование и карта тем), 8, 10–16 (артефакты, доказательства, отчёты).
- Факты: F001. Исторические сведения о доступности кейса заменены более свежим тематическим входом, но не официальным PDF.

<a id="s002"></a>
## S002 — Тематическое задание и пересказ checkpoint

- Происхождение: пользователь; [prompt_camera_calibration_geometry_6_agents.md](prompt_camera_calibration_geometry_6_agents.md).
- Тип: локальный входной документ, полностью прочитан. Дата публикации файла не установлена; доступ 2026-10-23, Europe/Moscow.
- Локатор: §§0–3 (обновлённый контекст и специальный конвейер), §§4–9 (охват и выходы).
- Факты: F002–F003. Сведения о сервере и приоритетах экспертов имеют статус пересказа команды. Сам официальный PDF кейса не предоставлен и не прочитан в этом запуске.

<a id="s003"></a>
## S003 — Собственный аналитический расчёт pinhole и sampling

- Автор: оркестратор этого исследования. [GEOMETRY_SANITY.py](_WORK/GEOMETRY_SANITY.py), [результат](_WORK/GEOMETRY_SANITY_RESULT.json).
- Тип: фактически выполненный локальный расчёт; Python 3.11, стандартная библиотека; 2026-10-23 19:35 Europe/Moscow.
- Локатор: `one_pixel_error`, `elevated_point`, `sampling`; формула `v=f*(h-z)/Z` для заданной горизонтальной идеальной камеры.
- Факты: F004–F006. Это синтетическая иллюстрация, без реального видео, измерений камеры, запуска OpenCV, моделей или LinQ. Числа не переносимы на производственную сцену.

## Время, скорость и temporal models — происхождение A03

Все источники этого блока открыты исследователем A03 2026-10-23; начало работы 19:34:55+03:00. Подробные выписки и локальные ID: [AGENT_03_SPEED.md](_WORK/AGENT_03_SPEED.md). Публичные измерения авторов не являются нашими тестами.

| ID | Первичный источник; дата/версия | Прямая ссылка и локатор | Факты и статус |
|---|---|---|---|
| <a id="s004"></a>S004 | PyAV contributors, Time; прочитанная страница **9.0.2**, дата публикации не установлена | [Time](https://pyav.org/docs/stable/api/time.html), Overview/Decoding | F007; A03-S01. `stable` не объявляется последним релизом |
| <a id="s005"></a>S005 | PyAV contributors, Frames; **9.0.2** | [Frame](https://pyav.org/docs/stable/api/frame.html), `pts/time/time_base/dts` | F007; A03-S02. Документация полей, не проверка камеры |
| <a id="s006"></a>S006 | FFmpeg developers, Doxygen **8.0** | [AVFrame](https://ffmpeg.org/doxygen/8.0/structAVFrame.html), `pts`, `best_effort_timestamp`, `pkt_dts` | F007; A03-S03. Дата генерации страницы неизвестна |
| <a id="s007"></a>S007 | FFmpeg developers, CLI docs; версия страницы неизвестна | [ffprobe](https://ffmpeg.org/ffprobe.html), `show_frames/show_streams/show_entries`, JSON | F020; A03-S04. Команда предложена, бинарник не запускался |
| <a id="s008"></a>S008 | FFmpeg developers, CLI docs; версия страницы неизвестна | [ffmpeg](https://ffmpeg.org/ffmpeg.html), `-r`, `-fps_mode`, `-copyts` | F008; A03-S05. Требуется сверка с установленной сборкой |
| <a id="s009"></a>S009 | Feichtenhofer, Fan, Malik, He, SlowFast; arXiv v3 **2019-10-29**, v1 **2018-12-10** | [Авторская статья](https://arxiv.org/html/1812.03982v3), §§3.1–3.4, table 1 | F009; A03-S06. Полный arXiv вместо CVF, который дал 403 |
| <a id="s010"></a>S010 | FAIR/facebookresearch, SlowFast; SHA `287ec0076846560f44a9327e931a5a2360240533`, commit **2026-03-16** | [SLOWFAST_8x8_R50.yaml](https://github.com/facebookresearch/SlowFast/blob/287ec0076846560f44a9327e931a5a2360240533/configs/Kinetics/SLOWFAST_8x8_R50.yaml), DATA/SLOWFAST; [LICENSE](https://github.com/facebookresearch/SlowFast/blob/287ec0076846560f44a9327e931a5a2360240533/LICENSE) | F009; A03-S07. Code inspected, Apache-2.0; веса/export не проверены |
| <a id="s011"></a>S011 | Duan, Zhao, Chen, Lin, Dai, PoseC3D; arXiv v2 **2022-04-02**, CVPR 2022 | [Авторская статья](https://arxiv.org/html/2104.13586v2), Experiments/table 3, supp. D.5 | F010; A03-S08. Benchmark авторов, не промышленное измерение |
| <a id="s012"></a>S012 | kennymckormick/pyskl; SHA `f2bf3a6b08e2e8dec744692d64efdb187fd6719a`, commit **2026-02-19** | [joint.py](https://github.com/kennymckormick/pyskl/blob/f2bf3a6b08e2e8dec744692d64efdb187fd6719a/configs/posec3d/slowonly_r50_ntu60_xsub/joint.py); [LICENSE](https://github.com/kennymckormick/pyskl/blob/f2bf3a6b08e2e8dec744692d64efdb187fd6719a/LICENSE) | F010; A03-S09. Apache-2.0 кода не определяет права на все веса/данные |
| <a id="s013"></a>S013 | pyskl, тот же SHA | [sampling.py](https://github.com/kennymckormick/pyskl/blob/f2bf3a6b08e2e8dec744692d64efdb187fd6719a/pyskl/datasets/pipelines/sampling.py), `UniformSampleFrames` | F011; A03-S10. Прочитан по SHA, не запускался |
| <a id="s014"></a>S014 | Pires, Lay, Rubenson, J. Experimental Biology 221(16), jeb174755; институциональная дата **2018-08-23** | [Запись авторского университета](https://research-repository.uwa.edu.au/en/publications/modulation-of-joint-and-limb-mechanical-work-in-walk-to-run-trans/), abstract; DOI `10.1242/jeb.174755` | F012; A03-S11. Прочитан только abstract, полного метода не получено |

## Проективная геометрия — происхождение A01

Доступ 2026-10-23; начало A01 19:34:51+03:00. [Полный материал](_WORK/AGENT_01_GEOMETRY.md). API и исходники ниже относятся к **4.13.0**, а не к неопределённому latest. Код не исполнялся.

| ID | Автор, версия/дата | URL и локатор | Связи / ограничение |
|---|---|---|---|
| <a id="s015"></a>S015 | OpenCV team, **4.13.0** | [calib3d](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), camera model, `calibrateCamera/findHomography/undistort/undistortPoints` | F021–F025; A01-S01. Дата самой страницы неизвестна |
| <a id="s016"></a>S016 | OpenCV team, **4.13.0** | [imgproc transform](https://docs.opencv.org/4.13.0/da/d54/group__imgproc__transform.html), `getPerspectiveTransform/warpPerspective` | F024; A01-S02 |
| <a id="s017"></a>S017 | OpenCV team, **4.13.0** | [core array](https://docs.opencv.org/4.13.0/d2/de8/group__core__array.html), `perspectiveTransform` | F024; A01-S03 |
| <a id="s018"></a>S018 | OpenCV team, **4.13.0** | [Homography tutorial](https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html), Basic theory/Demos 1–2 | F021–F022; A01-S04. Демонстрация, не CCTV benchmark |
| <a id="s019"></a>S019 | OpenCV contributors, tag **4.13.0** | [fundam.cpp](https://raw.githubusercontent.com/opencv/opencv/4.13.0/modules/calib3d/src/fundam.cpp), `HomographyEstimatorCallback::checkSubset/runKernel`, `cv::findHomography`, просмотрены строки 55–110, 345–427 | F022/F025; A01-S05. Вывод о четырёхточечном пути относится к этому исходнику |
| <a id="s020"></a>S020 | OpenCV contributors, tag **4.13.0** | [imgwarp.cpp](https://raw.githubusercontent.com/opencv/opencv/4.13.0/modules/imgproc/src/imgwarp.cpp), `getPerspectiveTransform`, 2705–2745, 2823–2827 | F024; A01-S06 |
| <a id="s021"></a>S021 | OpenCV contributors, tag **4.13.0** | [undistort.dispatch.cpp](https://raw.githubusercontent.com/opencv/opencv/4.13.0/modules/calib3d/src/undistort.dispatch.cpp), `undistort`, 263–287 | F023; A01-S07 |
| <a id="s022"></a>S022 | A. Criminisi, I. Reid, A. Zisserman, Oxford; **ICCV 1999**, 8-page conference paper | [PDF CMU mirror](https://www-2.cs.cmu.edu/~ph/869/papers/Criminisi99.pdf); [Microsoft Research author PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/1999/01/Criminisi_iccv1999.pdf), §§2–4, uncertainty pp.5–6 | F021/F022/F028/F036; A01-S08, A02-S12. Одна цепочка происхождения, не два независимых подтверждения; не IJCV 2000 |
| <a id="s023"></a>S023 | S. Paik, J. Youn, P. Kim, J. Jung / KICT; **2026-09-29**, CC-BY-4.0 | [Article](https://isprs-archives.copernicus.org/articles/L-4-W3-2026/131/2026/index.html), [PDF](https://isprs-archives.copernicus.org/articles/L-4-W3-2026/131/2026/isprs-archives-L-4-W3-2026-131-2026.pdf), §§2.1–2.3,3–4; DOI `10.5194/isprs-archives-L-4-W3-2026-131-2026` | F026; A01-S09. Blender и точные keypoints, не реальный detector benchmark |
| <a id="s024"></a>S024 | C. Koetsier, S. Busch, M. Sester, Leibniz Universität Hannover; **2019**, CC-BY-4.0 | [Trajectory Extraction for Analysis of Unsafe Driving Behaviour](https://isprs-archives.copernicus.org/articles/XLII-2-W13/1573/2019/isprs-archives-XLII-2-W13-1573-2019.pdf), p.1576, figs.8–10 | F026; A01-S10. Дорожный домен; повторный fetch конкретной строки дал timeout после чтения PDF |
| <a id="s025"></a>S025 | OpenCV release metadata | [4.13.0](https://github.com/opencv/opencv/releases/tag/4.13.0), [REST](https://api.github.com/repos/opencv/opencv/releases/tags/4.13.0): `2025-12-31T09:44:36Z`, short commit `fe38fc6`; [archive](https://opencv.org/releases./), [5.0.0](https://github.com/opencv/opencv/releases/tag/5.0.0) | F042; A01-S11/S13. Архив и REST дают разные даты 5.0.0; 4.x redirect не latest |
| <a id="s026"></a>S026 | OpenCV contributors, **4.13.0** | [LICENSE](https://raw.githubusercontent.com/opencv/opencv/4.13.0/LICENSE) | F042; A01-S12. Apache-2.0, сторонние notices отдельно |

## Полуавтоматизация и lifecycle — происхождение A02

Доступ 2026-10-23, начало 19:34:51+03:00. [Подробные выписки](_WORK/AGENT_02_CALIBRATION.md). A02 использовал отдельно закреплённые документы OpenCV **4.12.0**; это не конфликт с проверкой 4.13.0 у A01 и не заявление об актуальном latest. GUI, модели и библиотеки не запускались.

| ID | Автор, дата/версия | URL и локатор | Связи / ограничение |
|---|---|---|---|
| <a id="s027"></a>S027 | OpenCV contributors, **4.12.0**; release 2025-07-02, HTML generated 2025-07-03 | [ArUco/ChArUco calibration](https://docs.opencv.org/4.12.0/da/d13/tutorial_aruco_calibration.html), ChArUco boards, `CharucoDetector/matchImagePoints/calibrateCamera` | F031; A02-S01 |
| <a id="s028"></a>S028 | OpenCV contributors, **4.12.0** | [ChArUco detection](https://docs.opencv.org/4.12.0/df/d4a/tutorial_charuco_detection.html), board creation/detection/pose, note after 4.6.0 | F032; A02-S02 |
| <a id="s029"></a>S029 | Bernát Gábor / OpenCV, **4.12.0** | [Camera calibration sample](https://docs.opencv.org/4.12.0/d4/d94/tutorial_camera_calibration.html), Goal/Source/Explanation, `samples/cpp/tutorial_code/calib3d/camera_calibration/` | F031; A02-S03. Оконный образец intrinsics, не web zone editor |
| <a id="s030"></a>S030 | AprilRobotics / University of Michigan, **v3.4.5**, release **2025-08-29** | [README](https://raw.githubusercontent.com/AprilRobotics/apriltag/v3.4.5/README.md), Pose Estimation/Coordinate System; [apriltag_pose.h](https://raw.githubusercontent.com/AprilRobotics/apriltag/v3.4.5/apriltag_pose.h), `apriltag_detection_info_t`, `estimate_tag_pose`; [LICENSE.md](https://raw.githubusercontent.com/AprilRobotics/apriltag/v3.4.5/LICENSE.md) | F033; A02-S04/S05. BSD-2-Clause; tagsize между detection corners, pose ambiguity |
| <a id="s031"></a>S031 | Per Gantelius / fSpy, **v1.0.3**, **2019-01-02T07:42:50Z** | [Basics](https://fspy.io/basics/), [Tutorial](https://fspy.io/tutorial/); [solver.ts](https://raw.githubusercontent.com/perarnia/fSpy/v1.0.3/src/gui/solver/solver.ts), `computeTranslationVector`, `DEFAULT_CAMERA_DISTANCE_SCALE`; [release](https://github.com/perarnia/fSpy/releases/tag/v1.0.3), [LICENSE](https://raw.githubusercontent.com/perarnia/fSpy/v1.0.3/LICENSE) | F034; A02-S06/S07. GPL-3.0-or-later по code header; страницы без даты, код закреплён |
| <a id="s032"></a>S032 | F. Seegräber, M. She, F. Woelk, K. Köser / Kiel University, Calibmar **1.1.0**, SHA `5c5a8200b42b22bac4e1ff62d066c1373a5ce57b`, **2026-08-03** | [Workflow](https://mdskiel.github.io/calibmar_documentation/camera_calibration.html), [report](https://mdskiel.github.io/calibmar_documentation/calibration_report_format.html), [changelog](https://mdskiel.github.io/calibmar_documentation/changelog.html); [CMakeLists](https://raw.githubusercontent.com/MDSKiel/calibmar/5c5a8200b42b22bac4e1ff62d066c1373a5ce57b/CMakeLists.txt), [dialog source](https://raw.githubusercontent.com/MDSKiel/calibmar/5c5a8200b42b22bac4e1ff62d066c1373a5ce57b/src/app/ui/dialogs/file_calibration_dialog.cpp), [LICENSE](https://raw.githubusercontent.com/MDSKiel/calibmar/5c5a8200b42b22bac4e1ff62d066c1373a5ce57b/LICENSE.txt) | F035; A02-S08/S09. BSD-3-Clause, dependencies отдельно; GitHub зеркало, binary releases на GitLab, assets не скачивались |
| <a id="s033"></a>S033 | A. Veicht, P.-E. Sarlin, P. Lindenberger, M. Pollefeys, GeoCalib, ECCV 2024; arXiv **v2 2024-10-17** | [Полный HTML](https://arxiv.org/html/2409.06704v2), §§3,3.2, Appendix C; [version history](https://arxiv.org/abs/2409.06704) | F036; A02-S10. PDF слишком велик для fetch, прочитан полный HTML той же версии |
| <a id="s034"></a>S034 | cvg/GeoCalib, SHA `1dedb29f94fc11b896c5f572005978aeebccd67f`, **2026-10-14** | [Repository](https://github.com/cvg/GeoCalib); [extractor.py](https://raw.githubusercontent.com/cvg/GeoCalib/1dedb29f94fc11b896c5f572005978aeebccd67f/geocalib/extractor.py), `calibrate/_post_process`; [Gradio](https://raw.githubusercontent.com/cvg/GeoCalib/1dedb29f94fc11b896c5f572005978aeebccd67f/gradio_app.py); [LICENSE-WEIGHTS](https://raw.githubusercontent.com/cvg/GeoCalib/1dedb29f94fc11b896c5f572005978aeebccd67f/LICENSE-WEIGHTS) | F036; A02-S11. Apache-2.0 code / CC-BY-4.0 weights; demo UI inspected, не выполнен |
| <a id="s035"></a>S035 | OpenCV contributors, **4.12.0** | [Tracking / ECC](https://docs.opencv.org/4.12.0/dc/d6b/group__video__track.html), `findTransformECC` | F037; A02-S13. Registration contract, не доказательство метрической валидности |
| <a id="s036"></a>S036 | OpenCV contributors, **4.12.0**, release **2025-07-02T12:48:11Z** | [calib3d introduction](https://docs.opencv.org/4.12.0/d9/d0c/group__calib3d.html), intrinsics reuse/image scaling; [LICENSE](https://raw.githubusercontent.com/opencv/opencv/4.12.0/LICENSE) | F038/F042; A02-S14. Apache-2.0, fixed version |

## Опасное сближение — происхождение A04

Доступ 2026-10-23, начало 19:40:31+03:00. [Полный материал](_WORK/AGENT_04_PROXIMITY.md). Иностранные safety documents используются для понимания угроз и рабочих операций, **не как установленное российское нормативное требование**. Геометрические формулы прогноза — собственные выводы, не перенесённые пороги из дорожных/шахтных работ.

| ID | Автор, дата/версия | URL и локатор | Факты / происхождение |
|---|---|---|---|
| <a id="s037"></a>S037 | C. Jobes, J. Carr, J. DuCarme, J. Patts / NIOSH; IEEE IAS **2011**, pp.641–647, каталог **2011-10-01** | [CDC card](https://stacks.cdc.gov/view/cdc/227383), [PDF](https://stacks.cdc.gov/view/cdc/227383/cdc_227383_DS1.pdf), §II A–C, figs.4–5, table 1, eqs.1–7, §IV | F043–F044; A04-S01. Public Domain по карточке; magnetic proximity, не CCTV |
| <a id="s038"></a>S038 | Y.-S. Shin, J. Kim / Dankook University; Sustainability 14(13),7934, **2022-06-29**, CC-BY-4.0 | [DOI](https://doi.org/10.3390/su14137934), [полный PDF через зеркало](https://www.wisdomlib.org/uploads/journals/mdpi-sust/2022-volume-14-issue-13--2071-1050-14-13-7934-.pdf), §§2.4–2.5,3–4, fig.5 | F045; A04-S02. MDPI 429, прочитан тот же авторский текст через зеркало; одна цепочка |
| <a id="s039"></a>S039 | L. Pu, R. Joshi / Siemens ITS, FHWA; **May 2008**, FHWA-HRT-08-050 | [SSAM manual](https://www.fhwa.dot.gov/publications/research/safety/08050/), Appendix Terms and Definitions: TTC/PET/DeltaS | F049–F051; A04-S03. Road microsimulation surrogate measures, не промышленный threshold |
| <a id="s040"></a>S040 | HSE, Safe driving: reversing; footer **2021-05-11**, дата исходной редакции не установлена | [Guidance](https://www.hse.gov.uk/WORKPLACETRANSPORT/factsheets/reversing.htm), signaller/safety devices | F043/F055; A04-S04. Рабочая роль сигнальщика; OGL v3 exceptions |
| <a id="s041"></a>S041 | H. Kim et al., Sejong University; Sensors 22(20),7953, **2022-10-19**, CC-BY-4.0 | [Multispectral Benchmark Dataset and Baseline for Forklift Collision Avoidance](https://pmc.ncbi.nlm.nih.gov/articles/PMC9608680/), §§2.1,2.1.6, DOI `10.3390/s22207953` | F052; A04-S05. Onboard RGB/thermal/stereo, не fixed monocular CCTV |
| <a id="s042"></a>S042 | Shapely contributors, **2.1.2** | [distance API](https://shapely.readthedocs.io/en/2.1.2/reference/shapely.distance.html), [measurement.py](https://raw.githubusercontent.com/shapely/shapely/2.1.2/shapely/measurement.py), `distance`, lines49–76 | F047/F054; A04-S06. Python wrapper inspected, GEOS internals не аудированы, пакет не запускался |
| <a id="s043"></a>S043 | Shapely contributors, **2.1.2** | [buffer API](https://shapely.readthedocs.io/en/2.1.2/reference/shapely.buffer.html), Minkowski sum, `quad_segs` | F046/F048; A04-S07. Численная аппроксимация дуг, не физический safety model |
| <a id="s044"></a>S044 | Shapely contributors, **2.1.2** | [covers API](https://shapely.readthedocs.io/en/2.1.2/reference/shapely.covers.html), boundary examples; [LICENSE](https://raw.githubusercontent.com/shapely/shapely/2.1.2/LICENSE.txt) | F046/F054; A04-S08. BSD-3-Clause, dependencies отдельно |
| <a id="s045"></a>S045 | HSE, SPC/TECH/SI5/05; issue **2002-12-31**, review **2007-01-01** | [Idler roller nip hazards on heavy duty belt conveyors](https://www.hse.gov.uk/mining/techld55.htm), §§3,8–12 | F053; A04-S09. Старый отраслевой документ, footer 2021 не дата циркуляра |

## Pose, depth и сложные сцены — происхождение A05

Доступ 2026-10-23, начало 19:42:09+03:00; [полный материал](_WORK/AGENT_05_COMPLEX.md), snapshots/HTTP metadata в `_WORK/A05_SOURCES/`. A05-S01 объединён с S022: прочитан ICCV1999 PDF, [страница Oxford IJCV2000](https://robots.ox.ac.uk/~vgg/publications/2000/Criminisi00a/) не означает чтения полной журнальной версии. Все модели только исследованы по документам/коду.

| ID | Автор, дата/версия | URL и локатор | Факты / ограничения |
|---|---|---|---|
| <a id="s046"></a>S046 | Z. Cao, G. Hidalgo, T. Simon, S.-E. Wei, Y. Sheikh / CMU; OpenPose paper **v2 2019-05-30**; SHA `5c5d96523ef917bd30301245fdc8343937cae48d`, **2024-08-03** | [Paper abstract](https://arxiv.org/abs/1812.08008v2), [repo](https://github.com/CMU-Perceptual-Computing-Lab/openpose), `doc/02_output.md` JSON, [LICENSE](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/5c5d96523ef917bd30301245fdc8343937cae48d/LICENSE) | F059; A05-S02. Noncommercial research conditions, не permissive license |
| <a id="s047"></a>S047 | T. Jiang et al., Shanghai AI Lab, RTMPose **v2 2023-07-03**; MMPose SHA `759b39c13fea6ba094afc1fa932f51dc1b11cbf9`, **2025-08-04** | [Полная статья](https://arxiv.org/html/2303.07399v2), §§1,3.1,3.5; [README](https://github.com/open-mmlab/mmpose/blob/759b39c13fea6ba094afc1fa932f51dc1b11cbf9/projects/rtmpose/README.md), [LICENSE](https://github.com/open-mmlab/mmpose/blob/759b39c13fea6ba094afc1fa932f51dc1b11cbf9/LICENSE) | F060; A05-S03. Apache-2.0 code, selected checkpoint отдельно; предполагаемый rtmcc_head path дал 404 и не заявляется прочитанным |
| <a id="s048"></a>S048 | L. Yang et al., Depth Anything V2; paper **v2 2024-10-20**, NeurIPS2024; SHA `a561b849ebae10a6f5ef49e26c83cbbcd36c71bf`, **2026-03-24** | [Paper metadata/abstract](https://arxiv.org/abs/2406.09414v2), [root README](https://github.com/DepthAnything/Depth-Anything-V2/blob/a561b849ebae10a6f5ef49e26c83cbbcd36c71bf/README.md), `depth_anything_v2/dpt.py::forward` | F061/F064; A05-S04. Small Apache-2.0, Base/Large/Giant NC согласно root README |
| <a id="s049"></a>S049 | Те же авторы и SHA, metric branch | [metric README](https://github.com/DepthAnything/Depth-Anything-V2/blob/a561b849ebae10a6f5ef49e26c83cbbcd36c71bf/metric_depth/README.md), pretrained/usage; [DPT code](https://github.com/DepthAnything/Depth-Anything-V2/blob/a561b849ebae10a6f5ef49e26c83cbbcd36c71bf/metric_depth/depth_anything_v2/dpt.py), head/forward | F062; A05-S05. Отдельные metric weights, не простое изменение max_depth |
| <a id="s050"></a>S050 | M. Hu, W. Yin et al., Metric3Dv2 **v4 2025-01-03**; SHA `eb5b6fac0dc155e4e52f576e304fbf11655ff339`, **2025-03-13** | [Полная статья](https://arxiv.org/html/2404.15506v4), §III-A/B, supp.1.2; [repo](https://github.com/YvanYin/Metric3D), [do_test.py](https://github.com/YvanYin/Metric3D/blob/eb5b6fac0dc155e4e52f576e304fbf11655ff339/mono/utils/do_test.py), `transform_test_data_scalecano/align_scale/align_scale_shift`, LICENSE | F063; A05-S06. BSD-2-Clause code, commercial questions README адресует авторам |
| <a id="s051"></a>S051 | HSE, updated **2024-10-29**, исходная дата неизвестна | [Planning lifting operations](https://www.hse.gov.uk/work-equipment-machinery/planning-organising-lifting-operations.htm), Positioning/Working under suspended loads | F058; A05-S07. Отраслевой контекст, не российский регламент |
| <a id="s052"></a>S052 | Depth Anything authors, HF metric Hypersim cards; даты revisions неизвестны | [Small card](https://huggingface.co/depth-anything/Depth-Anything-V2-Metric-Hypersim-Small/blob/main/README.md), read revision `3bc65d4`; [Large card](https://huggingface.co/depth-anything/Depth-Anything-V2-Metric-Hypersim-Large/blob/main/README.md), revision `7972080`, YAML license | F064; A05-S08. Метаданные конкретного артефакта расходятся с общей root wording; правовой вывод не установлен |

## Runtime, разметка и эталоны — происхождение A06

Доступ 2026-10-23, начало 19:42:15+03:00; [полный материал](_WORK/AGENT_06_TOOLS.md), raw manifests/code в `_WORK/A06_EVIDENCE/`. A06-S01 объединён с S025/S026; A06-S06 — с S042. Никаких installation/resolver/import/benchmark tests не выполнялось.

| ID | Автор, дата/версия | URL и локатор | Факты / ограничения |
|---|---|---|---|
| <a id="s053"></a>S053 | OpenCV contributors, **4.13.0** | [perspective_correction.py](https://raw.githubusercontent.com/opencv/opencv/4.13.0/samples/python/tutorial_code/features2D/Homography/perspective_correction.py), `perspectiveCorrection`; tutorial S018 Demo2 | F071; A06-S02. Скачан/прочитан, не запускался; GUI image-to-image demo |
| <a id="s054"></a>S054 | OpenCV Python packaging maintainers / PyPI, **opencv-python-headless 4.13.0.92** | [Package JSON](https://pypi.org/pypi/opencv-python-headless/4.13.0.92/json), `requires_dist/requires_python`, локальная JSON-копия | F068; A06-S03. Manifest observation, не результат установки |
| <a id="s055"></a>S055 | S. Gillies / Shapely contributors, **2.1.2**, **2025-09-24** | [PyPI](https://pypi.org/project/shapely/2.1.2/), [requirements](https://shapely.readthedocs.io/en/2.1.2/index.html), [manual](https://shapely.readthedocs.io/en/2.1.2/manual.html), Coordinate Systems/Polygons | F067/F070; A06-S04. Python≥3.10, GEOS≥3.9, NumPy≥1.21; Z ignored |
| <a id="s056"></a>S056 | Shapely contributors, **2.1.2** | [contains](https://shapely.readthedocs.io/en/2.1.2/reference/shapely.contains.html), examples; covers S044 | F070; A06-S05. Boundary semantics, не uncertainty band |
| <a id="s057"></a>S057 | Tryolabs, Norfair **v2.3.0**, **2025-04-30**, SHA `e517b4236f6b67a6ecf342f5df1fccb7788dbc54` | [pyproject.toml](https://raw.githubusercontent.com/tryolabs/norfair/v2.3.0/pyproject.toml), [LICENSE](https://raw.githubusercontent.com/tryolabs/norfair/v2.3.0/LICENSE), [PyPI](https://pypi.org/project/norfair/2.3.0/) | F068/F069; A06-S07. BSD-3-Clause; source dependencies не проверены установкой |
| <a id="s058"></a>S058 | Y. Zhang et al., original ByteTrack, ECCV2022; SHA `d1bf0191adff59bc8fcfeaa0b33d3d1642552a99`, **2022-12-11T07:05:00Z** | [repo](https://github.com/FoundationVision/ByteTrack), [tracker.py](https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/byte_tracker.py), `STrack/BYTETracker`; [requirements](https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/requirements.txt), [LICENSE](https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/LICENSE) | F069; A06-S08. MIT оригинала, не всех сторонних реализаций |
| <a id="s059"></a>S059 | CVAT.ai/Intel, Community **v2.80.0**, release **2026-10-21T16:34:20Z**, SHA `bb0a873fe071e70d71458cd82127052025e05807` | [release](https://github.com/cvat-ai/cvat/releases/tag/v2.80.0), [LICENSE](https://github.com/cvat-ai/cvat/blob/v2.80.0/LICENSE), [XML format](https://docs.cvat.ai/docs/dataset_management/formats/format-cvat/), [points annotation](https://docs.cvat.ai/docs/annotation/manual-annotation/shapes/annotation-with-points/) | F074; A06-S09. Docs displayed develop; exact совпадение с release не проверено. MIT community, cloud/enterprise отдельно |
| <a id="s060"></a>S060 | CVLab–EPFL, Multi-camera Pedestrian Videos; дата страницы неизвестна | [Data page](https://www.epfl.ch/labs/cvlab/data/data-pom-index-php/), calibration/GT/terms, `grid_to_tv` | F072; A06-S10. Research-use terms; архивы не скачивались |
| <a id="s061"></a>S061 | J. Sochor et al., BrnoCompSpeed; arXiv **v2 2018-05-09**, v1 2017-02-21 | [Abstract/metadata](https://arxiv.org/abs/1702.06441v2) | F073; A06-S11. Полный PDF не прочитан; цифры состава/GT из abstract |
| <a id="s062"></a>S062 | J. Sochor et al., BrnoCompSpeed repo SHA `3e142eff6469ef0fdbea7d1c4677b8d0448f11ac`, **2022-01-03T09:38:08Z** | [README](https://raw.githubusercontent.com/JakubSochor/BrnoCompSpeed/3e142eff6469ef0fdbea7d1c4677b8d0448f11ac/README.md), Download/How to use/output JSON | F073; A06-S12. Download asks contact author, старый tar URL не подтверждён; license UNKNOWN |

## Существенные ограничения доступа

- Официальный `КЕЙС_LinQ.pdf`, SDK, устройство и видео не были предоставлены; получение/чтение не заявляется. Правила вычислений остаются Q001/Q005.
- CVF SlowFast дал 403 → использована авторская arXiv-версия; MDPI Shin–Kim дал 429 → прочитан полный PDF той же публикации через зеркало. Это замены доступа, не новые независимые источники.
- Полная IJCV2000 версия Single View Metrology не получена → все её содержательные выводы привязаны к прочитанной ICCV1999 версии S022. Попытки ORA/Berkeley и отдельные tool timeouts не доказывают отсутствия публикации.
- EPFL/Brno data archives, модели/веса и GUI-бинарники не скачивались и не запускались. Brno landing page не открылась инструментом; author contact не выполнялся.
- Неуспешные URL и поисковые зацепки без прочитанного материала перечислены в исходных AGENT-файлах; они не используются как факты отсутствия технологии.
