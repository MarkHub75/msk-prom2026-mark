import rarfile,pathlib,io,json,hashlib,collections
from PIL import Image,ImageOps,ImageDraw
p=pathlib.Path('_WORK/MATERIALS/W2-09');r=rarfile.RarFile('_WORK/MATERIALS/W1-06/Smoker Detection.rar');print(collections.Counter(x.compress_type for x in r.infolist()))
print('dll',list(pathlib.Path('C:/Program Files/7-Zip').glob('*')))
try:
 import libarchive
 rows=[];hashes=collections.defaultdict(list);samples=[]
 with libarchive.file_reader(str(r.filename)) as ar:
  for en in ar:
   if not en.pathname.lower().endswith('.jpg'):continue
   b=b''.join(en.get_blocks());im=Image.open(io.BytesIO(b));im.load();h=hashlib.sha256(im.convert('RGB').tobytes()).hexdigest();hashes[h].append(en.pathname);rows.append({'path':en.pathname,'size':im.size,'sha256_pixels':h})
   if len(samples)<40 and ('notsmoking' in en.pathname.lower()):samples.append((en.pathname,im.copy()))
 (p/'DECODE.json').write_text(json.dumps({'rows':rows,'decoded':len(rows),'dimensions':dict(collections.Counter(str(x['size']) for x in rows)),'pixel_duplicate_groups':[x for x in hashes.values() if len(x)>1]},indent=2),encoding='utf8')
 canvas=Image.new('RGB',(1000,1200),'white');d=ImageDraw.Draw(canvas)
 for i,(n,im) in enumerate(samples):
  x=(i%5)*200;y=(i//5)*150;canvas.paste(ImageOps.contain(im,(195,125)),(x,y));d.text((x,y+125),n.split('/')[-1][:28],fill='black')
 canvas.save(p/'NOTSMOKING_CONTACT.jpg');print('decoded',len(rows))
except Exception as e: print(type(e).__name__,str(e))
