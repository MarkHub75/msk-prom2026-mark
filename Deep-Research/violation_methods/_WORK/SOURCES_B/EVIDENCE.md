# W1_B — сохранённые первичные доказательства

Доступ: 2026-10-23, Europe/Moscow (+03:00); точный интервал сетевого чтения не зафиксирован. Собственные выписки и пересказ, не копии статей. DOC = первичная документация; CODE = чтение исходного кода без запуска; MEAS = опубликованное измерение автора; INF = наш вывод. Дата доступа не является датой публикации. Все ссылки открывались, если явно не указано обратное. Метаданные GitHub дополнительно получены через официальный REST API `/repos/{owner}/{repo}/commits/{ref}` и `/releases/latest`.

## W1-B-S01 — Frigate Zones [DOC]

Автор: Frigate project. URL: https://docs.frigate.video/configuration/zones/ . Дата публикации не указана; online docs version unpinned. Прочитаны разделы Zones, Zone Loitering, Zone Inertia, Speed Estimation, Best practices and caveats. Версия кода отдельно S05–S08; тождественность веб-документации релизу не предполагается.

**W1-B-F01.** Присутствие задаёт нижний центр bbox; величина пересечения рамки с полигоном не используется. Документация описывает `inertia` как последовательные кадры, примеры 3 и 1. `loitering_time` — минимальное время до включения зоны, пример 4 секунды. Это примеры настройки, не промышленные нормативы. Есть различие lifecycle: человек в loitering zone поддерживает review до выхода; для иных объектов stationary влияет на окончание.

**W1-B-F02.** Speed estimation требует четырёхточечной зоны на земле и измеренных длин сторон; рекомендовано прямолинейное движение, стабильная рамка и видимый нижний центр. Вне откалиброванной зоны скорость может искажаться. Производитель подчёркивает оценочный характер скорости. Это не доказательство точности около погрузчика или законности безопасной дистанции.

Практический смысл: anchor и единицы времени должны быть явной частью правила; геометрическое пересечение bbox и footprint-смысл события различаются.

## W1-B-S02 — Frigate MQTT [DOC]

Автор: Frigate project. URL: https://docs.frigate.video/integrations/mqtt/ . Дата публикации неизвестна; version unpinned. Прочитан `frigate/events`, пример before/after payload, `frigate/available`.

**W1-B-F03.** Обновления одного tracked object имеют одинаковый `id`; типы сообщений `new`, `update`, `end`. Первое сообщение публикуется после выхода из false_positive; лучший snapshot или смена зоны создают обновление. Финальное сообщение содержит `end_time`. Payload различает `current_zones` и `entered_zones`, содержит frame/start/end time и snapshot. Availability различает нормальную остановку, неожиданную потерю соединения и online. Это разные lifecycle: состояние процесса, трека и смыслового нарушения нельзя объединять одним флагом.

Ограничение: API сообщает конец трека, но не устанавливает физическую причину исчезновения человека и не обещает доказанный выход из зоны.

## W1-B-S03 — Frigate Filters [DOC]

Автор: Frigate project. URL: https://docs.frigate.video/configuration/object_filters/ . Дата неизвестна; version unpinned. Прочитан Object Scores и Minimum Score.

**W1-B-F04.** `min_score` отбрасывает отдельные слабые детекции; `threshold` связан с медианой истории score, дополненной до минимум трёх элементов. Слишком высокий min_score может удалить далёкие/перекрытые реальные объекты и разорвать треки. В примере документа есть табличная несогласованность score 0.90 против истории 0.95; числа этой таблицы не используем как эталон реализации. Это подтверждение различия detection gate и track confirmation, а не универсальное N из M.

## W1-B-S04 — Frigate release provenance [CODE metadata]

Автор: Frigate contributors. URL: https://github.com/blakeblackshear/frigate/releases/tag/v0.18.2 . GitHub API на дату доступа сообщил latest release `v0.18.2`, опубликован 2026-10-15T22:41:47Z. Tag разрешён через commit API: `cfa08c56b23d23280c3d0a218e5a43182c97445b`, commit date 2026-10-15T12:02:08Z. Это фиксация найденного релиза, не утверждение, что организаторы используют Frigate.

## W1-B-S05 — Frigate zone configuration [CODE]

URL: https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/config/camera/zone.py . Автор/версия S04. Прочитан raw-файл tag v0.18.2, строки 42–57, 108–116.

**W1-B-F05.** Объявленные defaults: `inertia=3`, `loitering_time=0`, `speed_threshold=None`. Валидация предупреждает о совместном loitering_time с distances/speed_threshold. Это источник параметров релиза, не рекомендуемые пороги проекта.

