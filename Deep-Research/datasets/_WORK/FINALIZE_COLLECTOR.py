from pathlib import Path
import re,json,datetime
R=Path(__file__).resolve().parent.parent
p=R/'RAW_FACTS.md';t=p.read_text(encoding='utf8')
terms={
'Conditionalmedicalface':'Conditional medical face','Currentonlinewebapplication':'Current online web application','Dangerousfilename':'Dangerous filename','Deformedmaskoverlay':'Deformed mask overlay','Dprojectionambiguity':'D projection ambiguity','Exactretrievalprepared':'Exact retrieval prepared','Exampleannotation':'Example annotation','Exhaustiveprotocol':'Exhaustive protocol','HMDBcurrentofficial':'HMDB current official','MOTdetectorvariants':'MOT detector variants','Noncommercialresearch':'Noncommercial research','PPEeventbenchmark':'PPE event benchmark','Syntheticplumbing':'Synthetic plumbing','USGovernmentconditions':'US Government conditions','YOLOnormalizedcxcywh':'YOLO normalized cxcywh','additionaltextnotices':'additional text notices','alertsperoperationalhour':'alerts per operational hour','auxiliarybranches':'auxiliary branches','blanketcommercialclearance':'blanket commercial clearance','cigarettevisibility':'cigarette visibility','closedcigaretteontology':'closed cigarette ontology','clotheschestregion':'clothes chest region','conditionalcrowdannotationfallback':'conditional crowd annotation fallback','conditionalobject':'conditional object','documentedbundled':'documented bundled','employeepermissions':'employee permissions','exhaustiveperpersonstate':'exhaustive per-person state','fragmentationfixture':'fragmentation fixture','grantredistribution':'grant redistribution','imagepixelcomparison':'image pixel comparison','imageredistributionprohibited':'image redistribution prohibited','inconvenientobjects':'inconvenient objects','incorrectfacelevelposition':'incorrect face-level position','independenceguarantee':'independence guarantee','independentscenes':'independent scenes','industrialloadingdock':'industrial loading dock','instructionsroute':'instructions route','labelednotvisible':'labeled not visible','localtrackingregression':'local tracking regression','makeavailabledatasetwholeorpart':'make available dataset whole or part','missingmediaannotations':'missing media annotations','occlusionvisibility':'occlusion/visibility','officialdocumentation':'official documentation','partiallyoccluded':'partially occluded','personcomplianceboxes':'person compliance boxes','positivefiltereddata':'positive filtered data','possiblethirdparty':'possible third party','reflectivevestconfusers':'reflective vest confusers','representativefalse':'representative false','separatedintegerx':'separated integer x','splitintersections':'split intersections','subjecttoopensource':'subject to open source','symmetricdifference':'symmetric difference','trackerregression':'tracker regression','upstreamexactmatchesunknown':'upstream exact matches unknown','upstreamphotoclearance':'upstream photo clearance','неаудированынами':'не аудированы нами','описываетпоставку':'описывает поставку','принеобязательном':'при необязательном','сообщеныавторами':'сообщены авторами','неавтоматическая':'не автоматическая',
'nonnegative':'nonnegative','cameraID':'camera ID','cameraIDs':'camera IDs','parentIDs':'parent IDs','subjectIDs':'subject IDs','trackID':'track ID','trackIDs':'track IDs','eventGT':'event GT','objectGT':'object GT','sourceGT':'source GT','allclasses':'all classes','smallobjects':'small objects','faceguard':'faceguard','lightmanifest':'light manifest','version1':'version 1','samplecounts':'sample counts','partiallabels':'partial labels','labelnoise':'label noise','ordinaryhats':'ordinary hats','sourceimage':'source image','bodyregion':'body region','subjectoverlap':'subject overlap','negativeGT':'negative GT','sourcephotos':'source photos','outputfile':'output file','maskbbox':'mask bbox','facebox':'face box','safeparser':'safe parser','cliplabels':'clip labels','classlabels':'class labels','groupIDs':'group IDs','groupID':'group ID','perimage':'per image','sourceURL':'source URL','exactmedia':'exact media','fulltar':'full tar','retailshop':'retail shop','framedimensions':'frame dimensions','generationscenarios':'generation scenarios','completeaudit':'complete audit','labelaudit':'label audit','sourcepixel':'source pixel','notvisible':'not visible','notlabeled':'not labeled','trueabsence':'true absence','crossdataset':'cross-dataset','sameimage':'same image','usecase':'use case','nodecode':'no decode','videoFPS':'video FPS','recordIDs':'record IDs','parentmedia':'parent media','perperson':'per person','pairedsample':'paired sample','dataactions':'data actions','targetclasses':'target classes','sourceclasses':'source classes','sourcefamilies':'source families','sourcefamily':'source family','classbalance':'class balance','trainvalsplit':'trainval split','referencecounts':'reference counts','samplingmethod':'sampling method','targetcamera':'target camera','CCTVtransfer':'CCTV transfer','rawlabels':'raw labels','rawoff':'raw off','sourcehash':'source hash','mediahash':'media hash','manualreview':'manual review','falsepositive':'false positive','absencelabels':'absence labels','mixedstates':'mixed states','rawstate':'raw state','sourceprotocol':'source protocol','IDlifecycle':'ID lifecycle','countconflict':'count conflict','framesampling':'frame sampling','datasetassembly':'dataset assembly','archiveREADME':'archive README','Layeredrights':'Layered rights','targetscale':'target scale','calibrationinput':'calibration input','personstate':'person state','workerstate':'worker state','sourceversion':'source version','annotationversion':'annotation version','filepaths':'file paths','coordinateframe':'coordinate frame','sourcecount':'source count','fullclass':'full class','seedunknown':'seed unknown','noticesunknown':'notices unknown',
}
for a,b in terms.items():t=t.replace(a,b)
# Fine spacing is prose-only: backticks, URLs and filenames remain exact.
parts=re.split(r'(`[^`\n]*`|https?://[^\s)]+|\]\([^\n]*?\))',t)
for i in range(0,len(parts),2):
 x=parts[i]
 x=re.sub(r'([,;])(?=[A-Za-zА-Яа-яЁё])',r'\1 ',x)
 x=re.sub(r'([А-Яа-яЁёA-Za-z])(?=(?:SHEL5K|SHWD|SH17|SFCHD|CHV|CPPE|SARD)\b)',r'\1 ',x)
 parts[i]=x
