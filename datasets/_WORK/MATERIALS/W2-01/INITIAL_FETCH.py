import requests,pathlib,json,concurrent.futures
p=pathlib.Path('_WORK/MATERIALS')
jobs={'kaggle_page':('01','https://www.kaggle.com/api/v1/datasets/list/mugheesahmad/sh17-dataset-for-ppe-detection?pageSize=1000'),'cppe_release':('08','https://api.github.com/repos/Rishit-dagli/CPPE-Dataset/releases/tags/v0.1.0'),'cppe_tree':('08','https://api.github.com/repos/Rishit-dagli/CPPE-Dataset/git/trees/v0.1.0?recursive=1'),'sh17_readme':('12','https://raw.githubusercontent.com/ahmadmughees/SH17dataset/2f832c289f9deea063367045ed8230b26e3e7ea9/README.md'),'sfchd_tree':('12','https://api.github.com/repos/lijfrank/SFCHD-SCALE/git/trees/main?recursive=1'),'sh17_zenodo':('12','https://zenodo.org/api/records/12750834')}
def f(k,v):
 d,u=v
 try:
  r=requests.get(u,timeout=45); (p/('W2-'+d)/(k+'.txt')).write_bytes(r.content); return dict(key=k,url=u,status=r.status_code,bytes=len(r.content),headers=dict(r.headers))
 except Exception as e:return dict(key=k,url=u,error=str(e))
res=list(concurrent.futures.ThreadPoolExecutor(6).map(lambda z:f(*z),jobs.items()))
(p/'W2-01'/'INITIAL_REQUESTS.json').write_text(json.dumps(res,indent=2)); print([(x['key'],x.get('status'),x.get('bytes')) for x in res])
