from pathlib import Path
import av,json,hashlib,csv,xml.etree.ElementTree as E,zipfile,pickletools,collections
from PIL import Image,ImageDraw
r=Path('_WORK/W2-06_evidence');records=[]
for p in r.glob('*.mp4'):
 root=E.parse(p.with_suffix('.xml')).getroot();ann={int(f.findtext('frameNumber')):[list(map(int,a.text.split())) for a in f.find('annotations').findall('_')] for f in root.find('frames')}; c=av.open(str(p));s=c.streams.video[0];fs=[];pts=[];bad=[]
 for f in c.decode(video=0):
  idx=len(fs); im=f.to_image();d=ImageDraw.Draw(im)
  for x,y,w,h in ann.get(idx,[]):
   if not(0<=x<x+w<=im.width and 0<=y<y+h<=im.height):bad.append(idx)
   d.rectangle((x,y,x+w,y+h),outline='lime',width=2)
  fs.append(im.resize((160,90)));pts.append({'frame':idx,'pts':f.pts,'time_base':str(f.time_base),'seconds':float(f.pts*f.time_base)})
 c.close()
 for st in range(0,len(fs),150):
  sheet=Image.new('RGB',(1600,1650),'white');d=ImageDraw.Draw(sheet)
  for k,im in enumerate(fs[st:st+150]):
   x=(k%10)*160;y=(k//10)*110;sheet.paste(im,(x,y));d.text((x,y+90),str(st+k),fill='black')
  sheet.save(r/f'{p.stem}_{st:04d}.jpg',quality=80)
 with (r/(p.stem+'_pts.csv')).open('w',newline='') as h:w=csv.DictWriter(h,fieldnames=pts[0]);w.writeheader();w.writerows(pts)
 records.append({'file':p.name,'width':s.width,'height':s.height,'codec':s.codec_context.name,'average_rate':str(s.average_rate),'time_base':str(s.time_base),'frames':len(fs),'first':pts[0],'last':pts[-1],'decode':'EOF no exception','xml_rate':root.findtext('frameRate'),'xml_frames':len(ann),'xml_first_last':[min(ann),max(ann)],'xml_empty':sum(not a for a in ann.values()),'xml_nonempty':sum(bool(a) for a in ann.values()),'xml_outside':bad,'xml_missing':sorted(set(range(len(fs)))-set(ann)),'xml_extra':sorted(set(ann)-set(range(len(fs))))})
(r/'decode_manifest.json').write_text(json.dumps(records,indent=2));print(json.dumps(records,indent=2))
result={}
for p in r.glob('*_best.pt'):
 with zipfile.ZipFile(p) as z:
  entry=next(i for i in z.infolist() if i.filename.endswith('data.pkl'));assert entry.file_size<1048576;b=z.read(entry);ops=list(pickletools.genops(b))
  with (r/(p.stem+'_dis.txt')).open('w',encoding='utf8') as h:pickletools.dis(b,out=h)
  result[p.stem]={'zip_files':len(z.infolist()),'pickle_bytes':len(b),'globals':sorted(set(str(a) for o,a,pos in ops if o.name=='GLOBAL')),'strings':[a for o,a,pos in ops if o.name in ('BINUNICODE','SHORT_BINUNICODE') and isinstance(a,str) and (a in ('smoke','fire','version','license','date','imgsz','names','ultralytics.nn.tasks') or 'AGPL' in a or '8.' in a or '202' in a)]}
(r/'checkpoint_static.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
