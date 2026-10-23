import ast,json,pathlib,hashlib,urllib.request,datetime
r=pathlib.Path(__file__).parent
s=r.parent/'W1_09/PYTPU_SOURCE/pytpu-15.0.24/pytpu'
out={}
for f in [s/'_bindings.py',s/'_converter_to_raw.py']:
 t=ast.parse(f.read_text())
 out[f.name]={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'definitions':[{'name':n.name,'start':n.lineno,'end':n.end_lineno} for n in ast.walk(t) if isinstance(n,(ast.FunctionDef,ast.ClassDef))]}
(r/'SOURCE_LOCATORS.json').write_text(json.dumps(out,indent=2))
a=json.loads((r/'MLPERF_TREE.json').read_text())
x=next(x for x in a['tree'] if x['path']=='closed/IVATech')
url='https://api.github.com/repos/mlcommons/inference_results_v0.7/git/trees/'+x['sha']+'?recursive=1'
data=urllib.request.urlopen(url,timeout=20).read()
(r/'MLPERF_SUBTREE.json').write_bytes(data)
obj=json.loads(data)
print('subtree truncated:',obj.get('truncated'))
print([x['path'] for x in obj['tree'] if x['path'].endswith(('.tpu','.zip','.h'))])
(r/'SUBTREE_FETCH.json').write_text(json.dumps({'url':url,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(data)},indent=2))
