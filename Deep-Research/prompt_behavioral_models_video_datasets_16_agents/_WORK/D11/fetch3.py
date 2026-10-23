import requests,pathlib,json,concurrent.futures
p=pathlib.Path('_WORK/D11'); rev=json.loads((p/'virat_commit.json').read_text())['id'];print('revision',rev)
urls={
'ground_folders.json':'https://data.kitware.com/api/v1/folder?parentType=folder&parentId=56f57e748d777f753209bed7&limit=100',
'ground_items.json':'https://data.kitware.com/api/v1/item?folderId=56f57e748d777f753209bed7&limit=100',
'VIRAT_S_000000.activities.yml':f'https://gitlab.kitware.com/viratdata/viratannotations/-/raw/{rev}/train/VIRAT_S_000000.activities.yml',
'VIRAT_S_000000.types.yml':f'https://gitlab.kitware.com/viratdata/viratannotations/-/raw/{rev}/train/VIRAT_S_000000.types.yml',
'validate_tree.json':'https://gitlab.kitware.com/api/v4/projects/viratdata%2Fviratannotations/repository/tree?path=validate&per_page=100'}
def get(t):
 n,u=t;r=requests.get(u,timeout=35);(p/n).write_bytes(r.content);return dict(name=n,url=u,status=r.status_code,bytes=len(r.content))
r=list(concurrent.futures.ThreadPoolExecutor(5).map(get,urls.items()));(p/'access3.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
