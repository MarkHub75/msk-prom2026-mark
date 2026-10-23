from pathlib import Path
import json,re

R=Path(__file__).resolve().parent.parent
reg=json.loads((R/'_WORK/COLLECTOR_REGISTRY.json').read_text(encoding='utf-8'))
aliases=reg['fact_aliases']
text=(R/'_WORK/RAW_CANONICAL.md').read_text(encoding='utf-8')
missing=[]

def ref(m):
    alias=m.group(1)
    if alias not in aliases:
        missing.append(alias)
        return alias+' (unresolved section locator)'
    return '['+alias+'](#'+aliases[alias]+')'

# Resolve explicit reference placeholders only. Never tokenize prose or change
# literal model names, numbers, hashes, class maps or source strings.
text=re.sub(r'\{\{([^}]+)\}\}',ref,text)
detail=(R/'_WORK/RAW_DETAIL.md').read_text(encoding='utf-8')
(R/'RAW_FACTS.md').write_text(text+'\n'+detail,encoding='utf-8')
print(json.dumps({'synthesis_chars':len(text),'raw_bytes':(R/'RAW_FACTS.md').stat().st_size,'missing_requested_aliases':missing},ensure_ascii=False,indent=2))
