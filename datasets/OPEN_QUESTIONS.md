# Открытые вопросы и программа практической проверки datasets

Срез: 23.10.2026, Europe/Moscow, после двух замороженных волн. Нового поиска, обучения и больших прогонов сборщик не проводил. Q — точное неизвестное; E — воспроизводимая программа. **Все E001–E018 ниже предложены для следующей практической работы**, даже когда отдельный их компонент уже выполнен в W1/W2. Уже выполненный компонент указан явно и не выдаётся за завершение всей программы. Подробные результаты текущих проверок — [RAW_FACTS.md](RAW_FACTS.md), первичные локаторы — [SOURCES.md](SOURCES.md), история замечаний — [CRITIC.md](CRITIC.md).

## Ближайшие вопросы, меняющие выбор

<a id="q001"></a>

### Q001 — обязательные классы, наблюдаемые состояния и метрики полного кейса

**P0; полный кейс/постановщик.** Известны только примеры каски, снятого респиратора, опасной зоны и курения рядом с горючими. Исходные промпты и все ветки не содержат полного обязательного taxonomy/event protocol. Неизвестно, что означает respirator, incorrect/removed, событие и допустимый unknown; возможны разные единицы boxes/человек/интервал. Это определяет объём решения, нужные donors и доразметку. Получить формулировку кейса, class definitions, positive/negative/ignore examples, правила зоны/длительности и требования оценки. До ответа карты provisional, дополнительные СИЗ не объявляются обязательными. Связи: F001–F004, E015, K008/K009/K010.

<a id="q002"></a>

### Q002 — реальный target video и preprocessing на LinQ

**P0; organizer media/SDK и соседние темы.** Нет target resolution/FPS/timebase/viewpoint/night mode, размера лиц/сигарет/голов, codec/битрейта и разрешённого model input/transform. Распределения S048 описывают donors и условный 640, не target. Решение: full-frame против crop/tiling, выбор representative calibration и класса, который визуально нельзя обещать. Получить короткие исходные clips разных условий и точный input contract от model_stack/linq_platform, выполнить E008/E015. Связи: F019/F037–F041/F065, K013.

<a id="q003"></a>

### Q003 — конкретные разрешённые действия с выбранными внешними artifacts

**P0 для public delivery/дальнейшего использования; правообладатель/постановщик.** SFCHD: explicit grant не найден в pinned README/tree/root LICENSE/официальном ZIP directory; SH17 Kaggle NC-SA против alternative Zenodo NC и paper commercial wording; SHWD/CHV/Pictor upstream/aggregate scope неполон. Нужно отдельно разрешение на local training/adaptation, публичные кадры/crops/demo, изменённые labels, weights и deployment. Unknown не означает установленный запрет или разрешение. Подготовить адресный запрос с dataset version/hash и перечнем действий; самим внешних писем исследование не отправляло. E014 фиксирует документы/слои/ответ. Независимая работа с organizer/own media продолжается. Связи: F018/F035/F045/F049/F055/F060/F064/F071, S008/S022/S034, K012.

<a id="q004"></a>

### Q004 — SH17: есть ли cleanup changes вне sample 13/228?

**P1; получение label слоя/практика.** Полный manifest 8,099 members и raw-members count объясняют candidate 75,994; 13 samples совпали по map/geometry. Все released YOLO не parsed, поэтому equal total не full equivalence и не actual per-class release counts. Получить exact version1 labels/VOC выбранного состава, выполнить full comparison, сохранить различия, authoritative converter/normalization version спросить автора при необходимости. Решение: готовый released loader против самостоятельной raw derivative. Связи: F006–F017, K001/K002, E001/E003.

<a id="q005"></a>

### Q005 — SH17: official off protocol, completeness и независимые source groups

**P1; author guideline/targeted annotation/image audit.** Есть off-предметы в руке/на стене, mask под подбородком и noisy candidates; нет exhaustive author rule, person associations или фотосессионных groups. Photographer ID не session ID; disjoint filenames не independence. Нужны guideline и stratified double review, exact/near/source grouping, отдельно rates только на определённой выборке. Решение: object-only donor либо новый wearing слой, безопасный holdout. Связи: F014–F022, K002, E004–E007.

