"""Offline evidence assembly. Reads saved worker paraphrases; no fetching/execution."""
from pathlib import Path
import re, json, hashlib
from urllib.parse import urlsplit, urlunsplit

ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'_WORK'
REPORTS=sorted(WORK.glob('W[12]_??.md'))
ID=re.compile(r'W([12])[-_](\d{2})[-_]([SFQE])(\d{2,3})')
URL=re.compile(r'https?://[^\s<>\]\)\|]+')
def canon_id(s):
    return ID.sub(lambda m:f'W{m[1]}-{m[2]}-{m[3]}{int(m[4]):02}',s)
def urls(s): return list(dict.fromkeys(x.rstrip(';,。') for x in URL.findall(s)))
def chain(s):
    us=urls(s)
    if not us: return 'local:'+re.sub(r'\s+',' ',s)[:120]
    u=us[0]
    p=urlsplit(u)
    q=re.search(r'(?:github\.com/([^/]+/[^/]+)/blob/|raw\.githubusercontent\.com/([^/]+/[^/]+)/)([^/]+)',u)
    if q:
        repo=(q[1] or q[2]).lower(); ref=q[3]
        # Same verified MediaMTX/PyAV tags and commits are one chain.
        ref={'v1.21.2':'914e39535ece709919ac325aaeed98d394ed9093'}.get(ref,ref) if repo=='bluenviron/mediamtx' else ref
        if repo=='pyav-org/pyav' and ref=='v16.0.1': ref='7687256d87f22f78cb75bb4aba94dc6e504c9983'
        return repo+'@'+ref
    return urlunsplit((p.scheme,p.netloc.lower(),p.path.rstrip('/'),p.query,''))

reports={p.stem:canon_id(p.read_text(encoding='utf-8-sig')) for p in REPORTS}
source_items=[]; source_ranges={}
for name,body in reports.items():
    lines=body.splitlines(); prefix=name.replace('_','-'); excluded=set()
    for i,line in enumerate(lines):
        m=re.match(r'^\|\s*('+re.escape(prefix)+r'-S\d+)(?:\s+[^|]*)?\s*\|',line)
        if m:
            source_items.append((m[1],name,i+1,line.strip('| ')))
            excluded.add(i)
        m=re.match(r'^(?:###\s+|\*\*)('+re.escape(prefix)+r'-S\d+)\b',line)
        if m:
            j=i+1
            while j<len(lines):
                if re.match(r'^#{1,3}\s',lines[j]) or re.match(r'^(?:- )?\*\*'+re.escape(prefix)+r'-[FS]\d',lines[j]): break
                j+=1
            source_items.append((m[1],name,i+1,'\n'.join(lines[i:j])))
            excluded.update(range(i,j))
    # Whole source-registry sections (includes table headers/provenance, not just rows).
    starts=[i for i,l in enumerate(lines) if re.match(r'^## (?:Реестр.*источник|Источники|Первичные источники|Новые (?:перво)?источники)',l)]
    for i in starts:
        j=i+1
        while j<len(lines) and not lines[j].startswith('## '):j+=1
        excluded.update(range(i,j))
    source_ranges[name]=excluded

groups={}; smap={}
for old,name,line,body in source_items:
    k=chain(body)
    if old=='W1-05-S05':k='bluenviron/mediamtx@914e39535ece709919ac325aaeed98d394ed9093'
    if old=='W2-05-S01':k='pyav-org/pyav@7687256d87f22f78cb75bb4aba94dc6e504c9983'
    if old=='W2-03-S09':k='python-websockets/websockets@fd3f16cc4f57ace08e323a7806f1432e957cb75e'
    if old=='W1-04-S19':k='local:W1_04_provenance'
    if old=='W1-01-S01':k='local:linq_platform_package'
    if k not in groups:groups[k]={'id':f'S{len(groups)+1:03}','records':[],'key':k}
    groups[k]['records'].append({'old':old,'report':name,'line':line,'body':body})
    smap[old]=groups[k]['id']

