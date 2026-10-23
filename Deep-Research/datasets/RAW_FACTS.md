# Подробная фактическая база datasets

Версия сборки: `datasets-collector-freeze-2026-10-23`, договор `mosprom-research-v1`. Основа — все 15 результатов первой и все 15 результатов второй волны, исходная критика K001–K015 и сохранённые первичные артефакты. Сборка без сети. Дата получения источников — 23.10.2026, Europe/Moscow (UTC+3); даты публикаций/версий — в [SOURCES.md](SOURCES.md). Веточные ID сохранены в [_WORK/ID_MAP.md](_WORK/ID_MAP.md). Это база до авторского синтеза: числа относятся к явно названным artifacts/scopes, а не к абстрактному имени датасета.

Для каждого F-ID ниже указывается вид основания: **документ** (первичный текст/схема), **заявление** (author claim/count/измерение автора), **наша проверка** (выполненное чтение/под счёт/декодирование/наблюдение), **вывод** (интерпретация перечисленных оснований), **предложено** (будущее действие), **неизвестно**. Прочитан о, получен manifest, получен payload, parsed, decoded, visually inspected — разные статусы. Если subsection содержит таблицу, её строки относятся к F-ID этого subsection. Карточки не являются проведённым обучением или полной semantic validation.

## Рамка задачи и единицы supervision

<a id="f001"></a>

### F001 — состояние кейса и границы

**Документ/контекст:** `Context-prompt.md`, `prompt-datasets.md`, mosprom-research-v1; это предоставленное задание, не новый сетевой источник. На срезе исследования полного кейса, target taxonomy, organizer media, точной LinQ конфигурации и target preprocessing нет. Каска, снятый респиратор, опасная зона, курение рядом с горючими — опубликованные примеры, не установленный полный обязательный список. Нельзя объявлять gloves/boots/harness обязательными или обещать поддержку всех примеров. Данные об RTX4070/облаке не устанавливают VRAM/SDK/input size.

<a id="f002"></a>

### F002 — разные объекты измерения

**Вывод:** S001/S014/S018/S020/S027/S031/S032. Предмет, часть тела, человек с атрибутом, класс изображения, clip class, track, временной интервал и нарушение policy требуют разных GT. Helmet box не равен helmeted-head box, а тот не равен full-person compliance box. Статичный off-предмет может не принадлежать видимому человеку. Zone crossing требует polygon/опорной точки/правила; unsafe event дополнительно требует policy. Отсутствующий label может означать out-of-scope, не видимость или пропуск. Ни один из этих случаев автоматически не verified absent.

<a id="f003"></a>

### F003 — что фактически проверено программой

**Наша проверка, сводная:** S004–S006/S010/S013/S016/S018/S019/S021/S026/S030/S032/S033/S037/S039/S044/S048. Выполнены небольшие acquisition/structure/semantic проверки и несколько полных annotation-layer audits: SH17 raw 8102; SFCHD annotations; SHEL5K5000 XML; CPPE original COCO; Smoker 1120 decode; Construction full directory/labels. Полных source-image duplicate audits, обучения, inference quality, LinQ throughput, целевых camera-hours и полного legal clearance нет. Замороженные W1/W2 журналы уточняют владельца каждого наблюдения; collector не повторял сеть и не превращает чужой count в свой.

<a id="f004"></a>

### F004 — отсутствие универсального открытого event GT

**Вывод с ограниченным scope:** S001–S046, все исследованные ветки. Не установлен один доступный первичный набор, одновременно покрывающий exact industrial respirator subtype/correctness/removal, person associations/tracks, site rules/zones и длинные репрезентативные safe periods. Это результат данного поиска, а не доказательство отсутствия таких данных вообще. Для событий целевая доразметка остаётся отдельным необходимым маршрутом; Q001/Q002/Q012, E012/E013.

## D01 — SH17: released v1, raw и источники фото

<a id="f005"></a>

### F005 — происхождение, annotation protocol и домен

**Заявление/документ:** S001 §III; S002 README. SH17 собран из Pexels/web фотографий промышленной деятельности, не из исходного CCTV. Пустые изображения при сборе исключались. Аннотировали четыре человека: три размечали, lead проверял/исправлял, graduate student дополнительно проверял; Dark Label/Label Img. Это manual/review lineage, не установленный pseudo-label pipeline. Формальное правило исчерпывающей разметки/min-size/occlusion по всем классам не найдено. Высокое разрешение и слово manufacturing не устанавливают target-camera transfer. Нет GT FPS/tracks/zones/events/person-item relation IDs.

<a id="f006"></a>

### F006 — точный released artifact и manifest

**Metadata, полностью прочитан о:** S003, W2-01 `MANIFEST_PROGRESS.json` (SHA256 `de54fdd338e6714bc3b6a884efc41a44e999da07a2af6241f0682637b9963746`). Kaggle owner/ref `mugheesahmad/sh17-dataset-for-ppe-detection`, id5329058, version 1, creation 03.07.2024 23:09:23.513 UTC. Полный listing 32,398 unique paths =8,099 `images/` +8,099 `labels/` +8,099 `meta-data/` +8,099 `voc_labels/` +2 split files; stem sets совпали. Listing bytes: images 14,203,596,226; YOLO2,998,015; metadata 10,672,761; VOC19,863,513. Ранее API total Bytes 14,096,291,832 — отдельное metadata поле, не локально измеренный ZIP и не сумма декодированных pixels. Ни один metadata size не называть полным скачанным архивом.

<a id="f007"></a>

### F007 — работающий путь получения и фактический payload

**Наша проверка:** S004. Работает query `?fileName={path}`; прежний path-suffix route возвращал 404, а `released_sh17.yaml` —404 JSON. Для W2 получены 13 released YOLO,2 VOC,2 metadata JSON,1 released image ZIP. Сохранены exact requests/status/bytes. Endpoint может вернуть text или ZIP, даже если имя заканчивается jpeg; формат определять по содержимому. Полностью 8,099 YOLO не downloaded/parsed. Для production ingestion зафиксировать version 1 и hash каждого полученного payload; не под менять release внешним current URL по сходству имени.

<a id="f008"></a>

### F008 — точная zero-based карта 17 классов

**Документ/артефакт:** S002 `sh17.yaml`; S004 sample IDs. Это порядок YAML, не порядок таблицы статьи. Box unit — объект/часть тела/человек по классу; source YOLO normalized cxcywh. В таблице counts — **авторская Table II**, не actual full release count.

| ID | Literal | Table II instances | Семантика и ограничение |
|---:|---|---:|---|
|0|person|13802|человек; raw demographic labels свернуты|
|1|ear|7730|часть тела|
|2|ear-mufs|318|в definition допускаются over-ear headphones|
|3|face|8950|face criterion связан с видимостью носа|
|4|face-guard|134|щиток; не full-face respirator|
|5|face-mask|669|Table II Face-mask-medical; не exact industrial respirator|
|6|foot|796|стопа без shoes, включая socks; не universal no_boots|
|7|tool|4647|предметы tools|
|8|glasses|1945|safety и vision объединены|
|9|gloves|2790|on/off объединены|
|10|helmet|927|raw on/off и цвета свернуты|
|11|hands|15850|кисть; не universal no_gloves|
|12|head|11985|часть тела любых ракурс о в; не no_helmet|
|13|medical-suit|155|medical clothing|
|14|shoes|4560|обычная/условно safety обувь объединена|
|15|safety-suit|530|опубликованные counts конфликтуют|
|16|safety-vest|530|предмет; raw on/off свернуты|

Написание `ear-mufs` сохранять; label IDs нельзя назначать по визуальному порядку README. YAML val placeholder/test empty и comment 128 images не являются реальным и split metadata.

<a id="f009"></a>

### F009 — splits и filename alias

**Наша полная проверка имён, не pixels:** S002/S003, W1-02 `split_audit.json`, W1-14 `SH17_split_audit.json`. Реальные `train_files.txt`6,479 unique и `val_files.txt`1,620 unique; intersection 0, union 8,099; test file 404 и в полном listing нет третьего split. Paper называет 20% test, artifact — val: не создавать обе независимые partitions. CSV содержит 8,099 unique URLs. Один alias: URL `carrying-on-head-indian-farm-worker-158011.jpeg` против split/raw `carrying-head-indian-farm-worker-158011.jpeg`. Join выполнять по release paths с явной alias table. Photographer/Pexels ID могут помочь, но не являются supplied session IDs.

<a id="f010"></a>

### F010 — полный raw structural parse

**Наша проверка:** S005 `raw_audit.json`/`geometry_audit.json`. ZIP5,835,796 bytes,8,103 entries=8,102 XML+directory;8,102 unique filename,76,008 objects, parse failures 0. Empty XML ровно 2:4480451/4614217. Range audit нашёл 2 bbox за declared bounds:258626 person `[1725,4430,1874,4664]` при 3456×4608;259265 tools-off `[1559,123,3509,1358]` при 3504×2336. Flags truncated 0/difficult 0=71,949, truncated 1/difficult 0=4,059, difficult 1 не найден. Это raw version, не доказанные ошибки final labels и не semantic error rate.

<a id="f011"></a>

### F011 — raw states и counts

**Наша проверка, scope 8,102 XML:** S005. Все literal classes/первые bboxes в raw_audit.json; state-specific поддержка ниже. On/off не исчезает из исходного XML; flattened release теряет эту информацию.

| Literal base | on objects | off objects |
|---|---:|---:|
|gloves|2669|121|
|glasses-vision|1357|163|
|glasses-safety|373|52|
|ear-mufs|211|107|
|face-mask-medical|635|35|
|safety-shoes|1150|22|
|other-shoes|3287|101|
|tools|1739|2903|
|safety-vest|525|5|
|safety-suit|234|6|
|face-guard|123|11|

Body-part counts hands 15,850/head 11,985/face 8,950/ear 7,730. Medical-suit-on157. Raw `halmet-*` сохраняет typo, state и цвет; полные 60 raw categories доступны также в scale artifact. Safety shoes в paper definition допускает thick joggers — label не сертификат industrial footwear.

<a id="f012"></a>

### F012 — raw→released состав и кандидатная к он версия

**Наша проверка множеств + вывод:** S003/S005/S004, W2-01-F02. Из raw исчезли 3 stems:4614217/4480451(empty),12069485(1 fork-lift). Released-only 0. Raw на released-member stems имеет 76,007 objects. Исключение 13 fork-lift, не входящих 17-map, даёт 75,994. Это объяснимый кандидатный route к заявленным 8,099/75,994; совпадение totals не full equality всех released labels. Author conversion удаляет on/off/цвет/safety-vs-vision, demographic→person, исправляет halmet→helmet; `COMPARE.py` — наша реализованная кандидатная функция, не общий официальный converter для любых future revisions.

<a id="f013"></a>

### F013 — реальное paired raw/released сравнение

**Наша выполненная проверка:** S004 `PAIRED_COMPARISON.json`;13 targeted images/228 boxes, coverage 16/17 IDs (нет foot 6), unmatched 0, category и normalized geometry совпали при maxabs<1e-6. Sample box counts 1,2,8,7,3,2,10,4,16,8,154,6,7. Это подтверждает conversion lineage только sample, не очистку/полноту всего release. Для 5691469 лежащая `gloves-off` стала ID9 gloves; подозрительный glasses у 5691606 стал ID8. Release conversion не и с правила этот конкретный semantic candidate.

<a id="f014"></a>

### F014 — off означает и не надетые предметы

**Наша visual проверка, targeted:** S006.5691469 gloves-off — пустая перчатка лежит;4299424 on — перчатка на руке.3822859 glasses-safety-off — висящие очки;8820998 on — на лице/удерживаются у висков.5715901 vision-off — очки в руке.209719 vest-off висит, halmet-off-blue на стене, halmet-on-yellow на голове одновременно.8961520 yellow-off каска в руке при голой голове. Эти существующие контрпримеры опровергают автоматический mapping off→person without PPE. Они не доказывают, что всякое off по формальному протокол у всегда одинаково; официальная exhaustive instruction не найдена.

<a id="f015"></a>

### F015 — mask/face-guard states и наблюдаемая noise

**Наша visual проверка:** S006.5726785 medical-mask-off спущена под подбородок;6098063 on закрывает рот/нос.3379761 face-guard-off держится перед/рядом с лицом сварщика: policy protection не задаётся одним off. У 5691606 glasses-vision-on bbox визуально охватывает перчатку/ручной инструмент, очки не различимы; dimensions 2537×3800 совпадают с XML, filename/URL связаны selection — кандидат wrong class, не необъяснённый frame mismatch.8488036 имеет перекрывающиеся halmet-on-yellow/red разного extent у одной головы. Не оценивать частоту noise по этим выбранным случаям и не менять source originals молча.

<a id="f016"></a>

### F016 — 13376117: разрешённый coordinate-frame mismatch

**Наша проверка exact media:** S004/S006. Current Pexels 13376117=8688×5792; raw и released VOC=8192×5461; source metadata тоже сообщает 8688×5792. Released endpoint вернул 4,580,857-byte ZIP; извлечён единственный JPEG8192×5461. Прямой overlay на released pixels согласуется с рабочими/предметами. Прежнее наложение pixel-box на current Pexels было ошибочным pairing и сохраняется как пример риска URL, не evidence массово сдвинутой разметки.12/13 current Pexels dimensions совпали, но equal dimensions само по себе не pixel identity.

