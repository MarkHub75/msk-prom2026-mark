# Исходная критика первой волны datasets

Критик со свежим контекстом: gpt-6.1-sol, reasoning_effort=high; история оркестратора не передавалась. Прочитаны полностью `Context-prompt.md`, `prompt-datasets.md`, `_WORK/PLAN.md`, `_WORK/AGENT_PROMPTS.md`, `_WORK/DOWNSTREAM_PROMPTS.md` и все 15 W1-XX. Срез первой волны — [_WORK/W1_BUNDLE_MANIFEST.json](_WORK/W1_BUNDLE_MANIFEST.json). Фактическое время фиксации критики: 23.10.2026, 06:29:41 Europe/Moscow / 03:29:41 UTC; сеть не использовалась. Дополнительно читались сохранённые README, статьи, metadata и списки файлов. Нового dataset audit, обучения и финального аудита отчётов здесь нет.

Это исходная история K-ID. Все замечания при создании имеют статус **передано во вторую волну, результат ещё неизвестен**. Сборщик после W2 должен дополнить их результатами, сохранив этот текст. P0 — может изменить ближайший выбор основного источника или допустимость объединения; P1 — меняет конкретную вспомогательную роль/проверку; P2 — дополнительная ветка, которую можно явно отложить при отсутствии соответствующего сценария.

## Оценка покрытия и уже достаточные результаты

Первая волна содержательно касается всех пятнадцати вопросов тематического промпта. Это не формальный каталог ссылок: реально получены raw SH17 XML, SFCHD COCO/YOLO labels, полные SHEL5K file metadata, Smoker RAR, SARD ZIP directories и один dense label, MOT labels. Сохранены существенные расхождения и границы проверок. Уязвимость — несколько сильных рекомендаций всё ещё опираются на статьи/карточки именно в тех местах, где небольшой первичный artifact или визуальный пример способен поменять решение. Особенно недозакрыты вопросы 2/5/7/8/9/12/13: получить ли набор без восстановления цепочки, что именно означает label, достаточно ли supervision и можно ли сохранить независимый test.

Следующее уже достаточно установлено для текущего решения; повторять общий поиск не нужно:

| Установленный результат | Основания W1 | Граница установленного |
|---|---|---|
| SH17 — Pexels/web industrial photographs, а не исходный CCTV; flat17 теряет on/off и safety/vision; `head` не no_helmet | W1-02-F04/F05/F07, W1-11-F01–04, W1-12-F03–05 | Значение конкретного off и соответствие released labels ещё требуют K001/K002 |
| Raw SH17 8102 XML/76008 objects — отдельный artifact; released8099/75994 — заявления другого состава; filename train/val audit уже выполнен | W1-02-F03/F06, W1-11-F03/F06, W1-14-F01–04 | Это не pixel duplicate audit и не semantic validation |
| CHV явно использует SHWD/GDUT-HWD; SHEL5K явно переаннотирует SHD5000; SHD и SHWD нельзя отождествлять по имени | W1-03-F05/F09, W1-09-F01–04 | Для отказа от предположения независимости parent/child не нужен полный повторный hash-поиск; точные совпадения нужны лишь для конкретной смеси |
| SHEL5K разделяет helmet/head/person геометрию: это показано XML, а не только названиями | W1-03-F10/F11, W1-12-F01 | Три пары не устанавливают полный protocol и полноту |
| SFCHD — surveillance двух chemical plants, около 40 scenes, последовательная выборка; точные current COCO counts, missing TXT и нетипичный test уже измерены | W1-03-F14–18, W1-15-F05–07 | Не нужно повторять простой count как независимое подтверждение; нужен K003/K004 |
| `blur_head`/`blur_clothes` нельзя превращать в отсутствие защиты | W1-03-F17, W1-11-F11, W1-12 map | Видимость, boundary и геометрию этих классов на реальных images ещё проверять |
| CPPE Mask неоднороден, filter halfmask действительно присутствует внутри Mask; отдельного industrial respirator state GT не установлено | W1-04-F01–07, W1-11-F07–09 | Не повторять тезис «респираторов нет»; исходные лицензии/состав всё ещё K008 |
| Smoker v1 реально получен, SHA совпал, 1120 JPG/716+180+224, image classification; hard-confuser queries документированы | W1-06-F01–05, W1-15-F08 | Не доказаны decode всех JPG, качество/независимость и cigarette/event GT |
| Önal691 curated clips не равны 4000h опубликованного потока; clip class не даёт onset/polygons/tracks | W1-07-F01–04 | Получение media и границы доступного временного материала ещё K010 |
| SARD первый/второй IDs нельзя объявить frame/track IDs; PhysicalAI parent/chunk/external pointers нельзя суммировать | W1-07-F05–08, W1-09-F08/F09, W1-15-F09 | Требуется документация или ограниченная проверка, а не уверенное переименование |
| Generic person/pose/tracking не даёт PPE negatives; CrowdHuman `tag=mask` — ignore/person-like region; MOT detector variants повторяют базовые sequences | W1-08-F02–11, W1-14-F05–07 | Достаточно для выбора вспомогательной роли; сейчас не нужен полный COCO/CrowdHuman audit |
| Лицензии статьи/кода/сборки/исходного media различаются; NC и unknown сохранены без обещаний коммерческой применимости | W1-10-F01–13 | Не нужно доказывать юридическую чистоту каждого фото. Нужны конкретные отсутствующие notices/metadata выбранных artifacts |
| Расчёт resize и ограничение crops не являются измерением модели; target-camera transfer/false alerts/h не установлены | W1-13-F07/F08, W1-07-E02, W1-06-E02 | До target data это точные условия, а не задача «доказать перенос» открытым поиском |