# Secondary saved worker records are locatable evidence of analysis, not new primary chains.
local_s={}
for name in reports:
    sid=f'S{len(groups)+1:03}';local_s[name]=sid
    groups['local:'+name]={'id':sid,'key':'local:'+name,'records':[{'old':name+'-LOCAL','report':name,'line':1,'body':f'Локальный исследовательский результат [{name}](_WORK/{name}.md), доступ/получение 2026-10-23. Автор: назначенный Medium исследователь соответствующей волны. Тип LOCAL/вторичный аналитический пакет. Version: сохранённый файл; SHA256 в _WORK/COLLECTOR_INPUT_HASHES.json. Фактически: чтение/получение источников и явно указанные metadata/арифметика; runtime не запускался. Не независимое подтверждение изложенных в нём первичных chains.'}]}

# Worker fact definitions, including grouped definitions (F07–F08 etc).
def fact_start(line,prefix):
    if not re.match(r'^(?:#{1,5}\s+|(?:- )?\*\*)',line):return None
    m=re.search(re.escape(prefix)+r'-F(\d{2})(?:[–-]F(\d{2}))?',line)
    if m and m.start()<35:return m
    return None

facts=[]; fmap={}; supplements=[]; exp_sections=[]; q_sections=[]
for name,body in reports.items():
    lines=body.splitlines(); prefix=name.replace('_','-')
    # Split at ## headers, except ## F definitions remain ordinary content.
    starts=[0]+[i for i,l in enumerate(lines) if i and (l.startswith('## ') or re.match(r'^### W1-04-P\d',l))]
    starts.append(len(lines))
    for a,b in zip(starts,starts[1:]):
        block='\n'.join(l for i,l in enumerate(lines[a:b],a) if i not in source_ranges[name]).strip()
        if not block: continue
        header=lines[a] if a else 'Введение/решение'
        if re.search(r'^## (?:Предлагаемые эксперименты|Эксперименты|Программа практической|Проект практических|Proposed experiments|Proposed E|Предложенные E|Discriminating E)',header):
            exp_sections.append((name,a+1,block));continue
        if re.search(r'^## (?:Точные открытые|Открытые вопросы|Локализованные пробелы|Неизвестные|Unknown/|Открытое|Локализованные неизвестные|Unknown и|Отрицательные результаты и вопросы|Матрица K и остаток неизвестного)',header):
            q_sections.append((name,a+1,block));continue
        bl=block.splitlines(); fst=[i for i,l in enumerate(bl) if fact_start(l,prefix)]
        if not fst:
            # Provenance is recorded once, K processing in CRITIC, introductions/duplicate decision summaries aren't new facts.
            if a==0 or re.search(r'^## (?:Ответ,|Вывод,|Вывод для|Решения,|Главные решения|Что меняет решение|Изменение решения|Матрица|Решение$|Решение,|Получение и ограничения)',header):continue
            if re.search(r'^## Каталог единой схемы',header):continue
            if len(block)<80:continue
            supplements.append({'report':name,'line':a+1,'body':block,'title':header.lstrip('# ')});continue
        if fst[0]>0:
            lead='\n'.join(bl[:fst[0]]).strip()
            if len(lead)>100:supplements.append({'report':name,'line':a+1,'body':lead,'title':header.lstrip('# ')+' — контекст'})
        for n,i in enumerate(fst):
            j=fst[n+1] if n+1<len(fst) else len(bl)
            raw='\n'.join(bl[i:j]).strip();m=fact_start(bl[i],prefix)
            olds=[f'{prefix}-F{k:02}' for k in range(int(m[1]),int(m[2] or m[1])+1)]
            rec={'report':name,'line':a+i+1,'body':raw,'old':olds,'title':bl[i].strip('#* ')}
            facts.append(rec)

# The NVDEC13.0 table is the same primary measurement in both workers.
alias={'W1-06-F02':'W1-02-F21','W1-04-F12':'W1-03-F10','W2-06-F05':'W2-04-F10'}
for rec in facts:
    target=next((fmap[alias[o]] for o in rec['old'] if o in alias and alias[o] in fmap),None)
    fid=target or f'F{len(set(fmap.values()))+1:03}'
    rec['id']=fid
    for old in rec['old']:fmap[old]=fid
base_count=len(set(fmap.values()))
for i,rec in enumerate(supplements,1):rec['id']=f'F{base_count+i:03}'
allfacts=facts+supplements
# Locate definitions in the original saved file, before source-section extraction.
for rec in facts:
    pref=rec['report'].replace('_','-');num=int(rec['old'][0].split('-F')[-1])
    for lineno,line in enumerate(reports[rec['report']].splitlines(),1):
        found=fact_start(line,pref)
        if found and int(found[1])==num:rec['line']=lineno;break

