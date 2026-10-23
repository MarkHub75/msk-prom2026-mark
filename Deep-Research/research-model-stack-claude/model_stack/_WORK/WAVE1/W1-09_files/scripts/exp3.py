import torch
from ultralytics import YOLO
for cfg in ("yolo26n.yaml","yolo11n.yaml"):
    m=YOLO(cfg)
    p=m.export(format="onnx",imgsz=640,simplify=True,device="cpu")
    print("EXPORTED",cfg,p)
    import onnx; o=onnx.load(p); print("ir",o.ir_version,[(x.domain,x.version) for x in o.opset_import],{k.key:k.value for k in o.metadata_props if k.key in("task","imgsz","end2end","names")})
    print(sorted({n.op_type for n in o.graph.node}))
