from pathlib import Path
from collections import defaultdict
from urllib.parse import urlsplit, unquote
import re, json, hashlib, datetime

ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'_WORK'
NAMES=[f'W1_M{i:02}' for i in range(1,9)]+[f'W1_D{i:02}' for i in range(9,17)]+[f'W2_{i:02}' for i in range(1,8)]
REPORTS={n:(WORK/(n+'.md')).read_text(encoding='utf-8-sig') for n in NAMES}
URL=re.compile(r'https?://[^\s<>`\[\]{}"“”]+')
FID=re.compile(r'(?:W[12][-_]\d{2}|W1[-_][MD]\d{2}|[MD]\d{2})-F\d{1,3}')
SID=re.compile(r'(?:W[12][-_]\d{2}|W1[-_][MD]\d{2}|[MD]\d{2})-S\d{1,3}')

def urls(t):
    result=[]
    for m in URL.finditer(t):
        u=m.group().rstrip('.,;:|')
        # A closing Markdown parenthesis is not part of these observed URLs.
        if u.endswith(')') and '(' not in u: u=u[:-1]
        if u not in result: result.append(u)
    return result

def localize(t):
    for a,b in {'вЂ”':'—','вЂ“':'–','Г—':'×','в†’':'→'}.items():t=t.replace(a,b)
    # Preserve relative links from _WORK reports when moved to the root dossier.
    def repl(m):
        label,target=m.group(1),m.group(2)
        if target.startswith(('http:','https:','#','mailto:')): return m.group(0)
        if target.startswith('../'):
            target=target[3:]
        else: target='_WORK/'+target
        return '['+label+']('+target+')'
    return re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)',repl,t)

sections=[]
source_notes=[]
aliases={}
for name,txt in REPORTS.items():
    lines=txt.splitlines()
    boundaries=[0]
    for i,line in enumerate(lines[1:],1):
        if re.match(r'^#{2,4}\s',line) or ((line.startswith('**') or (line.startswith('<a ') and '**' in line)) and FID.search(line[:150])):
            boundaries.append(i)
    boundaries.append(len(lines))
    for a,b in zip(boundaries,boundaries[1:]):
        body='\n'.join(lines[a:b]).strip()
        if not body: continue
        title=lines[a].lstrip('#* ').strip()
        first=re.sub(r'^<a[^>]*></a>\s*','',lines[a])
        bold=re.match(r'^\*\*(.+?)\*\*',first)
        if bold:title=bold.group(1)
        title=re.sub(r'<[^>]*>','',title)
        if len(title)>180:title=title[:177].rsplit(' ',1)[0]+'…'
        # Source-only registers are carried into SOURCES rather than duplicated.
        src=bool(re.search(r'(Primary[- ]source register|Source registry|Primary sources / exact|Primary sources and access register|Evidence register and locators|Реестр первичных источников|Источники и проверенные артефакты|Primary sources and pinned locators|Primary source register|Source register$|Primary sources and evidence registry)',title,re.I))
        rec={'branch':name,'line':a+1,'title':title,'text':body,'urls':urls(body),'old_f':[]}
        if src:
            source_notes.append(rec)
        else:
            rec['id']=f'F{len(sections)+26:03}'
            # Definitions are headings or the first line, not incidental references.
            rec['old_f']=list(dict.fromkeys(FID.findall(lines[a][:200])))
            for old in rec['old_f']: aliases.setdefault(old,rec['id'])
            sections.append(rec)

# Sources are normalized by literal canonical URL, never by number of copies.
observations=defaultdict(list)
source_alias_urls=defaultdict(list)
for name,txt in REPORTS.items():
    ls=txt.splitlines()
    for i,line in enumerate(ls):
        us=urls(line)
        if us:
            context=line
            for u in us:
                observations[u].append({'branch':name,'line':i+1,'context':context[:2600]})
        # Original source alias definitions, table rows and standalone source paragraphs.
        ss=SID.findall(line[:220])
        if ss and (line.startswith(('|','- **','* **','**','<a ','##'))):
            context=line
            if not urls(context):
                context='\n'.join(ls[i:min(i+3,len(ls))])
            sus=urls(context)
            for old in ss:
                for u in sus:
                    if u not in source_alias_urls[old]: source_alias_urls[old].append(u)

