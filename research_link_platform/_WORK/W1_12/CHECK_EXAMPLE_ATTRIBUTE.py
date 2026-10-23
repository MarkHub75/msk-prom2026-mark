import ast
from pathlib import Path
p=Path('research_link_platform/_WORK/W1_06/linq-cv-bench/scr/detection/run_yolov8_tpu.py')
t=ast.parse(p.read_text(encoding='utf-8'))
for n in ast.walk(t):
    if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='args' and n.attr.startswith('output_tens'):
        print('Attribute at line', n.lineno, repr(n.attr))
        from argparse import Namespace
        ns=Namespace(output_tensor_name=None)
        try: getattr(ns,n.attr)
        except AttributeError as e: print(type(e).__name__ + ': ' + str(e))
print('No third-party modules imported, no TPU access, full script NOT executed.')
