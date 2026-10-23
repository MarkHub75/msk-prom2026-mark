import io, logging
from copy import deepcopy
import torch
from ultralytics.nn.tasks import DetectionModel
from ultralytics.utils import LOGGER
import ultralytics
LOGGER.setLevel(logging.INFO)
def load_log(tgt, src):
    buf = io.StringIO(); h = logging.StreamHandler(buf); LOGGER.addHandler(h)
    tgt.load(src); LOGGER.removeHandler(h)
    return [l for l in buf.getvalue().splitlines() if "Transferred" in l or "Remapped" in l]
def mk(cfg, nc, names):
    m = DetectionModel(cfg, nc=nc, verbose=False); m.names = names; return m
coco = {i: n for i, n in enumerate(ultralytics.utils.YAML.load(str(__import__("pathlib").Path(ultralytics.__file__).parent / "cfg/datasets/coco.yaml"))["names"].values())}
cfg = "yolo11n.yaml"
src = mk(cfg, 80, coco).eval()
# A: target names with no overlap with COCO
t = mk(cfg, 4, {0:"hardhat",1:"no_hardhat",2:"vest",3:"no_vest"}); print("A no-overlap:", load_log(t, src))
# B: single class person
t = mk(cfg, 1, {0:"person"}); print("B nc=1 person:", load_log(t, src))
# C: placeholder names on target (user dataset names missing/numeric)
t = mk(cfg, 4, {i:str(i) for i in range(4)}); print("C placeholder tgt names:", load_log(t, src))
# D: second-stage: own nc=4 model -> new dataset nc=6 with 2 overlapping names, different order
own = mk(cfg, 4, {0:"person",1:"helmet",2:"head",3:"vest"}).eval()
t = mk(cfg, 6, {0:"vest",1:"smoke",2:"person",3:"cigarette",4:"helmet",5:"fire"}); print("D nc4->nc6 3 overlaps:", load_log(t, own))
sd=t.state_dict(); o=own.state_dict()
k="model.23.cv3.0.2.weight"; print("  D row checks: tgt[0]==own[3](vest):", torch.equal(sd[k][0], o[k][3]), "tgt[2]==own[0](person):", torch.equal(sd[k][2], o[k][0]), "tgt[4]==own[1](helmet):", torch.equal(sd[k][4], o[k][1]))
# E: same nc, different order
t = mk(cfg, 4, {0:"vest",1:"person",2:"head",3:"helmet"}); print("E same nc, reordered:", load_log(t, own))
sd=t.state_dict(); k="model.23.cv3.0.2.weight"; print("  E: tgt[1]==own[0]:", torch.equal(sd[k][1], o[k][0]), "tgt[3]==own[1]:", torch.equal(sd[k][3], o[k][1]))
# F: cls_remap-off equivalent: names placeholders on source (e.g. YAML-built w/ no names) -> no remap
src2 = mk(cfg, 80, {i:str(i) for i in range(80)}).eval()
t = mk(cfg, 4, {0:"person",1:"helmet",2:"head",3:"vest"}); print("F source placeholder names:", load_log(t, src2))
# G: freeze semantics (name substring logic copied from trainer.py L382-L398)
m = mk(cfg, 4, {0:"person",1:"helmet",2:"head",3:"vest"})
for fz in (10, 11, [0,1,2], ["23.cv2"]):
    fl = fz if isinstance(fz, list) else list(range(fz))
    names = [f"model.{x}." for x in fl] + [".dfl"]
    tot = sum(p.numel() for p in m.parameters()); fr = sum(p.numel() for k,p in m.named_parameters() if any(x in k for x in names))
    print(f"G freeze={fz}: frozen params {fr}/{tot} ({100*fr/tot:.1f}%)")
print("n layers:", len(m.model), "last layer type:", type(m.model[-1]).__name__, "layer10:", type(m.model[10]).__name__, "layer9:", type(m.model[9]).__name__)
