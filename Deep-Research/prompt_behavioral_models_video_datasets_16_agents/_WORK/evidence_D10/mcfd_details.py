import requests,pathlib,json,concurrent.futures
p=pathlib.Path('_WORK/evidence_D10');base='https://www.iro.umontreal.ca/~labimage/Dataset/'
r=requests.get(base+'Erratum-MCF.pdf',timeout=20);p.joinpath('Erratum-MCF.pdf').write_bytes(r.content);print('erratum',r.status_code,len(r.content),r.headers.get('Content-Type'))
import pymupdf
for n in ['technicalReport.pdf','Erratum-MCF.pdf']:
 d=pymupdf.open(p/n);t='\n'.join(x.get_text() for x in d);p.joinpath(n+'.txt').write_text(t,encoding='utf-8');print(n,'pages',len(d));print(t if 'Erratum' in n else t[t.find('4.3 Ground'):t.find('4.3 Ground')+1200])
def f(s):
 u=base+s
 try:
  r=requests.get(u,timeout=20,stream=True);v={'url':u,'status':r.status_code,'type':r.headers.get('Content-Type'),'length':r.headers.get('Content-Length')};r.close();return v
 except Exception as e:return {'url':u,'error':str(e)}
res=list(concurrent.futures.ThreadPoolExecutor(max_workers=3).map(f,['dataset.zip','chute-zip/chute23.zip','chute-zip/chute24.zip']));p.joinpath('mcfd_access.json').write_text(json.dumps(res,indent=2),encoding='utf-8');print(json.dumps(res,indent=2))
