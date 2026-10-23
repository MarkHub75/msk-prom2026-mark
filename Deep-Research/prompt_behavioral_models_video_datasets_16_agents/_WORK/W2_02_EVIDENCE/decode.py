from pathlib import Path
import av,csv,json,hashlib
from PIL import Image,ImageDraw
E=Path('_WORK/W2_02_EVIDENCE');out=[]
labels=list(csv.DictReader(open('_WORK/W1_M03_EVIDENCE/hf_labels_GMDCSA24.csv')))
sync={int(r[0]):int(r[1]) for r in csv.reader(open('_WORK/evidence_D10/adl-10-data.csv'))}
post={int(r[1]):int(r[2]) for r in csv.reader(open('_WORK/evidence_D10/urfall-cam0-adls.csv')) if r[0]=='adl-10'}
for name,key in [('S1_F11','Subject_1/Fall/11'),('S3_A08','Subject_3/ADL/08'),('S4_F01','Subject_4/Fall/01'),('adl-10-cam0',None)]:
 c=av.open(str(E/(name+'.mp4')));s=c.streams.video[0]; frames=list(c.decode(video=0)); rows=[]
 selected=[x for x in labels if x['path']==key]
 for i,f in enumerate(frames):
  t=float(f.pts*f.time_base); rel=float((f.pts-(s.start_time or 0))*f.time_base);active=[r['label'] for r in selected if float(r['start'])<=rel<float(r['end'])]
  rows.append(dict(index0=i,ordinal1=i+1,pts=f.pts,time_base=str(f.time_base),seconds=t,relative_seconds=rel,duration=f.duration,labels='|'.join(active),sync_ms=sync.get(i+1,'') if not key else '',posture=post.get(i+1,'') if not key else ''))
 with open(E/(name+'_pts_join.csv'),'w',newline='') as o:w=csv.DictWriter(o,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 entry=dict(name=name,path=key,sha256=hashlib.sha256((E/(name+'.mp4')).read_bytes()).hexdigest(),n=len(frames),width=s.width,height=s.height,codec=s.codec_context.name,time_base=str(s.time_base),average_rate=str(s.average_rate),stream_start=s.start_time,stream_duration=s.duration,container_duration=c.duration,first=rows[0],last=rows[-1],strictly_increasing=all(rows[i]['pts']<rows[i+1]['pts'] for i in range(len(rows)-1)),segments=selected)
 out.append(entry)
 def sheets(indices,tag):
  for page in range(0,len(indices),40):
   ix=indices[page:page+40]; im=Image.new('RGB',(5*300,8*192),'white');d=ImageDraw.Draw(im)
   for j,i in enumerate(ix):
    f=frames[i];pic=f.to_image();pic.thumbnail((300,164));x=(j%5)*300;y=(j//5)*192;im.paste(pic,(x,y));r=rows[i];tx=f"f{i} t={r['seconds']:.4f} rel={r['relative_seconds']:.3f} L={r['labels']}"
    if not key:tx+=f" p={r['posture']} s={r['sync_ms']}"
    d.text((x+2,y+165),tx,fill='black')
   im.save(E/(name+'_'+tag+f'_{page//40:02}.jpg'),quality=88)
 # 5fps uniform review entire available duration
 indices=[];prev=-1
 for i,r in enumerate(rows):
  bucket=int(r['seconds']*5)
  if bucket!=prev:indices.append(i);prev=bucket
 if len(frames)-1 not in indices:indices.append(len(frames)-1)
 sheets(indices,'whole5fps')
 # every decoded frame in a bounded transition interval
 limits={'S1_F11':(.4,2.9),'S3_A08':(2.9,4.1),'S4_F01':(1.05,2.65),'adl-10-cam0':(5.2,7.1)}[name]
 sheets([i for i,r in enumerate(rows) if limits[0]<=r['seconds']<=limits[1]],'transition_allframes')
(E/'decode_manifest.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
print('sync',len(sync),min(sync),max(sync),sync[max(sync)],'post',len(post),min(post),max(post))
