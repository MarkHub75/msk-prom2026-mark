import requests,json,pathlib,concurrent.futures,hashlib,datetime
p=pathlib.Path('_WORK/W2_06_EVIDENCE'); rev='13017fe8af477c25f5298d168e2dfede4b000753'
urls={'hf_model':f'https://huggingface.co/api/models/rabahdev/fire-smoke-yolov8n/revision/{rev}','hf_card':f'https://huggingface.co/rabahdev/fire-smoke-yolov8n/raw/{rev}/README.md','figshare':'https://api.figshare.com/v2/articles/28804448','article':'https://www.nature.com/articles/s41597-026-06810-6'}
def get(k,u):
 try:
  r=requests.get(u,timeout=35); (p/(k+'.txt')).write_bytes(r.content); return {'name':k,'url':u,'status':r.status_code,'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest(),'headers':dict(r.headers),'final_url':r.url}
 except Exception as e:return {'name':k,'url':u,'error':str(e)}
res=list(concurrent.futures.ThreadPoolExecutor(4).map(lambda t:get(*t),urls.items())); (p/'access_metadata.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':res},indent=2)); print(json.dumps(res,indent=2))
u='https://ndownloader.figshare.com/files/53696243'; r=requests.get(u,headers={'Range':'bytes=0-65535'},timeout=40,stream=True)
b=b''.join(r.iter_content(65536)) if r.status_code==206 else r.raw.read(65536);r.close(); (p/'rar_first64k.bin').write_bytes(b); (p/'rar_access.json').write_text(json.dumps({'url':u,'status':r.status_code,'headers':dict(r.headers),'final_url':r.url,'bytes_read':len(b),'hex_first32':b[:32].hex()},indent=2)); print('RAR',r.status_code,len(b),b[:32],dict(r.headers))
