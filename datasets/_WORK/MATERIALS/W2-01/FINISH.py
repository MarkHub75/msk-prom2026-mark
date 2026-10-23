import json,requests,pathlib
p=pathlib.Path('_WORK/MATERIALS/W2-01');q=json.loads((p/'MANIFEST_PROGRESS.json').read_text());token=q['nextPageToken'];s=requests.Session()
while token:
 r=s.get('https://www.kaggle.com/api/v1/datasets/list/mugheesahmad/sh17-dataset-for-ppe-detection',params={'pageSize':1000,'pageToken':token},timeout=35)
 if r.status_code!=200:print(r.status_code);break
 j=r.json();q['files']+=j['datasetFiles'];token=j.get('nextPageToken');q['nextPageToken']=token;(p/'MANIFEST_PROGRESS.json').write_text(json.dumps(q,indent=2))
print('complete',len(q['files']),bool(token));print([x['name'] for x in q['files'][-8:]])
# official file endpoint uses filename basename? inspect alternative documented Kaggle URL
name='labels/pexels-photo-5691469.txt'
for i,url in enumerate(['https://www.kaggle.com/api/v1/datasets/download/mugheesahmad/sh17-dataset-for-ppe-detection/'+name+'?datasetVersionNumber=1','https://www.kaggle.com/api/v1/datasets/download/mugheesahmad/sh17-dataset-for-ppe-detection?fileName='+name,'https://www.kaggle.com/api/v1/datasets/download/mugheesahmad/sh17-dataset-for-ppe-detection/pexels-photo-5691469.txt']):
 r=s.get(url,timeout=40);(p/('label_attempt'+str(i)+'.payload')).write_bytes(r.content);print(i,r.status_code,len(r.content),r.headers.get('Content-Type'))
