import pathlib,json,collections,hashlib,requests,re
from PIL import Image,ImageDraw,ImageOps
p=pathlib.Path(__file__).parent;b=p/'EXTRACTED';rows=[];counts=collections.Counter();chosen={}
for f in sorted((b/'labels').rglob('*.txt')):
 vals=[list(map(float,x.split())) for x in f.read_text().splitlines() if x.strip()]; split=f.parent.name; ims=list((b/'images'/split).glob(f.stem+'.*'))
 for v in vals:counts[int(v[0])]+=1
 rows.append({'label':str(f.relative_to(b)),'images':[str(x.relative_to(b)) for x in ims],'boxes':vals})
 for cls in [5,6,7,8,9,10]:
  if cls not in chosen and any(v[0]==cls for v in vals) and ims:chosen[cls]=rows[-1]
can=Image.new('RGB',(1500,900),'white');d=ImageDraw.Draw(can)
for i,(cls,row) in enumerate(chosen.items()):
 im=Image.open(b/row['images'][0]).convert('RGB');dr=ImageDraw.Draw(im);w,h=im.size
 for v in row['boxes']:
  c,x,y,bw,bh=v; box=[(x-bw/2)*w,(y-bh/2)*h,(x+bw/2)*w,(y+bh/2)*h]; dr.rectangle(box,outline='red',width=3);dr.text((box[0],box[1]),str(int(c)),fill='red')
 x=i%3*500;y=i//3*450;can.paste(ImageOps.contain(im,(495,420)),(x,y));d.text((x,y+422),f"target={cls} {row['images'][0]}",fill='black')
can.save(p/'SEMANTIC_CONTACT.jpg');(p/'AUDIT.json').write_text(json.dumps({'counts':dict(counts),'labels':len(rows),'split_counts':dict(collections.Counter(pathlib.PurePath(x['label']).parts[1] for x in rows)),'missing_or_multiple_pairs':[r['label'] for r in rows if len(r['images'])!=1],'chosen':chosen,'zip_sha256':hashlib.sha256((p/'construction-ppe.zip').read_bytes()).hexdigest()},indent=2));print((p/'AUDIT.json').read_text()[:1200])
for name,id in [('Images','1zDdTd8GVOIGENYVEHGABEFLUqBjnCzeS'),('Labels','17VMS2-EQAuB6CsCVDK5ScmxjrP-B2cgW')]:
 u='https://drive.google.com/drive/folders/'+id;r=requests.get(u,timeout=40);(p/('PICTOR_'+name+'.html')).write_bytes(r.content);print(name,r.status_code,len(r.content))
 html=r.text
 for m in re.finditer('data-id=',html):
  chunk=html[m.start():m.start()+500]
  if 'aria-label=' in chunk:print(chunk[:250])
