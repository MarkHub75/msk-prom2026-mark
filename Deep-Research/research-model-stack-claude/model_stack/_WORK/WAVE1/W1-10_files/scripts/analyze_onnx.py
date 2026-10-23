"""Inventory an ONNX file: opset/IR, IO, op counts, metadata, key node attributes. Usage: analyze_onnx.py model.onnx out.json"""
import sys, json, os, hashlib
from collections import Counter
import onnx
from onnx import numpy_helper, shape_inference

path, out = sys.argv[1], sys.argv[2]
m = onnx.load(path)
g = m.graph
def shp(vi):
    t = vi.type.tensor_type
    return {"name": vi.name, "dtype": onnx.TensorProto.DataType.Name(t.elem_type),
            "shape": [d.dim_param if d.dim_param else d.dim_value for d in t.shape.dim]}
ops = Counter(n.op_type for n in g.node)
inits = {i.name: i for i in g.initializer}
consts = {}
for n in g.node:
    if n.op_type == "Constant":
        for a in n.attribute:
            if a.name == "value":
                consts[n.output[0]] = numpy_helper.to_array(a.t)
def val(name):
    if name in inits: return numpy_helper.to_array(inits[name])
    if name in consts: return consts[name]
    return None
def attrs(n):
    d = {}
    for a in n.attribute:
        v = onnx.helper.get_attribute_value(a)
        if isinstance(v, bytes): v = v.decode()
        if isinstance(v, onnx.TensorProto): v = f"tensor{list(v.dims)}"
        if isinstance(v, list): v = [x.decode() if isinstance(x, bytes) else x for x in v]
        d[a.name] = v
    return d
details = {}
for kind in ["Resize", "MaxPool", "Softmax", "TopK", "NonMaxSuppression", "Split", "Gather", "GatherElements", "Concat",
             "MatMul", "Transpose", "Reshape", "Slice", "Loop", "If", "ReduceMax", "ArgMax", "Mod", "Div", "Mul", "Add", "Sub", "Sigmoid", "Einsum"]:
    lst = []
    for n in g.node:
        if n.op_type != kind: continue
        e = {"name": n.name, "attrs": attrs(n)}
        cin = []
        for i in n.input:
            v = val(i)
            if v is not None:
                cin.append({"input": i, "shape": list(v.shape), "dtype": str(v.dtype),
                            "values": v.flatten()[:8].tolist() if v.size <= 8 else f"size={v.size} min={float(v.min()):.4g} max={float(v.max()):.4g}"})
        if cin: e["const_inputs"] = cin
        lst.append(e)
    if lst: details[kind] = lst[:12] + ([f"... {len(lst)-12} more"] if len(lst) > 12 else [])
# value shapes for last few nodes
try:
    inf = shape_inference.infer_shapes(m)
    vis = {v.name: shp(v) for v in list(inf.graph.value_info) + list(inf.graph.output)}
except Exception as ex:
    vis = {}
tail = []
for n in g.node[-25:]:
    tail.append({"op": n.op_type, "name": n.name, "in": list(n.input), "out": [vis.get(o, {"name": o}) for o in n.output]})
res = {
    "file": os.path.basename(path), "size_bytes": os.path.getsize(path),
    "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(),
    "ir_version": m.ir_version, "opset_import": {(o.domain or "ai.onnx"): o.version for o in m.opset_import},
    "producer": f"{m.producer_name} {m.producer_version}",
    "inputs": [shp(i) for i in g.input if i.name not in inits], "outputs": [shp(o) for o in g.output],
    "n_nodes": len(g.node), "n_initializers": len(g.initializer),
    "op_counts": dict(sorted(ops.items(), key=lambda x: -x[1])),
    "metadata_props": {p.key: p.value for p in m.metadata_props},
    "details": details, "tail_nodes": tail,
}
try:
    onnx.checker.check_model(m, full_check=True); res["checker"] = "ok"
except Exception as ex:
    res["checker"] = f"FAIL: {ex}"[:500]
json.dump(res, open(out, "w"), indent=1, default=str)
print(res["file"], res["size_bytes"], res["opset_import"], "IR", res["ir_version"], res["inputs"], res["outputs"], res["checker"])
print(" ops:", res["op_counts"])