t=''.join(parts)
p.write_text(t,encoding='utf8')

# Source aliases: a single branch entry sometimes cites multiple primary artifacts.
sm={
'W1-01':[41,36,[1,2],[20,23],[30,31],32,17,46],
'W1-02':[1,2,3,3,5],
'W1-03':[9,12,[14,15],[17,18]],
'W1-04':[20,20,23,23,23,24,[1,2]],
'W1-05':[36,37,[1,2,5],38,40,40],
'W1-06':[25,28,33,29,27],
'W1-07':[30,31,32,32,45,46],
'W1-08':[42,43,44,44],
'W1-09':[9,12,[14,15],[17,18],33],
'W1-10':[2,7,1,8,9,11,12,15,22,41,25,36,45,30,32,17,47],
'W1-11':[1,5,5,20,[20,22],36,[17,18]],
'W1-12':[9,12,15,18,[2,5],23],
'W1-13':[[1,2],41,[20,23],[17,18],[30,31],32],
'W1-14':[1,[2,3],44,42,36,40,[9,12,14,15,17,18]],
'W1-15':[9,12,15,18,25,33],
'W2-01':[3,4,[2,5]],'W2-02':[[2,5],6,6],
'W2-03':[18,19,18],'W2-04':[17,19,19],
'W2-05':[9,10,10],'W2-06':[12,13,13],'W2-07':[15,14,16,16],
'W2-08':[21,21,21,22,23,20],'W2-09':[27,25,26],
'W2-10':[30,30,30],'W2-11':[32,32,32,32],
'W2-12':[17,[2,3],7,8,22,[9,11,12,15,30,36],[19,30],[37,39]],
'W2-13':[18,5,23,17],'W2-14':[36,37,39,39],
'W2-15':[33,34,35,33]}
fm={
'W1-01':[88,88,88,89,80,80,4],
'W1-02':[6,6,9,5,8,17,12,18,19],
'W1-03':[42,[42,44],43,45,46,47,47,49,[50,51],53,53,55,55,23,24,25,25,[27,28,30]],
'W1-04':[56,58,[56,58],59,[59,62],61,[57,60],94,[20,56]],
'W1-05':[80,80,82,11,83,83,87,87,87,87],
'W1-06':[63,63,63,64,63,95,76,77,79,95],
'W1-07':[67,68,70,71,72,72,73,75,95,96],
'W1-08':[90,90,91,90,91,91,91,92,92,93,93],
'W1-09':[42,46,50,99,26,32,31,76,78],
'W1-10':[18,18,45,49,55,60,89,64,82,95,71,[35,75],94],
'W1-11':[5,12,10,11,20,10,56,58,61,80,25],
'W1-12':[53,[25,28],8,12,20,58],
'W1-13':[19,88,62,[23,37,39],67,73,40,40],
'W1-14':[9,9,22,12,92,92,90,99,[27,30,32],80,87],
'W1-15':[43,47,50,50,[24,27,28],30,35,63,76],
'W2-01':[6,12,13,13,16],
'W2-02':[14,14,15,15,14,15,15,16,20,16],
'W2-03':[28,29,30,31,27],
'W2-04':[32,33,34,23,35],
'W2-05':[43,43,44,44,44],
'W2-06':[47,47,47,48,48,48],
'W2-07':[50,51,54,52,54,53,55,55],
'W2-08':[58,59,60,61,60],
'W2-09':[65,65,66,63,64],
'W2-10':[68,69,69,70,71],
'W2-11':[74,74,73,73,72],
'W2-12':[35,18],
'W2-13':[38,19,12,39,[16,61],29],
'W2-14':[81,81,82,84,85,85],
'W2-15':[77,77,78,76,79,79]}
def ids(prefix,vals):
 if isinstance(vals,int):vals=[vals]
 return '/'.join(f'{prefix}{i:03d}' for i in vals)
