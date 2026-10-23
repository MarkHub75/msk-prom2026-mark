from pathlib import Path
import re,json
R=Path(__file__).resolve().parent.parent;W=R/'_WORK'
new={'F327':['S170'],'F328':['S143','S152'],'F329':['S003','S030','S033','S063','S065','S090','S169'],'F330':['S002','S030','S033','S044','S143','S075','S136'],'F331':['S033','S026','S075','S077','S165'],'F332':['S030','S026','S027','S103'],'F333':['S152','S160','S172','S173']}
p=R/'SOURCES.md';t=p.read_text(encoding='utf-8')
for fid,sources in new.items():
    for sid in sources:
        a=t.index(f'<a id="{sid.lower()}"></a>');m=re.search(r'<a id="s\d+"></a>',t[a+1:]);b=a+1+m.start() if m else len(t)
        chunk=t[a:b]
        if f'RAW_FACTS.md#{fid.lower()}' not in chunk:
            chunk+=f'\n- Дополнительный сводный факт сборщика: [{fid}](RAW_FACTS.md#{fid.lower()}).\n\n'
            t=t[:a]+chunk+t[b:]
p.write_text(t,encoding='utf-8')

protect=re.compile(r'(\[[^\]]*\]\([^)]*\)|`[^`]*`|https?://[^\s]+)')
for p in [R/'OPEN_QUESTIONS.md',W/'AUTHOR_HANDOFF.md']:
    t=p.read_text(encoding='utf-8');parts=protect.split(t)
    for i in range(0,len(parts),2):
        c=parts[i]
        # Keep explicit anchor tags and heading IDs untouched; link prose references.
        lines=[]
        for line in c.splitlines(keepends=True):
            if re.match(r'^#{1,4} ',line) or '<a id=' in line:lines.append(line);continue
            if p.name=='OPEN_QUESTIONS.md':
                line=re.sub(r'\b(E\d{3}|R\d{3})\b',lambda m:f'[{m[0]}](_WORK/AUTHOR_HANDOFF.md#{m[0].lower()})',line)
                line=re.sub(r'\b(K\d{3})\b',lambda m:f'[{m[0]}](CRITIC.md#{m[0].lower()}-w2)',line)
            else:
                line=re.sub(r'\b(Q\d{3})\b',lambda m:f'[{m[0]}](../OPEN_QUESTIONS.md#{m[0].lower()})',line)
            line=line.replace('икритерий','и критерий')
            lines.append(line)
        parts[i]=''.join(lines)
    p.write_text(''.join(parts),encoding='utf-8')

names=['SOURCES.md','RAW_FACTS.md','OPEN_QUESTIONS.md','CRITIC.md','_WORK/AUTHOR_HANDOFF.md','_WORK/ID_MAP.md']
anchors={n:set(re.findall(r'<a id="([^"]+)"',(R/n).read_text(encoding='utf-8'))) for n in names};bad=[]
for n in names:
    for path,a in re.findall(r'\]\(([^)#]+)#([^ )]+)\)',(R/n).read_text(encoding='utf-8')):
        try:rel=((R/n).parent/path).resolve().relative_to(R).as_posix()
        except ValueError:continue
        if rel in anchors and a not in anchors[rel]:bad.append([n,path,a])
result={'anchors':{n:len(v) for n,v in anchors.items()},'bad_local_anchor_links':bad,'artifact_bytes':{n:(R/n).stat().st_size for n in names}}
(W/'ASSEMBLY_LINK_CHECK.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(W/'ASSEMBLY_BUILD_NOTE.md').write_text('''# Assembly artifact state

Author/editor/compressor consume the saved Markdown files; no scripts need to be rerun. IDs are frozen at174S/333F/35Q/20E/8R/20K. ASSEMBLY_DATA.json is the intermediate306local-fact/20matrix mapping, with final cross-wave F327–F333 and local S172–S174 additions recorded in ID_MAP.md. The original W1/W2 RESULT and source/probe files are unchanged.

RESTORE_AND_SPACE.py reconstructs the normalized evidence from original wave inputs and appends curated cards/dispositions; COMPLETE_ASSEMBLY_LINKS.py adds final backlink/reference coverage. Earlier ASSEMBLE/FINALIZE/POLISH scripts are staged components, not standalone final builders. FINISH_READABILITY.py is an abandoned spacing experiment and must not be run. Its Russian token segmentation was fully reverted; final output uses original wave prose plus explicit assembler spacing corrections.

ASSEMBLY_LINK_CHECK.json records internal stable-anchor consistency only. It is part of assembly bookkeeping, not a separate technical audit or research wave. No final report was created by the assembler.
''',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
