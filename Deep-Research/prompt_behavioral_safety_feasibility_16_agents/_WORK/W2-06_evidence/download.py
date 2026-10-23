import requests,pathlib,json,hashlib,concurrent.futures
r=pathlib.Path('_WORK/W2-06_evidence');base='https://raw.githubusercontent.com/steffensbola/furg-fire-dataset/6aff09d7baa27425f31d1df685284c26cbffe7af/'
def get(pair):
 name,url=pair;p=r/name
 q=requests.get(url,timeout=90);q.raise_for_status();b=q.content
 if len(b)>35000000:raise ValueError('bound')
 p.write_bytes(b);return dict(file=name,url=url,status=q.status_code,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
items=[(n,base+n) for n in ['README.md','LICENSE','Car1.mp4','Car1.xml','non_fire_patrolbot_onboard.mp4','non_fire_patrolbot_onboard.xml','barbecue.mp4','barbecue.xml']]
for short,repo,rev in [('rabah','rabahdev/fire-smoke-yolov8n','13017fe8af477c25f5298d168e2dfede4b000753'),('farhat','farhatullah0066/yolov8n-fire-smoke-detection','e4f808eb87d72b53ccc860c007f564baf174540a')]:
 items += [(short+'_best.pt',f'https://huggingface.co/{repo}/resolve/{rev}/best.pt'),(short+'_README.md',f'https://huggingface.co/{repo}/raw/{rev}/README.md'),(short+'_api.json',f'https://huggingface.co/api/models/{repo}?blobs=true')]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: rec=list(ex.map(get,items))
(r/'downloads.json').write_text(json.dumps(rec,indent=2));print(json.dumps(rec,indent=2))
