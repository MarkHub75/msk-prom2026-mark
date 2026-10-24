"""Attribute E003 observation loss at EXISTING decoder/consumer stages.

No inference, threshold search, model/rule changes, or new quality experiment.
Only source-visible literal running/walking actor windows are diagnostic scope.
Saved decoded records cannot explain missing pre-NMS tensors or low-score raw
anchors: those causes remain unknown rather than being invented as model facts.
"""
import argparse
from collections import Counter,defaultdict
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

from ml.quality.handoff import load_producer_ready
from .caviar import DATASET,USE,digest,associate,_iou,_label
from .running_zone import RunningZonePrototype

DECODER_SCORE=.25
CONSUMER_SCORE=.5


def attribute(objects,detections,index,anchor_available=None):
    """Mutually exclusive source-actor loss attribution; thresholds are fixed."""
    decoded=[d for d in detections if d['class_name']=='person' and d['score']>=DECODER_SCORE]
    accepted=[d for d in decoded if d['score']>=CONSUMER_SCORE]
    low=associate(objects,decoded);high=associate(objects,accepted)
    obj=objects[index]
    edges=[d for d in decoded if _iou(obj['bbox_xyxy_original'],d['bbox_xyxy'])>=.5]
    best=max((_iou(obj['bbox_xyxy_original'],d['bbox_xyxy']) for d in decoded),default=None)
    if index in high:
        category='consumer_unique_anchor_observed' if anchor_available else 'pose_anchor_or_track_gap'
    elif index in low and decoded[low[index]]['score']<CONSUMER_SCORE:
        category='consumer_score_gate'
    elif not decoded:category='no_decoded_person'
    elif not edges:category='localization_below_ownership_iou'
    else:category='ambiguous_ownership'
    return {'category':category,'decoded_person_count':len(decoded),'consumer_person_count':len(accepted),
        'decoder_unique_owner':index in low,'consumer_unique_owner':index in high,
        'best_decoded_person_iou':best,'decoder_candidate_scores':[d['score'] for d in edges],
        'decoder_candidate_ious':[_iou(obj['bbox_xyxy_original'],d['bbox_xyxy']) for d in edges]}


def xml_index(path):
    root=ET.parse(path).getroot();result={}
    for frame in root.findall('frame'):
        fid=int(frame.attrib['number'])
        for obj in frame.findall('./objectlist/object'):
            box=obj.find('box')
            if box is None:continue
            xc,yc,w,h=(float(box.attrib[k]) for k in ('xc','yc','w','h'))
            key=(fid,obj.attrib['id'])
            if key in result:raise ValueError('duplicate native XML object/frame')
            result[key]={'bbox':[xc-w/2,yc-h/2,xc+w/2,yc+h/2],
                'appearance':obj.findtext('appearance'),
                'movement_values':sorted(set(x.text.strip() for x in obj.findall('./hypothesislist/hypothesis/movement') if x.text))}
    return root.attrib.get('name'),result


