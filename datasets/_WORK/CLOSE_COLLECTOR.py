from pathlib import Path
import re,json,csv,datetime,hashlib
from NORMALIZE_COLLECTOR import normalize
R=Path(__file__).resolve().parent.parent
# Normalize only newly added working prose. The original critic history remains byte-for-byte text.
for file in ['_WORK/AUTHOR_BRIEF.md']:
 p=R/file;p.write_text(normalize(p.read_text(encoding='utf8')),encoding='utf8')
p=R/'CRITIC.md';t=p.read_text(encoding='utf8');mark='## Дополнение сборщика после завершённой второй волны';a,b=t.split(mark,1);t=a+mark+normalize(b);p.write_text(t,encoding='utf8')
# Replace known glued technical words in newly written prose, preserving exact source strings.
phrases={
'Physical AI':'PhysicalAI','SHEL5 K':'SHEL5K','Lin Q':'LinQ','респиратор о подобных':'респиратороподобных','copy right':'copyright','boxunits':'box units','partlocal':'part-local','part-localno':'part-local no','perclass':'per-class','primaryPDF':'primary PDF','rawstate':'raw state','rawmember':'raw member','nativecontainer':'native container','trainingartifact':'training artifact','actualsamples':'actual samples','queryне':'query не','testoverlap':'test overlap','proxygroups':'proxy groups','parentchild':'parent-child','safehours':'safe hours','calibrationplanning':'calibration planning','deviceperformance':'device performance','measuredAP':'measured AP','candidatepartial':'candidate partial','mediaidentity':'media identity','exactpixels':'exact pixels','personitem':'person-item','eventintervals':'event intervals','publicmediaaction':'public media action','partialcoverage':'partial coverage','sourceinventories':'source inventories','targettaxonomy':'target taxonomy','fullcase':'full case','worlddomain':'world domain','pairedimages':'paired images','rawperson':'raw person','selectedframes':'selected frames','groupholdout':'group holdout','lineagevalidated':'lineage validated','classIDs':'class IDs','scriptimplemented':'script implemented','schemaunknown':'schema unknown','classchanges':'class changes','sourceprovenance':'source provenance','metadatawindowsvalid':'metadata windows valid','falsealerts':'false alerts','realcamera':'real camera','camera-hourholdout':'camera-hour holdout','upstreamrights':'upstream rights','publicdataset':'public dataset','safetyclothing':'safety clothing','filelisting':'file listing','sourcemetadata':'source metadata','headstate':'head state','sourceframe':'source frame','exhaustiveannotations':'exhaustive annotations','correctwearing':'correct wearing','wornstate':'worn state','wearingstate':'wearing state','sourcecamera':'source camera','cameragroups':'camera groups','parentsubset':'parent subset','artifactmap':'artifact map','countconflict':'count conflict','geometrygate':'geometry gate','labelscope':'label scope','sourceURL':'source URL','sourceID':'source ID','sourceIDs':'source IDs','allclasses':'all classes','sixclass':'six-class','fiveclass':'five-class','mapApproach':'map Approach','classSafe':'class Safe','extraobjects':'extra objects','labelerror':'label error','labelmap':'label map','stemsets':'stem sets','confusersреальны':'confusers реальны','defermedia':'defer media','mapgate':'map gate','geometrycheck':'geometry check','fullaudit':'full audit','independentholdout':'independent holdout','targetholdout':'target holdout','own-data':'own-data','eventmetrics':'event metrics','datasetcode':'dataset code','wholeperson':'whole-person','domainshift':'domain shift','canonicalRGB':'canonical RGB','explicitgrant':'explicit grant','dataintake':'data intake','boundedcheck':'bounded check','pairedcount':'paired count','pairingcheck':'pairing check','samplecoverage':'sample coverage','targetscene':'target scene','targetdata':'target data','actorstate':'actor state','cropcontext':'crop context','classunit':'class unit','smallcounts':'small counts','sizequantiles':'size quantiles','minaxis':'min-axis','objectdonor':'object donor','broadface':'broad face','metadatajoin':'metadata join','nativeframes':'native frames','trainsplit':'train split','valsplit':'val split','testsplit':'test split',
}
for file in ['RAW_FACTS.md','SOURCES.md','OPEN_QUESTIONS.md','_WORK/AUTHOR_BRIEF.md']:
 p=R/file;t=p.read_text(encoding='utf8')
 parts=re.split(r'(`[^`\n]*`|https?://[^\s)]+|\]\([^\n]*?\))',t)
 for i in range(0,len(parts),2):
  for old,new in phrases.items():parts[i]=parts[i].replace(old,new)
  # Character boundaries are repaired without splitting conventional entity literals.
  parts[i]=re.sub(r'(?<=\d)(?=(?:paths|media|objects|boxes|images|labels|samples|clips|parents|chunks|records|groups|rows|files|members|XML|JPG|PNG|TXT|MP4|COCO|YOLO|bytes)\b)',' ',parts[i])
  parts[i]=re.sub(r'([,;])(?=[А-Яа-яA-Za-z])',r'\1 ',parts[i])
 t=''.join(parts);p.write_text(t,encoding='utf8')
