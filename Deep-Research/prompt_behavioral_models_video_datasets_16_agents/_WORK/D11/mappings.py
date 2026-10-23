import pathlib,requests,json,concurrent.futures
p=pathlib.Path('_WORK/D11')
items=requests.get('https://data.kitware.com/api/v1/item?folderId=56f57e748d777f753209bed8&limit=0',timeout=30).json();(p/'all_annotation_items.json').write_text(json.dumps(items))
sel=[x for x in items if x['name'].endswith('mapping.txt')][:24]
def get(x):
 u='https://data.kitware.com/api/v1/item/'+x['_id']+'/download';r=requests.get(u,timeout=20);(p/x['name']).write_bytes(r.content);runs=[l for l in r.text.splitlines() if len(l.split())>2 and l.split()[1]=='10'];return dict(name=x['name'],url=u,status=r.status_code,run_rows=runs)
r=list(concurrent.futures.ThreadPoolExecutor(6).map(get,sel));(p/'mapping_checks.json').write_text(json.dumps(r,indent=2));print(json.dumps([x for x in r if x['run_rows']],indent=2))
