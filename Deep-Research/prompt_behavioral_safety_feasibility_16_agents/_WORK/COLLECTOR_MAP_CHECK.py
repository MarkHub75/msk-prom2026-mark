from pathlib import Path
import re,json,hashlib
W=Path(__file__).resolve().parent;R=W.parent
s=(R/'SOURCES.md').read_text(encoding='utf-8'); lookup={}
for block in re.split(r'(?=<a id="S\d{3}"></a>)',s):
    sm=re.search(r'<a id="(S\d{3})"',block);um=re.search(r'^URL: (\S+)',block,re.M)
    if sm and um:lookup[um[1]]=sm[1]
mapping=[]
for fn in sorted(list(W.glob('W1-??.md'))+list(W.glob('W2-??.md'))):
    txt=fn.read_text(encoding='utf-8-sig');lines=txt.splitlines();defined=set()
    for i,line in enumerate(lines):
        matches=re.findall(r'W[12]-\d{2}-S\d{2,3}',line)
        for bid in matches:
            if bid in defined:continue
            is_def=(line.startswith('#') or line.startswith('**'+bid) or line.startswith(bid+' —') or line.startswith('|') and bid in line[:35])
            if not is_def:continue
            defined.add(bid)
            if line.startswith('|'):chunk=line
            else:
                end=next((j for j in range(i+1,len(lines)) if re.search(r'W[12]-\d{2}-S\d{2,3}',lines[j]) and (lines[j].startswith('#') or lines[j].startswith('W') or lines[j].startswith('**W'))),len(lines))
                chunk='\n'.join(lines[i:end])
            urls=[x.rstrip(').,;:—') for x in re.findall(r'https?://[^\s<>`\[\]"|]+',chunk)]
            hits=sorted({lookup[u] for u in urls if u in lookup})
            mapping.append((bid,hits,fn.name,i+1))
idmap=(W/'ID_MAP.md').read_text(encoding='utf-8');idmap+='\n## Source aliases: branch S → canonical exact-URL S\n\nОдин branchS объединял несколько первичных файлов; перечисленные canonicalS сохраняют эту one-to-many связь. Если в исходной строке только внутренняя атрибуция/неполный URL, canonicalF остаётся смысловым локатором в предыдущей таблице; source не выдумывается.\n\n| Branch S | Canonical exact-URL S | Original definition locator |\n|---|---|---|\n'
for bid,hits,name,line in mapping:idmap+='|'+bid+'|'+(', '.join(f'[{x}](../SOURCES.md#{x})' for x in hits) if hits else 'См. canonicalF mapping выше; definition без сопоставленного exact URL')+'|'+f'[{name}:{line}]({name})'+'|\n'
idmap+='\n## Local Q/E aliases → canonical thematic records\n\nBranch-local Q1/E1 labels не глобально уникальны и описывали несколько частей. Canonical grouping: W2-01Q1–5→Q001–004/Q019,E001; W2-02Q/E→Q002/Q005/Q017,E002; W2-03Q/E→Q006/Q020,E003/E004/E009; W2-04Q/E→Q009/Q010/Q017,E002/E006; W2-05Q/E→Q007/Q008/Q017,E005; W2-06Q/E→Q012/Q017,E002/E007; W2-07Q1–5→Q017/Q010/Q002; W2-08Q/E→Q018/Q019/Q020,E005/E009. Исходные K001–K011 сохранены в CRITIC.\n'
(W/'ID_MAP.md').write_text(idmap,encoding='utf-8')
files=['RAW_FACTS.md','SOURCES.md','OPEN_QUESTIONS.md','CRITIC.md','_WORK/ID_MAP.md','_WORK/COLLECTOR_HANDOFF.md']
anch={f:re.findall(r'<a id="([SFQEK]\d{3})"></a>',(R/f).read_text(encoding='utf-8')) for f in files}
issues=[]
for f in files:
    body=(R/f).read_text(encoding='utf-8')
    if len(anch[f])!=len(set(anch[f])):issues.append((f,'duplicate ID'))
    for target in re.findall(r'\]\(([^)]+)\)',body):
        if target.startswith(('http://','https://','mailto:')):continue
        p,_,frag=target.partition('#');dst=((R/f).parent/p).resolve() if p else (R/f).resolve()
        if not dst.exists():issues.append((f,'missing local target',target));continue
        if re.fullmatch(r'[SFQEK]\d{3}',frag):
            if frag not in re.findall(r'<a id="([SFQEK]\d{3})"></a>',dst.read_text(encoding='utf-8-sig')):issues.append((f,'missing canonical anchor',target))
    if re.search(r'turn\d+(?:search|view|fetch)\d+',body):issues.append((f,'browsercitation'))
    if re.search(r'(?i)(?:file:///|D:\\|C:\\Users\\)',body):issues.append((f,'absolute path'))
stats={f:{'bytes':(R/f).stat().st_size,'canonical_anchors':len(anch[f])} for f in files}
state={'status':'READY_FOR_AUTHOR','date':'2026-10-23','timezone':'Europe/Moscow UTC+3','canonical_F':69,'canonical_S':401,'canonical_Q':20,'canonical_E':10,'K_outcomes':11,'source_aliases':len(mapping),'actual_linq_inference':'NOT_RUN','new_network_by_collector':False,'stats':stats,'issues':issues,'check_scope':'in-role link/ID normalization only; no separate audit stage'}
(W/'COLLECTOR_LINK_CHECK.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
(W/'COLLECTOR_BUILD_STATE.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(state,ensure_ascii=False))
