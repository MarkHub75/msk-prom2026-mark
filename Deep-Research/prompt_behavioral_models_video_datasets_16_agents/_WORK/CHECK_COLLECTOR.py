from pathlib import Path
from collections import Counter
from urllib.parse import unquote
import re,json,datetime,hashlib
R=Path(__file__).resolve().parent.parent
files=['SOURCES.md','RAW_FACTS.md','OPEN_QUESTIONS.md','CRITIC.md']
texts={n:(R/n).read_text(encoding='utf-8') for n in files}
cache={str((R/n).resolve()):t for n,t in texts.items()}
anchors={n:set(re.findall(r'<a id="([^"]+)"></a>',t)) for n,t in texts.items()}
duplicates={n:{k:v for k,v in Counter(re.findall(r'<a id="([^"]+)"></a>',t)).items() if v>1} for n,t in texts.items()}
bad=[];external=0;links=0
for name,t in texts.items():
    for m in re.finditer(r'\[[^\]]*\]\((<[^>]+>|[^\s)]+)\)',t):
        target=m.group(1).strip('<>');links+=1
        if target.startswith(('http:','https:','mailto:')):external+=1;continue
        path,_,frag=target.partition('#')
        p=(R/unquote(path)).resolve() if path else R/name
        if not p.exists():bad.append({'file':name,'target':target,'reason':'missing file'});continue
        if frag and re.match(r'^[FSKQE]\d{3}$',frag):
            key=str(p)
            if key not in cache:cache[key]=p.read_text(encoding='utf-8-sig')
            tt=cache[key]
            if f'<a id="{frag}"></a>' not in tt:bad.append({'file':name,'target':target,'reason':'missing canonical anchor'})
    if re.search(r'<a id="\[',t):bad.append({'file':name,'reason':'Markdown injected into HTML anchor'})
reg=json.loads((R/'_WORK/COLLECTOR_REGISTRY.json').read_text(encoding='utf-8'))
coverage={n:sum(r['branch']==n for r in reg['sections']) for n in [f'W1_M{i:02}' for i in range(1,9)]+[f'W1_D{i:02}' for i in range(9,17)]+[f'W2_{i:02}' for i in range(1,8)]}
core=texts['RAW_FACTS.md'].split('## Detailed normalized evidence dossiers')[0]
literal_checks={
    'RTMPose literal intact':'RTMPose-m body7 e48f03d0' in core,
    'ByteTrack literal intact':'ByteTrack d1bf0191' in core,
    'body7 archive hash intact':'f7fbb6c5c11a1bb70f3d445e4ddec5d144ea89ad5649c081ef976f9b24a0b741' in core,
    'fall clock correction':'early raw-clock “missing tail” diagnostic is superseded' in core,
    'four fixture bound':'four files only' in core,
    'mist gap explicit':'Mist video is UNCONFIRMED' in core,
    'distinct INT8 architecture':'Different architecture from float' in core,
    'phone concurrency limit':'No convincing simultaneous locomotion/use was established' in core,
    'routine truck not near miss':'not certified danger' in core,
    'eight stage anchors':all(f'E{i:03}' in anchors['OPEN_QUESTIONS.md'] for i in range(1,9)),
    'eighteen questions':all(f'Q{i:03}' in anchors['OPEN_QUESTIONS.md'] for i in range(1,19)),
    'seven outcome anchors':all(f'K{i:03}' in anchors['CRITIC.md'] for i in range(1,8)),
    'original critic bytes preserved':(R/'CRITIC.md').read_bytes().startswith((R/'_WORK/CRITIC_ORIGINAL.md').read_bytes()),
    'all 23 reports retained':all(coverage.values()),
    'no intermediate spacing corruption':not any(x in core for x in ['Behavior al','collect or','RTMPose-m-body 7','pl a nn ed','UR Ls','YOL Ov 8']),
}
result={'checked_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).isoformat(),'role':'collector own assembly checks, not separate final audit','registry_counts':{'S':len([x for x in anchors['SOURCES.md'] if re.fullmatch(r'S\d{3}',x)]),'F':len([x for x in anchors['RAW_FACTS.md'] if re.fullmatch(r'F\d{3}',x)]),'Q':18,'E':8,'K':7},'duplicates':duplicates,'links_checked':links,'external_urls_not_retrieved':external,'bad_links':bad,'coverage':coverage,'checks':literal_checks,'owned_files':files,'later_required_report_names':['report_human_behavioral_models_video_data.md','report_machine_behavioral_models_video_data.md']}
(R/'_WORK/COLLECTOR_CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
