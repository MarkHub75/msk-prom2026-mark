"""Offline Running/Zone evaluation readiness, with no public Event changes.

Only an explicitly versioned mapping may compare fast_motion_candidate with
independent running GT, and doing so requires experimental-proxy acknowledgement.
Missing scene truth/polygon/coverage returns NOT_EVALUATED, never zero accuracy.
"""
import argparse
from collections import defaultdict
import hashlib
import json
import math
from pathlib import Path

from .evaluation import _matching, _metrics

SCENARIOS = ('running', 'zone_entry')
MAPPING = {'running': 'fast_motion_candidate', 'zone_entry': 'observed_polygon_entry'}
PROTOCOL = 'offline-motion-zone-episode-v1'


def _number(x):return type(x) in (int, float) and math.isfinite(x)
def _string(x):return isinstance(x, str) and bool(x)


def _unknown(reason):
    return {'status': 'NOT_EVALUATED', 'reason': reason, 'tp': None, 'fp': None,
            'fn': None, 'precision': None, 'recall': None, 'f1': None}


def _coverage(scene, scenario, actor, zone):
    rows = [c for c in scene.get('coverage', []) if
            (c.get('scenario'), c.get('actor_id'), c.get('zone_id')) == (scenario, actor, zone)]
    if len(rows) != 1:return None
    windows = rows[0].get('windows')
    if not isinstance(windows, list) or not windows:return None
    end = 0
    for w in windows:
        a,b = w.get('start_ms'),w.get('end_ms')
        if not all(_number(v) for v in (a,b)) or not 0<=a<b<=scene['duration_ms']:
            raise ValueError('invalid coverage interval')
        if a != end or w.get('observability') not in ('known','unknown'):
            return None  # Missing/overlapping coverage is not verified negative exposure.
        end = b
    return windows if end == scene['duration_ms'] else None


def _polygon_available(scene, zone):
    if not all(_string(zone.get(k)) for k in ('zone_id','geometry_revision','polygon_provenance','rule_revision')):
        return False
    size=scene.get('image_size');p=zone.get('polygon_xy')
    if not isinstance(size,list) or len(size)!=2 or any(type(x) is not int or x<=0 for x in size):return False
    if not isinstance(p,list) or len(p)<3 or any(not isinstance(v,list) or len(v)!=2 or not all(_number(x) for x in v) or not 0<=v[0]<=size[0] or not 0<=v[1]<=size[1] for v in p):return False
    return abs(sum(p[i-1][0]*v[1]-v[0]*p[i-1][1] for i,v in enumerate(p)))>1e-9


def _ready(scene, scenario):
    if scenario not in scene.get('episode_annotations_complete_for',[]):
        return 'EPISODE_COMPLETENESS_NOT_DECLARED'
    if scene.get('annotation_status')!='ANNOTATED' or scene.get('prediction_blind_annotation') is not True:
        return 'SCENE_GT_UNAVAILABLE_OR_NOT_BLIND'
    actors=scene.get('actor_ids')
    if not isinstance(actors,list) or not actors or len(set(actors))!=len(actors) or not all(_string(a) for a in actors):return 'ACTOR_CENSUS_UNAVAILABLE'
    if scenario=='running':zones=[None]
    else:
        zones=scene.get('zones')
        if not zones or not all(_polygon_available(scene,z) for z in zones):return 'POLYGON_OR_CAMERA_POLICY_UNAVAILABLE'
        if len({z['zone_id'] for z in zones})!=len(zones):raise ValueError('duplicate zone identity')
        zones=[z['zone_id'] for z in zones]
    for actor in actors:
        for zone in zones:
            if _coverage(scene,scenario,actor,zone) is None:return 'COMPLETE_KNOWN_UNKNOWN_COVERAGE_UNAVAILABLE'
    return None


