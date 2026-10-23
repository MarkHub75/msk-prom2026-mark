"""Offline source-reference episode diagnostics with onset-support bounds.

Requires explicit acknowledgement for partially reviewed source references.
Predictions are offline envelopes {video_id,event}; public event schema is intact.
Never derive test truth from model predictions or treat unrun videos as misses.
"""
import argparse
from copy import deepcopy
import json
import math
from pathlib import Path

from ml.contracts import validate_event
from .audit import audit_reference

TYPES = ('suspected_fall','prolonged_lying')


def bind_urfall_review(reference, review):
    audit_reference(reference)
    if review.get('predictions_accessed_for_annotation') is not False:
        raise ValueError('prediction-blind reference review is required')
    records={r['video_id']:r for r in review['records']}
    if len(records)!=len(review['records']) or set(records)!={m['video_id'] for m in reference['media']}:
        raise ValueError('one explicit review record per source video required')
    videos=[];episodes=[]
    for media in reference['media']:
        r=records[media['video_id']]
        if r['media_sha256']!=media['media_sha256']:
            raise ValueError('review and media hashes differ')
        if r.get('fall_episode_count') not in (0,1):
            raise ValueError('this importer only supports explicitly reviewed zero/one-fall sources')
        known=[{'start_ms':s['start_ms'],'end_ms':s['end_ms']} for s in media['source_segments'] if s['state']!='unknown']
        unknown=[{'start_ms':s['start_ms'],'end_ms':s['end_ms']} for s in media['source_segments'] if s['state']=='unknown']
        videos.append({k:deepcopy(media[k]) for k in ('video_id','media_sha256','group_id','split','duration_ms','camera_id','scene_id')})
        videos[-1].update(known_windows=known,unknown_windows=unknown,
            actor_policy='video-level source-single-person episode diagnostic; no spatial track/actor GT',
            floor_context=r.get('visible_floor_context'), review_sampling=r['inspection'])
        transitions=[s for s in media['source_segments'] if s['state']=='falling_transition']
        if r['fall_episode_count']==1:
            if len(transitions)!=1 or not r.get('visible_floor_context'):
                raise ValueError('reviewed fall must have one native transition and visible floor context')
            s=transitions[0];following=[v for v in media['source_segments'] if v['state']=='lying_on_ground' and abs(v['start_ms']-s['end_ms'])<.01]
            end=following[0]['end_ms'] if following else s['end_ms']
            episodes.append({'episode_id':media['video_id']+'/fall', 'video_id':media['video_id'],
                'type':'suspected_fall','onset_lower_ms':s['start_ms'],'onset_upper_ms':s['end_ms'],
                'end_ms':end,'left_censored':s['start_ms']==0,
                'right_censored':end==media['duration_ms'],
                'label_provenance':'native source coarse transition window + blinded RGB semantic review'})
        # In this subset all floor-lying tails are shorter than 3s. Intentional
        # bed lying is not converted into an industrial floor violation.
        for i,s in enumerate(media['source_segments']):
            if s['state']!='lying_on_ground' or not r.get('visible_floor_context'):
                continue
            if s['end_ms']-s['start_ms'] < 3000:
                continue
            episodes.append({'episode_id':media['video_id']+'/lying/'+str(i),'video_id':media['video_id'],
                'type':'prolonged_lying','onset_lower_ms':s['start_ms'],'onset_upper_ms':s['start_ms'],
                'end_ms':s['end_ms'],'left_censored':s['start_ms']==0,
                'right_censored':s['end_ms']==media['duration_ms'],
                'label_provenance':'native source lying state >=3s + blinded floor-context review'})
    return {'schema_version':'temporal-episode-gt-v1','quality_level':'source-reference-diagnostic',
        'fully_exhaustive_independent_human_review':False,
        'prediction_blind_annotation':True,
        'reviewer_is_model_developer':review.get('reviewer_is_model_developer',True),
        'final_test':False,'videos':videos,'episodes':episodes,'event_types':list(TYPES),
        'not_implemented':['running','zone_intrusion'],
        'scope':'finite developmental video-level episode diagnostics; source posture references with sampled RGB review; not exact-onset, actor-owned or industrial-quality GT'}


