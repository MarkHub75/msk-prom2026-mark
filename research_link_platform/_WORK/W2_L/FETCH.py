import concurrent.futures, datetime, hashlib, json, pathlib, re, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
URLS={'HOME':'https://lin-q.ru/','SOL':'https://lin-q.ru/sol','HR':'https://lin-q.ru/hr','FOOTER':'https://lin-q.ru/footer','CASE':'https://hackathon2026.otkroimosprom.ru/'}
def run(pair):
 name,url=pair; item={'name':name,'url':url,'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'urllib HTTPS GET; no cookies/login/form submission'}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=22) as r: data=r.read(); item.update(status=r.status,final_url=r.url,headers=dict(r.headers),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
  (ROOT/(name+'.html')).write_bytes(data)
  s=data.decode('utf-8','replace'); item['links']=sorted(set(re.findall(r'''(?:href|action)=["']([^"']+)''',s)))
  item['relevant_contexts']=[s[max(0,m.start()-180):m.end()+350] for m in re.finditer('linq|cloud|облач|вериф|popup|quota|upload|iframe|ssh|api|прототип|альфа',s,re.I) if ('script' not in s[max(0,m.start()-20):m.start()].lower())][:100]
 except Exception as e:item.update(error=repr(e))
 item['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat(); return item
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: rows=list(pool.map(run,URLS.items()))
(ROOT/'HTTP_LOG.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{k:v for k,v in r.items() if k in ('name','status','error','bytes','start_utc','end_utc')} for r in rows],ensure_ascii=False))
