"""Run yolov5 v7.0 export.py with torch.onnx.export forced to dynamo=False (torch>=2.9 defaults to dynamo=True,
which v7.0 does not expect). Same idea as ultralytics.utils.patches.onnx_export_patch. Usage: run_v5_export_legacy.py YOLOV5_ROOT -- export args"""
import sys, runpy, torch
root = sys.argv[1]; args = sys.argv[3:]
_f = torch.onnx.export
def _legacy(*a, **k):
    k.setdefault("dynamo", False)
    return _f(*a, **k)
torch.onnx.export = _legacy
sys.path.insert(0, root)
sys.argv = [root + "/export.py"] + args
runpy.run_path(root + "/export.py", run_name="__main__")
