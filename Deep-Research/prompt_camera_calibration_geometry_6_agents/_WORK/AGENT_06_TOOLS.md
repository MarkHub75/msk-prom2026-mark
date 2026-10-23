# Агент 06 — инструменты, воспроизводимость и validation

Дата проверки: 2026-10-23; начало зафиксировано `clock.curr_time`: 16:42:15 UTC / 19:42:15 Europe/Moscow. Одна поисковая волна, без дочерних агентов. Прочитаны `Context-prompt.md`, `prompt_camera_calibration_geometry_6_agents.md`, `_WORK/AGENT_PROMPTS.md`; специальный одноволновый процесс имеет приоритет. Результат этого агента — исследование и программа будущих измерений. Приложение, обучение, LinQ-запуск и benchmark не выполнялись.

## Практический выбор

**INFERENCE / A06-F01.** Для первого доказуемого MVP достаточно OpenCV для преобразования точек, Shapely для плоских зон/расстояний и заранее подготовленной разметки для проверки. Runtime трекера и инструмент разметки — отдельные зависимости; нейросетевая часть на LinQ остаётся условием кейса. Первые функции: запретная зона на фиксированной камере; измерение расстояния до статической зоны на проверенном участке пола; затем быстрое перемещение по траектории, если независимая проверка времени/локализации успешна. Наличие библиотек не доказывает точность этих функций на заводском видео.

**CODE_INSPECTED / A06-F02.** Нельзя записать `opencv-python-headless==4.13.0.92 + norfair==2.3.0` как готовый совместимый pip-стек на Python >=3.10: OpenCV metadata требует `numpy>=2`, Norfair `numpy ^1.23.0`, то есть `<2`. Это конфликт деклараций зависимостей, установленный чтением manifests; не результат установки. Совместимый lock, иной OpenCV build/версия или разнесение окружений требуют отдельного решения. Не обходить resolver через `--no-deps` как доказательство совместимости. [A06-S03, A06-S07]

**INFERENCE / A06-F03.** Самый полезный эталон — независимые измерения собственной сцены плюс целые позитивные и негативные эпизоды. EPFL пригоден для проверки coordinate bookkeeping и ground-plane localization; BrnoCompSpeed — пример независимого speed GT. Ни один не подтверждает промышленную безопасность и человеческий бег на нашей камере. [A06-S10–S12]

## Реестр первичных источников

Все источники проверены 2026-10-23; дата доступа не является датой публикации. Динамические docs без даты так и отмечены. Сохранённые исходники и package metadata находятся в `A06_EVIDENCE/` рядом с этим файлом. Содержимое пересказано, длинных цитат нет.

