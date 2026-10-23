from pathlib import Path
import re
R=Path(__file__).resolve().parent.parent
p=R/'RAW_FACTS.md';t=p.read_text(encoding='utf-8')
# Proper entity names and long joined prose fragments are repaired without changing
# source literals in backticks, URLs, filenames or numeric values.
fix={
'Physical AI':'PhysicalAI','SHEL5 K':'SHEL5K','Lin Q':'LinQ','CC BY4.0':'CC BY 4.0','CC BY-NC3.0':'CC BY-NC 3.0','CC BY-NC4.0':'CC BY-NC 4.0','CC BY-NC-SA4.0':'CC BY-NC-SA 4.0','CC BY-NC-SA3.0':'CC BY-NC-SA 3.0',
'автоматическийвывод':'автоматический вывод','вэтойветкенеполучены':'в этой ветке не получены','должнывосстанавливать':'должны восстанавливать','другоезаявленноесостояние':'другое заявленное состояние','еслицелеваяинструкцияопределила':'если целевая инструкция определила','здесьнеразработана':'здесь не разработана','зелёнаяполосаэтогозавода':'зелёная полоса этого завода','изоднойформулировкикарточки':'из одной формулировки карточки','любыеочкиотсутствуют':'любые очки отсутствуют','малойдвойнойдоразметкой':'малой двойной доразметкой','неисправлятьпоудобству':'не исправлять по удобству','неконкретные доказанные дубли':'конкретные дубли этим не доказаны','непокрасивомуимени':'не по красивому имени','неправополучателяперепубликовать':'не право получателя перепубликовать','несливатьоднойстрокой':'не сливать одной строкой','обувивспортивнойсцене':'обуви в спортивной сцене','общийповторпоискавущерб':'общий повтор поиска в ущерб','округлённыесайтовыечисла':'округлённые числа сайта','поставленнымилидокументированно':'поставленным или документированно','поставленными ли документированно':'поставленным или документированно','приоритетнеесинтетики':'приоритетнее синтетики','приэтомобычныеочкивидны':'при этом обычные очки видны','проверяютсясоседнимитемами':'проверяются соседними темами','спредварительнойкартой':'с предварительной картой','толькоприадреснойнужде':'только при адресной нужде','создаётриск':'создаёт риск','другдругу':'друг другу','сверканепроведена':'сверка не проведена','теже':'те же','задаютсяпосле':'задаются после','принадобности':'при надобности','неизобретать':'не изобретать','нерасходоватьна':'не расходовать на','иначеотложить':'иначе отложить','предложен о':'предложено','не верно':'неверно',
}
for a,b in fix.items():t=t.replace(a,b)
# All recorded entity prefixes are separated from ordinary prose suffixes.
for name in ['SH17','SHWD','SHEL5K','CHV','SFCHD','CPPE','SARD','PhysicalAI','LinQ','Pictor','Smoker','Construction','Harness','Önal','COCO','MOT17','Card','HF','Wang','Core','Mask','Approach']:
 t=re.sub(re.escape(name)+r'(?=[a-z])',name+' ',t)
