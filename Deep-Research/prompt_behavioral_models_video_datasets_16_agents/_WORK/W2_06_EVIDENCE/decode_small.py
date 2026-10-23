import pathlib,av,json,hashlib
from PIL import Image,ImageDraw
p=pathlib.Path('_WORK/W2_06_EVIDENCE');f=next((p/'small_video').rglob('*.mp4'));c=av.open(str(f));s=c.streams.video[0];info={'file':str(f),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'time_base':str(s.time_base),'average_rate':str(s.average_rate),'duration':s.duration,'metadata':dict(s.metadata),'frames_declared':s.frames,'width':s.width,'height':s.height};selected=[];frames=[]
for n,fr in enumerate(c.decode(s)):
 frames.append({'n':n,'pts':fr.pts,'time_base':str(fr.time_base),'seconds':float(fr.pts*fr.time_base) if fr.pts is not None else None})
 if n in [0,30,100,200,400,800]:selected.append((n,fr.to_image().resize((640,360))))
info['decoded_frames']=len(frames);info['first']=frames[0];info['last']=frames[-1];(p/'small_video_decode.json').write_text(json.dumps(info,indent=2));(p/'small_video_pts.json').write_text(json.dumps(frames));sheet=Image.new('RGB',(1280,400*((len(selected)+1)//2)),(250,250,250));d=ImageDraw.Draw(sheet)
for k,(n,im) in enumerate(selected):x=(k%2)*640;y=(k//2)*400;sheet.paste(im,(x,y));d.text((x+8,y+365),str(n),fill='black')
sheet.save(p/'small_video_contact.jpg');print(json.dumps(info,indent=2))
