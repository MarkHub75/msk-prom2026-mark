import json,hashlib,datetime
from pathlib import Path
P=Path('_WORK/W2_03_EVIDENCE');out={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decoder':'PyAV18.1.0','mapping_status':'spatial_scale_verified; exact_single_frame_origin_unresolved','sources':{},'canonical_clock':'decoded_index0/25 seconds; synthetic evaluation clock; original PTS retained; not wall clock or certified capture clock','uncertainty':'candidate index = XML frame + delta (CAVIAR), global frame -35450 + delta (BEHAVE); delta -1,0,+1 remain unresolved by manual bbox overlays; wider +/-5 inspected, not a confidence bound'}
for n,pa in [('runxml','_WORK/M04/runxml.txt'),('walkxml','_WORK/M04/walkxml.txt'),('xgtf','_WORK/D11/35450-47160F.xgtf'),('markup','_WORK/D11/markup.txt')]:
 p=Path(pa);out['sources'][n]={'path':pa,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
out['episodes']=[]
for name,a,b,actor in [('caviarrun',373,436,'7'),('caviarrun',385,489,'6'),('behave',8946,8997,'group1,2'),('behave',10856,10925,'group0,1')]:
 pts=json.loads((P/(name+'_clock.json')).read_text())['pts'];out['episodes'].append({'source':name,'actor':actor,'candidate_index_inclusive':[a,b],'canonical_half_open_seconds':[a/25,(b+1)/25],'original_pts_seconds_at_candidate_endpoints':[pts[a]['time'],pts[b]['time']],'origin_sensitivity_pts_seconds':{str(d):[pts[a+d]['time'],pts[b+d]['time']] for d in [-1,0,1]}})
(P/'mapping.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
