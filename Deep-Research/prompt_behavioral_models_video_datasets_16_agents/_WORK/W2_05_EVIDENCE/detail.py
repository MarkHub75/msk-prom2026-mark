import av,pathlib
from PIL import Image,ImageDraw
p=pathlib.Path(__file__).parent
ims=[]
for i,f in enumerate(av.open(str(p/'Camera_0000.mp4')).decode(video=0)):
 if 33*30<=i<42*30 and i%6==0:
  im=f.to_image().crop((0,0,1200,1080)).resize((400,360));ImageDraw.Draw(im).text((5,5),f't={float(f.time):.2f} PTS={f.pts}',fill='yellow',stroke_width=1,stroke_fill='black');ims.append(im)
for st in range(0,len(ims),15):
 out=Image.new('RGB',(1200,1800))
 for j,im in enumerate(ims[st:st+15]):out.paste(im,((j%3)*400,(j//3)*360))
 out.save(p/f'detail_{st//15}.jpg',quality=90)
