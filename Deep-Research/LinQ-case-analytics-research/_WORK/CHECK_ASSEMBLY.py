from pathlib import Path
import re,json,collections
R=Path(__file__).resolve().parent.parent
files=[R/x for x in ['SOURCES.md','RAW_FACTS.md','OPEN_QUESTIONS.md','CRITIC.md','_WORK/ID_MAP.md','_WORK/COLLECTOR_HANDOFF.md']]
texts={p:p.read_text(encoding='utf-8') for p in files}
anchors={p:set(re.findall(r'(?m)^### ([SFQE]\d{3})\s*$',s)) for p,s in texts.items()}
issues=[];counts={}
for p,s in texts.items():
    ids=re.findall(r'(?m)^### ([SFQE]\d{3})\s*$',s);counts[p.name]=len(ids)
    for k,v in collections.Counter(ids).items():
        if v>1:issues.append(('duplicate',p.name,k,v))
    for label,target in re.findall(r'\[([^\]\n]+)\]\(([^)\n]+)\)',s):
        target=target.strip('<>')
        if re.match(r'https?://|mailto:|plugin:|app:',target):continue
        path,_,anchor=target.partition('#')
        dest=(p.parent/path).resolve() if path else p
        if not dest.exists():issues.append(('missing file',p.name,label,target))
        elif re.match(r'^[sfqe]\d{3}$',anchor) and anchor.upper() not in anchors.get(dest,set()):issues.append(('missing anchor',p.name,label,target))
    if re.search(r'turn\d+(?:search|view|fetch)',s):issues.append(('internal web token',p.name))
mapping=json.loads((R/'_WORK/COLLECTOR_INDEX.json').read_text(encoding='utf-8'))['mapping']
norm=json.loads((R/'_WORK/NORMALIZED_BASE.json').read_text(encoding='utf-8'))
for old,r in norm['records'].items():
    if r['type'] in ['Q','F','I','E']:
        declarations=re.findall(r'(?m)^(?:[-*]\s*)?\*{0,2}(?:W[12]-\d{2}-)?[FQIE]\d{2,3}\b',r['text'])
        if len(declarations)>1:issues.append(('non-atomic record',old,len(declarations)))
case_facts=['W1-01-F01','W1-01-F02','W1-01-F03']
for old in case_facts:
    new=mapping[old];s=texts[R/'RAW_FACTS.md'];section=s.split('### '+new+'\n',1)[1].split('\n### ',1)[0]
    if 'Тип: **DOC**' not in section:issues.append(('case fact type',old,new))
for old,new in mapping.items():
    target=R/{'S':'SOURCES.md','F':'RAW_FACTS.md','Q':'OPEN_QUESTIONS.md','E':'RAW_FACTS.md'}[new[0]]
    if new not in anchors[target]:issues.append(('mapping anchor',old,new))
# Exact arithmetic values are illustrative, never the achieved performance of LinQ.
assert 6==3+1+1+1
assert 7==6+1
assert 3/4==.75 and 1/4==.25 and 2/4==.5
assert (20+90)/2==55
assert 8-11==-3
assert 0-0-500==-500 and 0-3000-500==-3500
assert 0*1000*2-1*1000*5-500==-5500
for literal in ['20,8','1,07','1,018','0,052','22,75','19,02','17,51','3,67','5974']:
    if literal not in texts[R/'RAW_FACTS.md']:issues.append(('missing statistical literal',literal))
out={'counts':counts,'bytes':{p.name:p.stat().st_size for p in files},'issues':issues,'arithmetic':'passed','note':'Локальные ссылки и арифметика сборки; нового внешнего поиска или испытания нет.'}
(R/'_WORK/COLLECTOR_CHECK.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