| ID | Источник, автор, дата/версия | Прямой адрес и прочитанный локатор | Статус и граница |
|---|---|---|---|
| A06-S01 | OpenCV project; releases page, динамическая дата публикации страницы неизвестна | https://opencv.org/releases/ — строки релизов 5.0.0 / 4.14.0 / 4.13.0; https://opencv.org/license/ — раздел 4.5.0 and higher | DOCUMENTED: на странице перечислены 5.0.0 (2026-08-19), 4.14.0 (2026-07-19), 4.13.0 (2025-12-31); проверенный tag 4.13.0 не latest; Apache-2.0 для OpenCV >=4.5 |
| A06-S02 | OpenCV contributors; tag 4.13.0, дата tag согласно S01 | https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html — Demo 2; https://raw.githubusercontent.com/opencv/opencv/4.13.0/samples/python/tutorial_code/features2D/Homography/perspective_correction.py — `perspectiveCorrection` | DOCUMENTED, CODE_INSPECTED: исходник скачан и прочитан, не запущен |
| A06-S03 | OpenCV Python packaging maintainers / PyPI; `opencv-python-headless==4.13.0.92` | https://pypi.org/pypi/opencv-python-headless/4.13.0.92/json — `info.requires_dist`, `requires_python` | CODE_INSPECTED metadata; сохранён JSON. Дата загрузки файлов есть в JSON; отдельную общую дату wheel-релиза здесь не утверждаем |
| A06-S04 | Sean Gillies and Shapely contributors; 2.1.2 released 2025-09-24 | https://pypi.org/project/shapely/2.1.2/ — requirements, license; https://shapely.readthedocs.io/en/2.1.2/index.html — Requirements; https://shapely.readthedocs.io/en/2.1.2/manual.html — Coordinate Systems, Geometric Objects, Polygons | DOCUMENTED: выбранная проверенная 2.1.2; это не latest, PyPI показывает 2.2.0. Manual dated 2025-09-24 |
| A06-S05 | Shapely contributors, API 2.1.2; отдельная дата страницы неизвестна | https://shapely.readthedocs.io/en/2.1.2/reference/shapely.contains.html ; https://shapely.readthedocs.io/en/2.1.2/reference/shapely.covers.html | DOCUMENTED: прочитаны определения и примеры с граничной точкой |
| A06-S06 | Shapely contributors, API 2.1.2; отдельная дата страницы неизвестна | https://shapely.readthedocs.io/en/2.1.2/reference/shapely.distance.html — definition/examples | DOCUMENTED: Cartesian distance; empty/None дают NaN |
| A06-S07 | Tryolabs; Norfair v2.3.0, 2025-04-30; commit `e517b4236f6b67a6ecf342f5df1fccb7788dbc54` | https://raw.githubusercontent.com/tryolabs/norfair/v2.3.0/pyproject.toml ; https://raw.githubusercontent.com/tryolabs/norfair/v2.3.0/LICENSE ; https://pypi.org/project/norfair/2.3.0/ — installation/demos/features | CODE_INSPECTED manifests/LICENSE, DOCUMENTED usage. GitHub API commit date 2025-04-30T17:04:22Z; source files saved |
| A06-S08 | Yifu Zhang et al.; original ByteTrack, ECCV 2022; repo main resolved `d1bf0191adff59bc8fcfeaa0b33d3d1642552a99`, 2022-12-11T07:05:00Z | https://github.com/FoundationVision/ByteTrack ; https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/byte_tracker.py ; https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/requirements.txt ; https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/LICENSE | CODE_INSPECTED `STrack.__init__`, `BYTETracker.__init__/update`, requirements, MIT license; README installation прочитан; не запущено |
| A06-S09 | CVAT.ai / Intel; CVAT Community v2.80.0; release 2026-10-21T16:34:20Z; commit `bb0a873fe071e70d71458cd82127052025e05807` | https://github.com/cvat-ai/cvat/releases/tag/v2.80.0 ; https://github.com/cvat-ai/cvat/blob/v2.80.0/LICENSE ; https://docs.cvat.ai/docs/getting_started/overview/ ; https://docs.cvat.ai/docs/dataset_management/formats/format-cvat/ — Interpolation XML; https://docs.cvat.ai/docs/annotation/manual-annotation/shapes/annotation-with-points/ | DOCUMENTED: release/license, points and track XML, `frame`, `outside`, `occluded`, `keyframe`. Docs открылись как develop; это не проверка их полного совпадения с v2.80.0 |
| A06-S10 | CVLab–EPFL, Multi-camera Pedestrian Videos; дата страницы неизвестна | https://www.epfl.ch/labs/cvlab/data/data-pom-index-php/ — calibration, Ground truth, terms; `grid_to_tv` | DOCUMENTED: ground-plane GT и calibration, research-use terms; данные не скачивались |
| A06-S11 | Jakub Sochor, Roman Juránek, Jakub Špaňhel, Lukáš Maršík, Adam Široký, Adam Herout, Pavel Zemčík; arXiv v1 2017-02-21, v2 2018-05-09 | https://arxiv.org/abs/1702.06441v2 — abstract, submission history, authors | DOCUMENTED / REPORTED_EXPERIMENT: прочитан abstract и metadata, полный PDF не исследован; точность опубликованных методов здесь не извлекалась |
| A06-S12 | Jakub Sochor et al.; BrnoCompSpeed repo `3e142eff6469ef0fdbea7d1c4677b8d0448f11ac`, 2022-01-03T09:38:08Z | https://github.com/JakubSochor/BrnoCompSpeed ; https://raw.githubusercontent.com/JakubSochor/BrnoCompSpeed/3e142eff6469ef0fdbea7d1c4677b8d0448f11ac/README.md — Download, How to use, output JSON | CODE_INSPECTED README; неизвестны окончательные условия лицензии dataset/code, не записывать как MIT. Официальная dataset-страница https://medusa.fit.vutbr.cz/traffic/research-topics/traffic-camera-calibration/brnocompspeed/ не открылась web-инструментом |

