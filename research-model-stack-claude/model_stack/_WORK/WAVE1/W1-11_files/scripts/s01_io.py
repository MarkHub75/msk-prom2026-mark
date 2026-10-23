import sys, glob, onnx, onnxruntime as ort, os
S = sys.argv[1]
paths = [S+"/weights-W1-11/yolox_nano/yolox_nano.onnx", S+"/weights-W1-11/yolox_s/yolox_s.onnx"] + sorted(glob.glob(S+"/onnx-W1-10/*/*.onnx"))
for p in paths:
    m = onnx.load(p)
    ops = [(i.domain or "ai.onnx", i.version) for i in m.opset_import]
    sess = ort.InferenceSession(p, providers=["CPUExecutionProvider"])
    ins = [(i.name, i.shape, i.type) for i in sess.get_inputs()]
    outs = [(o.name, o.shape, o.type) for o in sess.get_outputs()]
    md = {x.key: x.value for x in m.metadata_props}
    keys = {k: (v[:80]) for k, v in md.items() if k in ("task","stride","imgsz","batch","names","args","end2end","dynamic","channels")}
    print(os.path.relpath(p, S), "opset", ops, "\n   in", ins, "\n   out", outs, "\n   meta", {k:(v if k!='names' else v[:40]+'...') for k,v in keys.items()})
