import pathlib,json,collections,re,requests,hashlib
from PIL import Image,ImageDraw,ImageOps
p=pathlib.Path(__file__).parent;out={};allrows={}
for f in sorted(p.glob('pictor*.txt')):
 lines=[x for x in f.read_text().splitlines() if x.strip()]; rows=[]
 for line in lines:
  t=line.split();rows.append({'image':t[0],'boxes':[list(map(int,x.split(','))) for x in t[1:]]})
 out[f.name]={'images':len(rows),'unique_names':len(set(r['image'] for r in rows)),'boxes':sum(len(r['boxes']) for r in rows),'class_counts':dict(collections.Counter(str(b[-1]) for r in rows for b in r['boxes'])),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()};allrows[f.name]=rows
h=(p/'PICTOR_Images.html').read_text(encoding='utf8');h=re.sub(r'\\x([0-9a-fA-F]{2})',lambda m:chr(int(m[1],16)),h)
names=re.findall(r'\["([A-Za-z0-9_-]+)",\["1zDdTd8GVOIGENYVEHGABEFLUqBjnCzeS"\],"([^"]+\.jpg)"',h)
row=allrows['pictor_ppe_crowdsourced_approach-01_train.txt'][0];id,name=next((id,name) for id,name in names if name==row['image']);r=requests.get('https://drive.google.com/uc',params={'export':'download','id':id},timeout=40);(p/name).write_bytes(r.content)
im=Image.open(p/name).convert('RGB');dr=ImageDraw.Draw(im)
for b in row['boxes']:dr.rectangle(b[:4],outline=['red','blue','yellow'][b[-1]],width=3);dr.text((b[0],b[1]),str(b[-1]),fill='red')
im.save(p/'PICTOR_OVERLAY.jpg');out['sample']={'file':name,'id':id,'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest(),'dimensions':im.size,'row':row,'geometry_interpretation':'raw integer x1,y1,x2,y2,class; confirmed visually for this sample only'}
(p/'PICTOR_AUDIT.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2)[:5000])