Русскоязычный поиск выполнен запросом «калибровка камеры гомография пример OpenCV контроль расстояния». Он нашёл, в частности, русскую геодезическую статью, но не добавил более пригодного первичного воспроизводимого CCTV-кода; выводов по её сниппету не делаем. Основные технические основания — оригинальная документация и исходники выше.

## Ограниченный shortlist библиотек

| Компонент | Проверенная версия / лицензия | Реальная роль и runtime | Решение и ограничения |
|---|---|---|---|
| OpenCV | source tag 4.13.0; Apache-2.0; Python wheel отдельно 4.13.0.92 | геометрия/преобразование точек и визуальное наложение, CPU; `perspective_correction.py` показывает findHomography и warpPerspective | Основа. Wheel != source version; фиксировать полный package build. Для сервера выбирать один GUI/headless пакет после проверки decoder/backend. CUDA для этой геометрии не требуется. S01–S03 |
| Shapely | 2.1.2; BSD-3-Clause; dependency GEOS LGPL-2.1 | Point/Polygon, distance, contains/covers, проверка topology; Python >=3.10, GEOS >=3.9, NumPy >=1.21 | Основа плоских правил. Версию GEOS и его notice сохранять отдельно. Не 3D/CRS engine. На stable уже 2.2.0 с другими требованиями; фиксировать именно проверенную версию. S04–S06 |
| Norfair | v2.3.0; BSD-3-Clause; Python ^3.8 | tracker поверх переданных detections/keypoints; NumPy/SciPy/FilterPy/Rich; базовый tracker не требует GPU | Кандидат, не часть подтверждённого общего lock. `opencv-python` optional extra <5.0, NumPy ^1.23. На демо часто нужен GPU для detector — это не требование самого tracker. MotionEstimator не восстанавливает метрическую калибровку камеры автоматически. S07 |
| Original ByteTrack | commit S08; MIT | ассоциация boxes включая low-score detections; в прочитанном tracker импорт torch, в requirements также onnx/onnxruntime/onnx-simplifier старых версий | Альтернатива при наличии готового адаптера. `np.float` в STrack, непинованные dependencies, frame-based buffer требуют проверки. Не рекомендовать прямую установку repo как минимальную новую CPU-среду. Лицензия оригинала не переносится автоматически на Ultralytics implementation. S08 |
| CVAT Community | v2.80.0; MIT для community code | отдельное средство ручной разметки: точки контакта, track IDs, зоны, occlusion; экспорт сохраняет кадры/атрибуты | Подготовка GT, не обязательная runtime-зависимость сервиса. Время кадра в XML не равно source PTS: отдельная таблица frame→PTS обязательна. Docker/ресурсы self-hosting и ограничения конкретного формата проверить до установки. Enterprise/cloud имеют другие условия. S09 |

**CODE_INSPECTED / A06-F04.** В ByteTrack `BYTETracker.update()` принимает boxes+scores, масштабирует boxes через `img_info/img_size`, увеличивает `frame_id` на единицу; buffer зависит от `frame_rate`. Поэтому адаптер должен явно определить, координаты уже восстановлены после letterbox или ещё нет. Двойное масштабирование ломает H, а frame-based track lifetime нельзя считать временем источника при нерегулярной выборке. `np.float` и imports — наблюдения по одному commit, не утверждение обо всех портах ByteTrack. [A06-S08]

**INFERENCE / A06-F05.** CPU-geometric processing не требует PyTorch как математический принцип, но выбранный tracker-пакет способен добавить его как зависимость. До получения LinQ SDK наиболее экономный контракт — экспортированный список детекций с привязкой к исходному кадру; MVP-демонстрацию геометрии можно проверить на ручных track IDs, явно обозначив, что end-to-end tracking ещё не доказан.

