import pathlib,json,collections,requests,datetime,hashlib
p=pathlib.Path('_WORK/W1_M05');d=json.loads((p/'hico_annotations.txt').read_text());corr=[{'hoi':h,'object':o,'verb':v,'verb_name':d['verbs'][v]} for h,o,v in d['correspondence'] if o==67];print('phone_correspondence',corr)
counts=collections.Counter(); ims=collections.defaultdict(set)
for i,a in enumerate(d['annotation']):
 for h,o,v in zip(a['hoi'],a['object'],a['verb']):
  if o==67:counts[v]+=1;ims[v].add(d['filenames'][i])
summary={'phone_correspondence':corr,'train_phone_pair_label_counts':{d['verbs'][v]:n for v,n in counts.items()},'train_phone_image_counts':{d['verbs'][v]:len(x) for v,x in ims.items()},'all_annotation_images':len(d['annotation']),'example92':d['annotation'][91]};print(summary);(p/'phone_hico_counts.json').write_text(json.dumps(summary,indent=2))
u='https://download.openmmlab.com/mmaction/v1.0/detection/slowfast/slowfast_kinetics400-pretrained-r50_8xb6-8x8x1-cosine-10e_ava22-rgb/slowfast_kinetics400-pretrained-r50_8xb6-8x8x1-cosine-10e_ava22-rgb_20220906-d934a48f.pth';r=requests.head(u,timeout=25);print('AVA WEIGHT',r.status_code,r.headers.get('content-length'));(p/'ava_weight_head.json').write_text(json.dumps({'url':u,'status':r.status_code,'headers':dict(r.headers),'time':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