# Extract experiment/question items, retaining section-level context as their evidence.
def extract_items(sections,kind):
    records=[]
    for name,line,body in sections:
        prefix=name.replace('_','-'); ls=body.splitlines()
        starts=[]
        for i,l in enumerate(ls):
            # Table, bold or heading definitions; also local Qxx bullets in W1_04.
            m=re.search(re.escape(prefix)+r'-'+kind+r'(\d{2})\b',l)
            if m and (l.startswith('|') or l.startswith('**') or l.startswith('#') or l.startswith('- ') or l.startswith('* ')):
                starts.append((i,prefix+'-'+kind+m[1]))
            elif kind=='Q':
                m=re.match(r'^- Q(\d{2})[, ]',l)
                if m:starts.append((i,prefix+'-Q'+m[1]))
        for k,(i,old) in enumerate(starts):
            j=starts[k+1][0] if k+1<len(starts) else len(ls)
            # Table item is exactly one row; non-row tail should not absorb next unrelated section.
            if ls[i].startswith('|'):j=i+1
            text='\n'.join(ls[i:j]).strip()
            records.append({'old':old,'report':name,'line':line+i,'body':text,'context':ls[0]})
    return records
exps=extract_items(exp_sections,'E');questions=extract_items(q_sections,'Q')
emap={r['old']:f'E{i:03}' for i,r in enumerate(exps,1)}
qmap={r['old']:f'Q{i:03}' for i,r in enumerate(questions,1)}
mapping={**smap,**fmap,**emap,**qmap}

def norm(s,name=None,links=True):
    s=canon_id(s)
    # Explicit neighbouring namespace applies to its whole slash/range reference.
    def cross(m):
        pref=m[1].replace('_','-');kind=m[2]
        seq=m[3];out=[]
        for part in seq.split('/'):
            nums=re.findall(r'\d{2}',part)
            for n in range(int(nums[0]),int(nums[-1])+1):
                old=f'{pref}-{kind}{n:02}'
                out.append(mapping.get(old,old))
        return ', '.join(dict.fromkeys(out))
    s=re.sub(r'(W[12][-_]\d{2})[-/]([SFQE])((?:\d{2}(?:[–-][SFQE]?\d{2})?)(?:/[SFQE]\d{2}(?:[–-][SFQE]?\d{2})?)*)\b',cross,s)
    # The worker uses short S/F/Q/E references in its own namespace.
    if name:
        pref=name.replace('_','-')
        def localrange(m):
            kind=m[1]
            return ', '.join(dict.fromkeys(mapping.get(pref+f'-{kind}{i:02}',f'{kind}{i:02}') for i in range(int(m[2]),int(m[3])+1)))
        s=re.sub(r'(?<![\w-])([SFQE])(\d{2})[–-][SFQE]?(\d{2})(?!\w)',localrange,s)
        s=re.sub(r'(?<![\w-])([SFQE])(\d{2})(?!\w)',lambda m:mapping.get(pref+'-'+m[0],m[0]),s)
    s=ID.sub(lambda m:mapping.get(m[0],m[0]),s)
    # All worker-relative local links move one directory up in final files.
    s=re.sub(r'(?<!!)(\]\()(?:\./)?MATERIALS/',r'\1_WORK/MATERIALS/',s)
    s=re.sub(r'(?<!!)(\]\()(W[12]_\d{2}\.md)',r'\1_WORK/\2',s)
    s=s.replace('](../../research_link_platform/','](../research_link_platform/')
    s=s.replace('](_WORK/MATERIALS/','](_WORK/MATERIALS/')
    return s

def inferred_type(body,old=None):
    if re.search(r'^### W1-04-P\d',body):return 'DOC/CODE/INFERENCE'
    lead=body.split('\n\n',1)[0]
    known=['CLAIM','DOC','CODE','MEASURED','LOCAL','INFERENCE','HYPOTHESIS','UNKNOWN']
    found=[t for t in known if re.search(r'\b'+t+r'(?:\b|_)',lead)]
    if found:return '/'.join(found)
    return 'INFERENCE'

