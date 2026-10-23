import requests,json,pathlib,zipfile,xml.etree.ElementTree as E
p=pathlib.Path('_WORK/MATERIALS/W2-01'); j=json.loads((p/'kaggle_page.txt').read_text()); tok=j['nextPageToken'];u='https://www.kaggle.com/api/v1/datasets/list/mugheesahmad/sh17-dataset-for-ppe-detection'
for key in ['pageToken','page']:
 r=requests.get(u,params={'pageSize':1000,key:tok},timeout=40);(p/('page_'+key+'.json')).write_bytes(r.content)
 try:q=r.json();print(key,r.status_code,len(q.get('datasetFiles',[])),q.get('datasetFiles',[{}])[0].get('name'))
 except:print(key,r.status_code,r.text[:80])
# direct known label route
for file in ['labels/pexels-photo-5691469.txt','labels/building-construction-building-site-constructing.txt','sh17.yaml']:
 r=requests.get('https://www.kaggle.com/api/v1/datasets/download/mugheesahmad/sh17-dataset-for-ppe-detection/'+file,timeout=40); dest=p/('released_'+file.replace('/','_'));dest.write_bytes(r.content); print(file,r.status_code,len(r.content),r.headers.get('Content-Type'))