## W1-B-S06 — Frigate TrackedObject.update [CODE]

URL: https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/track/tracked_object.py . Автор/версия S04. Прочитаны initialization 50–80, update 130–390, serialization 400–433. Локаторы особенно 137–151, 186–207, 263–303.

**W1-B-F06.** `zone_score` вычисляется как прежнее сохранённое значение плюс один. Ветка снаружи при промежуточном счёте сохраняет `zone_score-1`, то есть прежнее значение, без обнуления. По чтению этот фрагмент не реализует reset последовательной серии, обещанной S01. После достижения inertia значение уже не обновляется этой веткой. `zone_loitering` увеличивается в подходящих in-zone обновлениях, сравнивается с `loitering_time * detect.fps`; явного сброса при выходе в прочитанном update нет. Это обнаруженное расхождение семантики DOC/CODE, **не проверенный runtime bug**: вызывающий lifecycle и полная трасса могут менять эффект.

**W1-B-F07.** Для отсутствующего в текущем кадре объекта score history получает 0; сохраняются последние десять score. Зональная проверка сама по себе не имеет общего условия свежести frame_time (такое условие есть в speed-ветке). Значит, при интеграции следует отдельно проверять, когда и с какими obj_data вызывается update. Предсказанное положение не становится наблюдением.

## W1-B-S07 — Frigate detection defaults [CODE]

URLs: https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/config/camera/detect.py и https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/config/config.py . Автор/версия S04. Прочитаны DetectConfig 63–78; config.py 842–850.

**W1-B-F08.** `detect.fps` default 5. Неустановленный `min_initialized` вычисляется как max(int(fps/2), 2), `max_disappeared` как fps*5. Это кадровые параметры lifecycle; приблизительное соответствие пяти секундам зависит от частоты реальных обновлений. Defaults не доказывают, что 5 FPS достаточно для наших камер.

## W1-B-S08 — Frigate review cutoff [CODE]

URLs: https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/config/camera/review.py и https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/review/maintainer.py . Автор/версия S04. Прочитаны AlertsConfig/DetectionsConfig и maintainer 139–158, 180–237, 429–555.

**W1-B-F09.** Cutoff defaults 40 секунд для alerts и 30 для detections; maintainer проверяет frame_time относительно последней активности плюс cutoff. Для законченного review end_time берётся из last_alert_time/last_detection_time. Это задержка закрытия/группирования review, **не cooldown запрета следующего самостоятельного нарушения**. Review использует current_zones; severity tracked object в другом участке использует entered_zones. Нельзя переносить semantics одного поля на весь проект.

## W1-B-S09 — Supervision PolygonZone [DOC + CODE]

Автор: Roboflow contributors. Docs: https://supervision.roboflow.com/latest/detection/tools/polygon_zone/ . Прочитаны Attributes и код trigger. Latest release API: `0.31.1`, 2026-10-20T18:13:09Z; tag commit `f2adfadf2cf9050f44bcb0e71b4b160d8746eab1`, 2026-10-20T18:04:12Z. Код прочитан raw tag: https://github.com/roboflow/supervision/blob/f2adfadf2cf9050f44bcb0e71b4b160d8746eab1/src/supervision/detection/tools/polygon_zone.py , init 84–122, trigger 134–213.

**W1-B-F10.** Default anchor BOTTOM_CENTER; `require_all_anchors=True` использует all, False — any. Это проверка заданных точек маской, не точное пересечение bbox-полигон: даже any четырёх углов не покрывает случай тонкого полигона через середину bbox. Trigger округляет координаты, проверяет bounds, суммирует попадания. Опциональный coord_transform преобразует anchors; он требует корректной оценки движения камеры извне.

**W1-B-F11.** В прочитанном trigger tracker_id не используется, хотя warning документации говорит о нём. Для текущего count identity не нужна; для уникальных входов и dwell её нужно хранить отдельно. Это CODE/DOC расхождение, не проверенный runtime defect.

## W1-B-S10 — NVIDIA Gst-nvdsanalytics [DOC]

Автор: NVIDIA. URL: https://docs.nvidia.com/deepstream/text/DS_plugin_gst-nvdsanalytics . Доступный dev-guide перенаправил на документацию с меткой версии **9.2**; дата публикации не установлена. Старый URL 7.1 позднее дал ошибку archive redirect; не приписываем прочитанное версии 7.1. Прочитаны вводные 27–32, Features, Configuration File Parameters 70–109.

