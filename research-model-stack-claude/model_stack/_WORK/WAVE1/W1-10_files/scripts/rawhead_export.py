"""OUR experimental 'no-decode' export (not an Ultralytics-documented mode): Detect returns per-level raw head maps.
Then decode on CPU in numpy and compare with Ultralytics default ONNX output on same input.
Usage: rawhead_export.py WEIGHT.pt OUT.onnx REF_DEFAULT.onnx OUT_JSON"""
import sys, json, types
import numpy as np, torch, onnxruntime as ort, cv2
from ultralytics import YOLO, ASSETS
from ultralytics.data.augment import LetterBox

wt, out, ref_onnx, out_json = sys.argv[1:5]
model = YOLO(wt).model.float().eval()
head = model.model[-1]
print("checkpoint head end2end:", getattr(head, "end2end", None))
if getattr(head, "one2one_cv2", None) is not None:
    head.end2end = False  # same choice as Exporter with default nms=None -> one-to-many head kept
model = model.fuse()
head = model.model[-1]
for p in model.parameters():
    p.requires_grad = False
from ultralytics.nn.modules.block import C2f
for m_ in model.modules():  # same as Exporter.__call__ for non-TF formats: chunk -> Split
    if isinstance(m_, C2f):
        m_.forward = m_.forward_split

def raw_forward(self, x):
    outs = []
    for i in range(self.nl):
        outs.append(self.cv2[i](x[i]))            # box: 4*reg_max channels (DFL logits) or 4 (reg_max=1)
    for i in range(self.nl):
        outs.append(self.cv3[i](x[i]).sigmoid())  # cls probs per level
    return tuple(outs)

head.forward = types.MethodType(raw_forward, head)
img = cv2.imread(str(ASSETS / "bus.jpg"))
x = LetterBox(new_shape=(640, 640), auto=False)(image=img)[..., ::-1].transpose(2, 0, 1)[None].astype(np.float32) / 255.0
x = np.ascontiguousarray(x)
names = [f"box_s{s}" for s in (8, 16, 32)] + [f"cls_s{s}" for s in (8, 16, 32)]
torch.onnx.export(model, torch.from_numpy(x), out, opset_version=13, input_names=["images"], output_names=names, dynamo=False)
s = ort.InferenceSession(out, providers=["CPUExecutionProvider"])
ys = s.run(None, {"images": x})
reg_max = head.reg_max
strides = [8, 16, 32]

def decode(ys):
    boxes, scores = [], []
    for i, st in enumerate(strides):
        b, c = ys[i][0], ys[3 + i][0]  # (4*reg_max,H,W), (nc,H,W)
        H, W = b.shape[1:]
        if reg_max > 1:
            b = b.reshape(4, reg_max, H, W)
            e = np.exp(b - b.max(1, keepdims=True)); e /= e.sum(1, keepdims=True)
            d = (e * np.arange(reg_max, dtype=np.float32)[None, :, None, None]).sum(1)  # (4,H,W) ltrb in grid units
        else:
            d = b
        gy, gx = np.meshgrid(np.arange(H) + 0.5, np.arange(W) + 0.5, indexing="ij")
        x1, y1, x2, y2 = gx - d[0], gy - d[1], gx + d[2], gy + d[3]
        xywh = np.stack([(x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1]) * st
        boxes.append(xywh.reshape(4, -1)); scores.append(c.reshape(c.shape[0], -1))
    return np.concatenate([np.concatenate(boxes, 1), np.concatenate(scores, 1)], 0)[None]

dec = decode(ys)
ref = ort.InferenceSession(ref_onnx, providers=["CPUExecutionProvider"]).run(None, {"images": x})[0]
import onnx
from collections import Counter
mo = onnx.load(out)
r = {"weights": wt, "reg_max": int(reg_max), "outputs": {n: list(y.shape) for n, y in zip(names, ys)},
     "box_raw_range": [float(min(y.min() for y in ys[:3])), float(max(y.max() for y in ys[:3]))],
     "cls_range": [float(min(y.min() for y in ys[3:])), float(max(y.max() for y in ys[3:]))],
     "op_counts": dict(Counter(n.op_type for n in mo.graph.node)),
     "cpu_decode_vs_default_onnx_maxabs_boxes": float(np.abs(dec[:, :4] - ref[:, :4]).max()),
     "cpu_decode_vs_default_onnx_maxabs_scores": float(np.abs(dec[:, 4:] - ref[:, 4:]).max())}
json.dump(r, open(out_json, "w"), indent=1)
print(json.dumps(r))
