import requests,pathlib,concurrent.futures,json,zipfile,io,csv
p=pathlib.Path('_WORK/W1_D12')
def f(k):
 u=f'https://iplab.dmi.unict.it/sharing/MECCANO/MECCANO_{k}_bounding_box_annotations.zip';r=requests.get(u,timeout=30);(p/('meccano_'+k+'.zip')).write_bytes(r.content)
 z=zipfile.ZipFile(io.BytesIO(r.content));print(k,r.status_code,len(r.content),z.namelist()[:10])
 for n in z.namelist():
  if n.endswith('.json'):
   b=z.read(n);d=json.loads(b);print(n,list(d)[:8],str(d)[:1200]);(p/(k+'_'+pathlib.Path(n).name)).write_bytes(b)
  elif 'readme' in n.lower():print(n,z.read(n)[:2000])
list(concurrent.futures.ThreadPoolExecutor(2).map(f,['hands','active_object']))