## Точная семантика зон и расстояния

**DOCUMENTED / A06-F06.** Shapely работает в x-y плоскости; Z не участвует в geometric analysis. `Point` и `Polygon` должны находиться в общей Cartesian системе. Если переданы пиксели, distance даёт пиксельное расстояние; если координаты пола измерены в метрах, результат в метрах. Shapely сама не калибрует камеру. Валидность Polygon не гарантируется конструктором. [A06-S04]

**DOCUMENTED / A06-F07.** Для точки на внешней границе `contains(zone, point)` false, `covers(zone, point)` true. Выбрать одну семантику при описании правила, проверить отверстия и касания, сохранять boundary policy в config. Это топологическое определение, а не допуск измерительной ошибки. [A06-S05]

**DOCUMENTED + INFERENCE / A06-F08.** `distance(a,b)` — Cartesian minimum distance; внутри/при пересечении заполненного polygon расстояние равно нулю. Это не signed distance до границы. Для глубины проникновения нужна отдельно boundary + знак по predicate. Empty geometry/None могут дать NaN; NaN не интерпретировать как «безопасно». Самопересечение зоны исправлять только после проверки человеком: автоматический make-valid способен изменить смысл участка. [A06-S06; A06-S04]

Предлагаемая трёхстатусная инженерная политика (INFERENCE): для estimate distance `d_hat`, validation-derived bound `epsilon_d`, danger limit `D`, оценивать интервал `[max(0,d_hat-epsilon_d), d_hat+epsilon_d]`. Entire interval ниже `D` — подтверждённое proximity по выбранной модели; entire interval выше `D` — proximity не обнаружено при достаточной наблюдаемости; пересекает `D` — неопределённость. Правило включения границы согласовать отдельно. Это не вероятностная уверенность, если epsilon — эмпирический допуск. Реальное нарушение дополнительно зависит от работы механизма/допуска. Для зоны аналогичная неопределённая полоса около boundary; её ширина выводится из проверок глубины/видимости, а не одна на все камеры.

## Два primary примера и смысл ground truth

**CODE_INSPECTED / A06-F09 — OpenCV perspective demo.** S02 обнаруживает углы шахматных досок в двух видах, строит H, warp и линии соответствий с homogeneous normalization. Это компактный официальный материал для smoke check direction/normalization. Второй вид — изображение, а не измеренная метрическая плоскость; красивое исправление перспективы не является подтверждением масштаба. В нашем recipe destination points задаются в метрах и добавляется независимый hold-out. Исходник использует imshow/waitKey, поэтому GUI demo нельзя без изменений назвать headless-серверным pipeline. Скачан и прочитан, не запущен.

**DOCUMENTED / A06-F10 — EPFL.** S10 даёт calibrated synchronized views и ground-plane GT для части записей; GT — дискретная сетка, с шагом разметки в заголовке и кодами undefined/out-of-grid. Требуется точная calibration и размер изображения; image→topview H ещё требует правильной интерпретации единиц. Research-use terms — не безусловная лицензия на коммерческую демонстрацию. Одна camera view с предоставленной GT полезна для coordinate/visibility tests, но label-grid quantization и sparse timing не дают эталон непрерывной скорости. Просьба использовать эти записи в питче требует отдельного выяснения условий. Dataset не скачан, единицы всех файлов не проверены.

**DOCUMENTED / REPORTED_EXPERIMENT / A06-F11 — BrnoCompSpeed.** Abstract S11 сообщает 18 примерно часовых Full-HD видео с шести мест, 20 865 vehicle instances, speed GT через оптические ворота с LiDAR и проверку несколькими reference GPS tracks. Это пример внешнего измерительного эталона. README S12 требует Python 2 и NumPy/SciPy/Matplotlib/Tabulate для старого evaluator, JSON road-plane positions и calibration scale; актуальный раздел Download просит связаться с автором. Старый tar URL, оставшийся в README, не доказывает текущую доступность данных. Публикация не содержит industrial person/forklift violation GT. Не переносить vehicle-speed accuracy на людей или наш зал.

