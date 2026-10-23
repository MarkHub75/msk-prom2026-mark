import av,pathlib,json
from PIL import Image,ImageDraw
p=pathlib.Path('_WORK/W1_D12');c=av.open(str(p/'charades_2RFLZ.mp4'));s=c.streams.video[0];d={'fps':str(s.average_rate),'frames':s.frames,'width':s.width,'height':s.height,'duration_seconds':float(s.duration*s.time_base)};print(d);sheet=Image.new('RGB',(1280,1000),'white');wanted=[0,3,6,9,12,14];i=0
for f in c.decode(video=0):
 t=float(f.pts*f.time_base)
 if i<len(wanted) and t>=wanted[i]:
  im=f.to_image();im.thumbnail((426,480));x=(i%3)*426;y=(i//3)*500;sheet.paste(im,(x,y+20));ImageDraw.Draw(sheet).text((x+10,y+3),f'{t:.3f} seconds',fill='black');i+=1
sheet.save(p/'charades_contact.jpg');(p/'charades_decode.json').write_text(json.dumps(d,indent=2));c.close()
