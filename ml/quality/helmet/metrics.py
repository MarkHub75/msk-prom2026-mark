"""Explicit object metrics with partial-label abstention and sealed-test guard.

These are AP101 object metrics (maxDets=300 by default), not a claim of exact
COCO evaluator equivalence. No unlabeled region/class implies verified absence.
"""
import math
import numpy as np


def _box(value):
    if not isinstance(value,(list,tuple)) or len(value)!=4 or any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in value):
        raise ValueError("box requires four finite numbers")
    if value[2]<=value[0] or value[3]<=value[1]:raise ValueError("box must have positive area")
    return np.asarray(value,dtype=float)


def _overlap(a,b,ioa=False):
    a,b=_box(a),_box(b);inter=np.maximum(np.minimum(a[2:],b[2:])-np.maximum(a[:2],b[:2]),0).prod()
    area=np.prod(a[2:]-a[:2]);den=area if ioa else area+np.prod(b[2:]-b[:2])-inter
    return float(inter/max(den,1e-12))


def _match(image,predictions,class_name,threshold,score_floor,max_detections,partial=False):
    gt=[v for v in image.get('annotations',[]) if v['class_name']==class_name and not v.get('ignore',False)]
    ignores=[v for v in image.get('annotations',[]) if v['class_name']==class_name and v.get('ignore',False)]
    ignores += [v for v in image.get('ignore_regions',[]) if v.get('class_name') in (None,class_name)]
    preds=[v for v in predictions if v['class_name']==class_name and v['score']>=score_floor]
    preds=sorted(enumerate(preds),key=lambda item:(-item[1]['score'],item[0]))[:max_detections]
    used=set();out=[];ignored=0
    for _,p in preds:
        matches=[(_overlap(p['bbox_xyxy'],g['bbox_xyxy']),i) for i,g in enumerate(gt) if i not in used]
        best=max(matches,default=(-1,-1),key=lambda v:(v[0],-v[1]))
        if best[0]>=threshold:
            used.add(best[1]);out.append((float(p['score']),1,0))
        elif any(_overlap(p['bbox_xyxy'],g['bbox_xyxy'],ioa=True)>=.5 for g in ignores):ignored+=1
        elif partial:ignored+=1
        else:out.append((float(p['score']),0,1))
    return out,len(gt),ignored,len(used)


def _ap(records,total):
    if total==0:return None
    ordered=sorted(enumerate(records),key=lambda item:(-item[1][0],item[0]))
    if not ordered:return 0.
    tp=np.cumsum([v[1][1] for v in ordered]);fp=np.cumsum([v[1][2] for v in ordered])
    recall=tp/total;precision=tp/np.maximum(tp+fp,1)
    return float(np.mean([max(precision[recall>=r],default=0.) for r in np.linspace(0,1,101)]))


def evaluate_dataset(dataset,predictions,classes=('helmet','bare_head'),confidence=.25,match_iou=.5,ap_score_floor=.001,max_detections=300,allow_test=False):
    """Score explicit full-GT images; partial known positives get recall only.

    Predictions map image_id -> [{class_name,bbox_xyxy,score}]. Missing image keys
    are errors: missed objects must be represented by an explicit empty list.
    """
    if not (0<=ap_score_floor<=confidence<=1 and 0<match_iou<=1) or type(max_detections) is not int or max_detections<1:
        raise ValueError('invalid operating point')
    images=dataset.get('images',[])
    if not images or len({v['image_id'] for v in images})!=len(images):raise ValueError('dataset needs unique nonempty images')
    if any(v.get('split')=='test' for v in images) and not allow_test:raise ValueError('sealed test evaluation requires explicit allow_test=True')
    if set(predictions)!={v['image_id'] for v in images}:raise ValueError('predictions must explicitly cover every image, no extras')
    groups={}
    for image in images:
        if not isinstance(image.get('group_id'),str) or not image['group_id']:raise ValueError('group_id required')
        group=image['group_id'];split=image.get('split')
        if group in groups and groups[group]!=split:raise ValueError('source group crosses splits')
        groups[group]=split
        for v in image.get('annotations',[]):_box(v['bbox_xyxy'])
        for v in image.get('ignore_regions',[]):_box(v['bbox_xyxy'])
        for p in predictions[image['image_id']]:
            _box(p['bbox_xyxy'])
            if isinstance(p.get('score'),bool) or not isinstance(p.get('score'),(int,float)) or not math.isfinite(p['score']) or not 0<=p['score']<=1:raise ValueError('invalid prediction score')
    result={'schema_version':'helmet-object-metrics-v1','status':'MEASURED','scope':'object boxes only, not wearer/event correctness',
            'protocol':{'confidence':confidence,'match_iou':match_iou,'ap_score_floor':ap_score_floor,'max_detections_per_image_class':max_detections,
                        'ap_interpolation':'101 recall points, class-aware greedy descending-score IoU',
                        'ignore_matching':'unmatched prediction IOA>=0.5 after ordinary GT matching',
                        'partial_labels':'known-positive recall only; no precision/AP contribution'},
            'images':len(images),'source_groups':len(groups),'classes':{}}
    for cls in classes:
        complete=[];partial=[];unknown=0
        for image in images:
            coverage=image.get('class_coverage',{}).get(cls,'unknown')
            if coverage not in ('complete','partial','unknown'):raise ValueError('invalid class coverage')
            if coverage=='complete':complete.append(image)
            elif coverage=='partial':partial.append(image)
            else:unknown+=1
        operating=[];total=ignored=0
        for image in complete:
            records,n,ig,_=_match(image,predictions[image['image_id']],cls,match_iou,confidence,max_detections)
            operating+=records;total+=n;ignored+=ig
        tp=sum(v[1] for v in operating);fp=sum(v[2] for v in operating);fn=total-tp
        precision=tp/(tp+fp) if tp+fp else None;recall=tp/total if total else None
        f1=(2*tp/(2*tp+fp+fn)) if 2*tp+fp+fn else None
        aps={}
        for threshold in [round(.5+.05*i,2) for i in range(10)]:
            records=[];gt=0
            for image in complete:
                values,n,_,_=_match(image,predictions[image['image_id']],cls,threshold,ap_score_floor,max_detections);records+=values;gt+=n
            aps[f'{threshold:.2f}']=_ap(records,gt)
        known_gt=known_tp=0
        for image in partial:
            _,n,_,matched=_match(image,predictions[image['image_id']],cls,match_iou,confidence,max_detections,partial=True)
            known_gt+=n;known_tp+=matched
        result['classes'][cls]={'complete_images':len(complete),'partial_images':len(partial),'unknown_images_excluded':unknown,
            'gt':total,'tp':tp,'fp':fp,'fn':fn,'ignored_predictions':ignored,'precision':precision,'recall':recall,'f1':f1,
            'ap50':aps['0.50'],'map50_95':float(np.mean([a for a in aps.values() if a is not None])) if total else None,'ap_by_iou':aps,
            'partial_known_gt':known_gt,'partial_known_tp':known_tp,'partial_known_recall':known_tp/known_gt if known_gt else None}
    for field in ('ap50','map50_95'):
        vals=[v[field] for v in result['classes'].values() if v[field] is not None];result['macro_'+field]=float(np.mean(vals)) if vals else None
    result['excluded_empty_gt_classes']=[k for k,v in result['classes'].items() if not v['gt']]
    return result
