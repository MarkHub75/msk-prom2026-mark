import requests,json,pathlib,hashlib,datetime
p=pathlib.Path('_WORK/W2_04_EVIDENCE'); out=[]
urls=['https://sites.research.google/gr/ava/download/','https://www.youtube.com/watch?v=QTmwhrVal1g','https://www.youtube.com/watch?v=WSPvfxtqisg','https://www.youtube.com/t/terms']
for i,u in enumerate(urls):
 try:
  r=requests.get(u,timeout=(10,20)); b=r.content;p.joinpath(f'http_{i}.html').write_bytes(b);out.append(dict(url=u,final_url=r.url,status=r.status_code,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),content_type=r.headers.get('Content-Type')))
 except Exception as e:out.append(dict(url=u,error=repr(e)))
p.joinpath('access.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
