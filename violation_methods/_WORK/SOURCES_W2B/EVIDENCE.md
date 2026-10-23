# W2_B — первичные доказательства и локаторы

Доступ 2026-10-23, примерно 06:15–06:26 Europe/Moscow (UTC+3); фактическое начало проверено clock: 03:15:47 UTC, завершение оформления03:25:45UTC. Даты публикации указаны отдельно. Это новая сетевая волна по K004–K006; запусков VMS, моделей и benchmark нет. Входы и критика прочитаны UTF-8. PDF skill применён только для чтения; PyMuPDF извлёк текст и отрисовал нужные страницы, Poppler в PATH отсутствует. Все дальнейшие трактовки — собственный пересказ. W1 и W2, читающие один Macroscop/Frigate, не независимые репликации.

## W2-B-S01 — Axxon Next VL: условия потока и освещения [primary manual]

Автор страницы Gleb Matskevich / AxxonSoft; updated 29.05.2023. Версия строго **Axxon Next 4.5.0–4.5.10**, не нынешняя линейка One. URL: https://docs.axxonsoft.com/confluence/spaces/next45en/pages/260906681/Video+stream+and+scene+requirements+for+PPE+detection+tool+VL+operation . Прочитан body items1–3, не только сниппет.

**W2-B-F01.** VL требует цвет; для typical tasks указан ≥13FPS. Раздел lighting не гарантирует стабильность при ночи/засветке, требует постоянства освещения. Текст пишет «200 lux per square meter»: единица в оригинале некорректна, здесь не исправляем её в новый норматив. Указаны ограничения перекрытий, отражений, вибрации, грязной оптики и fisheye. Это admission conditions конкретного модуля, не измерение деградации и не физическая невозможность любого IR-детектора. Новое относительно Macroscop: независимая продуктовая цепочка подтверждает, что generic camera night mode не является обещанием PPE night support.

## W2-B-S02 — Axxon Next VL: условия изображения объекта [primary manual]

Тот же автор, дата и версия. URL: https://docs.axxonsoft.com/confluence/spaces/next45en/pages/260906683/Objects+image+requirements+for+PPE+detection+tool+VL . Прочитаны items1–6 и таблица.

**W2-B-F02.** Требуются визуальная различимость СИЗ человеком, отсутствие шумов/артефактов сжатия/барьеров, видимость ≥8 кадров. Minimum **height of equipment on body area**: helmet/hood/gloves20px, vest50px. Это размер предмета, не человека; нельзя смешать с Bosch96px высоты человека. Таблица даёт59px/m и ~100px высоты объекта для перечисленных разрешений, но неоднозначное название последней колонки не превращаем в точное width×height. Порог не переносится на наш tensor. Смысл: документировать, где измерен размер, отдельно от source resolution.

## W2-B-S03 — Axis XFQ1656 manual [primary manual]

Автор Axis Communications; версия страницы **July2026**; URL https://help.axis.com/en-us/axis-xfq1656 . Прочитаны Adjust image: night mode, Reduce motion blur, Maximize details; Analytics and apps → PPE monitoring.

**W2-B-F03.** Night mode использует visible+nearIR и формирует monochrome image. Против blur manual предлагает более короткую выдержку/больший gain и при необходимости дополнительный свет; gain повышает шум. Для деталей — меньше compression, ценой bitrate/возможного FPS. PPE subsection предупреждает: малый объект может дать как miss, так и false alarm; нестандартная форма каски также даёт false alarm. Численного PPE night recall или универсального пиксельного порога нет. Из этого не следует, что thermal=NIR или что настройка экспозиции гарантирует восстановление PPE.

## W2-B-S04 — Bosch/Keenfinity settings [primary support/manual]

Автор Bosch Video Systems / текущий официальный support Keenfinity Group. URL https://knowledge.keenfinity-group.com/video-systems/article/how-to-optimize-camera-settings-for-video-analytic . Дата публикации не установлена; иллюстрация image2022-3-22 не принята за дату статьи. Прочитаны собственно article после длинной навигации, §1–5.

