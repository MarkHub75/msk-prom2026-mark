from pathlib import Path
import re,json,hashlib
W=Path(__file__).resolve().parent;R=W.parent
A=json.loads((W/'COLLECTOR_ATOMIC_MANIFEST.json').read_text(encoding='utf-8'))

# Link normalization against the final assigned atomic IDs (not proposed IDs).
qmap={1:{64:63},2:{51:50,53:52,56:55},3:{64:63},4:{63:62},7:{49:48,50:49},8:{49:48,50:49},9:{52:51},10:{51:50},11:{60:59},12:{53:52,54:53,55:54},13:{61:60},14:{56:55,57:56,62:61},15:{62:61},16:{59:58},17:{51:50,53:52,55:54},18:{65:64,66:65,67:66,68:67,69:68},19:{63:62,64:63},20:{69:68}}
emap={1:{64:63},2:{51:50,53:52,56:55},3:{67:66,69:68},4:{69:68},5:{49:48,50:49,65:64},6:{51:50,52:51,67:66},7:{53:52,54:53,55:54,67:66},8:{60:59,61:60,62:61},9:{65:64,66:65,67:66,68:67,69:68},10:{59:58}}
t=(R/'OPEN_QUESTIONS.md').read_text(encoding='utf-8')
for prefix,mp in [('Q',qmap),('E',emap)]:
    for n,trans in mp.items():
        ident=f'{prefix}{n:03d}';patt=r'(<a id="'+ident+r'"></a>)(.*?)(?=<a id="[QE]\d{3}"></a>|\Z)'
        def repl(m):return m[1]+re.sub(r'F(\d{3})',lambda z:f'F{trans.get(int(z[1]),int(z[1])):03d}',m[2])
        t=re.sub(patt,repl,t,flags=re.S)
(R/'OPEN_QUESTIONS.md').write_text(t,encoding='utf-8')

# Compact the registry without dropping any exact URL or provenance/F relation.
s=(R/'SOURCES.md').read_text(encoding='utf-8')
prefix=s[:s.index('<a id="S001">')]
blocks=re.split(r'(?=<a id="S\d{3}"></a>)',s[s.index('<a id="S001">'):])
new=[prefix]
for block in blocks:
    if not block.strip():continue
    if '<a id="S001">' in block:new.append(block);continue
    tail=''
    if '\n## Важные недоступные' in block:block,tail=block.split('\n## Важные недоступные',1);tail='\n## Важные недоступные'+tail
    sid=re.search(r'<a id="(S\d{3})"',block)[1]
    title=re.search(r'^## '+sid+r' — (.+)$',block,re.M)[1]
    url=re.search(r'^Прямой URL: (\S+)',block,re.M)[1]
    typ=re.search(r'\*\*Точный тип источника:\*\* ([^\n]+)',block)
    path=url.split('?')[0].rstrip('/').split('/')[-1]
    if not typ:
        if 'raw.githubusercontent.com' in url:stype='первичный versioned исходный файл '+path
        elif re.search(r'\.(pt|pth|onnx|safetensors)$',path):stype='конкретный weight/model artifact '+path
        elif re.search(r'\.(mp4|avi|mov|zip|rar)$',path):stype='конкретный media/archive artifact '+path
        elif '/api/' in url or 'api.github.com' in url:stype='первичный API/manifest/metadata endpoint'
        elif '/blob/' in url or '/tree/' in url:stype='versioned repository file/tree '+path
        elif 'license' in url.lower() or 'legalcode' in url.lower():stype='первичный лицензионный текст/owner policy'
        elif '.pdf' in url:stype='PDF документация/публикация'
        else:stype='author/publisher web document, dataset/model card или официальная документация'
        if title.endswith('/'+path) or path in ('README.md','LICENSE','LICENSE.md'):title=title+' — '+path
    else:stype=typ[1]
    own=re.search(r'Владелец/издатель: (.*?). Тип:',block)
    owner=own[1] if own else 'владелец указан в title и detailed locator'
    vers=re.search(r'/(?:blob|raw|resolve|tree)/([a-f0-9]{40}|v[^/]+)',url) or re.search(r'/([a-f0-9]{40})/',url)
    version=vers[1] if vers else ('versioned tag в URL; точный tag→commit в F' if re.search(r'/v\d',url) else 'immutable revision не установлена; current/дата публикации уточнены в F')
    pub='не установлена для этого URL; не подменяется accessdate'
    if '13354453' in url:pub='2024-08-21, dataset v2.1'
    elif 'xjmtb22pff' in url:pub='2024-06-11, dataset V1'
    elif '836749' in url:pub='2017-07-31, dataset v1'
    elif '2026_linq_presentation' in url:pub='2026 по титулу; точная дата публикации неизвестна'
    elif 'Framework_manual_H1' in url:pub='2025 по титулу; RU.РМДВ.04.06.014-03 34 01'
    elif 'releases/download/0.1.1rc0' in url:pub='release2021-08-18; asset created2021-08-18, breaking-changebody2021-08-19'
    elif 'releases/download/v8.3.0/yolov8n-pose.pt' in url:pub='release2024-09-29; embeddedmodeldate2023-04-17 отдельно'
    facts=sorted(set(re.findall(r'\[?(F\d{3})\]?\]\(RAW_FACTS.md#|RAW_FACTS.md#(F\d{3})',block)))
    facts=sorted({x for pair in facts for x in pair if x})
    origin=re.search(r'Локаторы происхождения: (.*?). Поддерживает ',block,re.S)
    origin=origin[1] if origin else 'точный canonical F + URL/path'
    # Keep complete branch locators; they are not copied evidence paragraphs.
    new.append(f'<a id="{sid}"></a>\n## {sid} — {title}\n\nURL: {url}\n\n- Владелец: {owner}. Тип: {stype}\n- Версия/файл: `{version}`; filename/endpoint `{path}`. Публикация/версиядаты: {pub}. Доступ/проверки веток: **2026-10-23**.\n- Точный source locator: `{urlparse_locator(url) if False else path}`; {origin}.\n- Факты/условия/действительно выполненные проверки/раздельные grants: '+', '.join(f'[{f}](RAW_FACTS.md#{f})' for f in facts)+'. HEAD/metadata, fullGET, structural scan и inference не взаимозаменяемы; конкретный статус указан в F.\n'+tail)