replacements={
'boxunits':'box units','headsourceabsencecandidate':'head source absence candidate','hathelmetedhead':'hat helmeted head','helmetobject':'helmet object','headgenericbodypart':'head generic body part','headcandidate':'head candidate','finaltarget':'final target','flatpartialwearing':'flat partial wearing','visionaudit':'vision audit','imageclass':'image class','clipclass':'clip class','actionraw':'action raw','familyreporting':'family reporting','unannotatedclassespartial':'unannotated classes partial','manualrelabel':'manual relabel','candidateflat':'candidate flat','originaltest':'original test','annotationsvalidated':'annotations validated','approaches':'approaches','crowdimages':'crowd images','overlappingchunks':'overlapping chunks','authorstatestransformed':'author states transformed','helmetdata':'helmet data','versioncrosswalk':'version crosswalk','presumedindependent':'presumed independent','organizertriage':'organizer triage','exactv':'exact v','semanticgates':'semantic gates','broadfaceprotection':'broad face protection','conditionalfallback':'conditional fallback','foundationpit':'foundation pit','loggedcorrections':'logged corrections','publicationdate':'publication date','archivebytes':'archive bytes','augmentationchain':'augmentation chain','overwriteoriginals':'overwrite originals','derivedrecords':'derived records','externalmerge':'external merge','timeholdout':'time holdout','perclass':'per class','targetgaps':'target gaps','onsetuncertainty':'onset uncertainty','Qconstraints':'Q constraints','Qruntime':'Q runtime','videosequences':'video sequences','specificcase':'specific case','readytemporalriskdataset':'ready temporal risk dataset','APIroute':'API route','Cardv':'Card v','safeclass':'safe class','safeperiods':'safe periods','filehash':'file hash','personbox':'person box','sourceclass':'source class','sourcebox':'source box','groupkey':'group key','objectbox':'object box','headbox':'head box','clothesbox':'clothes box','objectcounts':'object counts','labelcounts':'label counts','datasetcount':'dataset count','sizecheck':'size check','classmap':'class map','sourcegroups':'source groups','sourcepixels':'source pixels','sourcefields':'source fields','sourceunits':'source units','personabsence':'person absence','globalclass':'global class','stableobject':'stable object','byteidentity':'byte identity','pixelidentity':'pixel identity','filenamealias':'filename alias','publicartifact':'public artifact','datasetpermission':'dataset permission','exactjoin':'exact join','technicalgate':'technical gate','falsealerts':'false alerts','cameraindependence':'camera independence','splitmembership':'split membership','bodypart':'body part','helmetedhead':'helmeted head','normalhead':'normal head','fullperson':'full person','wholeperson':'whole person','fullbody':'full body','wholebody':'whole body','torsoexample':'torso example','nohelmet':'no helmet','correctfit':'correct fit','carriedhelmet':'carried helmet','ordinaryhat':'ordinary hat','fullXML':'full XML','fullmedia':'full media','trainingtotals':'training totals','groupaudit':'group audit','parenthashcrosswalk':'parent hash crosswalk','codeonly':'code only','modificationrepublication':'modification/republication','noneprotocol':'none protocol',
}
for a,b in replacements.items():t=t.replace(a,b)
# Rewrite the final synthesis in connected prose; literals are explicitly quoted.
start=t.index('### F097 —')
t=t[:start]+'''### F097 — Предварительная карта понятий и единиц

**Наш synthesis/предложено; final target IDs ещё нет.** Сохранять `semantic_unit` отдельно от concept/state. SH17 helmet — предмет с потерянным wearing state; SHWD hat — голова в каске; SHEL5K helmet/head_with_helmet/person_with_helmet — соответственно предмет, голова, человек. SFCHD head и SHEL5K head — source candidates головы без каски; SH17 head — общая часть тела. Эти labels нельзя объединить в один no_helmet box class. CPPE Goggles и SH17 glasses требуют проверки safety/vision; broad Mask не равен exact industrial respirator, Face_Shield не респиратор. Construction no_* — части тела, Pictor Approach2 — worker state, Smoker — image class, Önal — clip class, SARD — raw action, PhysicalAI — reporting family. Relations `exact/conditional/partial/incompatible/not_annotated` назначаются после определения цели.

Основания: S002/S010/S013/S016/S018/S021/S023/S027/S030/S032/S033/S037/S039, exact maps в соответствующих карточках.

### F098 — Coverage, visibility, wearing и policy — отдельные поля

**Наш вывод/предложено.** `annotation_status`: verified_present/verified_absent/not_annotated/out_of_scope/ambiguous. `visibility`: visible/occluded/too_small/blurred/unreviewed. `observed_state`: worn/unworn/adjusting/incorrect/unknown; incorrect допустим только по целевой инструкции. Невидимость не означает absence; off object не person absence; person state не нарушение без policy. Отдельно нужны coverage_by_dataset_class, source box unit, relation evidence и event fields. Для неаннотированных классов выбрать dataset heads/loss masks, ручную доразметку, локально проверенные crops либо exclusion. Реализация loss относится к model_stack/training_strategy и здесь не разработана.

Основания: S005/S006/S016/S018/S020/S023/S039; F002/F020/F025/F053/F061/F085.

### F099 — Lineage и известные зависимости

**Документ/наш synthesis.** SCUT-HEAD частично входит в SHWD; GDUT-HWD и SHWD — родители CHV; SHD5000 — родитель SHEL5K. Raw SH17 связан с released flat-map, но полная cleanup сверка не выполнена. CPPE original test29 и HF test29 имеют проверенную annotation lineage. Pictor approaches/crops используют те же crowd images. MOT17 переиспользует MOT16 и три detector variants одной базы; COCO2017 переиспользует COCO2014 images. PhysicalAI chunks происходят из parents и могут перекрываться. SHD и SHWD — разные имена; их точное пересечение неизвестно. Общий web источник SH17/Pictor/CPPE создаёт риск, конкретные дубли этим не доказаны. Harness paper называет transformed Wang helmet data, точный version crosswalk не получен. Parent/derivative не независимые holdouts; отсутствие crosswalk не доказательство независимости. E006/E007.

Основания: S001/S009/S012/S014/S020/S023/S033/S036/S040/S042/S044.

### F100 — Порядок ролей и условные маршруты объединения

**Наше решение до полного кейса.** Сначала organizer triage и locked target holdout. Для внешней подготовки приоритетны SFCHD intersection 12,372/50,552 для factory adaptation/development, восемь Önal inputs для real replay/manual events и exact SH17 v1 для broad object donors. SHEL5K даёт несколько геометрий, SHWD — головы; CHV — vest/color при надобности. CPPE нужен после subtype/per-image audit, Smoker — для crops/confusers. Construction/Pictor — условные fallback. SARD supplementary отложен до schema; PhysicalAI — optional после реального GT. SODA/harness/Foundation Pit нужны только при адресном сценарии.

Объединение требует одинаковой box unit либо явно новой задачи, обратимой class map, установленной полноты или partial-label стратегии, разрешённых действий, source groups и журнала исправлений. Calibration/threshold tuning выполняются на development; единственный independent test не используется для калибровки. Основания: F005–F096, S001/S010/S013/S016/S018/S019/S021/S026/S030/S032/S033/S037/S039.

### F101 — Manifest: достаточные поля и обратимость

**Предложенная schema, не существующие source fields.** В dataset registry хранить source_family/dataset_id, revision/commit/deposit_version, publication_date отдельно от accessed_at, download_url/file_id, archive bytes/hash и происхождение expected checksum, license_layer/notice_hash/action_evidence. Для каждого original: original_path/image_id/source_url, media_hash/decoded_pixel_hash/dimensions, annotation_path/hash, nullable source_class_id и source_literal, source_bbox/coordinate_convention/semantic_unit, split_original, nullable group_id_original, отдельно group_id_inferred/algorithm/evidence. Далее coverage/visibility/state/nullable relations, mapping_version/nullable target_class, transform_history с scale/padding/crop/orientation/clipping, parent/crop/augmentation chain, usage_role/inclusion_reason/quarantine_reason.

Source originals не перезаписывать. Derived records должны восстанавливать исходные classes/boxes. Hash файла и canonical decoded RGB hash различаются; процедуру orientation/colour normalization записать. Если camera/session IDs не даны, они остаются null. Основания: S002/S015/S018/S021/S033/S037/S039; E018.

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
'''
p.write_text(t,encoding='utf-8')
for name in ['SOURCES.md']:
 p=R/name;t=p.read_text(encoding='utf8')
 for a,b in fix.items():t=t.replace(a,b)
 t=t.replace(' (если имя отличается, точный payload путь в W1-08)','')
 t=re.sub(r'(### (S\d{3}) —)',lambda m:f'<a id="{m[2].lower()}"></a>\n\n'+m[1],t)
 p.write_text(t,encoding='utf8')
