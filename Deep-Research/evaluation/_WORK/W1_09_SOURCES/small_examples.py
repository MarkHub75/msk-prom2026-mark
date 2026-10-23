import sys, types, importlib.util, json, platform
from pathlib import Path
import numpy as np, scipy
root=Path(__file__).parent/'TrackEval'/'trackeval'
# Compatibility only: unmodified 2022 source uses removed NumPy scalar aliases.
np.float=float
np.int=int
for name,path in [('trackeval',root),('trackeval.metrics',root/'metrics')]:
 m=types.ModuleType(name);m.__path__=[str(path)];sys.modules[name]=m
for name,file in [('trackeval._timing','_timing.py'),('trackeval.utils','utils.py'),('trackeval.metrics._base_metric','metrics/_base_metric.py'),('trackeval.metrics.clear','metrics/clear.py'),('trackeval.metrics.hota','metrics/hota.py'),('trackeval.metrics.identity','metrics/identity.py')]:
 spec=importlib.util.spec_from_file_location(name,root/file);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
from trackeval.metrics.clear import CLEAR
from trackeval.metrics.hota import HOTA
from trackeval.metrics.identity import Identity

def data(ids,sim=None):
 gt=[np.array([0]) for _ in ids]; tr=[np.array(x,dtype=int) for x in ids]
 return dict(gt_ids=gt,tracker_ids=tr,num_gt_ids=1,num_tracker_ids=max([i for x in ids for i in x],default=-1)+1,num_gt_dets=len(ids),num_tracker_dets=sum(map(len,ids)),num_timesteps=len(ids),similarity_scores=[np.ones((1,len(x))) for x in ids] if sim is None else sim)
cases={'perfect':data([[0]]*10),'split_half':data([[0]]*5+[[1]]*5),'one_missing_global_empty':data([[0],[],[0]]),'one_missing_unmatched_box':data([[0],[1],[0]],[np.array([[1.]]),np.array([[0.]]),np.array([[1.]])])}
out={'environment':dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,compatibility='np.float=float; np.int=int; import modules without package __init__'), 'cases':{}}
for name,d in cases.items():
 c=CLEAR({'PRINT_CONFIG':False}).eval_sequence(d);h=HOTA().eval_sequence(d);i=Identity({'PRINT_CONFIG':False}).eval_sequence(d)
 out['cases'][name]={k:float(c[k]) for k in ['MOTA','IDSW','Frag','CLR_TP','CLR_FN','CLR_FP']};out['cases'][name].update(IDF1=float(i['IDF1']),HOTA=float(np.mean(h['HOTA'])),DetA=float(np.mean(h['DetA'])),AssA=float(np.mean(h['AssA'])))
print(json.dumps(out,indent=2))
Path(__file__).with_name('small_examples.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
