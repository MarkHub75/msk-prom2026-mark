import requests,json,datetime,pathlib,concurrent.futures
p=pathlib.Path('_WORK/M01')
urls={
'rtmpose':'https://raw.githubusercontent.com/open-mmlab/mmpose/main/projects/rtmpose/README.md',
'rtmo':'https://raw.githubusercontent.com/open-mmlab/mmpose/main/projects/rtmo/README.md',
'vitpose':'https://raw.githubusercontent.com/ViTAE-Transformer/ViTPose/main/README.md',
'ultra_pose':'https://raw.githubusercontent.com/ultralytics/ultralytics/main/docs/en/tasks/pose.md',
'mmpose_license':'https://raw.githubusercontent.com/open-mmlab/mmpose/main/LICENSE',
'vitpose_license':'https://raw.githubusercontent.com/ViTAE-Transformer/ViTPose/main/LICENSE',
'ultra_license':'https://raw.githubusercontent.com/ultralytics/ultralytics/main/LICENSE',
'mp_card':'https://storage.googleapis.com/mediapipe-assets/Model%20Card%20BlazePose%20GHUM%203D.pdf',
'mp_old':'https://raw.githubusercontent.com/google-ai-edge/mediapipe/master/docs/solutions/pose.md',
'movenet_multi':'https://raw.githubusercontent.com/tensorflow/tfjs-models/master/pose-detection/src/movenet/README.md',
'coco_eval':'https://raw.githubusercontent.com/cocodataset/cocoapi/master/PythonAPI/pycocotools/cocoeval.py',
'coco_terms':'https://cocodataset.org/#termsofuse',
}
def fetch(k,u):
 try:
  r=requests.get(u,timeout=35); fn=k+('.pdf' if 'pdf' in u else '.txt'); (p/fn).write_bytes(r.content)
  return {'key':k,'url':u,'final_url':r.url,'status':r.status_code,'bytes':len(r.content),'access_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 except Exception as e:return {'key':k,'url':u,'error':str(e)}
res=list(concurrent.futures.ThreadPoolExecutor(8).map(lambda kv:fetch(*kv),urls.items()))
(p/'FETCH.json').write_text(json.dumps(res,indent=2),encoding='utf8')
print(json.dumps(res,indent=2))
