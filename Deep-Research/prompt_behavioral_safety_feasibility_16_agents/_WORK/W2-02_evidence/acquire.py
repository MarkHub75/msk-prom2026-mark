import urllib.request, pathlib, hashlib, json, datetime, concurrent.futures
ROOT=pathlib.Path(__file__).parent
items={
'yolox_nano.onnx':'https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_nano.onnx',
'yolov8n-pose.pt':'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-pose.pt',
'rtmpose-t.zip':'https://huggingface.co/Tau-J/RTMPose/resolve/cd4d7095f5cfc9cfc4f46289bee91ea4a1e1d9fd/rtmposev1/onnx_sdk/rtmpose-t_simcc-body7_pt-body7_420e-256x192-026a1439_20230504.zip'}
def get(k,u):
 rec={'file':k,'url':u,'access_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'W2-static-research'}),timeout=60) as r:
   rec.update(status=r.status,headers=dict(r.headers))
   b=r.read(16*1024*1024+1)
   if len(b)>16*1024*1024: raise ValueError('bounded download exceeded')
  (ROOT/k).write_bytes(b)
  rec.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e: rec['error']=str(e)
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as p: results=list(p.map(lambda kv:get(*kv),items.items()))
(ROOT/'downloads.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps([{k:v for k,v in x.items() if k!='headers'} for x in results],indent=2))
