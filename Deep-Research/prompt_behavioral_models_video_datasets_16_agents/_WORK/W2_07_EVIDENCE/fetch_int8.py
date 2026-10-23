import pathlib,requests,hashlib,json,tarfile,io
p=pathlib.Path('_WORK/W2_07_EVIDENCE'); logs=[]
u='https://www.kaggle.com/api/v1/models/google/movinet/tflite/a0-stream-kinetics-600-classification-tflite-int8/1/download';r=requests.get(u,timeout=45); (p/'int8_v1.tar.gz').write_bytes(r.content); logs.append(dict(url=u,status=r.status_code,headers=dict(r.headers),bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())); t=tarfile.open(fileobj=io.BytesIO(r.content)); print([(x.name,x.size) for x in t.getmembers()]);
for x in t.getmembers():
 if x.isfile() and x.size<15000000:
  b=t.extractfile(x).read(); (p/('int8_'+pathlib.Path(x.name).name)).write_bytes(b); print(x.name,hashlib.sha256(b).hexdigest())
for i,u in enumerate(['https://www.kaggle.com/api/v1/models/google/movinet','https://www.kaggle.com/api/v1/models/google/movinet/tflite/a0-stream-kinetics-600-classification-tflite-int8/1','https://www.kaggle.com/api/v1/models/list?search=movinet']):
 r=requests.get(u,timeout=30); (p/f'kaggle_meta_{i}.txt').write_text(r.text,encoding='utf8'); logs.append(dict(url=u,status=r.status_code,headers=dict(r.headers),bytes=len(r.content))); print(i,r.status_code,r.text[:200])
(p/'int8_fetch_log.json').write_text(json.dumps(logs,indent=2))
