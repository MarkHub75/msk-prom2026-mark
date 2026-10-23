"""X2: detection-level comparison of pre/post pipelines against the Ultralytics predictor reference. local_observation."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, torch
import w11lib as L
from ultralytics import YOLO

OUT = sys.argv[1]
I = L.imgs()
models = [("yolov8n", "yolov8n_default"), ("yolo11n", "yolo11n_default"), ("yolo26n", "yolo26n_default")]
res = []


def ult(m, img, **kw):
    r = m.predict(img, verbose=False, **kw)[0]
    return r.boxes.data.cpu().numpy()


for mname, var in models:
    onnx_p = L.ONNX(var, mname)
    m_on = YOLO(onnx_p, task="detect")
    m_pt = YOLO(L.WT(mname))
    for iname, img in I.items():
        h, w = img.shape[:2]
        for conf, iou in [(0.25, 0.7), (0.25, 0.45), (0.05, 0.7)]:
            ref = ult(m_on, img, conf=conf, iou=iou)
            row = dict(model=mname, image=iname, conf=conf, iou=iou, n_ref=len(ref))
            # manual path: square letterbox + ORT + Ultralytics NMS/scale_boxes
            x, _ = L.pre_ultra_square(img)
            out = L.run(onnx_p, x)
            man = L.ultra_post(out[0], (640, 640), img.shape, conf=conf, iou=iou)
            row["manual_ultra_pipeline_vs_predictor"] = L.match(ref, man)
            row["manual_maxabs_boxes"] = float(np.abs(man - ref).max()) if len(man) == len(ref) and len(ref) else None
            # PT default (rect=True via Model.predict) and PT rect=False vs ONNX reference
            pt_def = ult(m_pt, img, conf=conf, iou=iou)
            pt_sq = ult(m_pt, img, conf=conf, iou=iou, rect=False)
            row["pt_default_rect_vs_onnx"] = L.match(ref, pt_def)
            row["pt_rect_false_vs_onnx"] = L.match(ref, pt_sq)
            # example-style pipelines (class-aware match against ref)
            x2, meta = L.pre_ort_example(img)
            o2 = L.run(onnx_p, x2)
            row["ort_example_flow_vs_ref"] = L.match(ref, L.ort_example_post(o2, img.shape[:2], 640, meta["pad"], conf=conf, iou=iou))
            x3, meta3 = L.pre_cpp_example(img)
            o3 = L.run(onnx_p, x3)
            row["cpp_example_flow_vs_ref"] = L.match(ref, L.cpp_post(o3, meta3["scale"], conf=conf, iou=iou))
            x4, meta4 = L.pre_cvdnn_py_example(img)
            o4 = L.run(onnx_p, x4)
            row["cvdnn_py_example_flow_vs_ref"] = L.match(ref, L.cvdnn_py_post(o4, meta4["scale"], conf=conf, iou=iou))
            # isolation: ultralytics NMS on example's preprocess (separates preprocessing effect from NMS/decode effect)
            row["cpp_pre_only_(ultra_post_topleft_not_possible)"] = None
            # NMS-only isolation: same tensor (square letterbox), ultralytics decode vs example decode (agnostic, int truncation)
            row["ort_example_post_on_ultra_tensor_vs_ref"] = L.match(ref, L.ort_example_post(out, img.shape[:2], 640, (round((640 - round(h * min(640 / h, 640 / w))) / 2 - 0.1), round((640 - round(w * min(640 / h, 640 / w))) / 2 - 0.1)), conf=conf, iou=iou))
            # agnostic variant of ultralytics postprocess
            row["ultra_agnostic_vs_ref"] = L.match(ref, L.ultra_post(out[0], (640, 640), img.shape, conf=conf, iou=iou, agnostic=True))
            res.append(row)
json.dump(res, open(OUT, "w"), indent=1)


def short(d):
    return "None" if d is None else f"{d['matched']}/{d['n_ref']}ref,{d['hyp_only']}extra,minIoU={d['min_iou']},dconf={d['max_dconf']},dbox={d['max_dbox_px']}"


for r in res:
    print(r["model"], r["image"], "conf", r["conf"], "iou", r["iou"], "n_ref", r["n_ref"])
    for k in ["manual_ultra_pipeline_vs_predictor", "pt_default_rect_vs_onnx", "pt_rect_false_vs_onnx", "ort_example_flow_vs_ref", "ort_example_post_on_ultra_tensor_vs_ref", "cpp_example_flow_vs_ref", "cvdnn_py_example_flow_vs_ref", "ultra_agnostic_vs_ref"]:
        print("   ", k, short(r[k]))
