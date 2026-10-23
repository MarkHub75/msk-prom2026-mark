import requests,json,pathlib,hashlib,av,zipfile,pickletools
from PIL import Image,ImageDraw
P=pathlib.Path(__file__).parent
s=requests.Session()
rev='7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5'
manifest=[]
for name in ['3_te1.mp4','7_te1.mp4']:
 u=f'https://huggingface.co/datasets/Voxel51/Safe_and_Unsafe_Behaviours/resolve/{rev}/data/{name}'
 f=P/name
 if not f.exists():
  r=s.get(u,timeout=90);r.raise_for_status();f.write_bytes(r.content)
 c=av.open(str(f));st=c.streams.video[0];pts=[];imgs=[]
 for i,fr in enumerate(c.decode(video=0)):
  pts.append(float(fr.pts*fr.time_base))
  if i%25==0:
   im=fr.to_image();im.thumbnail((640,360));imgs.append((i,pts[-1],im.copy()))
 sheet=Image.new('RGB',(1280,390*((len(imgs)+1)//2)), 'white');d=ImageDraw.Draw(sheet)
 for k,(i,t,im) in enumerate(imgs):
  x=(k%2)*640;y=(k//2)*390;sheet.paste(im,(x,y));d.text((x,y+363),f'{name} frame {i} PTS {t:.6f}',fill='black')
 sheet.save(P/(name+'.jpg'))
 manifest.append(dict(name=name,url=u,bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),frames=len(pts),pts=pts,width=st.width,height=st.height,time_base=str(st.time_base),average_rate=str(st.average_rate)))
 (P/'video_manifest.json').write_text(json.dumps(manifest,indent=2))
 print(name,manifest[-1]['sha256'],len(pts))
# Static inspection only: pickletools disassembly is not unpickling or torch.load.
mr='d8b594f321dd4c64eda16e435601fd266089fc32'
base=f'https://huggingface.co/keremberke/yolov8n-forklift-detection/resolve/{mr}/'
for name in ['README.md','config.json','best.pt']:
 r=s.get(base+name,timeout=90);r.raise_for_status();(P/name).write_bytes(r.content)
meta=s.get('https://huggingface.co/api/models/keremberke/yolov8n-forklift-detection',timeout=30).json();(P/'model_api.json').write_text(json.dumps(meta,indent=2))
with zipfile.ZipFile(P/'best.pt') as z:
 zi=z.infolist();(P/'checkpoint_zip.json').write_text(json.dumps([dict(name=x.filename,bytes=x.file_size,compressed=x.compress_size) for x in zi],indent=2))
 data=[x for x in zi if x.filename.endswith('data.pkl')][0]
 assert data.file_size<5000000
 b=z.read(data)
 with (P/'checkpoint_pickle_disassembly.txt').open('w',encoding='utf8') as out:pickletools.dis(b,out=out)
 print('checkpoint bytes/hash', (P/'best.pt').stat().st_size,hashlib.sha256((P/'best.pt').read_bytes()).hexdigest())