def source_refs(rec):
    ss=[]; pref=rec['report'].replace('_','-')
    if rec.get('old',[None])[0] in ['W1-01-F01','W1-01-F02','W1-01-F03','W1-01-F04']:ss.append(smap['W1-01-S01'])
    for m in re.finditer(r'(?<![\w-])S(\d{2})(?!\d)',rec['body']):
        old=pref+'-S'+m[1]
        if old in smap:ss.append(smap[old])
    for m in re.finditer(r'\bS(\d{2})[–-]S(\d{2})\b',rec['body']):
        ss.extend(smap[pref+f'-S{i:02}'] for i in range(int(m[1]),int(m[2])+1) if pref+f'-S{i:02}' in smap)
    for m in ID.finditer(rec['body']):
        if m[3]=='S' and m[0] in smap:ss.append(smap[m[0]])
    # Source table often declares supporting F, while fact body omits S.
    for old in rec.get('old',[]):
        local=old.split('-')[-1]
        for g in groups.values():
            if any(x['report']==rec['report'] and re.search(r'\b'+local+r'\b',x['body']) for x in g['records']):ss.append(g['id'])
    return list(dict.fromkeys(ss))

PROVENANCE='''Дата сборки и подтверждённая дата обращения: **2026-10-23 Europe/Moscow (UTC+3)**. Collector не получал новую сеть, не запускал приложения/камеры/SDK/LinQ и не выполнял предложенные E. W1 закончена до прерывания и не повторялась; несохранённый первый critic не восстанавливался. Сохранённый CRITIC создан отдельным fresh-context critic_resume, затем выполнены шесть W2 по K001–K010. Нет полного кейса, issued SDK/grant, actual LinQ output и runtime benchmark. Ранние интервалы W1_01/03 приблизительны: они не являются точным журналом отдельных обращений. SHA snapshot доказывает состав сохранённых bytes, а не неизменность current upstream или работу программы.\n'''

def build_sources():
    out=['# Источники video_architecture\n',PROVENANCE,'## Правило происхождения\n','Один S-ID объединяет одно первичное происхождение/ревизию; разные файлы той же pinned repo перечислены внутри записи. Ссылки повторных чтений не становятся независимыми измерениями. Current/live docs — **unfrozen**, если нет immutable revision; versioned docs тоже не автоматически immutable. Publication/commit/release приведены в исходных metadata ниже отдельно от access=2026-10-23. Неизвестная публикация — unknown. Прочитано исследователями; collector читал сохранённые извлечения и provenance.\n']
    for g in groups.values():
        sid=g['id'];refs=[]
        for r in allfacts:
            if sid in source_refs(r) or (g['key']=='local:'+r['report']):refs.append(r['id'])
        out += [f'<a id="{sid.lower()}"></a>\n',f'## {sid} — {g["key"]}\n',f'- Доступ: 2026-10-23; точные HTTP timestamps, где сохранены, — в provenance исходной записи.\n- Цепочка/алиасы: '+', '.join(x['old'] for x in g['records'])+'.\n- Поддерживаемые записи: '+(', '.join(dict.fromkeys(refs)) or 'каталог/проектные связи в RAW_FACTS; локаторы ниже')+'.\n']
        if g['key']=='pyav-org/pyav@7687256d87f22f78cb75bb4aba94dc6e504c9983':out.append('**Уточнение ревизии:** в W1 GitHub API hash lookup дал403, поэтому честно сохранён tag16.0.1 без SHA. W2_05 позднее разрешил tag в7687256d87f22f78cb75bb4aba94dc6e504c9983. Это уточнение provenance той же версии, не новое независимое измерение и не smoke install.\n')
        seen=set()
        for r in g['records']:
            txt=norm(r['body'],r['report'])
            if txt in seen:continue
            seen.add(txt)
            out.append(f'**Локатор сохранённого получения:** [_WORK/{r["report"]}.md:L{r["line"]}](_WORK/{r["report"]}.md).\n\n{txt}\n')
    out += ['## Важные недоступные материалы\n','Полный кейс и организаторские video/model artifacts — не получены; LinQ issued API/SDK/native/driver/firmware bundle и grant — не получены; actual target OS/ISA/runtime/build — unknown. Публичное предложение demo/download gate и аналитический пакет linq_platform не заменяют эти материалы. Уточнения — OPEN_QUESTIONS.md.\n']
    (ROOT/'SOURCES.md').write_text('\n'.join(out),encoding='utf-8')