<a id="q006"></a>

### Q006 — SFCHD: где pixels отсутствующего 192.168.2.20_1c_29.jpg?

**P1; exact artifact/автор.** В COCO есть семь boxes; old TXT получен и согласован, но JPEG нет в официальном images directory и в modern label/split составе. Candidate TXT не восстанавливает media. До exact JPEG запись исключена из working 12,372/50,552, source record сохранён. Получить author revision/pixels и проверить hash/dimensions/overlay, не подставлять похожий файл. Решение: восстановление записи, а не блокирование всего набора. F027/F028, K003, E001/E002.

<a id="q007"></a>

### Q007 — SFCHD: какой val protocol соответствует публикуемой метрике?

**P1; документация автора/точный reproduction.** COCO val и TXT val по 2,475 images, overlap520/symmetric difference3,910; tiny test6 полностью в TXT val. Это установленное различие, а не вопрос количества. Для сравнения metric нужен конкретный code/config/split membership версии статьи. Иначе отчёт воспроизводит отдельно named TXT protocol и COCO protocol, без общей метрики. F030/F031, K003, E007.

<a id="q008"></a>

### Q008 — SFCHD: supplied camera/scene/light grouping без sensitive metadata

**P1, P0 для заявления independent-camera quality; автор/практический audit.** Все40 prefixes в train/val,205 из231 inferred runs пересекаются; два runs одного prefix визуально один view. Directory.md/light manifest не найден, время/plant location de-identified. Нужны разрешённые scene/camera equivalence groups, а не попытка восстановить удалённые timestamps. До ответа own inferred-view-grouped split с manual collision review и явным ограничением. F032–F035, K004, E007.

<a id="q009"></a>

### Q009 — SHWD: coordinate convention и сложные головы

**P1; author instructions/targeted pairs.** XML/8 JPEG подтвердили normal-head и helmeted-head geometry, но ordinary hats, carried helmets, partial/occluded policies и точный VOC origin/inclusive convention не установлены. Получить guideline/адресные примеры и roundtrip; не менять координаты по одному имени VOC. Решение: какие labels считать usable head-state GT и как конвертировать. F042–F045, K005, E003/E004.

<a id="q010"></a>

### Q010 — helmet family: exact parent crosswalk и права исходных media

**P1; manifests/images/owner.** CHV прямо происходит из SHWD/GDUT-HWD, SHEL5K из SHD; SCUT частично в SHWD. Exact image matches/counts не измерены, SHD↔SHWD relationship неизвестен. MIT code/free-use/NC сборки не единый photo grant. При реальной смеси выполнить exact/near comparison и сохранить connected groups, запросить недостающий конкретный notice. Решение: training pool/holdout и public assets. F042–F055, K005/K006/K007/K012, E006/E014.

<a id="q011"></a>

### Q011 — SHEL5K: intended map восьми extra person и official split membership

**P1; author guideline/ручная доразметка.** Полный XML count/hash проверен; 8 person в пяти файлах, две пары показывают mixed/unknown states. Неизвестна author intention seventh literal; конкретные 4,000/1,000 names не найдены. Получить map/membership либо создать явно own split с source-family constraints; extra objects quarantine/relabel с журналом. Не присваивать автоматически no_helmet. F050–F055, K007, E004/E007.

<a id="q012"></a>

### Q012 — CPPE: source license join, original media frames и 100 test

**P0 для exact respirator/media publication; P1 для object tooling.** Original annotation 1,000/29 и HF test29 lineage подтверждены; code+labels Apache2.0 уточнены автором. Нет numeric ID→Flickr/Google source/author/license inventory; COCO/release tree/assets его не дали, остальная часть tar не проверена. Image762 exact filename dimension mismatch в quarantine; image15 candidate missed visible mask. Дополнительные100 testing paper не привязаны к public release. Получить source manifest/exact pixels/author protocol; проверить выбранные IDs до subtype training. Решение: разрешённые и корректно paired media donors, а не общий Mask→respirator merge. F056–F062, K008, E001/E002/E004/E014.

<a id="q013"></a>

