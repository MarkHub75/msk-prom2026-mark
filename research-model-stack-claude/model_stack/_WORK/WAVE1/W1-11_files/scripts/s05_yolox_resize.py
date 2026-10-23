"""X5/X6: YOLOX ONNX (release 0.1.1rc0 assets) preprocessing-contract test; resize-implementation divergence. local_observation."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, cv2, torch
import torch.nn.functional as F
import w11lib as L

OUT = sys.argv[1]
I = L.imgs()
res = {"yolox": [], "resize": []}


# ---- numpy ports of yolox/utils/demo_utils.py (read at YOLOX 6ddff48) ----
def demo_postprocess(outputs, img_size, p6=False):
    grids, strides_l = [], []
    strides = [8, 16, 32] if not p6 else [8, 16, 32, 64]
    for stride in strides:
        hs, ws = img_size[0] // stride, img_size[1] // stride
        xv, yv = np.meshgrid(np.arange(ws), np.arange(hs))
        grid = np.stack((xv, yv), 2).reshape(1, -1, 2)
        grids.append(grid)
        strides_l.append(np.full((*grid.shape[:2], 1), stride))
    grids = np.concatenate(grids, 1)
    es = np.concatenate(strides_l, 1)
    outputs = outputs.copy()
    outputs[..., :2] = (outputs[..., :2] + grids) * es
    outputs[..., 2:4] = np.exp(outputs[..., 2:4]) * es
    return outputs


def nms_np(boxes, scores, thr):
    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]]); yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]]); yy2 = np.minimum(y2[i], y2[order[1:]])
        w = np.maximum(0.0, xx2 - xx1 + 1); h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)
        order = order[np.where(ovr <= thr)[0] + 1]
    return keep


def multiclass_nms_agnostic(boxes, scores, nms_thr, score_thr):
    cls_inds = scores.argmax(1)
    cls_scores = scores[np.arange(len(cls_inds)), cls_inds]
    m = cls_scores > score_thr
    if m.sum() == 0:
        return np.zeros((0, 6))
    vs, vb, vc = cls_scores[m], boxes[m], cls_inds[m]
    keep = nms_np(vb, vs, nms_thr)
    return np.concatenate([vb[keep], vs[keep, None], vc[keep, None]], 1) if keep else np.zeros((0, 6))


def yolox_decode(raw, size, ratio, score_thr=0.1):
    p = demo_postprocess(raw, (size, size))[0]
    boxes = p[:, :4]
    scores = p[:, 4:5] * p[:, 5:]
    xyxy = np.ones_like(boxes)
    xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2; xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2
    xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2; xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2
    xyxy /= ratio
    return multiclass_nms_agnostic(xyxy, scores, 0.45, score_thr)


for mname, size in [("yolox_nano", 416), ("yolox_s", 640)]:
    p = f"{L.SCR}/weights-W1-11/{mname}/{mname}.onnx"
    for iname, img in I.items():
        base = None
        for vname, kw in [("BGR_0-255 (current preproc)", {}), ("RGB_0-255", dict(bgr=False)), ("BGR_/255", dict(div255=True)), ("legacy RGB_/255_meanstd", dict(bgr=False, legacy_norm=True))]:
            x, r = L.pre_yolox(img, size=size, **kw)
            raw = L.run(p, x)[0]
            dets = yolox_decode(raw, size, r, 0.1)
            d3 = dets[dets[:, 4] >= 0.3] if len(dets) else dets
            row = dict(model=mname, image=iname, variant=vname, n_ge_0p1=int(len(dets)), n_ge_0p3=int(len(d3)), top_conf=round(float(dets[:, 4].max()), 3) if len(dets) else None,
                       obj_max=round(float(raw[0][:, 4].max()), 3), cls_max=round(float(raw[0][:, 5:].max()), 3), raw_wh_range=[round(float(raw[0][:, 2:4].min()), 2), round(float(raw[0][:, 2:4].max()), 2)])
            if base is None:
                base = dets
            else:
                row["vs_current"] = L.match(base[:, [0, 1, 2, 3, 4, 5]], dets)
            res["yolox"].append(row)

# ---- resize implementation divergence: bus.jpg and zidane long side -> 640 and -> 320 ----
for iname, img in I.items():
    h, w = img.shape[:2]
    for tgt in (640, 320):
        r = tgt / max(h, w)
        nw, nh = int(round(w * r)), int(round(h * r))
        ref = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)
        outs = {"cv2.INTER_AREA": cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA),
                "cv2.INTER_LINEAR_EXACT": cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR_EXACT),
                "cv2.INTER_NEAREST": cv2.resize(img, (nw, nh), interpolation=cv2.INTER_NEAREST)}
        t = torch.from_numpy(img).permute(2, 0, 1)[None].float()
        for nm, kw in [("torch bilinear align_corners=False", dict(mode="bilinear", align_corners=False)), ("torch bilinear antialias=True", dict(mode="bilinear", align_corners=False, antialias=True))]:
            o = F.interpolate(t, size=(nh, nw), **kw)[0].permute(1, 2, 0).round().clamp(0, 255).byte().numpy()
            outs[nm] = o
        for nm, o in outs.items():
            dd = np.abs(o.astype(np.int16) - ref.astype(np.int16))
            res["resize"].append(dict(image=iname, target_long_side=tgt, impl=nm, vs="cv2.INTER_LINEAR", max_abs_u8=int(dd.max()), mean_abs_u8=round(float(dd.mean()), 3), frac_px_diff_gt1=round(float((dd > 1).mean()), 4)))
        # detection-level effect for 640 with yolov8n default ONNX
        if tgt == 640:
            onnx_p = L.ONNX("yolov8n_default", "yolov8n")
            x_ref, _ = L.pre_ultra_square(img)
            o_ref = L.run(onnx_p, x_ref)
            ref_det = L.ultra_post(o_ref[0], (640, 640), img.shape, 0.25, 0.7)
            for nm, o in outs.items():
                dw, dh = 640 - nw, 640 - nh
                top, bottom, left, right = round(dh / 2 - 0.1), round(dh / 2 + 0.1), round(dw / 2 - 0.1), round(dw / 2 + 0.1)
                pad = cv2.copyMakeBorder(o, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
                xx = L.to_tensor_rgb01(pad)
                oo = L.run(onnx_p, xx)
                det = L.ultra_post(oo[0], (640, 640), img.shape, 0.25, 0.7)
                res["resize"][-len(outs) + list(outs).index(nm)]["yolov8n_det_vs_ref_conf0.25"] = L.match(ref_det, det)
json.dump(res, open(OUT, "w"), indent=1)
for r in res["yolox"]:
    print(r["model"], r["image"], r["variant"], "n>=.1:", r["n_ge_0p1"], "n>=.3:", r["n_ge_0p3"], "top", r["top_conf"], "obj_max", r["obj_max"], "cls_max", r["cls_max"], "wh_raw", r["raw_wh_range"])
for r in res["resize"]:
    m = r.get("yolov8n_det_vs_ref_conf0.25")
    print(r["image"], r["target_long_side"], r["impl"], "max", r["max_abs_u8"], "mean", r["mean_abs_u8"], "frac>1", r["frac_px_diff_gt1"], ("det %s/%s +%s IoUmin=%s dconf=%s" % (m["matched"], m["n_ref"], m["hyp_only"], m["min_iou"], m["max_dconf"])) if m else "")
