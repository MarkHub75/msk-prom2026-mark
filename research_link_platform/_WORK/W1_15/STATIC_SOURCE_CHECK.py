"""Static/source-isolated checks only; no package import or TPU execution."""
import ast
import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[2]
source = root / '_WORK/W1_09/PYTPU_SOURCE/pytpu-15.0.24/pytpu/_bindings.py'
tree = ast.parse(source.read_text(encoding='utf-8'))
classes = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
methods = {k: [n.name for n in v.body if isinstance(n, ast.FunctionDef)] for k,v in classes.items()}
listing = next(n for n in classes['Device'].body if isinstance(n, ast.FunctionDef) and n.name == 'list_devices')
# Evaluate only the exact return expression with mocked directory entries.
names = ['tpu0','tpu9','tpu10','tpux','tpu.','tpu','nvidia0']
class MockOS:
    path = type('Path', (), {'join': staticmethod(lambda a,b: a+'/'+b)})
    listdir = staticmethod(lambda _: names)
expr = ast.Expression(body=listing.body[-1].value)
selected = eval(compile(ast.fix_missing_locations(expr), '<isolated list_devices return>', 'eval'),
                {'os': MockOS, 're': re})
repo = root / '_WORK/W1_06/linq-cv-bench/scr/detection/run_yolov8_tpu.py'
rtree = ast.parse(repo.read_text(encoding='utf-8'))
attrs = sorted({n.attr for n in ast.walk(rtree) if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='args'})
result = {'kind':'source-isolated local observation, no TPU/native library execution',
          'pytpu_version':'15.0.24','mock_directory_entries':names,'selected':selected,
          'device_methods':methods['Device'],'inference_methods':methods['Inference'],
          'has_stats_method':any('stats' in x for x in methods.values()),
          'suspicious_args_attributes':[x for x in attrs if not x.isascii()]}
path = pathlib.Path(__file__).with_name('STATIC_SOURCE_CHECK.json')
path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=True,indent=2))
