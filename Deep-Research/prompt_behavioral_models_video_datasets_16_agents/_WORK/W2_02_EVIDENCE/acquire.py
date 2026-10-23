from pathlib import Path
import requests,json,shutil,hashlib,datetime
E=Path('_WORK/W2_02_EVIDENCE'); log=[]
def get(url,name):
 r=requests.get(url,timeout=(15,55)); log.append(dict(url=url,status=r.status_code,bytes=len(r.content),type=r.headers.get('Content-Type'),sha256=hashlib.sha256(r.content).hexdigest(),at=datetime.datetime.now(datetime.timezone.utc).isoformat())); (E/'access.json').write_text(json.dumps(log,indent=2),encoding='utf-8'); (E/name).write_bytes(r.content); return r
base='https://api.github.com/repos/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/'
j=get(base+'git/trees/5abac7693229900cf80f722e878fbb119211fc1c?recursive=1','gmd_tree.json').json()
print(j.get('message','tree obtained'))
for src,name in [('../prompt_behavioral_safety_feasibility_16_agents/_WORK/W1-09_samples/positive_S1_F11.mp4','S1_F11.mp4'),('../prompt_behavioral_safety_feasibility_16_agents/_WORK/W1-09_samples/negative_S3_A08.mp4','S3_A08.mp4')]:
 shutil.copy2(src,E/name);log.append(dict(reused_from=src,name=name,bytes=(E/name).stat().st_size,sha256=hashlib.sha256((E/name).read_bytes()).hexdigest()))
raw='https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/5abac7693229900cf80f722e878fbb119211fc1c/'
get(raw+'Subject%204/Fall/01.mp4','S4_F01.mp4')
for name in ['LICENSE','README.md']:get(raw+name,'gmd_'+name)
get('https://zenodo.org/api/records/13354453','zenodo.json')
get('https://fenix.ur.edu.pl/~mkepski/ds/data/adl-10-cam0.mp4','adl-10-cam0.mp4')
get('https://fenix.ur.edu.pl/~mkepski/ds/uf.html','urfd_page.html')
(E/'access.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
print(log)