### Q013 — surveillance smoking/calling dataset по разумному запросу

**P1, P0 при обязательной localization; автор.** Полный Zhang et al. PDF получен; behavior-face+objects и separate cigarette/hand/phone boxes описаны, public payload не дан. Нужны actual images/LabelMe schema, source-video/subject/camera IDs, split, license и demo terms. Письма не отправлялись. Ответ определяет, сколько own annotation нужно и доступен ли localization donor; Smoker classification не заменяет boxes/events. F065/F066, K009, E012/E014.

<a id="q014"></a>

### Q014 — Önal continuous safe recordings и event protocol

**P0 для operational event metrics; автор/organizer.** 691 curated MP4 manifest и8 samples доступны; разное timing/view overlap, clip start иногда left-censored, class не exhaustive per-person. Нет continuous raw URL, supplied camera/session IDs, polygons/tracks/onset. Получить разрешённые continuous safe periods и protocol или разметить собственные target sequences. Решение: event recall/latency/false alerts per camera-hour с честным denominator. F067–F071, K010, E013.

<a id="q015"></a>

### Q015 — SARD schema, frame indexing, ID lifecycle, source/split map

**P1; author artifact, supplementary пока отложен.** Card обещает definitions/splits, directories/Zenodo related identifiers/ORCID не дали schema; raw_id_2 у340 IDs меняет class. Core sample иной sequence, егоFPS не проверяет4.txt. Нужны короткий excerpt4.mp4 с frame offset/FPS, column definitions/HOI map/reset rules и upstream/split manifests. Решение: usable tracking/action annotations либо только Core clip donor. F072–F075, K011, E011.

<a id="q016"></a>

### Q016 — PhysicalAI: exact media packaging, generator/scenario и actions

**P2, P1 при выборе synthetic; artifact/owner/terms.** Family282/157 и temporal metadata join установлены, actual ZIP members/media не получены. Per-video Veo/Cosmos assignment/scenario groups неизвестны; NVIDIA local AI development grant не public dataset redistribution. Дополнительные Google conditions и Trustworthy AI отсылка не полностью решены для нашей цели. Уточнить action scope/generator, затем directory/range/member sample. Решение: optional synthetic plumbing/augment, не real holdout. F076–F079, K015, E010/E014.

<a id="q017"></a>

### Q017 — Pictor map, 2,496/2,497 и разрешённые действия

**P1/P2 по scope; автор/реальный artifact.** Crowd774 annotations доступны, one paired image; Approach1 class1 vest не просмотрен paired, Approach2 exact numeric W/WH/WV/WHV map не дан. Actual2,497 worker boxes против README2,496; web698 не получены. Нужны map/version explanation и terms crowd/web/media/labels. Решение: оставить узкий hat/vest donor либо не тратить время. F080–F082, K014, E004/E005/E014.

<a id="q018"></a>

### Q018 — Construction-PPE none/completeness/upstream/10 orphans

**P1/P2 по scope; guideline/targeted annotation.** Part-local no_* и one torso none подтверждены; definition none не исчерпана одним примером. 10 train orphan labels и all-label counts известны, paired-only counts нужно отделить. Нет exhaustive visibility protocol/source-photo inventory. Internal AGPL notice установлен, его нельзя автоматически перенести на upstream photos/weights. Решение: ограниченный donor после фильтра и доразметки, не универсальный absence benchmark. F083–F086, K014, E002–E005/E014.

<a id="q019"></a>

### Q019 — отложенные SODA/harness/Foundation Pit/generic artifacts

**P2; открытый artifact/owner только при соответствующем кейсе.** SODA direct ZIP403, numeric map/internal terms не получены; harness tree/2 XML не decoded images/split/license/secured-anchor GT; Foundation Pit v2 video GT не исследован; COCO actual categories/CrowdHuman ODGT/MOT current class instructions требуют exact payload. Неизвестное не маскируется каталогом популярных наборов. Решение: адресная auxiliary роль, не новый общий обзор. F087–F096, E001/E009/E014.

<a id="q020"></a>

### Q020 — независимость и полнота выбранной training mixture

