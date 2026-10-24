"""Saved-output-only fixed-policy Helmet drift attribution; no model execution."""
import argparse
from collections import Counter
import json
from pathlib import Path
import numpy as np
from ml.quality.handoff import sha256
from .metrics import evaluate_dataset,_overlap

CLASSES=('helmet','bare_head')
CONFIDENCE=.25
IOU=.5


def trace(image,predictions):
    """Expose scorer's stable greedy assignments and explicit exclusion statuses."""
    gt=image.get('annotations',[]);matches={};records=[]
    for cls in CLASSES:
        coverage=image.get('class_coverage',{}).get(cls,'unknown')
        ordinary=[i for i,g in enumerate(gt) if g['class_name']==cls and not g.get('ignore',False)]
        ignores=[g for g in gt if g['class_name']==cls and g.get('ignore',False)]
        ignores += [g for g in image.get('ignore_regions',[]) if g.get('class_name') in (None,cls)]
        eligible=[(i,p) for i,p in enumerate(predictions) if p['class_name']==cls and p['score']>=CONFIDENCE]
        eligible=sorted(eligible,key=lambda v:(-v[1]['score'],v[0]))[:300]
        used=set()
        for index,p in eligible:
            best=max([(_overlap(p['bbox_xyxy'],gt[i]['bbox_xyxy']),i) for i in ordinary if i not in used],default=(-1,-1),key=lambda x:(x[0],-x[1]))
            row={'prediction_index':index,'prediction':p,'coverage':coverage,'matched_gt_index':None}
            if coverage=='unknown':row['status']='UNSCORED_UNKNOWN'
            elif best[0]>=IOU:
                used.add(best[1]);matches[best[1]]={'prediction_index':index,'prediction':p,'iou':best[0]}
                row.update(status='TP' if coverage=='complete' else 'PARTIAL_KNOWN_TP',matched_gt_index=best[1],iou=best[0])
            elif any(_overlap(p['bbox_xyxy'],g['bbox_xyxy'],ioa=True)>=.5 for g in ignores):row['status']='IGNORED_REGION'
            elif coverage=='partial':row['status']='IGNORED_PARTIAL_UNMATCHED'
            else:row['status']='FP'
            records.append(row)
    return {'matches':matches,'predictions':records}


def evidence_for_gt(gt,predictions):
    """Nearest saved boxes at unchanged floor/primary; labels are hypotheses only."""
    def best(rows):
        if not rows:return None
        i,p=max(rows,key=lambda x:(_overlap(x[1]['bbox_xyxy'],gt['bbox_xyxy']),x[1]['score'],-x[0]))
        return {'prediction_index':i,'prediction':p,'iou':_overlap(p['bbox_xyxy'],gt['bbox_xyxy'])}
    same=[(i,p) for i,p in enumerate(predictions) if p['class_name']==gt['class_name']]
    other=[(i,p) for i,p in enumerate(predictions) if p['class_name']!=gt['class_name'] and p['score']>=CONFIDENCE]
    floor=best(same);primary=best([(i,p) for i,p in same if p['score']>=CONFIDENCE]);wrong=best(other)
    if primary and primary['iou']>=IOU:reason='GREEDY_ASSIGNMENT_COMPETITION_POSSIBLE'
    elif floor and floor['iou']>=IOU and floor['prediction']['score']<CONFIDENCE:reason='SAVED_SAME_CLASS_OVERLAP_BELOW_PRIMARY_SCORE'
    elif wrong and wrong['iou']>=IOU:reason='OTHER_CLASS_OVERLAP_CANDIDATE_NOT_PROVEN_CLASS_ERROR'
    elif primary and primary['iou']>0:reason='SAME_CLASS_PRIMARY_LOCALIZATION_BELOW_IOU'
    else:reason='NO_OVERLAPPING_SAME_CLASS_PRIMARY_SAVED_BOX'
    return {'nearest_same_class_saved_floor':floor,'nearest_same_class_primary':primary,'nearest_other_class_primary':wrong,'unmatched_diagnostic':reason}