<a id="f017"></a>

### F017 — опубликованные counts и нерешённые расхождения

**Заявление/противоречие:** S001 Table II vs Appendix Table VIII. Safety-suit 530 против 195+45=240; medical-suit 155 против 114+43=157; mask 669 против 519+151=670; foot 796 против 610+149=759. Table VIII faceguard 110/24, earmuffs 269/49, helmet 773/154, vest 433/97 показывают редкую поддержку, не independent people/cameras. Вывод F012 объясняет total 75,994 на candidate map, но не выбирает молча одну class table как истинную. Actual full released counts остаются E001.

<a id="f018"></a>

### F018 — rights layers SH17

**Документ/metadata:** S002/S003/S007/S008. Kaggle v1 и README CC BY-NC-SA 4.0/research-education; Zenodo 12659325 v1 CC BY-NC 4.0/restricted files; paper Introduction/Conclusion commercial wording не от меняет NC artifact. Отдельная лицензия кода в tree не найдена. Raw attachment scope отдельно не прояснён. Pexels current Terms 20.10.2026 допускают commercial/noncommercial use при запретах standalone redistribution, ложного endorsement и ряда использований изображений лиц/брендов; crop/resize сам по себе standalone не снимает. Это не установленная историческая license каждого фото 2024 и не ML-specific blanket clearance. Призовой хакатон/weights/SA scope исследованием не решены; Q003/E014.

<a id="f019"></a>

### F019 — native масштаб SH17: опубликованное и подсчитанное

**Заявление:** S001 — max 8192×5462/min 1920×1002;39,764 annotations<1% image area и 59,025<5%. Это не bbox side pixels. **Наша проверка:** S048 computed declared-frame distributions для 60 raw categories, отдельно all/raw-release-members; min-axis 640 q10/q50/q90: mask-off 35 objects 5.27/26.56/64.42; mask-on6357.38/33.81/86.2; gloves-off 1217.25/20.98/95.56; gloves-on26697.24/30.67/102.46; glasses-safety-off 5215.14/30.34/75.31; on37310.33/37.04/76.28; vision-off 16311.89/29.69/76.81; on13579.71/24.75/51.24. Эти дробные px — hypothetical transform, не точность модели. Полные native/640 width/height/area/min-axis quantiles/histograms см.F041 и machine-readable artifact S048.

<a id="f020"></a>

### F020 — полнота и от ношения SH17

**Неизвестно/вывод:** S001/S005/S006. Head не no_helmet, hands не no_gloves, ear-mufs не удостоверяет protection against noise, on не correct-fit. Нет formal relation IDs или исчерпывающего wearing/absence protocol. Для raw-state adaptation нужен новый слой person_id, ppe_object_id, association_evidence, visibility, observed_state(worn/unworn/adjusting/unknown), annotation coverage. Policy/event хранить отдельно. Не размеченный целевой класс требует ignore/partial-label route или доразметки, не background assumption.

<a id="f021"></a>

### F021 — практическая роль и acquisition route SH17

**Вывод/предложено:** F005–F020. Условный broad object/body-part donor; воспроизводимый baseline — exact Kaggle v1 images+labels с author split, version/hash/alias log. Raw derivative — только явное membership intersection и checked coordinate frames; raw qualifiers сохранять отдельными полями. Не independent CCTV holdout и не ready absence detector. Получать все 14 GB ради class-map не нужно: label metadata слой мал; перед training выполнить E001/E003/E005/E006/E014. Нет автоматически признанного права на публичный raw/crop pack.

<a id="f022"></a>

### F022 — ограничения независимости SH17

**Заявление/неизвестно:** S001/S002/S003. Авторы пишут о duplicate removal, но distance method/cluster manifest не получены. Filename train/val disjoint не доказывает отсутствие near duplicates/общих фотосессий. Photographer ID/source URL/Pexels ID помогают audit, но photographer≠session. Crops/augmentation/raw relabel на следуют original group/split; E006/E007. Open Q004/Q005.

## D02 — SFCHD: chemical-plant CCTV, source-of-truth и proxy splits

<a id="f023"></a>

### F023 — domain, collection и de-identification

**Документ/заявление:** S017 §3.1–3.2. Два chemical plants, nearly 40 indoor/outdoor scenes, неделю сохраняли 1 image каждые 10 frames при наличии людей. Из~40,000 retained 12,373. Это не известный FPS/видео поток и не representative empty/safe camera hours. Шесть professional security inspectors размечали, три graduate students review; perfectaccuracy claim не наш audit. Время/plantlocation и другие sensitive fields de-identified. По пикселизированным надписям нельзя восстанавливать надёжные camera timestamps/session IDs. Extreme high/low/normal light категории описаны, но полный scene/light manifest не получен.

<a id="f024"></a>

### F024 — точный COCO artifact и counts

**Наша полная annotation проверка:** S018 `all_data.json`20,359,104 bytes:12,373 unique image IDs/names,50,559 unique annotation IDs, empty images 0, duplicate IDs0. `val.json`4,152,148 bytes:2,475 images/10,336 annotations. Declared dimensions:11,349 records 1280×704,1,024 records 1920×1080. Paper max 1920×1280 — другое документарное утверждение, не найденное максимальное JSON resolution. COCO bbox xywh pixels; segmentation empty/iscrowd 0 не создаёт segmentation labels, tracks или associations.

<a id="f025"></a>

### F025 — literal map и полные COCO counts

**Наша проверка:** S018 categories/classes.txt/count. Порядок ниже artifact, не порядок README table.

| ID | Literal | Actual COCO boxes | Geometry/meaning |
|---:|---|---:|---|
|0|person|17010|full/visible person region; state не задан|
|1|helmet|14298|каска object box|
|2|self_clothes|780|Other Clothing, преимущественно torso region|
|3|safety_clothes|14813|Safety Clothing torso; не автоматически generic reflective vest|
|4|head|1200|head region, source no-helmet candidate; не universal head|
|5|blur_head|1134|неразличимая защита головы из-за света/тени|
|6|blur_clothes|1324|неразличимая одежда|

Blur classes вести в unknown/ignore для target wearing, не no_helmet/no_vest. Relation IDs person→garment/helmet и correctness не заданы. Source semantic contract ограничивает допустимый merge даже при одинаковой numeric geometry.

<a id="f026"></a>

### F026 — три опубликованных total и один проверенный состав

**Противоречие/наша проверка:** S017/S018/S019. README overview 50,558, per-classsum 50,559; current PDF abstract/§3.2 встречается 50,552; COCO actual 50,559. Working media intersection из F027 имеет 50,552 boxes, но не утверждается, что именно это исторически объясняет все publisher counts. Не объявлять три числа тремя независимыми датасетами. Current commit 2025-format manuscript и ar Xiv2023/2024 — версии одного семейства, не independent data.

<a id="f027"></a>

### F027 — реальный media manifest и исключение

**Наша directory/membership проверка:** S019. Официальный ZIP total 1,972,746,810 bytes,37,216 entries; `QY_final_dataset/images/`12,372 JPG. COCO-only name ровно `192.168.2.20_1c_29.jpg`; extra JPEG0. В modern labels.zip отсутствует его TXT, author train+val union тоже его исключает. У COCO record 7 annotations (по одной ID0..6); old `yolo/train/` TXT реально извлечён и совпал с candidate COCO→YOLO. JPEG ни это, ни регенерация TXT не восстанавливает. Рабочий состав **12,372 media names/50,552 boxes**, reason `media_not_in_author_archive`; record quarantine до source pixels. Полные 12,372 JPEG не decoded.

<a id="f028"></a>

### F028 — COCO↔YOLO consistency

**Наша полная annotation проверка:** S018, W2-03 `AUDIT.json`. labels.zip 3,569,708 bytes,12,372 nonempty TXT+directory, extra stem 0. Все 50,552 sharedboxes совпали по class и normalizedcxcywh при tolerance 1e-5; actual maxerror 2.5673907444456745e-16. Единственное missing TXT с 7 boxes — F027. Consistency двух представлений не независимое semantic подтверждение; одинаковая ошибка может быть общей. COCO-native предпочтителен для source-of-truth, если выбор версии/rights принят.

<a id="f029"></a>

### F029 — geometry: численная tolerance и 12 material outliers

**Наша проверка:** S018 `SUPPLEMENT.json`,`GEOMETRY_OVER_0_001.json`. Strict bounds 530 OOBboxes при 1e-6 px, из них 518≤0.001 px;12>0.001 и>0.01 px, max 9.000288 px,10 person/2 safety_clothes. Example annotation 640 `192.168.2.20_35.jpg`: `[139.00032,456.00016,187.00032,257.000128]` при 1280×704, overflow 9.000288. Не удалять все 530 как corruption. Clipping только derived transform с original bbox/log/decoded WH; здесь удаление/clipping не выполнялось. Strict per-class OOB: person 314/helmet 54/safety_clothes 155/self_clothes 5/head 2.

<a id="f030"></a>

### F030 — два разных val и перекрывающийся tiny test

**Наша полная membership проверка:** S018. TXTtrain 9,897/TXTval 2,475 unique, intersection 0, union 12,372. COCO val тоже 2,475, но overlap TXTval 520, по 1,955 уникальных с каждой стороны, symmetric difference 3,910. COCO val records совпали с all_data по IDs/content. Это разные protocols. Все 6 test paths входят TXTval, не train; `annotations/test.json`0 bytes. Ни 6, ни COCO val+TXTval не образуют независимый третьий test. Сравнение published metric требует явного выбора протокола Q007.

<a id="f031"></a>

### F031 — точные tiny-test paths и path remap

**Наша проверка:** S018. Test: `192.168.11.13_neg_7c_2832.jpg`, `192.168.2.35_neg_12c_362.jpg`, `192.168.2.28_caiji_1_24.jpg`, `192.168.2.221_400.jpg`, `192.168.2.34_neg_12c_275.jpg`, `192.168.2.220_480.jpg`. Author TXT paths абсолютные `/home/yfs/data/QY_final_dataset/images/...`; loader должен remap в portable relative paths и проверить basename collisions. Старые sample folders в git повторяют bytes: blob`6c81d4c00b085864d05c5267f2f38988bf63e6b2` лежит и в sd_train, и в train/person для 2.20_17. Не прибавлять служебные copies к unique data.

<a id="f032"></a>

### F032 — proxy group overlap

**Наша metadata проверка:** S019 `RUN_GROUPS.json`/`PREFIX_GROUPS.json`. Удаление final `_integer` даёт 231 inferred runs:205 bothtrainval,24 train-only,2 val-only;6 из 205 также tinytest. Initial IPv4-like prefix даёт 40 prefixes, все 40 есть train+val,6 также test. Эти keys не supplied camera/run schema. Nearly 40 scenes в статье не доказывает 1:1 к 40 prefixes. Random filename split не independent-camera metric; доказанное пересечение proxy не равно доказанной утечке всех near-duplicate frames.

<a id="f033"></a>

### F033 — семь actual images и наблюдаемая geometry

**Наша targeted visual проверка:** S019 `PAIRED_AUDIT.json`/`CONTACT.jpg`; выбран первый annotation record каждого из 7 classes,7 JPEG/27 boxes, не случайная выборка.9 person/6 helmet/1 self_clothes/6 safety_clothes/2 head/1 blur_head/2 blur_clothes. Все 7 decoded WH совпали с COCO. Images 2.20_particular_duanxiu_13 и 2.20_caji_1021_1_70 показывают один устойчивый indoorview;2.209_caji_1021_1_0 — яркое помещение;2.221_400 — маленький дальний outdoorperson (1920×1080);11.13_neg_7c_2832 — двор;2.31_caji_1021_1_126 — за с ветка/blur;2.28_caiji_1_24 — тёмный цех/яркие окна. Остальные samples 1280×704. Head — не full person; clothing box — торс; blur помещён на трудноразличимые region. Не generalize completeness по 27 boxes.

<a id="f034"></a>

### F034 — run split не достаточен для нового вида

**Наш вывод по visual evidence:** F032/F033, S019. Два разных run suffix одного 2.20 prefix имеют совпадающие помещение/колонну/оборудование/framing. Поэтому разнести runs недостаточно для view-disjointness. Prefix grouping — более консервативный первый proxy, но другие prefixes тоже могут относиться к связанным views/sites; не проверено. Предлагается own inferred-view-grouped holdout с manual collision review и nullable author camera ID/plant ID. Это не author camera-disjoint test и не target-camera holdout.

<a id="f035"></a>

### F035 — exact acquisition и notice gap

**Наша проверка/неизвестно:** S017/S019. Drive/Baidu author route жив; Range 206 дал directory и members, full ZIPhash/revision неизвестны. Baidu README id1k2p Wg8r-G3 KSI2Q3 Tdt6 kg/passwordv 4 ao, дополнительный путь не получен как wholepayload. Archive directory не содержит LICENSE/terms/readme/directory.md, хотя README схематично показывает directory.md. В pinnedtree нет LICENSE; root LICENSE404. Это ограниченная проверка, не grant и не proof отсутствия любого author permission. Scope local training/public demo/labels/weights/deployment unknown Q003. Не загружать `labels.cache` как trusted executable; TXT/JSON достаточны.