**P0 перед заявлением независимого качества; практическая проверка.** Есть known lineage, annotation repeats, filename disjointness и один полный Smoker RGB duplicate audit, но нет полного image exact/near/source-group audit смеси. Missing label не отрицательный target. Нужны E005/E006/E007, сохранённые coverage и source components. Решение: допустимая training mixture, honest calibration/holdout, области метрик. F002/F022/F032/F097–F102, K002/K004/K006/K014.

## Готовая программа E001–E018

### E001 — получить точную версию выбранного набора

**Входы:** registry S002/S003/S010/S013/S015/S018/S019/S021/S025/S033/S037/S039 с exact revision/file IDs; выбрать только нужный источник. **Действия:** сохранить response metadata, advertised bytes/checksum origin; отличить text/ZIP/tar/RAR/LFS/HTML challenge, полный файл от Range prefix. Проверить archive directory/path safety, CRC member и локальный SHA256, pin release membership. **Наблюдения/артефакты:** acquisition manifest, HTTP status/Range total, archive/member hashes, failures и retry route. **Исходы:** exact payload — переход E002; unavailable/gated — адресный fallback/Q, без объявления всего имени закрытым. Уже выполнены некоторые directories/payloads и SH17 13 samples, но полный selected training artifact не получен. Успех не доказывает semantic quality/rights/independence.

### E002 — pairing, decode и coordinate-frame identity

**Входы:** exact source manifest/media/labels, exclusions F027, CPPE762, Construction orphans, SHWD case/old filename. **Действия:** joins по documented IDs/member stems, проверить collisions/case, missing/empty/orphan, decode и declared↔actual W/H; для сомнительного file идентифицировать exact historical pixels, не молча rescale. **Метрики:** counts пар/ошибок/несовпадений, bytes и decoded hashes; exceptions с locator. **Артефакты:** PAIRS/QUARANTINE/DECODE reports и overlays. **Исходы:** usable subset с named exclusions либо получение исходного media; запрет autojoining `(1)` orphan к чужому stem. Уже выполнены sample pairs/Smoker decode, не все source media. Успех структуры не exhaustive semantics.

### E003 — geometry и conversion roundtrip

**Входы:** exact categories/XML/TXT/COCO и decoded dimensions, chosen converter version. **Действия:** проверить ID/name/range, xyxy/xywh/normalized center, origin/inclusive rules по overlays; отдельно floating tolerance и material overflow; roundtrip source→canonical→source с сохранением bbox/class/split. Не clip/delete originals; clipping/log — derived choice. **Метрики:** unmatched objects, max coordinate error/IoU, zero-area/OOB/count shifts. **Артефакты:** converter commit, input/output checksums, per-object diff и visual cases. SFCHD shared50,552 и SH17 sample228 уже сравнены; полный ingestion/re-export ещё нет. Успех не правильность класса/полнота GT.

### E004 — семантика и визуально наблюдаемые состояния

**Входы:** targeted source pairs и target definitions, raw SH17/off, SHWD heads, SHEL extra person, CPPE subtypes, Pictor maps, Construction no_*. **Действия:** заранее записать reasons/strata/seed; два annotators отдельно отмечают bbox unit, видимый предмет/часть тела, worn/unworn/adjusting/incorrect/unknown и relation evidence; adjudication спорных случаев. **Метрики:** disagreement/unknown/reject по конкретным strata, не general dataset error rate по convenience sample. **Артефакты:** selection manifest, original/proposed labels/overlays/reasons. Исход — usable concept map, ручная доразметка или reject/unknown; on не correct fit, off не person absence. Успех не certification/policy correctness.

### E005 — class coverage и partial labels

**Входы:** несколько полноразмерных source/target кадров по нужным классам с visibility; CPPE15 и CHV bare-head candidate как расследуемые случаи. **Действия:** независимо доразметить все видимые target objects, сравнить source coverage, отделить out-of-scope/occluded/missed/verified absent. Выбрать dataset heads/loss masks, crops с локальной полнотой, relabel или exclusions. **Метрики:** missed visible objects/false labels/unknown per class и visibility, scope выборки. **Артефакты:** coverage_by_dataset_class, annotation_status, adjudication log. **Исход:** условие training route и границы eval. Успех small audit не доказывает полноту всего набора; loss implementation → model_stack/training_strategy.

