import io, logging, torch, torch.nn as nn
from ultralytics.nn.tasks import DetectionModel
from ultralytics.nn.modules import Conv
from ultralytics.utils import LOGGER
LOGGER.setLevel(logging.INFO)
def load_log(tgt, src):
    buf = io.StringIO(); h = logging.StreamHandler(buf); LOGGER.addHandler(h)
    tgt.load(src); LOGGER.removeHandler(h)
    return [l for l in buf.getvalue().splitlines() if "Transferred" in l or "Remapped" in l]
names4 = {0:"person",1:"helmet",2:"head",3:"vest"}
src = DetectionModel("yolo11n.yaml", nc=80, verbose=False); src.names = {i:f"c{i}" for i in range(80)}; src.eval()
# (a) C2PSA -> Identity at same index
t = DetectionModel("yolo11_noC2PSA_identity.yaml", nc=4, verbose=False); t.names = names4
print("a) C2PSA->Identity (indices kept):", load_log(t, src), "| params", sum(p.numel() for p in t.parameters()), "vs", sum(p.numel() for p in DetectionModel("yolo11n.yaml", nc=4, verbose=False).parameters()))
# (b) ReLU instead of SiLU: no new params; keys identical
Conv.default_act = nn.ReLU()
t = DetectionModel("yolo11n.yaml", nc=4, verbose=False); t.names = names4
print("b) SiLU->ReLU (Conv.default_act):", load_log(t, src), "| act in model.0:", type(t.model[0].act).__name__)
