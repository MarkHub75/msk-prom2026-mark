import av,csv,json,pathlib
from PIL import Image,ImageDraw
p=pathlib.Path(__file__).parent
c=av.open(str(p/'Camera_0000.mp4')); s=c.streams.video[0]
rows=[]; thumbs=[]
for i,f in enumerate(c.decode(s)):
 rows.append([i,f.pts,str(f.time_base),float(f.time),f.width,f.height])
 if i%30==0:
  im=f.to_image().resize((640,360));ImageDraw.Draw(im).text((5,5),f'frame={i} PTS={f.pts} t={float(f.time):.3f}',fill='yellow',stroke_width=1,stroke_fill='black'); thumbs.append(im)
with (p/'frame_pts.csv').open('w',newline='') as out:
 w=csv.writer(out);w.writerow(['decode_index','pts','time_base','time_seconds','width','height']);w.writerows(rows)
for st in range(0,len(thumbs),10):
 out=Image.new('RGB',(640*2,360*5))
 for j,im in enumerate(thumbs[st:st+10]):out.paste(im,((j%2)*640,(j//2)*360))
 out.save(p/f'timeline_{st:02d}_{st+9:02d}.jpg',quality=90)
meta=dict(codec=s.codec_context.name,frames=len(rows),stream_frames=s.frames,stream_duration=s.duration,time_base=str(s.time_base),average_rate=str(s.average_rate),first=rows[0],last=rows[-1],pts_strictly_increasing=all(b[1]>a[1] for a,b in zip(rows,rows[1:])),pts_deltas=sorted(set(b[1]-a[1] for a,b in zip(rows,rows[1:]))))
(p/'decode.json').write_text(json.dumps(meta,indent=2)); print(json.dumps(meta,indent=2))