### E006 — exact и near duplicates внутри/между families

**Входы:** original media выбранной смеси, известные parent/child relations, orientation/canonical RGB procedure. **Действия:** file SHA256 и decoded-pixel SHA256; near retrieval pHash/embedding candidates с ручной проверкой crop/resize/flip/re-encode/burst/adjacent frames. Не назначать универсальный threshold; connected component originals/derivatives держать вместе. **Метрики:** exact/near matched pairs с причинами/score/decision; ambiguous components quarantine. **Артефакты:** pair table/contact sheets/source lineage/groups. Smoker zero exactRGB groups и MOT GT repeats уже известны, полного media audit смеси нет. Успех hash search не доказывает независимость разных кадров одного видео.

### E007 — groups, split protocol и locked holdout

**Входы:** supplied camera/video/session/person IDs или nullable fields, SFCHD prefix/run proxies, Önal views, photographer metadata. **Действия:** сохранить official split для reproduction; отдельно строить own group split, вручную объединить совпавшие views/near groups, не выдавать inferred за supplied. Все crops/augmentations/MOT variants одной базы вместе. Development/calibration и locked test различны; repeated tuning превращает test в development. **Метрики:** group intersections, unresolved provenance, class/scale coverage по splits; CF camera-disjoint claim только при доказанных IDs. **Артефакты:** split manifest, group evidence/rule version, holdout lock record. Успех proxy grouping не гарантирует новую камеру/site; target holdout нужен отдельно.

### E008 — target scale/visibility и сравнение transforms

**Входы:** native organizer clips и реально допустимые input sizes/transforms, source distributions S048. **Действия:** label target head/person/PPE/cigarette с visibility/light/occlusion, измерить native/after-transform width/height/min-axis/area; сравнить full frame/crop/tiling на одном group holdout, учесть first-stage misses/crop context/end-to-end latency. **Метрики:** per-class quantiles/histograms, target unknown rate; quality/latency только после отдельного model experiment. **Артефакты:** transform spec, scales/overlays, model/runtime version при запуске. Уже есть donor declared-frame quantiles; target/quality сравнение не выполнено. Upscale/crop не создают отсутствующую исходную детализацию,640 не LinQ contract.

### E009 — generic person/pose/tracker fixtures

**Входы:** actual COCO categories/pose, CrowdHuman ODGT, MOT17 base sequences/GT/class instructions с условиями. **Действия:** проверить F/V/H geometry, visibility/ignore/unsure/crowd, MOT class filtering и timestamps, detector variants по base group; локально проверять ID switches/fragmentation/occlusion recovery и episode cooldown на искусственном правиле. **Артефакты:** exact subset manifest/filters/logs. **Исход:** pipeline regression fixture, не PPE/compliance/event quality. Ни generic missing PPE, ни CrowdHuman tag mask не PPE negative/positive.

### E010 — optional PhysicalAI exact retrieval и synthetic review

**Входы:** pinned S033, EXACT_JOIN282/157, S034/S035 action review. **Действия:** до multi-GB download проверить directory/members, subset bytes/checksums/window↔payload mapping, synthetic artifacts/visual label uncertainty, generator/scenario grouping; external pointers отдельно. **Метрики/артефакты:** packaged/actual counts, temporal consistency, visual issues, parent/scenario connected groups. **Исход:** optional plumbing/augment donor либо defer. Exact metadata join уже выполнен, media нет. Даже успешный synthetic test не camera-hour real holdout и не разрешение публично host raw/crops/annotations.

### E011 — SARD schema gate

**Входы:** author definitions/HOI/splits, excerpt4.mp4 с native FPS/frame offset и4.txt. **Действия:** overlay начало/середину/конец/occlusions; проверить frame indexing, xyxy/xywh, inclusive bounds, ID lifecycle/reset/class consistency, action vocabulary. Raw IDs до доказательства сохранять как raw_id_1/raw_id_2. **Метрики:** synchronized boxes/ID transitions/unresolved fields, не invented MOT score. **Артефакты:** schema mapping, sample overlays, author provenance. **Исход:** bounded supplementary role либо defer. Current Core clip другой sequence и safe parser не заменяют этот gate; успех нескольких frames не валидация девяти видео.