def category(r):
    name=r['report'];old=r.get('old',[''])[0]; n=int(old.split('-F')[-1]) if '-F' in old else 0
    title=r['title']
    if name=='W1_01':
        if (1<=n<=7) or 'матрица доступа' in title:return '01 LinQ: доступ, размещение, происхождение'
        if 'передачи' in title.lower():return '12 Адресные передачи и отрицательные результаты'
        return '10 Поставка, Astra Linux и безопасность'
    if name=='W1_02':return '02 Ingress, RTSP, decode, clocks и library knobs'
    if name=='W1_03':
        if n in (11,12,15,16):return '03 Payload, JPEG quality, transport и bandwidth'
        if 'передач' in title or 'Отрицательные' in title:return '12 Адресные передачи и отрицательные результаты'
        return '04 Scheduler, bounded work, state и temporal contract'
    if name=='W1_04':
        if 3<=n<=13 or re.search(r'W1-04-P',title):return '05 Каталог проектов: version, license, hardware, reuse'
        if 'передач' in title:return '12 Адресные передачи и отрицательные результаты'
        if n>=19:return '06 Events, brokers, outbox, concurrency и DB boundaries'
        return '04 Scheduler, bounded work, state и temporal contract'
    if name=='W1_05':
        if n<=9:return '07 Evidence: сегменты, generations, mapping, pins и finite policy'
        if n<=20:return '08 Browser: identity, transport, render-credit и lifetime'
        return '06 Events, brokers, outbox, concurrency и DB boundaries'
    if name=='W1_06':
        if n==15:return '11 Capacity50/500 и полный resource inventory'
        return '09 Resilience, measurement и интерпретация benchmark'
    if name=='W2_01':return '01 LinQ: доступ, размещение, происхождение' if n<=13 else '03 Payload, JPEG quality, transport и bandwidth'
    if name=='W2_02':return '07 Evidence: сегменты, generations, mapping, pins и finite policy'
    if name=='W2_03':return '08 Browser: identity, transport, render-credit и lifetime'
    if name=='W2_04':return '04 Scheduler, bounded work, state и temporal contract'
    if name=='W2_05':return '10 Поставка, Astra Linux и безопасность' if n<=4 else '06 Events, brokers, outbox, concurrency и DB boundaries'
    if name=='W2_06':
        if n<=5:return '11 Capacity50/500 и полный resource inventory'
        if n<=8:return '09 Resilience, measurement и интерпретация benchmark'
        return '13 Conditional minimum45ч: placement, owners, gates, latency'
    return '12 Адресные передачи и отрицательные результаты'