Различие 18/6 из paper и 21/7 во вторичных пересказах не разрешать молча добавлением видео: в отчёте принимается только явно прочитанная спецификация S11; README упоминает дополнительную session0, но её состав здесь не измерен. Нужна версия реально полученного архива.

## Минимальный демонстрационный набор (предложение, не выполнено)

1. **Scene fixture.** Один неизменный кадр камеры; raw resolution, crop/ROI, camera ID и hash файла. Разделить surveyed correspondences на fit и control до оценки. Охватить ближний/дальний/боковые участки; подтверждённая mask ограничивает применение H.
2. **Geometry-only check.** На ручных точках пола показать image+topview и ошибки hold-out координат/отрезков. Не участвуют detector и tracker: иначе источник ошибки нельзя локализовать.
3. **Visible movement.** Безопасная запись прохода по измеренному маршруту, независимые time gates/датчик или другой согласованный эталон. Для человека определить физическую GT-точку и интервал скорости; gate average нельзя сравнивать с мгновенной frame derivative как одинаковые величины.
4. **Explainable event.** Вход/выход зоны с source timestamps, границей и policy, уровнем видимости. Показать один разрешённый проход рядом с механизмом и один эпизод, удовлетворяющий согласованному правилу, без создания реальной опасности.
5. **Honest failure.** Закрыть ноги препятствием либо показать переход на другую плоскость; система указывает indeterminate и причину. Затем показать смещение камеры/зум как invalid calibration, а не продолжать выдавать метры.
6. **Replay.** Те же video/config/detections hashes дают те же геометрические решения; inference outputs должны быть реально с LinQ для claim об end-to-end LinQ. Ручная GT/предзаписанные detections допускаются для раздельного доказательства алгоритма, с соответствующей подписью.

Демо доказывает конкретную цепочку на конкретном материале, а не надёжность на предприятии, предотвращение травм или метрическую реконструкцию произвольных объектов.

## Программа измерений: сначала отделить источники ошибок

Все далее `A06-E*` — **HYPOTHESIS / proposed experiments**, не выполненные эксперименты. Acceptance задаётся символическими бюджетами и договорённостями; численные accuracy/универсальные пороги не назначаются.

| ID / вопрос | Входы и дизайн | Метрика | Смысл успешного результата | Чего успех не доказывает |
|---|---|---|---|---|
| A06-E01 reproducible environment | ОС/архитектура/Python сервера, exact wheels+hashes; resolver/lock отдельно от LinQ SDK; tiny import and API checks | dependency conflict, импорт, воспроизводимый lock, cv2/shapely/GEOS versions | заявленные функции реально доступны в целевой среде | скорость, точность, исполнение модели на LinQ |
| A06-E02 H coordinate-only | surveyed fit/control points; независимые physical coordinate measurements; raw/undistorted coordinate convention | position MAE/RMSE, median/P95/max, signed X/Y bias по near/mid/far и границам mask | ошибки в принятых бюджетах на support region, направление и единицы корректны | качество feet localization и points вне пола |
| A06-E03 distance-only | hold-out отрезки разных длин, ориентаций, глубин, pair/zone distances | absolute error в m, relative error только при meaningful ненулевых GT; threshold-near confusion | выбранная distance formulation пригодна у порога | произвольное surface clearance в 3D |
| A06-E04 detector contribution | manual visible foot contacts vs predicted point/pose/bbox на тех же кадрах, frozen H | pixel error и projected world error; coverage по visibility; paired delta относительно E02 | известна добавка локализации к ошибке | работа при скрытых ногах или другой обуви/ракурсе |
| A06-E05 trajectory/speed | независимое время и позиция/скорость; frozen config; проходы по разным направлениям/глубинам | speed MAE/bias/P95 на одинаковом interval, ID switches, broken tracks, valid-window coverage | physical speed error оценён на определённых интервалах | биомеханический «бег», краткое ускорение между samples |
| A06-E06 event quality | целые episodes normal/violation; blinded labels; rules context; отдельные sessions test | one-to-one event P/R/F1, FP/camera-hour, onset timing error, duplicates/event | известна пригодность правила на подписанном test domain | редкие unseen hazards, безопасность производства |
| A06-E07 abstention | full episodes включая visibility failure и invalid calibration; label eligible/observable независимо от model | abstention fraction, valid decision coverage, errors by reason, event recall всех GT и только observable GT | indeterminate не скрывает пропуски; usable coverage известна | корректность индикатора «нет опасности» вне eligible interval |
| A06-E08 robustness | lighting, occlusion, jitter camera, zoom/resize/crop, new plane; controlled one-variable changes | degradation по E02–E07, stale-calibration detection miss/delay | известны failure envelope и корректность отказа | автоматическая метрическая рекалибровка после любого сдвига |
| A06-E09 sampling | один full-source baseline, заданные sampling schedules включая 1 FPS, несколько phase offsets, gap/stale/drop tests | event recall, onset delay, speed error, tracking/coverage; real source time | видно, какие события переживают sampling | что высокая per-frame precision компенсирует невидимые events |
| A06-E10 LinQ boundary | actual SDK/output format/device/rules, uploaded video и model manifest | matching frames/coordinates, factual device execution logs, end-to-end latency | конкретная модель и интерфейс действительно работают в target | поддержка всех моделей/операторов/прочих режимов |

