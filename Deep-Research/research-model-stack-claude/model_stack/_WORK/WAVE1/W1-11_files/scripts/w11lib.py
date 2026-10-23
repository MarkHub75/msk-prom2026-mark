"""W1-11 helper library (our own code; local_observation tooling). CPU only."""
import numpy as np, cv2, torch, onnxruntime as ort, os, json
from ultralytics import ASSETS
from ultralytics.data.augment import LetterBox
from ultralytics.utils import nms as unms, ops as uops

SCR = os.environ["W11_SCRATCH"]
ONNX = lambda v, n: f"{SCR}/onnx-W1-10/{v}/{n}.onnx"
WT = lambda n: f"{SCR}/weights-W1-10/{n}.pt"


def imgs():
    return {"bus": cv2.imread(str(ASSETS / "bus.jpg")), "zidane": cv2.imread(str(ASSETS / "zidane.jpg"))}


_sess = {}


def sess(p):
    if p not in _sess:
        so = ort.SessionOptions()
        so.intra_op_num_threads = 4
        _sess[p] = ort.InferenceSession(p, so, providers=["CPUExecutionProvider"])
    return _sess[p]


def run(p, x):
    s = sess(p)
    return s.run(None, {s.get_inputs()[0].name: x})


# ---------------- preprocessing variants ----------------
def to_tensor_rgb01(img_bgr_padded):
    rgb = img_bgr_padded[..., ::-1]
    return np.ascontiguousarray(rgb.transpose(2, 0, 1)[None].astype(np.float32) / 255.0)


def pre_ultra_square(img, size=640):
    """Ultralytics LetterBox(auto=False): centered, pad 114, round(); the contract used for static ONNX in predictor."""
    lb = LetterBox((size, size), auto=False, stride=32)
    out = lb(image=img)
    return to_tensor_rgb01(out), dict(kind="ultra_sq")


def pre_ultra_rect(img, size=640, stride=32):
    lb = LetterBox((size, size), auto=True, stride=stride)
    out = lb(image=img)
    return to_tensor_rgb01(out), dict(kind="ultra_rect")


def pre_ort_example(img, size=640):
    """Port of examples/YOLOv8-ONNXRuntime/main.py::letterbox (+BGR2RGB, /255.0 in float64 then float32)."""
    shape = img.shape[:2]
    r = min(size / shape[0], size / shape[1])
    new_unpad = round(shape[1] * r), round(shape[0] * r)
    dw, dh = (size - new_unpad[0]) / 2, (size - new_unpad[1]) / 2
    im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if shape[::-1] != new_unpad:
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = round(dh - 0.1), round(dh + 0.1)
    left, right = round(dw - 0.1), round(dw + 0.1)
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
    data = np.array(im) / 255.0
    data = np.transpose(data, (2, 0, 1))[None].astype(np.float32)
    return data, dict(pad=(top, left))


def pre_cpp_example(img, size=640):
    """Port of examples/cpp/common/yolo_postprocess.hpp::Preprocess: top-left, zero (black) padding, resize default INTER_LINEAR."""
    h, w = img.shape[:2]
    scale = np.float32(min(size / np.float32(w), size / np.float32(h)))
    nw, nh = int(round(float(w * scale))), int(round(float(h * scale)))
    res = cv2.resize(img, (nw, nh))
    out = np.zeros((size, size, 3), np.uint8)
    out[:nh, :nw] = res
    return to_tensor_rgb01(out), dict(scale=float(scale))


def pre_cvdnn_py_example(img, size=640):
    """Port of examples/YOLOv8-OpenCV-ONNX-Python/main.py: square canvas padded bottom/right with zeros, then blobFromImage(1/255, size, swapRB)."""
    h, w = img.shape[:2]
    length = max(h, w)
    canvas = np.zeros((length, length, 3), np.uint8)
    canvas[:h, :w] = img
    blob = cv2.dnn.blobFromImage(canvas, scalefactor=1 / 255, size=(size, size), swapRB=True)
    return blob.astype(np.float32), dict(scale=length / size)