(R/'SOURCES.md').write_text('\n'.join(new),encoding='utf-8')

statuses=[
('УТОЧНЕНО; условный shortlist, execution OPEN','W2-01/04/05/06 дали независимые временные переменные: pose transition+gross low-motion; rolling translation/gait contrast; moving machine+pair; visible flame region+allowed policy. Матрица F003 и shortlist F004 не умножают genericzone. Есть1preparedfall candidate и2conditional priorities, не2–3finished LinQ scenarios. Zone/corridor остаётся одной infrastructure fallback; acceptance сужений у организатора не получен.','F003 F004 F046 F047 F048 F051 F052 F054 F063','Q001 Q003 Q006 Q007 Q008 Q009 Q012','E001 E003 E005 E006 E007 E009'),
('OPEN — requires organizer/access','W2-01 повторно открыл docs/press/tech/sol: актуального публичного hackathon runbook/catalog не установлено. Guide2025 и benchmark2026 — реальные документы разных контекстов, не выданный matched SDK. Actual teamgrant/customupload/hostboundary/quota/deviceproof остаются неизвестными. Не повторять широкий поиск вместо выдачи доступа.','F010 F011 F063','Q001 Q002 Q003 Q019','E001 E002'),
('ЧАСТИЧНО ЗАКРЫТО metadata; ПРОТИВОРЕЧИЯ уточнены; parity/device OPEN','W2-02 получил fullYOLOX/officialpose/RTMPose bytes+SHA, actualgraphalloutputs/operators. Первый ownprobe YOLOX nano; RTMPose posebackup. YOLOX tagRGBnormalized/currentBGR/releasebody неоднозначность оставляет BGR documentedtesthypothesis, не empiricalgolden. RTMPose actualaxes symbolic, twooutputs; fullcallerBGRvsSDKRGB и mean/minscore конфликт подтверждён, выбранSDK/MMPose1.1reference. Officialpose8.3.0asset embedded8.0.77/AGPL не sourceversionGPLgrant. Checker/export/staticderivative/PTQ/compile/device не выполнялись.','F014 F036 F037 F038 F039 F040 F041 F042 F043','Q002 Q005 Q017','E002'),
('УТОЧНЕНО / short-tail data CLOSED; long-tail/full event OPEN','W2-03 fullGET/decode/allframe review6clips1048frames. S3F07 показывает переход и conservativegrosslowmotion[2.560033,8.992067]=6.432033s; S1F11stable2.208033s послеsettling. Bend/exercise/intentlying/cropunknown controls добавлены. H10/H30 нетeligiblepositive, EOFrightcensoring неclear. Recovery/rearm/movinglimb/hardindustrial/independentholdout ещё открыты; consciousness не измеряется.','F017 F046 F047','Q006 Q020','E003 E004 E009'),
('УТОЧНЕНО; synthetic internal route GO, complete real route OPEN/NO-GO сейчас','W2-04 скачал3_te1/7_te1: реальные motion/driver есть, уверенный отдельныйwalkingpedestrian не установлен. ИзNVIDIAZIP64 получены00238co-visiblemovingpair и00298partialfarcontrol,с CRC/SHA/PTS; generated,неrealnear-miss. Exactbest.pt fullhash/staticnames0forklift1person закрыты. Stationarynear/realpairGT/calibration/explicitweightscope/export/device отсутствуют. FavorablepublisherMITindex сохранён,не blanket no-license.','F021 F022 F050 F051','Q009 Q010 Q017','E002 E006'),
('УТОЧНЕНО; matched sample CLOSED, operational movement pack OPEN','W2-05 получил matchedWeizmann AVI CRC/SHA/PTS/review, encoded25FPS противpage50; physicalcaptureclock unknown. CHAD schema pinned, exactrunningepisode не получен безогромногоZIP; binaryabnormal неrunGT. Fastwalk/same-tracktransition/burst/camera-motion/floor calibration/publicWeizmanngrant отсутствуют. Translation/gait/policy не смешиваются.','F019 F020 F048 F049','Q007 Q008 Q017 Q020','E005'),
('УТОЧНЕНО; fire media/artifact metadata CLOSED, quality/device OPEN','W2-06 full5video decode/allframe review и2PTSHA/staticnames. Rabah/farhat оба0smoke1fireAGPL;rabah теперьpreferred поprovenance readiness,не measuredquality. FURGXMLxywhconfirmed,29vs29.97FPS/extraendrows/stalecutboxes/falseemptylabels найдены. Headlightconfuser/BBQallowed-policycandidate есть; cessation/smokeonly/targetsteam/welding пока нет. Fire часть№4 независима отsmoking. R3-E6 grant unknown/fulltree license negative reference.','F026 F052 F053 F054','Q012 Q017 Q020','E002 E007 E009'),
('ЧАСТИЧНО ЗАКРЫТО exact4 copyright identity; supply/use scopes УТОЧНЕНЫ/OPEN','W2-07 доказал exact2GMDCSA ZIPmemberbyteidentity и exact2SafeUnsafeprimarymanifestSHA==localfullSHA. Все4 имеют positiveprimaryCCBY4copyrightоснование; нельзя сохранять старое «mirrorunverified/лицензиивидеонет». Residualpersonalrelease/recordingscope отдельно и неавтоматическийresearch/livecopyrightban. YOLOXApachecode/officialreleaseprovenancepositive,explicitstandaloneweightscope неустановлен;RTMPoseuploaderApachedeclared;officialposeembeddedAGPL/source8.0.77GPLconflict preserved. ForkliftpublisherMITsignal/explicitscope и fireAGPL/thirdpartymedia отдельно. FutureSDK/compiledredistribution невыданы. Exactcredits/notices вF015.','F015 F026 F040 F041 F044 F045 F050 F052 F054','Q010 Q017','E002 E003 E006 E007 E008'),
('УТОЧНЕНО; bounded tracker route выбран; runtime/video OPEN','W2-08 проследил directByteTrack,empty-skippingUltralyticscallback и DeepSORTfixed-dt baseline. Выбранfixedanalysisgrid сemptyupdates,observedsidecar,classseparation,orderedtickcommit; dt1 имеет смысл в шагахсетки,frame_rateменяетTTLнеF/Q. Новыйordercounterexample: associationраньшеexpiryможетreactivateexpiredlost;strictTTLтребуетprepruneadapter. Constructorarithmetic выполнена,realtracker/video/deviceexperienceнет.','F034 F064 F065 F069','Q018 Q019','E005 E009'),
('УТОЧНЕНО; official provenance/text strengthened; bytes/visual/methodology OPEN','W2-01нашёлofficialpress→PDF иindependenttextparser13pages,строки/footersповторились. TLS/requests/curlfailed; screenshotresulttextonlyнеvisualreview. НетfullPDFSHA/images/matchedmodel/inputprecision/timerscenario. Pose104.8/21.51 vs419.2/21.51остаётся text-extractedreportedmeasurement,visualverificationunavailable;неcheckpointproof/SLA,1/FPSнеlatency,ResNetpage3/4differenceсохранена.','F010 F013 F062','Q004 Q019','E001 E005'),
('УТОЧНЕНО; единый design выбран, executable integration OPEN','W2-08 поставил person/pair/fireregion contract,candidate/open/update/unknown/clear/rearm,initialoccupancy/censoring,observedvspredicted;keyedledger/outbox/UIview иone-to-oneeventmatching/rawcounts.14timelines разбираютTTL/gap/twopeople/IDambiguity/retry/outoforder/restart/clear/reentry. Этоsource-backeddesign/арифметика,неприложение/once-visiblePASS. E009долженпоказатьactualUI/journalconsumerguarantee;disparateW1gatesсохраняютсятолькокакproposals,нерейтингкачества.','F033 F034 F066 F067 F068','Q006 Q018 Q019 Q020','E003 E004 E009')
]
c=(R/'CRITIC.md').read_text(encoding='utf-8')
marker='\n## Результаты второй волны — дополнение сборщика'
if marker in c:c=c.split(marker)[0]
history_sha=hashlib.sha256(c.encode('utf-8')).hexdigest()
c+=marker+'\n\nСборка2026-10-23, Europe/Moscow(UTC+3). Исходная критика и задания выше сохранены; `pending` относится к историческому срезу доW2. Текущие статусы ниже — результат16W1+8W2, не отдельный финальный аудит и не новая сеть. Ни одного аппаратного/событийногоPASS исследование не создало.\n'
for i,(status,body,facts,qs,es) in enumerate(statuses,1):
    k=f'K{i:03d}';atomic=[a for a in A if a['id'] in facts.split()];src=sorted({ss for a in atomic for ss,u in a['sources']})
    c+=f'\n<a id="{k}"></a>\n### {k} — исход второй волны\n\n**Текущий статус: {status}.**\n\n{body}\n\n**Доказательства W2 → F/S:** '+', '.join(f'[{x}](RAW_FACTS.md#{x})' for x in facts.split())+'; '+', '.join(f'[{x}](SOURCES.md#{x})' for x in src)+'.\n\n**Остаток Q/E:** '+', '.join(f'[{x}](OPEN_QUESTIONS.md#{x})' for x in qs.split())+'; '+', '.join(f'[{x}](OPEN_QUESTIONS.md#{x})' for x in es.split())+'.\n'
