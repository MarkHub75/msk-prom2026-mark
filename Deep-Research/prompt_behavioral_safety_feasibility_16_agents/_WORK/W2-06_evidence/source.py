import requests,pathlib,json
r=pathlib.Path('_WORK/W2-06_evidence');rec=[]
for v in ['v8.4.51','v8.4.150']:
 for name in ['pyproject.toml','LICENSE','ultralytics/engine/exporter.py','ultralytics/nn/modules/head.py','ultralytics/data/augment.py']:
  u=f'https://raw.githubusercontent.com/ultralytics/ultralytics/{v}/{name}';q=requests.get(u,timeout=30);p=v+'_'+name.replace('/','_');(r/p).write_bytes(q.content);rec.append({'version':v,'source':name,'url':u,'status':q.status_code,'bytes':len(q.content)})
u='https://api.github.com/repos/Supakorn289/fire-smoke-detection-r3e6/git/trees/676f3280cf643f874ae6f12b41a4a412409d2830?recursive=1';q=requests.get(u,timeout=30);(r/'r3e6_tree.json').write_bytes(q.content);rec.append({'url':u,'status':q.status_code,'license_paths':[x['path'] for x in q.json().get('tree',[]) if any(a in x['path'].lower() for a in ['license','copying','notice'])]})
(r/'sources.json').write_text(json.dumps(rec,indent=2));print(json.dumps(rec,indent=2))
