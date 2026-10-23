import pathlib,json,hashlib,collections
from PIL import Image,ImageOps,ImageDraw
p=pathlib.Path('_WORK/MATERIALS/W2-09');rows=[];hs=collections.defaultdict(list);samples=[]
for f in (p/'SMOKER').rglob('*.jpg'):
 im=Image.open(f);im.load();h=hashlib.sha256(im.convert('RGB').tobytes()).hexdigest();hs[h].append(str(f));rows.append({'path':str(f.relative_to(p/'SMOKER')),'size':im.size,'pixel_sha256':h})
 if len(samples)<40 and 'notsmoking' in f.name.lower():samples.append((f.name,im.copy()))
(p/'DECODE.json').write_text(json.dumps({'decoded':len(rows),'dimensions':dict(collections.Counter(str(x['size']) for x in rows)),'pixel_duplicate_groups':[x for x in hs.values() if len(x)>1],'rows':rows},indent=2),encoding='utf8')
can=Image.new('RGB',(1000,1200),'white');d=ImageDraw.Draw(can)
for i,(n,im) in enumerate(samples):
 x=i%5*200;y=i//5*150;can.paste(ImageOps.contain(im,(195,125)),(x,y));d.text((x,y+125),n,fill='black')
can.save(p/'NOTSMOKING_CONTACT.jpg');print('decoded',len(rows),'duplicate_groups',len([x for x in hs.values() if len(x)>1]))
