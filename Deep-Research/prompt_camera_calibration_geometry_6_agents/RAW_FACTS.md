# Фактическая база camera_calibration_geometry

База включает извлечённые наблюдения, математические следствия и проектные процедуры с разными статусами. `DOCUMENTED` — первичная документация/публикация; `CODE_INSPECTED` — прочитанный код указанной версии; `REPORTED_EXPERIMENT` — чужое измерение с условиями; `LOCAL_OBSERVATION` — фактически выполненное действие в этом запуске; `INFERENCE` — наш вывод; `HYPOTHESIS` — проверяемое предложение; `UNKNOWN` — не установлено. Прочитанный код не означает запущенный; confidence нейросети не означает метрическую погрешность.

## Контекст и реально выполненное

<a id="f001"></a>
### F001 — Ресурсы и роль исследования

Основание: `DOCUMENTED` как сведения пользовательского задания, [S001](SOURCES.md#s001), §§2–4. Команда из пяти участников готовит сервис промышленной безопасности; обязательный inference нейросетевой модели заявлен на LinQ. Общий контекст упоминает RTX 4070 и возможность облачных GPU, но не устанавливает точную ОС, память, SDK, конфигурацию удалённого ускорителя. Исследование готовит решения и проверки, не является разработкой сдаваемого приложения. Истинность ресурсов независимо не проверялась.

<a id="f002"></a>
### F002 — Более свежие сведения имеют статус пересказа

Основание: пользовательский пересказ в [S002](SOURCES.md#s002), §0. Полный кейс, по входу, опубликован 23 октября; первый checkpoint уже состоялся. Эксперты акцентировали точность, по смыслу «пусть хоть 1 FPS». Сервер описан как LinQ+CPU без NVIDIA, видео советовали размещать на выделенной машине. Это не прочитанная официальная спецификация, не разрешение любого CPU-инференса и не гарантия доступных ресурсов/API. Фактические порты, пути, SDK и режим исполнения неизвестны.

<a id="f003"></a>
### F003 — Отсутствующие входы и фактический процесс

Основание: `LOCAL_OBSERVATION`; осмотр текущей папки и [состояние](_WORK/RUN_STATE.md). До начала работы в каталоге были ровно два входных Markdown-файла; PDF кейса, INDEX/SUMMARY, соседних отчётов, видео, калибровочных эталонов и данных устройства нет. Специальный конвейер [S002](SOURCES.md#s002), §3, заменяет общий: шесть исследователей одной волны, затем оркестратор. Отсутствие файла здесь не означает его отсутствия у команды или в интернете.

<a id="f004"></a>
### F004 — Локальная иллюстрация ошибки масштаба вдали

Основание: `LOCAL_OBSERVATION` вычисления, [S003](SOURCES.md#s003); интерпретация `INFERENCE`. Идеальная pinhole-камера: горизонтальная оптическая ось, высота `h=4 m`, фокус `f=1000 px`, нет дисторсии; координата от горизонта `v=fh/Z`. Добавление `+1 px` к v даёт ошибки глубины `0.015968 m` при `Z=8 m`, `0.099502 m` при `20 m`, `0.396040 m` при `40 m`. Это иллюстрирует неодинаковую чувствительность изображения; не является оценкой точности реальной камеры, bbox или калибровки.

<a id="f005"></a>
### F005 — Локальная иллюстрация точки над полом

Основание: `LOCAL_OBSERVATION` вычисления, [S003](SOURCES.md#s003); интерпретация `INFERENCE`. В той же модели точка на высоте `z=1 m` при истинной глубине `Z=8 m` имеет `v=375 px`. Ошибочное применение inverse floor mapping даёт `Z_hat=10.666667 m`, поскольку `Z_hat=hZ/(h-z)`. Даже идеальная H пола не исправляет неверную принадлежность точки плоскости. Здесь не утверждается, что любая реальная ошибка имеет именно это направление или величину.

<a id="f006"></a>
### F006 — Локальная иллюстрация краткого пересечения при 1 Hz

Основание: `LOCAL_OBSERVATION` аналитического примера, [S003](SOURCES.md#s003). При `x(t)=2t m`, `t∈[0,1] s`, зона `x∈(0.8,1.2) m` занята с `0.4` до `0.6 s`, то есть `0.2 s`. Кадры в `0` и `1 s` оба вне зоны. Наблюдаемого кадра внутри нет. Пересечение отрезка между точками можно вывести только с добавленной гипотезой о траектории; такой вывод не доказывает реальное время/маршрут между наблюдениями. Это не тест видеосервиса и не универсальная минимальная частота.

## Время, скорость и различие между перемещением и бегом

<a id="f007"></a>
### F007 — Источник времени для скорости

`DOCUMENTED`, [S004–S006](SOURCES.md#s004), A03-F01. В PyAV `t=pts*time_base`; `Frame.time` выражено в секундах. PTS описывает предъявление, DTS — декодирование. FFmpeg `best_effort_timestamp` является эвристической оценкой, не независимым датчиком времени экспозиции. `INFERENCE`: скорость считают по времени исходных наблюдений, а не завершению inference/декодирования. PTS файла без сведений о записи не равен проверенному capture UTC. Для live нужны происхождение capture time, модель синхронизации и epoch после reconnect. Проверено чтением документации; камера/видео не проверялись.

<a id="f008"></a>
### F008 — Преобразование FPS может менять доказательства

`DOCUMENTED`, [S008](SOURCES.md#s008), A03-F02: входной `-r` задаёт CFR timestamps, выходной при кодировании может дублировать/удалять кадры; `fps_mode` имеет разные режимы. `copyts` не исключает всех последующих преобразований muxer. `INFERENCE`: неизменный исходник и отображение производных frame IDs/PTS сохраняются отдельно. Повторённые кадры не дают новых наблюдений; `avg_frame_rate` не доказывает постоянный интервал. Точное поведение проверяют по целевой сборке FFmpeg, не по общему имени CLI.

<a id="f009"></a>
### F009 — SlowFast: проверенная конфигурация, не универсальный FPS

`DOCUMENTED/CODE_INSPECTED`, [S009](SOURCES.md#s009), [S010](SOURCES.md#s010), A03-F03. В примере статьи Slow выбирает 4 из 64 кадров с шагом 16, Fast — 32 с шагом 2, отношение частот 8. В отдельно прочитанном `SLOWFAST_8x8_R50.yaml` по SHA значения другие: `NUM_FRAMES: 32`, `SAMPLING_RATE: 2`, `ALPHA: 4`, 400 классов Kinetics. Их нельзя смешивать. При равномерном исходнике f span 32 позиций с шагом 2 равен `62/f` секунд; переход на 1 FPS меняет физический смысл окна. Конфиг обучения с 8 GPU не устанавливает inference requirement. Никаких запусков, весов, экспорта или LinQ-подтверждения нет.

<a id="f010"></a>
### F010 — PoseC3D: число временных позиций не задаёт секунды

`DOCUMENTED/CODE_INSPECTED`, [S011](SOURCES.md#s011), [S012](SOURCES.md#s012), A03-F04. PoseC3D строит temporal volume из heatmaps поз. Прочитанный NTU60-конфиг задаёт `clip_len=48`, validation 1 clip, test 10 clips. Статья рассматривает влияние sampling на наборах разной длительности. Это не готовое доказательство распознавания промышленного бега; weights/domain transfer/export неизвестны. Code licenses SlowFast/pyskl — Apache-2.0 в прочитанных LICENSE, условия весов/данных проверяются отдельно.

<a id="f011"></a>
### F011 — Sampler способен заполнить вход повторениями

`CODE_INSPECTED`, [S013](SOURCES.md#s013), A03-F05: `UniformSampleFrames` при коротком видео строит индексы с последующим modulo по числу исходных кадров, `frame_interval=None`. Поэтому 48 входных позиций могут не содержать 48 уникальных измерений. `INFERENCE`: сохранять число уникальных source frames, timestamps и span; нужная форма тензора не доказывает наличие фаз походки. Код прочитан и сохранён в `_WORK/A03_SOURCES/`, не запускался.

<a id="f012"></a>
### F012 — Скорость не определяет тип походки

`REPORTED_EXPERIMENT` с ограничением доступа, [S014](SOURCES.md#s014), A03-F06: доступный abstract исследования переходов walk-to-run включает бег медленнее предпочтительной ходьбы. Полный метод не прочитан; численные выводы оттуда не извлекаем. `INFERENCE`: единый порог m/s не является определением бега. Медленный бег, быстрый шаг и бег на месте должны иметь отдельные gait-метки; геометрический MVP честно называть «быстрое перемещение по полу».

<a id="f013"></a>
### F013 — Контракт наблюдения и разрыв истории

`INFERENCE`, A03-F07 из F007–F011 и требований F002. Запись: camera ID, calibration/zone version, source frame ID, PTS/time_base и stream epoch, track ID+generation, bbox/keypoints, coordinate space, floor point и observed/estimated/predicted flag, visibility/validity reason. Arrival/decode/inference/event-output времена — отдельная processing timeline. Смена камеры/калибровки, time reset, сомнительный ID, выход на другую плоскость или чрезмерный gap разрывают историю. Пропуск не равен нулевой скорости; tracker prediction не является новым измерением. Численные допустимые gaps не установлены.

<a id="f014"></a>
### F014 — Скорость хорды и скорость по пути

`INFERENCE`, A03-F08: для валидных координат пола `q_i` в метрах и `dt=t_j-t_i>0`, `v=(q_j-q_i)/dt`, `s=||v||` m/s; перевод в km/h — `3.6*s`. Это модуль средней векторной скорости, а не peak speed и не средняя скорость вдоль извилистой траектории. Возврат к исходной точке скрывает движение. Сумма длин плотных сегментов приближает путь, но jitter завышает его. Центр bbox торса не лежит на полу; его H-проекция физически неверна. Невидимые стопы требуют estimated/unknown статуса.

<a id="f015"></a>
### F015 — Причинное окно по секундам

`HYPOTHESIS/INFERENCE`, A03-F09. Baseline: валидные точки одного ID в `[t_now-W,t_now]`, робастная линейная регрессия `q_i≈a+b(t_i-t0)`; `||b||` — оценка скорости. Для weighted least squares `b=Σw_i(t_i-t_bar)(q_i-q_bar)/Σw_i(t_i-t_bar)^2`. Вес detector score нельзя автоматически считать inverse metric variance. Нужны минимальные unique samples/span, max gap, residual и причинность фильтра. Числа подбирают на tuning split; длительное окно снижает jitter, размывает рывки и добавляет задержку. Offline-фильтр с будущими точками не является online результатом. Kalman-transition учитывает фактический dt.

<a id="f016"></a>
### F016 — Ошибка скорости и компромисс интервала

`INFERENCE`, A03-F10. Если radial position errors действительно ограничены `e_i,e_j`, ошибка velocity vector не больше `(e_i+e_j)/dt` при точном времени; первый порядок добавляет `||dq||*|δdt|/dt²`. Это условная аналитическая граница, не измеренная точность. При общем H ошибки коррелированы: общий сдвиг может сократиться, масштабная ошибка сохраняется. Малый dt усиливает jitter; большой dt теряет краткие изменения. Ускорение ещё чувствительнее и не рекомендовано главным MVP-критерием без отдельного теста.

<a id="f017"></a>
### F017 — Редкий inference и редкое наблюдение различаются

`INFERENCE`, A03-F11–F12 из F006–F011. Медленная последовательная обработка всех кадров сохранённого плотного видео сохраняет temporal evidence, увеличивая time-to-result. Выбор только последнего кадра раз в секунду удаляет наблюдения. При событии короче sample interval возможен полный пропуск; для продолжающегося события ожидание следующего кадра — от 0 до почти одного интервала плюс окно/очередь/inference. Если события нет на выбранных кадрах, конечная detection latency не существует. Нужны source FPS, selected timestamps, inference throughput, phase offsets и задержка отдельно. Adaptive sampling после триггера не помогает, если триггер пропущен; pre-trigger buffer помогает расследованию, но сам не гарантирует online alert.

<a id="f018"></a>
### F018 — Метрики события и observability

`INFERENCE`, A03-F13. Speed MAE сравнивает одну величину и одинаковый временной интервал: segment average с segment average. Event precision/recall считаются на эпизодах с заранее фиксированным one-to-one matching и onset/overlap tolerance; дубли учитываются отдельно. False alerts/camera-hour сопровождаются обработанной длительностью, недоступным временем и coverage. Нужны timing/onset errors, реальная latency, ID errors, страты depth/direction/occlusion/camera. Нельзя улучшать итог, незаметно исключая abstentions: отдельно end-to-end recall по всем целевым GT и conditional quality по наблюдаемой части, доля indeterminate и её причины. Ни одной численной метрики на видео кейса в этом запуске нет.

<a id="f019"></a>
### F019 — Скоростное правило как эпизод

`HYPOTHESIS`, A03-F14. Формулировка: скорость по полу выше локального `T` в зоне в течение `D` source-seconds при достаточной наблюдаемости. Hysteresis входа/выхода, max gap и aggregation объединяют эпизод; необозреваемую паузу нельзя считать наблюдавшимся превышением. Пороги зависят от участка и смысла кейса, не исправляют неверный масштаб. Если валидированный интервал скорости пересекает T, результат неопределён; построение интервала требует независимых данных. Это проектная логика, не проверенная реализация.

<a id="f020"></a>
### F020 — Документированный способ выгрузки времени

`DOCUMENTED` CLI [S007](SOURCES.md#s007), `HYPOTHESIS` для будущего использования, A03-E01. Команды ниже **не запускались**; наличие полей сверяется с фактической сборкой:

```powershell
ffprobe -version
ffprobe -v error -select_streams v:0 -show_streams -show_frames -show_entries stream=index,time_base,avg_frame_rate,r_frame_rate:frame=pts,pts_time,best_effort_timestamp,best_effort_timestamp_time,pkt_dts_time,duration_time -of json input.mp4
```

Сохраняют hash исходника, версию бинарника, codec/container, raw metadata, таблицу PTS/dt и frame mapping. Repeated/missing/non-monotonic PTS, resets и inferred timestamps записывают явно. Эти проверки ещё не доказывают точность bbox, exposure time камеры или скорость объекта.

## Плоскость, метрический масштаб и измерительная ошибка

<a id="f021"></a>
### F021 — Камерная модель и направление H

`DOCUMENTED` [S015](SOURCES.md#s015), [S018](SOURCES.md#s018), `INFERENCE` специализации A01-F01. Для исправленных от дисторсии пикселей `λ p~=K[R|t](X,Y,Z,1)^T`. На плоскости `Z=0`: `λ p~=G q~`, `G=K[r1 r2 t]`, `H=G^-1` переводит image→floor. При `W=h31*u+h32*v+h33`, `X=(h11*u+h12*v+h13)/W`, `Y=(h21*u+h22*v+h23)/W`. Метрические единицы происходят из известных XY, не из самого H. При достаточных correspondences можно оценить G без отдельного восстановления K/R/t; одна известная K не задаёт масштаб сцены. H определена до множителя; homogeneous normalization точки обязательна. Это floor intersection луча, не восстановление произвольного 3D.

<a id="f022"></a>
### F022 — Что достаточно для H и чего недостаточно

`DOCUMENTED/CODE_INSPECTED` [S018–S019](SOURCES.md#s018), `INFERENCE` A01-F02. Общая H имеет 8 DoF: минимум четыре разные пары image↔known metric XY, в минимальном наборе никакие три точки не коллинеарны в обеих плоскостях. Практически нужны избыточные опоры с двумерным покрытием near/far и независимые controls. Ранг системы должен быть 8; почти коллинеарная конфигурация неустойчива даже при формально правильном ранге. Один известный отрезок без дополнительных ограничений не определяет general 2D metric mapping. Измеренный прямоугольник даёт `(0,0),(L,0),(L,W),(0,W)` только если прямоугольность установлена. В прочитанном традиционном пути 4.13.0 `method==0 || npoints==4` ведёт к kernel без robust выбора альтернатив: четыре согласованных клика не позволяют выявить одну неверную пару. Маска inliers не равна независимой приёмке.

<a id="f023"></a>
### F023 — Intrinsics, дисторсия и единая система пикселей

`DOCUMENTED/CODE_INSPECTED` [S015](SOURCES.md#s015), [S021](SOURCES.md#s021), A01-F03. `calibrateCamera` оценивает K/D и poses эталона по видам; poses движимой доски не являются автоматически extrinsics пола. `undistort` меняет растр, `undistortPoints` — точки: без P возвращаются normalized camera coordinates, с `P=Knew` — исправленные пиксели. В H нужно передавать именно то представление, на котором она fitted. Варианты: исправить кадр до детектора либо исправлять отдельные raw points; inverse resize/letterbox/ROI выполняется согласованно. Дисторсия нелинейна, одной H обычно не устраняется. Для fisheye нужна подходящая модель. Локальная H на raw pixels без K/D — допустимая проверяемая аппроксимация, но только с явным статусом и independent controls по рабочей области.

<a id="f024"></a>
### F024 — Контракты OpenCV 4.13.0

`DOCUMENTED/CODE_INSPECTED`, [S015–S021](SOURCES.md#s015), A01-F04. Прочитано, не запускалось:

| API | Назначение / данные | Ограничение |
|---|---|---|
| `calibrateCamera(objectPoints,imagePoints,imageSize,cameraMatrix,distCoeffs,...)` | K/D, rvecs/tvecs, reprojection RMS | Не создаёт само по себе floor mapping |
| `undistort(src,K,D,...,newCameraMatrix)` | Исправленный растр | Зафиксировать Knew/ROI |
| `undistortPoints(src,K,D,...,R,P)` | Исправленные points | Без P normalized, `P=Knew` pixel coordinates |
| `findHomography(srcPoints,dstPoints,method,...)` | Матрица и mask из 4+ correspondences | Пустой результат возможен; threshold units=dst |
| `getPerspectiveTransform(src,dst,solveMethod)` | Матрица из ровно 4 пар | В прочитанном InputArray wrapper 4 двумерные `CV_32F` точки; robust rejection отсутствует |
| `perspectiveTransform(src,m)` | Sparse points и homogeneous normalization | Float points, для 2D H 3×3; finite result не гарантирует низкую ошибку |
| `warpPerspective` | Создание bird’s-eye raster | Для расстояний достаточно sparse points, BEV растр необязателен |

Удобное представление point arrays — `N×1×2`; dtype согласовывают с API. Рисунок BEV диагностирует, но не доказывает физические метры.

<a id="f025"></a>
### F025 — RANSAC threshold зависит от направления преобразования

`DOCUMENTED` [S015](SOURCES.md#s015), `INFERENCE` A01-F05. Default `ransacReprojThreshold=3`, `maxIters=2000`, `confidence=0.995`. Residual выражен в координатах dst: image→floor с XY в m означает threshold 3 m, а не 3 px. Практическое предложение — fit `G:floor_m→undistorted_pixels` с явным pixel budget, затем invert H и independently проверить в m. Это не универсально оптимальный estimator: при существенной ошибке наземного survey нужны учёт errors-in-variables или perturbation study. `confidence` RANSAC не является confidence события. RANSAC не исправляет неверный масштаб, кривой пол, дисторсию и неверный contact point; расширять threshold ради прохождения приёмки нельзя.

<a id="f026"></a>
### F026 — Точка контакта — отдельная измерительная модель

`INFERENCE`, A01-F06, и ограниченное `REPORTED_EXPERIMENT` [S023](SOURCES.md#s023), [S024](SOURCES.md#s024). Bbox bottom-center `((left+right)/2,bottom)` — приближение только при соответствующей семантике полного bbox. Visible-only bbox при закрытых ногах заканчивается на препятствии. Ankle выше подошвы; среднее ankles не обязательно контакт. Маска уточняет силуэт, но не опору при прыжке/окклюзии/тени. Top-down view часто закрывает ноги телом. У автомобиля/погрузчика bottom-center меняет физический смысл с ориентацией и выступающими частями.

Paik et al. (2026) изолировали reference-point bias в Blender: 9 Mixamo-пешеходов, 5 поз опорной фазы, точные keypoints/camera, CCTV высоты 3/5/7 m, UAV 30/50/70 m. Toe midpoint лучше в среднем, но не во всех режимах. Реальные detector errors и весь цикл бега с полётной фазой этим не проверены. Нельзя заключить, что neural pose универсально точнее bbox. Для выбора нужны full-chain сравнения на конкретных кадрах.

<a id="f027"></a>
### F027 — Высотный bias, горизонт и несколько плоскостей

`INFERENCE`, A01-F07 из F021. Камера `C=(Cx,Cy,c)`, точка `P=(X,Y,z)`, горизонтальный пол `Z=0`: пересечение луча даёт `q_hat=Cxy+c/(c-z)*(Pxy-Cxy)`, ошибка `z/(c-z)*(Pxy-Cxy)`. При z≈c задача особенно чувствительна. Это математический вывод с явными предпосылками, не камера-бенчмарк; F005 иллюстрирует числа. Для general plane нужна ray–plane intersection. Одна плоская рампа допускает свою H, координаты измеряют расстояния вдоль неё; ступени/кривой пол/платформы не описываются одной H. Между разными плоскостями нужен общий 3D frame для физической дистанции. В H прямая W=0 — горизонт плоскости. Конечность координат недостаточна; абсолютный порог |W| без нормировки H неинвариантен. Extrapolation за опоры математически возможна, но не подтверждена контролями автоматически; даже convex hull не является гарантией качества.

<a id="f028"></a>
### F028 — Jacobian и разделение ошибок

`INFERENCE` собственных производных A01-F08, подход uncertainty propagation в [S022](SOURCES.md#s022), §4. При обозначениях F021:

```text
Jp=(1/W)*[[h11-X*h31, h12-X*h32],
          [h21-Y*h31, h22-Y*h32]]       # m/px
Sigma_q ≈ Jp*Sigma_p*Jp^T              # conditional on fixed H
```

При допустимой gauge `h33=1`, `theta=(h11,h12,h13,h21,h22,h23,h31,h32)`:

```text
Jtheta=(1/W)*[[u,v,1,0,0,0,-X*u,-X*v],
              [0,0,0,u,v,1,-Y*u,-Y*v]]
Sigma_q ≈ Jp*Sigma_p*Jp^T + Jtheta*Sigma_theta*Jtheta^T
```

Последнее предполагает independence текущей точки и calibration parameters; иначе нужны cross terms. Для raw→undistort→H берут chain-rule Jacobian. Большое singular value Jp указывает локальное усиление, но linear approximation около горизонта не даёт гарантированной границы. Ошибки плоскости, масштаба, скрытых стоп и ID — не автоматически gaussian noise. `calibrateCameraExtended` standard deviations не равны полной covariance H/footpoint. Perturbation/bootstrap требуют обоснованного noise model и отдельной проверки empirical coverage.

<a id="f029"></a>
### F029 — Общая калибровка коррелирует ошибки расстояния и скорости

`INFERENCE`, A01-F08/F09. Для `r=q1-q2`, `Sigma_r=Sigma1+Sigma2-Sigma12-Sigma12^T`; для `d=||r||>0`, `Var(d)≈e^T Sigma_r e`, `e=r/d`. При d≈0 first-order formula плохо определена. Для `v=dq/dt` при независимости dq и dt: `Sigma_v≈Sigma_dq/dt²+(dq*dq^T)*Var(dt)/dt⁴`; при зависимости нужны cross terms. Общий сдвиг и ошибка масштаба влияют по-разному. Нельзя просто считать ошибки двух людей/кадров независимыми, а residual регрессии — полным error bar. Эти формулы не включают ошибки association и не заменяют E-протокол.

<a id="f030"></a>
### F030 — Два независимых слоя проверки геометрии

`HYPOTHESIS`, A01-F10. Сначала H проверяется на физически других measured points/segments: position `e_i=||q_hat_i-q_GT_i||`, RMSE, median/upper quantiles/max и X/Y bias по пространственным стратам; distance `| ||q_hat_a-q_hat_b||-d_GT |` в разных направлениях/длинах. Survey uncertainty сохраняется. Затем измеряется full chain на людях/технике с видимыми/скрытыми контактами, чтобы отделить ошибку H от reference point. Repeated clicks измеряют repeatability, не absolute accuracy. `H^-1 H≈I`, training reprojection RMS и красивая сетка не являются независимым метрическим подтверждением. Budgets назначают до теста из требуемого различения события, не под результаты.

## Полуавтоматизация, lifecycle и наблюдаемость

<a id="f031"></a>
### F031 — Эталоны автоматизируют поиск correspondences

`DOCUMENTED` [S027](SOURCES.md#s027), [S029](SOURCES.md#s029), A02-F01/F03. OpenCV sample intrinsics читает camera/video/images, находит pattern points и сохраняет K/D XML/YAML. ChArUco допускает частичную видимость и сочетает IDs с углами шахматной доски. Это реальный документированный sample, не найденный готовый web onboarding промышленной камеры. Отдельно нужны floor scene mapping и controls. Код/GUI не запускались.

<a id="f032"></a>
### F032 — Спецификация физического ChArUco обязательна

`DOCUMENTED` [S028](SOURCES.md#s028), A02-F02. Хранят число squares X/Y, square length, marker length, dictionary/IDs, файл target и axis convention; документация предупреждает о смене направления board Z после OpenCV 4.6.0. Не все corners доступны при частичной видимости. `INFERENCE`: print scaling, неплоский лист и неверный размер создают systematic scale error; subpixel corner accuracy не равна метрам в цехе.

<a id="f033"></a>
### F033 — AprilTag pose требует known size и K

`DOCUMENTED/CODE_INSPECTED` [S030](SOURCES.md#s030), A02-F04. `apriltag_detection_info_t` получает tagsize в m и fx/fy/cx/cy в px; tagsize измеряется между detection corners на black/white border, не по внешнему листу. Planar pose может иметь два решения. v3.4.5 — BSD-2-Clause, C-библиотека, официальная поддержка Linux; установка на целевом сервере не проверялась. Tag на стене не задаёт floor plane без связи со сценой. Для H можно использовать known coplanar corners напрямую; один маленький tag не проверяет accuracy дальнего пола.

<a id="f034"></a>
### F034 — fSpy демонстрирует scale recovery, а не его отсутствие

`DOCUMENTED/CODE_INSPECTED` [S031](SOURCES.md#s031), A02-F05/F06. Interactive vanishing-point solver использует предположение перпендикулярных world directions; `DEFAULT_CAMERA_DISTANCE_SCALE=10` — условный scale. `computeTranslationVector` масштабирует translation через заданный referenceDistance. Поэтому perspective estimate не означает метрическую сцену. Малодисторсионная pinhole-сцена и пригодные линии — условия; почти параллельные линии ухудшают VP. v1.0.3 — закреплённый stable, GPL-3.0-or-later по header. Не копировать solver как permissive-код. Industrial validation и работоспособность бинарника здесь не проверены.

<a id="f035"></a>
### F035 — Calibmar — готовый GUI для intrinsics

`DOCUMENTED/CODE_INSPECTED` [S032](SOURCES.md#s032), A02-F07/F08. Calibmar 1.1.0 имеет file dialog, Import/Run, проверку параметров и YAML; workflow предусматривает разнообразные views, per-view statistics и экспорт txt/yaml с camera model/size. Zoom/focus/lens changes требуют новой калибровки по документации. BSD-3-Clause для самого проекта, dependencies проверяются отдельно. GitHub — зеркало, releases на университетском GitLab; GitHub без releases не означает отсутствие бинарников. Это intrinsics tool, не готовый editor safety zones; GUI/бинарники не запускались.

<a id="f036"></a>
### F036 — GeoCalib оценивает camera/gravity, не метры пола

`DOCUMENTED/CODE_INSPECTED` [S033–S034](SOURCES.md#s033), A02-F09/F10. Learned calibration предлагает focal/gravity/distortion с covariance/uncertainty; assumes square pixels/no skew, principal point в центре при отсутствии crop; yaw без доп. ограничений ненаблюдаем. `extractor.py` отменяет собственные scale/crop, Gradio UI действительно существует. Это не floor height/origin/absolute scale. Covariance параметров не включает footpoint/domain/scene-survey ошибки. Код Apache-2.0, веса CC-BY-4.0 на проверенном SHA. Запуск, CPU latency и LinQ path неизвестны; future proposal module, а не обязательная нейросетевая зависимость MVP. Геометрические ограничения single-view metrology [S022](SOURCES.md#s022) допускают измерения с доп. опорами, не arbitrary 3D без данных.

<a id="f037"></a>
### F037 — Drift registration — диагностика, не повторная приёмка

`DOCUMENTED` [S035](SOURCES.md#s035), `INFERENCE` A02-F12. `findTransformECC` имеет translation/euclidean/affine/homography models, initial warp/mask, возможную несходимость. Static anchors или fiducials позволяют предложить drift warning. Высокая корреляция не доказывает сохранение метрического масштаба; движущиеся объекты, свет и разная глубина нарушают диагностику. Отсутствие matches означает unknown, а не «камера неподвижна». Компенсация изображения без revalidation H и zones не даёт автоматической валидности.

<a id="f038"></a>
### F038 — Camera profile важнее имени камеры

`DOCUMENTED` [S036](SOURCES.md#s036), `INFERENCE` A02-F13. При известном чистом resize меняются pixel intrinsics, известные crop/rotation также допускают явное преобразование. Неизвестный video mode может менять sensor crop/ISP/dewarping и не сводится resize с тем же aspect ratio. Optical zoom/focus/lens, PTZ и camera move меняют применимость K/D/H; static camera при перестановке станка сохраняет проекцию пола, но теряет semantic validity зоны. Для PTZ нужны отдельно принятые presets либо suspension metric rules.

<a id="f039"></a>
### F039 — Три режима подключения камеры

`HYPOTHESIS`, W02-1…3 из A02, основание F021–F038. (A) Только image polygon + explicit observed point, без m/m/s; принять по independent episodes. (B) Measured floor XY, 4+ широко распределённых fit-pairs, отдельные hold-out controls, H, metric grid, world polygons, validity mask и signed approval. (C) Assisted: board/fiducials либо VP/GeoCalib дают редактируемые proposals, физические предпосылки и scale подтверждает человек, те же controls обязательны. Auto module принимают, если он сокращает настройку и сохраняет качество на независимой проверке. Unknown scale/plane, contradictory controls или camera profile возвращают к ручному/неметрическому режиму. Это наш workflow, не найденное единое industrial приложение.

<a id="f040"></a>
### F040 — Versioned config и объяснимость старого события

`HYPOTHESIS`, A02 proposed contract. Хранить schema/calibration/parent ID, camera/profile/preset, raw размеры/rotation/crop/resize/letterbox/undistort chain, lens/zoom/focus, reference hash/PTS, K/D/Knew и model version, plane frame/units, H direction, fit points/measurement provenance/method/threshold units, physically separate controls/results/budgets, validity mask, image vs metric polygons, drift anchors/outcomes/invalidation reason. Rule permissions/active schedule — отдельно от geometry. Состояния `draft→proposed→controls_pending→validated→active`, при изменении `suspect/invalid`, revalidation создаёт новую immutable version. Событие сохраняет свои calibration/profile/zone versions и raw evidence; последующая правка зоны не должна менять его объяснение задним числом.

<a id="f041"></a>
### F041 — Неопределённость у границы и три статуса

`INFERENCE/HYPOTHESIS` оркестратора из F018/F028–F030. Пусть signed distance s точки от границы положителен внутри, e — обоснованный radial error budget: `s>e` inside, `s<−e` outside, иначе ambiguous. Для proximity threshold r: `d_hat+e<r` уверенно ближе, `d_hat−e>r` уверенно дальше, иначе uncertain — **условно на справедливости error bound**. Empirical quantile не является гарантированной bound. Candidate warning policy может быть консервативнее и учитывать пересечение uncertainty envelope с опасной зоной; candidate не называют подтверждённым нарушением. Три итоговых смысла: нарушение по заданному правилу подтверждено; не обнаружено при достаточной наблюдаемости; сделать вывод невозможно. Последнее не равно safe. Детекторный confidence, RANSAC confidence и метрический error budget не взаимозаменяемы.

<a id="f042"></a>
### F042 — Версии OpenCV и лицензия: что установлено

`LOCAL_OBSERVATION` чтения release metadata A01, [S025](SOURCES.md#s025). `/4.x/` redirected в 4.13.0; `/4.14.0/`, `/5.0.0/` вернули 404 у инструмента. Архив указывает 5.0.0 датой 2026-08-19 и 4.14.0 2026-07-19, GitHub REST 5.0.0 — `2026-06-06T10:52:34Z`; расхождение дат не разрешено. Нельзя заключить ни «4.13.0 latest», ни «5.0.0 не существует». Нужные API/код проверены именно 4.13.0, A02 patterns/ECC — отдельно 4.12.0. [S026](SOURCES.md#s026), [S036](SOURCES.md#s036): Apache-2.0, сторонние notices сохраняются. Никакого локального installed package или binary compatibility это не доказывает.

## Proximity: измеряемая величина и смысл опасности

<a id="f043"></a>
### F043 — Mode/action-specific threat и legitimate proximity

`DOCUMENTED` [S037](SOURCES.md#s037), [S040](SOURCES.md#s040), `INFERENCE` A04-F01/F11. В NIOSH зоны связаны с конкретными опасными движениями машины; HSE описывает допустимую работу сигнальщика при reversing. Переносимый принцип — хранить hazard type, machine mode, guard и допустимую операцию. Близость сама не является нарушением, но blanket authorization также не отменяет любой физический риск. Положение плеч не доказывает внимание работника. Это рабочий контекст, не установленное право РФ и не доказанная система распознавания ролей.

<a id="f044"></a>
### F044 — Множество возможных положений вместо точного пикселя

`DOCUMENTED` [S037](SOURCES.md#s037), A04-F02: magnetic prototype NIOSH представляет uncertainty положения датчика кругом и рассматривает пересечение с action zone, учитывая размещение на теле. `INFERENCE`: для CCTV переносима конструкция возможного положения/envelope. Радиусы и точность магнитной системы не переносимы: для камеры нужен свой error budget, отдельно от радиуса модели тела и физического protective margin.

<a id="f045"></a>
### F045 — Полезная демонстрация с ошибочным для пола входом

`REPORTED_EXPERIMENT` [S038](SOURCES.md#s038), A04-F03: 12 минут строительного CCTV в Сеуле, исходник 30 fps 1280×720, обработка 640×360, RTX2080Ti, YOLOv3/OpenPose; известные габариты техники и worker ellipse. `INFERENCE` критического чтения §2.5: floor H применяется к центру bbox человека и плечевым точкам выше пола. Это нельзя копировать как ground localization; footprint идея не исправляет неверный anchor. Showcase не подтверждает event accuracy нашего домена, предотвращение травм или LinQ path. Разные выводы статьи сохраняются раздельно.

<a id="f046"></a>
### F046 — Уровень 1: фиксированная опасная зона

`INFERENCE/HYPOTHESIS`, A04-F04 из F021/F043 и [S043–S044](SOURCES.md#s043). Интегратор задаёт `Z(mode,t)` — конкретную опасную область, не обязательно корпус станка. Наблюдение `P_h(t)∩Z≠∅`, где P_h — footpoint или заранее определённый body envelope. `covers(Z,p_h)` включает границу; intersection envelope и footpoint intrusion — разные события. Без масштаба image polygon допустим, но означает проекцию выбранной точки в размеченной области, не метры и не reach-in руками. Mode/permission/active schedule неизвестны — geometric candidate, не доказанное нарушение. CPU point/polygon algorithms возможны вычислительно, разрешённость такой схемы кейсом UNKNOWN.

<a id="f047"></a>
### F047 — Уровень 2: расстояние до footprint

`INFERENCE`, A04-F05. `F_m(t)=q_m(t)+R(theta_m(t))*F0(mode,load)`; anchor q_m не равен автоматически bbox center. `g=dist(P_h,F_m)` — минимальное расстояние между горизонтальными множествами в m; intersection даёт g=0, не penetration depth. Для circle человека снаружи `g=max(0,dist(p_h,F_m)-r_h)`. Расстояние до polygon boundary опасно подменять distance до polygon: точка внутри может быть далеко от boundary, хотя overlap уже есть. Point-to-point distance не является зазором до вил/груза/кузова. Silhouette segmentation верхних частей машины через H не превращается в footprint. Heading кузова отдельно от направления скорости — reverse/standstill/turning это выявляют. Реальный 3D hand-to-part clearance здесь не измеряется.

<a id="f048"></a>
### F048 — Форма, uncertainty и protective margin различаются

`INFERENCE`, A04-F06. Если position/footprint ошибки действительно ограничены e_h и e_m (для формы — Hausdorff distance), `|g_true-g_hat|≤e_h+e_m`. Это условное Lipschitz-следствие, не выполненный тест. Calibration/shape/heading errors должны войти в budgets; empirical quantiles не deterministic guarantees. При unknown heading можно взять union допустимых oriented footprints или bounding circle; это conservative envelope с большими ложными кандидатами. Если envelope перекрывает всё рабочее место, лучше ограничить функцию, чем выдавать его за точную машину.

<a id="f049"></a>
### F049 — Уровень 3: closing speed и TCA

`INFERENCE`, A04-F07 из F007/F014/F047. `r=p_h-q_m` m, `u=v_h-v_m` m/s; closing speed `c=−r·u/||r||` при r≠0. `||u||` не равно радиальной скорости сближения. При `u·u>0`: `TCA=clip(−r·u/(u·u),0,T)`, `d_CA=||r+u*TCA||`. При u≈0 проверяют текущий gap; малый TCA при большом d_CA не означает collision. T — заявленный short-term prediction horizon, численно не установлен. Все скорости и позиции синхронизированы, с контролем возраста/gap/ID.

<a id="f050"></a>
### F050 — TTC для кругов, условия и единицы

`INFERENCE` самостоятельного constant-velocity вывода A04-F08; термин surrogate TTC в [S039](SOURCES.md#s039), дорожные thresholds не перенесены. Для суммарного radius R: решить `||r+u*tau||²=R²`. `a=u·u`, `beta=r·u`, `c0=r·r−R²`, `D=beta²−a*c0`. При c0≤0 TTC=0; иначе при a>0,beta<0,D≥0 earliest root `(-beta-sqrt(D))/a`, если в `[0,T]`. В других случаях future collision **в данной модели** не предсказано. Численная устойчивость a≈0/D≈0 требует проверки. TTC измеряется в s; `g/||u||` не general TTC. PET — иной, часто постфактум, временной разрыв занятия конфликтного места.

<a id="f051"></a>
### F051 — Prediction требует одновременности и новой информации

`INFERENCE`, A04-F09: для footprints `tau_hit=inf{tau∈[0,T]:P_h(t+tau)∩F_m(t+tau)≠∅}`. Swept-area overlap за весь T не доказывает одновременного занятия. Можно назвать его conservative route warning, но не collision. Поворот требует theta(t), load geometry и turn uncertainty. Discrete time slices способны пропустить краткое касание; нужен bound шага, continuous test либо conservative envelope. ID switch, stale frames и lag smoothing создают ложные прогнозы. Пока нет валидных anchors/time/heading, разумнее fixed corridor или текущий gap.

<a id="f052"></a>
### F052 — Остановочная зона не получается из detector confidence

`INFERENCE`, A04-F10: только для прямолинейной модели с задержкой L и гарантированным постоянным `a_min>0`, `s_stop=v*L+v²/(2*a_min)`, `T_stop=L+v/a_min`. Реакция человека/водителя/контроллера и end-to-end цепь должны быть определены; overlapping latency components не суммируют дважды. Нагрузка/пол/уклон/тормоз меняют a_min. [S041](SOURCES.md#s041), A04-F12 — чужая onboard multispectral forklift work, не fixed CCTV и не наши численные пороги. Без measured L/a_min/action contract нельзя обещать предотвращение столкновения; offline replay не доказывает оперативность.

<a id="f053"></a>
### F053 — Конвейер, кран и груз — разные угрозы

`DOCUMENTED` [S045](SOURCES.md#s045), `INFERENCE` A04-F14. Предусмотренный walk-under, reach-in к ролику и обслуживание конвейера различаются режимом, ограждением и доступными nip points. Footpoint polygon не измеряет пальцы у ролика. У крана отдельно задаются зона основания/противовеса и suspended-load operation perimeter; bbox груза нельзя переводить H пола в true vertical projection. Составу полезен known track corridor и габарит, но train-specific field benchmark в этой волне не установлен. Эти конфигурации — гипотезы по конкретной сцене, не автоматическое распознавание всех угроз.

<a id="f054"></a>
### F054 — Shapely semantics и invalid geometry

`DOCUMENTED/CODE_INSPECTED` [S042–S044](SOURCES.md#s042), A04-F13. В Shapely 2.1.2 `distance` — Cartesian distance, wrapper вызывает GEOS `lib.distance`; `buffer` — круговой Minkowski buffer с аппроксимацией, `covers` включает boundary. Единицы исходят из coordinate system, библиотека не делает pixels метрами. `None`/empty geometry могут дать NaN: результат нельзя превращать в safe из-за false comparison. Validate finite/validity и вернуть indeterminate. BSD-3-Clause для Shapely не отменяет dependency notices. APIs не запускались.

<a id="f055"></a>
### F055 — Ground truth proximity, violation и prediction раздельны

`INFERENCE/HYPOTHESIS`, A04 test protocol. Hard negatives: legitimate work у пульта, maintenance с подтверждённой изоляцией, signaller, человек за барьером/в кабине, параллельный проход, reverse/turn, штатный walk-under. Label current gap≤b отличается от semantic violation и от model-predicted conflict. Прогноз, после которого водитель затормозил, нельзя автоматически объявлять false positive по отсутствию финального collision: требуется заранее определённый target и отдельные данные о причинной реакции. Data split по манёврам/эпизодам/камерам, не соседним кадрам. Необходимы shape/heading/gap error, event quality, indeterminate coverage и age/lead-time, а не только detector accuracy.

## Сложная сцена и условная метрология одной камеры

<a id="f056"></a>
### F056 — Некоторые высоты измеримы при дополнительных опорах

`DOCUMENTED` [S022](SOURCES.md#s022), A05-F01. Single View Metrology использует vanishing line reference plane, vanishing point дополнительного направления и масштаб, например известную вертикальную длину. Соответствующие top/base должны принадлежать заданному направлению. Это условная метрология структурированной сцены. Она опровергает абсолютное «одна камера никогда не измеряет высоту», но не следует из одной floor H. Случайные голова и ступня согнувшегося человека не образуют гарантированную вертикаль. Прочитана конференционная версия ICCV1999, не полный IJCV2000 текст.

<a id="f057"></a>
### F057 — Известная 3D-сцена снимает часть неоднозначности луча

`INFERENCE`, A05-F02/F03 из F021/F027. При known K,R,C и плоскости `n^T X+d=0` мировой ray `r=R^T K^-1 [u,v,1]^T` пересекается при `lambda=−(n^T C+d)/(n^T r)`, `X=C+lambda*r`, если denominator≠0, depth положительна и системы согласованы. Без ограничения lambda неизвестна. Known load-height plane позволяет получить 3D contour и затем vertical projection, но rotating volumetric load требует формы/pose, а не только центра. Kinematic crane telemetry без swing bounds также недостаточна. Floor H возвращает optical-ray floor intersection, не vertical projection груза — F027.

<a id="f058"></a>
### F058 — Настроенная lifting envelope честнее неподтверждённого «под грузом»

`DOCUMENTED` отраслевого контекста [S051](SOURCES.md#s051), `INFERENCE` A05-F04. Known floor polygon всего допустимого диапазона lifting operation с запасом может поддерживать событие «вход в настроенную зону подъёма». Это не доказательство нахождения под текущим грузом. Bbox overlap может быть и при разных глубинах, а отсутствие overlap не исключает нависающий невидимый объём. Для actual under-load нужны синхронная geometry/pose/height/telemetry, дополнительные views/sensors либо достаточно ограниченная известная сцена. Размеры зоны и правило РФ неизвестны; HSE — не их замена.

<a id="f059"></a>
### F059 — OpenPose: body/foot keypoints, но не бесплатная универсальная 3D

`DOCUMENTED/CODE_INSPECTED` [S046](SOURCES.md#s046), A05-F05. Bottom-up Part Affinity Fields; body/foot output, JSON coordinates+confidence зависят от `--keypoint_scale`. Формат 3D-output не доказывает monocular metric depth. License предусматривает noncommercial research restrictions; permissive MIT/Apache не заявляется. Foot point остаётся кандидатом contact, не доказательством опоры. LinQ/export и применимость лицензии к выбранному использованию UNKNOWN.

<a id="f060"></a>
### F060 — RTMPose: другая pose-цепочка и свои входные ошибки

`DOCUMENTED` [S047](SOURCES.md#s047), A05-F06. Top-down detector+crops, SimCC coordinate classification; skip detection/pose NMS/smoothing описаны в §3.5. Missed person может не попасть в crop. Apache-2.0 MMPose code не фиксирует все условия весов; skeleton schema и checkpoint provenance выбирают отдельно. Публичные Intel/NVIDIA/mobile цифры и ONNX backend не доказывают LinQ-совместимость. Отдельная pose-сеть — neural inference, не обычная CPU-геометрия.

<a id="f061"></a>
### F061 — Relative Depth Anything V2 не имеет обещанных метров

`DOCUMENTED/CODE_INSPECTED` [S048](SOURCES.md#s048), A05-F07. Стандартный `DepthAnythingV2.forward` использует ReLU; metric branch отдельна. Положительность значений и цветовая палитра не устанавливают абсолютный scale. Root README: Small Apache-2.0, Base/Large/Giant CC-BY-NC-4.0. Relative depth годится как гипотеза порядка поверхностей; сантиметровый порог требует внешней привязки и отдельной hold-out проверки. Изменение палитры между кадрами не равно physical motion.

<a id="f062"></a>
### F062 — Metric V2: единицы выхода не равны точности clearance

`DOCUMENTED/CODE_INSPECTED` [S049](SOURCES.md#s049), A05-F08. Metric weights fine-tuned Hypersim indoor и Virtual KITTI outdoor, README `max_depth=20` / `80 m`, output H×W в m. Head sigmoid умножается на max_depth; смена параметра без подходящих весов не калибрует модель. Цех, блестящий металл, тонкие тросы/сетки и unusual view требуют собственных independent depth/clearance controls. Положение видимой поверхности не раскрывает скрытого человека или connector. Accuracy и LinQ path не измерялись.

<a id="f063"></a>
### F063 — Metric3D: intrinsics и режим evaluation важны

`DOCUMENTED/CODE_INSPECTED` [S050](SOURCES.md#s050), A05-F09. Canonical camera transformation использует focal length; `transform_test_data_scalecano` получает `[fx,fy,u0,v0]`. В прочитанном testing path есть `.cuda()`; это не готовый CPU/LinQ маршрут. Metric evaluation без scale alignment отличается от affine-invariant результата с scale/shift fit к GT. Default focal и подгонка к test GT не доказывают absolute metric accuracy. BSD-2-Clause code, README отдельно адресует commercial вопросы авторам; weights/dependencies проверяют отдельно.

<a id="f064"></a>
### F064 — Конфликт лицензии конкретных V2 weights не разрешён

`LOCAL_OBSERVATION/DOCUMENTED` чтения [S048](SOURCES.md#s048), [S052](SOURCES.md#s052), A05-F10. Root README относит Large к CC-BY-NC-4.0, авторская HF card `Depth-Anything-V2-Metric-Hypersim-Large`, README revision `7972080`, содержит Apache-2.0. Small card revision `3bc65d4` тоже Apache-2.0. Это разные уровни metadata; юридическое наследование выбранного artifact не установлено. Не делать универсальный запрет всех metric V2 и не обещать commercial suitability Large по badge. Нужен exact checkpoint/revision и однозначные условия автора, Q012.

<a id="f065"></a>
### F065 — Падение, неподвижность и страховка: наблюдаемое отличается от причины

`INFERENCE`, A05 matrix/F11/F13. Горизонтальный bbox может быть нормальной работой лёжа; fall требует перехода/temporal evidence. Неподвижный track может означать stale frame, потерю человека или filter prediction; нужны fresh source data и видимость, а не вывод о сознании. Harness visible не доказывает connector/anchor relation и правильность крепления; отсутствие детекции при закрытом карабине не доказывает отсутствие привязи. Для fence crossing линия/переход стороны не равны climbing; under conveyor «до/под/за» неоднозначны при occlusion. Опора платформы требует её plane_id. Правило получает свой observability gate, а не один общий camera confidence.

<a id="f066"></a>
### F066 — Разметка трудных сценариев должна сохранять unknown

`HYPOTHESIS`, A05-F12. Scene annotations: plane IDs/geometry, edges/barriers/проходы, occlusion regions, lifting envelope semantics/time, machine state. Object labels: source time/ID, bbox semantics, keypoint schema/scale/visible/occluded/out-of-frame, contact отдельно от ankle. Harness labels: worn/visible lanyard/connector/anchor/attachment relation/unknown. Event labels: onset/offset/context/visibility intervals, normal floor work и authorised entry. Не дорисовывать hidden contact как измеренный GT. При исчезновении после positive event сохранять последнее подтверждение и текущий indeterminate отдельно; скрытый интервал нельзя ретроспективно объявить безопасным.

## Инструменты, доступность и воспроизводимость

<a id="f067"></a>
### F067 — Минимальное geometric ядро и реальные требования

`DOCUMENTED/INFERENCE`, A06-F01 из [S015–S017](SOURCES.md#s015), [S055](SOURCES.md#s055). OpenCV — sparse transformations, Shapely — Cartesian zones/distance/topology. Для проверенной Shapely2.1.2: Python≥3.10, GEOS≥3.9, NumPy≥1.21, BSD-3-Clause; GEOS LGPL-2.1 notices отдельно. Это candidate dependency set, **не выполненный lock/import тест**. GPU для этих mathematical operations не требуется, но latency сервера неизвестна. Annotation и tracker не обязаны быть runtime dependency геометрического demonstrator; ручные tracks показывают только отдельный слой, не end-to-end tracking.

<a id="f068"></a>
### F068 — Конфликт declared dependencies OpenCV wheel/Norfair

`CODE_INSPECTED` package manifests [S054](SOURCES.md#s054), [S057](SOURCES.md#s057), A06-F02. `opencv-python-headless==4.13.0.92` для Python≥3.9 требует `numpy>=2`; Norfair v2.3.0 задаёт NumPy `^1.23.0`, то есть `<2`. Для совместного Shapely2.1.2 baseline на Python≥3.10 это несовместимые декларации. Norfair Python `^3.8`, optional `opencv-python<5.0` не устраняет NumPy конфликт. Установка не выполнялась: нельзя заявлять работоспособность/невозможность всех адаптаций. Нужны другой проверенный build/version, изоляция/adapter либо иной tracker; `--no-deps` не является доказательством compatibility.

<a id="f069"></a>
### F069 — Tracker package может добавить лишние предпосылки

`CODE_INSPECTED` [S058](SOURCES.md#s058), A06-F04. Original ByteTrack MIT по pinned SHA, но tracker импортирует torch, использует `np.float`, `frame_id+=1` и frame_rate-dependent buffer; requirements имеют старые ONNX pins и unpinned NumPy. `img_info/img_size` rescale может дважды преобразовать уже восстановленные detections. Это наблюдение одного original commit, не всех ports. Не рекомендовать его как plug-and-play CPU installation; frame lifetime при VFR/редком sampling требует time-aware adapter. Norfair — BSD-3-Clause candidate без обязательного GPU для tracker, но manifest conflict F068 остаётся. Лицензия original ByteTrack не определяет лицензию Ultralytics-порта.

<a id="f070"></a>
### F070 — Shapely не 3D engine; boundary policy явная

`DOCUMENTED` [S055–S056](SOURCES.md#s055), [S044](SOURCES.md#s044), A06-F06–F08. Геометрия анализируется в XY, Z игнорируется. Конструктор Polygon не гарантирует validity; automatic make-valid может изменить semantic zone. `contains(zone,boundary_point)=False`, `covers(...)=True`. Это topology, не uncertainty band. Hole/corner/touching tests и units входят в config. Distance до заполненного polygon не signed depth; NaN handling см. F054.

<a id="f071"></a>
### F071 — Official perspective demo полезен, но не метрический benchmark

`CODE_INSPECTED` [S053](SOURCES.md#s053), A06-F09. `perspectiveCorrection` находит board corners в двух изображениях, строит H/warp/соответствия и normalization. Destination — другой image, не measured floor XY. Есть imshow/waitKey: без изменений не headless pipeline. Прочитан, не запущен. Годится для понимания direction, не подтверждает scale/industrial accuracy.

<a id="f072"></a>
### F072 — EPFL ground-plane GT дискретен

`DOCUMENTED` [S060](SOURCES.md#s060), A06-F10. Calibrated synchronized views и GT части записей полезны для coordinate/localization tests; GT grid, sampling step и undefined/out-of-grid codes требуют чтения конкретного файла. Image→topview не гарантирует units m без interpretation `grid_to_tv`. Research-use terms не равны безусловной публичной/коммерческой лицензии. Архив не получен; непрерывная speed GT из grid labels не установлена. Не использовать как доказательство forklift/running safety.

<a id="f073"></a>
### F073 — BrnoCompSpeed показывает независимый speed GT, доступ не гарантирован

`DOCUMENTED/REPORTED_EXPERIMENT` abstract [S061](SOURCES.md#s061): 18 примерно часовых Full-HD videos, 6 locations, 20,865 vehicle instances, optical LiDAR gates и reference GPS tracks. Полный paper не прочитан, accuracy методов не извлекается. `CODE_INSPECTED` README [S062](SOURCES.md#s062): Python2 evaluator, road-plane positions/scale, Download просит связаться с автором; старый tar URL не подтверждён скачиванием. Dataset/code license UNKNOWN, условия не выдумываются. Secondary 21/7 не смешиваются с прочитанными 18/6; нужна версия реального архива. Vehicle benchmark не доказывает person gait или industrial events.

<a id="f074"></a>
### F074 — CVAT удобен для GT, но XML frame не PTS

`DOCUMENTED` [S059](SOURCES.md#s059), A06 shortlist/F13. Community v2.80.0 MIT, docs открыты как develop; exact format совпадение с release не проверено. Points/tracks/occluded/outside/keyframe пригодны для reference annotations. Interpolation — инструмент разметчика, не измерение каждой скрытой позиции. Нужна отдельная frame→source PTS таблица. CVAT не обязательная runtime dependency; Docker/ресурсы и enterprise/cloud conditions не проверялись.

<a id="f075"></a>
### F075 — События сопоставляются one-to-one

`HYPOTHESIS/INFERENCE`, A06-F14. До test фиксировать event class/camera/zone/participant mapping, intervals/onset tolerance, dwell/merge/cooldown/boundary. Для interval events temporal IoU=`|I_pred∩I_GT|/|I_pred∪I_GT|`, threshold tau заранее; для crossing лучше agreed onset tolerance. Один GT даёт не больше одного TP; unmatched prediction FP, unmatched GT FN; track IDs связывают с GT, не требуют буквального равенства. `Precision=TP/(TP+FP)`, `Recall=TP/(TP+FN)`; zero denominators явно undefined, дубли отдельно. Не менять matching по test result.

<a id="f076"></a>
### F076 — FAR, coverage и latency имеют разные знаменатели/часы

`INFERENCE`, A06-F14/F15 и F018. `FAR=FP/camera-hours`, две камеры по часу дают 2 camera-hours; не inference wall-time и не person-hours. Показать все protocol-eligible часы, valid-monitoring часы, downtime/abstention; negative-only FAR отдельно от full timeline FAR. Coverage=`valid decision duration/eligible duration`. Recall по всем GT и дополнительно independently observable GT; отказ на опасном событии не TN. Source onset error отдельно от wall-clock queue/infer/display и replay rate; offline alarm output не равен live latency. Ноль FP на коротком клипе не доказывает нулевой эксплуатационный FAR.

<a id="f077"></a>
### F077 — Бюджеты и test split задаются заранее

`HYPOTHESIS`, A06-F12/F13/F16. До измерений согласовать `B_pos(region)`, `B_dist(region)`, `B_speed(interval)`, event recall/FAR/latency/coverage budgets. Independent survey controls, rule tuning и final test — разные роли данных; после изменения H по controls нужен новый hold-out. Split по trajectories/sessions/cameras в зависимости от claim, bootstrap по независимым episodes/sessions, не соседним frames. Малый N делает P95 нестабильным: сохранять N/raw/max и uncertainty reference. Если far zone не проходит — mask/image-only; temporal evidence недостаточно — sampling/claim change. Post-hoc budget не является прошедшим критерием.

<a id="f078"></a>
### F078 — LinQ/CPU route остаётся условной архитектурой

`UNKNOWN` для правил/SDK/device, `HYPOTHESIS` A06-F17. Если CPU postprocessing разрешён и SDK даёт нужные outputs: uploaded server video→decode+PTS→нейромодель на LinQ→inverse preprocessing один раз→CPU tracking/plane mapping/polygons/time rules→versioned episode+evidence. Embeddings/ReID/pose/depth/action — отдельный neural inference, не скрытая CPU-геометрия. Execution proof требует реальных runtime/model/device logs и matched source frames, не названия файла или NVIDIA-test. Replay bundle: hashes video/config/annotation/detections, OS/Python/package+GEOS/cv2 build, model/runtime IDs, selected timestamps/phase, raw output и geometry reasons. Сервер не подключался, никакие пути/commands LinQ не придуманы.

## Сравнение величин: одинаковые «расстояния» решают разные задачи

Таблица — `INFERENCE` из F021/F026/F043–F058/F070. Численное качество каждого варианта на видео кейса UNKNOWN.

| Величина | Наблюдение и входы | Единицы / смысл | Чего не устанавливает | Независимая проверка |
|---|---|---|---|---|
| Pixel bbox gap/overlap | Image boxes в одном profile | px / видимое наложение проекций | Floor meters, depth order, actual under-load | Разметка projected target и контрпримеры разных глубин |
| Point-to-point floor distance | Two actual floor contacts + surveyed H | m между выбранными опорами | Nearest body/machine surface gap | Separate physical marks; paired contact errors |
| Point/envelope-to-zone | Explicit contact/body model + image/floor polygon | Intrusion; m only with metric frame | Reach-in и arbitrary3D proximity | Boundary episodes/contexts и hold-out distance |
| Footprint gap | Real anchor/shape/heading/load + H | Minimum horizontal projected-set distance | True hand-to-part3D clearance | Shape/heading/gap GT по сторонам/поворотам |
| TCA/d_CA | Synchronized floor positions/velocities + horizon | s до closest approach и m в модели | Collision if closest approach stays distant | Independent trajectories, near-pass/diverging cases |
| TTC | Relative trajectory + physical/defensive shape | First simultaneous modeled contact in s | Prevention/actual driver response | Frozen motion assumptions/lead-time/miss cases |
| Single-view height | Known reference geometry/direction/scale, corresponding top/base | Conditional height under structural model | Arbitrary3D scene/harness topology | Independent heights, pose/visibility failures |
| Learned metric depth | Exact weights/K/preprocessing | Predicted visible-surface depth in m | Hidden objects/validated critical clearance | Independent test depth/clearance, no test scale fit |

## Программы будущих измерений

Консолидированные E001–E010 содержат входы, шаги, метрики, сохраняемые доказательства, исходы и пределы вывода в [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md#программа-экспериментов-предложено-не-выполнено). Все они `HYPOTHESIS`, не выполненные опыты. E001 environment; E002 geometry hold-out; E003 contact A/B; E004 time/speed; E005 events/negatives; E006 sampling+phase; E007 drift/observability; E008 footprint/prediction; E009 complex3D/depth; E010 target execution/demo. Локальное исполнение F004–F006 не подменяет ни один видео/device benchmark.

## Сопоставление исходных и нормализованных идентификаторов

Исходные подробности/неуспешные поисковые следы сохранены без перезаписи в `_WORK/AGENT_01_GEOMETRY.md` … `_WORK/AGENT_06_TOOLS.md`. Источники Axx-S сопоставлены в [SOURCES.md](SOURCES.md); повтор Criminisi между A01/A02/A05 — одна цепочка S022. Формулы и workflows могут иметь несколько нормализованных F, потому что объединены дубли и разделены наблюдение/вывод.

| Исходное происхождение | Итоговые F-ID |
|---|---|
| A01-F01…F07 | F021…F027 соответственно |
| A01-F08/F09/F10 | F028–F029; F014/F029; F030 |
| A02-F01/F03 | F023/F031 |
| A02-F02/F04 | F032; F033 |
| A02-F05/F06; F07/F08; F09/F10 | F034; F035; F036 |
| A02-F11/F12/F13; workflows/config | F021/F056; F037; F038; F039/F040 |
| A03-F01…F10 | F007…F016 соответственно |
| A03-F11/F12/F13/F14; E01 CLI | F006/F017; F017; F018; F019; F020 |
| A04-F01…F10 | F043…F052 соответственно |
| A04-F11/F12/F13/F14 | F043/F055; F052; F054; F053 |
| A05-F01/F02/F03/F04 | F056; F027/F057; F057; F058 |
| A05-F05…F10 | F059…F064 соответственно |
| A05-F11/F12/F13 | F041/F065; F066; F065/F066 |
| A06-F01/F02/F03/F04/F05 | F067; F068; F072/F073; F069; F067/F078 |
| A06-F06/F07/F08/F09/F10/F11 | F070; F070; F054/F070; F071; F072; F073 |
| A06-F12/F13/F14/F15/F16/F17 | F028–F030/F077; F074/F077; F075/F076; F076; F077; F078 |
| Оркестратор: входы/локальный расчёт/границы | F001–F006/F041; остальные собственные синтезы явно помечены |

Источник силы вывода — его указанные условия и доказательства. Несколько исследователей, прочитавших тот же документ, не создают независимого экспериментального подтверждения. Никакие neural inference, installation, video benchmark или field deployment не выполнены; этот остаток сохранён в Q-ID.