### Определения ошибок и неопределённости

**INFERENCE / A06-F12.** Для GT `p_i` и mapped estimate `p_hat_i` ошибка положения `e_i=||p_hat_i-p_i||_2`, MAE `mean(e_i)`, RMSE `sqrt(mean(e_i^2))`. Сохранять signed component bias, quantiles, N и raw residuals. Среднее всей сцены может спрятать дальний участок; report по depth/image regions и внутри/снаружи fit support. P95 при малой выборке нестабилен — показывать число независимых точек/эпизодов и максимум, не изображать строгую гарантию.

Для пары GT distance `d` и estimate `d_hat`: `e_d=abs(d_hat-d)`; отдельно ошибка положения обоих объектов, polygon/footprint definition и ошибки survey. Для скорости согласовать interval definition, затем `MAE_v=mean(abs(v_hat-v_GT))`; избегать pseudo-GT из той же H/того же tracker.

Если `e_a,e_b` — векторные ошибки объектов, то `Cov(e_a-e_b)=Sigma_a+Sigma_b-Cov(e_a,e_b)-Cov(e_b,e_a)`. Общая калибровка вызывает коррелированные ошибки: независимое сложение двух variance не обосновано. Common translation может сократиться в pair distance, scale/projective bias — сохраняется. Для temporal displacement та же проблема: static calibration bias не равен независимому новому шуму каждого кадра.

Proposed uncertainty study: повторить ручные clicks разными операторами/в разные моменты; perturb fit coordinates в диапазоне измеренной survey/click uncertainty; для каждой perturbation пересчитать одну H и весь набор траекторий совместно. Так сохраняется общий источник ошибки. Synthetic perturbations измеряют sensitivity при заданной модели ошибок, не дают автоматически calibrated confidence interval. Эмпирические epsilons проверять на отдельном наборе; softmax detector score не является error bar в метрах.

### GT и разбиение

**INFERENCE / A06-F13.** Разметка через ту же H может быть хорошей reference annotation в данной системе, но не независимой проверкой её метрического масштаба. Hold-out physical marks должны иметь внешний survey. На скорости полезны optical gates/другой независимый измеритель с известным timing/position uncertainty. Рулетка и секундомер дают только average по своему интервалу; точность такого эталона также фиксируется.

Сохранить отдельные множества: calibration-fit, calibration-validation, rule-development, final-test episodes. Если по controls изменили H, это development set, нужен новый hold-out. Не дробить соседние кадры одной траектории между train/tune/test; разделять полные траектории/сессии/камеры в зависимости от утверждаемой переносимости. Bootstrap/error intervals делать по независимым sessions/cameras или episodes, не по коррелированным соседним кадрам. Для одной камеры вывод ограничен ей.

Для аннотаторов: инструкции о точке контакта и плоскости; отдельные labels visible/occluded/outside-support/unknown; механический state/authorized worker когда требуется; события с onset/offset и границами неопределённости. CVAT interpolation — удобство, не фактическое наблюдение каждого промежуточного положения. Проверить keyframes возле границы/ускорения/окклюзии; не присваивать hidden foot точные координаты без основания. Часть спорных эпизодов размечают два человека, disagreement сохраняется и разрешается по заранее заданной процедуре. [A06-S09]

