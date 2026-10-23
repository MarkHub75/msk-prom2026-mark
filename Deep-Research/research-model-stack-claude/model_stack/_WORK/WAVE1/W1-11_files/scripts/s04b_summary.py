import json, sys
d = json.load(open(sys.argv[1]))
out = ["### Raw-tensor parity, max over 8 inputs per model (bus/zidane x {orig, flip, bright1.4, crop16x9}; NB: zidane crop16x9 == zidane because zidane is already 16:9, so 6 distinct inputs)\n",
       "| model | comparison | box max abs, all 8400 anchors (px) | box max abs, anchors with ref cls prob>0.05 (px) | cls prob max abs | min cosine over 4 box channels | min cosine over class channels |",
       "|---|---|---|---|---|---|---|"]
for m in ["yolov8n", "yolo11n", "yolo26n"]:
    rows = [r for r in d["parity"] if r["model"] == m]
    for key, label in [("pt_vs_ort", "PT fused fp32 vs ORT fp32 (same tensor)"), ("pt_fp16cpu_vs_pt_fp32", "PT fp16 (CPU) vs PT fp32")]:
        ps = [r[key] for r in rows if isinstance(r[key], dict)]
        if not ps:
            out.append(f"| {m} | {label} | failed | | | | |"); continue
        out.append("| %s | %s | %.3g | %.3g | %.3g | %.8f | %.5f |" % (m, label, max(p["box_maxabs_px"] for p in ps), max(p["box_maxabs_on_pos_anchors_px"] for p in ps),
                                                                max(p["cls_maxabs"] for p in ps), min(p["cos_box_min"] for p in ps), min(p["cos_cls_min"] for p in ps)))
out.append("\n### Synthetic output-tensor fake quantization (NOT LinQ; calibrated on the same tensor = best case). cell: matched/n_ref, +extra, min IoU (conf=0.25 / iou=0.7)\n")
out.append("| model | image | scenario | max box err px | max cls err | conf=0.25 | conf=0.05 |")
out.append("|---|---|---|---|---|---|---|")
for r in d["fakequant"]:
    c, e = r["conf025"], r["conf005"]
    out.append("| %s | %s | %s | %.2f | %.4f | %d/%d +%d IoUmin=%s | %d/%d +%d |" % (r["model"], r["image"], r["scenario"], r["err_box_max_px"], r["err_cls_max"],
                                                                       c["matched"], c["n_ref"], c["hyp_only"], c["min_iou"], e["matched"], e["n_ref"], e["hyp_only"]))
print("\n".join(out))