def build_raw():
    out=['# Подробная доказательная база video_architecture\n',PROVENANCE,'## Как читать базу\n','CLAIM — заявление автора; DOC — первичная документация; CODE — прочитанный код; MEASURED — чужое опубликованное измерение с условиями; LOCAL — реально полученные локальные metadata/арифметика; INFERENCE — наш инженерный проект/вывод; HYPOTHESIS — кандидат; UNKNOWN — не установлено. Тип и исполнение раздельны. Любые runtime-команды и конфигурации здесь **proposed, не запускались**. Локальные арифметические расчёты не benchmark.\n\nСохранены исследовательские пересказы и точные параметры/команды обеих волн; это не копии внешних страниц. Повтор одного primary chain не даёт независимого подтверждения. W2 уточняет область W1; исходная W1 не является release lock. Каждый F имеет явный HTML anchor. Полная обратная карта — [_WORK/ID_MAP.md](_WORK/ID_MAP.md).\n']
    byid={}
    for r in allfacts:byid.setdefault(r['id'],[]).append(r)
    out.append('## Тематический навигатор\n\n'+ '\n'.join(f'- {c}' for c in sorted(set(category(rs[0]) for rs in byid.values())))+'\n')
    lastcat=None
    for fid,rs in sorted(byid.items(),key=lambda x:(category(x[1][0]),int(x[0][1:]))):
        r=rs[0];typ=inferred_type(r['body'])
        cat=category(r)
        if cat!=lastcat:out.append(f'# {cat}\n');lastcat=cat
        title=re.sub(r'W[12][-_]\d{2}[-_]F\d+(?:[–-]F\d+)?','',r['title'],count=1).strip(' —.*-')
        if title.startswith('['):title=re.sub(r'^\[[^]]*\][.*\s]*','',title)
        elif '.**' in title:title=title.split('.**',1)[1].lstrip()
        title=re.sub(r'^(?:DOC|CODE|CLAIM|MEASURED|LOCAL|INFERENCE|HYPOTHESIS|UNKNOWN)(?:/[A-Z]+)*:\s*','',title)
        title=re.sub(r'\s+',' ',norm(title,r['report'])).strip('* .:—-')
        if len(title)>150:title=title[:147].rsplit(' ',1)[0]+'…'
        ss=list(dict.fromkeys(x for rr in rs for x in source_refs(rr)))
        provenance_sources=list(dict.fromkeys(local_s[rr['report']] for rr in rs))
        out += [f'<a id="{fid.lower()}"></a>\n',f'## {fid} — {title}\n',f'**Тип основания:** {typ}. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. '+('Арифметика — локально вычислено, если явно указано ниже. ' if re.search(r'арифмет|arithmetic|LOCAL',r['body'],re.I) else '')+'Runtime/предлагаемые commands/configs: **не запускалось**.\n', '**Основание/контекст:** '+(', '.join(f'[{s}](SOURCES.md#{s.lower()})' for s in ss) if ss else 'INFERENCE/LOCAL по аналитическому источнику и связанным F ниже')+'. **Сохранённый аналитический источник:** '+', '.join(f'[{s}](SOURCES.md#{s.lower()})' for s in provenance_sources)+'. Версия, units, условия, ограничения и связи — в извлечении.\n']
        for rr in rs:
            text=rr['body']
            # Final integration explicitly points back to authoritative F rather than copying all A–E a second time.
            if rr.get('old')==['W2-06-F12']:
                text='INFERENCE: окончательное согласование A–E: tracker optional по cadence/reset gate (W2-04-F01–F13); полный cycle включает postprocess, remote credits не снимаются local Gap. Prospective artifact baseline и SQLite advisory/backup/restore — W2-05-F01–F12. Общие contracts до параллельной разработки: FrameEnvelope/StreamStatus; InferenceRequest/Result+transforms; JobLedger; OrderedResult/Gap/EpochReset/TrackingReset; EventMutation/revision/coverage; EvidenceManifest/status; processed wire/ACK. Positive/empty/error/late/old-generation fixtures обязательны. Это согласование proposals, не новый runtime факт.'
            out.append(f'**Происхождение:** [_WORK/{rr["report"]}.md:L{rr["line"]}](_WORK/{rr["report"]}.md)'+('; '+', '.join(rr['old']) if rr.get('old') else '; дополнительная тематическая выписка')+'.\n\n'+norm(text,rr['report'])+'\n')
    (ROOT/'RAW_FACTS.md').write_text('\n'.join(out),encoding='utf-8')

def dump_state():
    data={'sources':list(groups.values()),'facts':allfacts,'questions':questions,'experiments':exps,'question_sections':q_sections,'experiment_sections':exp_sections,'mapping':mapping,'source_map':smap,'fact_map':fmap,'question_map':qmap,'experiment_map':emap}
    (WORK/'COLLECTOR_STATE.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (WORK/'COLLECTOR_INPUT_HASHES.json').write_text(json.dumps({p.name:hashlib.sha256((WORK/'CRITIC_ORIGINAL.md').read_bytes() if p.name=='CRITIC.md' and (WORK/'CRITIC_ORIGINAL.md').exists() else p.read_bytes()).hexdigest() for p in REPORTS+[ROOT/'Context-prompt.md',ROOT/'prompt-video-architecture.md',WORK/'PLAN.md',WORK/'RUN_STATE.md',ROOT/'CRITIC.md']},indent=2),encoding='utf-8')
if __name__=='__main__':
    build_sources();build_raw();dump_state()
    print(json.dumps({'sources':len(groups),'source_aliases':len(smap),'facts':len(set(r['id'] for r in allfacts)),'native_fact_aliases':len(fmap),'supplements':len(supplements),'questions':len(questions),'experiments':len(exps),'files':[(p.name,p.stat().st_size) for p in [ROOT/'SOURCES.md',ROOT/'RAW_FACTS.md']]},ensure_ascii=False))