**W2-B-F04.** Exposure и temporal/spatial denoise могут снижать detail/contrast, создавать motion blur/ghosting; крайний low light может лишить детектор объекта. Важное ограничение переноса: рассматриваемая встроенная Bosch analytics получает изображение **до encoder**; её нечувствительность к compression не относится к нашему серверу, получающему декодированный RTSP. Thermal cameras описаны отдельно и не равны night grayscale. Это механизм/рекомендации производителя, не PPE-сравнительный эксперимент.

## W2-B-S05 — Frigate crop/resize developer report и pinned preprocessing [code + developer claim]

Автор ответа NickM-27, **25.06.2026**; https://github.com/blakeblackshear/frigate/discussions/23563 . Прочитан вопрос, accepted answer и replies. **W2-B-F05:** автор сообщает об увеличении FP при испробованном увеличении слишком маленьких regions; dataset, denominator и численная величина не раскрыты. Это ограничивающий опыт разработчика, не controlled benchmark и не PPE. Поэтому увеличение crop не обещаем как универсальное улучшение.

Pinned docs/code: commit `cfa08c56b23d23280c3d0a218e5a43182c97445b` (v0.18.2 по W1 provenance), автор Frigate contributors; дата commit15.10.2026 по W1 metadata. URL https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/docs/docs/frigate/camera_setup.md , строки19–25; code https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/util/object.py , `create_tensor_input`,288–305. Сохранены camera_setup.md, util_object.py. **W2-B-F06 [code inspection]:** region преобразуется в RGB/BGR/YUV, затем при несовпадении shape resize в model.width×height через INTER_LINEAR. Camera docs объясняют потерю деталей при уменьшении большого region. Это конкретная реализация crop→tensor, не проверка нашей модели.

## W2-B-S06 — конкретная промышленная закупка Oil India [official procurement]

Заказчик Oil India Limited, Duliajan, Ministry of Petroleum and Natural Gas. Номер **GEM/2026/B/7902194**, dated **11.08.2026**, услуга PPE and Unsafe Act Detection using Video Analytics. Официальная карточка https://www.oil-india.com/tender-details/124?in_detail=NzBleHVBPT0%3D . Открытая на дату доступа карточка показывает closing12.11.2026 и opening13.11.2026; ранний NIT содержит прежние даты08.09.2026, поэтому не использовать NIT как актуальный календарь.

Оригинальный NIT URL https://www.oil-india.com/download-tender-document?ten_detail=NzBleHVDSEw2RXFyMmdHdQ%3D%3D . Web отверг binary/octet-stream; PowerShell успешно получил8p PDF: [OIL_NIT.pdf](OIL_NIT.pdf), текст OIL_NIT.txt. Прочитаны p1,4–5; p4 hyperlink ведёт к **Scope of Work1786430899.pdf** на GeM: https://bidplus.gem.gov.in/resources/upload_nas/AugQ326/bidding/biddoc/bid-9738605/1786430899.pdf . Полный SoW **не получен**: web inaccessible; PowerShell transfer closed; curl35s timeout. Его clauses ниже читаются в официальных prebid-таблицах, а не объявляются прямым чтением полного SoW.

**W2-B-F07.** Это уже идентифицированная закупка промышленного клиента, не грант/маркетинг. Но наличие NIT и спецификации не подтверждает award, внедрение, accepted performance либо действующий SLA.

## W2-B-S07 — Oil India pre-bid minutes: самая полезная часть цепочки [official clarification]

Автор Oil India Limited. Заголовок **Minutes of Pre-Bid Meeting dated25.08.2026 (GEM/2026/B/7902194)**; опубликовано в официальной карточке **01.10.2026**. URL https://www.oil-india.com/download-tender-document?detail=NzBleHVDck00a3lnMlFxc2tzdVlrTUI0cC92Vg%3D%3D . Получен97p PDF:94 нумерованные содержательные страницы+3 добавочные без извлечённого текста. [OIL_PREBID.pdf](OIL_PREBID.pdf), извлечённый OIL_PREBID.txt. Визуально проверены p12,24,36,79,80,81,82,83; PNG сохранены.

