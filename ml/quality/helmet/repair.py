"""Apply explicit blind-reviewed GT patches without changing source labels."""
from copy import deepcopy
import hashlib,json
from pathlib import Path


def apply_reviews(dataset,patches):
    result=deepcopy(dataset);images={i['image_id']:i for i in result['images']}
    if set(patches)-set(images):raise ValueError('review refers to image outside frozen selection')
    for image_id,patch in patches.items():
        image=images[image_id]
        if patch.get('reviewer')!='AI-agent' or not isinstance(patch.get('reason'),str):raise ValueError('explicit reviewer/reason required')
        image.setdefault('source_annotations',deepcopy(image['annotations']))
        for kind in ('annotations','ignore_regions'):
            if kind in patch:
                values=deepcopy(patch[kind])
                for value in values:
                    box=value['bbox_xyxy']
                    if len(box)!=4 or any(isinstance(v,bool) or not isinstance(v,(int,float)) for v in box) or not (0<=box[0]<box[2]<=image['width'] and 0<=box[1]<box[3]<=image['height']):raise ValueError('review box outside image or invalid')
                image[kind]=values
        if 'class_coverage' in patch:image['class_coverage']=deepcopy(patch['class_coverage'])
        if any(v not in ('complete','partial','unknown') for v in image['class_coverage'].values()):raise ValueError('invalid review coverage')
        image['review']={k:deepcopy(v) for k,v in patch.items() if k not in ('annotations','ignore_regions','class_coverage')}
    result['parent_dataset_digest']=result.pop('dataset_digest',None)
    result['dataset_id']='helmet-development-quality-v2'
    result['annotation_unit']='helmet = visible safety helmet object; bare_head = full observable anatomical head extent scalp-to-chin; ordinary hats/insufficient visibility unknown'
    result['review_scope']='AI-agent GT repair; no human expert claim; no model improvement implied'
    result['dataset_digest']=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return result
