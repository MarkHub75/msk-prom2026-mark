from PIL import Image,ImageOps,ImageDraw
import pathlib
p=pathlib.Path(__file__).parent
files=sorted(p.glob('*.mp4-*.jpg')); out=Image.new('RGB',(1200,180*((len(files)+3)//4)),'white');d=ImageDraw.Draw(out)
for i,f in enumerate(files):
 x=i%4*300;y=i//4*180;out.paste(ImageOps.contain(Image.open(f),(296,155)),(x,y));d.text((x,y+156),f.name,fill='black')
out.save(p/'CONTACT.jpg')
