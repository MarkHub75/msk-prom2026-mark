import pathlib,re,json,requests,importlib.util
for n in ['09','10','11','14','15']:
 p=pathlib.Path('_WORK/MATERIALS/W2-'+n);p.mkdir(exist_ok=True)
 pathlib.Path('_WORK/W2-'+n+'.md').write_text('# W2-'+n+' — рабочий результат\n\nДата доступа 2026-10-23. Работа в процессе; основания и ограничения сохраняются прогрессивно.\n',encoding='utf8')
s=pathlib.Path('_WORK/MATERIALS/W1-15/mendeley-app.js').read_text(encoding='utf8')
for pat in ['public-api','/folders','/files']:
 print(pat,[(m.start(),s[max(0,m.start()-100):m.start()+160]) for m in list(re.finditer(re.escape(pat),s))[:8]])
for m in ['rarfile','PIL','cv2','imageio_ffmpeg']:
 print(m, bool(importlib.util.find_spec(m)))
urls={'files':'https://data.mendeley.com/public-api/datasets/xjmtb22pff/versions/1/files','folders':'https://data.mendeley.com/public-api/datasets/xjmtb22pff/versions/1/folders','paper':'https://mdpi-res.com/d_attachment/electronics/electronics-12-03225/article_deploy/electronics-12-03225.pdf'}
for k,u in urls.items():
 try:
  r=requests.get(u,timeout=40);pathlib.Path('_WORK/MATERIALS/W2-'+('09' if k=='paper' else '10')+'/'+k+('.pdf' if k=='paper' else '.json')).write_bytes(r.content);print(k,r.status_code,len(r.content),r.text[:100] if k!='paper' else r.content[:20])
 except Exception as e: print(k,str(e))
