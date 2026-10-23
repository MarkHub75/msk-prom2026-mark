import requests,pathlib,json,datetime,hashlib,concurrent.futures
p=pathlib.Path('_WORK/D11');p.mkdir(exist_ok=True)
urls={
'behave.html':'https://groups.inf.ed.ac.uk/vision/DATASETS/BEHAVEDATA/INTERACTIONS/index.html',
'markup.txt':'https://groups.inf.ed.ac.uk/vision/DATASETS/BEHAVEDATA/INTERACTIONS/markup.txt',
'35450-47160F.xgtf':'https://groups.inf.ed.ac.uk/vision/DATASETS/BEHAVEDATA/INTERACTIONS/35450-47160F.xgtf',
'virat.html':'https://viratdata.org/',
'virat_release.pdf':'https://data.kitware.com/api/v1/file/56f581c88d777f753209c9ce/download',
'virat_agreement.pdf':'https://viratdata.org/resources/VIRAT-Video-Data-Set-Protection-Agreement-1-4-11.pdf',
'virat_repo_readme.txt':'https://gitlab.kitware.com/viratdata/viratannotations/-/raw/master/README.md',
'virat_tree.json':'https://gitlab.kitware.com/api/v4/projects/viratdata%2Fviratannotations/repository/tree?per_page=100',
'virat_folders.json':'https://data.kitware.com/api/v1/folder?parentType=collection&parentId=56f56f478d777f753209ba9f&limit=100'}
def get(it):
 n,u=it;t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=requests.get(u,timeout=35);b=r.content
  if len(b)<12000000:(p/n).write_bytes(b)
  return dict(name=n,url=u,final=r.url,status=r.status_code,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),access=t,headers=dict(r.headers))
 except Exception as e:return dict(name=n,url=u,access=t,error=str(e))
res=list(concurrent.futures.ThreadPoolExecutor(5).map(get,urls.items()));(p/'access.json').write_text(json.dumps(res,indent=2));print(json.dumps([{k:v for k,v in x.items() if k!='headers'} for x in res],indent=2))
import fitz
for n in ['virat_release','virat_agreement']:
 try:
  d=fitz.open(p/(n+'.pdf'));(p/(n+'.txt')).write_text('\n'.join(x.get_text() for x in d),encoding='utf8')
 except Exception as e: print(e)
