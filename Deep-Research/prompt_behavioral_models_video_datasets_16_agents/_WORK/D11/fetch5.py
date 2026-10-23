import requests,pathlib,json,datetime,hashlib,concurrent.futures
p=pathlib.Path('_WORK/D11'); rev=json.loads((p/'virat_commit.json').read_text())['id']
urls={'README_format_release2.txt':'https://data.kitware.com/api/v1/item/56f581c78d777f753209c9c6/download','VIRAT_S_000001.viratdata.events.txt':'https://data.kitware.com/api/v1/item/56f57e748d777f753209bed9/download','VIRAT_S_000001.viratdata.mapping.txt':'https://data.kitware.com/api/v1/item/56f57e748d777f753209bedc/download','VIRAT_S_000001.activities.yml':f'https://gitlab.kitware.com/viratdata/viratannotations/-/raw/{rev}/train/VIRAT_S_000001.activities.yml','video_files.json':'https://data.kitware.com/api/v1/item/56f581ce8d777f753209ca44/files'}
def get(t):
 n,u=t;r=requests.get(u,timeout=30);(p/n).write_bytes(r.content);return dict(name=n,url=u,status=r.status_code,bytes=len(r.content),access=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(r.content).hexdigest())
r=list(concurrent.futures.ThreadPoolExecutor(5).map(get,urls.items()));(p/'access5.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
import yaml
acts=yaml.safe_load((p/'VIRAT_S_000001.activities.yml').read_text());out=[]
for x in acts:
 a=x.get('act',{});lab=next(iter(a.get('act2',{})),'')
 if lab=='activity_running':out.append(a)
(p/'virat_runs.json').write_text(json.dumps(out,indent=2));print('runs',out)
