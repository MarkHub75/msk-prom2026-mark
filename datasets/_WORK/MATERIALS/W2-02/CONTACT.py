from PIL import Image,ImageDraw
import pathlib
p=pathlib.Path('_WORK/MATERIALS/W2-02');fs=list(p.glob('overlay_*.jpg'))
for k in range(0,len(fs),4):
 out=Image.new('RGB',(1440,1050),'white');dr=ImageDraw.Draw(out)
 for i,f in enumerate(fs[k:k+4]):
  im=Image.open(f);im.thumbnail((710,480));x=(i%2)*720;y=(i//2)*525;out.paste(im,(x,y+30));dr.text((x,y),f.name,fill='black')
 out.save(p/('CONTACT'+str(k//4)+'.jpg'))