<a id="f036"></a>

### F036 — роли и безопасная подготовка SFCHD

**Вывод/предложено:** F023–F035. Один из ближайших найденных factory CCTV donors для adapt/development и unknown-aware helmet/clothing; не готовое видео/track/event GT. Pin COCO/source split, intersect 12,372 media/50,552 boxes, сохранить missingrecord и original bbox, decode выбранный split, tolerance отдельно от 12 material outliers, derived YOLO с roundtrip. Official TXTsplit для reproduction; COCO val отдельным name; independent testing — own proxy groups и позднее target holdout. Rights gate отдельно. E001/E002/E003/E007/E014.

<a id="f037"></a>

### F037 — SFCHD measured per-class size quantiles

**Наша проверка:** S048 full COCO12,373/50,559, включая 7 missing media annotations; не media-ready subset. Minimumaxis q10/q50/q90 в pixels ниже; continuous hypothetical letterbox 640 по declared WH, без rasterrounding/clipping. Native/640 width, height, area и все quantiles лежат в SCALE_SUMMARY/QUANTILES.

| Class | n | Native min-axis q10 / q50 / q90 | 640 min-axis q10 / q50 / q90 |
|---|---:|---|---|
|helmet|14298|12 /27 /58|6 /13 /29|
|head|1200|12 /21.06 /39|4.21 /9 /18.5|
|blur_head|1134|4 /14 /24|2 /6.5 /12|
|blur_clothes|1324|9 /26 /53.51|4.5 /12.5 /25.37|
|person|17010|27 /58 /129|13 /28 /63.02|
|safety_clothes|14813|24 /49 /105|11.32 /23.5 /52.5|
|self_clothes|780|28 /53 /100.1|11.97 /26 /50.05|

<a id="f038"></a>

### F038 — частота малого min-axis не качество detector

**Наша проверка/вывод:** S048. Условный 640 helmet min-axis<16 px у 8,845/14,298(104+3,334+5,407 histogram bins), blur_head 1,100/1,134. Это основание проверить crops/tiling/input size, не утверждение универсального рабочего порога и не measured AP. Причины blur/visible absence отдельно; нельзя заменить unknown отрицательным классом. Target object pixels и end-to-end cascade losses нужно измерять E008.

<a id="f039"></a>

### F039 — исправление small threshold

**Первичный документ и наш пересчёт:** S017 §3.3/S048. Цитируемое SPIE0.12% в статье отличается от собственного SFCHD smallarea_fraction<0.001(0.1%), large>0.002(0.2%), remainingmedium. W1-13-F04 ошибочно подписал таблицу 0.12%; исправлен о через K013/W2-13, исходная история сохранена. Equality boundary относится к remainingmedium. Это relativearea, не COCO32²pixels и не min axis.

| Class | Total | Small<0.1% | Medium | Large>0.2% | Small при 0.12% |
|---|---:|---:|---:|---:|---:|
|helmet|14298|7717|3030|3551|8472|
|head|1200|941|164|95|1010|
|blur_clothes|1324|730|313|281|799|
|blur_head|1134|1078|41|15|1096|

Собственный 0.1% точно восстанавливает source table;0.12% не восстанавливает.

<a id="f040"></a>

### F040 — иллюстративный resize и crops

**Расчёт/вывод, не модельный эксперимент:** S048/W1-13. Letterbox 640: s=min(640/W,640/H), bbox width/height×s, area×s²; padding меняет позицию, не размер. Hypothetical 1920×1080 head 30×24→10×8;3840×2160 тотже native box→5×4. Person crop width 180 при input 640 условно растянет тотже 30×24 head до 106.7×85.3 input pixels, но исходных samples остаётся 30×24. Crop не восстанавливает отсутствующую оптику; проверять first-stage miss, обрезание, контекст переносимого PPE и число crops/latency.640 не установленный LinQ input.

<a id="f041"></a>

### F041 — полная сохранённая scale metadata

**Наша executed проверка:** S048. `BOXES.csv`202,781 rows =SFCHD50,559+SH17 raw 76,008+SH17 raw release-member 76,007+CPPE test 207. Rawsubsets намеренно перекрываются, не суммировать как unique observations.132 dataset/class groups=7+60+60+5. `SCALE_SUMMARY.json` хранит input SHA256, native/640 width, height, area, min axis quantiles 0/.1/.25/.5/.75/.9/1 (numpy linear) и histograms. Min-axis 640 bins[0,4),[4,8),[8,16),[16,32),[32,64),[64,128),[128,256),[256,640),[640, inf). VOCwidth=xmax−xmin без+1, COCO xywh; upscaleallowed, rasterrounding/clipping нет. Это declared coordinate frame audit, не оптическая различимость или media quality benchmark. Полные per-class values доступны в[_WORK/MATERIALS/W2-13/QUANTILES.csv](_WORK/MATERIALS/W2-13/QUANTILES.csv) и SCALE_SUMMARY.json, не теряются при переносе папки.




## D03 — SHWD: головы в касках и без касок


<a id="f042"></a>

### F042 — SHWD: происхождение и заявленные counts

**Документ/заявление, прочитано.** README: 7,581 images; 9,044 helmet-wearing positive objects; 111,514 normal-head negatives. Positive images — Google/Baidu, часть normal heads — SCUT-HEAD; ручной Label Img/VOC. Это авторские object totals, не наш полный count XML. Loader `CLASSES=['hat','person']` имеет order 0/1, но VOC хранит текстовые имена. Literal `person` в этой задаче означает голову, а не тело. SHWD/SHW и SHD 5,000 нельзя отождествлять по сокращению.

