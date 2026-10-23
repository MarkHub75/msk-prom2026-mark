"""CPU-only deterministic construction-PPE inventory and development selection."""
from collections import Counter
import hashlib,json,math
from pathlib import Path,PurePosixPath
import zipfile
import numpy as np
from PIL import Image,ImageOps,ImageDraw


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _features(path):
    with Image.open(path) as im:
        rgb=ImageOps.exif_transpose(im).convert('RGB');w,h=rgb.size
        exact=hashlib.sha256(np.asarray(rgb).tobytes()).hexdigest()
        gray=rgb.convert('L');a=np.asarray(gray.resize((32,32),Image.Resampling.LANCZOS),float)
        cosine=np.cos(np.outer(np.arange(8),(2*np.arange(32)+1))*math.pi/64)
        coeff=cosine@a@cosine.T;median=np.median(coeff.reshape(-1)[1:]);bits=(coeff>median).reshape(-1)
        p=sum(int(v)<<i for i,v in enumerate(bits));b=np.asarray(gray.resize((9,8),Image.Resampling.LANCZOS),float)
        d=sum(int(v)<<i for i,v in enumerate((b[:,1:]>b[:,:-1]).reshape(-1)))
    return w,h,exact,p,d


def curate(archive,output,artifacts,count=32):
    archive,output,artifacts=Path(archive),Path(output),Path(artifacts);artifacts.mkdir(parents=True,exist_ok=True)
    if not output.exists():
        output.mkdir(parents=True)
        with zipfile.ZipFile(archive) as z:
            for name in z.namelist():
                pure=PurePosixPath(name)
                if pure.is_absolute() or '..' in pure.parts:raise ValueError('unsafe source archive path')
            z.extractall(output)
    # Artifact has top-level images/labels; tolerate an explicit single root dir.
    base=output
    if not (base/'images').is_dir():
        matches=list(base.glob('*/images'))
        if len(matches)!=1:raise ValueError('cannot find unique archive images directory')
        base=matches[0].parent
    archive_hash=digest(archive)
    images=[];orphans=[];classes={0:'helmet',7:'bare_head'}
    for split in ('train','val','test'):
        stems={}
        for path in sorted((base/'images'/split).glob('*')):
            if path.suffix.lower() not in ('.jpg','.jpeg','.png'):continue
            if path.stem in stems:raise ValueError('ambiguous image stem')
            stems[path.stem]=path
            label=base/'labels'/split/(path.stem+'.txt')
            if not label.is_file():continue
            w,h,rgb,ph,dh=_features(path);annotations=[];all_labels=[]
            for line in label.read_text().splitlines():
                if not line.strip():continue
                values=line.split()
                if len(values)!=5:raise ValueError('unexpected non-detection label')
                cls=int(values[0]);cx,cy,bw,bh=map(float,values[1:])
                box=[(cx-bw/2)*w,(cy-bh/2)*h,(cx+bw/2)*w,(cy+bh/2)*h]
                if not all(math.isfinite(v) for v in box) or bw<=0 or bh<=0:raise ValueError('invalid YOLO box')
                all_labels.append({'source_class':cls,'bbox_xyxy':box})
                if cls in classes:annotations.append({'class_name':classes[cls],'bbox_xyxy':box,'ignore':False})
            images.append({'image_id':'construction:'+split+':'+path.name,'path':str(path.resolve()),'label_path':str(label.resolve()),'original_split':split,'split':split,
                           'source_name':'ultralytics-construction-ppe','source_version':'sha256:'+archive_hash,'source_url':'https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip',
                           'license':'AGPL-3.0 notice in artifact; upstream photo rights unresolved','file_sha256':digest(path),'label_sha256':digest(label),'decoded_rgb_sha256':rgb,
                           'width':w,'height':h,'phash64':f'{ph:016x}','dhash64':f'{dh:016x}','annotations':annotations,'source_labels':all_labels,
                           'class_coverage':{'helmet':'partial','bare_head':'partial'},'ignore_regions':[],
                           'camera_id':None,'actor_group_id':None,'pretraining_overlap':'UNKNOWN_NOT_PROVEN_INDEPENDENT'})
        orphans += [str(p.relative_to(base)) for p in (base/'labels'/split).glob('*.txt') if p.stem not in stems]
    parent=list(range(len(images)))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b:parent[max(a,b)]=min(a,b)
    edges=[]
    for i,a in enumerate(images):
        for j in range(i):
            b=images[j];exact=a['file_sha256']==b['file_sha256'] or a['decoded_rgb_sha256']==b['decoded_rgb_sha256']
            pd=(int(a['phash64'],16)^int(b['phash64'],16)).bit_count();dd=(int(a['dhash64'],16)^int(b['dhash64'],16)).bit_count()
            near=pd<=6 and dd<=8 and abs(math.log((a['width']/a['height'])/(b['width']/b['height'])))<=.05
            if exact or near:
                union(i,j);edges.append({'a':a['image_id'],'b':b['image_id'],'kind':'exact' if exact else 'perceptual_proxy','phash_distance':pd,'dhash_distance':dd})
    components={}
    for i,image in enumerate(images):components.setdefault(find(i),[]).append(image)
    groups=[]
    for component in components.values():
        group='construction-proxy:'+min(x['file_sha256'] for x in component)[:20]
        splits=sorted({x['original_split'] for x in component})
        for image in component:image['group_id']=group
        groups.append({'group_id':group,'members':[x['image_id'] for x in component],'original_splits':splits,'independence':'duplicate proxy only; camera/source lineage unknown'})
    eligible=[x for x in images if x['original_split']=='val' and 'test' not in next(g['original_splits'] for g in groups if g['group_id']==x['group_id'])]
    selected=[];seen=set()
    for image in sorted(eligible,key=lambda x:(x['file_sha256'],x['image_id'])):
        if image['group_id'] in seen:continue
        seen.add(image['group_id']);selected.append(image)
        if len(selected)==count:break
    for image in selected:image['split']='val'
    dataset={'schema_version':'helmet-dataset-v1','dataset_id':'construction-ppe-fixed-dev32-v1','selection':'one image per duplicate-proxy component, lowest SHA; official-val only, no official-test-touching component',
             'pretraining_overlap':'UNKNOWN; not an independent final test','annotation_status':'SOURCE_LABEL_BENCHMARK_PARTIAL_UNTIL_BLIND_REVIEW','images':selected}
    raw=json.dumps(dataset,sort_keys=True,separators=(',',':')).encode();dataset['dataset_digest']=hashlib.sha256(raw).hexdigest()
    (artifacts/'development-dataset.json').write_text(json.dumps(dataset,indent=2)+'\n')
    audit={'archive_sha256':archive_hash,'paired_images':len(images),'original_split_counts':dict(Counter(x['original_split'] for x in images)),'orphan_labels':orphans,'components':groups,'edges':edges,'cross_split_components':sum(len(g['original_splits'])>1 for g in groups),'selected_images':len(selected),'dataset_digest':dataset['dataset_digest'],'test_inference':'NOT_RUN'}
    (artifacts/'dataset-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    (artifacts/'inventory-all.json').write_text(json.dumps({'images':images},indent=2)+'\n')
    tiles=[]
    for image in selected:
        im=Image.open(image['path']).convert('RGB');draw=ImageDraw.Draw(im)
        for a in image['annotations']:
            box=a['bbox_xyxy'];draw.rectangle(box,outline='red' if a['class_name']=='bare_head' else 'lime',width=3);draw.text(box[:2],a['class_name'],fill='red' if a['class_name']=='bare_head' else 'lime')
        im.thumbnail((480,360));tile=Image.new('RGB',(480,390),'white');tile.paste(im,(0,0));ImageDraw.Draw(tile).text((4,365),image['image_id'],fill='black');tiles.append(tile)
    for start in range(0,len(tiles),8):
        sheet=Image.new('RGB',(480*2,390*4),'white')
        for k,tile in enumerate(tiles[start:start+8]):sheet.paste(tile,((k%2)*480,(k//2)*390))
        sheet.save(artifacts/f'blind-gt-{start//8+1}.jpg')
    return {'dataset_digest':dataset['dataset_digest'],'selected':len(selected),'paired':len(images),'components':len(groups),'cross_split_components':audit['cross_split_components'],'orphan_labels':len(orphans)}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--archive',required=True);p.add_argument('--output',required=True);p.add_argument('--artifacts',required=True);a=p.parse_args()
    print(json.dumps(curate(a.archive,a.output,a.artifacts)))
