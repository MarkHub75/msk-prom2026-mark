import av,pathlib,json,xml.etree.ElementTree as ET,re,collections
from PIL import Image,ImageDraw
p=pathlib.Path('_WORK/D11'); c=av.open(str(p/'35450-47160.avi'));s=c.streams.video[0]
info=dict(codec=s.codec_context.name,width=s.width,height=s.height,avg_rate=str(s.average_rate),time_base=str(s.time_base),declared_frames=s.frames,duration=s.duration)
indices=[0,6383,8946,9000,9035,10856,10925]; ims=[];n=0; pts=[]
for n,f in enumerate(c.decode(video=0)):
 if n in indices:
  im=f.to_image().convert('RGB');ImageDraw.Draw(im).text((5,5),f'decode_index={n}; hypothesis global={35450+n}',fill='yellow');ims.append(im);pts.append([n,f.pts,str(f.time)])
info.update(decoded_frames=n+1,samples=pts)
root=ET.parse(p/'35450-47160F.xgtf').getroot();ns={'v':'http://lamp.cfar.umd.edu/viper#','d':'http://lamp.cfar.umd.edu/viperdata#'}
info['xml_objects']=[o.attrib for o in root.findall('.//v:object',ns)];info['bbox_examples']=[b.attrib for b in root.findall('.//d:bbox',ns)[:3]]
board=Image.new('RGB',(640*2,480*4));
for k,im in enumerate(ims):board.paste(im.resize((640,480)),((k%2)*640,(k//2)*480))
board.save(p/'behave_contact.jpg');(p/'behave_decode.json').write_text(json.dumps(info,indent=2));print(json.dumps(info,indent=2))