qmap={1:[1,19,8,17],2:[4,5,3],3:[9,10,11,8],4:[1,12,12,5],5:[17,18,19],6:[13,14,16],7:[14,15,15,19],8:[19,20],9:[10,20],10:[3,12,3,15],11:[5,20],12:[1,20],13:[2,2,8,2],14:[20,8],15:[3,20]}
eplan={1:[15,4],2:[1,4,6],3:[3,4,7],4:[4,8],5:[4,5,14],6:[2,12,10],7:[13,13,11],8:[9,9],9:[6],10:[14,14],11:[4,3,5],12:[3,15],13:[8,8,12],14:[18,6,6,7,7],15:[1]}
q2={1:[4,4,3],2:[5,4,5],3:[6,7],4:[8,3],5:[9,3],6:[10,3],7:[11,11,9],8:[12,12],9:[13],10:[14],11:[15],12:[3,3,12],13:[2,12],14:[17,18],15:[16,16]}
execmap={1:19,2:20,3:21,4:22,5:23,6:24,7:25,8:26,9:27,10:28,11:29,12:30,13:31,14:32,15:33}
rows=['# Сопоставление веточных ID с общими\n','Фиксация collector: 23.10.2026, Europe/Moscow. S/F/Q/E общие; K001–K015 сохранены. Многие веточные записи объединены; список через `/` означает несколько оснований/аспектов. Повторный пересказ одной статьи не независимый источник. Сокращённые F01/S01 внутри веточной card понимаются с префиксом её имени. E019–E033 — выполненные bounded checks; E001–E018 — предложенные программы, их статусы нельзя смешивать.\n','## Источники\n\n| Local | Global |\n|---|---|']
for branch,arr in sm.items():
 for i,val in enumerate(arr,1):rows.append(f'|{branch}-S{i:02d}|{ids("S",val)}|')
