import requests,pathlib,json,concurrent.futures
p=pathlib.Path('_WORK/MATERIALS/W2-10');folders=json.loads((p/'folders.json').read_text());
def get(f):
 u='https://data.mendeley.com/public-api/datasets/xjmtb22pff/files';r=requests.get(u,params={'folder_id':f['id'],'version':1,'$start':0,'$limit':1000},timeout=40);(p/('files-'+f['id']+'.json')).write_bytes(r.content);return {'folder':f,'status':r.status_code,'files':r.json()}
a=list(concurrent.futures.ThreadPoolExecutor(8).map(get,folders));(p/'MANIFEST.json').write_text(json.dumps(a,indent=2),encoding='utf8');print([(x['folder']['name'],len(x['files'])) for x in a]);print('total',sum(len(x['files']) for x in a));print(json.dumps(next(x['files'][0] for x in a if x['files']),indent=2))