(R/'CRITIC.md').write_text(c,encoding='utf-8')
(W/'COLLECTOR_HISTORY_SHA.json').write_text(json.dumps({'critic_original_prefix_sha256':history_sha,'outcomes_added':11},indent=2),encoding='utf-8')

# Canonical links integrity: one explicit anchor per ID and existing portable targets.
files=['SOURCES.md','RAW_FACTS.md','OPEN_QUESTIONS.md','CRITIC.md']
anchors={f:re.findall(r'<a id="([SFQEK]\d{3})"></a>',(R/f).read_text(encoding='utf-8')) for f in files}
issues=[]
for f,ids in anchors.items():
    if len(ids)!=len(set(ids)):issues.append((f,'duplicate anchors'))
for f in files:
    body=(R/f).read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)',body):
        if target.startswith(('https://','http://','mailto:')):continue
        path,sep,frag=target.partition('#'); dest=f if not path else path
        if not (R/dest).exists():issues.append((f,'missing target',target))
        elif frag and re.fullmatch(r'[SFQEK]\d{3}',frag):
            if frag not in anchors.get(dest,[]):issues.append((f,'missing canonical anchor',target))
    if re.search(r'turn\d+(?:search|view|fetch)\d+',body):issues.append((f,'browser citation leftover'))
# Correct a genuinely missing historical link in quoted branch prose to a plain locator.
for f,kind,*rest in list(issues):
    if kind!='missing target':continue
    target=rest[0]
    body=(R/f).read_text(encoding='utf-8')
    body=body.replace(']('+target+')','] (исторический локатор `'+target+'`, файл не найден в поставке)')
    (R/f).write_text(body,encoding='utf-8')
issues=[x for x in issues if x[1]!='missing target']
stats={f:{'bytes':(R/f).stat().st_size,'anchors':len(anchors[f])} for f in files}
(W/'COLLECTOR_LINK_CHECK.json').write_text(json.dumps({'stats':stats,'issues':issues,'purpose':'in-role assembly consistency; no separate audit agent/stage'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'stats':stats,'issues':issues},ensure_ascii=False))