Особенно полезны найденные контрпримеры: потеря SH17 state в conversion, разные boxes SHEL5K, неоднородный CPPE Mask и SFCHD missing TXT. Вторая волна должна продолжить такую проверку рекомендаций, включая возможность понизить кандидата, а не только добавить карточки.

## K001 — SH17: основной release не связан с реально прочитанными labels

- **Priority:** P0.
- **Problem:** устойчивое позиционирование SH17 как первого multi-PPE donor пока основано на YAML/статье и отдельно raw attachment. Не получен ни один released YOLO label; полный Kaggle file listing не закончен. `kaggle_files_all.json` тоже содержит только 200 entries и непустой pagination token. Raw8102 нельзя молча подставить вместо release8099.
- **Material:** W1-02-F01–07/E01, W1-11-F02–06, W1-14-F04; `_WORK/MATERIALS/W1-02/kaggle_files_all.json`, `sh17.yaml`, `kaggle_*_files.txt`; `_WORK/MATERIALS/W1-11/SH17-raw.zip`.
- **Impact:** меняет воспроизводимость acquisition, loader map, достоверность class counts и стоимость подготовки. Если release не получить или conversion другой, SH17 остаётся условным донором либо отдельной raw-derivative задачей.
- **Missing evidence:** полный file manifest или точный ограниченный путь к released labels; несколько labels с paired images; реально наблюдаемый ID/format; сравнение released↔raw для одинаковых basenames. Причины table counts не требуется угадывать.
- **W2 task:** **W2-01, Medium.** Продолжить официальную Kaggle pagination/авторский путь до labels, не скачивая 14GB images. Сохранить exact version, status, bytes/hash; получить стратифицированные released samples с helmet/glasses/gloves/rare PPE и проверить against YAML. Сопоставить source names и несколько boxes с raw, явно описать правила и расхождения. Если небольшой label доступ отдельно невозможен, сохранить конкретный endpoint/ответ и минимальный следующий download, а не объявлять весь dataset закрытым. Выход: `W2-01.md`, manifest/diff в собственной MATERIALS. Не повторять известный raw structural count как новую проверку final release.

## K002 — SH17: наличие raw on/off ещё не устанавливает wearing supervision

- **Priority:** P0.
- **Problem:** raw tags выглядят ценным выходом из потери состояния, но semantic image audit SH17 не выполнен вообще. Слово off может относиться к лежащему предмету, носителю, части тела или авторскому соглашению; не заданы person relations, correct fit и исчерпывающие negatives. Переход к raw-state exploration разумен только как гипотеза.
- **Material:** W1-02-F07/E02, W1-05-F04, W1-11-F02/F04/F05/E01, W1-12-F04/F05; author Issue4 conversion и raw XML.
- **Impact:** может полностью изменить маршрут от «брать raw для wearing» к «object donor плюс ручная доразметка». Влияет на violation_methods и partial-label обучение сильнее, чем ещё одна таблица количества предметов.
- **Missing evidence:** визуально подтверждённые примеры конкретных on/off и safety/vision tags на совпадающих image IDs; наличие нескольких людей/неоднозначной связи; наблюдаемые пропуски видимых объектов; границы авторской инструкции.
- **W2 task:** **W2-02, Medium.** По уже полученным raw XML и CSV получить небольшой содержательно выбранный paired sample: helmet on/off, gloves off/on, safety/vision glasses, masks, несколько многолюдных/малых/перекрытых случаев. Число и причины отбора записать; сохранять ID, raw literal, bbox, source image hash, overlay и решения present/absent/not-annotated/ambiguous. Проверить только наблюдаемые случаи, не объявлять статистику ошибок всей коллекции. Искать точный author protocol по off; при отсутствии разделить visual observation и interpretation. Не присваивать person association только по пересечению boxes без оговорки. Сформулировать пригодный маршрут либо отказ от state merge.

## K003 — SFCHD: между COCO и YOLO не выбран проверенный исходник

- **Priority:** P0.
- **Problem:** missing TXT — реальный симптом, но его устранение ещё не делает YOLO эквивалентным COCO. Не проверены все ID, count/box equivalence, размеры, пустые labels и membership COCO val относительно text lists. Paper train9898 против TXT9897 — конкретное различие состава. Tiny `test.txt` не следует превращать в третий benchmark.
- **Material:** W1-03-F15–18, W1-12-F02/E01, W1-15-F05–07; pinned `all_data.json`, `val.json`, `labels.zip`, `new_split_yolo/*.txt`.
- **Impact:** определяет, можно ли быстро получить однозначный loader, какой artifact считать исходным и какой split воспроизводить. Может выявить более широкое расхождение, чем одна отсутствующая запись.
- **Missing evidence:** image-ID/basename join, поклассовый counts/box comparison с нормализацией, text-list membership, роль 6 test paths, источник 7 annotations отсутствующего TXT.
- **W2 task:** **W2-03, Medium.** На уже сохранённых artifacts провести полный annotation-only consistency audit: set/category/range/geometry/empty records, per-image/per-class COCO↔YOLO сравнение с явно заданной rounding tolerance; COCO val↔TXT val;6 test paths↔train/val/all. Сохранить machine-readable mismatches, hashes и проверяемую candidate conversion для missing image, не перезаписывая originals. Предложить один воспроизводимый маршрут COCO-native или regenerated YOLO с сохранением original split. Он остаётся annotation проверкой до image pairing/decode. Нет нужды заново скачивать annotations или притворяться, что images уже получены.

