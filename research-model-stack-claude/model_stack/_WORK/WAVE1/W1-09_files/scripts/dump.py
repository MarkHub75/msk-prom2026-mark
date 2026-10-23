import onnx,collections,json,sys,hashlib
out={}
for f in ("run1/yolo26n.onnx","run1/yolo11n.onnx"):
    o=onnx.load(f); c=collections.Counter(n.op_type for n in o.graph.node)
    out[f]={"sha256":hashlib.sha256(open(f,"rb").read()).hexdigest(),"ir_version":o.ir_version,"opsets":[(x.domain,x.version) for x in o.opset_import],"op_counts":dict(c),"inputs":[(i.name,[d.dim_value or d.dim_param for d in i.type.tensor_type.shape.dim]) for i in o.graph.input],"outputs":[(i.name,[d.dim_value or d.dim_param for d in i.type.tensor_type.shape.dim]) for i in o.graph.output]}
json.dump(out,open(sys.argv[1],"w"),indent=1)
print(json.dumps(out,indent=0)[:1500])
