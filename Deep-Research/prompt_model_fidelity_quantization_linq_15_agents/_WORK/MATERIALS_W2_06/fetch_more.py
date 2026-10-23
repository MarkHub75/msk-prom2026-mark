import runpy, pathlib, urllib.request, json, hashlib, datetime
root=pathlib.Path(__file__).resolve().parent
U='389b87f8cb9dbf2f31be8b70a94a3e47e11693db'; M='5408bc76f5b848cf925a0d1857899011d8c5b497'; D='bc75c9d6c8940aa03d0e1e5b5962bd930478ba77'
files={
'd_init.py':('open-mmlab/mmdeploy',D,'mmdeploy/codebase/mmpose/models/__init__.py'),
'd_heads_init.py':('open-mmlab/mmdeploy',D,'mmdeploy/codebase/mmpose/models/heads/__init__.py'),
'd_pose_init.py':('open-mmlab/mmdeploy',D,'mmdeploy/codebase/mmpose/models/pose_estimators/__init__.py'),
'd_pose_static.py':('open-mmlab/mmdeploy',D,'configs/mmpose/pose-detection_static.py'),
'd_basepose.py':('open-mmlab/mmdeploy',D,'configs/mmpose/pose-detection.py'),
'd_ort.py':('open-mmlab/mmdeploy',D,'configs/_base_/backends/onnxruntime.py'),
'd_baseonnx.py':('open-mmlab/mmdeploy',D,'configs/_base_/onnx_config.py'),
'd_requirements.txt':('open-mmlab/mmdeploy',D,'requirements/codebases.txt'),
'm_metafile.yml':('open-mmlab/mmpose',M,'configs/body_2d_keypoint/rtmpose/coco/rtmpose_coco.yml'),
'm_bbox.py':('open-mmlab/mmpose',M,'mmpose/datasets/transforms/common_transforms.py'),
'm_runtime.py':('open-mmlab/mmpose',M,'configs/_base_/default_runtime.py'),
'm_transformer.py':('open-mmlab/mmpose',M,'mmpose/models/utils/transformer.py'),
'u_torchutils.py':('ultralytics/ultralytics',U,'ultralytics/utils/torch_utils.py'),
'u_enginepredict.py':('ultralytics/ultralytics',U,'ultralytics/engine/predictor.py'),
}
records=[]
for name,(repo,sha,path) in files.items():
 url=f'https://raw.githubusercontent.com/{repo}/{sha}/{path}'
 r=dict(file=name,url=url,commit=sha,path=path,access_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  data=urllib.request.urlopen(url,timeout=20).read(); (root/name).write_bytes(data); r.update(status=200,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
 except Exception as e:r['error']=str(e)
 records.append(r); print(name,r.get('status',r.get('error')),flush=True)
(root/'sources_more.json').write_text(json.dumps(records,indent=2),encoding='utf8')