def audit(protocol,selected,observations,run,model_manifest,pointer,output):
    manifest,verification=load_producer_ready(pointer,dataset_id=DATASET,allowed_use=USE)
    protocol=Path(protocol);p=json.loads(protocol.read_text());run_path=Path(run);execution=json.loads(run_path.read_text());model_path=Path(model_manifest);model=json.loads(model_path.read_text())
    target=Path(output)
    if target.exists():raise ValueError('fresh immutable audit output required')
    if execution['status']!='COMPLETED' or execution['observations_sha256']!=digest(observations) or execution['protocol_sha256']!=digest(protocol) or execution['selected_inputs_sha256']!=digest(selected):raise ValueError('E003 execution identities changed')
    if execution['model_manifest_sha256']!=digest(model_path) or model['thresholds']['confidence']!=DECODER_SCORE:raise ValueError('existing decoder model/threshold identity changed')
    if p['baseline']['min_score']!=CONSUMER_SCORE or p['baseline']['keypoint_score']!=.5:raise ValueError('existing consumer/ankle threshold changed')
    root=Path(manifest['absolute_path'])
    if p['hashes'].get(str(root/'manifest.json'))!=digest(root/'manifest.json'):raise ValueError('producer release differs from frozen E003')
    # The top-level producer pointer can legitimately advance; the immutable
    # selected release and its asset hashes must still match the E003 snapshot.
    for path,h in p['hashes'].items():
        if path.endswith('/READY.json'):continue
        if digest(path)!=h:raise ValueError('frozen annotation/source metadata changed')
    refs={(r['sequence'],r['frame_id_from_source_filename']):r for r in (json.loads(x) for x in (root/'frame_annotations.jsonl').read_text().splitlines())}
    chosen=[json.loads(x) for x in Path(selected).read_text().splitlines()];selected_refs={};xml={};checks=Counter()
    for r in chosen:
        key=(r['sequence'],r['frame_id_from_source_filename']);source=refs[key];fid=key[1]
        if key in selected_refs or fid%5 or int(Path(r['path']).stem[len(r['sequence']):])!=fid or source['frame_index0']!=fid or r['canonical_frame_time_ms']!=fid*40:raise ValueError('source filename/frame/time mismatch')
        if any(r[k]!=source[k] for k in ('path','bytes','sha256','width','height')):raise ValueError('selected input/producer record mismatch')
        source_xml=source['source_annotation_path']
        if source_xml not in xml:xml[source_xml]=xml_index(source_xml)
        name,objects=xml[source_xml]
        if name!=r['sequence']:raise ValueError('native XML sequence mismatch')
        for o in source['source_objects']:
            native=objects[(fid,o['source_object_id'])]
            if native['bbox']!=o['bbox_xyxy_original'] or native['appearance']!=o['appearance'] or native['movement_values']!=sorted(o['movement_values']):raise ValueError('native XML/GT conversion mismatch')
            checks['native_xml_actor_boxes_verified']+=1
            b=o['bbox_xyxy_original'];w,h=r['width'],r['height']
            checks['source_boxes_outside_image']+=not(0<=b[0]<b[2]<=w and 0<=b[1]<b[3]<=h)
        selected_refs[key]=source;checks['original_source_ids_and_geometry_verified']+=1
    seen=set();details=[];per=defaultdict(Counter);totals=Counter();probes={};scores=Counter();records=[]
    for line in Path(observations).read_text().splitlines():
        item=json.loads(line);batch=item['batch'];key=(item['video_id'],batch['frame_id'])
        if key not in selected_refs or key in seen:raise ValueError('unexpected/duplicate saved frame')
        seen.add(key);source=selected_refs[key];seq,fid=key;w,h=source['width'],source['height']
        if batch['image_size']!=[w,h] or batch['media_time_ms']!=fid*40 or item['input_sha256']!=source['sha256']:raise ValueError('saved original frame geometry/time/hash mismatch')
        if batch['status']!='ok':raise ValueError('feature pass reported non-ok observation')
        for d in batch['detections']:
            scores[d['class_name']+(':consumer_accepted' if d['score']>=.5 else ':decoder_only')]+=1
            if not math.isfinite(d['score']) or d['score']<DECODER_SCORE:raise ValueError('saved detection contradicts decoder confidence')
            b=d['bbox_xyxy'];checks['decoded_boxes_verified']+=1
            checks['decoded_boxes_outside_original_image']+=not(0<=b[0]<b[2]<=w and 0<=b[1]<b[3]<=h)
            for point in d.get('keypoints') or []:
                checks['decoded_keypoints_outside_original_image']+=not(0<=point[0]<=w and 0<=point[1]<=h)
        if seq not in probes:probes[seq]=RunningZonePrototype({**p['baseline'],'camera_id':batch['camera_id'],'image_size':[w,h]})
        probe=probes[seq];result=probe.update(batch)
        accepted=[d for d in batch['detections'] if d['class_name']=='person' and d['score']>=.5]
        owners=associate(source['source_objects'],accepted);camera=probe.tracker.export_state()['cameras'][batch['camera_id']]
        for index,obj in enumerate(source['source_objects']):
            label=_label(obj)
            if label not in ('running','walking'):continue
            track_keys=[]
            if index in owners:
                person=accepted[owners[index]]
                track_keys=[f"{batch['camera_id']}/{batch['stream_epoch']}/{camera['generation']}/{tr['id']}" for tr in camera['tracks'] if tr['last_seen']==batch['media_time_ms'] and tr['box']==person['bbox_xyxy']]
            anchor=len(track_keys)==1 and track_keys[0] in probe.previous
            finding=attribute(source['source_objects'],batch['detections'],index,anchor)
            record={'source':seq,'source_frame_id':fid,'derived_ms':fid*40,'source_actor':obj['track_id'],'source_movement':label,'source_box_xyxy':obj['bbox_xyxy_original'],'image_size':[w,h],
                **finding,'matched_track_keys':track_keys,'baseline_unknowns':result['unknowns']}
            details.append(record);per[(seq,label)][finding['category']]+=1;totals[label+':'+finding['category']]+=1
        records.append({'source':seq,'source_frame_id':fid,'decoded_persons':sum(d['class_name']=='person' for d in batch['detections']),
            'accepted_persons':len(accepted),'input_sha256':item['input_sha256']})
    if seen!=set(selected_refs):raise ValueError('incomplete saved frame census')
    report={'experiment':'E007','status':'MEASURED_ERROR_ATTRIBUTION_ONLY','new_inference':False,'new_hypothesis':False,'threshold_sweep':False,'model_quality_claim':False,
        'source_label_scope':'sourceXML visible literal running/walking only; unboxed/active/inactive/appearance windows never negative',
        'existing_stages':{'decoder_confidence':.25,'consumer_person_score':.5,'ownership_unique_bidirectional_iou':.5,'ankle_confidence':.5},
        'sampled_images':len(seen),'checks':dict(checks),'detection_counts':dict(scores),'totals':dict(totals),
        'per_source_movement':{s+':'+m:dict(c) for (s,m),c in per.items()},'producer_verification':verification,
        'coordinate_evidence':'Saved originalimage geometry/inputSHA match producer frame IDs. GTxyxy rederived exactly from native XML xc/yc/w/h. Decoded original-coordinate bounds checked. Per-request raw output tensors/transforms were not saved, so numerical inverse-letterbox re-execution or below-decoder model evidence is unavailable.',
        'limitations':['no pre-NMS/raw tensors: cannot separate low-score raw anchors, NMS suppression, or complete model non-response below decoded stage','no new native rerun and no thresholds changed','numerical integrity is not independent visual GT verification','nominal25FPS derived time is not native camera PTS','stage attribution is not new event accuracy or industrial quality'],
        'hashes':{str(f):digest(f) for f in (protocol,Path(selected),Path(observations),run_path,model_path,root/'manifest.json',root/'frame_annotations.jsonl',Path(__file__))},
        'native_XML_hashes':{path:digest(path) for path in xml}}
    target.mkdir(parents=True,exist_ok=False)
    (target/'actor-attribution.jsonl').write_text(''.join(json.dumps(d)+'\n' for d in details))
    (target/'frame-census.jsonl').write_text(''.join(json.dumps(d)+'\n' for d in records))
    (target/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('protocol','selected','observations','run','model-manifest','pointer','output'):p.add_argument('--'+name,required=True)
    a=p.parse_args();r=audit(a.protocol,a.selected,a.observations,a.run,a.model_manifest,a.pointer,a.output)
    print(json.dumps({'totals':r['totals'],'checks':r['checks']}))

if __name__=='__main__':main()
