# Агент 02 — полуавтоматическая калибровка и calibration wizard

Проверено: 2026-10-23; время начала зафиксировано `clock.curr_time`: **16:34:51 UTC / 19:34:51 Europe/Moscow**. Одна исследовательская волна; субагенты не создавались. Прочитаны полностью `Context-prompt.md`, `prompt_camera_calibration_geometry_6_agents.md`, общие инструкции и секция агента 02 в `_WORK/AGENT_PROMPTS.md`. Специальный одноволновый конвейер имеет приоритет над историческим общим.

## Практический ответ

Команде стоит готовить два режима подключения: **зона в изображении без метрических обещаний** и **метрическая плоскость пола по измеренным соответствиям с независимой приёмкой**. Автоматизация полезна для поиска углов эталона, предложений линий перспективы, предварительной оценки оптики и предупреждения о сдвиге камеры. Масштаб и соответствие эталона реальному полу должен подтвердить интегратор. Предлагаемый ниже wizard — наша проектная процедура, а не найденное готовое промышленное приложение.

Реальные инструменты найдены: OpenCV с образцами калибровки, Calibmar с GUI для параметров камеры, fSpy с интерактивными точками схода и эталонным расстоянием, GeoCalib с авторским Gradio/webcam demo. Они решают разные подзадачи. Ни один из прочитанных источников не доказывает готовность универсального wizard «любой промышленный кадр → точные метры → безопасные события», совместимость с LinQ или точность на наших камерах.

Обозначения: `DOCUMENTED` — первичная документация/публикация; `CODE_INSPECTED` — прочитан конкретный исходный файл; `LOCAL_OBSERVATION` — выполнено здесь; `INFERENCE` — инженерный вывод; `HYPOTHESIS` — предлагаемая проверка; `UNKNOWN` — не установлено. Измерений точности и запусков CV/GUI в этой работе **не было**.

## Источники и точные локаторы

Все URL ниже открыты и прочитаны 2026-10-23. Дата доступа не является датой публикации. Для незакреплённых страниц документации дата публикации неизвестна, если не указано иное.

