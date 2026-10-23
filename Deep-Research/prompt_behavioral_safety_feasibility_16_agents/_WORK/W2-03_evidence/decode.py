from pathlib import Path
import av,json,hashlib,csv
from PIL import Image,ImageDraw
r=Path('_WORK/W2-03_evidence'); paths=list(r.glob('*.mp4'))+list(Path('_WORK/W1-09_samples').glob('*.mp4')); records=[]
for p in paths:
 c=av.open(str(p)); s=c.streams.video[0]; fs=[]; pts=[]; durations=[]; codec=s.codec_context.name
 for f in c.decode(video=0):
  pts.append({'frame':len(pts),'pts':f.pts,'time_base':str(f.time_base),'seconds':float(f.pts*f.time_base),'duration':f.duration})
  fs.append(f.to_image().resize((192,108)))
 assert all(b['seconds']>a['seconds'] for a,b in zip(pts,pts[1:])); c.close()
 with (r/(p.stem+'_pts.csv')).open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=pts[0]);w.writeheader();w.writerows(pts)
 for st in range(0,len(fs),80):
  sub=fs[st:st+80]; sheet=Image.new('RGB',(1536,1280),'white'); d=ImageDraw.Draw(sheet)
  for k,im in enumerate(sub):
   x=(k%8)*192;y=(k//8)*128;sheet.paste(im,(x,y));d.text((x,y+109),f'{st+k} | {pts[st+k]["seconds"]:.4f}s',fill='black')
  sheet.save(r/f'{p.stem}_frames_{st:03d}.jpg',quality=87)
 steps=[b['seconds']-a['seconds'] for a,b in zip(pts,pts[1:])]
 records.append(dict(local=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,codec=codec,width=s.width,height=s.height,time_base=str(s.time_base),stream_duration=s.duration,average_rate=str(s.average_rate),decoded_frames=len(fs),first_pts=pts[0]['seconds'],last_pts=pts[-1]['seconds'],min_step=min(steps),max_step=max(steps),decode='complete to EOF; no exception',pts_csv=p.stem+'_pts.csv',review='all-frame sheets; no temporal subsampling'))
(r/'decode_manifest.json').write_text(json.dumps(records,indent=2)); print(json.dumps(records,indent=2))