## K004 — SFCHD: ближайший заводской источник ещё не даёт независимый holdout

- **Priority:** P0.
- **Problem:** factory domain обоснован, но camera-like prefixes, source runs, scenes и lighting groups не сопоставлены с splits. W1 осторожно сохраняет неизвестное, однако рекомендация «отдельный camera holdout после groups» пока не превращена в реальную возможность. Статья прямо сообщает de-identification времени/локации; требование получить полные timestamps может оказаться недостижимым.
- **Material:** W1-03-F14/F17, W1-09-F06/F07, W1-13-F04, W1-14-F09/E04; saved paper §3.1 (`Data Privacy`), README/tree, COCO filenames.
- **Impact:** меняет роль SFCHD adapt/development versus independent evaluation и объём собственной целевой разметки. Random split при общих камерах не доказывает leakage соседних кадров, но и не защищает от неё.
- **Missing evidence:** документированная filename/group convention либо наблюдаемая proxy grouping с проверкой images; число и пересечение таких групп; actual semantic/geometry examples head/self_clothes/blur classes; source media notices и наличие самих images.
- **W2 task:** **W2-04, Medium.** Пройти авторский image route до archive listing/малого paired sample; получить примеры нескольких filename families, normal/high/low light и всех 7 classes. На доступных metadata построить таблицу prefix/run↔split и source evidence; проверить несколько визуальных групп, пометить inferred отдельно от supplied. Искать `directory.md`, scene/light lists и author collection convention; учитывать de-identification и не выдумывать camera IDs. Подтвердить на overlays geometry и наблюдаемую семантику head/self_clothes/blur. Сохранить вывод: какой grouped holdout реально можно создать, а какое знание остаётся отсутствующим. Общую независимость всего набора по нескольким фото не объявлять. Условия данных передать W2-12.

## K005 — SHWD: критическое переименование person всё ещё не подтверждено XML/image парой

- **Priority:** P0.
- **Problem:** README достаточно доказывает normal-head смысл, но box extent `hat`/`person`, архивный split и filename/map ещё не прочитаны. Это точечная проверка сильного кандидата, не повод заново искать обзор helmet datasets. Демонстрационная картинка/loader не заменяют annotations.
- **Material:** W1-03-F01–04, W1-12 map/S01, W1-15-F01; pinned README и `shwd-train.py`; Drive `VOC2028.zip`.
- **Impact:** предотвращает full-person/head смешение, меняет возможный merge с SHEL5K и тип no_helmet supervision; устанавливает реальную цену acquisition.
- **Missing evidence:** несколько actual VOC XML+images, archive tree/splits, literal labels и box extent для helmeted/bare/crowded/occluded heads; notices из archive, если существуют.
- **W2 task:** **W2-05, Medium.** Проследить author Drive/Baidu route до реального payload или адресной manifest/sample возможности; получить 20–50 содержательно выбранных pairs, либо меньший обоснованный sample при ограничения доступа. Проверить normal head, helmet object/head extent, carried helmet/ordinary hat, если такие примеры реально найдены, VOC coordinate convention и split files. Сохранить observations/overlays/exact access failure. Нельзя заключать отсутствие carried-helmet cases, если они не встретились; права SCUT research-only уже установлены и не требуют нового общего поиска.

## K006 — CHV: paper map есть, archive map и полезность переаннотации не проверены

- **Priority:** P0.
- **Problem:** числовой порядок 0–5 взят из первичной статьи и правдоподобен, но конкретный downloadable artifact ещё не проверен. CHV может быть полезным vest/color donor, однако не установлены фактический формат/полнота labels и цена восстановления исходников. Доказанное происхождение SHWD/GDUT-HWD уже запрещает считать его автоматически independent test.
- **Material:** W1-03-F05–08, W1-09-F02, W1-12 CHV rows, W1-15-F02; `CHV_dataset.zip`, pinned author repo, article §2.3/Fig.5–6.
- **Impact:** решает, стоит ли добавлять CHV ради новых labels или достаточно другого donor. Может изменить mapping и риск ложных negatives при совместном обучении.
- **Missing evidence:** archive config/labels/pairs/split manifests/notices; конкретное соответствие paper↔artifact; видимые person/vest/colored helmet examples и непокрытые/неоднозначные головы.
- **W2 task:** **W2-06, Medium.** Получить author archive listing/малую выборку, прочитать class map, сохранить несколько paired images/labels по всем 6 classes и проверить box units. Сопоставить official split sizes/files статье. По доступным basenames/metadata и небольшой найденной parent sample подтвердить конкретные parent links, если это возможно; полный hash-audit всех SHWD/CHV сейчас не обязателен. Не выводить independence из отсутствия matched samples. Отдельно сохранить изменение annotations/added classes и наблюдаемую partial completeness; условия archive передать W2-12.

