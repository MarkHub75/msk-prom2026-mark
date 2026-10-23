"""UNVALIDATED offline image-plane motion/zone probe over existing detections.

No model runs, metres/second, gait-classification claim or production events.
Zone geometry/provenance and camera-specific speed threshold must be explicit.
"""
import argparse
from copy import deepcopy
import json
import math
from pathlib import Path

from ml.behavior import BehaviorEngine
from ml.contracts import validate_observation


def _finite(x):return type(x) in (int,float) and math.isfinite(x)


def _distance_segment(p,a,b):
    dx,dy=b[0]-a[0],b[1]-a[1]
    t=0 if dx*dx+dy*dy==0 else max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)))
    return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)


def _relation(point, polygon, margin):
    inside=False;x,y=point
    for i,b in enumerate(polygon):
        a=polygon[i-1]
        if _distance_segment(point,a,b)<=margin:return 'unknown'
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
    return 'inside' if inside else 'outside'


def _cross(a,b,c,d):
    side=lambda p,q,r:(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    return side(a,b,c)*side(a,b,d)<0 and side(c,d,a)*side(c,d,b)<0


class RunningZonePrototype:
    """One camera/source geometry, shared existing tracker, diagnostics only.

    'fast_motion_candidate' is a configured displacement proxy, not recognized
    running. No output matches or extends the public event schema.
    """
    def __init__(self, config):
        self.config=deepcopy(config)
        for k in ('camera_id','geometry_revision','polygon_provenance'):
            if not isinstance(config.get(k),str) or not config[k]:raise ValueError('explicit '+k+' required')
        size=config.get('image_size')
        if not isinstance(size,list) or len(size)!=2 or any(type(v) is not int or v<=0 for v in size):raise ValueError('fixed original image_size required')
        poly=config.get('polygon_xy')
        if not isinstance(poly,list) or len(poly)<3 or any(not isinstance(p,list) or len(p)!=2 or not all(_finite(v) for v in p) or not 0<=p[0]<=size[0] or not 0<=p[1]<=size[1] for p in poly):raise ValueError('valid original-image polygon required')
        if len({tuple(p) for p in poly})!=len(poly):raise ValueError('duplicate polygon vertex')
        if abs(sum(poly[i-1][0]*p[1]-p[0]*poly[i-1][1] for i,p in enumerate(poly)))<1e-6:raise ValueError('degenerate polygon')
        for i in range(len(poly)):
            for j in range(i+1,len(poly)):
                if j in (i,(i+1)%len(poly)) or i==(j+1)%len(poly):continue
                if _cross(poly[i],poly[(i+1)%len(poly)],poly[j],poly[(j+1)%len(poly)]):raise ValueError('self-intersecting polygon')
        self.units=config.get('speed_units')
        if self.units not in ('pixels_per_second','image_diagonals_per_second'):raise ValueError('explicit image-plane speed_units required')
        self.threshold=config.get('speed_threshold')
        if not _finite(self.threshold) or self.threshold<=0:raise ValueError('explicit positive camera-specific speed_threshold required')
        self.max_gap=config.get('max_gap_ms',750)
        self.confirm=config.get('speed_confirm_ms',1000)
        self.min_score=config.get('min_score',.5);self.kp_score=config.get('keypoint_score',.5)
        self.margin=config.get('boundary_margin_px',1)
        self.direction_min=config.get('direction_min_motion_px',5)
        self.direction_cos=config.get('against_direction_cosine',-.3)
        for name,value in [('max_gap_ms',self.max_gap),('speed_confirm_ms',self.confirm),('boundary_margin_px',self.margin),('direction_min_motion_px',self.direction_min)]:
            if not _finite(value) or value<0:raise ValueError('invalid '+name)
        if not all(_finite(v) and 0<=v<=1 for v in (self.min_score,self.kp_score)) or not _finite(self.direction_cos) or not -1<=self.direction_cos<=0:raise ValueError('invalid confidence/direction policy')
        direction=config.get('allowed_direction_xy')
        if direction is not None:
            if not isinstance(direction,list) or len(direction)!=2 or not all(_finite(v) for v in direction) or math.hypot(*direction)==0:raise ValueError('nonzero image-plane direction required')
            length=math.hypot(*direction);direction=[v/length for v in direction]
        self.direction=direction
        self.tracker=BehaviorEngine({'min_score':self.min_score,'max_gap_ms':self.max_gap})
        self.previous={};self.epoch=None;self.last_time=None;self.last_frame=None;self.retired=set()

    def _anchor(self,person):
        if person.get('visibility') in ('occluded','unknown'):return None
        points=person.get('keypoints')
        if points is None or len(points)!=17:return None
        feet=[points[i] for i in (15,16)];w,h=self.config['image_size']
        if any(p[2]<self.kp_score or not 0<=p[0]<w or not 0<=p[1]<h for p in feet):return None
        return [(feet[0][0]+feet[1][0])/2,max(feet[0][1],feet[1][1])]

    def update(self,batch):
        validate_observation(batch)
        if batch['camera_id']!=self.config['camera_id'] or list(batch['image_size'])!=self.config['image_size']:
            raise ValueError('camera/geometry mismatch')
        result={'status':'UNVALIDATED_PROTOTYPE','production_running_zone':'NOT_IMPLEMENTED',
                'not_an_external_event':True,'camera_id':batch['camera_id'],'stream_epoch':batch['stream_epoch'],
                'frame_id':batch['frame_id'],'media_time_ms':batch['media_time_ms'],
                'input_backend':batch.get('backend','unknown'),'speed_units':self.units,
                'geometry_revision':self.config['geometry_revision'],
                'polygon_provenance':self.config['polygon_provenance'],
                'physical_calibration':'NONE','diagnostics':[],'unknowns':[]}
        epoch,t,fid=batch['stream_epoch'],batch['media_time_ms'],batch['frame_id']
        if epoch in self.retired or epoch==self.epoch and self.last_time is not None and (t<=self.last_time or fid<=self.last_frame):
            result['ignored_reason']='late_or_duplicate_source_observation';return result
        if self.epoch is not None and epoch!=self.epoch:
            self.retired.add(self.epoch);self.previous.clear();self.last_time=None
        gap=self.last_time is not None and t-self.last_time>self.max_gap
        if gap or batch['status']!='ok':
            self.previous.clear();result['unknowns'].append({'reason':'observation_gap_reset'})
        self.epoch,self.last_time,self.last_frame=epoch,t,fid
        if batch['status']!='ok':
            self.tracker.on_gap(batch);return result
        # Reuse existing camera/epoch/generation tracker; ignore its unrelated
        # fall/helmet events. This probe never publishes a production event.
        self.tracker.update(batch)
        camera=self.tracker.export_state()['cameras'][batch['camera_id']]
        persons=[d for d in batch['detections'] if d['class_name']=='person' and d['score']>=self.min_score]
        current={}
        for track in camera['tracks']:
            if track['last_seen']!=t:continue
            key=f"{batch['camera_id']}/{epoch}/{camera['generation']}/{track['id']}"
            matches=[p for p in persons if p['bbox_xyxy']==track['box']]
            if len(matches)!=1:
                result['unknowns'].append({'track_key':key,'reason':'ambiguous_current_detection'});continue
            anchor=self._anchor(matches[0])
            if anchor is None:
                result['unknowns'].append({'track_key':key,'reason':'insufficient_ankle_observability'});continue
            relation=_relation(anchor,self.config['polygon_xy'],self.margin)
            if relation=='unknown':
                result['unknowns'].append({'track_key':key,'reason':'polygon_boundary_uncertain'});continue
            old=self.previous.get(key)
            state={'point':anchor,'time':t,'relation':relation,'fast_since':None,'fast_emitted':False,'against_emitted':False}
            emit=lambda kind,**fields:result['diagnostics'].append({'kind':kind,'track_key':key,'anchor_xy':anchor,**fields})
            if old is None:
                if relation=='inside':result['unknowns'].append({'track_key':key,'reason':'inside_at_first_observation_entry_unknown'})
            else:
                elapsed=(t-old['time'])/1000
                dx,dy=anchor[0]-old['point'][0],anchor[1]-old['point'][1]
                distance=math.hypot(dx,dy)
                speed=distance/elapsed
                if self.units=='image_diagonals_per_second':speed/=math.hypot(*batch['image_size'])
                if speed>=self.threshold:
                    state['fast_since']=t if old['fast_since'] is None else old['fast_since']
                    state['fast_emitted']=old['fast_emitted']
                    if not state['fast_emitted'] and t-state['fast_since']>=self.confirm:
                        emit('fast_motion_candidate',speed=speed,units=self.units,
                             start_media_ms=state['fast_since'],confirmed_media_ms=t,
                             interpretation='image-plane displacement proxy; not gait/running recognition')
                        state['fast_emitted']=True
                if old['relation']=='outside' and relation=='inside':
                    emit('observed_polygon_entry',start_media_ms=old['time'],confirmed_media_ms=t,
                         crossing_time_bounds_ms=[old['time'],t],physical_intrusion_claim=False)
                if old['relation']=='inside' and relation=='outside':emit('observed_polygon_exit',confirmed_media_ms=t)
                if old['relation']==relation=='outside' and any(_cross(old['point'],anchor,self.config['polygon_xy'][i-1],p) for i,p in enumerate(self.config['polygon_xy'])):
                    result['unknowns'].append({'track_key':key,'reason':'unobserved_path_may_cross_polygon'})
                if self.direction and relation=='inside' and distance>=self.direction_min:
                    cosine=(dx*self.direction[0]+dy*self.direction[1])/distance
                    if cosine<self.direction_cos:
                        state['against_emitted']=True
                        if not old['against_emitted']:emit('motion_against_configured_direction',cosine=cosine,confirmed_media_ms=t)
            current[key]=state
        if not persons:result['unknowns'].append({'reason':'no_accepted_person_observation'})
        self.previous=current
        return result


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True);p.add_argument('--config',required=True);p.add_argument('--output',required=True);args=p.parse_args(argv)
    probe=RunningZonePrototype(json.loads(Path(args.config).read_text()))
    with Path(args.input).open() as source,Path(args.output).open('w') as target:
        for line in source:
            if line.strip():target.write(json.dumps(probe.update(json.loads(line)),allow_nan=False)+'\n')


if __name__=='__main__':main()
