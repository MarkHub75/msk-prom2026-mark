import pathlib,json,zipfile,collections,hashlib,math,re,requests,concurrent.futures,time
R=pathlib.Path(__file__).parent
def out(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
def sf():
 b=R/'MATERIALS/W1-03/SFCHD-SCALE/dataset_SFCHD';o=R/'MATERIALS/W2-03';o.mkdir(parents=True,exist_ok=True)
 d=json.loads((b/'annotations/all_data.json').read_text());v=json.loads((b/'annotations/val.json').read_text());ims={x['id']:x for x in d['images']};aa=collections.defaultdict(list)
 for a in d['annotations']:aa[a['image_id']].append(a)
 z=zipfile.ZipFile(b/'labels.zip');zz={pathlib.Path(n).stem:n for n in z.namelist() if n.endswith('.txt')};mis=[];bad=[];maxerr=0;matched=0;empty=[]
 for i,im in ims.items():
  stem=pathlib.Path(im['file_name']).stem;w,h=im['width'],im['height'];expected=[]
  for a in aa[i]:
   x,y,bw,bh=a['bbox'];expected.append([a['category_id'],(x+bw/2)/w,(y+bh/2)/h,bw/w,bh/h])
   if x<0 or y<0 or bw<=0 or bh<=0 or x+bw>w+1e-6 or y+bh>h+1e-6:bad.append({'image':im['file_name'],'annotation':a})
  if stem not in zz:
   mis.append({'image':im['file_name'],'reason':'missing TXT','n_coco':len(expected)});(o/(stem+'.candidate.txt')).write_text('\n'.join(' '.join([str(a[0])]+[format(q,'.10g') for q in a[1:]]) for a in expected)+'\n');continue
  rows=[[float(x) for x in l.split()] for l in z.read(zz[stem]).decode().splitlines() if l.strip()]
  if not rows:empty.append(stem)
  left=list(rows);errs=[]
  for a in expected:
   candidates=[(max(abs(x-y) for x,y in zip(a[1:],q[1:])),j) for j,q in enumerate(left) if len(q)==5 and q[0]==a[0]]
   if not candidates:errs.append({'missing':a});continue
   err,j=min(candidates);maxerr=max(maxerr,err)
   if err>1e-5:errs.append({'coco':a,'yolo':left[j],'max_normalized_error':err})
   left.pop(j);matched+=1
  if errs or left:mis.append({'image':im['file_name'],'errors':errs,'extra_yolo':left})
 splits={s:[pathlib.PurePosixPath(x.strip()).name for x in (b/f'new_split_yolo/{s}.txt').read_text().splitlines() if x.strip()] for s in ['train','val','test']}
 sv=set(splits['val']);vc={x['file_name'] for x in v['images']};ad={a['id']:a for a in d['annotations']};va=[a for a in v['annotations'] if ad.get(a['id'])!=a]
 groups=collections.defaultdict(collections.Counter)
 for s,ns in splits.items():
  for n in ns:groups[re.sub(r'_\d+$','',pathlib.Path(n).stem)][s]+=1
 out(o/'AUDIT.json',{'categories':d['categories'],'images':len(ims),'image_unique_ids':len(ims),'unique_names':len({x['file_name'] for x in ims.values()}),'annotations':len(ad),'duplicate_annotation_ids':len(d['annotations'])-len(ad),'invalid_geometry':bad,'empty_coco':sum(not aa[i] for i in ims),'empty_yolo':empty,'compared_boxes':matched,'tolerance_normalized':1e-5,'max_coordinate_error':maxerr,'mismatches':mis,'val_name_set_difference':sorted(sv^vc),'val_annotation_record_mismatches':va,'test_membership':{n:{s:n in splits[s] for s in ['train','val']} for n in splits['test']},'split_counts':{s:len(ns) for s,ns in splits.items()},'group_rule':'remove final _integer from basename; inferred run, not camera','inferred_runs':groups,'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [b/'annotations/all_data.json',b/'annotations/val.json',b/'labels.zip']}})
 out(R/'MATERIALS/W2-04/RUN_GROUPS.json',groups)
 print('SF',len(mis),len(bad),maxerr,len(groups),flush=True)
def routes():
 for num,id in [('04','1-2z7r3J4sZdLvVt5mllvSEwAFO49Y-zj'),('05','1qWm7rrwvjAWs1slymbrLaCf7Q-wnGLEX'),('06','1fdGn67W0B7ShpBDbbQpUF0ScPQa4DR0a')]:
  o=R/f'MATERIALS/W2-{num}';o.mkdir(parents=True,exist_ok=True);logs=[]
  for name,url in [('view',f'https://drive.google.com/file/d/{id}/view'),('download',f'https://drive.usercontent.google.com/download?id={id}&export=download&confirm=t')]:
   try:
    q=requests.get(url,timeout=40,stream=True);body=next(q.iter_content(150000),b'');(o/f'drive-{name}.bin').write_bytes(body);logs.append({'url':url,'status':q.status_code,'headers':dict(q.headers),'saved_prefix_bytes':len(body),'final_url':q.url});q.close()
   except Exception as e:logs.append({'url':url,'error':str(e)})
  out(o/'ACCESS.json',logs);print(num,[(x.get('status'),x.get('saved_prefix_bytes')) for x in logs],flush=True)
def shel():
 o=R/'MATERIALS/W2-07';o.mkdir(parents=True,exist_ok=True);m=json.loads((R/'MATERIALS/W1-15/shel-Annotations-manifest.json').read_text());dest=o/'XML';dest.mkdir(exist_ok=True)
 def get(a):
  p=dest/a['filename'];url=a['content_details']['download_url']
  if p.exists():b=p.read_bytes()
  else:
   try:
    q=requests.get(url,timeout=35);q.raise_for_status();b=q.content;p.write_bytes(b)
   except Exception as e:return {'file':a['filename'],'error':str(e)}
  return {'file':a['filename'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'hash_match':hashlib.sha256(b).hexdigest()==a['content_details']['sha256_hash']}
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
  logs=[]
  for i,r in enumerate(ex.map(get,m)):
   logs.append(r)
   if i%100==0:out(o/'DOWNLOAD_LOG.json',logs);print('XML',i,flush=True)
 out(o/'DOWNLOAD_LOG.json',logs)
if __name__=='__main__':
 import sys
 {'sf':sf,'routes':routes,'shel':shel}[sys.argv[1]]()
