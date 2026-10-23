import json, sys
rows = json.load(open(sys.argv[1]))
keys = [("pt_default_rect_vs_onnx", "PT predict (rect=True default) vs ONNX predict"),
        ("pt_rect_false_vs_onnx", "PT predict rect=False vs ONNX predict"),
        ("ort_example_flow_vs_ref", "examples/YOLOv8-ONNXRuntime flow"),
        ("cpp_example_flow_vs_ref", "examples/cpp flow (top-left, zero pad, batched NMS)"),
        ("cvdnn_py_example_flow_vs_ref", "examples/YOLOv8-OpenCV-ONNX-Python flow")]
def s(d):
    if d is None: return "-"
    return f"{d['matched']}/{d['n_ref']}, +{d['hyp_only']}, IoUmin {d['min_iou']}, dconf {d['max_dconf']}, dbox {d['max_dbox_px']}px"
out = []
for conf, iou in [(0.25, 0.45), (0.25, 0.7), (0.05, 0.7)]:
    out.append(f"\n### conf={conf}, iou={iou} (cell: matched/n_ref, +extra detections, min IoU of matched pairs, max |dconf|, max box-corner deviation)\n")
    out.append("| model | image | " + " | ".join(k[1] for k in keys) + " |")
    out.append("|---|---|" + "---|" * len(keys))
    for r in rows:
        if r["conf"] == conf and r["iou"] == iou:
            out.append(f"| {r['model']} | {r['image']} | " + " | ".join(s(r[k[0]]) for k in keys) + " |")
print("\n".join(out))
