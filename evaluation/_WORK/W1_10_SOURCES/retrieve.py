import urllib.request,json, pathlib, datetime, hashlib, concurrent.futures
p=pathlib.Path('_WORK/W1_10_SOURCES'); p.mkdir(exist_ok=True)
repos={'ort':('microsoft/onnxruntime','v1.20.1'),'ultra':('ultralytics/ultralytics','v8.3.0'),'onnx':('onnx/onnx','v1.17.0'),'torch':('pytorch/pytorch','v2.5.1')}
meta={}
def req(u):
 r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'research-parity/1.0'}),timeout=45); return r.read(),r.url,r.status
for key,(repo,tag) in repos.items():
 try:
  b,_,_=req('https://api.github.com/repos/'+repo+'/commits/'+tag); x=json.loads(b); meta[key]={'repo':repo,'tag':tag,'sha':x['sha'],'date':x['commit']['committer']['date']}
 except Exception as e: meta[key]={'error':str(e)}
resolved={'ort':'5c1b7ccbff7e5141c1da7a9d963d660e5741c319','ultra':'a46b49a27a97d44c642882a405c8b57979e6d368','onnx':'b8baa8446686496da4cc8fda09f2b6fe65c2a02c','torch':'a8d6afb511a69687bbb2b7e88a3cf67917e1697e'}
for key,sha in resolved.items(): meta[key].update({'repo':repos[key][0],'tag':repos[key][1],'sha':sha,'date':'unknown; GitHub API rate limited; SHA obtained by git ls-remote tag'})
(p/'versions.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
files=[('ort','docs/execution-providers/index.md','ort-execution-providers.md'),('ort','docs/performance/model-optimizations/quantization.md','ort-quantization.md'),('ort','onnxruntime/python/tools/quantization/qdq_loss_debug.py','qdq_loss_debug.py'),('ultra','ultralytics/engine/predictor.py','predictor.py'),('ultra','ultralytics/data/augment.py','augment.py'),('ultra','ultralytics/utils/ops.py','ops.py'),('onnx','onnx/defs/object_detection/defs.cc','object_detection_defs.cc'),('torch','docs/source/notes/numerical_accuracy.rst','numerical_accuracy.rst')]
def get(f):
 k,loc,name=f
 if 'sha' not in meta[k]:return {'file':name,'error':'unresolved'}
 u='https://raw.githubusercontent.com/'+meta[k]['repo']+'/'+meta[k]['sha']+'/'+loc
 try:
  b,final,status=req(u); (p/name).write_bytes(b);return {'file':name,'url':u,'final_url':final,'status':status,'sha256':hashlib.sha256(b).hexdigest(),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'locator':loc,**meta[k]}
 except Exception as e:return {'file':name,'url':u,'error':str(e)}
res=list(concurrent.futures.ThreadPoolExecutor(8).map(get,files));(p/'provenance.json').write_text(json.dumps(res,indent=2),encoding='utf8');print(json.dumps(meta,indent=2));print(json.dumps(res,indent=2))