Основания: [S009](SOURCES.md#s009), [S011](SOURCES.md#s011). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f043"></a>

### F043 — SHWD: реальный архив и split membership

**Наша проверка directory и полученных TXT.** ZIP total 1,117,970,537 bytes по Content-Range; 15,171 entries, 7,581 XML и 7,581 JPG, unmatched stems 0. У media 7,571 `.jpg` и 10 `.JPG`. Actual split files: train 5,457, val 607, test 1,517, trainval 6,064; train/val/test по пар но disjoint, trainval=train+val. Не поставлены camera/session IDs. Получены directory, четыре split файла, 20 XML и восемь JPEG; whole ZIP SHA256/revision неизвестны. Нет найденных README/LICENSE/terms members. Directory pairing не означает full decode.

Основания: [S010](SOURCES.md#s010). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f044"></a>

### F044 — SHWD: actual XML и visual head geometry

**Наша targeted проверка.** 20 XML содержат 214 objects: 24 `hat`, 190 `person`. В восьми paired JPEG все decoded W/H совпали с XML, 127 person/14 hat boxes. `000000.jpg` 947×1421, hat `[60,66,910,1108]` охватывает каску и голову/лицо; `001477.jpg` 955×1300 — тоже helmeted head со stock watermark. `part2_000069.jpg` 901×362 — коллаж трёх портретов; `part2_000761.jpg` 626×417 — семь касок на головах строителей. `PartA_00063/00535/00772` — classroom views 1091×612/1063×600/1043×575, с 4/54/67 literal person boxes на головах. `000993.jpg` 720×405 — street view с 2 person/2 hat. Это подтверждает head geometry и смешанный web/classroom domain, не обычные шапки/переносимые каски во всём наборе. XML filename/path бывает устаревшим: Part A_00772 содержит `772.jpg`; join по actual memberstem с сохранением raw fields. VOC integer xyxy; origin/inclusive convention не установлен.

Основания: [S009](SOURCES.md#s009), [S010](SOURCES.md#s010). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f045"></a>

### F045 — SHWD: mapping, rights и роль

**Вывод/неизвестно.** Безопасная provisional карта: `shwd:person -> normal_head_region`; `shwd:hat -> helmeted_head_region`. Не смешивать с full-person и helmet-object-only boxes. Correct fit/ordinary hat/carried helmet policy не установлен. MIT root LICENSE — software/associated documentation; SCUT upstream academic-research-only и поисковые фото имеют отдельные ограничения. Весь SHWD не объявляется MIT. Условный head donor; CHV не независимый holdout после него. Exact parent overlaps требуют E006, scope действий — E014/Q003/Q010.

Основания: [S009](SOURCES.md#s009), [S010](SOURCES.md#s010), [S011](SOURCES.md#s011). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


## D04 — CHV: Color Helmet and Vest


<a id="f046"></a>

### F046 — CHV: documented lineage и объём

**Документ/author claim.** Статья §2.3: из примерно 10,000 изображений GDUT-HWD и SHWD отобрано 1,330 images/9,209 instances; новые vest/color labels размечены Label Img и проверены другим исследователем. Выбирались construction backgrounds, позы, ракурсы, дистанции. Random split 1,064/133/133. Это selection+reannotation, не 1,330 новых независимых scenes. Exact image crosswalk не получен; для запрета предполагать независимость parent/child достаточно прямого author lineage.

Основания: [S012](SOURCES.md#s012). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f047"></a>

### F047 — CHV: проверенная карта артефакта, формат и splits

**Документ артефакта/наша directory проверка.** ZIP 439,733,771 bytes; без `__MACOSX/` содержит 1,330 JPG/1,330 TXT stems, unmatched 0. Apple Double `._*` не labels. Archive README: `0 person`, `1 vest`, `2 blue helmet`, `3 red helmet`, `4 white helmet`, `5 yellow helmet`; статья сокращает последние до blue/red/white/yellow. YOLO `<class> <x_center> <y_center> <width> <height>`, normalized по W/H, center не top-left. Actual train 1,064/valid 133/test 133, по парные intersections 0. Полный image decode/9,209 object recount не выполнен. Отдельного LICENSE/terms notice нет.

Основания: [S012](SOURCES.md#s012), [S013](SOURCES.md#s013). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f048"></a>

### F048 — CHV: actual sample и неполная absence supervision

**Наша проверка 27 TXT/4 JPEG.** 194 objects: person 77, vest 48, blue 10, red 11, white 33, yellow 15; unknown IDs/bad five-column rows/out-of-[0,1] values 0. Четыре пары: ppe_0027 660×372, ppe_0071 1000×762, ppe_0183 800×528, ppe_0311 1064×1300; 37 boxes (13 person,11 vest,10 white,1 yellow,1 red,1 blue). Person — тело/видимая часть, helmet colors — каска, vest — одежда/торс с reflective strips; не любая безрукавка. Есть portrait/stock construction images. В ppe_0183 человек без явной каски имеет person box, но no_helmet class/status нет: кандидат доразметки, не exhaustive negative GT. Relation IDs и correctness не заданы. Sample выбран ради coverage, не error-rate estimate.

Основания: [S012](SOURCES.md#s012), [S013](SOURCES.md#s013). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f049"></a>

### F049 — CHV: разрешительный statement и практическая роль

**Документ/вывод.** README “open for free use” и citation — разрешительное заявление с нераскрытым modification/republication/commercial scope, не стандартная blanket media license. Archive README описывает format, не устраняет upstream SHWD/GDUT conditions. Conditional vest/color donor при соответствующем кейсе; не no_helmet donor по missing labels и не independent cross-dataset test. Малый actual artifact снял access/map gate, полнота и права остаются Q003/Q010, E005/E006/E014.

Основания: [S012](SOURCES.md#s012), [S013](SOURCES.md#s013). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


## D05 — SHEL5K: multi-geometry SHD reannotation


<a id="f050"></a>

### F050 — SHEL5K: parent, manifest и полный XML слой

**Документ/наша проверка.** Mendeley v1 23.04.2021, parent SHD `andrewmvd/hard-hat-detection`: те же 5,000 images, расширение 3→6 classes/исправление пропусков по статье. Metadata: 5,000 XML+5,000 PNG, stem sets match. Сумма XML 19,154,616 bytes; PNG 1,310,436,038 bytes — metadata sizes, не compressed ZIP. Получены все 5,000 XML, каждый SHA256 совпал с author metadata; PNG получены семь (3 W1+4 W2), не весь 1.3 GB. Folder API важен: пустой root files [] не отсутствие вложенных файлов. Exact API/folder IDs и content download URLs сохранены S015.

Основания: [S014](SOURCES.md#s014), [S015](SOURCES.md#s015), [S016](SOURCES.md#s016). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f051"></a>

### F051 — SHEL5K: exact literals/counts и объяснение 75,570/75,578

**Наша полная structural проверка XML.** 75,578 objects = `helmet`19,252 + `head_with_helmet`16,048 + `person_with_helmet`14,767 + `face`14,135 + `head`6,120 + `person_no_helmet`5,248 + unexpected `person`8. Шесть advertised literals дают ровно paper 75,570, все six-class counts воспроизведены. Card 75,578 подтверждено payload. Это объясняет арифметику, не author intention seventh literal. Numeric IDs отсутствуют в VOC: производный loader map назначается явно. Parse failures/empty/actual filename-stem mismatch/hash mismatch 0.

Основания: [S014](SOURCES.md#s014), [S015](SOURCES.md#s015), [S016](SOURCES.md#s016). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f052"></a>

### F052 — SHEL5K: full geometry, размеры и flags

**Наша проверка.** Integer range `0<=xmin<xmax<=W`, `0<=ymin<ymax<=H`: нарушений 0; это не установление точного VOC origin/inclusive convention. Declared dimensions: 416×416 —2,192; 416×415 —2,461; 415×416 —324; 415×415 —23. Flags `(truncated,difficult)`=(0,0)69,531 и (1,0)6,047, difficult везде 0. Нельзя считать все изображения 416-square или все примеры простыми по difficult=0. Остальные 4,993 PNG hashes/decode не проверены. Source XML содержит несколько different geometry units.

Основания: [S016](SOURCES.md#s016). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f053"></a>

### F053 — SHEL5K: подтверждённые object/head/person extent

**Наша XML/paired visual проверка.** hard_hat_workers 0 helmet `[360,118,406,149]`, head_with_helmet `[360,118,406,175]`; 1000 person_with_helmet `[249,92,416,311]`, helmet `[327,91,409,147]`. W2 hard_hat_workers 1005 416×415/20 objects содержит explicit person_no_helmet у наклонившегося работника и helmeted persons; 2743 416×416/104 objects — плотная группа, partial heads/faces. Boxes человека отдельно от головы, лица, предмета. Person-state class кодирует observed attribute, но отдельного relation ID между boxes нет; correct fastening не доказан. Это targeted semantic sample, не full completeness audit.

Основания: [S014](SOURCES.md#s014), [S015](SOURCES.md#s015), [S016](SOURCES.md#s016). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f054"></a>

### F054 — SHEL5K: eight extra person — точные locators и quarantine

**Наша full XML/targeted visual проверка.** `1016.xml`: `[75,125,232,325]`,`[256,105,284,176]`; `1303.xml`: `[87,94,211,374]`,`[242,133,370,378]`; `1571.xml`: `[325,130,393,329]`,`[380,139,416,318]`; `1595.xml`: `[211,74,262,251]`; `380.xml`: `[259,33,335,286]` (все с prefix hard_hat_workers). Только 1016/1303 дополнительно просмотрены paired. В 1016 закрытая/неразличимая голова и tiny background worker; в 1303 один worker явно в жёлтой каске, другой со спорным головным убором/без ясной каски. Не map all 8→no helmet или helmeted. Сохранить `raw_person_unresolved`, quarantine из six-class loss или вручную доразметить с reason log. Семантику оставшихся четырёх objects не угадывать, originals не удалять.

Основания: [S016](SOURCES.md#s016). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f055"></a>

### F055 — SHEL5K: split/completeness/rights и роль

**Документ/неизвестно/вывод.** Completed missing labels/partial helmet-face annotation — author claims, не наш полный semantic audit. Random 4,000/1,000 описан размерами, filename membership не найден в pinned repo (только README), Mendeley manifests или XML fields. Не выдумывать official random seed. Ordinary hat/carried helmet/correct-fit protocol не установлен. Mendeley CC BY-NC 3.0, не SA; upstream photos отдельный слой. SHD после SHEL5K не independent holdout. Conditional donor раздельных helmet/head/person-state геометрий; E004/E006/E014, Q010/Q011.

Основания: [S014](SOURCES.md#s014), [S015](SOURCES.md#s015), [S016](SOURCES.md#s016). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


## D06 — CPPE-5: original COCO, HF и респираторный gap


<a id="f056"></a>

### F056 — CPPE: medical web domain и annotation protocol

**Документ/заявление.** Paper §§3–4: преимущественно Flickr, меньше Google Images, medical/non-iconic photographs; real-life не fixed CCTV. Рассматривали семь categories, respirator/shoe cover исключили из final из-за недостатка rich annotated examples; full-facepiece respirator не входил даже в исходный список. Два volunteers независимо размечают, третий согласует, verification; exhaustive claim относится к пяти final classes. Это не отсутствие всех респиратороподобных объектов внутри Mask и не GT industrial correctness/removal.

Основания: [S020](SOURCES.md#s020). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f057"></a>

### F057 — CPPE: exact release и ограниченный tar retrieval

**Наша проверка.** v0.1.0 published 14.12.2021 19:20:05 UTC, tag commit `c18d33dd33230c601c62f944df2626cd73412a79`; dataset.tar.gz metadata 238,482,705 bytes, HTTP Last-Modified 15.04.2023 отдельно. v0.2.0 published 15.04.2023 без assets. Получен Range prefix 8,388,608 bytes; stream прочитал полные train.json 690,419 bytes/test.json 30,993 bytes и два PNG. Это не полный tar manifest/MD5 validation. README MD5 `f4e043f983cff94ef82ef7d57a879212` не проверен. Old tree request по tag 404 заменён successful exact-commit tree.

Основания: [S021](SOURCES.md#s021). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f058"></a>

### F058 — CPPE: original counts, exact categories и HF shift

**Наша полная annotation проверка/документ.** Original train 1,000 image records/4,491 annotations, test 29/207, total 1,029/4,698. Это records, не full media decode. Original IDs1 Coverall,2 Face_Shield,3 Gloves,4 Goggles,5 Mask; HF0–4 в том же порядке. COCO bbox xywh pixels; HF objects{id, area, bbox, category}, image_id, width, height, без relation/track/state. Published full object counts: Coverall 1,197, Face_Shield 447, Gloves 1,343, Goggles 407, Mask 1,304 — author Table 3. Category underscores и ID shift сохранять. Нельзя присвоить всем COCO exports один zero-based map без categories.

Основания: [S020](SOURCES.md#s020), [S021](SOURCES.md#s021), [S023](SOURCES.md#s023). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f059"></a>

### F059 — CPPE: original↔HF test 29 annotation lineage

**Наша выполненная проверка.** Все 29 test image IDs, declared dimensions и category+bbox multisets совпали после `HF category+1 -> originalcategory`; join по image_id, не row order. HF test objects 207:45 Coverall/17 Face_Shield/61 Gloves/32 Goggles/52 Mask. Original PNG↔HF JPEG byte/pixel identity не проверена. Paper experiments говорит 1,029 training + another 100 testing; это не доказанный публичный 1,129 archive. Для данного artifact protocol 1,000/29; состав дополнительных 100 остаётся неизвестным Q012. Test 29 мал для редких states.

Основания: [S020](SOURCES.md#s020), [S021](SOURCES.md#s021), [S023](SOURCES.md#s023). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f060"></a>

### F060 — CPPE: source inventory и права annotations

**Наша bounded проверка/датированный author statement.** Original COCO root только images, type, annotations, categories; image fields file_name, height, width, id, нет source URL/author/license/root licenses. Exact release git tree/assets и HF не дали per-image inventory, хотя paper§3.2 его описывает. Нельзя говорить, что metadata не существует: остальная часть tar/авторы не проверены. Issue 6 comment 29.03.2022 explicitly licenses code+annotations Apache 2.0 и отделяет copyright images/Flickr conditions. W1 “Apache only code, labels unknown” уточняется этим более конкретным statement. HF license unknown относится к dataset целиком. Нужен numeric image_id→source/author/license join; media blanket clearance/weights не следует из annotation grant.

Основания: [S020](SOURCES.md#s020), [S021](SOURCES.md#s021), [S022](SOURCES.md#s022), [S023](SOURCES.md#s023). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f061"></a>

### F061 — CPPE: Mask subtype и конкретные artifact problems

**Наша targeted visual проверка.** HF1012 1280×720 Mask `[369,271,516,438]` — эластомерная полумаска с фильтрами/ремнями;1013 1920×1088 — формованная фильтрующая полумаска, goggles/coverall/gloves. Original 15.png 943×663 совпадает declared: видны три masked people, в COCO только две Mask bbox ids 114/115 — кандидат partial labels, не full error rate. Exactjoin762.png→image_id762 дал actual 2246×1498 против declared 1200×1200, COCO три Mask boxes: **quarantine coordinate/version mismatch**, не подтверждённая GT pair и не основание молча rescale. Train 762 не входит test 29 scale audit. Наш subtype по виду — не author subtype GT/сертификация/fit test.

Основания: [S021](SOURCES.md#s021), [S023](SOURCES.md#s023). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f062"></a>

### F062 — CPPE: per-class scale и практическая роль

**Наша проверка/вывод.** Только HF test 29/207, min-axis native→условный 640 q10/q50/q90: Coverall 45 `102.8/300/525.4 ->95.02/196/327.25`; Face_Shield 17 `67/122/316.6 ->40.35/88/184.02`; Gloves 61 `34/59/194 ->22/37.33/77`; Goggles 32 `24.2/40/161.7 ->22.42/29.5/58.3`; Mask 52 `24/54/210.8 ->21.45/38.78/74.12`. Test OOB0 в declared frames. Image 1023 Gloves 23×15 при 600×400→24.53×16, image 1022 Mask 25×28: не весь CPPE крупноплановый. Conditional object donor Goggles/Face_Shield/broad Mask, после subtype/rights audit. Для industrial respirator нужен новый visibility/worn/removed/incorrect/unknown/person-association слой; missing box не no_respirator. Полные width/height/area/min-axis quantiles S048, E004/E005/E008/E012/E014.

Основания: [S020](SOURCES.md#s020), [S021](SOURCES.md#s021), [S023](SOURCES.md#s023), [S048](SOURCES.md#s048). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


## D07 — Smoker Detection и surveillance smoking/calling


<a id="f063"></a>

### F063 — Smoker: payload, splits, decode и exact duplicates

**Наша проверка.** RAR65,575,997 bytes, SHA256 `2b0ef67ec714a507cff7248ef7f3d7bbdb4c4e00adc8e309cfac02cd2b6e5d18` совпал API.1,120 JPG+4 directories, Training 716(358+358), Validation 180(90+90), Testing 224(112+112). Все 1,120 Pillow load decoded 250×250; decoded RGB SHA256 exact duplicate groups 0. Filename smoking_/notsmoking_ — image class, не cigarette bbox. Near duplicates/subject/session/source overlaps не проверены; zero exact duplicates не independence.

Основания: [S025](SOURCES.md#s025), [S026](SOURCES.md#s026). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f064"></a>

### F064 — Smoker: actual confusers, домен и условия

**Документ/targeted visual.** Search queries включают cigarette/person/coughing/inhaler/phone/drinking, но queries не доказывают actual покрытие всех действий. Из 40 первых negative thumbnails: notsmoking_0091 телефон у лица,0053 телефон в руках,0120 ингалятор у рта,0041 неоднозначная рука у лица. Это наши proposed tags, не source labels или час то ты; drinking/eating не объявлять подтверждёнными здесь. Web portraits/studio/crops не factory CCTV. Нет tracks/FPS/events/zones/source person IDs. Card CC BY 4.0, upstream поисковые photo rights не восстановлены. Conditional crop-classification/hard-negative relabel donor, не operational false alerts/h.

Основания: [S025](SOURCES.md#s025), [S026](SOURCES.md#s026). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f065"></a>

### F065 — Surveillance smoking: точные единицы GT/counts

**Документ/author counts, actual dataset не получен.** Zhang et al.2023 §3.1: indoor/outdoor videos, screen every several frames, MTCNN оставляет face-containing images. Label Me behavior box охватывает лицо+связанные objects, labels smoking/calling/normal; отдельно hand/cigarette/phone boxes. Face coordinates automated MTCNN, не manual face GT. Не full-person и не temporal intervals. Train 10,461 frames:4,516 smoking/3,968 calling/1,977 normal; object 9,861 hand/6,197 cigarette/4,873 phone. Test 1,167 images from other videos/webpages. Face-visibility selection ограничивает дальнюю/верхнюю/отвёрнутую камеру. Different videos не supplied subject/camera/session holdout.

Основания: [S027](SOURCES.md#s027). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f066"></a>

### F066 — Surveillance smoking: access и event gap

**Документ/неизвестно.** Полный издательский PDF получен после HTML429; Data Availability upon reasonable request to corresponding author, public dataset URL не указан. Письмо не отправлено. Article CC BY 4.0 не лицензия неприсланных images/labels. Подготовленный запрос Q013: images/Label Me map, source-video IDs/splits, license/demo/redistribution. Smoking near flammable materials, intervals/policy и continuous safe denominator не получены; не объявлять, что visual dataset вообще не существует. E012 — собственная target annotation как независимый маршрут.

Основания: [S027](SOURCES.md#s027). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


## D08 — Önal/Dandıl: реальное заводское replay


<a id="f067"></a>

### F067 — Önal: source cameras и 4,000h против 691 clips

**Документ/author claim.** Две UNV IPC2122 CR3-PF40-A IP-камеры завода Kafaoğlu Metal Plastik Makine San. ve Tic. A.Ş., Eskişehir; съёмка 05.11–13.12.2022, около 4,000 hraw. Высота~4m, дневной свет/ночные лампы. Paper MP4/H.264/1920×1080/24 FPS — документарный контракт, actual rates ниже отличаются. Published 691 curatedclips не 4,000h доступного benchmark и не operational safe denominator.

Основания: [S030](SOURCES.md#s030), [S031](SOURCES.md#s031). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f068"></a>

### F068 — Önal: exact class map, split и manifest

**Документ/наш полный inventory metadata.** 691 MP4 entries в 16 leaf class/split folders, train 566/test 125, totaladvertised 9,999,951,582 bytes. Class 0 Safe Walkway Violation 178/32;1 Unauthorized Intervention 97/11;2 Opened Panel Cover 129/13;3 Carrying Overload with Forklift 48/8;4 Safe Walkway 50/25;5 Authorized Intervention 23/15;6 Closed Panel Cover 19/13;7 Safe Carrying 22/8 (train/test). Имена 0_tr1/0_te1 кодируют class/split/clip. Root files пуст, interval/polygon/track/multi-label sidecars/README/license files в manifest нет; unpublished GT этим не исключено. Статья допускает несколько behaviors в клипе.

Основания: [S030](SOURCES.md#s030), [S031](SOURCES.md#s031). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f069"></a>

### F069 — Önal: восемь actual samples и timing

**Наша проверка.** Все 8 H264 1920×1080, yuv 420p/yuvj 420p, selected JPEG extracted; UUID/bytes/SHA256 в SAMPLE_OBSERVATIONS. Clip / bytes / duration s / start s / displayedfps / tbn: 0_te23 /6391494/10.48/0/23/19672; 0_te9 /33474374/17.02/0/24.80/15872;4_te5 /4217183/10.44/0/25.10/19672;4_te19 /28558205/15.06/0/24.83/19864;0_tr128 /3021735/10.45/0/25.08/19672;0_tr16 /34584860/16.98/0.040008/24.80/15872;4_tr13 /3240413/10.41/0/25.06/19672;4_tr6 /42290441/20.84/0/25.05/16032.4_tr6 Bandicut Joiner, другие Cutter;20.84s уточняет paper 1–20s. ffmpeg-i без output ожидаемо пишет“atleastoneoutput…”, это не decodefailure. Для timing использовать timestamps, не hardcode 24/clip start. Full 691 decode не выполнен.

Основания: [S030](SOURCES.md#s030). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f070"></a>

### F070 — Önal: view overlap, semantics и новая event-разметка

**Документ/наше targeted visual наблюдение.** Walkway — зелёная полоса этого завода; paper отмечает 2 D projection ambiguity. Authorization/overload требуют person/equipment/block context.0_te23/0_tr128 и 4_te5/4_tr13/4_tr6 имеютсходный framing;0_te9/0_tr16 и 4_te19 другой crop/angle; оба observedviews есть train/test, это inferred View A/B, не supplied camera IDs. Некоторые клипы начинаются с уже присутствующим person: onset left-censored. В 4_tr6 Safe Walkway выбранные frames содержат person вне полосы; multipleactors/behaviors/convention возможны, не автоматическая label error. Folderclass не exhaustive per-person state. Нужны policy, polygon/footpoint, tracks, visibility, onset/end/cutflags; manual GT не author GT.

Основания: [S030](SOURCES.md#s030), [S031](SOURCES.md#s031). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f071"></a>

### F071 — Önal: права, готовые inputs и пределы

**Документ/вывод.** Card data CC BY 4.0, article CC BY-NC 4.0 — разные artifacts. Company/employee permissions сообщены авторами, не аудированы нами; additional text notices в manifest нет. Готовые 8 MP4 с hash/native timing подходятдля replay inputs video_architecture/linq_platform, но throughput здесь не измерен. Real replay/manualzonepilot приоритетнее синтетики, но 8 curatedclips не representative false alerts per operational hour. Continuous raw URL/timestamps/supplied camera-session IDs не получены, Q014/E013. Attribution/changes/DOI сохранять, не выдавать съёмку 2022 за own 2026.

Основания: [S030](SOURCES.md#s030), [S031](SOURCES.md#s031). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


## D09 — SARD: construction activity, dense raw labels и неизвестная identity schema


<a id="f072"></a>

### F072 — SARD: deposit, archive inventory и counts

**Документ/metadata и наша directory проверка.** Zenodo 19926448 v1/revision 4, publication 30.04.2026, created/modified 13.05.2026; creator Wu, Chengfeng. Card: core 748 clips/11 activities/27 HOI, supplementary 9 clips/67,098 annotated frames/1,018,232 person boxes — последние counts не пересчитаны полностью. Core ZIP8,250,845,424 bytes MD5`0302eb8d2af0722a9aa02f578cd03f89`,760 entries/748 media. Folder counts: Carry object 52, Climb ladders 47, Hammer nails 51, Install scaffolding 79, Laying bricks 104, Measure 46, Mix concrete 86, Pour concrete 96, Saw54, Shovel 49, Weld 84. Supplementary 35,002,552,520 bytes MD5`ba5586b6b5badf1987c62d84b876829c`, directory+1..9 MP4+1..9 TXT. Full archives не скачаны, source IDs по похожим filenames не установлены.

Основания: [S032](SOURCES.md#s032). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f073"></a>

### F073 — SARD: один dense label, safe parser и raw IDs

**Наша проверка одного member.** Supplementary 4.txt 5,963,836 bytes/160,824 lines, CRC при извлечении проверен. Class counts: person 49,546, vest 47,417, helmet 38,901, slogan 10,484, hopper 10,272, hook 2,446, board 1,357, scaffold 381, brick 11, ebox 9. Parser отделяет первые 2 integers, source_class, последние 4 coords и средний raw_action; переменная длина, `Unknow`/empty сохраняются. raw_id_1:43,951 unique от 1 до 60,432; raw_id_2:2,180 unique в range 1..4495 (range не count).340 raw_id_2 встречаются с разными classes:48 person/vest,174 helmet/hook/person/vest. Возможны reset/class changes/иная schema; **не validated stable object tracks**. ID2=1 у последовательных ID1 и плавные boxes поддерживают только гипотез у. Пример `2 2 helmet 1328 112 1346 127`, условно 18×15 xyxy;11 строк wear mask(O3d) не 11 independent respirator events. Parser executed, но schema не validated.

Основания: [S032](SOURCES.md#s032). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f074"></a>

### F074 — SARD: bounded media и не установленная schema

**Наша проверка/неизвестно.** Core Set/Mix concrete/27115_29941.mp4 извлечён CRC-checked:81,218 memberbytes/172,585 network bytes с headers/directory; H264480×270, duration 2.84s, start 0, displayed 23.96 fps, tbn 19168. Это **другая sequence**, не pair к 4.txt, её FPS нельзя переносить на 4.mp4. Related_identifiers schema/paper отсутствуют в Zenodo JSON; ORCIDworks пуст; exact-name bounded search не дал новую первичную schema. ZIPdirectories не содержат отдельных definitions/splits/manifests. Это не отсутствие любых unpublisheddocs. Frame-index/coordinate/ID-lifecycle overlay4.mp4 не выполнен; E011/Q015.

Основания: [S032](SOURCES.md#s032). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f075"></a>

### F075 — SARD: роль и rights

**Вывод/документ.** Deposit CC BY 4.0 не устанавливает upstream права всех web/video источников; source URL/license inventory не получен. Core допускается условным construction-action/video-plumbing donor; supplementary отложить до schema/identity/split gate. Activity не unsafe policy; нет zonepolygons/onset/authorization GT. Не главный temporal/PPE-event donor. Полный supplementary 35 GB ради одной пары не получали; предпочтителен author excerpt с FPS/frame offset. Независимость source-video groups неизвестна.

Основания: [S032](SOURCES.md#s032). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


## D10 — PhysicalAI-Event-Videos: synthetic family и условия


<a id="f076"></a>

### F076 — PhysicalAI: release units/provenance и packaging

**Документ/metadata, media не получены.** NVIDIA v1.0/revision 7f79b39 fcd 1 ef1 dc39f23f227 cd8a9480d6077 db, creation 15.06.2026.1,612 parent records/3,796 labeledchunks; documented bundled media 1,486 generated parents/2,939 clips=2,919 labeled+20 unlabeled QC-excluded. CHAD/VAD-R1 external source pointers не bundled media. Veo3/Cosmos 3 Super generation; hybrid labels, частично model-generated captions/queries, выборочная human correction, provenance Gemma 4-31b-it temperature 0.7. Train only, official val/test нет. Parent и chunk не независимые observations;20 unlabeled не negatives.

Основания: [S033](SOURCES.md#s033). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f077"></a>

### F077 — PhysicalAI: deterministic smoking family join

**Наша executed metadata проверка.** Правило ordered category mapping: is_anomaly=false→Normal; иначе первая regex по anomaly_type; default Other. Family Smoking/vaping=282 labeledchunks у 157 unique parents:143 chunks NV-VAD-v1/139 NV-VAD-v1.1, external 0, все documented bundled. Unique(dataset, video_id, chunk_index)=282. Прежний substringsmok|vap выбирал 187 parents(96/87/4), другой scope, не заменить 157. CSVfilename, dataset, chunk_count не имеет video_idcolumn; join dataset+basename(parent.video_path)→dataset+manifest.filename, каждый chunk ровно 1 match. ZIPdirectory/memberexistence/actual bytes не проверены. Reporting family не closed cigarette ontology.

Основания: [S033](SOURCES.md#s033). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f078"></a>

### F078 — PhysicalAI: temporal metadata и независимость

**Наша metadata проверка/документ.** Selected parents declared FPS24.0, start>=0, positivewindows, end<=duration+0.001s. NV-VAD-v1/video_00375: parent 8s/192 frames, chunk[0,5]s, frames 0..119, chunk_000.mp4, anomaly_type vaping smoking. NV-VAD-v1.1/video_01415: parent 7.875s/189 frames, chunk[2.875,7.875], frames 69..188, chunk_001.mp4, type person vaping visible smoke. Inclusiveend согласуется с этими examples, не общий author protocol. Windows перекрываются, card предупреждает near-duplicate generation scenarios; supplied scenario IDs не получены. Captions industrial loading dock/retail shop — source text, не visualvalidation. Media FPS/temporal boundaries не измерялись.

Основания: [S033](SOURCES.md#s033). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f079"></a>

### F079 — PhysicalAI: NVIDIA/Google условия и решение отложить

**Прочитанные документы/условный вывод.** NVIDIA textversion 21.11.2025,§1 limited/revocable/non-transferable/non-sublicensable grant solely AItraining/development;§2 authorizedusers через secure network;§3.2 запрещает transfer/distribute/embed/host/make available dataset whole or part;§3.3 notices;§3.4 не делать dataset subject to open source;§4 отсылка Trustworthy AI(отдельно не разобраны);§12.3 tradeconditions. Card“redistributable”описывает поставку NVIDIA, не право получателя перепубликовать raw/crops/labels. Google§17a/b дополнительные ограничения для Veooutput; per video Veo/Cosmosassignment не получен. Не blanket commercial clearance/weightsreview. Synthetic plumbing/augment гипотеза, не real CCTVholdout; отложить media acquisition при необязательном scope. Exact retrieval prepared: pinned 2026/train/videos.zip 7,954,992,209 bytes/chunks.zip 3,853,242,520 bytes, сначала directory/range после action review; не actual download. Q016/E010/E014.

Основания: [S033](SOURCES.md#s033), [S034](SOURCES.md#s034), [S035](SOURCES.md#s035). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


## D11 — Pictor-v3: доступная crowd часть и три задачи


<a id="f080"></a>

### F080 — Pictor: опубликованные части и три approaches

**Документ/заявление.** README774 crowd images/2,496 workers +698 web images/2,230 workers =1,472/4,726. Вторичные“784”или“1500/4700”неисправляют primary. Approach 1 worker/hat/vest objects+classifier W/WH/WV/WHV; Approach 2 wholeworker с state; Approach 3 worker crops classification. Это разные annotations/tasks на одних source images, не independent datasets. Download README обещает crowdpart; все 1,472 не получены.

Основания: [S036](SOURCES.md#s036). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f081"></a>

### F081 — Pictor: actual annotation manifests/counts/map

**Наша проверка.** Все 9 TXT: по 3 approaches×train 502/valid 120/test 152, union 774 unique basenames, split intersections 0. Format filename+tab-separated integer x 1, y1, x2, y2, class tuples. Approach 1 train 2,752/valid 707/test 726 boxes; totalsclass 0=1,646, class 1=42, class 2=2,497. Paired sample подтверждает class 2 worker/class 0 hat-head region; class 1 vest следует README/exclusion, vest positive paired sample не просмотрен. Approach 2 counts 0=873,1=1,583,2=1,3=40;**exactnumeric W/WH/WV/WHV map не известен**, не assign по READMEorder. Approach 3 all 2,497 boxes class 0. Author 2,496 против actual 2,497 worker boxes — version/protocolquestion, не исправлять по удобству. Web698 не получены этим manifest.

Основания: [S036](SOURCES.md#s036), [S037](SOURCES.md#s037). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f082"></a>

### F082 — Pictor: actual pair, права и роль

**Наша targeted проверка/неизвестно.** image_from_china(1).jpg 1221×912,583,945 bytes, SHA256`82c4d916bdcecd8dbd36a27817cc9a8e6b5cd60898a2995fe44bd1228b04d5c2`; три worker boxes совпадаютмежду approaches, Approach 2 class 1/Approach 3 class 0 каждому. Один sample не полнота 774 media/correctness/independence. В pinnedrepo нет LICENSE, annotations без notice, citationrequest не grant redistribution/deployment. Vest donor узкий(42 source boxes), conditional crowd annotation fallback после map/rights; не industrial benchmark. Q017/E005/E014.

Основания: [S036](SOURCES.md#s036), [S037](SOURCES.md#s037). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


## D12 — Construction-PPE: actual ZIP, part-local negatives


<a id="f083"></a>

### F083 — Construction-PPE: version/hash/notice и exact map

**Наша проверка/документ artifact.** Full ZIP178,415,813 bytes, SHA256`bef8dcb599aa4e9d9f5e602cb6fa7143d3c84d7f6a0ff40463d7f2a4c2632ccc`, asset updated 07.09.2025T05:14:00Z, mutabletagv 0.0.0 зафиксирован hash. Internal data.yaml 0 helmet,1 gloves,2 vest,3 boots,4 goggles,5 none,6 Person,7 no_helmet,8 no_goggle,9 no_gloves,10 no_boots. YOLO normalized cxcywh. Нет no_vest class. Internal LICENSE full AGPLv3(19.11.2007 — дата текста license, не датасета), YAMLAGPL-3.0. Это notice конкретного artifact, не upstream photo clearance/автоматический вывод AGPL→weights.

Основания: [S038](SOURCES.md#s038), [S039](SOURCES.md#s039). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f084"></a>

### F084 — Construction-PPE: pairs/orphans и полные label counts

**Наша directory/label проверка.** ZIP2,852 entries;1,416 images=1,132 train/143 val/141 test;1,426 labels=1,142 train/143 val/141 test.1,416 exact stem image-label pairs,10 train orphans: image 940(1),941(1),944(1),945(1),946(1),947(1),948(1),949(1),95(1),950(1). Неавто join к stem без(1), не plus 10 images. All1,426 label counts включая orphans: helmet 1,750/gloves 1,461/vest 1,632/boots 1,613/goggles 526/none 800/Person 2,265/no_helmet 485/no_goggle 411/no_gloves 556/no_boots 115. Этоне paired-onlytraining totals.

Основания: [S039](SOURCES.md#s039). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f085"></a>

### F085 — Construction-PPE: semantic samples и разные bbox units

**Наша targeted visual проверка.** Первая pair каждого none/Person/no_*дала 4 unique images/6 panels. test/image 1.jpeg Personwhole/visible body и отдельные gear; image 1120.jpgportrait без industrial PPE: no_helmet head, no_goggleeyeregion, none торс, Person body; при этом обычные очки видны, no_goggle не“любые очки отсутствуют”. image 1132.jpgno_gloves кистиребёнка; image 1145.jpgno_boots области стоп/обуви в спортивной сцене. No_* — part-local, не whole person compliance boxes. None по одному torso example не переименовывать no_vest. Web/sport/portrait domain не factory CCTV. Exhaustive protocol/occlusion/visibility/source URLs не получены.

Основания: [S039](SOURCES.md#s039). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f086"></a>

### F086 — Construction-PPE: роль и подготовка

**Вывод/предложено.** Доступный conditional object/part-negative fallback при gloves/boots/gogglesneeds после кейса. Filter manifest к 1,416 pairs, source units сохранить, association Person→item отдельно с uncertainty, unknown/ignore дляневидимого. Orphans в quarantine, upstream rights/none protocol Q018; E002/E003/E005/E014. Full ZIP/structuralcounts неполная semantic validation, не independent holdout.

Основания: [S038](SOURCES.md#s038), [S039](SOURCES.md#s039). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


## D13 — адресные дополнительные источники


<a id="f087"></a>

### F087 — Harness: article-to-tree-to-XML chain

**Документ/наша tree/XML проверка.** Xu/Huang/Huang 2023:3,300 images=2,000 clothes+1,300 harness; transformed helmet data Wang+surveillance+web, split 16:4:5(author protocol). Personwhole body, harness/clothes chest region, reflective vest confusers. Pinnedtree 6,600 paths=3,300 XML+3,299.jpg+1.JPG, не full media decode. Actual Dangerous 0001.xml 400×486 clothes[109,63,266,166]/person[77,11,342,352]; Safety Harness 0001.xml 1920×1080 harness[608,183,908,613]/person[403,1,950,1078], truncated 1. Textlabels, no numeric IDs/relation ID. Images не просмотрены. Chestharness не securedanchor/hook GT; Dangerous filename не event. Tree без LICENSE/split manifests, rights/upstream exact matches unknown. Conditionaldonor лишьпринужном scenario, Q019.

Основания: [S040](SOURCES.md#s040). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f088"></a>

### F088 — Site Object Detection SODA: exact identity и published geometry

**Документ/author counts.** Duanetal.2022, не SODA-D/A ине SODA10M.19,846 JPG/286,201 boxes/15 categories: person, helmet, vest, board, wood, rebar, brick, scaffold, handcart, cutter, ebox, hopper, hook, fence, slogan.Numeric IDs не установлены без XML. UAV/handheld/hookmonitoring реальных с трое к;21,863 initial→19,846 cleaned,86%1920×1080. Every 30 frames не FPS; manualdedup не independence guarantee. Random 90/10=17,861 train/1,985 test. Fence не hazardpolygon, slogan не policy. Blurred/ambiguousimages удалялись, partially occluded/inconvenient objects моглиопускаться; positive filtered data не continuous safe negatives.

Основания: [S041](SOURCES.md#s041). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f089"></a>

### F089 — SODA: access/rights и стоимость неизвестного

**Наша access проверка/неизвестно.** Direct VOCv1.zip Range GET23.10.2026 дал 403 Aliyun OSS, архив не получен, bytes/MD5/internal LICENSE/map не проверены. Это один failedroute, не доказательство общей закрытости. “Open-source”в paper не явное разрешение всех media actions. Отложитьдо construction-specificneed; точный author fallback/notice Q019, E001/E014. Не prioritise общий повтор поиска в ущерб real CCTV/target data.

Основания: [S041](SOURCES.md#s041). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


## D14 — generic person/head/pose/tracking: ограниченные роли


<a id="f090"></a>

### F090 — COCO: reused images, схема и права слоёв

**Прочитанная official documentation, full payload не получен.**2017 train 118K/18 GB, val 5K/1 GB, test 41K/6 GB, annotations 241 MB — округлённые сайтовые числа, ненаш count.2017 переиспользует 2014 images с 118K/5 Ksplit;2020 новых detection/keypointdata неприбавляет. Image fields id, width, height, file_name, license, flickr_url, coco_url, date_captured; camera/session IDs не заданы. COCO xywh 0 indexed, categories читать из actual JSON, не 80-listlibrary; exact category IDs в этой ветке не получены. Web site/annotations CC BY 4.0, photos Flickr/per-image conditions, не blanket BYmedia.

Основания: [S042](SOURCES.md#s042). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f091"></a>

### F091 — COCO pose и Crowd Human: visibility/ignore semantics

**Документ.** COCO keypoints(x, y, v), v0 not labeled/v1 labeled not visible/v2 visible; small/crowd может num_keypoints 0, pose для большинства medium/large/noncrowd, не allpersons. Source claimed>200 Kimages/250 Kpersonkeypoints, public trainval>150 Kpeople/1.7 Mlabeledpoints не local count. Crowd Human Shao 2018 claims 15,000 train/4,370 val/5,000 test,470 Kpersonstrainval/~23 per image. ODGTJSONlines ID, gtboxes{tag, vbox, fbox, hbox, extra, head_attr}, xywhvisible/full/head, ignore/occ/unsure. **tag=mask — person-like/crowd/reflection ignore region, не medical mask**. PPEstate не размечен. ODGT/media не получены. Noncommercial research/education, image redistribution prohibited по official page; revision/source photo groups unknown.

Основания: [S042](SOURCES.md#s042), [S043](SOURCES.md#s043). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f092"></a>

### F092 — MOT17: repeats, actual GT hashes и время

**Документ/наша labels проверка.**21 train/21 test entries=7 base videos×3 DPM/FRCNN/SDP каждый split,14 base videos всего, не 42 independent scenes. MOT16 sequencesreuse с new GT. Actual 10,107,022-byte Labels ZIP/105 entries,21 train GTfiles образуют 7 SHA256 groups по 3 variants; это annotation content duplicates, не image pixel comparison. Sample MOT17-01-DPMseqinfo 30 FPS/450 frames/1920×1080, GT9 numericcolumns; classfiltering не выдумывать, прочитанный instructions route 410. Current online web application/evaluationclosed, resultsarchive 16.04.2026; local tracking regression вместообещания submission. Conditions CC BY-NC-SA 3.0+possible third party. Media не получены.

Основания: [S044](SOURCES.md#s044). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f093"></a>

### F093 — Generic datasets не создают PPE negatives

**Вывод/предложено.** COCO/Crowd Human/MOT подходятдля person/ROI/occlusion/pose/tracker regression, не helmet/respirator/events quality. Preserveiscrowd, ignore/unsure, MOTclassfilters. Unlabeled PPE не background для PPEloss; для negative нужна verified visibility и verified absence нужного предмета. Все MOT detector variants одной base group держать вместе; track IDswitch/fragmentation fixture не PPE event benchmark. E005/E006/E007/E009.

Основания: [S042](SOURCES.md#s042), [S043](SOURCES.md#s043), [S044](SOURCES.md#s044). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f094"></a>

### F094 — Mask ed Face-Net: synthetic medical position, не industrial fit

**Документ, media не получены.** Current README133,783 images=67,049 CMFD+66,734 IMFD,1024×1024, One Drive~19 GBeachpart/mirrors; oldabstract 137,016 другое заявленное состояние. Deformed mask overlay на FFHQfaces, correct/incorrect face-level position, не industrial respirator object/fit-test/removalintime. Filename связан FFHQmetadata. Assembly BY-NC-SA4.0, FFHQsource images разные BY2.0/BY-NC2.0/CC0/Public Domain Mark/US Government conditions. Commit неприкреплён(403 API). Conditional medical face-crop donor, не CCTVholdout.

Основания: [S024](SOURCES.md#s024). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f095"></a>

### F095 — HMDB51, SED и CMA: задачи и доступ не взаимозаменяемы

**Документ, full media не получены.** HMDB current official 6,849 clips/51 classes, smoke/eat/drink/chew/talk, unstabilized/stabilized и 3 splitsets; movie/web domain, clip class не puff/onset/cigarette visibility/policy. Page CC BY 4.0, exact media revision нужен при download. SED11 subjects/20 sessions/2.69h; SED-FL7 subjects/10 alldaysessions/78.3h,3 sharedsubjects; publicpickle 6 Do Fsmartwatch, smartphonevideo использовали для GT, публичный visualpayload не подтверждён — исключить из video training. CMAREADME1,595 clips/7 actions(невторичные 2,000), Baiducodez 7a2, actual 7 names IDs не установлены; research-only/no-commercial data при MITrepo/дополнительном READMEscope. Это адресные auxiliary branches, не factory event holdout.

Основания: [S028](SOURCES.md#s028), [S029](SOURCES.md#s029), [S045](SOURCES.md#s045). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


<a id="f096"></a>

### F096 — Foundation Pit v2: отложенная temporal зацепка

**Документ/неизвестно.** Card v 2 dated 07.11.2025 добавляет video sequences к image dataset, CC BY 4.0. FPS/counts/identities/polygons/event annotations не установлены. Один неверно предположенный API route 404 не отсутствие данных. При excavation-specific case проверить artifact/GT, иначе отложить; не ready temporal risk dataset из одной формулировки карточки.

Основания: [S046](SOURCES.md#s046). Точные первичные локаторы и границы доступа — записи SOURCES; дополнительные execution logs — соответствующая W2 card.


## Сводные mapping, lineage, роли и приём organizer data


<a id="f097"></a>

### F097 — Предварительная карта понятий и единиц

**Наш synthesis/предложено; final target IDs ещё нет.** Сохранять `semantic_unit` отдельно от concept/state. SH17 helmet — предмет с потерянным wearing state; SHWD hat — голова в каске; SHEL5K helmet/head_with_helmet/person_with_helmet — соответственно предмет, голова, человек. SFCHD head и SHEL5K head — source candidates головы без каски; SH17 head — общая часть тела. Эти labels нельзя объединить в один no_helmet box class. CPPE Goggles и SH17 glasses требуют проверки safety/vision; broad Mask не равен exact industrial respirator, Face_Shield не респиратор. Construction no_* — части тела, Pictor Approach2 — worker state, Smoker — image class, Önal — clip class, SARD — raw action, PhysicalAI — reporting family. Relations `exact/conditional/partial/incompatible/not_annotated` назначаются после определения цели.

Основания: S002/S010/S013/S016/S018/S021/S023/S027/S030/S032/S033/S037/S039, exact maps в соответствующих карточках.

<a id="f098"></a>

### F098 — Coverage, visibility, wearing и policy — отдельные поля

**Наш вывод/предложено.** `annotation_status`: verified_present/verified_absent/not_annotated/out_of_scope/ambiguous. `visibility`: visible/occluded/too_small/blurred/unreviewed. `observed_state`: worn/unworn/adjusting/incorrect/unknown; incorrect допустим только по целевой инструкции. Невидимость не означает absence; off object не person absence; person state не нарушение без policy. Отдельно нужны coverage_by_dataset_class, source box unit, relation evidence и event fields. Для неаннотированных классов выбрать dataset heads/loss masks, ручную доразметку, локально проверенные crops либо exclusion. Реализация loss относится к model_stack/training_strategy и здесь не разработана.

Основания: S005/S006/S016/S018/S020/S023/S039; F002/F020/F025/F053/F061/F085.

<a id="f099"></a>

### F099 — Lineage и известные зависимости

**Документ/наш synthesis.** SCUT-HEAD частично входит в SHWD; GDUT-HWD и SHWD — родители CHV; SHD5000 — родитель SHEL5K. Raw SH17 связан с released flat-map, но полная cleanup сверка не выполнена. CPPE original test29 и HF test29 имеют проверенную annotation lineage. Pictor approaches/crops используют те же crowd images. MOT17 переиспользует MOT16 и три detector variants одной базы; COCO2017 переиспользует COCO2014 images. PhysicalAI chunks происходят из parents и могут перекрываться. SHD и SHWD — разные имена; их точное пересечение неизвестно. Общий web источник SH17/Pictor/CPPE создаёт риск, конкретные дубли этим не доказаны. Harness paper называет transformed Wang helmet data, точный version crosswalk не получен. Parent/derivative не независимые holdouts; отсутствие crosswalk не доказательство независимости. E006/E007.

Основания: S001/S009/S012/S014/S020/S023/S033/S036/S040/S042/S044.

<a id="f100"></a>

### F100 — Порядок ролей и условные маршруты объединения

**Наше решение до полного кейса.** Сначала organizer triage и locked target holdout. Для внешней подготовки приоритетны SFCHD intersection 12,372/50,552 для factory adaptation/development, восемь Önal inputs для real replay/manual events и exact SH17 v1 для broad object donors. SHEL5K даёт несколько геометрий, SHWD — головы; CHV — vest/color при надобности. CPPE нужен после subtype/per-image audit, Smoker — для crops/confusers. Construction/Pictor — условные fallback. SARD supplementary отложен до schema; PhysicalAI — optional после реального GT. SODA/harness/Foundation Pit нужны только при адресном сценарии.

Объединение требует одинаковой box unit либо явно новой задачи, обратимой class map, установленной полноты или partial-label стратегии, разрешённых действий, source groups и журнала исправлений. Calibration/threshold tuning выполняются на development; единственный independent test не используется для калибровки. Основания: F005–F096, S001/S010/S013/S016/S018/S019/S021/S026/S030/S032/S033/S037/S039.

<a id="f101"></a>

### F101 — Manifest: достаточные поля и обратимость

**Предложенная schema, не существующие source fields.** В dataset registry хранить source_family/dataset_id, revision/commit/deposit_version, publication_date отдельно от accessed_at, download_url/file_id, archive bytes/hash и происхождение expected checksum, license_layer/notice_hash/action_evidence. Для каждого original: original_path/image_id/source_url, media_hash/decoded_pixel_hash/dimensions, annotation_path/hash, nullable source_class_id и source_literal, source_bbox/coordinate_convention/semantic_unit, split_original, nullable group_id_original, отдельно group_id_inferred/algorithm/evidence. Далее coverage/visibility/state/nullable relations, mapping_version/nullable target_class, transform_history с scale/padding/crop/orientation/clipping, parent/crop/augmentation chain, usage_role/inclusion_reason/quarantine_reason.

Source originals не перезаписывать. Derived records должны восстанавливать исходные classes/boxes. Hash файла и canonical decoded RGB hash различаются; процедуру orientation/colour normalization записать. Если camera/session IDs не даны, они остаются null. Основания: S002/S015/S018/S021/S033/S037/S039; E018.

<a id="f102"></a>

### F102 — Organizer data: готовая процедура приёма

**Предложено; данные ещё не поступили.**

1. Зафиксировать полный кейс, allowed data actions, определения objects/wearing/events, метрики и обязательные LinQ constraints.
2. Создать immutable inventory/hashes; проверить decode, timing, schema, pairs и geometry без предположений об объёме или качестве.
3. Сопоставить exact source IDs/literals, box units, coverage, visibility, relations, zone/event semantics с предварительной картой. Неизвестное сохранить.
4. До внешней смеси выделить locked target holdout по реально поставленным либо документированно восстановленным camera/site/session/person/time groups. Official test не использовать для tuning.
5. На development измерить per-class scale/occlusion/light/confusers, сравнить donors с target и проверить overlap с внешними источниками.
6. Закрыть целевые пробелы малой двойной доразметкой; сохранить agreement/adjudication, policy/onset uncertainty и cut flags.
7. Выбрать donor/partial-loss/conversion после этих проверок, сохранить versioned manifest.
8. Representative calibration samples и thresholds брать из development. Export/LinQ runtime и latency проверяют соседние темы; здесь эти проверки не выполнены.

Основания: F001–F004/F097–F101; S001/S018/S020/S030/S048; E015/E018.

## Приложение к F041 — все 132 dataset/class groups scale audit

**Наша выполненная проверка E031/S048.** Значения ниже извлечены из сохранённого QUANTILES.csv, без нового измерения. Native и условный640 min-axis: q10/q50/q90 в px; W/H — медианы width/height после640; A — медиана area640 в px². Округление отображения до двух десятичных знаков; все точные квантили0/.1/.25/.5/.75/.9/1 для native/640 width/height/area/min-axis и area_fraction, input hashes и histograms сохранены в [QUANTILES.csv](_WORK/MATERIALS/W2-13/QUANTILES.csv) и [SCALE_SUMMARY.json](_WORK/MATERIALS/W2-13/SCALE_SUMMARY.json). Raw all и raw release-member scopes перекрываются, их нельзя складывать. Rare raw categories с1–10 instances не получают устойчивых population quantiles от этой таблицы. Demographic raw literals сохранены только для provenance и не входят в продуктовую таксономию.

| Scope | Literal | n objects | images | Native min-axis q10/q50/q90 | 640 min-axis q10/q50/q90 | W640/H640/A640 q50 |
|---|---|---:|---:|---|---|---|
|`CPPE_HF_test29`|`Coverall`|45|25|102.8/300/525.4|95.02/196/327.25|198.4/330.4/60054.4|
|`CPPE_HF_test29`|`Face_Shield`|17|14|67/122/316.6|40.35/88/184.02|92.8/112/9856|
|`CPPE_HF_test29`|`Gloves`|61|22|34/59/194|22/37.33/77|44/44.8/2017.39|
|`CPPE_HF_test29`|`Goggles`|32|18|24.2/40/161.7|22.42/29.5/58.3|55.31/29.5/1489.59|
|`CPPE_HF_test29`|`Mask`|52|26|24/54/210.8|21.45/38.78/74.12|45.88/39.47/1961.19|
|`SFCHD_allCOCO`|`blur_clothes`|1324|1149|9/26/53.51|4.5/12.5/25.37|12.5/16/198.17|
|`SFCHD_allCOCO`|`blur_head`|1134|1004|4/14/24|2/6.5/12|6.5/7/46.71|
|`SFCHD_allCOCO`|`head`|1200|879|12/21.06/39|4.21/9/18.5|9.5/9.95/94.47|
|`SFCHD_allCOCO`|`helmet`|14298|10872|12/27/58|6/13/29|13.5/15/200|
|`SFCHD_allCOCO`|`person`|17010|12365|27/58/129|13/28/63.02|28/66.5/1893.38|
|`SFCHD_allCOCO`|`safety_clothes`|14813|11187|24/49/105|11.32/23.5/52.5|24.05/30/731.25|
|`SFCHD_allCOCO`|`self_clothes`|780|712|28/53/100.1|11.97/26/50.05|26/33.5/894.25|
|`SH17_raw_all8102`|`asian-children`|53|41|76.6/911/2418|13.28/103.16/278.24|109.68/217.02/20557.54|
|`SH17_raw_all8102`|`asian-female`|1211|922|557/1639/3065|57.75/183.32/342.65|185.07/293.59/55060.16|
|`SH17_raw_all8102`|`asian-male`|930|679|323.7/1387.5/2825.1|42.13/160.97/335.75|165.16/259.15/42699.6|
|`SH17_raw_all8102`|`black-children`|6|5|450.5/1966.5/3646.5|68/201.69/436.76|201.69/335.08/71631.67|
|`SH17_raw_all8102`|`black-female`|775|707|835.4/2030/3515.4|102.5/224.86/388.65|226.33/355.14/81548.32|
|`SH17_raw_all8102`|`black-male`|1107|1002|876.4/2070/3481.6|96.98/232.13/380.22|239/348.21/81731.58|
|`SH17_raw_all8102`|`brown-children`|12|8|644.3/936.5/1395.1|72.43/106.68/248.02|115.05/227.54/24759.56|
|`SH17_raw_all8102`|`brown-female`|250|227|552.9/1886/3481.9|57.15/185.88/361.02|187.66/306.24/56615.69|
|`SH17_raw_all8102`|`brown-male`|605|454|270.2/1170/2850.8|34.09/141.04/315.34|142.19/241.39/34266.63|
|`SH17_raw_all8102`|`ear`|7730|4884|30/92/206|3.69/10.44/22.91|10.47/20.43/216.7|
|`SH17_raw_all8102`|`ear-mufs-off`|107|84|207.6/377/898.4|21.84/44/92.25|70.93/50.53/2894.39|
|`SH17_raw_all8102`|`ear-mufs-on`|211|148|141/530/1168|15.85/57.24/129.07|63.44/69.55/4740.85|
|`SH17_raw_all8102`|`face`|8950|5646|117/420/864|14.29/47.97/96.96|49.01/61.47/3017.09|
|`SH17_raw_all8102`|`face-guard-off`|11|11|170/382/685|17.55/54.43/99.28|88.8/54.43/4833.09|
|`SH17_raw_all8102`|`face-guard-on`|123|118|236.6/614/1374.2|29.68/76.8/159.33|88.53/96.64/8349.18|
|`SH17_raw_all8102`|`face-mask-medical-off`|35|35|47/225/708.4|5.27/26.56/64.42|26.56/38.4/1033.08|
|`SH17_raw_all8102`|`face-mask-medical-on`|635|370|58.4/301/762.6|7.38/33.81/86.2|39.18/36.62/1473.47|
|`SH17_raw_all8102`|`foot`|759|347|43/156/374.2|5.34/17.17/40.27|23.36/20.39/468.91|
|`SH17_raw_all8102`|`fork-lift`|14|9|187/792.5/3138.3|21.87/76.2/290.95|77.32/107.41/8133.7|
|`SH17_raw_all8102`|`glasses-safety-off`|52|49|140.9/285/793.2|15.14/30.34/75.31|42.9/40.76/1526.88|
|`SH17_raw_all8102`|`glasses-safety-on`|373|314|81/298/613.4|10.33/37.04/76.28|63.14/39.25/2615.47|
|`SH17_raw_all8102`|`glasses-vision-off`|163|138|102/268/775.8|11.89/29.69/76.81|46/36.7/1689.37|
|`SH17_raw_all8102`|`glasses-vision-on`|1357|1120|81.6/229/471.4|9.71/24.75/51.24|48.89/25.39/1277.29|
|`SH17_raw_all8102`|`gloves-off`|121|83|66/196/752|7.25/20.98/95.56|25.92/33.1/871.63|
|`SH17_raw_all8102`|`gloves-on`|2669|1274|56/263/942.4|7.24/30.67/102.46|35.63/36.44/1307.03|
|`SH17_raw_all8102`|`halmet-off-black`|1|1|237/237/237|25.21/25.21/25.21|40.43/25.21/1019.24|
|`SH17_raw_all8102`|`halmet-off-blue`|4|3|142.5/255.5/577.1|16.38/38.38/65.93|46.25/42.63/2648.5|
|`SH17_raw_all8102`|`halmet-off-orange`|9|6|23.8/98/433.6|1.86/12.47/48.4|15.8/12.47/191.19|
|`SH17_raw_all8102`|`halmet-off-red`|5|4|15.8/23/252.8|1.23/2.19/27.91|2.19/2.19/4.8|
|`SH17_raw_all8102`|`halmet-off-white`|5|5|156.6/463/1059.4|27.35/74.08/128.97|97.12/74.08/10022.78|
|`SH17_raw_all8102`|`halmet-off-yellow`|10|8|105.9/607.5/1264.7|9.1/51.85/120.9|56.32/57.68/5579.89|
|`SH17_raw_all8102`|`halmet-on-black`|27|13|34.6/178/486.6|7.36/23.36/51.77|29.68/23.36/605.49|
|`SH17_raw_all8102`|`halmet-on-blue`|82|46|22.9/117.5/366.8|2.43/14.99/53.19|20.07/15.36/275.76|
|`SH17_raw_all8102`|`halmet-on-green`|3|3|55/83/236.6|8.73/13.18/37.81|14.29/13.18/188.3|
|`SH17_raw_all8102`|`halmet-on-grey`|10|7|37.7/66/115.8|5.32/10.76/19.1|12.88/10.76/141.96|
|`SH17_raw_all8102`|`halmet-on-orange`|95|60|50.2/150/583.8|5.77/19.65/72.25|24.56/19.65/598.55|
|`SH17_raw_all8102`|`halmet-on-pink`|1|1|55/55/55|10.16/10.16/10.16|10.16/16.07/163.34|
|`SH17_raw_all8102`|`halmet-on-red`|82|55|36.9/198.5/551.3|4.95/27.7/68.17|29.47/30.67/847.27|
|`SH17_raw_all8102`|`halmet-on-white`|312|203|49.1/197/842.9|5.67/26.94/94.22|33.83/27.87/1028.46|
|`SH17_raw_all8102`|`halmet-on-yellow`|276|170|39.5/203.5/959.5|5.29/25.18/100.26|36.43/26.36/903.67|
|`SH17_raw_all8102`|`hands`|15850|6455|94/317/797|11.28/36.2/91.09|44.57/40.89/1821.99|
|`SH17_raw_all8102`|`head`|11985|6495|77/550/1196|9.89/62.82/132.28|63.79/79.43/5108.36|
|`SH17_raw_all8102`|`helmet`|4|3|204.1/318.5/626.8|27.06/44.13/73.5|61.31/50.49/3217.43|
|`SH17_raw_all8102`|`helmet-yellow-on`|1|1|45/45/45|6.02/6.02/6.02|7.22/6.02/43.45|
|`SH17_raw_all8102`|`medical-suit-on`|157|114|502.8/1811/2628.2|78/206.1/306.69|250/253.96/64530.72|
|`SH17_raw_all8102`|`other-shoes-off`|101|29|79/225/658|7.89/21.88/57.34|24.39/33.95/817.78|
|`SH17_raw_all8102`|`other-shoes-on`|3287|1178|41/177/421|5.22/20.37/45.67|27.5/23.24/654.81|
|`SH17_raw_all8102`|`person`|4351|2314|65/657/3097|8.44/81.83/353.63|83.31/152.72/13753.6|
|`SH17_raw_all8102`|`safety-shoes-off`|22|8|26.2/240/422.8|5.46/33.93/69.45|46.51/42.27/1595.19|
|`SH17_raw_all8102`|`safety-shoes-on`|1150|409|42/154.5/403.2|5.71/19/47.13|23.21/23.29/572.69|
|`SH17_raw_all8102`|`safety-suit-off`|6|3|140.5/224.5/1542|19.44/31.06/213.22|31.61/45.45/1228.91|
|`SH17_raw_all8102`|`safety-suit-on`|234|139|187.6/540.5/2128.4|21.87/75.34/245.41|76.64/143.52/10249.03|
|`SH17_raw_all8102`|`safety-vest-off`|5|4|55/256/697.8|11.7/42.27/109.57|42.27/58.78/2484.75|
|`SH17_raw_all8102`|`safety-vest-on`|525|212|35/222/1131.4|3.86/32.22/151.26|33.35/43.19/1485.49|
|`SH17_raw_all8102`|`tools`|5|4|871.8/1144/1633.6|96.87/127.11/181.51|226.44/127.11/28783.6|
|`SH17_raw_all8102`|`tools-off`|2903|1006|45.2/183/1027.2|5.11/21.19/125.43|33.28/43.02/1221.26|
|`SH17_raw_all8102`|`tools-on`|1739|1503|119/582/1896.2|16.22/67.58/229.15|90.41/101.13/8892.5|
|`SH17_raw_all8102`|`white-children`|39|34|451.2/1560/2628|53.86/183.19/339.17|183.19/320.62/57626.74|
|`SH17_raw_all8102`|`white-female`|2039|1745|766.4/1891/3292.6|89.22/217.44/364.5|221.76/339.24/74816.23|
|`SH17_raw_all8102`|`white-male`|2424|2037|546.9/1725/3180.4|65.46/198.04/354.41|200.89/318.06/64204.59|
|`SH17_raw_release_members`|`asian-children`|53|41|76.6/911/2418|13.28/103.16/278.24|109.68/217.02/20557.54|
|`SH17_raw_release_members`|`asian-female`|1211|922|557/1639/3065|57.75/183.32/342.65|185.07/293.59/55060.16|
|`SH17_raw_release_members`|`asian-male`|930|679|323.7/1387.5/2825.1|42.13/160.97/335.75|165.16/259.15/42699.6|
|`SH17_raw_release_members`|`black-children`|6|5|450.5/1966.5/3646.5|68/201.69/436.76|201.69/335.08/71631.67|
|`SH17_raw_release_members`|`black-female`|775|707|835.4/2030/3515.4|102.5/224.86/388.65|226.33/355.14/81548.32|
|`SH17_raw_release_members`|`black-male`|1107|1002|876.4/2070/3481.6|96.98/232.13/380.22|239/348.21/81731.58|
|`SH17_raw_release_members`|`brown-children`|12|8|644.3/936.5/1395.1|72.43/106.68/248.02|115.05/227.54/24759.56|
|`SH17_raw_release_members`|`brown-female`|250|227|552.9/1886/3481.9|57.15/185.88/361.02|187.66/306.24/56615.69|
|`SH17_raw_release_members`|`brown-male`|605|454|270.2/1170/2850.8|34.09/141.04/315.34|142.19/241.39/34266.63|
|`SH17_raw_release_members`|`ear`|7730|4884|30/92/206|3.69/10.44/22.91|10.47/20.43/216.7|
|`SH17_raw_release_members`|`ear-mufs-off`|107|84|207.6/377/898.4|21.84/44/92.25|70.93/50.53/2894.39|
|`SH17_raw_release_members`|`ear-mufs-on`|211|148|141/530/1168|15.85/57.24/129.07|63.44/69.55/4740.85|
|`SH17_raw_release_members`|`face`|8950|5646|117/420/864|14.29/47.97/96.96|49.01/61.47/3017.09|
|`SH17_raw_release_members`|`face-guard-off`|11|11|170/382/685|17.55/54.43/99.28|88.8/54.43/4833.09|
|`SH17_raw_release_members`|`face-guard-on`|123|118|236.6/614/1374.2|29.68/76.8/159.33|88.53/96.64/8349.18|
|`SH17_raw_release_members`|`face-mask-medical-off`|35|35|47/225/708.4|5.27/26.56/64.42|26.56/38.4/1033.08|
|`SH17_raw_release_members`|`face-mask-medical-on`|635|370|58.4/301/762.6|7.38/33.81/86.2|39.18/36.62/1473.47|
|`SH17_raw_release_members`|`foot`|759|347|43/156/374.2|5.34/17.17/40.27|23.36/20.39/468.91|
|`SH17_raw_release_members`|`fork-lift`|13|8|185/814/3147.2|21.64/70.66/293.85|70.66/133.07/9402.39|
|`SH17_raw_release_members`|`glasses-safety-off`|52|49|140.9/285/793.2|15.14/30.34/75.31|42.9/40.76/1526.88|
|`SH17_raw_release_members`|`glasses-safety-on`|373|314|81/298/613.4|10.33/37.04/76.28|63.14/39.25/2615.47|
|`SH17_raw_release_members`|`glasses-vision-off`|163|138|102/268/775.8|11.89/29.69/76.81|46/36.7/1689.37|
|`SH17_raw_release_members`|`glasses-vision-on`|1357|1120|81.6/229/471.4|9.71/24.75/51.24|48.89/25.39/1277.29|
|`SH17_raw_release_members`|`gloves-off`|121|83|66/196/752|7.25/20.98/95.56|25.92/33.1/871.63|
|`SH17_raw_release_members`|`gloves-on`|2669|1274|56/263/942.4|7.24/30.67/102.46|35.63/36.44/1307.03|
|`SH17_raw_release_members`|`halmet-off-black`|1|1|237/237/237|25.21/25.21/25.21|40.43/25.21/1019.24|
|`SH17_raw_release_members`|`halmet-off-blue`|4|3|142.5/255.5/577.1|16.38/38.38/65.93|46.25/42.63/2648.5|
|`SH17_raw_release_members`|`halmet-off-orange`|9|6|23.8/98/433.6|1.86/12.47/48.4|15.8/12.47/191.19|
|`SH17_raw_release_members`|`halmet-off-red`|5|4|15.8/23/252.8|1.23/2.19/27.91|2.19/2.19/4.8|
|`SH17_raw_release_members`|`halmet-off-white`|5|5|156.6/463/1059.4|27.35/74.08/128.97|97.12/74.08/10022.78|
|`SH17_raw_release_members`|`halmet-off-yellow`|10|8|105.9/607.5/1264.7|9.1/51.85/120.9|56.32/57.68/5579.89|
|`SH17_raw_release_members`|`halmet-on-black`|27|13|34.6/178/486.6|7.36/23.36/51.77|29.68/23.36/605.49|
|`SH17_raw_release_members`|`halmet-on-blue`|82|46|22.9/117.5/366.8|2.43/14.99/53.19|20.07/15.36/275.76|
|`SH17_raw_release_members`|`halmet-on-green`|3|3|55/83/236.6|8.73/13.18/37.81|14.29/13.18/188.3|
|`SH17_raw_release_members`|`halmet-on-grey`|10|7|37.7/66/115.8|5.32/10.76/19.1|12.88/10.76/141.96|
|`SH17_raw_release_members`|`halmet-on-orange`|95|60|50.2/150/583.8|5.77/19.65/72.25|24.56/19.65/598.55|
|`SH17_raw_release_members`|`halmet-on-pink`|1|1|55/55/55|10.16/10.16/10.16|10.16/16.07/163.34|
|`SH17_raw_release_members`|`halmet-on-red`|82|55|36.9/198.5/551.3|4.95/27.7/68.17|29.47/30.67/847.27|
|`SH17_raw_release_members`|`halmet-on-white`|312|203|49.1/197/842.9|5.67/26.94/94.22|33.83/27.87/1028.46|
|`SH17_raw_release_members`|`halmet-on-yellow`|276|170|39.5/203.5/959.5|5.29/25.18/100.26|36.43/26.36/903.67|
|`SH17_raw_release_members`|`hands`|15850|6455|94/317/797|11.28/36.2/91.09|44.57/40.89/1821.99|
|`SH17_raw_release_members`|`head`|11985|6495|77/550/1196|9.89/62.82/132.28|63.79/79.43/5108.36|
|`SH17_raw_release_members`|`helmet`|4|3|204.1/318.5/626.8|27.06/44.13/73.5|61.31/50.49/3217.43|
|`SH17_raw_release_members`|`helmet-yellow-on`|1|1|45/45/45|6.02/6.02/6.02|7.22/6.02/43.45|
|`SH17_raw_release_members`|`medical-suit-on`|157|114|502.8/1811/2628.2|78/206.1/306.69|250/253.96/64530.72|
|`SH17_raw_release_members`|`other-shoes-off`|101|29|79/225/658|7.89/21.88/57.34|24.39/33.95/817.78|
|`SH17_raw_release_members`|`other-shoes-on`|3287|1178|41/177/421|5.22/20.37/45.67|27.5/23.24/654.81|
|`SH17_raw_release_members`|`person`|4351|2314|65/657/3097|8.44/81.83/353.63|83.31/152.72/13753.6|
|`SH17_raw_release_members`|`safety-shoes-off`|22|8|26.2/240/422.8|5.46/33.93/69.45|46.51/42.27/1595.19|
|`SH17_raw_release_members`|`safety-shoes-on`|1150|409|42/154.5/403.2|5.71/19/47.13|23.21/23.29/572.69|
|`SH17_raw_release_members`|`safety-suit-off`|6|3|140.5/224.5/1542|19.44/31.06/213.22|31.61/45.45/1228.91|
|`SH17_raw_release_members`|`safety-suit-on`|234|139|187.6/540.5/2128.4|21.87/75.34/245.41|76.64/143.52/10249.03|
|`SH17_raw_release_members`|`safety-vest-off`|5|4|55/256/697.8|11.7/42.27/109.57|42.27/58.78/2484.75|
|`SH17_raw_release_members`|`safety-vest-on`|525|212|35/222/1131.4|3.86/32.22/151.26|33.35/43.19/1485.49|
|`SH17_raw_release_members`|`tools`|5|4|871.8/1144/1633.6|96.87/127.11/181.51|226.44/127.11/28783.6|
|`SH17_raw_release_members`|`tools-off`|2903|1006|45.2/183/1027.2|5.11/21.19/125.43|33.28/43.02/1221.26|
|`SH17_raw_release_members`|`tools-on`|1739|1503|119/582/1896.2|16.22/67.58/229.15|90.41/101.13/8892.5|
|`SH17_raw_release_members`|`white-children`|39|34|451.2/1560/2628|53.86/183.19/339.17|183.19/320.62/57626.74|
|`SH17_raw_release_members`|`white-female`|2039|1745|766.4/1891/3292.6|89.22/217.44/364.5|221.76/339.24/74816.23|
|`SH17_raw_release_members`|`white-male`|2424|2037|546.9/1725/3180.4|65.46/198.04/354.41|200.89/318.06/64204.59|