## K007 — SHEL5K: доступный небольшой слой annotations оставлен без полной проверки

- **Priority:** P1, повышается до P0 при выборе head/person-state обучения.
- **Problem:** уже есть полный 5000XML manifest и воспроизводимый API; весь annotation слой по metadata всего 19,154,616bytes. При этом сохраняется 75,570/75,578 конфликт, class support неизвестен, а semantic выводы основаны на 3 pairs. Это дешёвый по данным шанс уточнить кандидата с явной геометрией.
- **Material:** W1-03-F09–13, W1-12-F01, W1-15-F03/F04; Mendeley v1 manifests/XML+PNG, paper §3/Fig.3, NC3.0 уже установлен.
- **Impact:** меняет доступные head/person-state классы, rare-state поддержку, стоимость relabel и возможность использовать SHEL5K вместо рискованной строки SHWD person. Parent SHD не становится independent test.
- **Missing evidence:** полный actual XML count/class distribution/geometry flags и source filename consistency; wider sample ambiguous/occluded/crowded head/person cases; точные official split instructions либо явная их ненайденность.
- **W2 task:** **W2-07, Medium.** При доступном API получить только 5000XML, сверить metadata hashes где даны, parse/count/IDs/text names/empty/bbox ranges и объяснить только наблюдаемую часть расхождения 75,570/75,578. Расширить paired visual sample целевыми head/person_no_helmet/person_with_helmet/occluded/ordinary-hat candidates, сохранить coverage. Проверить источник official split, не создавать авторские manifests по догадке. Уважать NC scope; это проверка структуры/семантики, не обещание допустимости commercial use. При недоступности bulkXML достаточно exact failure и готовой процедуры, не выдумывать counts.

## K008 — CPPE: оригинальный manifest важнее повторного доказательства medical domain

- **Priority:** P0 для респиратора; P1 для broad Goggles/Face_Shield donor.
- **Problem:** HF29rows/2images доказывают heterogeneous Mask, но не восстанавливают original source/license inventory, origin IDs и спорный 100test protocol. Респираторный gap сформулирован верно, однако второй волне ещё есть что проверить до перехода к неизбежной целевой разметке.
- **Material:** W1-04-F01–07/E01/Q02/Q03, W1-11-F07–09, W1-10-F06; original README даёт versioned GitHub release `v0.1.0/dataset.tar.gz` наряду с Drive и MD5, а HF — отдельную representation.
- **Impact:** позволяет отобрать лицензированные/прослеживаемые source images и оценить, есть ли практический respirator subtype donor. Может сократить или увеличить ручную разметку; не закрывает removed/correct GT автоматически.
- **Missing evidence:** original tar tree/metadata files, per-image source/license availability, exact category/split records и связь с HF; несколько дополнительных mask types с known origin/scale.
- **W2 task:** **W2-08, Medium.** Пройти versioned release route, сначала listing/metadata либо bounded tar retrieval (~230MB по README, это author size). Найти source URL/author/license/MD5 inventory или доказательно локализовать отсутствующее звено. Сопоставить original split/category IDs с HF revision `66f6a5efd474e35bd7cb94bf15dea27d4c6ad3f8` и 100test утверждением статьи, не дорисовывая 1129. На стратифицированном mask sample вручную фиксировать visual subtype/visibility/worn/carrying/unknown, не certification. Результат — какие конкретные images пригодны как conditional donor и что требуется доразметить; считать доли всей CPPE по выборке нельзя.

## K009 — smoking: реальная surveillance detection ветка осталась на поисковом extract

- **Priority:** P0.
- **Problem:** classification donor разобран хорошо, но ветка cigarette/person-action localization фактически остановилась на 429 одного MDPI открытия. HMDB кино и synthetic PhysicalAI не заменяют попытку получить primary surveillance-smoking annotations. Это может существенно изменить оценку одного из четырёх исходных сценариев.
- **Material:** W1-06-S05/F01–10/E01, W1-15-F08; DOI10.3390/electronics12153225 §3.1 указан, но первоисточник не получен. RAR уже локально доступен.
- **Impact:** может дать нужный cigarette/hand/phone/person localization donor либо подтвердить необходимость собственной разметки. Меняет архитектуру данных и hard-negative программу, а не только число источников.
- **Missing evidence:** полный primary paper/data availability для smoking/calling surveillance, exact author repository/archive, label unit/IDs, source/domain/splits/terms и actual sample; для Smoker — реальные decode/confuser/duplicate observations вместо одних запросов сбора.
- **W2 task:** **W2-09, Medium.** Восстановить DOI через OA PDF/авторский repository/издательский asset, проследить data link до artifact или конкретного запроса авторам (самим не писать). Искать ограничивающие условия: public media ли, cigarette bbox или person behavior bbox, реальные intervals или static frames, subject/video split. При полезном artifact получить небольшой sample и точные классы; рядом декодировать локальный Smoker RAR, проверить хотя бы все file headers/dimensions и выбрать реальные phone/drink/inhaler/hands-to-face examples из обоих классов, сохраняя ручные tags отдельно от source labels. Не заявлять, что confusers все присутствуют по query list. Если новое visual GT не найдено, сохранить точный маршрут и gap; «не найдено» не становится «не существует».