### E012 — target smoking/respirator annotation pilot

**Входы:** разрешённые native target clips/definitions; при доступе donor localization S027 и CPPE exact selected pixels. **Действия:** subtype/visibility/person relations; cigarette/hand/phone/face/head и похожие phone/drink/eat/inhaler/hands-to-face, отдельно policy flammable area/context. Для respirator worn/removed/incorrect/unknown по инструкции, без сертификации по фото. **Метрики:** annotation agreement, observable/unknown coverage, object и event units отдельно. **Артефакты:** manual layer/source hashes/relations/uncertain intervals. **Исход:** достоверное минимальное GT или исключение невизуализируемого состояния из обещаний. Это не уже выполненное обучение и не operational benchmark.

### E013 — zone/event pilot и continuous safe denominator

**Входы:** 8 Önal MP4 как ограниченный replay, затем continuous organizer/own media для operational оценки. **Действия:** full-clip review, policy_id, polygon/ground footpoint, tracks, visibility/ignore, onset/end, left/right-censored cuts, episode relation/cooldown; сохранять timestamps, multiple actors и uncertain boundary. **Метрики:** event recall/missed episodes, onset delay, repeat alerts/episode; false alerts/hour только по действительно размеченным safe hours и данным scope. **Артефакты:** video/event manifest, polygons/tracks/manual intervals и reviewed camera-hours. **Исход:** demo/pipeline fixture либо representative target evaluation. Curated clip class/start не author onset; восемь clips не долгосрочная частота тревог.

### E014 — action-specific rights/provenance ledger

**Входы:** exact chosen revisions/hashes и primary notices, author clarification при необходимости. **Действия:** отдельно code/labels/photos/assembly/article/weights; link source author/license/date/notice hash; записать local train, modify, public raw/crop/demo, labels, weights, deploy как evidence/conditional/unknown. Подготовить точный owner вопрос, не blanket commercial_ok. **Артефакты:** source/action matrix в manifest и сохранённые ответы/notices. **Исход:** разрешённая роль/ограниченная поставка/замена media на own/organizer. Исследование не отправляло сообщений. Успех не гарантирует все third-party rights; не решать автоматически SA/AGPL на weights или NC на призовой хакатон.

### E015 — organizer data triage до внешней смеси

**Входы:** полный кейс и фактически переданные files/terms; объём/качество не предполагаются. **Действия:** immutable inventory, exact labels/units/state/event map, decode/timing/pairs/geometry, source groups, locked target holdout до merge; затем coverage/scale/confuser audit и comparison external donors, development calibration отдельно. **Артефакты:** intake manifest/assumptions/holdout protocol/question list к постановщику. **Исход:** revised candidate order и минимальная целевая доразметка. Успех data intake не LinQ execution/real-time/quality proof.

### E016 — полный selected artifact integrity после выбора

**Входы:** источник, прошедший access/rights/semantic gates; exact subset до training. **Действия:** объединить E001–E007 для всех реально используемых records, не для всех когда-либо найденных наборов; сохранить errors/quarantine/derived totals. **Наблюдения:** paired-only actual class counts, actual dimensions, split components, transformation lineage. **Исход:** воспроизводимая training/development dataset revision. Выборочные W2 checks не переименовывать задним числом в этот full selected audit.

### E017 — manual evaluation и uncertain-state agreement

**Входы:** target holdout с source groups/политикой. **Действия:** два разметчика независимо оценивают ambiguous visibility/state/boundary, adjudication; раздельно object/person/event outputs и unknown. **Метрики:** disagreement по классу/масштабу/свету, доля not-observable, precision/recall только для установленного scope. **Артефакты:** frozen GT version/changes/review notes. **Исход:** честные границы обещаний/порогов; согласие людей не доказывает визуально недоступную сертификацию изделия.

### E018 — manifest и lineage roundtrip доставки

