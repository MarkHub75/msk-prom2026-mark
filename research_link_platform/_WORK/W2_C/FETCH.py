from pathlib import Path
import requests,json,datetime,concurrent.futures,hashlib
P=Path('research_link_platform/_WORK/W2_C')
items={
'ULTRA_V830_EXPORTER.py':'https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/engine/exporter.py',
'ULTRA_V830_HEAD.py':'https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/nn/modules/head.py',
'ULTRA_V830_BLOCK.py':'https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/nn/modules/block.py',
'ULTRA_V830_TAL.py':'https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/utils/tal.py',
'ULTRA_V830_DEFAULT.yaml':'https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/cfg/default.yaml',
'ULTRA_V830_TAG.json':'https://api.github.com/repos/ultralytics/ultralytics/git/ref/tags/v8.3.0',
'YOLO5_V70_EXPORT.py':'https://raw.githubusercontent.com/ultralytics/yolov5/v7.0/export.py',
'YOLO5_V70_YOLO.py':'https://raw.githubusercontent.com/ultralytics/yolov5/v7.0/models/yolo.py',
'ONNX_V1160_DEFS.cc':'https://raw.githubusercontent.com/onnx/onnx/v1.16.0/onnx/defs/tensor/defs.cc',
'FRONTEND_PYPI.json':'https://pypi.org/pypi/onnx-direct/json',
'FRAMEWORK_PYPI.json':'https://pypi.org/pypi/tpu-framework/json',
'LINQ_SOL.html':'https://lin-q.ru/sol',
'LINQ_DOCS.html':'https://lin-q.ru/docs',
'GH_ONNX_DIRECT_REPOS.json':'https://api.github.com/search/repositories?q=onnx_direct',
'GH_TPU_FRAMEWORK_REPOS.json':'https://api.github.com/search/repositories?q=tpu_framework',
}
def fetch(k,u):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=requests.get(u,timeout=35); (P/k).write_bytes(r.content)
  return dict(file=k,url=u,time_utc=t,status=r.status_code,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
 except Exception as e:return dict(file=k,url=u,time_utc=t,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: rows=list(pool.map(lambda kv:fetch(*kv),items.items()))
(P/'HTTP_LOG.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
for r in rows: print(r['file'],r.get('status'),r.get('bytes'),r.get('error',''))