## K010 — Önal: главный реальный video кандидат ещё не получен даже как manifest/sample

- **Priority:** P0.
- **Problem:** рекомендация replay/event donor пока полностью документальная. В статье допускается несколько behaviors в клипе; фактический annotation payload, camera identification, frames до/после события и непрерывные safe periods не прочитаны. На фоне успешного Mendeley API других наборов это адресная незакрытая проверка.
- **Material:** W1-07-F01–04/E01/E02/Q01, W1-13-F05; `safe_unsafe_metadata.json`, article110791, Mendeley xjmtb22pff/1.
- **Impact:** решает, доступен ли пригодный replay сейчас и можно ли получить даже ограниченный zone-event validation без новой съёмки. Нельзя обещать false alerts/h по 691 curated clips.
- **Missing evidence:** exact files/folders/bytes/checksums/notices; actual labels; sample safe/unsafe clips with duration/FPS/timebase and camera views; наличие либо отсутствие опубликованного continuous material.
- **W2 task:** **W2-10, Medium.** Использовать установленный Mendeley folder/file API pattern с правильным version, сохранить полный metadata manifest. Получить несколько safe/unsafe walkway clips, включая разные documented cameras при наблюдаемом различии. Измерить media metadata, проверить class/filename convention/multi-label file, temporal lead-in и видимую границу walkway. Проверить published raw/continuous linkage; не требовать 4000h download. Разметить максимум демонстрационный небольшой event example с чёткой маркировкой proposed/manual, если контекста хватает; не превращать его в author GT. Если camera ID inferred, хранить основание. Итог должен сказать, какие E-inputs реально получить и чего clips принципиально не подтверждают.

## K011 — SARD: одна плотная annotation не заменяет schema/tracks/source protocol

- **Priority:** P1; P0 если рассматривается как главный temporal donor.
- **Problem:** substantial new source найден, но пока неизвестны даже точный смысл двух числовых полей и continuity identity. Сохранять file parser как предложение корректно, однако без следующего шага SARD останется дорогой необъяснимой видео-зацепкой.
- **Material:** W1-07-F05–08/E03/Q02/Q03, W1-13-F06; Zenodo19926448 revision4, `SARD_4.txt`, два ZIP directories.
- **Impact:** меняет возможность использовать tracking/HOI/actions и стоимость загрузки 35GB supplementary. Может обнаружиться annotation-object ID вместо track ID или иная frame indexing.
- **Missing evidence:** author paper/supplement/schema/class definitions/split/source manifest; actual media4 dimensions/FPS and frame overlays, temporal identity validation; upstream scope.
- **W2 task:** **W2-11, Medium.** Проследить Zenodo related identifiers/author publication до schema; получить небольшой linked video или пригодный ограниченный member, сверить frame index/coordinate convention и persistence IDs на нескольких удалённых и соседних моментах. Не извлекать 35GB ради одного sample, если другой путь доступен. Найти promised split/HOI definitions и source-video mapping; при отсутствии сохранить explicit unknown и safe parser, который не переименовывает IDs в tracks. Отличать source CC BY от upstream rights. Итог — конкретная роль либо обоснованное понижение приоритета, а не повторение card counts.

## K012 — права: нужны точные оставшиеся notices выбранных artifacts, а не всеобщая юридическая гарантия

- **Priority:** P0 для SFCHD/SH17, P1 для остальных выбранных donors.
- **Problem:** W1 правильно разделяет слои, но acquisition order «уточнить условия → всё остальное» может стать неопределённой остановкой, если не назвать конкретные доступные документы и fallback. Самая близкая CCTV ветка SFCHD остаётся license unknown; SH17 README/Kaggle NC-SA против Zenodo NC и paper commercial wording. У archive images/labels могут быть notices, ещё не прочитанные W1.
- **Material:** W1-10-F01–12/E01/E02/Q01–04, W1-15 acquisition order; W1-04-F07, W1-07-F04. Pexels legal text прочитан web агентом W1, но сохранённые shell HTML —403 challenge, не legal snapshot.
- **Impact:** определяет допустимые роли local research/train, public demo/raw/crops/labels redistribution и последующее deployment. Unknown не должен автоматически означать запрет всех действий, но и не разрешение. Нельзя одним commercial_ok стереть расхождения.
- **Missing evidence:** явный author artifact notice SFCHD; точная применимая версия SH17 conditions; внутренние notices получаемых CHV/SHWD/Önal/Pictor artifacts; original CPPE source inventory (K008). Для текущего исследования не требуется установить права каждого photographer/лица.
- **W2 task:** **W2-12, Medium.** Выполнить bounded поиск конкретных author/release/archive notices и dataset terms для SFCHD и SH17, затем принять notices от W2-04/05/06/08/10/14. Зафиксировать цитируемый locator, version/date/access, scope code/labels/images/assembly/article, explicit permitted/restricted actions и remaining link. Для Pexels при необходимости повторно получить легальный текст законным доступным способом, не выдавая 403 за содержимое. Не делать общих юридических выводов о SA на weights или NC на призовой хакатон: подготовить точный вопрос правообладателю/постановщику и условные маршруты. Внешних сообщений не отправлять. Результат — action matrix и минимальные blockers, а не требование недостижимого полного clearance.