def _validate(gt):
    if gt.get('schema_version')!='motion-zone-episode-gt-v1':raise ValueError('unsupported offline motion GT schema')
    if not _string(gt.get('config_version')) or not _string(gt.get('mapping_version')) or gt.get('scenario_to_diagnostic')!=MAPPING:
        raise ValueError('explicit supported scenario/diagnostic mapping and config versions required')
    scenes={};group_splits={};source_splits={}
    for s in gt.get('scenes',[]):
        if not all(_string(s.get(k)) for k in ('source_id','camera_id','source_epoch','scene_id','group_id','split')) or not _number(s.get('duration_ms')) or s['duration_ms']<=0:
            raise ValueError('explicit source/camera/epoch/scene/group/split identity and duration required')
        digest=s.get('source_sha256')
        if gt.get('artifact_kind')!='SYNTHETIC_FIXTURE' and (not isinstance(digest,str) or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest)):
            raise ValueError('non-synthetic reference requires lowercase SHA256 source identity')
        if s['source_id'] in scenes:raise ValueError('duplicate source identity')
        for mapping,key in ((group_splits,s['group_id']),(source_splits,s.get('source_sha256',s['source_id']))):
            if key is not None and key in mapping and mapping[key]!=s['split']:raise ValueError('protected source/group crosses splits')
            mapping[key]=s['split']
        scenes[s['source_id']]=s
    seen=set()
    for e in gt.get('episodes',[]):
        if not _string(e.get('episode_id')) or e['episode_id'] in seen:raise ValueError('duplicate/invalid GT episode identity')
        seen.add(e['episode_id'])
        if e.get('source_id') not in scenes or e.get('scenario') not in SCENARIOS:raise ValueError('unknown GT source/scenario')
        scene=scenes[e['source_id']]
        if scene.get('actor_ids') and e.get('actor_id') not in scene['actor_ids']:raise ValueError('unknown GT actor')
        if e['scenario']=='running' and e.get('zone_id') is not None:raise ValueError('running GT is actor-scoped, not implicitly zone-scoped')
        if e['scenario']=='zone_entry' and scene.get('zones') and e.get('zone_id') not in [z.get('zone_id') for z in scene['zones']]:raise ValueError('unknown GT zone')
        a,b,end=e.get('onset_lower_ms'),e.get('onset_upper_ms'),e.get('end_ms')
        if not all(_number(v) for v in (a,b,end)) or not 0<=a<=b<end<=scene['duration_ms']:raise ValueError('invalid GT onset support/end')
        if any(type(e.get(k)) is not bool for k in ('left_censored','right_censored')) or e.get('observability') not in ('known','unknown'):
            raise ValueError('explicit censoring and event observability required')
    return scenes


def _binding(scene, track_key, t):
    matches=[b for b in scene.get('track_bindings',[]) if b.get('track_key')==track_key and
             _number(b.get('start_ms')) and _number(b.get('end_ms')) and b['start_ms']<=t<b['end_ms'] and
             _string(b.get('binding_revision')) and _string(b.get('provenance'))]
    return matches[0]['actor_id'] if len(matches)==1 else None


