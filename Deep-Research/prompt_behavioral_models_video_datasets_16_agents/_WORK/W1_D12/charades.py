import requests,pathlib,zipfile,io,json,concurrent.futures
p=pathlib.Path('_WORK/W1_D12')
urls={'charades_annotations':'https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades.zip','charades_video':'https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades_v1_480.zip','meccano_weight':'https://iplab.dmi.unict.it/sharing/MECCANO/models/active_object_recognition/MECCANO_active_objects.pth','100doh_ego_weight':'https://drive.google.com/file/d/1H2tWsZkS7tDF8q1-jdjx6V9XrK25EDbE/view'}
def f(k,u):
 try:
  r=requests.get(u,headers={'Range':'bytes=0-2097151' if 'annotations' in k else 'bytes=0-511'},stream=True,timeout=20);b=next(r.iter_content(2097152 if 'annotations' in k else 512),b'');r.close();(p/(k+'.probe')).write_bytes(b);return dict(key=k,url=u,status=r.status_code,headers=dict(r.headers),bytes_read=len(b))
 except Exception as e:return dict(key=k,url=u,error=str(e))
a=list(concurrent.futures.ThreadPoolExecutor(4).map(lambda x:f(*x),urls.items()));(p/'probes2.json').write_text(json.dumps(a,indent=2));print([{k:v for k,v in d.items() if k!='headers'}|{'size':d.get('headers',{}).get('Content-Range')} for d in a])
try:
 with zipfile.ZipFile(p/'charades_annotations.probe') as z:
  print(z.namelist())
  for n in z.namelist():
   if not n.endswith('/'):(p/('charades_'+pathlib.Path(n).name)).write_bytes(z.read(n))
except Exception as e: print(e)
