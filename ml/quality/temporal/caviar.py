"""Source-XML running development protocol and CPU saved-observation evaluation.

No data acquisition or inference. Derived25FPS time is not native camera PTS.
Only literal visible running/walking actors are scored; unboxed people and other
movement states are not negatives. Source windows are not independently reviewed
running-onset truth or industrial violations.
"""
import argparse
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path

from ml.quality.handoff import load_producer_ready
from .evaluation import _metrics
from .running_zone import RunningZonePrototype

DATASET='caviar-running-walking-source3'
USE='sourceXMLactor/bbox/movement import and temporal development'

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _label(obj):
    values=obj.get('movement_values',[])
    return values[0] if obj.get('appearance')=='visible' and values in (['running'],['walking']) else None


def freeze(pointer,output):
    entry,manifest=load_producer_ready(pointer,dataset_id=DATASET,allowed_use=USE)
    root=Path(entry['absolute_path'])
    rows=[json.loads(x) for x in (root/'frame_annotations.jsonl').read_text().splitlines()]
    target=Path(output);target.mkdir(parents=True,exist_ok=False)
    per=defaultdict(Counter);actor=defaultdict(dict);selected=[];seen=set()
    for row in rows:
        seq,f=row['sequence'],row['frame_id_from_source_filename']
        if f!=row['frame_index0'] or (seq,f) in seen or row['canonical_frame_time_ms']!=f*40:
            raise ValueError('invalid source frame identity/time')
        seen.add((seq,f));per[seq]['frames']+=1
        for obj in row['source_objects']:
            key=obj['track_id']
            if f in actor[(seq,key)]:raise ValueError('duplicate actor/frame')
            actor[(seq,key)][f]=obj
            per[seq]['literal_'+('/'.join(obj['movement_values']))+'_person_frames']+=1
            label=_label(obj)
            per[seq]['visible_'+str(label)+'_person_frames']+=1
        if f%5==0:selected.append({k:row[k] for k in ('sequence','group_id','frame_id_from_source_filename','path','bytes','sha256','width','height','canonical_frame_time_ms')})
    episodes=[]
    for (seq,key),frames in sorted(actor.items()):
        maximum=per[seq]['frames']-1
        for f,obj in sorted(frames.items()):
            label=_label(obj)
            if label is None:continue
            if episodes and episodes[-1]['source']==seq and episodes[-1]['actor']==key and episodes[-1]['label']==label and episodes[-1]['end_frame_exclusive']==f:
                episodes[-1]['end_frame_exclusive']=f+1
            else:
                episodes.append({'episode_id':f'{key}:{label}:{f}','source':seq,'actor':key,'label':label,'start_frame':f,'end_frame_exclusive':f+1})
        for e in [e for e in episodes if e['source']==seq and e['actor']==key]:
            start,end=e['start_frame'],e['end_frame_exclusive']
            e.update(start_derived_ms=start*40,end_derived_ms_exclusive=end*40,duration_derived_ms=(end-start)*40,
                left_censored=start==0 or start-1 not in frames or frames[start-1].get('appearance')!='visible',
                right_censored=end>maximum or end not in frames or frames[end].get('appearance')!='visible',
                onset_semantics='source movement window boundary; not independent gait onset')
    protocol={'protocol':'caviar-source-movement-development-v1','dataset_id':DATASET,'group_id':json.loads((root/'split_manifest.json').read_text())['group_id'],
        'split':'development','independent_test':False,'annotation_provenance':'SOURCE_ANNOTATION / AUTO_PROPOSED import; no new human labels',
        'source_time':'NOMINAL25FPS_DERIVED: source_frame_id*40ms; not original camera PTS; physical time uncertainty unmeasured',
        'sampling':'source_frame_id %5 ==0; no ordinal relabelling','images':len(rows),'sampled_images':len(selected),
        'per_source':{k:dict(v) for k,v in per.items()},'episodes':episodes,
        'baseline':{'running_only':True,'speed_units':'image_diagonals_per_second','speed_threshold':.2,'speed_confirm_ms':1000,'min_score':.5,'keypoint_score':.5,'max_gap_ms':750},
        'H1':{'running_only':True,'speed_units':'body_heights_per_second','speed_threshold':1.5,'speed_confirm_ms':1000,'min_score':.5,'keypoint_score':.5,'max_gap_ms':750},
        'H1_normalization':'distance / elapsed / max(previous observed bbox height,current observed bbox height); apparent body-height proxy, no m/s',
        'H2':'NOT_IMPLEMENTED; only if baseline/H1 require, observed bbox-center running-only anchor with truncation reset, fixed threshold/no grid; root allocation required',
        'selection_gate':'same frozen development: eventF1 gain, no FP increase and no recall regression; root final selection',
        'matching':'person class; unique IoU>=.5 both sourceactor-to-observation and observation-to-sourceactor; ambiguity/unmatched outside scope unknown',
        'negative_scope':'visible literal walking only, never active/inactive/unboxed/annotation-empty',
        'episode_metric':'source running windows, one matched confirmed diagnostic within window is TP; extra distinct diagnostic episodes FPduplicates; walking diagnostics FP; outside known windows unknown; censoring separate',
        'frame_metric':'sampled visible source running/walking actor frames; emitted ongoing fast-state=true is positive; unmatched/abstained source-running frames FN in end-to-end metric, unknown coverage also reported',
        'rights':entry['rights'],'manifest_path':str(root/'manifest.json'),'hashes':{str(p):digest(p) for p in (Path(pointer),root/'manifest.json',root/'frame_annotations.jsonl',root/'source_intervals.json',root/'split_manifest.json',root/'class_map.json')},
        'feature_pass':'Native SplitPose only after root GPU slot allocation; weights/preprocess/runtime/input hashes must be pinned before execution; source JPEG original geometry'}
    (target/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    (target/'selected-inputs.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in selected))
    return protocol


def _iou(a,b):
    ix=max(0,min(a[2],b[2])-max(a[0],b[0]));iy=max(0,min(a[3],b[3])-max(a[1],b[1]))
    i=ix*iy;u=(a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-i
    return i/u if u>0 else 0


def associate(objects,persons):
    """Return unique bidirectional actor/detection ownership, not greedy matches."""
    edges={i:[j for j,p in enumerate(persons) if p['class_name']=='person' and _iou(o['bbox_xyxy_original'],p['bbox_xyxy'])>=.5] for i,o in enumerate(objects)}
    return {i:js[0] for i,js in edges.items() if len(js)==1 and sum(js[0] in v for v in edges.values())==1}


def evaluate_saved(protocol_path,observations,output,*,policy='baseline'):
    if policy not in ('baseline','H1','H2'):raise ValueError('only frozen baseline/H1/H2 accepted')
    protocol_path=Path(protocol_path);p=json.loads(protocol_path.read_text());target=Path(output)
    if target.exists():raise ValueError('fresh immutable output required')
    for path,h in p['hashes'].items():
        if digest(path)!=h:raise ValueError('frozen input changed')
    rows=[json.loads(x) for x in Path(next(k for k in p['hashes'] if k.endswith('/frame_annotations.jsonl'))).read_text().splitlines()]
    refs={(r['sequence'],r['frame_id_from_source_filename']):r for r in rows if r['frame_id_from_source_filename']%5==0}
    probes={};seen=set();sources=defaultdict(Counter);windows=defaultdict(Counter);candidates=[];history={};frame_truth=0;frame_pred=0;frame_tp=0
    target.mkdir(parents=True,exist_ok=False)
    diagnostics=[]
    for line in Path(observations).read_text().splitlines():
        item=json.loads(line);b=item.get('batch',item);seq=item.get('video_id',b['camera_id']);fid=b['frame_id'];identity=(seq,fid)
        if identity not in refs or identity in seen:raise ValueError('observation outside frozen sample or duplicate')
        seen.add(identity);ref=refs[identity]
        if b['media_time_ms']!=fid*40 or b['image_size']!=[ref['width'],ref['height']]:raise ValueError('source time/geometry mismatch')
        if seq not in probes:probes[seq]=RunningZonePrototype({**p[policy],'camera_id':b['camera_id'],'image_size':b['image_size']})
        probe=probes[seq];result=probe.update(b);diagnostics.append({'source':seq,'frame_id':fid,'result':result})
        persons=[d for d in b['detections'] if d['class_name']=='person' and d['score']>=.5] if b['status']=='ok' else []
        objects=ref['source_objects'];matches=associate(objects,persons);camera=probe.tracker.export_state()['cameras'].get(b['camera_id'],{})
        keys={}
        for tr in camera.get('tracks',[]):
            if tr['last_seen']!=b['media_time_ms']:continue
            js=[j for j,person in enumerate(persons) if person['bbox_xyxy']==tr['box']]
            if len(js)==1:keys[js[0]]=f"{b['camera_id']}/{b['stream_epoch']}/{camera['generation']}/{tr['id']}"
        actor_by_key={keys[j]:objects[i] for i,j in matches.items() if j in keys}
        c=sources[seq];c['sampled_frames']+=1;c['unassigned_observed_persons_unknown']+=len(persons)-len(matches)
        for i,obj in enumerate(objects):
            label=_label(obj)
            if label is None:c['source_actor_frames_unknown_or_other_state']+=1;continue
            c[label+'_source_actor_frames']+=1;frame_truth+=label=='running'
            key=keys.get(matches.get(i));state=probe.previous.get(key)
            if key is None:c['unmatched_source_actor_frames']+=1
            elif not state:c['matched_but_anchor_unknown_actor_frames']+=1
            else:c['observed_anchor_actor_frames']+=1
            if key:
                aid=obj['track_id'];old=history.get((seq,aid))
                if old and old!=key:c['actor_track_key_changes']+=1
                history[(seq,aid)]=key
            predicted=bool(state and state['fast_emitted']);frame_pred+=predicted;frame_tp+=predicted and label=='running'
            c['frame_truth_running']+=label=='running';c['frame_predicted_running']+=predicted;c['frame_tp']+=predicted and label=='running'
            for window in p['episodes']:
                if window['source']==seq and window['actor']==obj['track_id'] and window['start_frame']<=fid<window['end_frame_exclusive']:
                    w=windows[window['episode_id']];w['sampled_actor_frames']+=1;w['matched_person_frames']+=key is not None
                    w['observed_anchor_frames']+=state is not None;w['predicted_running_frames']+=predicted
        for d in result['diagnostics']:
            if d['kind']!='fast_motion_candidate':continue
            obj=actor_by_key.get(d['track_key']);label=_label(obj) if obj else None
            e={'source':seq,'actor':obj['track_id'] if obj else None,'frame_id':fid,'track_key':d['track_key'],'label':label,'diagnostic':d}
            candidates.append(e)
        for u in result['unknowns']:c['unknown_'+u['reason']]+=1
    if seen!=set(refs):raise ValueError('incomplete frozen sample census; report cannot pretend full run')
    run=[e for e in p['episodes'] if e['label']=='running'];matched=set();tp=fp=unknown=duplicates=0
    for pred in candidates:
        if pred['label'] is None:unknown+=1;sources[pred['source']]['unknown_prediction_episodes']+=1;continue
        sources[pred['source']]['adjudicable_prediction_episodes']+=1
        fits=[e for e in run if e['source']==pred['source'] and e['actor']==pred['actor'] and e['start_frame']<=pred['frame_id']<e['end_frame_exclusive']]
        if fits:
            eid=fits[0]['episode_id']
            if eid in matched:fp+=1;duplicates+=1
            else:matched.add(eid);tp+=1;sources[pred['source']]['episode_tp']+=1
        else:fp+=1
    report={'protocol':'caviar-source-movement-development-v1','policy':policy,'status':'SOURCE_REFERENCE_EVALUATED','industrial_quality_claim':False,'original_camera_PTS':False,'independent_test':False,
        'episode_metrics':_metrics(tp,tp+fp,len(run)),'frame_metrics':_metrics(frame_tp,frame_pred,frame_truth),
        'unknown_prediction_episodes':unknown,'duplicate_prediction_episodes':duplicates,
        'source_running_episodes':len(run),'source_running_censored_episodes':sum(e['left_censored'] or e['right_censored'] for e in run),
        'per_source':{s:{'coverage':dict(c),
            'frame_metrics':_metrics(c['frame_tp'],c['frame_predicted_running'],c['frame_truth_running']),
            'episode_metrics':_metrics(c['episode_tp'],c['adjudicable_prediction_episodes'],sum(e['source']==s for e in run))} for s,c in sources.items()},
        'actor_window_coverage':[{'episode_id':e['episode_id'],'label':e['label'],'left_censored':e['left_censored'],'right_censored':e['right_censored'],**dict(windows[e['episode_id']])} for e in p['episodes']],
        'sampled_frames':len(seen),
        'hashes':{'protocol':digest(protocol_path),'observations':digest(observations),'code':digest(__file__),'running_zone':digest(Path(__file__).with_name('running_zone.py'))},
        'scope':'Only literal visible sourceXML running/walking actors; unknown/unboxed background excluded. Missing model evidence on source-positive frames is FN, not silently removed. No operational falsealarms/hour.'}
    (target/'diagnostics.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in diagnostics))
    (target/'predictions.json').write_text(json.dumps(candidates,indent=2)+'\n')
    (target/'metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main():
    a=argparse.ArgumentParser(description=__doc__);sub=a.add_subparsers(dest='cmd',required=True)
    f=sub.add_parser('freeze');f.add_argument('--pointer',required=True);f.add_argument('--output',required=True)
    e=sub.add_parser('evaluate');e.add_argument('--protocol',required=True);e.add_argument('--observations',required=True);e.add_argument('--output',required=True);e.add_argument('--policy',choices=('baseline','H1','H2'),default='baseline')
    args=a.parse_args()
    if args.cmd=='freeze':r=freeze(args.pointer,args.output);print(json.dumps({k:r[k] for k in ('images','sampled_images','per_source')}))
    else:print(json.dumps(evaluate_saved(args.protocol,args.observations,args.output,policy=args.policy)))

if __name__=='__main__':main()