def evaluate(gt, predictions, evaluated_source_ids, *, allow_experimental_running_proxy=False, deadline_ms=5000):
    if not _number(deadline_ms) or deadline_ms<0:raise ValueError('finite nonnegative deadline required')
    base={'protocol':PROTOCOL,'public_event_schema_changed':False,'real_quality_claim':False,
          'running_is_experimental_proxy':True,'delivery_latency_measured':False,
          'artifact_kind':gt.get('artifact_kind','UNSPECIFIED_REFERENCE') if isinstance(gt,dict) else 'UNAVAILABLE',
          'per_type':{s:_unknown('SCENE_GT_UNAVAILABLE') for s in SCENARIOS}}
    if not isinstance(gt,dict) or not gt.get('scenes') or not isinstance(gt.get('episodes'),list):
        return {**base,'status':'NOT_EVALUATED'}
    scenes=_validate(gt);evaluated=list(evaluated_source_ids)
    if len(set(evaluated))!=len(evaluated) or not set(evaluated)<=set(scenes):raise ValueError('invalid evaluated-source census')
    base.update(config_version=gt['config_version'],mapping_version=gt['mapping_version'],
                evaluated_source_ids=evaluated,unrun_source_ids=sorted(set(scenes)-set(evaluated)))
    unique={};duplicates=0;gaps=0;abstentions=0
    for p in predictions:
        source=p.get('source_id')
        if source not in scenes or source not in evaluated:raise ValueError('prediction source not in explicit evaluated census')
        scene=scenes[source]
        for k in ('camera_id','source_epoch','group_id'):
            if p.get(k)!=scene[k]:raise ValueError('prediction source lineage mismatch')
        if p.get('config_version')!=gt['config_version'] or p.get('mapping_version')!=gt['mapping_version']:
            raise ValueError('prediction configuration/scenario mapping changed')
        if p.get('record_kind') in ('gap','abstention'):
            if not _number(p.get('media_time_ms')) or not 0<=p['media_time_ms']<scene['duration_ms']:raise ValueError('invalid missing-observation record')
            gaps+=p['record_kind']=='gap';abstentions+=p['record_kind']=='abstention';continue
        scenario=p.get('scenario')
        if scenario not in SCENARIOS or p.get('diagnostic_kind')!=MAPPING[scenario]:raise ValueError('unsupported/unmapped diagnostic')
        if not all(_string(p.get(k)) for k in ('prediction_episode_id','track_key')):raise ValueError('stable prediction episode/track identity required')
        t=p.get('confirmed_media_ms')
        if not _number(t) or not 0<=t<scene['duration_ms']:raise ValueError('prediction time outside observed source')
        key=p['prediction_episode_id'];old=unique.get(key)
        if old is not None:
            identity=('source_id','camera_id','source_epoch','group_id','track_key','actor_id','scenario','zone_id','geometry_revision','config_version','mapping_version')
            if any(old.get(k)!=p.get(k) for k in identity):raise ValueError('prediction episode identity reused across actors/tracks/zones/configs')
            duplicates+=1
        if old is None or t<old['confirmed_media_ms']:unique[key]=p
    base.update(repeated_diagnostic_rows_coalesced=duplicates,gap_records=gaps,abstention_records=abstentions,
                model_gaps_do_not_delete_gt_positives=True)
    for scenario in SCENARIOS:
        if not evaluated:
            base['per_type'][scenario]=_unknown('NO_EVALUATED_SOURCES');continue
        if scenario=='running' and not allow_experimental_running_proxy:
            base['per_type'][scenario]=_unknown('EXPERIMENTAL_RUNNING_PROXY_ACK_REQUIRED');continue
        missing={source:_ready(scenes[source],scenario) for source in evaluated}
        if any(missing.values()):
            base['per_type'][scenario]={**_unknown('GT_OR_POLICY_NOT_READY'), 'source_reasons':{s:r for s,r in missing.items() if r}};continue
        truths=[e for e in gt.get('episodes',[]) if e['scenario']==scenario and e['source_id'] in evaluated and e['observability']=='known' and not e['left_censored']]
        unresolved_truth=[e for e in gt.get('episodes',[]) if e['scenario']==scenario and e['source_id'] in evaluated and (e['observability']=='unknown' or e['left_censored'])]
        accepted=[];unknown=[];wrong_identity=[]
        for p in unique.values():
            if p['scenario']!=scenario:continue
            scene=scenes[p['source_id']];t=p['confirmed_media_ms'];actor=p.get('actor_id');zone=p.get('zone_id')
            binding=_binding(scene,p['track_key'],t)
            if actor not in scene['actor_ids'] or binding is None:
                unknown.append({'prediction_episode_id':p['prediction_episode_id'],'reason':'ACTOR_OR_TRACK_BINDING_UNRESOLVED'});continue
            if scenario=='zone_entry':
                configured=[z for z in scene['zones'] if z['zone_id']==zone]
                if not configured or p.get('geometry_revision')!=configured[0]['geometry_revision']:
                    unknown.append({'prediction_episode_id':p['prediction_episode_id'],'reason':'ZONE_POLICY_UNRESOLVED'});continue
            elif zone is not None:raise ValueError('running diagnostic unexpectedly zone-scoped')
            windows=_coverage(scene,scenario,actor,zone)
            if any(w['observability']=='unknown' and w['start_ms']<=t<w['end_ms'] for w in windows):
                unknown.append({'prediction_episode_id':p['prediction_episode_id'],'reason':'UNKNOWN_REFERENCE_WINDOW'});continue
            if any(e['source_id']==p['source_id'] and e['actor_id']==actor and e.get('zone_id')==zone and e['onset_lower_ms']<=t<e['end_ms'] for e in unresolved_truth):
                unknown.append({'prediction_episode_id':p['prediction_episode_id'],'reason':'UNRESOLVED_OR_LEFT_CENSORED_EPISODE'});continue
            accepted.append(p)
            if binding!=actor:wrong_identity.append(p['prediction_episode_id'])
        definite=[];possible=[]
        for p in accepted:
            d=[];u=[];t=p['confirmed_media_ms']
            if p['prediction_episode_id'] not in wrong_identity:
                for j,e in enumerate(truths):
                    if (p['source_id'],p['actor_id'],p.get('zone_id'))!=(e['source_id'],e['actor_id'],e.get('zone_id')) or t>=e['end_ms']:continue
                    lo,hi=e['onset_lower_ms'],e['onset_upper_ms']
                    if t>=hi and t-lo<=deadline_ms:d.append(j)
                    if t>=lo and t-hi<=deadline_ms:u.append(j)
            definite.append(d);possible.append(u)
        lower=_metrics(len(_matching(definite)),len(accepted),len(truths))
        upper=_metrics(len(_matching(possible)),len(accepted),len(truths))
        known_ms=sum(w['end_ms']-w['start_ms'] for source in evaluated for c in scenes[source]['coverage'] if c['scenario']==scenario for w in c['windows'] if w['observability']=='known')
        unknown_ms=sum(w['end_ms']-w['start_ms'] for source in evaluated for c in scenes[source]['coverage'] if c['scenario']==scenario for w in c['windows'] if w['observability']=='unknown')
        base['per_type'][scenario]={'status':'EVALUATED_SYNTHETIC_FIXTURE' if base['artifact_kind']=='SYNTHETIC_FIXTURE' else 'EVALUATED_EXPERIMENTAL_REFERENCE',
            'truth_episodes':len(truths),'adjudicable_predictions':len(accepted),'unknown_predictions':unknown,
            'wrong_actor_binding_predictions':len(wrong_identity),'unresolved_or_left_censored_truth':len(unresolved_truth),
            'known_actor_scenario_ms':known_ms,'unknown_actor_scenario_ms':unknown_ms,
            'lower':lower,'upper':upper,'point':lower if lower['tp']==upper['tp'] else None,
            'diagnostic_kind':MAPPING[scenario], 'not_a_validated_running_classifier':scenario=='running'}
    done=sum(r['status'].startswith('EVALUATED') for r in base['per_type'].values())
    base['status']='EVALUATED' if done==len(SCENARIOS) else 'PARTIALLY_EVALUATED' if done else 'NOT_EVALUATED'
    base['fp_definition']='unmatched strict timely episode assertions, including wrong actor/zone and duplicate distinct episodes; not operational false-alarm rate'
    return base