source_ids={u:f'S{i+2:03}' for i,u in enumerate(observations)}
for rec in sections:
    su=set(rec['urls'])
    for old in SID.findall(rec['text']): su.update(source_alias_urls.get(old,[]))
    # Branch-local short [S01] references: resolve only a matching defined branch prefix.
    prefix=rec['branch'].replace('W1_','').replace('_','-')
    shorts=re.findall(r'(?<![\w-])S\d{1,3}(?!\d)',rec['text'])
    for a,b in re.findall(r'S(\d{1,3})[–—-]S?(\d{1,3})',rec['text']):
        if int(b)>=int(a) and int(b)-int(a)<40:
            shorts += ['S'+str(x).zfill(len(a)) for x in range(int(a),int(b)+1)]
    for short in shorts:
        for candidate in [prefix+'-'+short,rec['branch'].replace('_','-')+'-'+short]:
            su.update(source_alias_urls.get(candidate,[]))
    rec['sources']=[source_ids[u] for u in observations if u in su]

def norm(t):
    t=localize(t)
    # Canonical anchors are supplied by the dossier wrapper. Avoid rewriting old
    # HTML id values into Markdown links inside attributes.
    t=re.sub(r'<a\s+id="[^"]+"\s*></a>','',t)
    # Branch aliases remain searchable, with canonical fact links.
    t=FID.sub(lambda m:'['+m.group()+'](RAW_FACTS.md#'+aliases[m.group()]+')' if m.group() in aliases else m.group(),t)
    t=SID.sub(lambda m:'['+m.group()+'](SOURCES.md#'+m.group()+')' if m.group() in source_alias_urls else m.group(),t)
    return t

def author(u):
    p=urlsplit(u); host=p.netloc.lower(); path=p.path.strip('/').split('/')
    if host in ['github.com','raw.githubusercontent.com','api.github.com']:
        if host=='api.github.com' and path and path[0]=='repos': path=path[1:]
        return '/'.join(path[:2])+' publisher/contributors'
    if 'huggingface.co' in host:
        if path and path[0] in ['datasets','api','models']: path=path[1:]
        if path and path[0] in ['datasets','models']: path=path[1:]
        return '/'.join(path[:2])+' publisher; exact individual authors in observations below'
    known={'download.openmmlab.com':'OpenMMLab','storage.googleapis.com':'Google/publisher identified by object namespace','www.tensorflow.org':'TensorFlow/Google','blog.tensorflow.org':'TensorFlow authors identified below','fenix.ur.edu.pl':'Michał Kępski / University of Rzeszów','homepages.inf.ed.ac.uk':'Robert Fisher / CAVIAR team','groups.inf.ed.ac.uk':'Edinburgh Vision Group / BEHAVE','ai2-public-datasets.s3-us-west-2.amazonaws.com':'AllenAI / Charades authors','www.aicitychallenge.org':'AI City Challenge organizers','www.youtube.com':'YouTube official player; underlying media owner separately identified where known'}
    return known.get(host,host+'; individual author/title attribution retained in source observations where established')

def version(u):
    shas=re.findall(r'(?<![a-f0-9])[a-f0-9]{40}(?![a-f0-9])',u)
    if shas:return 'immutable revision '+', '.join(shas)+'; publication date is separate'
    v=re.search(r'(?:arxiv.org/(?:abs|html|pdf)/)([^/?#]+)',u)
    if v:return 'arXiv '+v.group(1)+'; use dated version in observations'
    return 'no immutable revision inferable from URL; release/publication/transport dates, if observed, are retained separately below; otherwise unknown'

now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).isoformat()
bundle={'completed_at':now,'sources':source_ids,'sections':sections,'fact_aliases':aliases,'source_aliases':dict(source_alias_urls),'source_notes':source_notes}
(WORK/'COLLECTOR_REGISTRY.json').write_text(json.dumps(bundle,ensure_ascii=False,indent=2),encoding='utf-8')

