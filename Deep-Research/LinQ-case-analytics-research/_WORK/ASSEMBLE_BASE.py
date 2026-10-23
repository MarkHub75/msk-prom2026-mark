from pathlib import Path
import re, json, hashlib, collections

ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'_WORK'
files=sorted(WORK.glob('W1_*.md'))+sorted(WORK.glob('W2_*.md'))
texts={p.stem[:5].replace('_','-'):p.read_text(encoding='utf-8-sig') for p in files}
paths={p.stem[:5].replace('_','-'):p for p in files}
# Read every agreed input in its entirety, retaining hashes for the assembly record.
inputs=[ROOT/'Context-prompt.md',ROOT/'prompt-linq-case-analytics.md',ROOT/'CRITIC.md']+files+[WORK/x for x in ['PROMPT_COLLECTOR.md','ROLE_BRIEFS.md','CASE_NOTES.md','CASE_METADATA.json','CRITIC_HANDOFF.md','AGENT_PROMPTS.md','RUN_STATE.md','ORCHESTRATOR_DECISIONS.md']]
input_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
input_contents={str(p.relative_to(ROOT)):p.read_text(encoding='utf-8-sig') for p in inputs}
meta=json.loads((WORK/'CASE_METADATA.json').read_text(encoding='utf-8-sig'))
FULL=re.compile(r'W[12]-\d{2}-[SFIQE]\d{2,3}')
SHORT=re.compile(r'(?<![\w-])([SFIQE])(\d{2,3})(?!\d)')
URL=re.compile(r'https?://[^\s<>\]`|]+')

def paragraph_at(txt,pos):
    a=txt.rfind('\n\n',0,pos)+2
    if a==1:a=0
    b=txt.find('\n\n',pos)
    if b<0:b=len(txt)
    para=txt[a:b].strip()
    line=txt[txt.rfind('\n',0,pos)+1:txt.find('\n',pos) if txt.find('\n',pos)>=0 else len(txt)]
    if line.lstrip().startswith('|') or re.match(r'^\s*[-*]\s+',line):return line.strip()
    return para

def ids_in(txt,branch):
    out=set(FULL.findall(txt))
    out.update(branch+'-'+m.group(0) for m in SHORT.finditer(FULL.sub('',txt)))
    return out

sources={}; records={}; occurrences=collections.defaultdict(list)
for branch,txt in texts.items():
    for m in FULL.finditer(txt):occurrences[m.group()].append((branch,m.start()))
    for typ in 'SFIQE':
        # Local identifiers only become entities if used in an explicit declaration/row.
        pat=re.compile(r'(?m)^(?:\|\s*|#{1,5}\s*|[-*]\s*)?(?:\*\*)?('+re.escape(branch)+r'-'+typ+r'\d{2,3})(?=[\s,.:;—(→|*])')
        for m in pat.finditer(txt):
            ident=m.group(1)
            if ident in records:continue
            if typ=='S' and txt[m.start():].lstrip().startswith('#'):
                end=re.search(r'(?m)^#{1,3} ',txt[m.end():])
                block=txt[m.start():m.end()+end.start() if end else len(txt)].strip()
            else:block=paragraph_at(txt,m.start(1))
            records[ident]={'branch':branch,'type':typ,'text':block,'path':str(paths[branch].relative_to(ROOT))}
    # W2-04 deliberately abbreviates F02..05 within its methodological section.
    if branch=='W2-04':
        for m in re.finditer(r'\*\*F(0[2-5])\b',txt):
            ident=branch+'-F'+m.group(1)
            records.setdefault(ident,{'branch':branch,'type':'F','text':paragraph_at(txt,m.start()),'path':str(paths[branch].relative_to(ROOT))})
    for m in re.finditer(r'(?m)^(?:\|\s*|[-*]\s*)(?:\*\*)?([QIE]\d{2,3})(?=[\s,.:;—(→|*])',txt):
        ident=branch+'-'+m.group(1)
        records.setdefault(ident,{'branch':branch,'type':m.group(1)[0],'text':paragraph_at(txt,m.start()),'path':str(paths[branch].relative_to(ROOT))})

for ident,rec in records.items():
    if rec['type']!='S':continue
    s=rec['text']
    urls=[]
    for x in URL.findall(s):
        x=x.rstrip(').,;:')
        if x not in urls:urls.append(x)
    rec['urls']=urls
    # All representations of the supplied case are one source, not new sources.
    if ident in ['W1-01-S01','W1-02-S01','W1-03-S00','W1-07-S13','W2-03-S01','W2-05-S13']:
        key='CASE_PDF'
    elif urls:
        key=urls[0].replace('http://','https://').replace('https://www.','https://').rstrip('/')
        # Transport URL does not create an additional document.
        key=key.replace('r.jina.ai/https://','')
    else:key='LOCAL:'+ident
    rec['key']=key
    sources.setdefault(key,[]).append(ident)

# Capture inline declarations that do not start a paragraph (e.g. access failures).
for ident,occs in occurrences.items():
    if ident in records:continue
    own=ident[:5]
    candidates=[paragraph_at(texts[b],pos) for b,pos in occs if b==own]
    if not candidates:continue
    block=max(candidates,key=len)
    typ=ident.split('-')[-1][0]
    records[ident]={'branch':own,'type':typ,'text':block,'path':str(paths[own].relative_to(ROOT))}