def wrap_prototype_result(result, *, source_id, group_id, config_version, mapping_version, actor_by_track, zone_id):
    """Explicit caller-owned association/config binding; never guesses actor/zone.

    Repeated identical logical diagnostics get a stable internal episode key.
    Distinct logical IDs are not merged merely because they are close in time.
    """
    base={'source_id':source_id,'camera_id':result['camera_id'],'source_epoch':result['stream_epoch'],
          'group_id':group_id,'config_version':config_version,'mapping_version':mapping_version}
    rows=[]
    for d in result.get('diagnostics',[]):
        scenario=next((s for s,k in MAPPING.items() if d.get('kind')==k),None)
        if scenario is None:continue  # Exit/direction are not running/entry assertions.
        if scenario=='zone_entry' and not _string(zone_id):raise ValueError('explicit configured zone ID required')
        track=d['track_key'];zone=zone_id if scenario=='zone_entry' else None
        t=d['confirmed_media_ms'];anchor=d.get('start_media_ms',t)
        identity=[source_id,result['stream_epoch'],track,scenario,zone,anchor]
        rows.append({**base,'record_kind':'diagnostic','prediction_episode_id':hashlib.sha256(json.dumps(identity,separators=(',',':')).encode()).hexdigest(),
            'scenario':scenario,'diagnostic_kind':d['kind'],'track_key':track,
            'actor_id':actor_by_track.get(track),'zone_id':zone,
            'geometry_revision':result.get('geometry_revision') if zone is not None else None,
            'confirmed_media_ms':t,'support_start_media_ms':anchor})
    for u in result.get('unknowns',[]):
        rows.append({**base,'record_kind':'gap' if u.get('reason')=='observation_gap_reset' else 'abstention',
                     'media_time_ms':result['media_time_ms'],'reason':u.get('reason'),'track_key':u.get('track_key')})
    return rows


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--truth',required=True);p.add_argument('--predictions',required=True);p.add_argument('--evaluated-sources',required=True);p.add_argument('--output',required=True);p.add_argument('--allow-experimental-running-proxy',action='store_true');p.add_argument('--deadline-ms',type=float,default=5000);args=p.parse_args(argv)
    read=lambda f:json.loads(Path(f).read_text())
    result=evaluate(read(args.truth),[json.loads(x) for x in Path(args.predictions).read_text().splitlines() if x.strip()],read(args.evaluated_sources),allow_experimental_running_proxy=args.allow_experimental_running_proxy,deadline_ms=args.deadline_ms)
    Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'artifact_kind':result['artifact_kind'],'real_quality_claim':False}))


if __name__=='__main__':main()
