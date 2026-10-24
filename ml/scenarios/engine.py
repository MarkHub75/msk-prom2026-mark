"""One shared context and temporal engine for all eight observation rule groups."""
from copy import deepcopy
import hashlib
import importlib
import json
from pathlib import Path
from uuid import uuid5,NAMESPACE_URL
from ml.contracts import validate_observation
from .common import iou,finite,validate_finding,finding
from .contracts import validate_candidate

MODULES={'01':'motion','02':'machinery','03':'phone','04':'fire_smoking',
         '05':'barriers','06':'height','07':'fall','08':'cargo'}


def load_config(path=None):
    if path is not None:return json.loads(Path(path).read_text())
    directory=Path(__file__).resolve().parents[2]/'configs/scenarios'
    return {'schema_version':'mosprom-scenarios-v1','modules':{key:json.loads((directory/(key+'.json')).read_text()) for key in MODULES},
            'temporal':{'confirm_ms':1000,'min_observations':2,'max_gap_ms':750}}


class ScenarioSuite:
    def __init__(self,config):
        self.config=deepcopy(config)
        if config.get('schema_version')!='mosprom-scenarios-v1' or set(config.get('modules',{}))!=set(MODULES):
            raise ValueError('explicit eight-module suite config required')
        self.policy={'confirm_ms':1000,'min_observations':2,'max_gap_ms':750,**config.get('temporal',{})}
        for key in ('confirm_ms','max_gap_ms'):
            if not finite(self.policy[key]) or self.policy[key]<0:raise ValueError('invalid temporal policy')
        if type(self.policy['min_observations']) is not int or self.policy['min_observations']<1:raise ValueError('invalid observation support')
        for identity,module in config['modules'].items():
            if module.get('scenario_id')!=identity:raise ValueError('rule config scenario identity mismatch')
            policy={**self.policy,**module.get('temporal',{})}
            if any(not finite(policy[k]) or policy[k]<0 for k in ('confirm_ms','max_gap_ms')) or type(policy['min_observations']) is not int or policy['min_observations']<1:
                raise ValueError('invalid per-rule temporal support')
        self.fingerprint=hashlib.sha256(json.dumps(config,sort_keys=True,allow_nan=False).encode()).hexdigest()
        self.modules={key:importlib.import_module('ml.scenarios.rules.'+name).evaluate for key,name in MODULES.items()}
        self.last={};self.previous_people={};self.previous_objects={};self.object_counter=0;self.episodes={}

    def export_state(self):
        return deepcopy({'version':1,'fingerprint':self.fingerprint,'last':self.last,
                         'previous_people':self.previous_people,'previous_objects':self.previous_objects,
                         'object_counter':self.object_counter,'episodes':self.episodes})

    def restore_state(self,state):
        if state.get('version')!=1 or state.get('fingerprint')!=self.fingerprint:raise ValueError('suite policy changed')
        for key in ('last','previous_people','previous_objects','object_counter','episodes'):setattr(self,key,deepcopy(state[key]))

    def _context(self,batch,behavior,legacy_events):
        camera=behavior.export_state()['cameras'].get(batch['camera_id'])
        people=[];active={e['event_id']:e for e in legacy_events}
        if camera and camera['epoch']==batch['stream_epoch']:
            for track in camera['tracks']:
                if track['last_seen']!=batch['media_time_ms']:continue
                found=[d for d in batch['detections'] if d['class_name']=='person' and d['score']>=behavior.config['min_score'] and d['bbox_xyxy']==track['box']]
                if len(found)!=1:continue
                key=f"{batch['camera_id']}/{batch['stream_epoch']}/{camera['generation']}/{track['id']}"
                old=self.previous_people.get(key)
                dt=batch['media_time_ms']-old['time'] if old else None
                if dt is not None and not 0<dt<=self.policy['max_gap_ms']:old=None;dt=None
                people.append({**found[0],'track_key':key,'previous':deepcopy(old['detection']) if old else None,'dt_ms':dt,'posture':behavior._posture(found[0])})
                self.previous_people[key]={'time':batch['media_time_ms'],'detection':deepcopy(found[0])}
                for event in track['active'].values():active.setdefault(event['event_id'],event)
        objects=[];old_objects=self.previous_objects.get(batch['camera_id'],[]);used=set()
        for det in batch['detections']:
            if det['class_name'] in ('person','helmet','bare_head'):continue
            matches=[(iou(det['bbox_xyxy'],old['detection']['bbox_xyxy']),i,old) for i,old in enumerate(old_objects)
                     if i not in used and old['epoch']==batch['stream_epoch'] and old['detection']['class_name']==det['class_name']
                     and 0<batch['media_time_ms']-old['time']<=self.policy['max_gap_ms']
                     and (det.get('object_key')==old['key'] if det.get('object_key') else iou(det['bbox_xyxy'],old['detection']['bbox_xyxy'])>=.2)]
            matches.sort(key=lambda x:x[0],reverse=True)
            old=None
            if matches and (len(matches)==1 or matches[0][0]-matches[1][0]>.1):
                _,index,old=matches[0];used.add(index)
            key=det.get('object_key') or (old['key'] if old else None)
            if not key:self.object_counter+=1;key='object-'+str(self.object_counter)
            objects.append({**det,'object_key':key,'previous':deepcopy(old['detection']) if old else None,
                            'dt_ms':batch['media_time_ms']-old['time'] if old else None})
        self.previous_objects[batch['camera_id']]=[{'key':o['object_key'],'detection':{k:v for k,v in o.items() if k not in ('previous','dt_ms')},
                                                   'epoch':batch['stream_epoch'],'time':batch['media_time_ms']} for o in objects]
        return {'batch':batch,'people':people,'objects':objects,'legacy_events':list(active.values())}

    def _interrupt(self,key,end,reason):
        record=self.episodes[key];record['start']=None;record['n']=0
        event=record.get('event')
        if event and event['state']=='open':
            event.update(state='interrupted',revision=event['revision']+1,end_media_ms=max(end,event['confirmed_media_ms']),reason=reason)
            return deepcopy(event)
        return None

    def update(self,batch,behavior,legacy_events):
        validate_observation(batch);cid=batch['camera_id'];epoch=batch['stream_epoch'];t=batch['media_time_ms']
        if self.config.get('camera_id') is not None and self.config['camera_id']!=cid:raise ValueError('suite camera mismatch')
        if self.config.get('image_size') is not None and self.config['image_size']!=list(batch['image_size']):raise ValueError('suite original image geometry mismatch')
        previous=self.last.get(cid);camera=behavior.export_state()['cameras'].get(cid)
        if camera and camera['epoch']!=epoch:return [],[]
        if previous and previous['epoch']==epoch and (t<=previous['time'] or batch['frame_id']<=previous['frame_id']):return [],[]
        emitted=[]
        broken=previous and (previous['epoch']!=epoch or t-previous['time']>self.policy['max_gap_ms'])
        if broken or batch['status']!='ok':
            for key,record in list(self.episodes.items()):
                if record['camera_id']==cid:
                    e=self._interrupt(key,previous['time'] if previous and previous['epoch']!=epoch else t,'source_reset_or_observation_gap')
                    if e:emitted.append(e)
            self.previous_objects.pop(cid,None)
        self.last[cid]={'epoch':epoch,'time':t,'frame_id':batch['frame_id']}
        if batch['status']!='ok':return emitted,[]
        context=self._context(batch,behavior,legacy_events);findings=[]
        for identity,evaluate in self.modules.items():
            result=evaluate(context,self.config['modules'][identity])
            if not result:result=[finding(identity,'observability','scene','UNKNOWN','no_observable_subject')]
            findings.extend(validate_finding(r) for r in result)
        seen=set()
        for f in findings:
            key=json.dumps([cid,epoch,f['track_key'],f['scenario_id'],f['subrule']],separators=(',',':'))
            if key in seen:raise ValueError('duplicate rule verdict for same subject/frame')
            seen.add(key)
            record=self.episodes.setdefault(key,{'camera_id':cid,'start':None,'n':0,'event':None})
            if f['verdict']=='POSITIVE':
                if record['event'] and record['event']['state']=='open':continue
                if record['start'] is None:record['start']=t
                record['n']+=1
                policy={**self.policy,**self.config['modules'][f['scenario_id']].get('temporal',{})}
                # Existing Fall engine has already confirmed its own temporal rule.
                if f['scenario_id']=='07':policy.update(confirm_ms=0,min_observations=1)
                if record['n']<policy['min_observations'] or t-record['start']<policy['confirm_ms']:continue
                if record['event'] and record['event']['state']=='interrupted':
                    event=record['event'];event.update(state='open',revision=event['revision']+1);event.pop('end_media_ms',None)
                else:
                    identity=str(uuid5(NAMESPACE_URL,key+':'+str(record['start'])))
                    source_start,source_confirm=record['start'],t
                    if f['scenario_id']=='07' and f['subrule'] in ('suspected_fall','prolonged_lying'):
                        a,b=f['attributes'].get('legacy_start_media_ms'),f['attributes'].get('legacy_confirmed_media_ms')
                        if finite(a) and finite(b) and 0<=a<=b<=t:source_start,source_confirm=a,b
                    event={'schema_version':'1.0','contract':'mosprom.event_candidate.v1','candidate_id':identity,'revision':1,
                           'scenario_id':f['scenario_id'],'subrule':f['subrule'],'type':f['subrule'],'camera_id':cid,'stream_epoch':epoch,
                           'track_key':f['track_key'],'state':'open','start_media_ms':source_start,'confirmed_media_ms':source_confirm}
                event.update(reason=f['reason'],confidence=f['score'],attributes=deepcopy(f['attributes']),
                             evidence={'status':'pending','frame_id':batch['frame_id'],'media_time_ms':t,'snapshot_ref':None,'clip_ref':None},
                             qualification='PROTOTYPE_NOT_INDEPENDENTLY_VALIDATED',
                             provenance={'observation_backend':batch.get('backend','unknown'),'source_kind':batch.get('source_kind','unknown'),
                                         'supplied_current_fact_sources':sorted({x['source'] for x in batch.get('scenario_context',{}).get('facts',[]) if isinstance(x,dict) and isinstance(x.get('source'),str) and x.get('frame_id')==batch['frame_id'] and x.get('media_time_ms')==t})})
                event['episode_group_id']=f['attributes'].get('legacy_event_id',event['candidate_id'])
                record['event']=event;emitted.append(deepcopy(event))
            elif f['verdict']=='NEGATIVE':
                event=record.get('event')
                if event and event['state']!='closed':
                    event.update(state='closed',revision=event['revision']+1,end_media_ms=max(t,event['confirmed_media_ms']),reason=f['reason']);emitted.append(deepcopy(event))
                record['event']=None;record['start']=None;record['n']=0
            else:
                e=self._interrupt(key,t,f['reason'])
                if e:emitted.append(e)
        for key,record in list(self.episodes.items()):
            if record['camera_id']==cid and key not in seen:
                e=self._interrupt(key,t,'subject_not_observed')
                if e:emitted.append(e)
        for event in emitted:validate_candidate(event)
        return emitted,findings