**W1-B-F12.** ROI использует bottom center; direction/line crossing требуют tracker-id и истории. Линия задаётся отдельно от вектора направления. `extended=0` ограничивает пересечение отрезком, 1 — продолженной линией. `mode` strict/balanced/loose регулирует допустимое направление, численные угловые пороги не раскрыты. config-width/config-height задают исходное разрешение, правила масштабируются для runtime. Масштабирование разрешения не означает компенсацию pan/zoom/смены ракурса. Документ подтверждает декларативные параметры и metadata output, но не переносимость самого NVIDIA plugin на LinQ.

## W1-B-S11 — OpenCV homography [DOC]

Автор: OpenCV contributors. URL после редиректа: https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html . Версия 4.13.0; дата публикации неизвестна. Прочитаны Introduction, Basic theory и coplanar/perspective correction sections.

**W1-B-F13.** Planar homography задаёт преобразование плоскостей матрицей 3×3 с восемью степенями свободы. Это основание проектировать ground-plane geometry. Применять floor homography к голове, ковшу, поднятым вилам или человеку на платформе — дополнительное необоснованное предположение. Сам документ не даёт требуемой для безопасности ошибки расстояния.

## W1-B-S12 — ByteTrack [MEAS автора + CODE]

Авторы: Yifu Zhang et al. Статья: https://arxiv.org/abs/2110.06864v3 , v3 2022-04-07; прочитаны abstract и metadata. Код: https://github.com/FoundationVision/ByteTrack/blob/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/byte_tracker.py , BYTETracker.__init__/update; commit 2022-12-11T07:05:00Z, получен API main на дату доступа. Второй файл: https://github.com/FoundationVision/ByteTrack/blob/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/kalman_filter.py , KalmanFilter.__init__.

**W1-B-F14.** Двухэтапная association использует слабые детекции для восстановления существующих tracklets. В прочитанном коде низкая группа ограничена score>0.1, а high зависит от track_thresh. `frame_id` увеличивается на вызов update, `buffer_size=int(frame_rate/30*track_buffer)`; Kalman dt фиксирован 1. Поэтому передача frame_rate меняет буфер, но сама не вводит переменный timestamp в motion model. Эти параметры — конкретная реализация, не нормативы.

Ограничение: benchmark abstract на MOT17 не отвечает на event-F1 в цехе. Низкие score следует сохранять для association, не автоматически принимать их за надёжные атрибуты СИЗ.

## W1-B-S13 — OC-SORT [MEAS автора + метод]

Авторы: Jinkun Cao, Jiangmiao Pang, Xinshuo Weng, Rawal Khirodkar, Kris Kitani. URL: https://arxiv.org/html/2203.14360v3 , 2023-03-16; CVPR 2023. Прочитаны abstract, §3–4, §5.2, Table 2, KITTI limitation, Appendix F. PDF CVF дал 403, использован авторский arXiv HTML.

**W1-B-F15.** На MOT20-test с одинаковыми detections Table 2: ByteTrack/OC-SORT HOTA 61.3/62.1, MOTA 77.8/75.5, IDF1 75.2/75.9, IDs 1223/913, Frag 1460/1198. Улучшение association сопровождается снижением MOTA: единственный показатель не выбирает метод. ORU исправляет накопленную motion error после повторного наблюдения; виртуальные наблюдения не являются доказательствами видимого нарушения. Авторы прямо отмечают низкий/нулевой IoU при low FPS или быстрых объектах в default IoU association. Внешность — дополнительная cue, а не гарантия.

## W1-B-S14 — BoT-SORT [CODE + авторское описание]

Авторы: Nir Aharon, Roy Orfaig, Ben-Zion Bobrovsky. Статья: https://arxiv.org/abs/2206.14651v2 , 2022-07-07; прочитан abstract/metadata. Код: https://github.com/NirAharon/BoT-SORT/blob/251985436d6712aaf682aaaf5f71edb4987224bd/tracker/bot_sort.py . API main commit date 2022-10-30T15:12:42Z. Прочитаны BOTSORT init/update, ReID/GMC/association.

**W1-B-F16.** ReID опционален через with_reid; FastReID encoder вызывается на dets. GMC применяется отдельно к track states. Appearance distance маскируется и appearance threshold, и геометрическим proximity threshold. Значит, добавление ReID не гарантирует спасения очень большого разрыва между кадрами при неизменном gate. Семейство без ReID и с ReID имеет разную нейровычислительную нагрузку; GMC не калибрует автоматически физическую опасную зону.

## W1-B-S15 — AXIS Object Analytics manual [DOC]

Автор: Axis Communications. URL: https://help.axis.com/en-us/axis-object-analytics . Дата публикации неизвестна; online manual version unpinned. Прочитаны Modify a scenario, Calibrate perspective, PTZ preset, Ignore short-lived objects, Record video when human stays too long.

