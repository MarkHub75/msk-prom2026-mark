import requests,pathlib,json,re
p=pathlib.Path('_WORK/evidence_D10'); results=[]
for name,u in [('mcfd-index.html','https://www.iro.umontreal.ca/~labimage/Dataset/'),('technicalReport.pdf','https://www.iro.umontreal.ca/~labimage/Dataset/technicalReport.pdf')]:
 r=requests.get(u,timeout=25);p.joinpath(name).write_bytes(r.content);results.append({'url':u,'status':r.status_code,'type':r.headers.get('Content-Type'),'bytes':len(r.content)})
 if name.endswith('html'):print(r.text[:16000])
print(results)
try:
 import pymupdf
 d=pymupdf.open(p/'technicalReport.pdf');t='\n'.join(x.get_text() for x in d);p.joinpath('technicalReport.txt').write_text(t,encoding='utf-8');print('pdf pages',len(d));print(t[t.find('4.3 Ground'):t.find('4.3 Ground')+1800])
except Exception as e:print(e)
