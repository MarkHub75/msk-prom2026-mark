import requests,pathlib,json,datetime,hashlib,concurrent.futures
p=pathlib.Path('_WORK/D11')
urls={
'35450-47160.avi':'https://groups.inf.ed.ac.uk/vision/DATASETS/BEHAVEDATA/INTERACTIONS/35450-47160.avi',
'virat_r2_folders.json':'https://data.kitware.com/api/v1/folder?parentType=folder&parentId=56f57e748d777f753209bed6&limit=100',
'virat_r2_items.json':'https://data.kitware.com/api/v1/item?folderId=56f57e748d777f753209bed6&limit=100',
'diva.pdf':'https://gitlab.kitware.com/viratdata/viratannotations/-/raw/master/DIVA-Annotation-Guidelines-V1.0.docx.pdf',
'virat_commit.json':'https://gitlab.kitware.com/api/v4/projects/viratdata%2Fviratannotations/repository/commits/master',
'virat_train_tree.json':'https://gitlab.kitware.com/api/v4/projects/viratdata%2Fviratannotations/repository/tree?path=train&per_page=100'}
def get(it):
 n,u=it;t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=requests.get(u,timeout=45,stream=True);b=bytearray()
  for chunk in r.iter_content(65536):
   b.extend(chunk)
   if len(b)>22000000:raise ValueError('size bound')
  (p/n).write_bytes(b)
  return dict(name=n,url=u,final=r.url,status=r.status_code,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),access=t,headers=dict(r.headers))
 except Exception as e:return dict(name=n,url=u,access=t,error=str(e))
res=list(concurrent.futures.ThreadPoolExecutor(5).map(get,urls.items()));(p/'access2.json').write_text(json.dumps(res,indent=2));print(json.dumps([{k:v for k,v in x.items() if k!='headers'} for x in res],indent=2))
import fitz
d=fitz.open(p/'diva.pdf');(p/'diva.txt').write_text('\n'.join(x.get_text() for x in d),encoding='utf8')