# Authoritative case record, then one literal-URL source per acquisition identity.
casefiles=list((WORK/'CASE').glob('*.pdf'))
case='_WORK/CASE/'+casefiles[0].name if casefiles else '_WORK/CASE_NOTES.md'
out=['# Primary sources and exact artifact/access registry','',
     'Collector assembly of the two completed waves. No new network retrieval or model execution. A source ID identifies one literal URL; repeated reads, mirrors and copied releases are **not independent confirmations**. Source observations preserve the acquisition layer: landing page, HEAD/range, full bytes/hash, static parse, decode and sampled/full visual review. An HTTP200 HTML page is not a binary. `local_test` in a branch often means parsing or decoding, never implied inference. All research accesses were on 2026-10-23; local assembly date may cross midnight. Per-request timestamps in linked saved JSON logs take precedence over an approximate branch window.',
     '',f'<a id="S001"></a>\n## S001 — local original LinQ case, 20 pages\n\nPrimary supplied/local document, publisher ООО «ХайТэк» / case organizers as identified in the document. Public URL unknown. Portable byte-identical [PDF](<{case}>) and [direct-reading notes](_WORK/CASE_NOTES.md); SHA256 `7dbece3cf414e2a09ff03c93e9e1ed87172d7724fb7edd5cd3a3ad565063689e`. Root rendered and visually read all20pages on 2026-10-23 after22:12Moscow, recorded22:15:57+03. This is root primary inspection, not collector independent visual reading. Pages4,5,7–10,12–13,15,18–19; publication date not asserted beyond supplied2026case. Supports [F001](RAW_FACTS.md#F001), [F002](RAW_FACTS.md#F002), [F017](RAW_FACTS.md#F017).',
     '', '## Acquisition windows','', '| Acquisition task | Actual reported access/review window and action boundary |','|---|---|']
for name,txt in REPORTS.items():
    time_lines=[x for x in txt.splitlines()[:18] if re.search(r'2026|Access|Дата|Research',x) and not x.startswith(('|','**D09-S')) and 'https://' not in x][:1]
    out += ['| '+name+' | '+localize(' '.join(time_lines)).replace('|','/').replace('#','').strip()[:1100]+' |']
out += ['', '## Literal URL registry','', 'Each record uses the acquisition window above. Fine-grained request timestamps are in the named branch access/fetch logs; an approximate window is not an invented per-request timestamp. URLs for the same repository/release are acquisition locators within one provenance family, not separate independent scientific confirmations. Rich source metadata registers are retained once at the end.','']
for u,s in source_ids.items():
    obs=observations[u]
    supporting=[r['id'] for r in sections if s in r['sources']]
    title=unquote(urlsplit(u).path.rsplit('/',1)[-1] or urlsplit(u).netloc)
    v=version(u)
    if v.startswith('no immutable'): v='Revision/publication: unstated in URL; use source metadata/observation below (otherwise unknown).'
    out += [f'<a id="{s}"></a>',f'### {s} — {title}', '', f'<{u}>', '', f'{author(u)}. {v}.', '', 'Facts: '+(', '.join(f'[{x}](RAW_FACTS.md#{x})' for x in supporting) or 'provenance context only')+'.','']
    # Preserve distinct wave/source observations, but not repeated identical prose.
    seen=set()
    for o in obs:
        key=(o['branch'],o['context'])
        if key in seen:continue
        seen.add(key)
        context=localize(o['context']).replace('\n',' ').strip()
        context=re.sub(r'<a\s+id="[^"]+"\s*></a>','',context)
        # The exact URL already has a dedicated field; avoid repeating it or unrelated URLs.
        context=URL.sub(lambda m:'[this locator]' if m.group().rstrip('.,;:|)')==u else '[related locator]',context)
        context=re.sub(r'^\|\s*|\s*\|$','',context).replace(' | ','; ')
        context=re.sub(r'\s+',' ',context)
        # Long technical paragraphs are retained once in RAW_FACTS; here give a locator,
        # explicit acquisition boundary and concise source-specific extract.
        if len(context)>700:
            sentences=re.split(r'(?<=[.!?])\s+(?=[A-ZА-Я*])',context)
            chosen=[x for x in sentences if re.search(r'HTTP|GET|HEAD|access|download|acquir|licen|revision|commit|Дата|доступ|скача|получ|SHA|artifact',x,re.I)]
            context=(' '.join(chosen) or context)[:700].rstrip()+' [full conditions in canonical fact dossier]'
        out += [f"- [{o['branch']}:{o['line']}](_WORK/{o['branch']}.md): "+context,'']