**W1-B-F17.** Time in area и Keep active while tracked — отдельные настройки. Последняя держит rule активным по треку, а не только на время alarm. Short-lived filter задерживает реакцию; запись нуждается в prebuffer. Perspective calibration использует объекты известной высоты на земле; поддержка зависит от камеры. При смене PTZ preset нужна перекалибровка; рекомендация manual — минимум 15 секунд между preset в guard tour. Это конкретный продуктовый режим, не универсальное время стабилизации камеры.

## W1-B-S16 — AXIS Object Analytics API [DOC]

Автор: Axis Communications. URL: https://www.developer.axis.com/vapix/applications/axis-object-analytics-api/ . Дата неизвестна, website unpinned; примеры apiVersion 1.2, поддержку надо получать от устройства. Прочитаны Configuration capabilities, Scenario types/triggers/filters, Short-lived objects, Occupancy in area.

**W1-B-F18.** `timeShortLivedLimit` отсчитывает время видимости объекта в изображении: объект, уже видимый дольше фильтра, может сразу вызвать alarm при входе в include area. Это не dwell внутри зоны. `triggerDelay` occupancy — секунды после достижения численного порога. Разрешённые min/max/default и комбинации сценариев запрашиваются `getConfigurationCapabilities`; нельзя назначить один универсальный набор для всех камер. Speed filter в прочитанном API требует secondary radar, поэтому не служит доказательством monocular metric speed. В строках таблицы capabilities есть расхождения имён Time/Distance; буквальные примеры следует проверять capabilities, не копировать механически.

## W1-B-S17 — Monocular proximity around excavator [MEAS автора, качественные результаты]

Авторы: Hyojoo Son, Hyunwoo Sung, Hyunchul Choi, Sungwook Lee, Changwan Kim. 2017, ISARC pp.500–505, DOI 10.22260/ISARC2017/0069. URL полного текста: https://www.iaarc.org/publications/fulltext/ISARC2017-Paper069.pdf . Прочитаны §2–5, страницы PDF 2–5; фигуры 1–5 рассмотрены через извлечённый текст/описания; screenshot вызван, но изображение инструмент не вывел, поэтому визуальная QA рисунка не заявляется.

**W1-B-F19.** Исследование допускает monocular proximity при известных высоте/азимуте камеры и плоской земле; камера на корпусе экскаватора, distortion correction, shadow removal, perspective transforms. Пример выделяет препятствия высотой минимум 1 м и круговую область для заданного экскаватора; это условия метода, не безопасные нормативы. В conclusion отказ от planar-ground assumption остаётся future work. Публикация показывает примеры работы, не даёт измерения event false alarms/hour. Для цеха нужны собственные ground calibration и модель footprint/рабочего органа.

## W1-B-S18 — DCASE 2022 event matching [DOC протокола]

Авторы: организаторы DCASE Task 4 (Romain Serizel et al., список на странице). URL: https://dcase.community/challenge2022/task-sound-event-detection-in-domestic-environments . Контекст 2022, дата последнего обновления неизвестна. Прочитаны Strong annotations, Evaluation metrics и Contrastive metric.

**W1-B-F20.** Публичный протокол разделяет intersection-based и collar-based event F1; collar example onset 200ms, offset max(200ms,20% duration), с явно выбранным operating point. Это **аудиозадача**; переносим только принцип объявленного temporal matching и отдельно class/time annotations. Указанные допуски и результаты нельзя объявлять стандартом промышленной видеоаналитики.

## W1-B-S19 — ITV/Axxon registry manuals: доступ частичный, параметры не приняты как факт

Зацепки: https://docs.itvgroup.ru/confluence/pages/viewpage.action?pageId=157705313 ; https://docs.itvgroup.ru/confluence/download/attachments/337546226/RegistryKeys.pdf?api=v2 ; https://docs.itvgroup.ru/confluence/download/attachments/136937518/RegistryKeys.pdf . Web один раз открыл первые страницы/оглавление 344-страничного «Интеллект 5.0», updated 06.02.2025. Последующее чтение целевых страниц не удалось (502/TLS EOF); standalone 4.11 page metadata: Roman Nazarov, обновление Evgeniya Kononova 26.11.2025.

Поисковые сниппеты содержат `VMDA.oneAlarmPerTrack`, `LongInZoneTimeout2`, `report_frequency`; это полезные точные ключи для второй волны, но окружающие таблицы нужной версии реально не прочитаны. **Не использовать defaults 1/10sec/3000ms из этой зацепки как доказанные параметры нашего отчёта.** Нет подтверждённого документа приёмочных испытаний или закупки по промышленной безопасности.
