import pathlib, urllib.request, json, hashlib, concurrent.futures
R=pathlib.Path(__file__).parent
y='https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/'
r='https://raw.githubusercontent.com/Tau-J/rtmlib/03a1693e59e4f7cd84582c0fb30459b3bf18ad42/'
urls={
'yolox_readme.md':y+'demo/ONNXRuntime/README.md','yolox_inference.py':y+'demo/ONNXRuntime/onnx_inference.py','yolox_demo_utils.py':y+'yolox/utils/demo_utils.py','yolox_data_augment.py':y+'yolox/data/data_augment.py','yolox_export.py':y+'tools/export_onnx.py','yolox_head.py':y+'yolox/models/yolo_head.py','coco_classes.py':y+'yolox/data/datasets/coco_classes.py',
'rtmpose.py':r+'rtmlib/tools/pose_estimation/rtmpose.py','base.py':r+'rtmlib/tools/base.py','wholebody.py':r+'rtmlib/tools/solution/wholebody.py','body.py':r+'rtmlib/tools/solution/body.py','rtm_pre.py':r+'rtmlib/tools/pose_estimation/pre_processings.py','rtm_post.py':r+'rtmlib/tools/pose_estimation/post_processings.py',
'ultralytics_release.json':'https://api.github.com/repos/ultralytics/assets/releases/tags/v8.3.0','yolox_release.json':'https://api.github.com/repos/Megvii-BaseDetection/YOLOX/releases/tags/0.1.1rc0',
'mmdeploy_pipeline.py':'https://raw.githubusercontent.com/open-mmlab/mmdeploy/v1.3.1/mmdeploy/codebase/mmpose/deploy/pose_detection.py'}
def get(k,u):
 rec={'file':k,'url':u}
 try:
  with urllib.request.urlopen(u,timeout=40) as f:b=f.read(2*1024*1024+1)
  assert len(b)<=2*1024*1024
  (R/k).write_bytes(b);rec.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:rec['error']=str(e)
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as p:out=list(p.map(lambda kv:get(*kv),urls.items()))
(R/'sources_manifest.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
