"""X7: torchvision SSDLite320 pre/post contract check on a randomly initialised model (weights=None; no checkpoint deserialised). local_observation."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, torch, torch.nn.functional as F, torchvision
import w11lib as L
from torchvision.models.detection import ssdlite320_mobilenet_v3_large

torch.manual_seed(0)
m = ssdlite320_mobilenet_v3_large(weights=None, weights_backbone=None, num_classes=91).eval()
img = L.imgs()["bus"][:, :, ::-1].copy()  # RGB uint8 HxWx3
t = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0
with torch.no_grad():
    il, _ = m.transform([t])
manual = F.interpolate(t[None], size=(320, 320), mode="bilinear", align_corners=False)[0]
manual = (manual - 0.5) / 0.5
with torch.no_grad():
    f = m.backbone(il.tensors)
    f = list(f.values()) if not isinstance(f, torch.Tensor) else [f]
    ho = m.head(f)
HO = {k: list(v.shape) for k, v in ho.items()}
res = dict(
    repr_transform=repr(m.transform),
    defaults=dict(score_thresh=m.score_thresh, nms_thresh=m.nms_thresh, detections_per_img=m.detections_per_img, topk_candidates=m.topk_candidates,
                  image_mean=m.transform.image_mean, image_std=m.transform.image_std, size_divisible=m.transform.size_divisible, fixed_size=m.transform.fixed_size),
    transform_out_shape=list(il.tensors.shape), image_sizes=il.image_sizes,
    transform_vs_manual_maxabs=float((il.tensors[0] - manual).abs().max()),
    transform_range=[float(il.tensors.min()), float(il.tensors.max())],
    box_coder_weights=list(m.box_coder.weights),
    head_out_shapes=HO,
)
json.dump(res, open(sys.argv[1], "w"), indent=1)
print(json.dumps(res, indent=1))
