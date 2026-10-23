"""Read-only primary source retrieval; no ML packages or model execution."""
import urllib.request, pathlib, hashlib, json, datetime
ROOT = pathlib.Path(__file__).resolve().parent
U='389b87f8cb9dbf2f31be8b70a94a3e47e11693db'
M='5408bc76f5b848cf925a0d1857899011d8c5b497'
D='bc75c9d6c8940aa03d0e1e5b5962bd930478ba77'
FILES={
 'u_model.yaml':('ultralytics/ultralytics',U,'ultralytics/cfg/models/rt-detr/rtdetr-l.yaml'),
 'u_transformer.py':('ultralytics/ultralytics',U,'ultralytics/nn/modules/transformer.py'),
 'u_ops.py':('ultralytics/ultralytics',U,'ultralytics/nn/modules/utils.py'),
 'u_exporter.py':('ultralytics/ultralytics',U,'ultralytics/engine/exporter.py'),
 'u_predict.py':('ultralytics/ultralytics',U,'ultralytics/models/rtdetr/predict.py'),
 'u_head.py':('ultralytics/ultralytics',U,'ultralytics/nn/modules/head.py'),
 'u_pyproject.toml':('ultralytics/ultralytics',U,'pyproject.toml'),
 'm_model.py':('open-mmlab/mmpose',M,'configs/body_2d_keypoint/rtmpose/coco/rtmpose-m_8xb256-420e_coco-256x192.py'),
 'm_head.py':('open-mmlab/mmpose',M,'mmpose/models/heads/coord_cls_heads/rtmcc_head.py'),
 'm_gau.py':('open-mmlab/mmpose',M,'mmpose/models/utils/rtmcc_block.py'),
 'm_codec.py':('open-mmlab/mmpose',M,'mmpose/codecs/simcc_label.py'),
 'm_affine.py':('open-mmlab/mmpose',M,'mmpose/datasets/transforms/topdown_transforms.py'),
 'm_estimator.py':('open-mmlab/mmpose',M,'mmpose/models/pose_estimators/topdown.py'),
 'd_config.py':('open-mmlab/mmdeploy',D,'configs/mmpose/pose-detection_simcc_onnxruntime_dynamic.py'),
 'd_static.py':('open-mmlab/mmdeploy',D,'configs/mmpose/pose-detection_simcc_onnxruntime_static.py'),
 'd_base.py':('open-mmlab/mmdeploy',D,'configs/mmpose/pose-detection_simcc_static.py'),
 'd_rewrite.py':('open-mmlab/mmdeploy',D,'mmdeploy/codebase/mmpose/models/heads/rtmcc_head.py'),
 'd_pose.py':('open-mmlab/mmdeploy',D,'mmdeploy/codebase/mmpose/models/pose_estimators/topdown.py'),
 'd_backend.py':('open-mmlab/mmdeploy',D,'mmdeploy/codebase/mmpose/deploy/pose_detection_model.py'),
 'd_docs.md':('open-mmlab/mmdeploy',D,'docs/en/04-supported-codebases/mmpose.md'),
 'd_test.yml':('open-mmlab/mmdeploy',D,'tests/regression/mmpose.yml'),
}
records=[]
for name,(repo,sha,path) in FILES.items():
 url=f'https://raw.githubusercontent.com/{repo}/{sha}/{path}'
 rec=dict(file=name,url=url,repo=repo,commit=sha,path=path,access_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(url,timeout=30) as r: data=r.read(); rec['status']=r.status
  (ROOT/name).write_bytes(data)
  rec.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
 except Exception as e: rec['error']=str(e)
 records.append(rec)
 print(name, rec.get('status',rec.get('error')))
(ROOT/'sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
