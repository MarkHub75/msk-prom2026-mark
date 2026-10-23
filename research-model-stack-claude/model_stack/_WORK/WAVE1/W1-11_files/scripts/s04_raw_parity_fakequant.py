"""X3: raw-tensor parity PT(fused,fp32) vs ORT(fp32) vs PT(fp16 CPU) on identical input tensors.
X4: synthetic output-tensor fake quantization (NOT LinQ) to illustrate how output tensor layout affects detections. local_observation."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, torch, cv2
import w11lib as L
from ultralytics import YOLO

OUT = sys.argv[1]
I = L.imgs()
models = [("yolov8n", "yolov8n_default"), ("yolo11n", "yolo11n_default"), ("yolo26n", "yolo26n_default")]
res = {"parity": [], "fakequant": []}


def variants():
    for n, im in I.items():
        yield n, im
        yield n + "_flip", im[:, ::-1].copy()
        yield n + "_bright1.4", np.clip(im.astype(np.float32) * 1.4, 0, 255).astype(np.uint8)
        yield n + "_crop16x9", im[: int(im.shape[1] * 9 / 16) if im.shape[0] > im.shape[1] * 9 / 16 else im.shape[0], :].copy()


def group_stats(a, b, nc):
    """a=ref, b=test, shape (4+nc, A)."""
    d = np.abs(a - b)
    box, cls = d[:4], d[4:]
    pos = a[4:].max(0) > 0.05  # anchors with a plausible detection
    cos_cls = []
    for c in range(nc):
        x, y = a[4 + c].astype(np.float64), b[4 + c].astype(np.float64)
        nx, ny = np.linalg.norm(x), np.linalg.norm(y)
        if nx > 1e-9 and ny > 1e-9:
            cos_cls.append(float(x @ y / (nx * ny)))
    cos_box = [float(a[k].astype(np.float64) @ b[k].astype(np.float64) / (np.linalg.norm(a[k]) * np.linalg.norm(b[k]))) for k in range(4)]
    r = dict(
        box_maxabs_px=float(box.max()), box_meanabs_px=float(box.mean()),
        box_maxabs_on_pos_anchors_px=float(box[:, pos].max()) if pos.any() else None,
        cls_maxabs=float(cls.max()), cls_meanabs=float(cls.mean()),
        cls_maxabs_on_pos=float(d[4:, pos].max()) if pos.any() else None,
        cls_max_rel_where_ref_gt_0p05=float((cls[a[4:] > 0.05] / a[4:][a[4:] > 0.05]).max()) if (a[4:] > 0.05).any() else None,
        n_pos_anchors=int(pos.sum()), cos_box_min=min(cos_box), cos_cls_min=min(cos_cls) if cos_cls else None, n_cls_channels_cos=len(cos_cls),
    )
    return r


for mname, var in models:
    onnx_p = L.ONNX(var, mname)
    m = YOLO(L.WT(mname))
    m.predict(I["bus"], verbose=False)  # builds predictor/AutoBackend (fused fp32)
    ab = m.predictor.model
    for vname, img in variants():
        x, _ = L.pre_ultra_square(img)
        o_ort = L.run(onnx_p, x)[0][0]
        with torch.inference_mode():
            y = ab(torch.from_numpy(x))
        y = y[0] if isinstance(y, (list, tuple)) else y
        o_pt = y.numpy()[0]
        row = dict(model=mname, variant=vname, input_hw=list(x.shape[2:]), pt_vs_ort=group_stats(o_pt, o_ort, 80))
        # fp16 on CPU (torch): may be unsupported / slow; record outcome
        try:
            mh = YOLO(L.WT(mname)).model.fuse().half().eval()
            with torch.inference_mode():
                yh = mh(torch.from_numpy(x).half())
            yh = yh[0] if isinstance(yh, (list, tuple)) else yh
            row["pt_fp16cpu_vs_pt_fp32"] = group_stats(o_pt, yh.float().numpy()[0], 80)
        except Exception as e:
            row["pt_fp16cpu_vs_pt_fp32"] = "failed: %s" % repr(e)[:200]
        res["parity"].append(row)

# X4: fake quantization of the final output tensor (single output [1,84,8400]) -- synthetic, calibrated on the same tensor (best case)
def fq(a, lo, hi, qmin, qmax):
    scale = (hi - lo) / (qmax - qmin)
    zp = qmin - lo / scale
    q = np.clip(np.round(a / scale + zp), qmin, qmax)
    return ((q - zp) * scale).astype(np.float32), scale


for mname, var in models:
    onnx_p = L.ONNX(var, mname)
    for iname in ["bus", "zidane"]:
        img = I[iname]
        x, _ = L.pre_ultra_square(img)
        o = L.run(onnx_p, x)[0]  # (1,84,8400)
        ref = L.ultra_post(o, (640, 640), img.shape, conf=0.25, iou=0.7)
        ref05 = L.ultra_post(o, (640, 640), img.shape, conf=0.05, iou=0.7)
        a = o[0]
        scen = {}
        # S1: one tensor, int8 symmetric, scale from max|value| (~box pixels)
        s1, sc1 = fq(a, -np.abs(a).max(), np.abs(a).max(), -127, 127)
        scen["S1_single_tensor_int8_symmetric(scale=%.3f)" % sc1] = s1
        # S2: one tensor, uint8 asymmetric over [min,max]
        s2, sc2 = fq(a, a.min(), a.max(), 0, 255)
        scen["S2_single_tensor_uint8_asym(scale=%.3f)" % sc2] = s2
        # S3: split tensors: boxes int8 symmetric (own range), class probs uint8 over [0,1]
        b3, scb = fq(a[:4], -np.abs(a[:4]).max(), np.abs(a[:4]).max(), -127, 127)
        c3, scc = fq(a[4:], 0.0, 1.0, 0, 255)
        scen["S3_split_box_int8(scale=%.3f)_cls_uint8(scale=%.4f)" % (scb, scc)] = np.concatenate([b3, c3], 0)
        # S4: boxes normalised by 640 and stored with probs in one tensor, uint8 over [0,1]
        n4 = a.copy(); n4[:4] /= 640.0
        q4, sc4 = fq(n4, 0.0, 1.0, 0, 255)
        q4[:4] *= 640.0
        scen["S4_single_tensor_boxes_div640_uint8(scale=%.4f)" % sc4] = q4
        # S5: split, boxes uint8 over [0,640], class probs uint8 over [0,1]
        b5, scb5 = fq(a[:4], 0.0, 640.0, 0, 255)
        scen["S5_split_box_uint8_0to640(scale=%.3f)_cls_uint8" % scb5] = np.concatenate([b5, c3], 0)
        for sname, arr in scen.items():
            det = L.ultra_post(arr[None], (640, 640), img.shape, conf=0.25, iou=0.7)
            det05 = L.ultra_post(arr[None], (640, 640), img.shape, conf=0.05, iou=0.7)
            res["fakequant"].append(dict(model=mname, image=iname, scenario=sname,
                                          err_box_max_px=float(np.abs(arr[:4] - a[:4]).max()), err_cls_max=float(np.abs(arr[4:] - a[4:]).max()),
                                          conf025=L.match(ref, det), conf005=L.match(ref05, det05)))
json.dump(res, open(OUT, "w"), indent=1)

print("== parity (PT fused fp32 vs ORT fp32, identical tensor)")
for r in res["parity"]:
    p = r["pt_vs_ort"]
    print(r["model"], r["variant"], "box_max=%.2e box_pos=%s cls_max=%.2e cls_pos=%s cos_box_min=%.8f cos_cls_min=%s" % (
        p["box_maxabs_px"], "%.2e" % p["box_maxabs_on_pos_anchors_px"] if p["box_maxabs_on_pos_anchors_px"] is not None else None, p["cls_maxabs"],
        "%.2e" % p["cls_maxabs_on_pos"] if p["cls_maxabs_on_pos"] is not None else None, p["cos_box_min"], p["cos_cls_min"]))
    h = r["pt_fp16cpu_vs_pt_fp32"]
    if isinstance(h, dict):
        print("     fp16cpu: box_max=%.3f box_pos=%s cls_max=%.4f cls_pos=%s cos_cls_min=%s" % (h["box_maxabs_px"], h["box_maxabs_on_pos_anchors_px"], h["cls_maxabs"], h["cls_maxabs_on_pos"], h["cos_cls_min"]))
    else:
        print("     fp16cpu:", h)
print("== fakequant")
for r in res["fakequant"]:
    c = r["conf025"]; d = r["conf005"]
    print(r["model"], r["image"], r["scenario"], "errbox=%.2f errcls=%.4f | conf.25: %s/%s +%s IoUmin=%s dconf=%s | conf.05: %s/%s +%s" % (
        r["err_box_max_px"], r["err_cls_max"], c["matched"], c["n_ref"], c["hyp_only"], c["min_iou"], c["max_dconf"], d["matched"], d["n_ref"], d["hyp_only"]))