### Event matching и ложные тревоги

**INFERENCE / A06-F14.** До test зафиксировать: event class, camera/zone, participant identity mapping, onset/offset, минимальные durations, правила merge/cooldown, правила matching и boundary policy. Model track ID не должен быть обязательным буквальным равенством GT ID: нужна association. Предлагаемое matching — one-to-one среди одинаковых class/camera/zone/participants по temporal IoU `|I_pred∩I_GT|/|I_pred∪I_GT| >= tau`, где tau заранее согласован; для точечного crossing — onset tolerance вместо произвольно раздутого interval. Не менять matching после просмотра test.

Непарные GT — FN; непарные predicted events — FP. Дубликаты одного GT не повышают TP; отдельно показать duplicate alarms/event. `Precision=TP/(TP+FP)`, `Recall=TP/(TP+FN)`. Указывать случаи zero denominator, не подставлять молча идеальное качество. Event boundaries с ambiguities учитывать явно.

`FAR=FP / camera-hours`. Часы — часы исходного наблюдаемого видео, а не inference wall-time и не сумма человеко-часов; две камеры по часу дают 2 camera-hours. Показать два denominators: все пригодные по protocol часы и часы фактического валидного monitoring, плюс downtime/abstention. Длинные отказы нельзя улучшать FAR без раскрытия coverage. На negative-only clips отдельно FP/negative-camera-hour; не смешивать без маркировки с full timeline FAR. Нулевые FP на коротком видео не доказывают нулевую вероятность тревог в эксплуатации.

Считать recall на всех annotated GT и дополнительно conditional recall на independently observable GT, с числом excluded/abstained событий. Отказ по опасному эпизоду не превращать в TN. Coverage — duration(valid decisions)/duration(eligible monitoring); также доля событий с достаточным coverage. Pixel masking, низкое качество трека и stale calibration — разные reasons.

### Время и latency

**INFERENCE / A06-F15.** Event onset timing error измеряется в source-time: `t_pred_onset_source - t_GT_onset_source`. Для офлайн файла wall-clock появления тревоги не равен задержке относительно события в реальном времени. Отдельно показать media-time detection delay, очередь/decode/inference/rule/display wall-time и фактический replay rate. Source PTS сохраняется от декодера до события; scheduling/inference timestamps сохраняются дополнительно. При gap нельзя выводить отсутствие короткого события из отсутствия sample.

### Acceptance budgets

**HYPOTHESIS / A06-F16.** До эксперимента согласовать `B_pos(region)`, `B_dist(region)`, `B_speed(interval)`, минимальный event recall, допустимый FAR, latency budget, минимальный coverage. Они следуют из конкретного правила/порога и цели оператора; здесь чисел нет. Успешная метрика на тесте сравнивается с этими заранее заданными бюджетами и uncertainty эталона. Если дальний участок не проходит, сократить validity mask или перейти к image-zone-only; если feet скрыты, отказаться от метрического вывода; если transient пропадает при 1 FPS, повысить temporal sampling/изменить claim. Post-hoc подобранный budget — гипотеза следующей проверки.

## Условная граница LinQ + CPU и конфигурация

**UNKNOWN / A06-F17.** LinQ SDK, model outputs, формат timestamps, фактическое разрешение CPU tracking/rules и ресурсы сервера недоступны. Не найден/не исследован полный кейс PDF; устные сведения команды не становятся официальной спецификацией. Ни лицензии, ни CPU-реализуемость geometry не отвечают на регламент конкурса.

**HYPOTHESIS / recipe.** Если правила разрешают CPU postprocessing и SDK возвращает coordinates, uploaded video декодируется на сервере; LinQ запускает единственную согласованную нейросетевую модель; CPU снимает letterbox/crop transform один раз, связывает detections с source frame/PTS, ведёт tracker (если среда разрешена), переводит contact points на floor, применяет planar rules и журналирует события. При недоступных outputs нельзя обещать эту схему: потребуется документированный иной интерфейс. Любые embeddings/pose/depth/ReID — отдельный neural inference, не называть CPU geometry способом скрыто обойти обязательный LinQ.

