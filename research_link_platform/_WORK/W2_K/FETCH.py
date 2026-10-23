import requests,json,datetime,pathlib,re
p=pathlib.Path('research_link_platform/_WORK/W2_K')
urls={'ADMIN':'https://ivacv.ru/wp-content/uploads/2026/05/Руководство_администратора_сайт.pdf','USER':'https://ivacv.ru/wp-content/uploads/2026/05/Руководство-пользователя-сайт.pdf','VIDEO_PAGE':'https://gdspace.ru/interview/2391','PLATFORM':'https://ivacv.ru/platforma/'}
log=[]
for name,url in urls.items():
 try:
  r=requests.get(url,timeout=25); row={'name':name,'url':url,'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':r.status_code,'bytes':len(r.content),'type':r.headers.get('Content-Type')}
  if r.status_code==200:
   (p/(name+('.pdf' if r.content.startswith(b'%PDF') else '.html'))).write_bytes(r.content)
  log.append(row)
 except Exception as e:log.append({'name':name,'error':str(e),'time':datetime.datetime.now(datetime.timezone.utc).isoformat()})
(p/'HTTP_LOG.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(log,ensure_ascii=False,indent=2))
