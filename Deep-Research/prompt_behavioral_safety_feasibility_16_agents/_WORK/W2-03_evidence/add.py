from pathlib import Path
import requests,json,hashlib
root=Path('_WORK/W2-03_evidence'); p='Subject 3/Fall/07.mp4'; u='https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/5abac7693229900cf80f722e878fbb119211fc1c/'+requests.utils.quote(p,safe='/')
r=requests.get(u,timeout=60); r.raise_for_status(); assert len(r.content)<15000000
name='Subject3_Fall_07.mp4'; (root/name).write_bytes(r.content)
a=dict(path=p,url=u,local=name,status=r.status_code,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest()); path=root/'downloads.json'; out=json.loads(path.read_text()); out.append(a); path.write_text(json.dumps(out,indent=2)); print(a)
