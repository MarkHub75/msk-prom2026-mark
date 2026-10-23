from pathlib import Path
import requests,json,hashlib
from concurrent.futures import ThreadPoolExecutor
root=Path('_WORK/W2-03_evidence'); base='https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/5abac7693229900cf80f722e878fbb119211fc1c/'
paths=['Subject 1/Fall/13.mp4','Subject 1/ADL/16.mp4','Subject 4/ADL/05.mp4','Subject 1/ADL.csv','Subject 2/Fall.csv','Subject 3/Fall.csv','Subject 4/Fall.csv','Subject 4/ADL.csv','README.md','LICENSE']
def get(p):
 u=base+requests.utils.quote(p,safe='/'); r=requests.get(u,timeout=50); r.raise_for_status(); assert len(r.content)<15000000
 name=p.replace('/','_').replace(' ',''); (root/name).write_bytes(r.content)
 return dict(path=p,url=u,local=name,status=r.status_code,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
with ThreadPoolExecutor(max_workers=4) as ex: out=list(ex.map(get,paths))
(root/'downloads.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
