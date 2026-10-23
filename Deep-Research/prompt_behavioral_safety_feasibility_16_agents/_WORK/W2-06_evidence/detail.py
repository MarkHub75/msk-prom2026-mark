from pathlib import Path
import av,xml.etree.ElementTree as E
from PIL import Image,ImageDraw
r=Path('_WORK/W2-06_evidence')
for stem,idxs in [('Car1',[0,245,246,378,379,442,443,629]),('barbecue',[595,596,602,603,638,639,640,641,642]),('non_fire_patrolbot_onboard',[239,240,241,242,243,244,245])]:
 root=E.parse(r/(stem+'.xml')).getroot();ann={int(f.findtext('frameNumber')):[list(map(int,a.text.split())) for a in f.find('annotations').findall('_')] for f in root.find('frames')};c=av.open(str(r/(stem+'.mp4')));sheet=Image.new('RGB',(1280,((len(idxs)+1)//2)*390),'white');d=ImageDraw.Draw(sheet)
 for i,f in enumerate(c.decode(video=0)):
  if i not in idxs:continue
  im=f.to_image();z=ImageDraw.Draw(im)
  for x,y,w,h in ann[i]:z.rectangle((x,y,x+w,y+h),outline='lime',width=3)
  k=idxs.index(i);x=(k%2)*640;y=(k//2)*390;sheet.paste(im.resize((640,360)),(x,y));d.text((x,y+361),f'{stem} frame {i} / {float(f.pts*f.time_base):.6f}s / {ann[i]}',fill='black')
 c.close();sheet.save(r/(stem+'_detail.jpg'),quality=90)
