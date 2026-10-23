from pathlib import Path
import requests,json,datetime
p=Path('research_link_platform/_WORK/W2_C')
urls={
'ULTRA_V830_TAG_OBJECT.json':'https://api.github.com/repos/ultralytics/ultralytics/git/tags/a46b49a27a97d44c642882a405c8b57979e6d368',
'ULTRA_V83200_EXPORTER.py':'https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.200/ultralytics/engine/exporter.py',
'ONNX_V1160_MATH.cc':'https://raw.githubusercontent.com/onnx/onnx/v1.16.0/onnx/defs/math/defs.cc',
'ULTRA_V830_YOLO11.yaml':'https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/cfg/models/11/yolo11.yaml',
'ULTRA_V830_YOLOV8.yaml':'https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/cfg/models/v8/yolov8.yaml',
'YOLO5_V70_TAG.json':'https://api.github.com/repos/ultralytics/yolov5/git/ref/tags/v7.0',
}
rows=[]
for f,u in urls.items():
 r=requests.get(u,timeout=30);(p/f).write_bytes(r.content);rows.append(dict(file=f,url=u,status=r.status_code,time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),bytes=len(r.content)));print(f,r.status_code,len(r.content))
(p/'HTTP_LOG_2.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