out += ['## Original source-alias map','', 'Aliases below preserve branch locators. They map to literal URL identities and are not additional independent sources. A definition may group a paper, card and exact artifact; consult the distinct URL records for access.','']
for old,us in sorted(source_alias_urls.items()):
    out += [f'<a id="{old}"></a>',f'**{old}** → '+', '.join(f'[{source_ids[u]}](#{source_ids[u]})' for u in us if u in source_ids)+'.','']
out += ['## Retained primary metadata and acquisition notebooks','', 'The following source-register sections retain exact authors, titles, publication/version dates, commit locators and access limitations that cannot be recovered from a URL alone. These are metadata records of the same sources above, not extra confirmations.','']
for r in source_notes:
    note=re.sub(r'<a\s+id="[^"]+"\s*></a>','',localize(r['text']))
    out += [f"### {r['branch']} — {r['title']}", '',f"Provenance: [{r['branch']}:{r['line']}](_WORK/{r['branch']}.md).",'',note, '']
(ROOT/'SOURCES.md').write_text('\n'.join(out),encoding='utf-8')

detail=['\n## Detailed normalized evidence dossiers','', 'These canonical fact records retain substantive findings from all16W1 and7W2 reports in the public evidence base itself. Source-only registries are in SOURCES. They are grouped by research question; earlier W1 observations remain historical, and the canonical decision records F001–F025 and later W2 outcomes govern supersession. A branch-local test keeps its original meaning (CSV/static/media inspection), not neural execution. Embedded proposed tests are proposals. Internal method/alias labels are provenance names, not additional measured systems.','']
for r in sections:
    refs=', '.join(f'[{s}](SOURCES.md#{s})' for s in r['sources'])
    detail += [f"<a id=\"{r['id']}\"></a>",f"### {r['id']} — {r['branch']}: {r['title']}",'',f"Provenance: [{r['branch']}:{r['line']}](_WORK/{r['branch']}.md); original aliases: {', '.join(r['old_f']) or 'section record'}. Sources: {refs or 'see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted'}.",'',norm(r['text']), '']
(WORK/'RAW_DETAIL.md').write_text('\n'.join(detail),encoding='utf-8')
mapping=['# Branch to canonical ID map','',f'Assembled {now}. No new evidence retrieval.','', '| Original fact | Canonical record |','|---|---|']
mapping += [f'| {a} | [{b}](../RAW_FACTS.md#{b}) |' for a,b in sorted(aliases.items())]
mapping += ['', '## Source aliases','']+[f'- {a}: '+', '.join(source_ids[u] for u in us if u in source_ids) for a,us in sorted(source_alias_urls.items())]
mapping += ['', '## Complete section coverage','']+[f"- {r['branch']}:{r['line']} → [{r['id']}](../RAW_FACTS.md#{r['id']}) — {r['title']}" for r in sections]
(WORK/'ID_MAP.md').write_text('\n'.join(mapping),encoding='utf-8')
print(json.dumps({'sources':len(source_ids)+1,'fact_dossiers':len(sections),'aliases':len(aliases),'source_aliases':len(source_alias_urls),'source_notebooks':len(source_notes),'sources_bytes':(ROOT/'SOURCES.md').stat().st_size,'detail_bytes':(WORK/'RAW_DETAIL.md').stat().st_size},indent=2))