# These branch E labels denote product inferences, not experiments.
for ident,r in records.items():
    if r['type']=='E' and r['branch'] in ['W2-01','W2-05','W2-06']:r['type']='I'

# Explicit local derivatives are linked to the original case.
for ident in ['W2-05-S13']:
    if ident in records:
        old=records[ident].get('key')
        if old and ident in sources.get(old,[]):sources[old].remove(ident)
        sources.setdefault('CASE_PDF',[]).append(ident);records[ident]['key']='CASE_PDF'
sources={k:v for k,v in sources.items() if v}
sources.setdefault('CASE_PDF',[])
sources={'CASE_PDF':sources.pop('CASE_PDF'),**sources}
mapping={};canon_sources={}
for n,(key,aliases) in enumerate(sources.items(),1):
    cid=f'S{n:03}'
    canon_sources[cid]={'key':key,'aliases':aliases}
    for x in aliases:mapping[x]=cid
for typ,target in [('F','F'),('I','F'),('Q','Q'),('E','E')]:
    n=sum(1 for x in mapping.values() if x.startswith(target))
    for ident in sorted(k for k,r in records.items() if r['type']==typ):
        n+=1;mapping[ident]=f'{target}{n:03}'

def norm(txt,branch):
    placeholders={}
    def protect(m):
        key=f'ZZENTITY{len(placeholders)}ZZ';placeholders[key]=mapping.get(m.group(),m.group());return key
    txt=FULL.sub(protect,txt)
    txt=SHORT.sub(lambda m:mapping.get(branch+'-'+m.group(),m.group()),txt)
    for key,val in placeholders.items():txt=txt.replace(key,val)
    # All original links were relative to _WORK; the final evidence files live one level above it.
    def local_link(m):
        target=m.group(1);path=target.split('#')[0]
        if path.startswith('_WORK/') and (ROOT/path).exists():return ']('+target+')'
        if (WORK/path).exists():return '](_WORK/'+target+')'
        if (ROOT/path).exists():return ']('+target+')'
        # Preserve the locator as text, without fabricating a working local link.
        return ']('+target+')'
    txt=re.sub(r'\]\((?!https?://|#|/)([^)]+)\)',local_link,txt)
    txt=txt.replace('D:/msk-prom2026-mark/Deep-Research/LinQ-case-analytics-research/','')
    txt=txt.replace('D:\\msk-prom2026-mark\\Deep-Research\\LinQ-case-analytics-research\\','')
    return txt

def entry_refs(ident):
    rec=records[ident];refs=ids_in(rec['text'],rec['branch'])
    if rec['type']=='F':
        # RU catalogue has the source immediately preceding the fact under its S heading.
        if rec['branch']=='W1-04':refs.add('W1-04-S'+ident[-2:])
    return sorted({mapping[x] for x in refs if x in mapping and mapping[x].startswith('S')})

def classify(ident):
    r=records[ident];s=r['text'];b=r['branch'];num=int(ident.split('-')[-1][1:])
    if r['type']=='I':return 'INF','Аналитическая конструкция; не реализованная функция и не измеренный эффект'
    if re.search(r'Факт чтения|Нормативный (?:текст|факт)|\bDOC\b|Документация\.',s,re.I):return 'DOC','Проверено содержание документа; целевой сценарий, установленная функция и измеренный эффект различаются'
    if b=='W2-04' and num in [3,6,7]:return 'INF','Методическая конструкция/вывод; численные примеры условны'
    if re.search(r'собственный вывод|наш вывод|гипотез|проектн|предлагаем|вывод исследовател|исследовательский вывод|вывод из',s,re.I):
        if not re.search(r'\bDOC\b|Нормативный|W1-03-F02',s):return 'INF/HYP','Вывод или рекомендация; применение и эффект не испытаны'
    if b=='W2-01' or (b=='W2-06') or (b=='W2-03' and num in range(4,11)):return 'VENDOR/CUSTOMER SELF-REPORT','Прочитан первичный текст заинтересованной стороны; исполнение процесса нами не наблюдалось'
    if re.search(r'измерение|эксперимент|MEAS|опрос|42 штатных|survey|исследовани[ея]',s,re.I) and b in ['W1-03','W1-08']:return 'MEAS','Опубликованное внешнее исследование; не наш эксперимент; перенос ограничен выборкой/задачей'
    if re.search(r'VC|VENDOR|SELF.REPORT|поставщик|клиентск|Автор сообщает|внедрен|внедрён|заявлен',s,re.I):return 'VENDOR/CUSTOMER SELF-REPORT','Заявление/описание в прочитанном материале; независимого испытания продукта нет'
    return 'DOC','Проверено содержание документа/описания; установленный продукт и практический эффект этим не проверены'

data={'mapping':mapping,'sources':canon_sources,'records':records,'input_hashes':input_hashes}
for r in records.values():r['path']=r['path'].replace('\\','/')
(WORK/'NORMALIZED_BASE.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':
    print('files',len(files),'source records',sum(r['type']=='S' for r in records.values()),'canonical sources',len(canon_sources))
    print('record counts',dict(collections.Counter(r['type'] for r in records.values())))
    unresolved=sorted(x for x in occurrences if x not in mapping)
    print('unresolved explicit references',unresolved)
    print('facts without S:',[x for x,r in records.items() if r['type']=='F' and not entry_refs(x)])
