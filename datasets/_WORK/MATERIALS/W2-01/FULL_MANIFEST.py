import requests,json,pathlib,time
p=pathlib.Path('_WORK/MATERIALS/W2-01'); q=json.loads((p/'kaggle_page.txt').read_text());items=q['datasetFiles'];token=q.get('nextPageToken');log=[];s=requests.Session()
while token:
 r=s.get('https://www.kaggle.com/api/v1/datasets/list/mugheesahmad/sh17-dataset-for-ppe-detection',params={'pageSize':1000,'pageToken':token},timeout=35)
 if r.status_code!=200:log.append({'status':r.status_code,'body':r.text[:400]});break
 q=r.json();items.extend(q.get('datasetFiles',[]));token=q.get('nextPageToken');log.append({'status':r.status_code,'n':len(q.get('datasetFiles',[])),'last':items[-1]['name']});
 (p/'MANIFEST_PROGRESS.json').write_text(json.dumps({'files':items,'nextPageToken':token,'log':log},indent=2))
 if len(log)%10==0:print(len(items),items[-1]['name'],flush=True)
 if len(log)>100:break
print('done',len(items),bool(token));print([x['name'] for x in items if not x['name'].startswith('images/')][:12])
