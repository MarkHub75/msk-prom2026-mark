import av,pathlib,json
from PIL import Image,ImageDraw
p=pathlib.Path('_WORK/W2_04_EVIDENCE');c=av.open('_WORK/W1_D12/charades_2RFLZ.mp4');want=[38,55,70,77,91,123,134,145];sheet=Image.new('RGB',(1920,620),'white');d=ImageDraw.Draw(sheet)
for ix,f in enumerate(c.decode(video=0)):
 if ix in want:
  k=want.index(ix);x=k%4*480;y=k//4*310;sheet.paste(f.to_image(),(x,y+38));t=float(f.pts*f.time_base);d.text((x+5,y+3),f'frame {ix}; source PTS {t:.4f}s',fill='black');d.text((x+5,y+18),'Original CSV c019 [3.0,10.4]; NO actor/phone boxes',fill='black')
sheet.save(p/'native_review.jpg',quality=98)