**W2-B-F08.** p12 row13, p24 rows6–7: quoted SoW7.13 требует90% ideal/80% challenging; ответ заказчика относит оценку к каждому use case и переносит методику в Design с OIL approval. Denominator, FP/FN и temporal matching этим ответом не заданы. p36 row55: SAT/signoff предусмотрены, criteria решат до UAT/SAT. p19 фиксирует вопрос о конфликтующих95% и90/80%; ответ не даёт новой формулы. Это документированная **незавершённая спецификация приёмки**, не95% achieved.

**W2-B-F09.** p79 row10: участник оспаривает80% вне IR-range; OIL отвечает internal review, а не принимает физическую гарантию. p79–80 row11: small PPE на legacy wide views → joint survey/remediation report; upgrades у OIL. p82 row18: zone analytics только fixed park/approved stable PTZ presets. p83 row22: steam/dust/exhaust/flares оценивать camera-wise с exclusions/calibration; чисел PPE dust recall нет. Утверждение bidder и обязательный ответ OIL различены.

## W2-B-S08 — pinned Frigate caller/lifecycle [code inspection, без исполнения]

Единственная версия во всём разборе `cfa08c56b23d23280c3d0a218e5a43182c97445b`. GitHub API rate-limit, затем codeload ZIP успешно скачан; никаких инструкций из репозитория не исполняли. `rg` всего каталога frigate по zone_presence/zone_loitering нашёл записи только в tracked_object.py; сохранён COUNTER_WRITES.txt. Локальные оригиналы имеют настоящую нумерацию с пустыми строками; web text иногда удаляет пустые строки, его номера не использовать как Python line numbers.

Paths/URLs и прочитанные места:

- https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/track/tracked_object.py : init65–68, update130–140, zone186–305, state385–386; local tracked_object.py.
- https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/camera/state.py : finished307–308; reset310–347; update349–425, removed494–500; local camera_state.py.
- https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/track/object_processing.py : queue773–799; cleanup819–830; local object_processing.py.
- https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/track/norfair_tracker.py : register273–292; deregister312–316; update459–491; synthetic stationary493–507; match509–648; local norfair_tracker.py.
- https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/video/detect.py : tracker106; process_frames176+, resolution reset245–260, missing frame287–292, stationary/detection300–434, build438+, queue534–550; local video_detect.py.
- https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/docs/docs/configuration/zones.md : Zone Inertia223–232; local zones.md. Same-commit docs требуют consecutive, поэтому W1 unpinned-doc оговорка здесь устранена для этого утверждения. zone_config.py46 также consecutive.

**W2-B-F10–F13.** Подробная собственная ручная трасса и все scope-оговорки в [W2_B.md](../W2_B.md), K006. Это не runtimebug, не tested defect, не характеристика иных релизов. Lifecycle статически исследован; очередь/активность Norfair и actual event impact ещё проверяются replay E-B04.

## W2-B-S09 — Axis Object Analytics generic considerations [primary manual]

Автор Axis Communications, **September2026** на странице; https://help.axis.com/en-us/axis-object-analytics . Прочитаны Considerations и Classification. **W2-B-F14:** взгляд строго сверху затрудняет classification; частичная видимость, fog/noise/плохой контраст ограничивают generic human/vehicle analytics. Это не численная оценка topview PPE. Не распространять4%/8% human heights на сигарету или респиратор.

## W2-B-S10 — Axxon One collection requirements [primary manual/vendor claim]

Автор Alina Luchkina,09.04.2025, One3.0/3.1; https://docs.axxonsoft.com/confluence/spaces/ONE2025/pages/314536470/Data+collection+requirements+for+neural+network+training . Прочитана общая таблица и PPE subsection. **W2-B-F15:** требует actual camera/resolution/conditions; для PPE отдельно сказано artificial constant lighting. Рекламные общие90–97% и5–7% не извлекаются как PPE achieved: denominator не определён. Общий custom-training claim night/IR на отраслевой странице не отменяет более узкую спецификацию PPE.
