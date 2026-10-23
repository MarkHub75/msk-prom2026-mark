"""Export torchvision ssdlite320_mobilenet_v3_large with RANDOM weights (no download) to see graph structure. Usage: ssdlite_export.py OUT_DIR"""
import sys, torch, torchvision, onnx, onnxruntime as ort, numpy as np
from collections import Counter
out = sys.argv[1]
m = torchvision.models.detection.ssdlite320_mobilenet_v3_large(weights=None, weights_backbone=None).eval()
x = torch.rand(1, 3, 320, 320)
for opset in (11, 17):
    f = f"{out}/ssdlite_full_op{opset}.onnx"
    try:
        torch.onnx.export(m, ([x[0]],), f, opset_version=opset, dynamo=False, input_names=["image"], output_names=["boxes", "scores", "labels"])
        mo = onnx.load(f); c = Counter(n.op_type for n in mo.graph.node)
        print(opset, "export ok", len(mo.graph.node), "nodes; key ops:", {k: c[k] for k in ["NonMaxSuppression", "TopK", "Loop", "If", "NonZero", "Resize", "Gather", "Exp", "Softmax", "Sigmoid", "HardSigmoid", "HardSwish", "Clip"] if c[k]})
        s = ort.InferenceSession(f, providers=["CPUExecutionProvider"])
        y = s.run(None, {s.get_inputs()[0].name: x[0].numpy()})
        print("  ort ok:", [a.shape for a in y], "inputs:", [(i.name, i.shape) for i in s.get_inputs()])
    except Exception as e:
        print(opset, "FAIL", repr(e)[:400])
# head-only graph (backbone+head, no anchors/postprocess)
class Core(torch.nn.Module):
    def __init__(s, m): super().__init__(); s.m = m
    def forward(s, x):
        feats = list(s.m.backbone(x).values()); h = s.m.head(feats)
        return h["bbox_regression"], h["cls_logits"]
f = f"{out}/ssdlite_core_op13.onnx"
torch.onnx.export(Core(m), x, f, opset_version=13, dynamo=False, input_names=["images"], output_names=["bbox_regression", "cls_logits"])
mo = onnx.load(f); print("core:", dict(Counter(n.op_type for n in mo.graph.node)), [(o.name, [d.dim_value for d in o.type.tensor_type.shape.dim]) for o in mo.graph.output])
print("torch", torch.__version__, "torchvision", torchvision.__version__)
