"""Read-only isolated probes of pinned example helpers; no SDK/model execution."""
import ast
import argparse
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1] / 'W1_06/linq-cv-bench'
ns = {'np': np}
tiny = ast.parse((ROOT / 'scr/detection/run_tiny_yolo3_accuracy.py').read_text(encoding='utf-8'))
helper = next(n for n in tiny.body if isinstance(n, ast.FunctionDef) and n.name == 'infer_desc_dtype')
module = ast.Module(body=[ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0), helper], type_ignores=[])
exec(compile(ast.fix_missing_locations(module), '<isolated pinned helper>', 'exec'), ns)
dtype_result = str(ns['infer_desc_dtype']({'dtype': 'uint8'}, np.dtype(np.float32)))
yolo = ast.parse((ROOT / 'scr/detection/run_yolov8_tpu.py').read_text(encoding='utf-8'))
attrs = sorted({n.attr for n in ast.walk(yolo) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == 'args' and 'output_tens' in n.attr})
arg_namespace = argparse.Namespace(output_tensor_name=None)
attr_checks = {a: hasattr(arg_namespace, a) for a in attrs}
# Exact integer geometry copied as formulas, without OpenCV image interpolation.
geometry = []
for h, w in [(1080,1920),(479,641),(641,479)]:
    size=640; r=min(size/h,size/w); nw,nh=round(w*r),round(h*r)
    dw,dh=size-nw,size-nh
    geometry.append({'hw':[h,w], 'r':r, 'resized_wh':[nw,nh], 'padding_lrtb':[dw//2,dw-dw//2,dh//2,dh-dh//2], 'actual_xy_scales':[nw/w,nh/h]})
print(json.dumps({'numpy_version':np.__version__, 'pinned_commit':'3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140','dtype_uint8_result':dtype_result,'args_attribute_checks':attr_checks,'geometry_formula_only':geometry,'hardware_inference_executed':False}, ensure_ascii=True, indent=2))