def _validate_gt(gt):
    if gt.get('schema_version')!='temporal-episode-gt-v1':raise ValueError('unsupported episode GT')
    videos={v['video_id']:v for v in gt['videos']}
    if len(videos)!=len(gt['videos']):raise ValueError('duplicate GT video')
    grouped={}; hashes={}
    for v in videos.values():
        if not v.get('group_id') or not v.get('split'):raise ValueError('group and split required')
        for store,key in ((grouped,v['group_id']),(hashes,v['media_sha256'])):
            if key in store and store[key]!=v['split']:raise ValueError('GT lineage crosses splits')
            store[key]=v['split']
        covered=[]
        for windows in (v['known_windows'],v['unknown_windows']):
            for w in windows:
                a,b=w['start_ms'],w['end_ms']
                if not all(type(x) in (float,int) and math.isfinite(x) for x in (a,b)) or not 0<=a<b<=v['duration_ms']+.01:
                    raise ValueError('invalid coverage window')
                covered.append((a,b))
        last=0
        for a,b in sorted(covered):
            if abs(a-last)>.01:raise ValueError('known/unknown coverage must partition video')
            last=b
        if abs(last-v['duration_ms'])>.01:raise ValueError('incomplete review coverage')
    ids=set()
    for e in gt['episodes']:
        if e['episode_id'] in ids:raise ValueError('duplicate GT episode')
        ids.add(e['episode_id'])
        if e['video_id'] not in videos or e['type'] not in TYPES:raise ValueError('unknown GT target')
        a,b,end=e['onset_lower_ms'],e['onset_upper_ms'],e['end_ms']
        if not all(type(x) in (float,int) and math.isfinite(x) for x in (a,b,end)) or not 0<=a<=b<end<=videos[e['video_id']]['duration_ms']+.01:
            raise ValueError('invalid onset support or episode interval')
    return videos


def _matching(edges):
    """Maximum-cardinality bipartite matching, deterministic for fixed inputs."""
    owners={}
    def visit(pred,seen):
        for gt in edges[pred]:
            if gt in seen:continue
            seen.add(gt)
            if gt not in owners or visit(owners[gt],seen):
                owners[gt]=pred;return True
        return False
    for pred in range(len(edges)):visit(pred,set())
    return owners


def _metrics(tp,predicted,truth):
    precision=tp/predicted if predicted else None
    recall=tp/truth if truth else None
    f1=None if precision is None or recall is None else (2*precision*recall/(precision+recall) if precision+recall else 0)
    return {'tp':tp,'fp':predicted-tp,'fn':truth-tp,'precision':precision,'recall':recall,'f1':f1}


