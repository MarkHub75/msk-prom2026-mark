from pathlib import Path
from collections import Counter
import re, unicodedata, hashlib, json
from datetime import datetime, timezone, timedelta

root=Path.cwd()
report=root/'report_human_datasets.md'
draft=root/'_WORK/HUMAN_DRAFT.md'
text=report.read_text(encoding='utf-8')
original=draft.read_text(encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def slug(h):
    h=re.sub(r'<[^>]+>','',h).replace('`','').lower()
    h=''.join(c for c in h if c in '-_ ' or unicodedata.category(c)[0] in 'LN')
    return h.replace(' ','-')

links=[]
errors=[]
for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',text):
    if re.match(r'https?://',target):continue
    file,_,anchor=target.partition('#')
    p=root/file if file else report
    links.append(target)
    if not p.exists():errors.append({'missing_file':target});continue
    if anchor:
        doc=p.read_text(encoding='utf-8')
        anchors=set(re.findall(r'<a\s+id="([^"]+)"',doc))
        anchors.update(slug(h) for h in re.findall(r'^#{1,6}\s+(.*?)\s*$',doc,re.M))
        if anchor not in anchors:errors.append({'missing_anchor':target})

checks={}
for name,pattern in {
 'inline_code_literals':r'(?<!`)`([^`\n]+)`(?!`)',
 'external_urls':r'https?://[^\s<>`)]+',
 'fenced_code_blocks':r'```[^\n]*\n.*?```',
}.items():
    a=Counter(re.findall(pattern,original,re.S));b=Counter(re.findall(pattern,text,re.S))
    checks[name]={'missing':dict(a-b),'added':dict(b-a),'unchanged':a==b}

ids={}
for kind in ['F','Q','E','S','K']:
    a=set(re.findall(r'\b'+kind+r'\d{3}\b',original));b=set(re.findall(r'\b'+kind+r'\d{3}\b',text))
    ids[kind]={'missing':sorted(a-b),'added':sorted(b-a)}

tables=[]
table=None
fenced=False
for no,line in enumerate(text.splitlines(),1):
    if line.startswith('```'):fenced=not fenced
    if fenced:continue
    if line.startswith('|'):
        # A literal vertical bar would need escaping outside inline code. None
        # of the report's table cells contain such a literal.
        cells=len(line.split('|'))-2
        if table is None:table={'line':no,'columns':cells,'rows':0}
        if cells!=table['columns']:errors.append({'table_width':no})
        table['rows']+=1
    elif table:
        tables.append(table);table=None
if table:tables.append(table)
if fenced:errors.append({'unclosed_fence':True})

frozen=json.loads((root/'_WORK/COLLECTOR_FREEZE.json').read_text(encoding='utf-8'))
evidence={name:sha(root/name)==meta['sha256'] for name,meta in frozen['files'].items()}
assert all(evidence.values()),evidence
assert not errors,errors
assert all(x['unchanged'] for x in checks.values()),checks
assert all(not x['missing'] and not x['added'] for x in ids.values()),ids
state={
 'checked_at':datetime.now(timezone(timedelta(hours=3))).isoformat(),
 'role':'editor; no new network, research, agents or separate audit',
 'freeze':True,
 'report':'report_human_datasets.md',
 'bytes':report.stat().st_size,
 'lines':len(text.splitlines()),
 'whitespace_words':len(text.split()),
 'sha256':sha(report),
 'draft_sha256':sha(draft),
 'local_links_checked':len(links),
 'link_errors':errors,
 'literal_comparison':checks,
 'identifier_comparison':ids,
 'tables':tables,
 'frozen_evidence_unchanged':evidence,
 'markdown_check':'Local targets and heading/explicit anchors, table column consistency, balanced fences and source code blocks checked. No visual Markdown renderer available in installed Python/CLI/Node tools; no pixel-level rendering claimed.',
 'numeric_edit_note':'Numerical values retained. Whitespace-separated lists were normalized; repeated references 13/228 added to disambiguate SH17. 2D translated, repeated SHA256 mention merged, generic 416-square shorthand replaced by the original exact dimensions.',
}
(root/'_WORK/EDITOR_FREEZE.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:state[k] for k in ['bytes','lines','whitespace_words','sha256','local_links_checked']},ensure_ascii=True))