# Critic appendix: use the same prose repair, with untouched historical prefix.
p=R/'CRITIC.md';t=p.read_text(encoding='utf8');a,b=t.split(mark,1)
for old,new in phrases.items():b=b.replace(old,new)
b=re.sub(r'(\d)(?=(?:paths|media|objects|boxes|images|labels|samples|clips|parents|chunks|records|groups|rows|files|members|XML|JPEG|JPG|PNG|TXT|MP4|COCO|YOLO|bytes)\b)',r'\1 ',b)
p.write_text(a+mark+b,encoding='utf8')
# Correct question references to the final, frozen F numbering.
p=R/'OPEN_QUESTIONS.md';t=p.read_text(encoding='utf8')
subs={
'F018/F035/F046/F050/F056/F062/F068/F076':'F018/F035/F045/F049/F055/F060/F064/F071',
'F042–F046':'F042–F045','F042–F056':'F042–F055','F051–F056':'F050–F055','F057–F066':'F056–F062','F069/F070':'F065/F066','F071–F076':'F067–F071',
'F080–F082':'F080–F082','F083–F086':'F083–F086',
}
for old,new in subs.items():t=t.replace(old,new)
p.write_text(t,encoding='utf8')
# A portable native/640 per-class appendix complements the full exact CSV/JSON.
p=R/'RAW_FACTS.md';t=p.read_text(encoding='utf8').split('\n## Приложение к F041')[0]
t+='''\n## Приложение к F041 — все 132 dataset/class groups scale audit

**Наша выполненная проверка E031/S048.** Значения ниже извлечены из сохранённого QUANTILES.csv, без нового измерения. Native и условный640 min-axis: q10/q50/q90 в px; W/H — медианы width/height после640; A — медиана area640 в px². Округление отображения до двух десятичных знаков; все точные квантили0/.1/.25/.5/.75/.9/1 для native/640 width/height/area/min-axis и area_fraction, input hashes и histograms сохранены в [QUANTILES.csv](_WORK/MATERIALS/W2-13/QUANTILES.csv) и [SCALE_SUMMARY.json](_WORK/MATERIALS/W2-13/SCALE_SUMMARY.json). Raw all и raw release-member scopes перекрываются, их нельзя складывать. Rare raw categories с1–10 instances не получают устойчивых population quantiles от этой таблицы. Demographic raw literals сохранены только для provenance и не входят в продуктовую таксономию.

| Scope | Literal | n objects | images | Native min-axis q10/q50/q90 | 640 min-axis q10/q50/q90 | W640/H640/A640 q50 |
|---|---|---:|---:|---|---|---|
'''
def fmt(s):return f'{float(s):.2f}'.rstrip('0').rstrip('.')
with (R/'_WORK/MATERIALS/W2-13/QUANTILES.csv').open(encoding='utf8',newline='') as fp:
 for x in csv.DictReader(fp):
  qa='/'.join(fmt(x['min_axis_q'+q]) for q in ['0.1','0.5','0.9'])
  qb='/'.join(fmt(x['min_axis640_q'+q]) for q in ['0.1','0.5','0.9'])
  med='/'.join(fmt(x[k+'_q0.5']) for k in ['width640','height640','area640'])
  t+=f'|`{x["dataset"]}`|`{x["category"]}`|{x["n"]}|{x["images"]}|{qa}|{qb}|{med}|\n'
p.write_text(t,encoding='utf8')
# Inventory/references check is part of collection, not an additional role or wave.
files=['SOURCES.md','RAW_FACTS.md','OPEN_QUESTIONS.md','CRITIC.md','_WORK/ID_MAP.md','_WORK/AUTHOR_BRIEF.md']
issues=[]
for file in files:
 text=(R/file).read_text(encoding='utf8')
 for label,dest in re.findall(r'\[([^\]]+)\]\(([^)\n]+)\)',text):
  if dest.startswith(('http','mailto:','#')):continue
  target=(R/file).parent/dest.split('#')[0]
  # Markdown parentheses in source filenames need URL encoding; reports use folder locators.
  if not target.exists():issues.append((file,dest))
result={'checked_at':datetime.datetime.now().astimezone().isoformat(),'counts':{'S':48,'F':102,'Q':20,'E_proposed':18,'E_executed':15,'K':15},'missing_relative_links':issues,'files':{f:{'bytes':(R/f).stat().st_size,'sha256':hashlib.sha256((R/f).read_bytes()).hexdigest()} for f in files}}
(R/'_WORK/COLLECTOR_FREEZE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=True,indent=2))
