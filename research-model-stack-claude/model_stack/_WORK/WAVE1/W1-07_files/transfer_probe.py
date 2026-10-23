# W1-07 probe: weight transfer when nc changes. No training, no downloads; random-init source models built from yaml.
import sys, io, logging
from copy import deepcopy
import torch
from ultralytics.nn.tasks import DetectionModel
from ultralytics.utils import LOGGER, YAML
from ultralytics.utils.torch_utils import intersect_dicts
from ultralytics.cfg import get_cfg
import ultralytics
print("ultralytics", ultralytics.__version__, "torch", torch.__version__)
coco = YAML.load(str(__import__("pathlib").Path(ultralytics.__file__).parent / "cfg/datasets/coco.yaml"))["names"]
tgt_names = {0: "person", 1: "helmet", 2: "head", 3: "vest"}
def probe(cfg, label):
    src = DetectionModel(cfg, nc=80, verbose=False)
    src.names = dict(coco)
    src.eval()
    tgt = DetectionModel(cfg, nc=4, verbose=False)
    tgt.names = dict(tgt_names)
    n_total = len(tgt.state_dict())
    old = intersect_dicts(src.float().state_dict(), tgt.state_dict())   # what plain name+shape intersect would transfer
    tgt_before = deepcopy(tgt.state_dict())
    buf = io.StringIO(); h = logging.StreamHandler(buf); LOGGER.addHandler(h); LOGGER.setLevel(logging.INFO)
    tgt.load(src)   # actual code path of DetectionTrainer.get_model -> model.load(weights)
    LOGGER.removeHandler(h)
    log = [l for l in buf.getvalue().splitlines() if "Transferred" in l or "Remapped" in l]
    h0 = src.model[-1]; h1 = tgt.model[-1]
    # which keys changed vs random init, which equal source
    sd = tgt.state_dict(); ssd = src.state_dict()
    same = [k for k in sd if k in ssd and sd[k].shape == ssd[k].shape and torch.equal(sd[k].float(), ssd[k].float())]
    new = [k for k in sd if k not in same]
    print(f"\n== {label} cfg={cfg}")
    print(" state_dict tensors target:", n_total, "| plain intersect_dicts would transfer:", len(old))
    print(" log:", log)
    print(" head cv3[0] hidden width src/tgt:", h0.cv3[0][0][1].conv.out_channels if hasattr(h0.cv3[0][0],'__getitem__') else None,
          h1.cv3[0][0][1].conv.out_channels if hasattr(h1.cv3[0][0],'__getitem__') else None)
    print(" tensors NOT equal to source (new/random):", len(new))
    print(" first few:", new[:8], "...")
    print(" last-conv shapes src/tgt:", tuple(h0.cv3[0][-1].weight.shape), tuple(h1.cv3[0][-1].weight.shape))
    print(" tgt.names:", tgt.names)
for cfg, lab in [("yolo11n.yaml","yolo11n"),("yolo11s.yaml","yolo11s"),("yolo26n.yaml","yolo26n"),("yolov8n.yaml","yolov8n"),("yolov5nu.yaml","yolov5nu(yolov5.yaml)")]:
    try: probe(cfg, lab)
    except Exception as e: print("\n== ", lab, "FAILED", type(e).__name__, str(e)[:300])
