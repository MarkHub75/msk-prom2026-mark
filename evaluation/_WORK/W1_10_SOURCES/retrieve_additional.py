import urllib.request,pathlib,json,hashlib,datetime,concurrent.futures
p=pathlib.Path('_WORK/W1_10_SOURCES')
items=[('predictor.py','https://raw.githubusercontent.com/ultralytics/ultralytics/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/engine/predictor.py'),('augment.py','https://raw.githubusercontent.com/ultralytics/ultralytics/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/data/augment.py'),('ops.py','https://raw.githubusercontent.com/ultralytics/ultralytics/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/utils/ops.py'),('ort-quantization.html','https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html'),('ort-execution-providers.html','https://onnxruntime.ai/docs/execution-providers/'),('trt-accuracy.html','https://docs.nvidia.com/deeplearning/tensorrt/10.8.0/inference-library/accuracy-considerations.html'),('trt-troubleshooting.html','https://docs.nvidia.com/deeplearning/tensorrt/10.8.0/reference/troubleshooting.html'),('torch-onnx-2.5.html','https://docs.pytorch.org/docs/2.5/onnx.html'),('torchvision-nms.html','https://docs.pytorch.org/vision/0.20/generated/torchvision.ops.nms.html')]
def get(x):
 name,u=x
 try:
  r=urllib.request.urlopen(u,timeout=30);b=r.read();(p/name).write_bytes(b);return {'name':name,'url':u,'final_url':r.url,'status':r.status,'sha256':hashlib.sha256(b).hexdigest(),'access_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 except Exception as e:return {'name':name,'url':u,'error':str(e)}
r=list(concurrent.futures.ThreadPoolExecutor(9).map(get,items));(p/'additional-provenance.json').write_text(json.dumps(r,indent=2),encoding='utf8');print(json.dumps(r,indent=2))
