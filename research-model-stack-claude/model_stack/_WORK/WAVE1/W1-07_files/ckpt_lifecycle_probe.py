# Synthetic checkpoint (own random-init model, NOT a downloaded file) shaped exactly like BaseTrainer.save_model() output (trainer.py L800-L825, tag v8.4.184)
import torch, io, sys
from copy import deepcopy
from pathlib import Path
from ultralytics.nn.tasks import DetectionModel, load_checkpoint
from ultralytics.utils.torch_utils import strip_optimizer, convert_optimizer_state_dict_to_fp16
from ultralytics.cfg import get_cfg
from ultralytics import __version__
out = Path(sys.argv[1])
m = DetectionModel("yolo11n.yaml", nc=4, verbose=False); m.names = {0:"person",1:"helmet",2:"head",3:"vest"}
args = get_cfg(overrides={"data":"x.yaml","epochs":3}); m.args = args
opt = torch.optim.SGD(m.parameters(), lr=0.01, momentum=0.9); 
for p in m.parameters(): p.grad = torch.zeros_like(p)
opt.step()
ema = deepcopy(m).half()
ck = {"epoch":1,"best_fitness":0.1,"stopper":{"best_fitness":0.1,"best_epoch":2},"model":None,"ema":ema,"updates":100,"modelopt":None,
      "optimizer":convert_optimizer_state_dict_to_fp16(deepcopy(opt.state_dict())),"scaler":{},"train_args":vars(args),"train_metrics":{"fitness":0.1},
      "train_results":{},"date":"d","version":__version__,"git":{},"license":"AGPL-3.0","docs":"x"}
torch.save(ck, out/"last_unstripped.pt")
def desc(p):
    x = torch.load(p, map_location="cpu", weights_only=False)
    ema_ = x.get("ema"); mod = x.get("model")
    return {"keys": sorted(x.keys()), "model_is_None": mod is None, "ema_is_None": ema_ is None, "epoch": x["epoch"],
            "weights_dtype": str(next((mod if mod is not None else ema_).parameters()).dtype), "optimizer_is_None": x.get("optimizer") is None,
            "requires_grad_any": any(p.requires_grad for p in (mod if mod is not None else ema_).parameters()), "n_train_args": len(x["train_args"]),
            "size_MB": round(p.stat().st_size/1e6,2)}
print("BEFORE strip:", desc(out/"last_unstripped.pt"))
import shutil; shutil.copy(out/"last_unstripped.pt", out/"best_stripped.pt")
strip_optimizer(out/"best_stripped.pt")
print("AFTER  strip:", desc(out/"best_stripped.pt"))
model, ckpt = load_checkpoint(out/"best_stripped.pt")
print("load_checkpoint ->", type(model).__name__, next(model.parameters()).dtype, "names:", model.names, "stride:", model.stride.tolist())
model2, ckpt2 = load_checkpoint(out/"last_unstripped.pt"); print("load_checkpoint(unstripped) -> dtype", next(model2.parameters()).dtype, "names:", model2.names)
