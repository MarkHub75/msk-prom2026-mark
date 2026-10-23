from pathlib import Path
from collections import Counter
import re,json,runpy

root=Path(__file__).resolve().parent.parent
names=['SOURCES.md','RAW_FACTS.md','OPEN_QUESTIONS.md','CRITIC.md']
texts={n:(root/n).read_text(encoding='utf-8') for n in names}
anchors={n:re.findall(r'<a id="([^"]+)"',s) for n,s in texts.items()}
errors=[]; warnings=[]
for n,aa in anchors.items():
    for a,count in Counter(aa).items():
        if count!=1: errors.append(f'{n}: duplicate anchor {a}')
for n,s in texts.items():
    if n!='CRITIC.md':
        if re.search(r'turn\d|[A-Z]:[/\\]',s): errors.append(f'{n}: private/tool path')
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',s):
        if re.match(r'https?://|mailto:',target): continue
        p,sep,a=target.partition('#')
        path=(root/p) if p else root/n
        if not path.exists(): errors.append(f'{n}: missing {target}');continue
        if a and (not p or p in names):
            key=p or n
            if a not in anchors.get(key,[]): errors.append(f'{n}: missing anchor {target}')
    # Non-provenance wave references indicate an unnormalised shorthand.
    if n!='CRITIC.md':
        for line in s.splitlines():
            if '**Происхождение:**' in line or 'Search-only' in line: continue
            if re.search(r'W[12][A-F]-[SF]\d{2}\b',line): warnings.append(f'{n}: '+line[:180])
expected={'SOURCES.md':75,'RAW_FACTS.md':110,'OPEN_QUESTIONS.md':56,'CRITIC.md':15}
for n,count in expected.items():
    if len(anchors[n])!=count: errors.append(f'{n}: anchors {len(anchors[n])}, expected {count}')
print(json.dumps({'anchors':{n:len(a) for n,a in anchors.items()},'errors':errors,'warnings':warnings},ensure_ascii=False,indent=2))
if errors: raise SystemExit(1)