| ID | Автор / первоисточник | Версия и дата материала | Прямой URL и прочитанный локатор | Что поддерживает / предел |
|---|---|---|---|---|
| A02-S01 | OpenCV contributors | Документация **4.12.0**, release 2025-07-02; HTML generated 2025-07-03 | [Calibration with ArUco and ChArUco](https://docs.opencv.org/4.12.0/da/d13/tutorial_aruco_calibration.html), вводная и Calibration with ChArUco Boards; пример `CharucoDetector`, `matchImagePoints`, `calibrateCamera` | A02-F01; калибровка intrinsics/distortion по нескольким видам; не доказательство world-plane calibration |
| A02-S02 | OpenCV contributors | 4.12.0; дата отдельного текста неизвестна | [Detection of ChArUco Boards](https://docs.opencv.org/4.12.0/df/d4a/tutorial_charuco_detection.html), Board Creation, Detection, Pose Estimation, note after 4.6.0 | A02-F02; параметры эталона, частичная видимость, версия системы координат |
| A02-S03 | Bernát Gábor / OpenCV | 4.12.0; дата отдельного текста неизвестна | [Camera calibration With OpenCV](https://docs.opencv.org/4.12.0/d4/d94/tutorial_camera_calibration.html), Goal, Source code, Explanation; образец `samples/cpp/tutorial_code/calib3d/camera_calibration/` | A02-F03; реальное оконное sample-приложение с видео/камерами/списком файлов и XML/YAML; не web zone editor |
| A02-S04 | AprilRobotics / University of Michigan | **v3.4.5**, release **2025-08-29** | [README](https://raw.githubusercontent.com/AprilRobotics/apriltag/v3.4.5/README.md), Install, Tuning, Pose Estimation, Coordinate System; [apriltag_pose.h](https://raw.githubusercontent.com/AprilRobotics/apriltag/v3.4.5/apriltag_pose.h), `apriltag_detection_info_t`, `estimate_tag_pose_orthogonal_iteration`, `estimate_tag_pose` | A02-F04; размеры и intrinsics нужны для метрической pose, возможны два решения planar pose; библиотека не calibration wizard |
| A02-S05 | AprilRobotics | v3.4.5 | [LICENSE.md](https://raw.githubusercontent.com/AprilRobotics/apriltag/v3.4.5/LICENSE.md) | BSD-2-Clause; лицензия библиотеки, не гарантия аппаратной совместимости |
| A02-S06 | Per Gantelius / fSpy | Страницы basics/tutorial без даты; закреплённый код **v1.0.3**, release **2019-01-02** | [Basics](https://fspy.io/basics/), Vanishing points / Perpendicular directions / Limitations; [Tutorial](https://fspy.io/tutorial/), reference distance / principal point / single VP; [solver.ts](https://raw.githubusercontent.com/perarnia/fSpy/v1.0.3/src/gui/solver/solver.ts), `DEFAULT_CAMERA_DISTANCE_SCALE`, `solve1VP`, `computeTranslationVector` | A02-F05; интерактивная перспектива и внешний масштаб; approximation и pinhole assumptions |
| A02-S07 | fSpy authors | v1.0.3; stable release metadata 2019-01-02T07:42:50Z | [Release](https://github.com/perarnia/fSpy/releases/tag/v1.0.3), [API metadata](https://api.github.com/repos/perarnia/fSpy/releases/tags/v1.0.3), [LICENSE](https://raw.githubusercontent.com/perarnia/fSpy/v1.0.3/LICENSE), copyright header `solver.ts` | A02-F06; GPL-3.0-or-later по заголовку кода. GitHub `stuffmatic/fSpy` перенаправляет в `perarnia/fSpy`; код не следует копировать, считая его permissive |
| A02-S08 | Felix Seegräber, Mengun She, Felix Woelk, Kevin Köser / Kiel University | Calibmar **1.1.0**; commit **5c5a8200b42b22bac4e1ff62d066c1373a5ce57b**, 2026-08-03; docs ©2025, точная дата каждой страницы неизвестна | [Camera calibration](https://mdskiel.github.io/calibmar_documentation/camera_calibration.html), Workflow / FAQ; [Report](https://mdskiel.github.io/calibmar_documentation/calibration_report_format.html); [Changelog](https://mdskiel.github.io/calibmar_documentation/changelog.html); [CMakeLists](https://raw.githubusercontent.com/MDSKiel/calibmar/5c5a8200b42b22bac4e1ff62d066c1373a5ce57b/CMakeLists.txt) | A02-F07; реально документированная GUI-калибровка камеры и экспорт отчёта, не метрические зоны безопасности |
| A02-S09 | Calibmar / Kiel University | Тот же commit | [file_calibration_dialog.cpp](https://raw.githubusercontent.com/MDSKiel/calibmar/5c5a8200b42b22bac4e1ff62d066c1373a5ce57b/src/app/ui/dialogs/file_calibration_dialog.cpp), constructor / `Validate` / `ImportParameters`; [LICENSE.txt](https://raw.githubusercontent.com/MDSKiel/calibmar/5c5a8200b42b22bac4e1ff62d066c1373a5ce57b/LICENSE.txt); [original repository](https://github.com/MDSKiel/calibmar) README | A02-F08; BSD-3-Clause для Calibmar, зависимости отдельно; GitHub — зеркало, бинарные releases на университетском GitLab |
| A02-S10 | Alexander Veicht, Paul-Edouard Sarlin, Philipp Lindenberger, Marc Pollefeys / ETH Zurich, Microsoft | GeoCalib, ECCV 2024; arXiv v1 2024-09-10, **v2 2024-10-17** | [Полный HTML статьи](https://arxiv.org/html/2409.06704v2), §3 Camera calibration, §3.2 uncertainty, Appendix C; [история версий](https://arxiv.org/abs/2409.06704) | A02-F09; gravity / focal / distortion, не floor scale. Benchmarks автора не заменяют промышленный тест |
| A02-S11 | cvg / GeoCalib authors | commit **1dedb29f94fc11b896c5f572005978aeebccd67f**, 2026-10-14 | [README](https://github.com/cvg/GeoCalib), Camera models / License; [extractor.py](https://raw.githubusercontent.com/cvg/GeoCalib/1dedb29f94fc11b896c5f572005978aeebccd67f/geocalib/extractor.py), `GeoCalib.__init__`, `_post_process`, `calibrate`; [gradio_app.py](https://raw.githubusercontent.com/cvg/GeoCalib/1dedb29f94fc11b896c5f572005978aeebccd67f/gradio_app.py), `format_output`, UI construction; [LICENSE-WEIGHTS](https://raw.githubusercontent.com/cvg/GeoCalib/1dedb29f94fc11b896c5f572005978aeebccd67f/LICENSE-WEIGHTS) | A02-F10; есть исходный GUI и uncertainties; Apache-2.0 code, CC-BY-4.0 weights; LinQ export не проверен |
| A02-S12 | A. Criminisi, I. Reid, A. Zisserman / Oxford | **ICCV 1999** conference paper; не путать с расширенной IJCV 2000 статьёй | [Single View Metrology, авторский PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/1999/01/Criminisi_iccv1999.pdf), abstract, §2 Geometry, §3 algebraic representation, §4 error propagation | A02-F11; отношения и scale ambiguity при геометрических предпосылках; не универсальное извлечение 3D |
| A02-S13 | OpenCV contributors | 4.12.0 | [Object Tracking](https://docs.opencv.org/4.12.0/dc/d6b/group__video__track.html), `findTransformECC` docs | A02-F12; image alignment для предложенного drift monitor, не метрическая сертификация |
| A02-S14 | OpenCV contributors | 4.12.0, release 2025-07-02T12:48:11Z | [calib3d model introduction](https://docs.opencv.org/4.12.0/d9/d0c/group__calib3d.html), intrinsics reuse / image scaling; [LICENSE](https://raw.githubusercontent.com/opencv/opencv/4.12.0/LICENSE); [release API](https://api.github.com/repos/opencv/opencv/releases/tags/4.12.0) | A02-F13; Apache-2.0 для закреплённого OpenCV. Это выбранная проверенная версия, не утверждение о latest на дату исследования |

## Извлечённые факты и значение

### A02-F01 — калибровка объектива и калибровка пола — разные процедуры

`DOCUMENTED` A02-S01. OpenCV определяет здесь calibration как получение внутренних параметров и коэффициентов дисторсии по соответствиям, снятым с разных точек зрения. Для фиксированной камеры можно двигать эталон. ChArUco допускает частичную видимость; авторы рекомендуют его углы вместо менее точных углов обычных ArUco markers. API примера: `CharucoDetector::detectBoard`, `CharucoBoard::matchImagePoints`, `calibrateCamera`.

`INFERENCE`: даже идеально известные K и distortion не задают положение пола в мировой системе. После калибровки объектива нужен отдельный этап scene/floor mapping. Если эталон перемещали в руках перед камерой, его положение в каждом кадре не становится координатной системой пола.

### A02-F02 — известный эталон сокращает ручную разметку, но требует точной спецификации

`DOCUMENTED` A02-S02. ChArUco задаётся количеством квадратов по X/Y, длиной квадрата, длиной маркера, словарём и IDs; pose требует intrinsics. Не все визуально видимые углы обязательно восстанавливаются при перекрытии окружающих маркеров. Документация предупреждает о несовместимом изменении направления оси Z board после OpenCV 4.6.0.

`INFERENCE`: нужно хранить файл напечатанного эталона и его измеренные размеры, словарь, IDs, конвенцию осей и версию генератора. «Такая же шахматная доска» недостаточно. Не приравнивать документированную subpixel refinement к сантиметрам на заводе. Ошибка физического размера, неплоская печать и неверная принадлежность плоскости не исправляются детектором.

### A02-F03 — у OpenCV есть работающее по замыслу авторов sample-приложение, но это не наш onboarding

`DOCUMENTED` A02-S03. Образец читает камеру, видео или список изображений, получает точки patterns, рассчитывает reprojection error, сохраняет параметры XML/YAML. Это реальный reference workflow для intrinsics. Его UI и код здесь не запускались; перенос в веб-редактор зон требует отдельной реализации.

### A02-F04 — AprilTag pose уже предполагает метры и параметры камеры

`DOCUMENTED`, `CODE_INSPECTED` A02-S04/S05. В `apriltag_detection_info_t` размер тега передаётся в метрах, fx/fy/cx/cy — в пикселях. README определяет `tagsize` как длину между detection corners на границе белого/чёрного, а не внешнюю ширину листа. Заголовок API допускает одно или два решения pose; упрощённая функция возвращает object-space error. Библиотека — C с минимальными зависимостями; официальная поддержка заявлена для Linux. Лицензия BSD-2-Clause.

`INFERENCE`: один распознанный tag не является доказательством точной floor map на всей площадке. Если tag на стене, получается плоскость/pose стены; для пола нужны известное взаимное положение или floor correspondences. Несколько разнесённых floor fiducials лучше диагностируют область применения, чем один маленький tag в углу. Для чистой 2D floor homography можно использовать известные coplanar tag corners без запуска pose solver; геометрию H раскрывает агент 01.

### A02-F05 — fSpy явно отделяет перспективу от масштаба

`DOCUMENTED`, `CODE_INSPECTED` A02-S06. Пользователь задаёт линии к точкам схода; соответствующие мировые направления предполагаются перпендикулярными. Почти параллельные в изображении линии ухудшают локализацию точки схода. `computeTranslationVector` использует `DEFAULT_CAMERA_DISTANCE_SCALE=10`, затем при заданном `referenceDistanceAxis` умножает translation на отношение `referenceDistance/defaultHandleDistance`. Без эталонного расстояния размер сцены условный.

`INFERENCE`: этот код — прямой контрпример обещанию «точки схода автоматически дают метры». fSpy пригоден как отдельный ручной инструмент исследования перспективы; не найдено доказательства готового CCTV zone editor или industrial safety validation. Basics ограничивает применение перспективными изображениями с малой дисторсией; сильная fisheye distortion, панорамы и изменённая перспектива проблемны.

### A02-F06 — версия/лицензия fSpy меняют путь повторного использования

`LOCAL_OBSERVATION`, `DOCUMENTED` A02-S07. Через GitHub API получена дата stable v1.0.3; страница releases также содержит более новые по номеру prerelease, но они не использованы как стабильный baseline. `solver.ts` указывает GPL v3 или более позднюю. Для хакатона можно изучить внешний инструмент и алгоритм, но перенос исходника требует соблюдения его лицензии. Готовность бинарника на нашей ОС не проверена.

### A02-F07 — Calibmar даёт полезный образец GUI-приёмки intrinsics

`DOCUMENTED` A02-S08. Workflow: подготовить разнообразные изображения эталона при нужных zoom/focus/lens, выбрать файлы/модель/target, запустить, просмотреть per-view statistics, удалить проблемные кадры и повторить, сохранить calibration. Изменение зума, фокуса или объектива требует перекалибровки по документации. Отчёт включает `.txt` и `.yaml`; пример YAML содержит модель, параметры, ширину и высоту. Документация советует покрывать поле зрения и избегать blur/бликов; фиксированное число снимков не является доказательством качества.

### A02-F08 — Calibmar GUI подтверждён исходником, но его границы узкие

`CODE_INSPECTED` A02-S09. В конструкторе `FileCalibrationDialog` есть каталог изображений, Import и Run; `Validate` проверяет существование каталога и передаёт проверку параметров widget. `ImportParameters` читает YAML и заполняет target/camera options. Это подтверждает реализацию диалога, а не полевую точность. Тот же закреплённый CMake задаёт 1.1.0. Сам Calibmar — BSD-3-Clause, условия зависимостей отдельные. На GitHub releases отсутствуют потому, что README направляет к оригинальному GitLab; это не доказательство отсутствия бинарников. GitLab assets здесь не скачивались.

### A02-F09 — learned single-image calibration может предложить оптику и вертикаль

`DOCUMENTED` A02-S10. GeoCalib оценивает gravity, focal length и distortion из одной картинки; §3 предполагает square pixels/no skew, а principal point — в центре при отсутствии crop. Yaw без дополнительных ограничений обычно ненаблюдаем. §3.2 связывает parameter covariance с inverse Hessian в точке сходимости; Appendix C исследует uncertainty на OpenPano.

`INFERENCE`: uncertainty этих параметров полезна для отказа от предложения, но не измеряет полный метрический риск floor mapping, ошибку footpoint и изменение заводской сцены. Публикация не заменяет проверку наших контрольных расстояний. Её задача не включает восстановление высоты камеры и абсолютного масштаба пола из воздуха.

### A02-F10 — GeoCalib имеет настоящий GUI, но это нейросетевая зависимость

`CODE_INSPECTED` A02-S11. `extractor.py::calibrate` возвращает camera, gravity, covariance и поля confidence/uncertainty; `_post_process` отменяет scale/crop preprocessing. `__init__` загружает веса из release v1.0. `gradio_app.py` строит upload/model selector и визуализации, выводит roll/pitch/vFoV/focal uncertainty; это исходный demo UI. README фиксирует principal point в центре. Код Apache-2.0, веса CC-BY-4.0. Не запускалось; CPU latency и экспорт/инференс на LinQ неизвестны. Этот вариант разумен как future proposal module после согласования правила обязательного neural inference.

### A02-F11 — известная геометрия даёт измерения при явных условиях

`DOCUMENTED` A02-S12. Criminisi/Reid/Zisserman строят single-view metrology из vanishing line опорной плоскости и vanishing point направления вне неё. Статья различает отношения размеров и расстояния между параллельными плоскостями до общего масштаба; отдельно разбирает перенос ошибки image measurements. Это основание искать известные размеры и геометрические связи, а не обещать полную 3D из любой картинки.

### A02-F12 — image registration подходит для drift warning, а не автоматического признания валидности

`DOCUMENTED` A02-S13. `findTransformECC` оценивает warp по корреляционному критерию, допускает translation/euclidean/affine/homography; использует начальное приближение, для больших сдвигов требует близкой инициализации и может бросить исключение при несходимости. Есть input mask.

`INFERENCE`: мониторинг стабильного фона или fiducials может сигнализировать о сдвиге. Большая корреляция не гарантирует правильный масштаб; сцена с разными глубинами, движущимися объектами и освещением создаёт дополнительные отказы. Отсутствие совпадений означает «проверить», а не «камера точно неподвижна».

### A02-F13 — размер изображения входит в контракт калибровки

`DOCUMENTED` A02-S14. OpenCV связывает intrinsics в пикселях с размером изображения; при простом масштабировании пиксельные параметры масштабируются, переиспользование связано с неизменным focal length. В прочитанном tag OpenCV 4.12.0 лицензия Apache-2.0.

`INFERENCE`: filename камеры и RTSP URL недостаточны для выбора H. Нужен конкретный вариант изображения после всех геометрических преобразований. Математически известное чистое resize/crop допускает перенос параметров, но неизвестная смена video mode может означать другой sensor crop или ISP warp; её нельзя считать resize по совпадению aspect ratio.

## Что именно автоматизировать

Следующая таблица — инженерная классификация `INFERENCE` из A02-F01–F13; она не является заявлением о единой готовой реализации.

| Подзадача | Автоматическая часть | Что подтверждает человек | Что остаётся неизвестным без дополнительных входов |
|---|---|---|---|
| Intrinsics/distortion | Найти corners эталона, подобрать модель, показать reprojection residuals | Физические размеры, жёсткость/плоскостность target, настройки объектива, плохие кадры | Положение пола в world frame |
| Floor homography | Предложить corners/IDs, рассчитать H, показать сетку и residuals | Что точки на одном полу; реальные координаты, правильные соответствия, независимые controls | Геометрия выше пола и за областью проверок |
| Vanishing points | Найти кандидаты линий/сходов, показать альтернативы | Параллельность/перпендикулярность в мире, выбранная плоскость, единицы/размер | Метры без масштаба, неоднозначные линии |
| Learned calibration | Предложить focal/gravity/distortion с diagnostic uncertainty | Пригодность model/crop assumptions и физический scale reference | Ground plane origin/height/scale; промышленная переносимость |
| Zone editor | Привязать polygon к координатной системе, проверить самопересечение, визуализировать | Где опасная граница, режим станка, допустимые операции, время/допуски | Само правило производственной безопасности |
| Drift | Сравнить stable anchors и metadata, выдать warning | Причину изменения; повторную приёмку геометрии и зон | Безошибочная автокомпенсация движения/зума |

Относительная depth map — отдельный тип выхода: порядок/форма глубины не равны физическим метрам, и она не подменяет floor calibration. Даже predicted metric depth требует domain validation; конкретные модели и ограничение 3D передаются агенту 05.

## Три реалистичных workflow

Все этапы ниже — `INFERENCE` / проектное предложение. Это не реализованное приложение. Любое автоматическое предложение хранится как candidate и требует явного подтверждения интегратором; измерительные controls должны быть независимы от подгонки.

### W02-1: MVP — область в изображении, без масштаба

**Когда выбирать:** есть только видео фиксированной камеры, нет доступа на площадку, размеров или надёжного scene plan. Входы: неизменённый кадр, исходная геометрия потока, человек, знающий участок и режим опасности.

1. Выбрать camera profile и репрезентативный резкий кадр, сохранить source frame/timestamp и размеры. На экране должно быть видно, относится ли polygon к raw или undistorted image.
2. Обвести запрещённый участок; явно выбрать правило наблюдаемой точки: например projected ground-contact estimate, а не неявное «любое пересечение bbox».
3. Отметить неразличимые/закрытые участки и границу применимости. Отдельно задать режим оборудования, расписание и допустимые исключения, если они известны.
4. Просмотреть replay с проходами внутри/снаружи/вдоль границы, с рабочими у оборудования и с перекрытиями. Исправить конфигурацию по семантическим ошибкам; сохранить новые тестовые эпизоды для последующей независимой проверки.
5. Сохранить версию image polygon и активировать только для данного camera profile.

**Приёмка:** зона соответствует видимой сцене и согласованному смыслу события; на независимых эпизодах проверены ошибки границы и выбранной точки объекта. **Отказ:** camera moved, polygon скрыт, участок нельзя отличить по изображению, видимые точки выше пола делают интерпретацию неоднозначной. **Что не получаем:** скорость м/с, метрическое удаление, универсальный буфер «2 м» или 3D расстояние. Отсутствие scale не блокирует MVP intrusion, но имя правила должно отражать его наблюдаемый смысл.

### W02-2: practical/enhanced — измеренная плоскость пола

**Когда выбирать:** можно получить достоверные координаты ориентиров на общей плоскости. Входы: камера/профиль, raw-to-analysis chain, размеры/координаты пола, calibration fit points и отдельно control points/segments. Практический минимум H — четыре пригодных соответствия; фактическую устойчивость определяет их конфигурация, а не число кликов (подробности у агента 01).

1. Зафиксировать camera profile, фокус/зум, разрешение, ROI, rotation, crop/resize/letterbox и факт undistortion. При заметной дисторсии сначала получить/проверить camera model, затем размечать в выбранном representation.
2. Выбрать локальную систему пола: origin, направления X/Y, единицы `m`, `plane_id`. Ввести измеренные координаты опорных точек. Для настоящего прямоугольника известные L/W дают corners `(0,0),(L,0),(L,W),(0,W)`; не превращать визуальный quadrilateral в прямоугольник без знания сцены.
3. Сопоставить пиксельные точки; автоматические corners/lines — редактируемые кандидаты. Отобразить порядковые номера и плоскость. Программа проверяет дубли, геометрическое вырождение, конечность результата; numeric fit не подтверждает правильность координат.
4. Рассчитать H; показать overlay метрической сетки на кадре и вид сверху, подписать единицы. Показать fit residuals, места опор и маску проверяемой области. Сетка — diagnostic, а не доказательство точности.
5. На плане пола задать metric polygons, буферы и статическое footprint оборудования. Сохранить world geometry как источник истины; image overlay получать преобразованием для выбранного профиля. Указать отдельно image-only annotations.
6. Разметить **не использованные в fit** контрольные точки/отрезки ближнего, дальнего и боковых участков. Внести наземные измерения с происхождением и точностью инструмента; показать сравнение предсказания с ними. Не проверять только длину того же прямоугольника, которым задан масштаб.
7. Принять либо ограничить validity mask/правила, либо запросить повторные измерения. Сохранить immutable calibration version, источник размеров, результаты controls и подтверждение интегратора.

**Приёмка:** известна и корректна физическая система координат; в каждой активируемой зоне независимые position/distance controls укладываются в заранее согласованные бюджеты ошибки; ошибка сопоставима с требуемым различением события. **Отказ:** перепутанные corners, весь fit в маленьком углу, уклон/ступень/платформа, большой residual на дальнем плане, недостаточно независимых controls или контрольный размер ненадёжен. Можно принять подмножество площади с узкой mask; это не делает всю камеру метрически валидной.

### W02-3: assisted/future — эталоны и автоматические предложения

**Ветка A, надёжнее в контролируемом onboarding:** измеренный жёсткий checkerboard/ChArUco для intrinsics; floor markers/план для scene mapping. Сначала собрать достаточно разнообразные качественные виды эталона по полю зрения, затем отдельно зарегистрировать плоскость пола. Подтверждать physical target specification, settings камеры и независимые controls. Calibmar/OpenCV дают основу первого этапа; AprilTag может дать устойчивые IDs и контроль неподвижных anchors.

**Ветка B, когда эталон в кадр не поставить:** линии/плитка/габариты из обследования или GeoCalib предлагают initial perspective/camera model. Интегратор подтверждает параллельность и ортогональность линий, принадлежность полу, известную длину и crop assumptions. Затем те же controls и versioned activation, что W02-2. Не пытаться спрятать недостающий масштаб под «AI confidence».

**Приёмка:** предложение сокращает ручную работу и не ухудшает контролируемую ошибку; полностью воспроизводится из сохранённых inputs/config. **Отказ/возврат к W02-2:** недостаточно markers, target слишком мал/размыт, lines соответствуют другой плоскости, неортогональная сцена, неоднозначная pose, неизвестный scale, contradictory controls. **Future, а не MVP promise:** автоматическая компенсация PTZ/вибрации, обучаемая оценка оптики на LinQ и multi-plane scene reconstruction.

## Приёмка и неопределённость: измеряемое условие вместо красивой картинки

Это предлагаемый протокол `HYPOTHESIS`, не проведённый тест. Детальные event metrics принадлежат агенту 06.

Для независимых точек пола считать `e_i = ||H(p_i) - X_i||` после homogeneous normalization, отдельно по участкам near/far/left/right. Для контрольных отрезков `e_d = | ||H(p_a)-H(p_b)|| - d_measured |`. Бюджеты `B_position(zone)`, `B_distance(zone)` назначить из требуемого различения события и качества наземного эталона **до** просмотра результата. Не существует найденного универсального порога в сантиметрах. Если controls не покрывают интересующий участок, статус его точности — `UNKNOWN`.

Повторные клики разных разметчиков и повторные кадры показывают sensitivity, но не независимую абсолютную accuracy. Предлагается возмущать fit points в пределах реально наблюдаемой repeatability и смотреть перемещение сетки/границы; это diagnostic устойчивости. Ошибка физических размеров и общий неверный scale могут одновременно сдвинуть все результаты, оставаясь незаметными на fit residuals. Стандартная ошибка reprojection — ещё не world-position error.

Следует различать: intrinsic parameter uncertainty; H sensitivity; ошибку измерений scene reference; невидимую ground-contact точку; drift; ambiguity плоскости. Их нельзя свести к одному проценту confidence. Около границы зона неопределённости должна выражать измеренную геометрическую неоднозначность и uncertainty локализации объекта; её величина не получена настоящим исследованием. Калибровка может пройти, а rule оказаться ненаблюдаемым из-за закрытых ног.

## Жизненный цикл: когда сохранённая калибровка перестаёт подходить

Следующая state machine — `INFERENCE` для продукта, не найденная industrial implementation: `draft → proposed → controls_pending → validated → active`; из active при изменении профиля/дрейфе — `suspect/invalid`, после новых controls — новая validated version. Старые версии не перезаписывать, события сохранять с применённым calibration ID.

| Изменение | Что сделать | Почему |
|---|---|---|
| Известное чистое resize изображения | Пересчитать pixel-coordinate transforms в новой версии; повторить controls | Математически компенсируемо, но легко перепутать source/analysis coordinates |
| Известный crop/ROI/letterbox/rotation | Хранить явный mapping и порядок операций; обновить image geometry/mask, перепроверить | Нормированные x/W,y/H не учитывают crop/letterbox semantics |
| Неизвестная смена stream profile/sensor mode | Suspend metric rules; получить сведения и controls | Новый режим может менять effective field of view/ISP warp |
| Lens/optical zoom/focus | Переоценить intrinsics/distortion и scene mapping | Параметры объектива больше не обязаны соответствовать калибровке |
| PTZ, перестановка/поворот камеры, электронная стабилизация с меняющимся crop | Invalidate или отдельный валидированный preset/profile; не сохранять одну H на все виды | Scene-to-image mapping меняется |
| Вибрация | Drift warning по stable anchors; при нестабильности abstain/suspend; проверить blur | Постоянная H не описывает все кадры, резкость тоже меняется |
| Перестройка участка/перенос станка/платформа | Отдельно пересмотреть plane и смысл zones | Камера может быть неподвижной, а опасная область уже другой |
| Тени/свет/окклюзия/background texture loss | Статус drift check «недостаточно данных», запрос проверочного кадра | Failure регистрации не равен доказательству движения или его отсутствия |

Предлагаемый drift diagnostic: сохранять reference frame и несколько явно неподвижных anchors по полю зрения; маскировать людей/машины; измерять residual displacement в пикселях и его метрическое следствие в активных зонах; реагировать на устойчивую динамику и изменение metadata. Можно использовать fiducials, feature matching или ECC. Пороги и длительность должны быть измерены на спокойном видео с нормальной вибрацией и проверены на искусственном/реальном сдвиге. **Нельзя** после регистрации нового кадра автоматически объявлять H безопасной: чистый поворот, перенос камеры при разной глубине, изменение focal length и неплоская сцена не тождественны одной надёжной floor correction.

Validity mask — отдельная область, где приняты plane assumptions, видны необходимые признаки и есть контроль качества. Она не обязана равняться всему изображению или convex hull опор. Hull можно показать как diagnostic extrapolation, но его внутренняя область сама по себе ещё не прошла проверку. Metric polygon в world coordinates сохраняет геометрический смысл при смене вида, однако вновь проецировать его можно только через подходящую валидированную mapping. Image polygon привязан к camera profile, а не к площадке в метрах.

## Предлагаемый контракт versioned config

Это список полей для последующей реализации, **не существующий формат OpenCV/Calibmar**. Числовые matrices и budgets должны заполняться измерениями, поэтому фиктивный готовый JSON не создаётся.

- `schema_version`, `calibration_id`, `parent_calibration_id`, `status`, `created_at`, `approved_at`, `approved_by`.
- `camera_id`, physical installation/preset, source profile; raw width/height; orientation; optical/digital zoom, focus/lens identifiers при наличии.
- `coordinate_chain`: raw → crop → resize/letterbox → undistort/analysis, с размерами и матрицами там, где они корректны; `pixel_coordinate_convention` и правило inverse mapping outputs модели.
- `reference_frame`: path/hash/source timestamp, формат; `reference_anchors` и mask неподвижных частей.
- `camera_model`, K, distortion model/coefficients, calibration resolution, версия библиотеки, target description и measured dimensions; возможность «intrinsics unknown» должна быть явной.
- `plane_id`, origin/axis convention/units, floor assumptions; H direction `image_to_floor`, representation входных пикселей; fit correspondences, метод/параметры, source measurements.
- `independent_controls`: отдельные IDs, measured values, units, происхождение и uncertainty эталона, residuals по участкам, принятые budgets и actual results.
- `validity_mask`, unsupported/occluded regions, `metric_zones` и `image_zones` с различными coordinate-system fields; rule exceptions отдельно от geometry.
- `drift_checks`: метод, reference, последние outcomes/метрики, threshold provenance; причина invalidation.
- На каждом событии: `camera_profile_id`, `calibration_id`, `zone_version`, координаты и observability flags; иначе объяснение старой тревоги изменится после редактирования зоны.

## UX-антипаттерны и последствия

1. Кнопка «Автокалибровать» молча включает правила в метрах: пользователь не знает, что scale придуман. Требуется separate review/controls activation.
2. Ввести одну длину и применять один m/px по всему наклонному кадру: результат меняется с глубиной. Одна длина пригодна после достаточно определённого metric rectification, а не вместо определения перспективы.
3. Принимать четыре случайных клика как четыре метрических соответствия: пиксели сами не задают мировые координаты.
4. Проверять тот же калибровочный прямоугольник: fit может быть точным при ошибочном масштабе; независимого подтверждения нет.
5. Рисовать сетку поверх сцены без маркировки единиц, support и unknown regions: визуальная правдоподобность превращается в ложное ощущение accuracy.
6. Смешивать raw coordinates разметки и resized/letterboxed outputs модели: даже хорошая H применяется к другим пикселям.
7. Делать print-to-fit, измерять внешний лист AprilTag или использовать nominal tile size без измерения: систематическая ошибка масштаба.
8. Считать board pose на стене калибровкой пола или применять H пола к ногам на платформе: неверная плоскость.
9. Копировать H после смены потока/зума или одного PTZ preset на другой: конфигурация формально существует, физически устарела.
10. Пытаться исправить drift по людям/движущемуся станку: алгоритм отслеживает сцену, а не неподвижную камеру.
11. Прятать сложность в одном AI confidence: confidence intrinsics не подтверждает scale, foot contact и правило опасности.
12. Считать временной/персональный допуск изменением polygon: теряется геометрический аудит. Разрешение работы — отдельная логика, в неизвестном состоянии не следует из положения человека.

## Что действительно выполнено и что ещё проверить

`LOCAL_OBSERVATION`: выполнен английский и русский интернет-поиск; открыты перечисленные первичные страницы и raw source files; GitHub REST API использован для release timestamps и commit metadata fSpy, AprilTag, Calibmar, GeoCalib и OpenCV. Просмотрены код fSpy `computeTranslationVector`, AprilTag pose header, Calibmar file dialog/CMake, GeoCalib extractor и Gradio UI. Источники читались через web и HTTP API, локальные copies чужих репозиториев не создавались. PowerShell использован только для чтения входных Markdown и метаданных; этот файл создан как исследовательский результат.

Не запускались detection/calibration/GUI, не скачивались модели, не обучались сети, не оценивалась accuracy/скорость, не проверялись binaries/CPU dependencies/LinQ SDK. PDF GeoCalib прямым web fetch оказался слишком большим для инструмента; прочитана полная HTML-версия той же v2. Попытка `calibmar_documentation/usage.html` не дала страницы; вместо неё прочитан актуальный `camera_calibration.html`. Это ограничения доступа к отдельным адресам, не отрицательный результат алгоритмов.

## Открытые вопросы и адресная передача

| ID | Вопрос / меняемое решение | Что нужно и способ закрытия | Приоритет / адресат |
|---|---|---|---|
| A02-Q01 | Есть ли физически измеренные floor correspondences и независимые controls для каждого видео? | План с координатами/обследование, source кадр; проверить plane membership и reference measurements. Без них W02-1, не обещать метры | P0; интегратор, агент 01 |
| A02-Q02 | Откуда берутся кадры и детекции: raw resolution, ROI, resize, letterbox, undistort, optical/digital zoom, PTZ? | Pipeline metadata и один проверяемый overlay с inverse transform; сопоставить клики/выходы модели в одной системе | P0; video_architecture/model_stack |
| A02-Q03 | Какая метрическая ошибка допустима у границы конкретной опасной зоны? | Эксперт задаёт physical decision margin; evaluation утверждает независимый control protocol. Не искать универсальное число в чужой статье | P0; evaluation, агенты 04/06 |
| A02-Q04 | Можно ли выполнять нейросетевую proposal calibration вне LinQ, либо GeoCalib тоже должен исполняться на нём? | Официальная формулировка кейса и фактический SDK; если запрещено/нет export path, удалить learned proposal из MVP | P1; linq_platform |
| A02-Q05 | Можно ли временно разместить измеренные markers/board и снять разные target poses? | Ответ площадки, размеры/печать/фото/target files; при положительном ответе выбрать W02-3A для intrinsics и W02-2 для пола | P1; интегратор |
| A02-Q06 | Есть ли drift/вибрация/PTZ и достаточные постоянные anchors? | Видео спокойного фона и контролируемых сдвигов, exposure/zoom metadata; измерить warning failures и latency | P1; video_architecture, агент 06 |
| A02-Q07 | Какая сборка/лицензии dependencies допустимы и доступны на LinQ+CPU сервере? | Lockfile, OS/toolchain, review package notices, smoke tests на фактическом сервере. GUI не обязан работать на inference server, но это архитектурное решение | P1; агент 06 |
| A02-Q08 | Какие плоскости и исключения реально нужны: ступени, platforms, поднятый груз, legitimate work? | Scene survey и правила допуска; отдельные plane IDs или abstention. Floor H не выдавать за 3D scene model | P0/P1; агенты 04/05 |

Передача агенту 01: держать separate intrinsics/floor mapping; scale reference и independent control sets обязательны в wizard. Агенту 03: каждый track point должен ссылаться на calibration/profile version; при invalid/suspect metric speed не продолжать молча. Агенту 04: зоны в метрах и image polygons имеют разную семантику; пользователь подтверждает machine footprint и легитимные рабочие операции. Агенту 05: learned camera calibration не устраняет scale/plane/height ambiguity. Агенту 06: reproducible baselines и точные URLs выше; GUI/source inspection не равняется запуску, calibration residual не равняется event quality.

## Итог выбора для хакатона

**Сначала W02-1 и W02-2, при доступных размерах; W02-3 — необязательное ускорение настройки.** При отсутствии наземных данных MVP остаётся честным image-zone intrusion. При наличии контролей имеет смысл включить локальную метрическую floor map и поверх неё ограниченные правила расстояния/скорости. Публичные sources подтверждают отдельные строительные блоки полуавтоматизации; готовность end-to-end, промышленная accuracy и LinQ path остаются вопросами для фактических испытаний.