def audit_predictions(dataset,variants):
    metrics={name:evaluate_dataset(dataset,preds) for name,preds in variants.items()}
    images=[];gts=[];fp=[];counts={}
    for image in dataset['images']:
        identity=image['image_id'];traces={name:trace(image,preds[identity]) for name,preds in variants.items()}
        # Numerical attribution must reproduce established scorer, not redefine it.
        for name,t in traces.items():
            for cls in CLASSES:
                statuses=Counter(r['status'] for r in t['predictions'] if r['prediction']['class_name']==cls)
                counts.setdefault(name,Counter()).update({f'{cls}:tp':statuses['TP'],f'{cls}:fp':statuses['FP'],f'{cls}:partial_tp':statuses['PARTIAL_KNOWN_TP']})
            for row in t['predictions']:
                if row['status']!='FP':continue
                prediction=row['prediction'];candidates=[(i,g,_overlap(prediction['bbox_xyxy'],g['bbox_xyxy'])) for i,g in enumerate(image.get('annotations',[])) if not g.get('ignore',False)]
                nearest=max(candidates,key=lambda x:x[2],default=None)
                reason='NO_OVERLAPPING_LABELED_GT'
                if nearest and nearest[2]>0:
                    reason='OTHER_CLASS_OVERLAP_CANDIDATE' if nearest[1]['class_name']!=prediction['class_name'] else ('DUPLICATE_GT_OVERLAP_CANDIDATE' if nearest[2]>=IOU else 'SAME_CLASS_LOCALIZATION_BELOW_IOU')
                fp.append({'variant':name,'image_id':identity,**row,'diagnostic':reason,'nearest_labeled_gt':None if nearest is None else {'gt_index':nearest[0],'annotation':nearest[1],'iou':nearest[2]}})
        images.append({'image_id':identity,'class_coverage':image.get('class_coverage',{}),'variant_prediction_records':{name:t['predictions'] for name,t in traces.items()}})
        for index,gt in enumerate(image.get('annotations',[])):
            coverage=image.get('class_coverage',{}).get(gt['class_name'],'unknown')
            if gt['class_name'] not in CLASSES or gt.get('ignore',False):continue
            record={'gt_id':f'{identity}#{index}','image_id':identity,'gt_index':index,'annotation':gt,'coverage':coverage,'variants':{}}
            for name,t in traces.items():
                match=t['matches'].get(index)
                state=('NOT_SCORED_UNKNOWN' if coverage=='unknown' else ('TP' if match else 'FN'))
                record['variants'][name]={'state':state,'match':match,**evidence_for_gt(gt,variants[name][identity])}
            gts.append(record)
    for name,c in counts.items():
        for cls in CLASSES:
            if c[f'{cls}:tp']!=metrics[name]['classes'][cls]['tp'] or c[f'{cls}:fp']!=metrics[name]['classes'][cls]['fp'] or c[f'{cls}:partial_tp']!=metrics[name]['classes'][cls]['partial_known_tp']:
                raise ValueError('trace differs from frozen scorer')
    pairs={}
    for a,b in [('native','float'),('float','baseline_ptq'),('native','baseline_ptq')]:
        if a not in variants or b not in variants:continue
        summary={}
        for cls in CLASSES:
            transitions=Counter();reasons=Counter()
            for g in gts:
                if g['coverage']!='complete' or g['annotation']['class_name']!=cls:continue
                x,y=(g['variants'][n]['state'] for n in (a,b));transitions[f'{x}->{y}']+=1
                if x=='TP' and y=='FN':reasons[g['variants'][b]['unmatched_diagnostic']]+=1
            summary[cls]={'primary_complete_gt_transitions':dict(transitions),'lost_tp_diagnostic_reasons':dict(reasons)}
        pairs[f'{a}_to_{b}']=summary
    fp_pairs={}
    for pair in pairs:
        a,b=pair.split('_to_');links=[]
        for image in dataset['images']:
            src=[r for r in fp if r['variant']==a and r['image_id']==image['image_id']]
            dst=[r for r in fp if r['variant']==b and r['image_id']==image['image_id']];used=set()
            for source in sorted(src,key=lambda x:(-x['prediction']['score'],x['prediction_index'])):
                candidates=[(_overlap(source['prediction']['bbox_xyxy'],target['prediction']['bbox_xyxy']),j) for j,target in enumerate(dst) if j not in used and target['prediction']['class_name']==source['prediction']['class_name']]
                overlap,index=max(candidates,default=(-1,-1),key=lambda x:(x[0],-x[1]))
                opposite=[{'prediction_index':target['prediction_index'],'class_name':target['prediction']['class_name'],'iou':_overlap(source['prediction']['bbox_xyxy'],target['prediction']['bbox_xyxy'])} for target in dst if target['prediction']['class_name']!=source['prediction']['class_name'] and _overlap(source['prediction']['bbox_xyxy'],target['prediction']['bbox_xyxy'])>=IOU]
                retained=overlap>=IOU
                if retained:used.add(index)
                links.append({'image_id':image['image_id'],'class_name':source['prediction']['class_name'],'source_prediction_index':source['prediction_index'],
                     'status':'RETAINED_FP_OVERLAP' if retained else 'SOURCE_FP_WITHOUT_SAME_CLASS_FP_COUNTERPART',
                     'target_prediction_index':dst[index]['prediction_index'] if retained else None,'counterpart_iou':overlap if retained else None,
                     'other_class_fp_overlap_candidates':opposite})
            for j,target in enumerate(dst):
                if j not in used:links.append({'image_id':image['image_id'],'class_name':target['prediction']['class_name'],'target_prediction_index':target['prediction_index'],'status':'TARGET_FP_WITHOUT_SAME_CLASS_FP_COUNTERPART'})
        fp_pairs[pair]={'policy':'diagnostic greedy score-order same-class FP correspondence IoU>=0.5, not an added metric/threshold experiment','counts':dict(Counter(x['status'] for x in links)),'records':links}
    return {'metrics':metrics,'pair_summary':pairs,'per_gt':gts,'false_positives':fp,'per_image':images,'fp_pairs':fp_pairs}


