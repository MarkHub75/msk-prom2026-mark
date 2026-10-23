import av, json, hashlib, shutil
from pathlib import Path
from PIL import Image,ImageDraw
import xml.etree.ElementTree as ET
P=Path('_WORK/W2_03_EVIDENCE')
ns={'v':'http://lamp.cfar.umd.edu/viper#','d':'http://lamp.cfar.umd.edu/viperdata#'}
def cx(path):
 r=ET.parse(path).getroot(); d={}
 for f in r.findall('frame'):
  d[int(f.attrib['number'])]=[(o.attrib['id'],o.find('box').attrib,o.findtext('.//movement')) for o in f.findall('./objectlist/object')]
 return d
def bx(path):
 r=ET.parse(path).getroot();d={}
 for o in r.findall('.//v:object',ns):
  for b in o.findall('.//d:bbox',ns):
   a,z=map(int,b.attrib['framespan'].split(':'))
   for f in range(a,z+1):d.setdefault(f,[]).append((o.attrib['id'],b.attrib,'bbox'))
 return d
configs=[('caviarrun',Path('_WORK/M04/caviarrun.mpg'),cx('_WORK/M04/runxml.txt'),[0,21,22,174,372,373,384,385,410,436,437,489,490,550],False),('caviarwalk',Path('_WORK/M04/caviarwalk.mpg'),cx('_WORK/M04/walkxml.txt'),[0,17,39,63,100,101,236,444,475,610],False),('behave',Path('_WORK/D11/35450-47160.avi'),bx('_WORK/D11/35450-47160F.xgtf'),[41829,41850,44381,44396,44400,44401,44425,44447,44448,46306,46334,46360,46375,46376,46600],True)]
manifest={}
for name,path,labels,keys,behave in configs:
 origin=35450 if behave else 0
 targets=set(k-origin+d for k in keys for d in [-5,-1,0,1,5]);frames={};pts=[]
 c=av.open(str(path));s=c.streams.video[0]
 for i,f in enumerate(c.decode(video=0)):
  pts.append({'index0':i,'pts':f.pts,'time_base':str(f.time_base),'time':f.time})
  if i in targets:frames[i]=f.to_image()
 meta={'file':str(path),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rate':str(s.average_rate),'time_base':str(s.time_base),'start_time':s.start_time,'decoded':len(pts),'xml_frames':len(labels),'pts':pts}
 (P/(name+'_clock.json')).write_text(json.dumps(meta,indent=2))
 manifest[name]={k:v for k,v in meta.items() if k!='pts'}
 # Each row is a fixed annotation frame, image changes by candidate decoder offset.
 for part in range(0,len(keys),5):
  selected=keys[part:part+5]; w,h=(640,480) if behave else (384,288)
  sheet=Image.new('RGB',(w*3,(h+34)*len(selected)),(20,20,20));dr=ImageDraw.Draw(sheet)
  for row,k in enumerate(selected):
   for col,off in enumerate([-1,0,1]):
    ix=k-origin+off
    if ix not in frames:continue
    im=frames[ix].copy();d=ImageDraw.Draw(im)
    for aid,b,lab in labels.get(k,[]):
     if behave:x,y,ww,hh=map(float,[b['x'],b['y'],b['width'],b['height']])
     else:ww,hh,x,y=map(float,[b['w'],b['h'],b['xc'],b['yc']]);x-=ww/2;y-=hh/2
     color=['red','lime','cyan','orange','magenta','yellow','white','pink'][int(aid)%8]
     d.rectangle((x,y,x+ww,y+hh),outline=color,width=2);d.text((x,max(0,y-12)),aid+':'+str(lab),fill=color)
    sheet.paste(im,(col*w,row*(h+34)+34));dr.text((col*w+3,row*(h+34)+3),f'{name} XML {k} decoded {ix} offset {off:+} scale '+('1' if behave else '1'),fill='white')
  sheet.save(P/(name+f'_offsets_{part//5}.jpg'),quality=93)
 # scale comparison at motion boundary
 k=44425 if behave else (410 if name=='caviarrun' else 63)
 w,h=frames[k-origin].size;sheet=Image.new('RGB',(w*3,h+30));dr=ImageDraw.Draw(sheet)
 for col,scale in enumerate([1,2,.5] if behave else [.5,1,2]):
  im=frames[k-origin].copy();d=ImageDraw.Draw(im)
  for aid,b,lab in labels.get(k,[]):
   if behave:x,y,ww,hh=map(float,[b['x'],b['y'],b['width'],b['height']])
   else:ww,hh,x,y=map(float,[b['w'],b['h'],b['xc'],b['yc']]);x-=ww/2;y-=hh/2
   x*=scale;y*=scale;ww*=scale;hh*=scale
   d.rectangle((x,y,x+ww,y+hh),outline='red',width=2);d.text((x,y),aid,fill='yellow')
  sheet.paste(im,(col*w,30));dr.text((col*w+3,3),f'{name} XML {k}, scale {scale}',fill='white')
 sheet.save(P/(name+'_scales.jpg'),quality=93)
(P/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2))

