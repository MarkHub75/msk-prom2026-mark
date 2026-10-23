from pathlib import Path
import types, copy, json
import numpy as np
src=Path(__file__).with_name('cocoeval.py').read_text()
# Deliberate compatibility/import adapters: no compiled mask extension tested.
src=src.replace('from . import mask as maskUtils','maskUtils = None').replace('dtype=np.float','dtype=float')
m=types.ModuleType('inspected_cocoeval'); exec(compile(src,'cocoeval.py','exec'),m.__dict__)
def run(name,gts,dts,ious):
 e=m.COCOeval(iouType='bbox'); p=e.params; p.imgIds=[1];p.catIds=[1];p.iouThrs=np.array([.5]);p.areaRng=[[0,1e10]];p.areaRngLbl=['all'];p.maxDets=[100]
 e._gts[1,1]=gts;e._dts[1,1]=dts;e.ious[1,1]=np.array(ious).reshape(len(dts),len(gts))
 r=e.evaluateImg(1,1,p.areaRng[0],100);e.evalImgs=[r];e._paramsEval=copy.deepcopy(p);e.accumulate()
 valid=e.eval['precision'];valid=valid[valid>-1]
 return {'name':name,'matches':r['dtMatches'].tolist() if r else None,'ignored':r['dtIgnore'].tolist() if r else None,'recall':e.eval['recall'].tolist(),'AP50':float(valid.mean()) if len(valid) else None}
def gt(i=1,crowd=0):return {'id':i,'ignore':crowd,'iscrowd':crowd,'area':100}
def dt(i,s):return {'id':i,'score':s,'area':100}
results=[run('duplicate_after_TP',[gt()],[dt(1,.9),dt(2,.8)],[[1],[1]]),run('FP_before_TP',[gt()],[dt(1,.9),dt(2,.8)],[[0],[1]]),run('absent_class',[],[dt(1,.9)],[[]]),run('GT_no_detections',[gt()],[],[]),run('crowd_multiple_ignored',[gt(crowd=1)],[dt(1,.9),dt(2,.8)],[[1],[1]])]
print(json.dumps({'numpy':np.__version__,'tests':results},indent=2))
