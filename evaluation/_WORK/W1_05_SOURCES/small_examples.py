"""Small deterministic examples, not full benchmark execution."""
import ast, math, json, runpy
from pathlib import Path
p=Path(__file__).parent
root=ast.parse((p/'sed_eval_sound_event.py').read_text(encoding='utf-8'))
cls=next(n for n in root.body if isinstance(n,ast.ClassDef) and n.name=='EventBasedMetrics')
funcs=[n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name in ['validate_onset','validate_offset']]
for n in funcs: n.decorator_list=[]
ns={'math':math}; exec(compile(ast.Module(body=funcs,type_ignores=[]),'<extracted sed_eval validators>','exec'),ns)
match=runpy.run_path(str(p/'sed_eval_event_matching.py'))['bipartite_match']
def event(a,b): return {'onset':a,'offset':b}
def tiou(a,b):
 i=max(0,min(a[1],b[1])-max(a[0],b[0])); return i/(a[1]-a[0]+b[1]-b[0]-i)
rows=[]
for name,g,d in [('late long',(10,110),(15,110)),('brief correct onset',(10,20),(10,11)),('split first',(10,20),(10,15)),('split second',(10,20),(15,20)),('merged versus first',(10,14),(10,20))]:
 rows.append(dict(case=name,tiou=tiou(g,d),onset=ns['validate_onset'](event(*g),event(*d),0.2),offset=ns['validate_offset'](event(*g),event(*d),0.2,0.2)))
g=[event(10,11),event(10.3,11.3)]; d=[event(10.15,11.15),event(9.85,10.85)]
graph={i:[j for j,r in enumerate(g) if ns['validate_onset'](r,x,0.2)] for i,x in enumerate(d)}
result={'cases':rows,'collar_ambiguity':{'graph':graph,'optimal_match':match(graph)},'scope':'Extracted pinned sed_eval validator functions and matching function executed; full evaluators not executed. tIoU is own scalar implementation.'}
print(json.dumps(result,indent=2)); (p/'small_examples_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