def evaluate(gt, predictions, evaluated_video_ids, *, deadline_ms=5000, allow_source_reference=False):
    videos=_validate_gt(gt)
    if type(deadline_ms) not in (int,float) or not math.isfinite(deadline_ms) or deadline_ms<0:
        raise ValueError('finite nonnegative deadline required')
    if not gt.get('fully_exhaustive_independent_human_review') and not allow_source_reference:
        raise ValueError('source-reference diagnostic requires explicit acknowledgement; not final-quality GT')
    evaluated=set(evaluated_video_ids)
    if len(evaluated)!=len(evaluated_video_ids) or not evaluated<=set(videos):raise ValueError('invalid evaluated-video census')
    unique={}; duplicate_rows=0
    for envelope in predictions:
        video_id=envelope['video_id']; event=validate_event(envelope.get('event',envelope))
        if video_id not in videos or video_id not in evaluated:raise ValueError('prediction video is unknown or not in evaluated census')
        if event['type'] not in TYPES:raise ValueError('unexpected prediction type in temporal-only scorer')
        key=event['event_id'];old=unique.get(key)
        if old:
            for k in ('type','confirmed_media_ms'):
                if event[k]!=old['event'][k]:raise ValueError('incident type/confirmation changed across revisions')
            if video_id!=old['video_id']:raise ValueError('incident UUID reused across videos')
            duplicate_rows+=1
        if old is None or event['revision']<old['event']['revision']:
            unique[key]={'video_id':video_id,'event':event}
    eligible=[];unknown=[]
    for row in sorted(unique.values(),key=lambda r:(r['event']['confirmed_media_ms'],r['event']['event_id'])):
        v=videos[row['video_id']];t=row['event']['confirmed_media_ms']
        if not 0<=t<v['duration_ms']:raise ValueError('prediction confirmation lies outside observed source')
        censored=any(e['video_id']==row['video_id'] and e['type']==row['event']['type'] and e.get('left_censored') and e['onset_lower_ms']<=t<e['end_ms'] for e in gt['episodes'])
        if censored or any(w['start_ms']<=t<w['end_ms'] for w in v['unknown_windows']):unknown.append(row)
        else:eligible.append(row)
    positives=[e for e in gt['episodes'] if e['video_id'] in evaluated and not e.get('left_censored')]
    by_type={}
    for kind in TYPES:
        actual=[e for e in positives if e['type']==kind]
        predicted=[p for p in eligible if p['event']['type']==kind]
        definite=[];possible=[]
        for p in predicted:
            t=p['event']['confirmed_media_ms'];d=[];u=[]
            for j,e in enumerate(actual):
                if e['video_id']!=p['video_id'] or t>=e['end_ms']:continue
                lo,hi=e['onset_lower_ms'],e['onset_upper_ms']
                if t>=hi and t-lo<=deadline_ms:d.append(j)
                if t>=lo and t-hi<=deadline_ms:u.append(j)
            definite.append(d);possible.append(u)
        lo,hi=len(_matching(definite)),len(_matching(possible))
        lower,upper=_metrics(lo,len(predicted),len(actual)),_metrics(hi,len(predicted),len(actual))
        by_type[kind]={'truth_episodes':len(actual),'adjudicable_predictions':len(predicted),
            'unknown_predictions':sum(p['event']['type']==kind for p in unknown),
            'lower':lower,'upper':upper,
            'point':lower if lo==hi else None,
            'point_status':'ONSET_BOUNDS_AGREE' if lo==hi else 'AMBIGUOUS_ONSET_SUPPORT_NO_POINT_ESTIMATE'}
    annotated_ms=sum(sum(w['end_ms']-w['start_ms'] for w in videos[v]['known_windows']) for v in evaluated)
    unknown_ms=sum(sum(w['end_ms']-w['start_ms'] for w in videos[v]['unknown_windows']) for v in evaluated)
    return {'protocol':'source-reference-bounded-timely-confirmation-v1',
        'quality_level':gt['quality_level'],'final_test':gt.get('final_test',False),
        'scope':gt['scope'],'deadline_ms':deadline_ms,'evaluated_videos':len(evaluated),
        'unrun_videos':sorted(set(videos)-evaluated),'source_known_ms':annotated_ms,'source_unknown_ms':unknown_ms,
        'unknown_source_duration_rate':unknown_ms/(annotated_ms+unknown_ms) if annotated_ms+unknown_ms else None,
        'unknown_predictions':len(unknown),'revision_rows_deduplicated':duplicate_rows,
        'left_censored_gt_excluded':sum(e['video_id'] in evaluated and bool(e.get('left_censored')) for e in gt['episodes']),
        'per_type':by_type,'not_implemented':{k:{'status':'NOT_IMPLEMENTED','precision':None,'recall':None} for k in gt.get('not_implemented',[])},
        'false_positive_definition':'unmatched strict timely episode assertion; may include semantically true late or repeated alerts',
        'operational_false_alert_rate_measured':False,'model_observation_unknown_rate_measured':False,
        'delivered_alert_latency_measured':False}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    b=sub.add_parser('bind-urfall');b.add_argument('--reference',required=True);b.add_argument('--review',required=True);b.add_argument('--output',required=True)
    e=sub.add_parser('evaluate');e.add_argument('--truth',required=True);e.add_argument('--predictions',required=True);e.add_argument('--evaluated-videos',required=True);e.add_argument('--output',required=True);e.add_argument('--deadline-ms',type=float,default=5000);e.add_argument('--allow-source-reference',action='store_true')
    args=p.parse_args(argv);read=lambda f:json.loads(Path(f).read_text())
    if args.command=='bind-urfall':result=bind_urfall_review(read(args.reference),read(args.review))
    else:result=evaluate(read(args.truth),[json.loads(x) for x in Path(args.predictions).read_text().splitlines() if x.strip()],read(args.evaluated_videos),deadline_ms=args.deadline_ms,allow_source_reference=args.allow_source_reference)
    Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':'WRITTEN','schema_or_protocol':result.get('schema_version',result.get('protocol'))}))


if __name__=='__main__':main()
