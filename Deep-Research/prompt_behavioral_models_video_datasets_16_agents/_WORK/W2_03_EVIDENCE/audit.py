import av,hashlib,json
from pathlib import Path
P=Path('_WORK/W2_03_EVIDENCE');out={}
for name,path in [('caviarrun','_WORK/M04/caviarrun.mpg'),('caviarwalk','_WORK/M04/caviarwalk.mpg'),('behave','_WORK/D11/35450-47160.avi')]:
 hs=[]
 for f in av.open(path).decode(video=0):hs.append(hashlib.sha256(f.to_ndarray(format='rgb24').tobytes()).hexdigest())
 adj=[i for i in range(1,len(hs)) if hs[i]==hs[i-1]]
 pts=json.loads((P/(name+'_clock.json')).read_text())['pts']
 out[name]={'adjacent_identical_indices':adj,'first_pts':pts[:12],'last_pts':pts[-3:],'nonincreasing_pts_indices':[i for i in range(1,len(pts)) if pts[i]['pts']<=pts[i-1]['pts']]}
(P/'duplicate_audit.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2)[:8500])