**Входы:** выбранный converted subset и предлагаемая schema F101/F102. **Действия:** независимым чтением восстановить original class/name/bbox/media/group/split/reason из derived records; проверить nullable original IDs, hash origin и transform reversibility, исключённые records остаются в журнале. **Метрики:** lost fields/unknown remaps/untraceable crops/split changes, допустимые численные tolerance. **Артефакты:** roundtrip report и manifests с version. **Исход:** переносимая база для model_stack/training_strategy/evaluation. Успех provenance не доказывает model accuracy или полную правовую применимость.

## Реестр уже выполненных bounded checks E019–E033

Здесь E-ID обозначает выполненное действие второй волны. Оно не получает более широкого scope от совпадения темы с предлагаемой программой выше. Исходные artifacts/version/access и execution locators — в соответствующих S/F-записях.

| ID | Выполненное действие и охват | Сохранённые результаты и границы |
|---|---|---|
|E019|SH17 complete manifest, stem audit,13 released labels/228 mapped boxes, exact released13376117|F006/F012/F013/F016; W2-01 MANIFEST_PROGRESS/PAIRED_COMPARISON/RELEASE_IMAGE_DECODE. Не full released parse/quality audit.|
|E020|SH17 targeted13 current-URL pairs, decode/dimensions/contact sheets|F014–F016; W2-02 SAMPLE_SELECTION/CONTACT. Source-state cases, не error rate; текущий URL одного image не historical pixels.|
|E021|SFCHD full annotation consistency, split comparison и OOB tolerance|F024–F031; W2-03 AUDIT/SUPPLEMENT/GEOMETRY. Не full image semantics.|
|E022|SFCHD official archive directory,7 pairs/27 boxes, prefix/run overlap|F027/F032–F035; W2-04 MANIFEST/PAIRED_AUDIT/GROUPS. Proxy groups не supplied cameras.|
|E023|SHWD directory,4 splits,20 XML/8 JPEG|F043/F044; W2-05 STRUCTURE/PAIRED/CONTACT. Head geometry, не completeness ordinary hats.|
|E024|CHV directory/map/splits,27 labels/4 JPEG|F047/F048; W2-06 README/AUDIT. Не all9,209 recount или rights proof.|
|E025|SHEL5K5000 XML, все metadata hash matched,4 новых PNG|F050–F055; W2-07 XML_AUDIT/PAIRED_AUDIT. Count conflict localized, remaining4993 PNG не checked.|
|E026|CPPE prefix tar,2 complete COCO,29 HF comparison,2 PNG и author comment|F057–F061; W2-08 COCO/COMPARISON/PAIRING/issue6. Не полный tar/source license inventory.|
|E027|Smoking primary PDF восстановлен; Smoker1120 decodedRGB и40negative thumbnails|F063–F066; W2-09 PDF/DECODE/CONTACT. Zero exact duplicates не independence.|
|E028|Önal full691 metadata inventory/8 actual MP4 container probes/frames|F068–F071; W2-10 MANIFEST/SAMPLE_OBSERVATIONS. Не event GT/continuous safe hours.|
|E029|SARD bounded Core member, raw4.txt parser/ID-class analysis|F072–F075; W2-11 CORE/ID_STRUCTURE/PARSER. Другой Core clip не pair к4.txt, tracks не validated.|
|E030|Bounded rights notices проверены, wrong Zenodo record исключён|F018/F035/F060/F079/F083; W2-12 BOUNDED_REQUESTS/PEXELS notes. Не legal clearance/ответ владельца.|
|E031|Scale annotations132 groups/202,781 rows, threshold0.1% восстановлен|F019/F037–F041/F062; W2-13 SCALE_SUMMARY/QUANTILES/BOXES. Declared frames, не accuracy/LinQ input.|
|E032|Pictor9 TXT/1image; full Construction ZIP/labels и4 semantic pairs|F080–F086; W2-14 AUDIT/PICTOR_AUDIT/CONTACT. Не full semantic QA/scene independence.|
|E033|PhysicalAI deterministic smoking family282 chunks/157 parents и terms read|F076–F079; W2-15 EXACT_JOIN/JOIN_SUMMARY/LICENSE. Media member/quality не checked.|
