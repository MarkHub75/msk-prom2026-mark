import requests,pathlib,re,json,concurrent.futures,datetime
out=pathlib.Path('_WORK/M08')
urls=['https://storage.googleapis.com/tf_model_garden/vision/movinet/movinet_a0_stream.tar.gz','https://storage.googleapis.com/tf_model_garden/vision/movinet/movinet_a0_stream.tflite','https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/X3D_XS.pyth','https://download.openmmlab.com/mmaction/v1.0/skeleton/data/ntu60_2d.pkl','https://research.google.com/ava/download/ava_v2.2.zip','https://research.google.com/ava/download/ava_val_v2.2.csv.zip','https://s3.amazonaws.com/kinetics/400/val/k400_val_path.txt']
for f,pattern in [('stgcnpp.txt',r'https[^)]+86e1e77a.pth'),('slowfast.txt',r'https[^)]+39133ec7.pth'),('tsm.txt',r'https[^)]+\.pth'),('videomae.txt',r'https[^)]+860a3cd3.pth')]:
 m=re.search(pattern,(out/f).read_text());
 if m:urls.append(m[0])
def check(u):
 try:
  r=requests.head(u,timeout=20,allow_redirects=True);return dict(url=u,status=r.status_code,final=r.url,headers=dict(r.headers),time=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:return dict(url=u,error=str(e))
a=list(concurrent.futures.ThreadPoolExecutor(8).map(check,urls));(out/'artifact_heads.json').write_text(json.dumps(a,indent=2));print(json.dumps([{k:v for k,v in i.items() if k!='headers'}|{'length':i.get('headers',{}).get('Content-Length'),'type':i.get('headers',{}).get('Content-Type')}for i in a],indent=2))