def pre_yolox(img, size=640, bgr=True, div255=False, legacy_norm=False):
    """YOLOX data_augment.preproc: top-left, pad 114, int() truncation, BGR, 0..255 float32 (no /255 in current code)."""
    pad = np.ones((size, size, 3), np.uint8) * 114
    r = min(size / img.shape[0], size / img.shape[1])
    res = cv2.resize(img, (int(img.shape[1] * r), int(img.shape[0] * r)), interpolation=cv2.INTER_LINEAR).astype(np.uint8)
    pad[: int(img.shape[0] * r), : int(img.shape[1] * r)] = res
    x = pad.transpose(2, 0, 1).astype(np.float32)
    if not bgr:
        x = x[::-1]
    if div255 or legacy_norm:
        x = x / 255.0
    if legacy_norm:
        x = (x - np.array([0.485, 0.456, 0.406], np.float32).reshape(3, 1, 1)) / np.array([0.229, 0.224, 0.225], np.float32).reshape(3, 1, 1)
    return np.ascontiguousarray(x[None], dtype=np.float32), r


# ---------------- postprocessing ----------------
def ultra_post(out, input_shape_hw, orig_shape, conf=0.25, iou=0.7, agnostic=False, multi_label=False, max_det=300, classes=None):
    """Ultralytics non_max_suppression + scale_boxes on a (1,4+nc,A) numpy output. Returns (n,6) xyxy,conf,cls in original pixels."""
    t = torch.from_numpy(np.array(out)).float()
    r = unms.non_max_suppression(t, conf, iou, classes, agnostic, multi_label, max_det)[0]
    r = r.clone()
    if len(r):
        r[:, :4] = uops.scale_boxes(input_shape_hw, r[:, :4], orig_shape)
    return r.numpy()


def ort_example_post(out, orig_shape, size, pad, conf=0.5, iou=0.5):
    """Port of examples/YOLOv8-ONNXRuntime/main.py::postprocess (without drawing). Returns xyxy float (int-truncated), conf, cls."""
    outputs = np.transpose(np.squeeze(np.array(out[0]).copy()))
    gain = min(size / orig_shape[0], size / orig_shape[1])
    outputs[:, 0] -= pad[1]
    outputs[:, 1] -= pad[0]
    boxes, scores, cids = [], [], []
    for i in range(outputs.shape[0]):
        cs = outputs[i][4:]
        ms = np.amax(cs)
        if ms >= conf:
            cid = np.argmax(cs)
            x, y, w, h = outputs[i][:4]
            boxes.append([int((x - w / 2) / gain), int((y - h / 2) / gain), int(w / gain), int(h / gain)])
            scores.append(float(ms))
            cids.append(int(cid))
    if not boxes:
        return np.zeros((0, 6), np.float32)
    idx = cv2.dnn.NMSBoxes(boxes, scores, conf, iou)
    res = []
    for i in np.array(idx).flatten():
        b = boxes[int(i)]
        res.append([b[0], b[1], b[0] + b[2], b[1] + b[3], scores[int(i)], cids[int(i)]])
    return np.array(res, np.float32).reshape(-1, 6)


def cvdnn_py_post(out, scale, conf=0.25, iou=0.45):
    """Port of examples/YOLOv8-OpenCV-ONNX-Python/main.py post (score thr 0.25, NMSBoxes(.., 0.25, 0.45, 0.5), agnostic)."""
    o = np.array([cv2.transpose(np.array(out[0])[0])])
    boxes, scores, cids = [], [], []
    for i in range(o.shape[1]):
        cs = o[0][i][4:]
        (_a, ms, _b, (_x, mi)) = cv2.minMaxLoc(cs)
        if ms >= conf:
            boxes.append([o[0][i][0] - 0.5 * o[0][i][2], o[0][i][1] - 0.5 * o[0][i][3], o[0][i][2], o[0][i][3]])
            scores.append(float(ms))
            cids.append(int(mi))
    if not boxes:
        return np.zeros((0, 6), np.float32)
    idx = np.array(cv2.dnn.NMSBoxes(boxes, scores, conf, iou, 0.5)).flatten()
    res = []
    for i in idx:
        b = boxes[int(i)]
        res.append([b[0] * scale, b[1] * scale, (b[0] + b[2]) * scale, (b[1] + b[3]) * scale, scores[int(i)], cids[int(i)]])
    return np.array(res, np.float32).reshape(-1, 6)