## K013 — размер: доступны реальные annotations, но пока даны почти только расчётные примеры

- **Priority:** P1; P0 если выбор сводится к full-frame против crops.
- **Problem:** W1 верно не обещает CCTV перенос, но не использует уже полученные SFCHD COCO/raw SH17/CPPE29 для per-class size distributions. Дополнительно W1-13-F04 неточно называет SFCHD small threshold0.12%: saved current paper §3.3 сначала цитирует SPIE0.12%, затем **собственный** small<0.1%, large>0.2%. README size totals нельзя подписать неверным порогом.
- **Material:** W1-13-F01/F04/F06–08/E01/E02; saved `sfchd-scale.txt` §3.3, lines around877–884; raw SH17 XML, all_data.json, HF29rows. W1-09 также замечает подозрительные comparison tables, но не нужно использовать их вместо original protocols.
- **Impact:** меняет приоритет per-class donors и ожидаемую потребность crop/detector stages; исправляет сравнение «small» между наборами. Не устанавливает минимальный рабочий пиксельный порог модели.
- **Missing evidence:** измеренные native and hypothetical640 per-class width/height/area/min-axis distributions с image dimensions и exact transform; различие raw/release и sample/full scopes; проверенный literal порог source table.
- **W2 task:** **W2-13, Medium.** По уже сохранённым annotations посчитать понятные per-class quantiles/histograms native и после явно условного letterbox640; не называть 640 установленным LinQ input. Для SFCHD разнести helmet/head/blur, для SH17 — raw classes/on-off и исключения состава, для CPPE — только 29test scope. Сверить threshold0.1/0.12 и при возможности восстановить source size table по обоим порогам, сохранив несовпадение. Визуальные sample dimensions от W2-02/04/08 использовать для проверки declared sizes. Подготовить воспроизводимый scale audit artifact; не выдавать это за accuracy/optical resolvability или target transfer.

## K014 — альтернативные PPE donors: хотя бы один практический fallback должен дойти до labels

- **Priority:** P1 для vest/gloves/boots, P2 для расширения вне опубликованных примеров кейса.
- **Problem:** Pictor известен по трем approaches, Construction-PPE содержит явные no_* строки, но ни один actual annotation sample не получен. Pictor README обещает доступ именно crowd-sourced части: полные 1472 нельзя считать реально выдаваемым пакетом. Construction-PPE none/no_* geometry неизвестна. Сейчас оба могут оказаться дорогими и избыточными альтернативами, а не готовыми fallback.
- **Material:** W1-01-F05/F06/Q04, W1-05-F01–06/E01/E02, W1-11-F10, W1-14-F10; saved Pictor README §§Download the crowd-sourced dataset/Methods, Construction YAML/release link.
- **Impact:** меняет выбор donor при отложенном SH17/CHV и показывает, существует ли явное absence supervision с нужной геометрией. Не должно расширять обязательный scope на harness/boots по одному названию.
- **Missing evidence:** Pictor available subset/split/real map/box units и notices; Construction-PPE all none/no_* actual units, source/version/labels completeness и paired confusers.
- **W2 task:** **W2-14, Medium.** Проследить Pictor Drive subfolders до небольших labels/images и выяснить, какие approaches/774crowd/698web реально выдаются. Для Construction-PPE pinned release получить directory/class config и stratified no_helmet/no_gloves/no_boots/no_goggle/none/Person pairs, сохраняя mixed geometry и unobservable cases. Не считать наличие no_* гарантией exhaustive labels. Получить точный provenance/terms statement или локализовать пробел. Если оба не проходят минимальный artifact/semantic gate, честно понизить их и оставить конкретную альтернативу/вопрос. SODA403 имеет более низкий приоритет, если construction-specific scope не нужен; не тратить эту ячейку на полный повтор SODA обзора.

## K015 — synthetic PhysicalAI: bounded проверка нужна до включения в план событий

- **Priority:** P1 при намерении использовать; P2 при явном откладывании synthetic.
- **Problem:** найдена rich event schema, но full license не прочитан, smoke/vap substring не равен family subset, а приведённые 282chunks и 187parents относятся к разным единицам. Без deterministic join и условий техническое богатство может создать ложную практическую рекомендацию.
- **Material:** W1-06-F07–09/E03, W1-09-F08/F09, W1-15-F09; pinned PhysicalAI card, provenance, labels, category mapping, media manifest.
- **Impact:** определяет полезность synthetic event-plumbing/augment donor и отсутствие реального camera-hour holdout. Может исключить external-pointer records и существенно уменьшить доступный smoking/PPE subset.
- **Missing evidence:** прочитанные specific license/additional generation conditions; deterministic family↔parent↔chunk↔redistributable media join; несколько actual temporal records с доступным payload path, subtype и confusers.
- **W2 task:** **W2-15, Medium.** По сохранённым JSON/CSV построить точный smoking-family subset, отдельно parents/chunks/packaged/external/unlabeled, проверить temporal bounds/FPS fields и dedup keys. Прочитать linked NVIDIA Dataset License/Google conditions для выбранного artifact, сохранить локаторы без широкого commercial вывода. Один-два media samples получать только если это необходимо для решения и доступно ограниченно; иначе подготовить exact retrieval. Отметить free-text/model-generated uncertainty и scenario group. Если источник остаётся лишь дополнительной гипотезой, явно отложить его, не приравнивая к реальным industrial data.

