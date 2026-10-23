"""Standard-library shape/score counterexamples; no SDK, model or NMS execution."""
import ast,pathlib,json,types
p=pathlib.Path(__file__).parent
src=(p.parent/'W1_06/linq-cv-bench/scr/detection/run_yolov8_tpu.py').read_text(encoding='utf8')
tree=ast.parse(src); f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='normalize_prediction_shape')
class Shape:
 def __init__(self,shape): self.shape=shape; self.ndim=len(shape)
 def transpose(self,*axes): return Shape(tuple(self.shape[i] for i in axes))
ns={'np':types.SimpleNamespace(ndarray=Shape)}
exec(compile(ast.Module(body=[f],type_ignores=[]),'pinned_normalizer','exec'),ns)
results=[]
for s in [(1,5,8400),(1,6,8400),(1,7,8400),(1,84,8400),(1,85,8400),(1,84,84),(1,6,84)]:
 try: result=list(ns['normalize_prediction_shape'](Shape(s)).shape)
 except RuntimeError as e: result=str(e)
 results.append({'input_shape':s,'actual_pinned_normalizer':result})
results.append({'old_head_nc2':[100,100,20,20,.1,.9,.2], 'correct_old_v5_score':.1*.9, 'v8_nc_inferred':3,'v8_class_scores_if_transposed_accepted':[.1,.9,.2], 'wrong_v8_selected_class':1,'wrong_v8_score':.9,'correct_old_v5_class':0})
results.append({'old_COCO85_with_nc80':'v8 consumes objectness as class0, classes0..78 shift to1..79, class79 becomes one extra channel; no objectness multiplication'})
(p/'SCHEMA_PROBE_RESULT.json').write_text(json.dumps(results,indent=2),encoding='utf8')
print(json.dumps(results,indent=2))
