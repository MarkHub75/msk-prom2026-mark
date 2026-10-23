import requests,pathlib,json,datetime,concurrent.futures
p=pathlib.Path('_WORK/evidence_D10')
urls=['https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-cam0-rgb.zip','https://fenix.ur.edu.pl/~mkepski/ds/data/adl-10-cam0.mp4','https://fenix.ur.edu.pl/~mkepski/ds/data/adl-10-data.csv','https://www.iro.umontreal.ca/~labimage/Dataset/technicalReport.pdf','https://imvia.u-bourgogne.fr/en/database/fall-detection-dataset-2.html','https://zenodo.org/api/records/12773013']
def f(u):
 try:
  r=requests.get(u,timeout=20,stream=True); out={'url':u,'status':r.status_code,'final':r.url,'type':r.headers.get('Content-Type'),'length':r.headers.get('Content-Length')}
  if 'api/records' in u:
   j=r.json(); p.joinpath('zenodo12773013.json').write_text(json.dumps(j,indent=2),encoding='utf-8');out['license']=j.get('metadata',{}).get('license');out['files']=[{'key':x['key'],'size':x['size'],'url':x['links']['self']} for x in j.get('files',[])]
  elif u.endswith('.csv'):
   data=r.content;p.joinpath(u.split('/')[-1]).write_bytes(data);out['bytes']=len(data)
  r.close();return out
 except Exception as e:return {'url':u,'error':str(e)}
res=list(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(f,urls));p.joinpath('access2.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':res},indent=2),encoding='utf-8');print(json.dumps(res,indent=2))