## Рекомендуемое распределение второй волны

Это пятнадцать разных проверок, а не пятнадцать повторных обзоров. При трёх доступных Medium исполнителях удобно распределить последовательные ячейки так, чтобы каждый владел собственной папкой и результатом; связанные артефакты передавать другим как ссылки, не перезаписывать общие файлы:

| Группа | Индивидуальные результаты | Что должно измениться |
|---|---|---|
| A — SH17, права и реальный scale | W2-01(K001), W2-02(K002), W2-08(K008), W2-12(K012), W2-13(K013) | Из условной flat/raw рекомендации получить конкретный состав/semantic gate, source-license inventory и измеренные масштабы |
| B — каски и воспроизводимый CCTV artifact | W2-03(K003), W2-04(K004), W2-05(K005), W2-06(K006), W2-07(K007) | Выбрать исходный SFCHD format/split, установить head/person geometry и практическую цену helmet-family acquisition |
| C — события, smoking и ограниченные fallback | W2-09(K009), W2-10(K010), W2-11(K011), W2-14(K014), W2-15(K015) | Найти или адресно ограничить visual/event GT; проверить реальное видео, schema и donor fallback вместо накопления карточек |

Внутри групп порядок выбирать по зависимостям: SFCHD consistency можно делать сразу локально; W2-12 получает notices по мере находок соседей; W2-13 сначала использует сохранённые annotations и позже уточняет визуальные dimensions. В другой допустимой раскладке W2-12 можно поручить исполнителю с меньшей текущей сетевой нагрузкой; K-ID и отдельные выходы должны сохраниться. Новые findings передавать до конца группы, особенно blocking access и semantic contradictions.

Для P0 ячеек полезный результат обязателен, но «источник не удалось получить после конкретных официальных fallback» — тоже результат с exact access evidence и готовой следующей процедурой. Нельзя закрыть ячейку повторением оговорки W1 без новой попытки получить недостающее звено. P2 допустимо явно отложить по scope и сохранить Q; это не должно подменить вторую волну только документальным пересказом.

## Что передать сборщику после W2

Сохранять W1 facts как исходные и привязать W2 corrections, а не переписывать их задним числом. Для каждого K нужен итог: закрыто / область уточнена / противоречие / открыто / утратило значение, с W2 source/fact/artifact и практическим изменением. В частности, порог SFCHD и de-identification — наблюдения по сохранённому первоисточнику; их не нужно представлять как новый сетевой discovery.

Общая программа manifest/roundtrip/partial labels и приём organizer data уже намечена в W1-12/14/15. Сборщик должен свести её в готовые E-ID с inputs/version/actions/metrics/artifacts/outcomes/limits и nullable original group IDs. Для этого не нужна новая сетевая ячейка. Нужно явно разделить coverage_by_dataset_class, source object/region geometry, visibility, annotation status, observed wearing state, relation evidence и policy/event fields; одна строка unknown не заменяет все эти различия.

Данные организаторов и обязательная target taxonomy остаются внешними неизвестными. Отсутствие их сейчас не блокирует W2, но ни одна успешная открытая проверка не докажет CCTV/LinQ перенос, real-time performance, event false alerts/h или правильность промышленного респиратора на целевой камере.

---

## Дополнение сборщика после завершённой второй волны

Добавлен о 23.10.2026, Europe/Moscow, после замороженных W1/W2. Исходный текст выше не переписан: он описывает состояние до второй волны. Это обработка исходных замечаний, не финальный аудит отчётов. Сборщик использовал сохранённые первичные artifacts, новых сетевых запросов/волны/агентов нет. Общие F/S/Q/E-ID — [RAW_FACTS.md](RAW_FACTS.md), [SOURCES.md](SOURCES.md), [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md); local→global — [_WORK/ID_MAP.md](_WORK/ID_MAP.md).

