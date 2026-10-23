"""Assembly-time integrity checks; no external fetch, no product/runtime tests."""
from pathlib import Path
import re,json,hashlib,math
ROOT=Path(__file__).resolve().parent.parent
FILES=[ROOT/'SOURCES.md',ROOT/'RAW_FACTS.md',ROOT/'OPEN_QUESTIONS.md',ROOT/'CRITIC.md',ROOT/'_WORK/ID_MAP.md',ROOT/'_WORK/COLLECTOR_HANDOFF.md']
anchors={};issues=[]
for p in FILES:
    body=p.read_text(encoding='utf-8')
    aa=re.findall(r'<a id="([^"]+)"',body)
    if len(aa)!=len(set(aa)):issues.append((p.name,'duplicate anchors'))
    anchors[p.resolve()]=set(aa)
    if re.search(r'\]\([^)]*turn\d+(?:search|view|fetch)',body):issues.append((p.name,'tool citation'))
    for ref in re.findall(r'\]\(([^\n]+?)\)',body):
        if ref.startswith(('http://','https://','mailto:')):continue
        ref=ref.strip('<>')
        target,_,anchor=ref.partition('#')
        if not target:continue
        path=(p.parent/target).resolve()
        if not path.exists():issues.append((p.name,'missing local target',ref))
        elif anchor and path in anchors and anchor not in anchors[path]:issues.append((p.name,'missing anchor',ref))
# A second anchor pass now all files are known.
for p in FILES:
    for ref in re.findall(r'\]\(([^\n]+?)\)',p.read_text(encoding='utf-8')):
        if ref.startswith(('http://','https://','mailto:')):continue
        target,_,anchor=ref.strip('<>').partition('#')
        path=(p.parent/target).resolve()
        if anchor and path in anchors and anchor not in anchors[path]:issues.append((p.name,'missing anchor',ref))
data=json.loads((ROOT/'_WORK/COLLECTOR_STATE.json').read_text(encoding='utf-8'))
defs=set(x.upper() for p,aa in anchors.items() for x in aa if re.fullmatch('[sfqe]\\d{3}',x))
mapped=set(data['mapping'].values())
if mapped-defs:issues.append(('ID_MAP','undefined target',sorted(mapped-defs)))
for name in ['SOURCES.md','RAW_FACTS.md','OPEN_QUESTIONS.md']:
    body=(ROOT/name).read_text(encoding='utf-8')
    # Bare two-digit F/S remain only if a native citation was not resolved.
    unresolved=sorted(set(re.findall(r'(?<![\w-])[SFE]\d{2}(?!\w)',body)))
    if unresolved:issues.append((name,'unresolved two-digit IDs',unresolved))
for rec in data['experiments']+data['questions']:
    if rec['old'] not in data['mapping']:issues.append(('ID_MAP','unmapped native item',rec['old']))
original=(ROOT/'_WORK/CRITIC_ORIGINAL.md').read_bytes()
if not (ROOT/'CRITIC.md').read_bytes().startswith(original):issues.append(('CRITIC','original prefix changed'))
arith={
 'jpeg50_Mbps':8*50*5*100000/1e6,'jpeg500_Mbps':8*500*5*100000/1e6,
 'tensor640u8_50_Gbps':8*50*5*640*640*3/1e9,'tensor640fp32_500_Gbps':8*500*5*640*640*3*4/1e9,
 'raw_return_bytes':84*8400*4,'compact_bytes':100*24+4,
 'return_raw50_Gbps':8*50*5*(84*8400*4)/1e9,'return_compact500_Mbps':8*500*5*2404/1e6,
 'main50_TBday':50*4e6*86400/8/1e12,'main500_TB30day':500*4e6*86400*30/8/1e12,
 'main500_TB7day':500*4e6*86400*7/8/1e12,'ring40_500_GB':500*4e6*40/8/1e9,
 'decode1080_500_GPixsec':500*1920*1080*25/1e9,'decode720_50_GPixsec':50*1280*720*25/1e9,
 'latestRGB_500_GB':500*1920*1080*3/1e9,'latestNV12_50_MB':50*1920*1080*1.5/1e6,
 'viewer_Mbps':8*3*4*2*100000/1e6,'serial_viewcycle_ms':1000/(4*2),
 'poll_calls_sec':math.ceil(50/1)/.5,'per_camera_L300_ceiling':1/.3,
 'hyp_nodes300u70_50':math.ceil(50*5/(300*.7)),'hyp_nodes300u70_500':math.ceil(500*5/(300*.7))}
expected={'jpeg50_Mbps':200,'jpeg500_Mbps':2000,'tensor640u8_50_Gbps':2.4576,'tensor640fp32_500_Gbps':98.304,'raw_return_bytes':2822400,'compact_bytes':2404,'return_raw50_Gbps':5.6448,'return_compact500_Mbps':48.08,'main50_TBday':2.16,'main500_TB30day':648,'main500_TB7day':151.2,'ring40_500_GB':10,'decode1080_500_GPixsec':25.92,'decode720_50_GPixsec':1.152,'latestRGB_500_GB':3.1104,'latestNV12_50_MB':155.52,'viewer_Mbps':19.2,'serial_viewcycle_ms':125,'poll_calls_sec':100,'per_camera_L300_ceiling':1/.3,'hyp_nodes300u70_50':2,'hyp_nodes300u70_500':12}
assert all(math.isclose(arith[k],v,rel_tol=1e-12) for k,v in expected.items())
res={'scope':'collector assembly integrity; not product/runtime verification','checked_at_date':'2026-10-23 Europe/Moscow','anchors':{p.name:len(aa) for p,aa in anchors.items()},'native_aliases':len(data['mapping']),'original_critic_sha256':hashlib.sha256(original).hexdigest(),'arithmetic_scenarios':arith,'issues':issues,'files':{str(p.relative_to(ROOT)):p.stat().st_size for p in FILES}}
(ROOT/'_WORK/COLLECTOR_INTEGRITY.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(res,ensure_ascii=False))
