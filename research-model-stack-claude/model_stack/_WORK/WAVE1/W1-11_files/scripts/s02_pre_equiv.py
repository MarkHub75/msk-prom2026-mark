"""X1: preprocessing equivalence. Compare tensors from Ultralytics predictor.preprocess vs manual ports. local_observation."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, torch
import w11lib as L
from ultralytics import YOLO
import ultralytics, onnxruntime, cv2

OUT = sys.argv[1]
res = {"versions": dict(ultralytics=ultralytics.__version__, torch=torch.__version__, ort=onnxruntime.__version__, cv2=cv2.__version__, numpy=np.__version__)}
I = L.imgs()
onnx_p = L.ONNX("yolov8n_default", "yolov8n")
m_onnx = YOLO(onnx_p, task="detect")
m_pt = YOLO(L.WT("yolov8n"))
res["images"] = {k: list(v.shape) for k, v in I.items()}
rows = []
for name, img in I.items():
    # Ultralytics predictor tensors
    m_onnx.predict(img, verbose=False)
    t_on = m_onnx.predictor.preprocess([img]).numpy()
    m_pt.predict(img, verbose=False)  # Model.predict sets rect=True
    t_pt = m_pt.predictor.preprocess([img]).numpy()
    m_pt.predict(img, verbose=False, rect=False)
    t_pt_sq = m_pt.predictor.preprocess([img]).numpy()
    sq, _ = L.pre_ultra_square(img)
    rect, _ = L.pre_ultra_rect(img)
    ort_ex, _ = L.pre_ort_example(img)
    cpp, _ = L.pre_cpp_example(img)
    cvd, _ = L.pre_cvdnn_py_example(img)
    r = {
        "image": name, "orig_hw": list(img.shape[:2]),
        "predictor_onnx_shape": list(t_on.shape), "predictor_pt_default_shape": list(t_pt.shape), "predictor_pt_rect_false_shape": list(t_pt_sq.shape),
        "args_rect_onnx": bool(m_onnx.predictor.args.rect), "args_rect_pt": True,
        "onnx_predictor_vs_manual_square_maxabs": float(np.abs(t_on - sq).max()),
        "pt_rect_false_vs_manual_square_maxabs": float(np.abs(t_pt_sq - sq).max()),
        "pt_default_vs_manual_rect_maxabs": float(np.abs(t_pt - rect).max()) if t_pt.shape == rect.shape else "shape-mismatch %s vs %s" % (t_pt.shape, rect.shape),
        "ort_example_vs_ultra_square_maxabs": float(np.abs(ort_ex - sq).max()),
        "ort_example_vs_ultra_square_frac_px_diff": float((np.abs(ort_ex - sq) > 1e-6).mean()),
        "cpp_example_vs_ultra_square_frac_px_diff": float((np.abs(cpp - sq) > 1e-6).mean()),
        "cpp_example_vs_ultra_square_maxabs": float(np.abs(cpp - sq).max()),
        "cvdnn_py_example_vs_ultra_square_frac_px_diff": float((np.abs(cvd - sq) > 1e-6).mean()),
        "cvdnn_py_example_vs_ultra_square_maxabs": float(np.abs(cvd - sq).max()),
        "pad_value_ultra_sq_corner": float(sq[0, 0, 0, 0]),  # 114/255
        "pad_value_cpp_corner_bottomright": float(cpp[0, 0, -1, -1]),
    }
    rows.append(r)
res["rows"] = rows
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(res, indent=1))
