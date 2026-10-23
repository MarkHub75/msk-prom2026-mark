import cv2,pathlib,json
from PIL import Image,ImageDraw
p=pathlib.Path('_WORK/W1_D12');c=cv2.VideoCapture(str(p/'charades_2RFLZ.mp4'));d={'fps':c.get(cv2.CAP_PROP_FPS),'frames':c.get(cv2.CAP_PROP_FRAME_COUNT),'width':c.get(cv2.CAP_PROP_FRAME_WIDTH),'height':c.get(cv2.CAP_PROP_FRAME_HEIGHT)};print(d);sheet=Image.new('RGB',(1280,1000),'white')
for i,t in enumerate([0,3,6,9,12,14]):
 c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read()
 if ok:
  im=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB));im.thumbnail((426,480));x=(i%3)*426;y=(i//3)*500;sheet.paste(im,(x,y+20));ImageDraw.Draw(sheet).text((x+10,y+3),str(t)+' seconds',fill='black')
sheet.save(p/'charades_contact.jpg');(p/'charades_decode.json').write_text(json.dumps(d,indent=2));c.release()