| K-ID | Итоговый статус | Новое основание и изменение решения | Что остаётся |
|---|---|---|---|
|K001|Область уточнена|W2-01/E019: full manifest 32,398 paths, exact release member counts 8,099×4+2;13 YOLO samples/228 boxes matched mapped raw,16/17 IDs. F006–F013. Для object baseline выбран exact Kaggle v1, raw остаётся отдельным artifact.|Не full released label parse/cleanup equivalence; Q004/E001/E003.|
|K002|Область уточнена; упрощение опровергнуто|W2-02/E020: off включает лежащую перчатку, очки/каску в руке, жилет на стене, mask под подбородком; wearing-object и absence-person нельзя приравнять. F014/F015/F020.13376117 coordinate discrepancy разрешён exact released image, F016.|Official off/completeness/association protocol и доли noise неизвестны; Q005/E004/E005.|
|K003|Противоречия локализованы; source route установлен|W2-03/E021:50,552 sharedboxes совпали COCO↔YOLO,12 material OOB отделены от 518 tiny; два разных val, test 6⊂TXTval; missing JPEG и TXT одного basename. Рабочее intersection 12,372 media/50,552 boxes, не regened TXT как восстановление media. F024–F031.|Missing pixels и paper split metric Q006/Q007; E001–E003.|
|K004|Область уточнена|W2-04/E022: official media directory,7 paired images/27 boxes,40 prefixes все в train/val,205 sharedruns; два runs одного prefix имеют один view. De-identification ограничивает timestamps. F032–F036. Роль adapt/development, own proxy holdout.|Нет supplied camera/plant groups и explicit data grant; Q008/Q003/E007/E014.|
|K005|Закрыт критический geometry gate; область ограничена|W2-05/E023: actual archive/splits,20 XML/8 JPEG; literalperson — normal-head bbox, hat часто helmetedhead/face, не shell-only. F042–F045. Loader должен сохранить head unit.|Ordinary hats/carried helmet/coordinate origin/aggregate rights Q009/Q010.|
|K006|Область уточнена; artifact map gate закрыт|W2-06/E024: map 0 person/1 vest/2 blue/3 red/4 white/5 yellow подтверждён archive README,1,330 pairs/splits,27 labels/4 JPEG; person/body и vest/object units. F046–F049.|Exactparentcrosswalk, full completeness, rights Q010/Q003; отсутствие no_helmet label не negative.|
|K007|Count contradiction объяснён; область уточнена|W2-07/E025:5,000 XML все hash matched,75,578 objects=75,570 six-class+8 unexpectedperson; две пары extra имеют mixed/unknown states, quarantine. F050–F055. Структурный XML gate закрыт.|Intended extra map/official 4,000/1,000 membership/ordinary hat protocol Q011/Q009; PNG layer не audited полностью.|
|K008|Область уточнена|W2-08/E026: original 1,000/29 COCO, HFtest 29 annotations matched с categoryshift; author 29.03.2022 распространяет Apache 2.0 на code+labels. Mask неоднороден; PNG15 candidate partial; exact PNG762 dimension mismatch quarantined. F056–F062.|Per image license/source join,100 test protocol, exact media frames и industrial subtype/state GT Q012/E004/E014.|
|K009|Область уточнена; access gap локализован|W2-09/E027: smoking/calling primary PDF прочитан; behavior face+objects и cigarette/hand/phoneboxes описаны, payload только reasonable request. Smoker 1120 decode 250×250, exact RGBduplicates 0, actualphone/inhalerconfusers. F063–F066.|Detectiondata/terms/source groups по Q013; temporal/flammablepolicy GT нужно разметить E012.|
|K010|Область уточнена; replay inputs получены|W2-10/E028:691 MP4 manifest~10 GB,8 actual samples 1080p/H264 с разными rates/timebases/start, view overlap и possibleleftcensoredonset. F067–F071. Реальный replay готов.|Continuoussafe hours, polygons/tracks/events и supplied camera IDs Q014/E013.4,000h не опубликованный benchmark.|
|K011|Область уточнена; приоритет понижен|W2-11/E029: raw_id_2 у 340 IDs встречается с разными classes; safe parser сохраняет raw IDs; Core clip иной sequence, не paired 4.txt. F072–F075. Supplementary не выбирать maintracking/event donor.|Schema/frameindex/identity/splits/source provenance Q015/E011; отсутствие найденных docs не их не существование.|
|K012|Область уточнена; основные permissions открыты|W2-12/E030 и archive checks: SFCHDnotice не найден, SH17 exactv 1 NC-SA/Zenodo NC/paperwording сохранены; CPPElabel scope уточнён; Construction internal AGPL установлен;Önaldata/articlelayers различены. F018/F035/F045/F049/F055/F060/F071/F079/F083.|Action-specific SFCHD/SH17/others Q003/E014. Unknown не общий запрет; own-data/metadata preparation продолжается.|
|K013|Закрыто для annotation-scale задачи|W2-13/E031:132 groups/202,781 rows, native/640 per-class quantiles/hists; SFCHDsmall<0.1%, large>0.2% точно восстанови ли table. W1-13-F04 threshold 0.12% исправлен F039, история сохранена.|Target pixels/exact LinQinput/accuracy/optical resolvability не установлены, Q002/E008.|
|K014|Область уточнена; fallback дошёл до artifacts|W2-14/E032: Pictor 774 crowdmanifest/2,497 workers vs2,496 published, map Approach 2 ещё unknown; Construction full ZIP1,416 pairs/10 orphans, part-local no_* и torso none sample. F080–F086.|Pictormap/terms, Q017; Constructionnone/completeness/upstream, Q018; не whole-personabsence и не universalindustrialbenchmark.|
|K015|Область уточнена; synthetic отложен по роли|W2-15/E033: deterministicfamily 282 chunks/157 parents, не substring 187; allselecteddocumentedbundled,1:1 manifest join, metadata windows valid. NVIDIAgrant/restrictions и Googleconditions прочитаны. F076–F079.|Exact media member/visualquality/generator/scenario groups/action scope Q016/E010/E014; не real camera-hour holdout.|

Ни одно замечание не отмечено «утратило значение»: проверки изменили допустимую роль или точнее локализовали неизвестное. «Закрыто» в K005/K013 относится только к указанному geometry/annotation-scale вопрос у, а не к общей пригодности набора. Новые открытые вопросы не запускают скрытую третью волну; это программа следующей практической работы.

