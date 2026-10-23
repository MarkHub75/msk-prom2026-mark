import json, datetime, urllib.request, ssl, pathlib, hashlib
root = pathlib.Path(__file__).parent
urls = [
 'https://files.lin-q.ru/tpu/docs/_HPact_manual_LINQ_HP1M_02.pdf',
 'http://files.lin-q.ru/tpu/docs/_HPact_manual_LINQ_HP1M_02.pdf',
 'https://raw.githubusercontent.com/sherstpasha/linq-cv-bench/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/classification/run_resnet50_parallel_direct.py'
]
records=[]
for url in urls:
 r={'url':url,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'urllib.request.urlopen, default verified TLS, timeout=10'}
 try:
  with urllib.request.urlopen(url,timeout=10) as resp:
   data=resp.read(); r.update(status=resp.status,headers=dict(resp.headers),length=len(data),sha256=hashlib.sha256(data).hexdigest())
   if data.startswith(b'%PDF'):
    (root / url.rsplit('/',1)[1]).write_bytes(data)
   elif 'githubusercontent' in url:
    (root / 'PARALLEL_DIRECT_REMOTE.py').write_bytes(data)
 except Exception as e:r['error']=repr(e)
 records.append(r)
(root/'RETRIEVE_PROBE_RESULT.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(records,ensure_ascii=False,indent=2))
