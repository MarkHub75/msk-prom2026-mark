import requests,pathlib,json,concurrent.futures
p=pathlib.Path('_WORK/W2_06_EVIDENCE')
us={'hf_current':'https://huggingface.co/api/models/rabahdev/fire-smoke-yolov8n','dfire_readme':'https://raw.githubusercontent.com/gaiasd/DFireDataset/master/README.md','dfire_license':'https://raw.githubusercontent.com/gaiasd/DFireDataset/master/LICENSE','dfire_commit':'https://api.github.com/repos/gaiasd/DFireDataset/commits/master','model_license':'https://huggingface.co/rabahdev/fire-smoke-yolov8n/raw/13017fe8af477c25f5298d168e2dfede4b000753/LICENSE'}
def get(t):
 k,u=t
 try:r=requests.get(u,timeout=25);(p/(k+'.txt')).write_bytes(r.content);return {'name':k,'url':u,'status':r.status_code,'bytes':len(r.content)}
 except Exception as e:return {'name':k,'url':u,'error':str(e)}
x=list(concurrent.futures.ThreadPoolExecutor(5).map(get,us.items()));(p/'rights_access.json').write_text(json.dumps(x,indent=2));print(x)