def cpp_post(out, scale, conf=0.25, iou=0.45):
    """Port of examples/cpp/common/yolo_postprocess.hpp::PostprocessDetect grid branch (top-left, NMSBoxesBatched, int trunc)."""
    d = np.array(out[0])[0]  # (4+nc, A)
    inv = 1.0 / scale
    cls = d[4:]
    best = cls.argmax(0)
    bs = cls.max(0)
    keep = bs >= conf
    cx, cy, w, h = d[0][keep], d[1][keep], d[2][keep], d[3][keep]
    boxes = [[int((a - 0.5 * c) * inv), int((b - 0.5 * e) * inv), int(c * inv), int(e * inv)] for a, b, c, e in zip(cx, cy, w, h)]
    sc = bs[keep].astype(float).tolist()
    ci = best[keep].astype(int).tolist()
    if not boxes:
        return np.zeros((0, 6), np.float32)
    k = cv2.dnn.NMSBoxesBatched(boxes, sc, ci, conf, iou)
    res = [[boxes[i][0], boxes[i][1], boxes[i][0] + boxes[i][2], boxes[i][1] + boxes[i][3], sc[i], ci[i]] for i in np.array(k).flatten()]
    return np.array(res, np.float32).reshape(-1, 6)


# ---------------- matching ----------------
def iou_mat(a, b):
    a = np.asarray(a, np.float64).reshape(-1, 4)
    b = np.asarray(b, np.float64).reshape(-1, 4)
    if len(a) == 0 or len(b) == 0:
        return np.zeros((len(a), len(b)))
    x1 = np.maximum(a[:, None, 0], b[None, :, 0])
    y1 = np.maximum(a[:, None, 1], b[None, :, 1])
    x2 = np.minimum(a[:, None, 2], b[None, :, 2])
    y2 = np.minimum(a[:, None, 3], b[None, :, 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    aa = (a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1])
    ab = (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])
    return inter / (aa[:, None] + ab[None, :] - inter + 1e-12)


def match(ref, hyp, iou_thr=0.5, class_aware=True):
    """Greedy by ref confidence. Returns dict with counts, mean/min IoU, max |dconf|, max box-corner deviation (px)."""
    ref = np.asarray(ref).reshape(-1, 6)
    hyp = np.asarray(hyp).reshape(-1, 6)
    M = iou_mat(ref[:, :4], hyp[:, :4])
    if class_aware and len(ref) and len(hyp):
        M = M * (ref[:, 5][:, None] == hyp[:, 5][None, :])
    used = set()
    pairs = []
    for i in (np.argsort(-ref[:, 4]) if len(ref) else []):
        if len(hyp) == 0:
            break
        row = M[i].copy()
        for k in used:
            row[k] = -1
        j = int(np.argmax(row))
        if row[j] < iou_thr:
            continue
        used.add(j)
        pairs.append((int(i), j))
    mi = [M[i, j] for i, j in pairs]
    dconf = [abs(float(ref[i, 4]) - float(hyp[j, 4])) for i, j in pairs]
    dbox = [float(np.abs(ref[i, :4] - hyp[j, :4]).max()) for i, j in pairs]
    return dict(n_ref=len(ref), n_hyp=len(hyp), matched=len(pairs), ref_only=len(ref) - len(pairs), hyp_only=len(hyp) - len(pairs),
                mean_iou=round(float(np.mean(mi)), 4) if mi else None, min_iou=round(float(np.min(mi)), 4) if mi else None,
                max_dconf=round(max(dconf), 4) if dconf else None, max_dbox_px=round(max(dbox), 2) if dbox else None)