rows+=['\n## Факты\n\n| Local | Global |\n|---|---|']
for branch,arr in fm.items():
 for i,val in enumerate(arr,1):rows.append(f'|{branch}-F{i:02d}|{ids("F",val)}|')
rows+=['\n## Вопросы и программы\n\n| Local namespace | Global | Status/правило |\n|---|---|---|']
for wave in [1,2]:
 for num in range(1,16):
  branch=f'W{wave}-{num:02d}';text=(R/'_WORK'/f'{branch}.md').read_text(encoding='utf8')
  qs=qmap[num] if wave==1 else q2[num]
  for i,val in enumerate(qs,1):rows.append(f'|{branch}-Q{i:02d} / Q-{branch}-{i:02d}|Q{val:03d}|Канонизация полного/сокращённого Q; родственные уточнения объединены|')
  if wave==1:
   for i,val in enumerate(eplan[num],1):rows.append(f'|{branch}-E{i:02d}|E{val:03d}|Предложенная программа; выполненные компоненты отдельно в facts|')
  else:
   rows.append(f'|E-{branch}-01 / {branch}-E01|E{execmap[num]:03d}|Выполненный bounded check, scope в реестре E|')
   # Subsequent proposed checks are routes, not a retroactive measurement.
   routes={1:[1,3],2:[4,5],3:[1,2,3,7],4:[7,14],5:[4,14],6:[5,6,14],7:[4,7],8:[14,4],9:[12],10:[13],11:[11],12:[14],13:[8],14:[2,4,5],15:[10,14]}[num]
   rows.append(f'|{branch}: последующие proposed E/процедуры|{ids("E",routes)}|Не выполнено; точный inputs/actions/scope в OPEN_QUESTIONS|')
rows+=['\nНекоторые ветки описывают практическую процедуру без локального E-ID; она получила глобальный программный E-ID по предмету. Сводные F001–F004/F097–F102 — synthesis/proposed, а не новые первичные наблюдения. W1-13-F04 исправлен F039, W2-02-F08 уточнён F016, W1 CPPE code-only rights уточнены F060; история не удалена.','\n## Реальные inputs/freeze\n\nВсе W1/W2 прочитаны полностью; использованы сохранённые первичные JSON/XML/README/author comment/PDF/legal text и visual contact sheets. Нового поиска/обучения/массового media audit нет. Outputs: SOURCES.md, RAW_FACTS.md, OPEN_QUESTIONS.md, добавление CRITIC.md, этот ID_MAP и AUTHOR_BRIEF.']
(R/'_WORK'/'ID_MAP.md').write_text('\n'.join(rows)+'\n',encoding='utf8')
# Explicit source anchors and reverse support index.
s=R/'SOURCES.md';st=s.read_text(encoding='utf8')
for name in ['Physical AI','SHEL5 K','Lin Q']:st=st.replace(name,{'Physical AI':'PhysicalAI','SHEL5 K':'SHEL5K','Lin Q':'LinQ'}[name])
st=st.split('\n## Обратный индекс')[0]
st+='\n## Обратный индекс поддерживаемых фактов\n\n'
fs=list(re.finditer(r'^### (F\d{3}) —',t,re.M))
for n in range(1,49):
 sid=f'S{n:03d}';support=[]
 for i,m in enumerate(fs):
  chunk=t[m.start():fs[i+1].start() if i+1<len(fs) else len(t)]
  if re.search(r'\b'+sid+r'\b',chunk):support.append(m[1])
 st+=f'- **{sid}:** '+(', '.join(support) or 'Контекст/terms в связанных карточках, без отдельного значимого F.')+'\n'
s.write_text(st,encoding='utf8')
print('ID_MAP source aliases',sum(map(len,sm.values())),'fact aliases',sum(map(len,fm.values())))
