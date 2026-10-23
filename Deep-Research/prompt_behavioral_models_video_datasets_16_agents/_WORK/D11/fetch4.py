import requests,json,pathlib,concurrent.futures,datetime,hashlib
p=pathlib.Path('_WORK/D11')
urls={'virat_docs_items.json':'https://data.kitware.com/api/v1/item?folderId=56f581c78d777f753209c9c2&limit=100','virat_video_items.json':'https://data.kitware.com/api/v1/item?folderId=56f581ce8d777f753209ca43&limit=100','virat_annotation_items.json':'https://data.kitware.com/api/v1/item?folderId=56f57e748d777f753209bed8&limit=100'}
def get(t):
 n,u=t;r=requests.get(u,timeout=30);(p/n).write_bytes(r.content);return dict(name=n,url=u,status=r.status_code,bytes=len(r.content),access=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(r.content).hexdigest())
r=list(concurrent.futures.ThreadPoolExecutor(3).map(get,urls.items()));(p/'access4.json').write_text(json.dumps(r,indent=2))
for n in urls:
 print(n,[(x['name'],x['_id'],x['size']) for x in json.loads((p/n).read_text())][:15])
import yaml
acts=yaml.safe_load((p/'VIRAT_S_000000.activities.yml').read_text());runs=[x for x in acts if 'act' in x and 'activity_running' in x['act'].get('act2',{})];print('runs',json.dumps(runs,indent=2))
