# W1_B — журнал поиска и локализованные пробелы

Дата доступа 2026-10-23 Europe/Moscow. Поиск web, первичное чтение web/open; GitHub raw и API — PowerShell Invoke-WebRequest/Invoke-RestMethod. Training, benchmark и запуск трекеров не проводились.

## Сильные цепочки

- Frigate zones → filters → MQTT → release API → pinned v0.18.2 config/tracked_object/review maintainer. Закрыто различие геометрии, lifecycle и cutoff. Обнаружены DOC/CODE расхождения; runtime эффект остался экспериментом.
- supervision PolygonZone → latest/release API → tag 0.31.1 → Git tree: исходники перемещены в `src/supervision/...`; прежний путь дал 404. Прочитан актуальный trigger, подтверждён anchor-based смысл.
- ByteTrack paper → original repository redirect FoundationVision → commit API → byte_tracker.py + kalman_filter.py. Прочитан фиксированный dt и frame-based lost buffer.
- OC-SORT CVPR → PDF 403 → arXiv HTML v3. Прочитано полезное отрицательное условие IoU/low FPS и сравнение при одинаковых detections.
- NVIDIA DeepStream 7.1 → archive redirect недоступен; dev-guide → текущая страница с меткой 9.2. Источник честно указан 9.2; не утверждаем знания 7.1 из позднего получения.
- AXIS manual → API → разделы capabilities и short-lived. Закрыта разница object age и time in area.
- monocular equipment proximity → IAARC 2017 original fulltext → §2 geometry assumptions / §5 limitation. Не ограничились abstract.

## Запросы по закупкам: положительного первичного протокола не получено

Запросы (русский):

- `видеоаналитика опасная зона техническое задание ложных срабатываний приемочные испытания`
- `"видеоаналитика" "ложных срабатываний" "техническое задание"`
- `"опасной зоны" "видеоаналитика" "закупка"`
- `site.zakupki.gov.ru "видеоаналитика" "ложных"`
- `"видеоаналитика" "приемочных испытаний" касок`
- `"контроль" "опасных зон" "видеоаналитика" "техническое задание"`
- `"закупка" "видеоаналитики" "95%"`
- `"видеоаналитика" "не более" "ложных тревог"`

Выдача давала маркетинговые страницы, общие охранные руководства, несвязанные закупки городского наблюдения/спорта/СКУД. Пример несоответствующей карточки 0128600006826000399 (Александров, городская система), 0173100013824000024 (СКУД Роскомнадзора): первичные вложения с требуемым приёмочным протоколом не получены и численные требования не извлекались. Наличие карточки в агрегаторе не доказывает состав её ТЗ. Запросы не дали пригодного результата, но это не доказательство отсутствия таких закупок.

Нужный остаток: конкретное ТЗ промышленного заказчика, где определены наблюдаемость, длительность отрицательной записи, denominator ложных тревог, правила сопоставления GT и дублей. Можно закрыть второй волной или запросом у постановщика. В текущем выборе метода не заменять это маркетинговой «точностью 95%».

## Запросы по методам и негативным условиям

- `Frigate zones inertia loitering_time bottom center speed estimation documentation`
- `NVIDIA DeepStream nvdsanalytics bottom center line crossing direction configuration`
- `AXIS Object Analytics time in area perspective excluded area trigger delay`
- `site.github.com/roboflow/supervision polygon_zone.py triggering_anchors bottom center`
- `ByteTrack ECCV 2022 arxiv low score detection association`
- `OC-SORT CVPR 2023 observation centric low frame rate`
- `multi object tracking low frame rate benchmark BoT-SORT ByteTrack arxiv`
- `site.mdpi.com construction equipment proximity homography monocular collision risk computer vision`
- `site.docs.itvgroup.ru "Время нахождения" "зоне"`
- `site.macroscop.com "время нахождения" "зоне"`
- `site.docs.itvgroup.ru "LongInZoneTimeout2"`
- `site.docs.itvgroup.ru "VMDA.oneAlarmPerTrack" "0" "1"`
- `site.dcase.community event based metrics collar onset 200ms`

В поиске обнаружена TU Wien thesis Costin Bernhart 2025 о снижении FPS до 5; не открыта целиком и не использована для численных рекомендаций. Иные свежие benchmark snippets также не используются как измерения. Предпочтено первичное отрицательное условие из OC-SORT с оригинальными detections/таблицей.

## Недоступность и ограниченное чтение

- CVF PDF OC-SORT: 403; компенсировано arXiv v3 HTML.
- Случайный arXiv html v4: 404; корректный v3 доступен.
- MDPI event metrics article 2016: 429; university mirror 403; взят первичный протокол DCASE только как пример temporal matching, не промышленный стандарт.
- ITV Confluence и PDF: периодические 502/timeout; PowerShell и Python urllib завершились TLS EOF. Прочитано оглавление/metadata, но не целевые параметры, поэтому S19 оставлен в недочитанных зацепках. Повторять бесконечно в первой волне нецелесообразно.
- IAARC screenshot страницы был запрошен, изображение не отобразилось в выводе tool; утверждений о визуальной проверке figure нет.

## Версии

Зафиксированы release/commit: Frigate v0.18.2 cfa08c56b23d23280c3d0a218e5a43182c97445b; supervision 0.31.1 f2adfadf2cf9050f44bcb0e71b4b160d8746eab1; ByteTrack d1bf0191adff59bc8fcfeaa0b33d3d1642552a99; BoT-SORT 251985436d6712aaf682aaaf5f71edb4987224bd. OC_SORT master metadata 8462e7e729a93ccd3bd995c0a79a890336cb3a0b (2026-04-21T23:31:31Z): прочитаны выборочные signatures/frame_count/max_age в trackers/ocsort_tracker/ocsort.py; детальное утверждение о variable-dt этой реализации не делается. OpenCV docs redirect 4.13.0. AXIS online docs/manual не pinned; наличие apiVersion example 1.2 не есть версия установленного приложения.
