import urllib.request,pathlib,json,hashlib,datetime
root=pathlib.Path(__file__).resolve().parent
U='389b87f8cb9dbf2f31be8b70a94a3e47e11693db'; D='bc75c9d6c8940aa03d0e1e5b5962bd930478ba77'; T='ecac3a77becc63f23d9f6980b2a36f86acd00a8a'
files={
'u_exportutils.py':('ultralytics/ultralytics',U,'ultralytics/utils/export/__init__.py'),
'u_downloads.py':('ultralytics/ultralytics',U,'ultralytics/utils/downloads.py'),
'd_task.py':('open-mmlab/mmdeploy',D,'mmdeploy/codebase/mmpose/deploy/pose_detection.py'),
'd_simcc.py':('open-mmlab/mmdeploy',D,'mmdeploy/codebase/mmpose/models/heads/simcc_head.py'),
'd_posebase.py':('open-mmlab/mmdeploy',D,'mmdeploy/codebase/mmpose/models/pose_estimators/base.py'),
'd_simcc_trt.py':('open-mmlab/mmdeploy',D,'configs/mmpose/pose-detection_simcc_tensorrt_dynamic-256x192.py'),
'd_trt_int8.py':('open-mmlab/mmdeploy',D,'configs/mmpose/pose-detection_tensorrt-int8_static-256x192.py'),
't_backbone.py':('open-mmlab/mmdetection',T,'mmdet/models/backbones/cspnext.py'),
't_csp.py':('open-mmlab/mmdetection',T,'mmdet/models/layers/csp_layer.py'),
'd_scalenorm.py':('open-mmlab/mmdeploy',D,'mmdeploy/codebase/mmpose/models/utils/rtmcc_block.py'),
'd_deploy.py':('open-mmlab/mmdeploy',D,'tools/deploy.py'),
}
rec=[]
for name,(repo,sha,path) in files.items():
 url=f'https://raw.githubusercontent.com/{repo}/{sha}/{path}'; r=dict(file=name,url=url,commit=sha,path=path,access_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  data=urllib.request.urlopen(url,timeout=20).read(); root.joinpath(name).write_bytes(data);r.update(status=200,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
 except Exception as e:r['error']=str(e)
 rec.append(r);print(name,r.get('status',r.get('error')),flush=True)
root.joinpath('sources_final.json').write_text(json.dumps(rec,indent=2))
