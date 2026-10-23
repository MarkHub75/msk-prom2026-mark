from pathlib import Path
import json,collections,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageOps
R=Path(__file__).parent
for num in ['04','05','06']:
 o=R/('MATERIALS/W2-'+num);d=o/'pairs';records=[];panels=[]
 if num=='04':
  co=json.loads((R/'MATERIALS/W1-03/SFCHD-SCALE/dataset_SFCHD/annotations/all_data.json').read_text());ims={x['file_name']:x for x in co['images']};aa=collections.defaultdict(list)
  for a in co['annotations']:aa[a['image_id']].append(a)
  cats={x['id']:x['name'] for x in co['categories']}
 for p in sorted(d.glob('*')):
  if p.suffix.lower() not in ['.jpg','.png']:continue
  im=Image.open(p).convert('RGB');w,h=im.size;boxes=[];decl=None
  if num=='04':
   a=ims[p.name];decl=[a['width'],a['height']]
   for x in aa[a['id']]:
    xx,y,bw,bh=x['bbox'];boxes.append((cats[x['category_id']],[xx,y,xx+bw,y+bh]))
  elif num=='05':
   root=ET.parse(d/(p.stem+'.xml')).getroot();decl=[int(root.findtext('size/width')),int(root.findtext('size/height'))]
   for x in root.findall('object'):boxes.append((x.findtext('name'),[float(x.findtext('bndbox/'+k)) for k in ['xmin','ymin','xmax','ymax']]))
  else:
   for l in (d/(p.stem+'.txt')).read_text().splitlines():
    c,x,y,bw,bh=map(float,l.split());boxes.append((['person','vest','blue','red','white','yellow'][int(c)],[(x-bw/2)*w,(y-bh/2)*h,(x+bw/2)*w,(y+bh/2)*h]))
  rec={'image':p.name,'decoded_wh':[w,h],'declared_wh':decl,'boxes':boxes};records.append(rec)
  fac=600/w;out=im.resize((600,round(h*fac)));dr=ImageDraw.Draw(out)
  for j,(c,b) in enumerate(boxes):
   col={'person':'red','hat':'lime','helmet':'lime','head':'yellow','self_clothes':'magenta','safety_clothes':'cyan','blur_head':'orange','blur_clothes':'white','vest':'cyan','blue':'blue','red':'magenta','white':'white','yellow':'yellow'}.get(c,'lime');bb=[v*fac for v in b];dr.rectangle(bb,outline=col,width=2);dr.text((bb[0],max(0,bb[1]-11)),c,fill=col,stroke_width=1,stroke_fill='black')
  out.save(o/(p.stem+'.overlay.jpg'));thumb=ImageOps.contain(out,(600,380));panel=Image.new('RGB',(600,410),'#202020');panel.paste(thumb,(0,20));ImageDraw.Draw(panel).text((4,2),p.name,fill='white');panels.append(panel)
 sheet=Image.new('RGB',(1200,410*((len(panels)+1)//2)),'#101010')
 for j,x in enumerate(panels):sheet.paste(x,((j%2)*600,(j//2)*410))
 sheet.save(o/'CONTACT.jpg');(o/'PAIRED_AUDIT.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8');print(num,len(records),collections.Counter(c for x in records for c,b in x['boxes']))
