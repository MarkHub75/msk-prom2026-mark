"""Print nodes of the detect head (names containing given prefix) with shapes and small constants. Usage: head_trace.py model.onnx prefix"""
import sys, onnx
from onnx import numpy_helper, shape_inference
m = shape_inference.infer_shapes(onnx.load(sys.argv[1])); g = m.graph; pre = sys.argv[2]
vi = {v.name: [d.dim_param or d.dim_value for d in v.type.tensor_type.shape.dim] for v in list(g.value_info)+list(g.output)+list(g.input)}
init = {i.name: numpy_helper.to_array(i) for i in g.initializer}
for n in g.node:
    if n.op_type == "Constant":
        for a in n.attribute:
            if a.name == "value": init[n.output[0]] = numpy_helper.to_array(a.t)
for n in g.node:
    if pre not in n.name or n.op_type in ("Conv",) and "cv" in n.name: continue
    if n.op_type == "Constant": continue
    ins = []
    for i in n.input:
        if i in init:
            v = init[i]; ins.append(f"C{list(v.shape)}" + (str(v.flatten().tolist()) if v.size <= 6 else f"[{v.min():.3g}..{v.max():.3g}]"))
        else: ins.append(f"{i.split('/')[-1]}{vi.get(i,'?')}")
    at = {a.name: onnx.helper.get_attribute_value(a) for a in n.attribute}
    print(n.op_type, n.name.replace(pre, ""), at if at else "", "<-", ", ".join(ins), "->", [vi.get(o, "?") for o in n.output])