Минимальный versioned config (проектное предложение): `schema_version`, `camera_id`, `source_resolution`, `crop_roi`, `resize_letterbox_transform`, `coordinate_domain(raw|undistorted)`, `calibration_frame_hash`, `K/distortion_if_used`, `H_direction`, `world_units`, `fit_points`, `control_points/separate_reference`, `validity_mask`, `zone_coordinate_space`, `zone_polygons`, `boundary_policy`, `rule_version/thresholds`, `uncertainty_policy`, `created_at`, `camera_state`, `software_lock_hash`. На событии: config/model/runtime IDs, original frame IDs+PTS, input detections/points, transformed values, rule reason, visibility state, evidence frames. Не хранить только screenshot с bbox и итоговым красным цветом.

Replay package: hashes исходного видео/конфига/разметки/вывода LinQ, exact environment (OS, Python, wheels, GEOS, cv2 build/backends), command/parameters и sampling schedule с seed/phase. Детерминированный replay геометрии поверх зафиксированных detections отдельно от возможной nondeterministic inference. Реальное device execution подтверждать runtime artifacts, а не названием model file.

## Приоритетные открытые вопросы и адресная передача

| ID | Вопрос / почему меняет решение | Способ закрыть |
|---|---|---|
| A06-Q01 | Разрешены ли CPU tracking/rules и формат model outputs/coordinate convention? Без ответа LinQ recipe условен | полный PDF кейса, SDK example, ответ постановщика; → linq_platform/video_architecture |
| A06-Q02 | Какие реальные fixed camera clips, размеры пола и независимые контрольные точки доступны? | получить кадры+survey; → агент 01/02; иначе only image-zone MVP |
| A06-Q03 | Нужен ли tracker в той же Python-среде, что OpenCV/LinQ? | dependency resolver на фактическом Python; конфликт NumPy S03/S07; → model_stack/video_architecture |
| A06-Q04 | Что именно считается реальным нарушением рядом с оборудованием и какие разрешённые операции есть? | согласовать event ontology, machinery state, hard-negative labels; → агент 04/evaluation/operator_product |
| A06-Q05 | Какой независимый speed GT и source-time mapping возможен? | gates/sensor и frame→PTS table; → агент 03; не использовать output tracker как собственный GT |
| A06-Q06 | Можно ли использовать research datasets публично в питче/продукте? | конкретные terms архивов/разрешения; EPFL research use, Brno license UNKNOWN; → datasets |
| A06-Q07 | Какие budgets/FAR/coverage и minimum observed durations нужны оператору? | согласование перед test и получение достаточного negative camera-hours; → evaluation/operator_product |

Передача соседям внутри этой волны: агенту 01 — geometry-only vs contact-localization error и correlated uncertainty; агенту 02 — boundary policy и invalidation reason/config fields; агенту 03 — interval-consistent speed GT и sampling phase offsets; агенту 04 — event ontology и разрешённые работы; агенту 05 — Z игнорируется Shapely, indeterminate включать в coverage. Оркестратору заранее переданы найденные несовместимости dependencies и ограничение EPFL/Brno GT.

## Фактическое выполнение и остаточные ограничения

Выполнены реальные web.search (русский/английский), web.open первичных docs, чтение original code/metadata через HTTPS, разрешение commit SHA GitHub API, сохранение перечисленных исходников. Начальный UTF-8 файл PowerShell показал mojibake; повторно прочитан с `-Encoding UTF8`. Отдельные большие чтения были обрезаны инструментом, необходимые части повторно прочитаны диапазонами. Метки CODE_INSPECTED относятся к прочитанным файлам, не к исполнению.

Не выполнялись pip installation/resolver, import smoke tests, GUI demos, скачивание датасетов/видео, survey, геометрический benchmark, обучение, inference, LinQ доступ, систематический поиск industrial field deployment. Следовательно, measured local accuracy и target throughput здесь **UNKNOWN**. Поиск закончился содержательным shortlist и точно заданными проверками; дополнительные независимые агенты/вторая волна не создавались.