def raw_audit(dataset,variants,raw_dirs):
    identities=[i['image_id'] for i in dataset['images']]
    # These historical native raw files lack explicit per-NPZ IDs. Report this
    # binding assumption and require preserved prediction insertion order parity.
    if any(list(p)!=identities for p in variants.values()):
        return {'status':'SKIPPED','reason':'raw index cannot be bound to common GT order without inference'}
    inventories={};available={}
    for name,directory in raw_dirs.items():
        directory=Path(directory);files=[directory/f'{i:04d}.npz' for i in range(len(identities))]
        inventories[name]={'path':str(directory),'expected':52,'present':sum(p.is_file() for p in files)}
        if not all(p.is_file() for p in files):continue
        available[name]=files
    records=[]
    for index,identity in enumerate(identities):
        arrays={};hashes={}
        for name,files in available.items():
            with np.load(files[index],allow_pickle=False) as archive:
                if archive.files!=['output0']:raise ValueError('unexpected saved raw ABI')
                a=archive['output0']
                if a.shape!=(1,6,8400) or a.dtype.kind!='f' or not np.isfinite(a).all():raise ValueError('invalid saved numeric output')
                arrays[name]=a
            hashes[name]=sha256(files[index])
        comparisons={}
        for a,b in [('native','float'),('float','baseline_ptq')]:
            if a not in arrays or b not in arrays:continue
            x,y=arrays[a],arrays[b];delta=np.abs(x.astype(np.float64)-y.astype(np.float64))
            comparisons[f'{a}_to_{b}']={'bitwise_equal':bool(np.array_equal(x,y)),'allclose_rtol1e5_atol1e5':bool(np.allclose(x,y,rtol=1e-5,atol=1e-5)),
                'mean_abs_diff_by_channel':delta.mean(axis=(0,2)).tolist(),'max_abs_diff_by_channel':delta.max(axis=(0,2)).tolist(),
                'class_anchor_primary_crossings_down':((x[:,4:]>=CONFIDENCE)&(y[:,4:]<CONFIDENCE)).sum(axis=(0,2)).tolist(),
                'class_anchor_primary_crossings_up':((x[:,4:]<CONFIDENCE)&(y[:,4:]>=CONFIDENCE)).sum(axis=(0,2)).tolist()}
        records.append({'image_id':identity,'raw_index':index,'raw_sha256':hashes,'comparisons':comparisons})
    return {'status':'DIAGNOSTIC','inventory':inventories,'channels':['cx','cy','w','h','helmet','bare_head'],
        'binding':'historical numeric filenames indexed by preserved same52 dataset/prediction order; no embedded native NPZ image identity',
        'anchor_crossings_are_not_object_counts':True,'images':records}


def run(dataset_path,prediction_paths,raw_dirs,output):
    dataset=json.loads(Path(dataset_path).read_text());variants={k:json.loads(Path(p).read_text()) for k,p in prediction_paths.items()}
    # The established evaluator rejects sealed test, partial FP invention and missing images.
    result=audit_predictions(dataset,variants);raw=raw_audit(dataset,variants,raw_dirs)
    out=Path(output);out.mkdir(parents=True,exist_ok=False)
    protocol={'status':'DIAGNOSTIC_SAVED_OUTPUTS_ONLY','dataset_file_sha256':sha256(dataset_path),'dataset_semantic_digest':dataset.get('dataset_digest'),
        'prediction_sha256':{k:sha256(p) for k,p in prediction_paths.items()},'images':len(dataset['images']),
        'confidence':CONFIDENCE,'iou':IOU,'nms':'unchanged preserved predictions; not rerun','raw_score_floor':.001,
        'scope':'source-overlapping AI-reviewed development GT; no independent accuracy/improvement/hardware claim',
        'diagnostic_reasons':'nearest saved-box overlap is evidence, not a proven causal attribution; NMS/raw-anchor provenance not reconstructed',
        'execution':'NO_NN_NO_GPU_NO_COMPILE_NO_LINQ_NO_DATA_DOWNLOAD_NO_GT_EDITS'}
    for name,value in [('protocol.json',protocol),('summary.json',{'status':protocol['status'],'pair_summary':result['pair_summary'],'metrics':result['metrics'],'fp_pair_counts':{k:v['counts'] for k,v in result['fp_pairs'].items()},'false_positive_reason_counts':{n:dict(Counter(x['diagnostic'] for x in result['false_positives'] if x['variant']==n)) for n in variants}}),('fp-pair-correspondence.json',result['fp_pairs']),('per-gt.json',result['per_gt']),('false-positives.json',result['false_positives']),('per-image.json',result['per_image']),('raw-comparison.json',raw)]:
        (out/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    return result['pair_summary']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--dataset',required=True);p.add_argument('--native',required=True);p.add_argument('--float',dest='float_path',required=True);p.add_argument('--ptq',required=True);p.add_argument('--native-raw',required=True);p.add_argument('--float-raw',required=True);p.add_argument('--ptq-raw',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    print(json.dumps(run(a.dataset,{'native':a.native,'float':a.float_path,'baseline_ptq':a.ptq},{'native':a.native_raw,'float':a.float_raw,'baseline_ptq':a.ptq_raw},a.output),indent=2))
