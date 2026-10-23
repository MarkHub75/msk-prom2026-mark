import requests,json,pathlib,datetime,concurrent.futures
p=pathlib.Path('_WORK/W1_D12')
urls={'100doh_download':'https://fouheylab.eecs.umich.edu/~dandans/projects/100DOH/download.html','100doh_readme':'https://raw.githubusercontent.com/ddshan/hand_object_detector/master/README.md','100doh_demo':'https://raw.githubusercontent.com/ddshan/hand_object_detector/master/demo.py','100doh_voc':'https://raw.githubusercontent.com/ddshan/hand_object_detector/master/lib/datasets/pascal_voc.py','pdestre':'http://p-destre.di.ubi.pt/index.html','pdestre_https':'https://p-destre.di.ubi.pt/index.html'}
def fetch(k,u):
 try:
  r=requests.get(u,timeout=30); (p/(k+'.txt')).write_text(r.text,encoding='utf-8'); return dict(key=k,url=u,status=r.status_code,bytes=len(r.content),final=r.url,time=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:return dict(key=k,url=u,error=str(e))
a=list(concurrent.futures.ThreadPoolExecutor(6).map(lambda kv:fetch(*kv),urls.items())); (p/'access.json').write_text(json.dumps(a,indent=2),encoding='utf-8');print(json.dumps(a,indent=2))
