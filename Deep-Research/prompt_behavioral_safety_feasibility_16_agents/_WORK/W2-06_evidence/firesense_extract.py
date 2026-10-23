import requests,pathlib,json,struct,zlib,hashlib,av,csv
from PIL import Image,ImageDraw
r=pathlib.Path('_WORK/W2-06_evidence');u='https://zenodo.org/api/records/836749/files/fire_videos.1406.zip/content';members=json.loads((r/'firesense_members.json').read_text());recs=[]
def rng(a,b):
 q=requests.get(u,headers={'Range':f'bytes={a}-{b}'},stream=True,timeout=30)
 assert q.status_code==206
 z=q.raw.read(b-a+2);assert len(z)==b-a+1;q.close();return z
for name in ['pos/posVideo11.870.avi','neg/negsVideo2.859.avi']:
 m=next(x for x in members if x['name']==name);a=m['offset'];h=rng(a,a+29);v=struct.unpack_from('<5H3I2H',h,4);start=a+30+v[-2]+v[-1];comp=rng(start,start+m['compressed']-1);raw=zlib.decompress(comp,-15);assert len(raw)==m['uncompressed'] and zlib.crc32(raw)==m['crc32'];p=r/pathlib.Path(name).name;p.write_bytes(raw)
 c=av.open(str(p));s=c.streams.video[0];pts=[];fs=[]
 for f in c.decode(video=0):pts.append({'frame':len(fs),'pts':f.pts,'time_base':str(f.time_base),'seconds':float(f.pts*f.time_base)});fs.append(f.to_image().resize((160,120)))
 for st in range(0,len(fs),100):
  sheet=Image.new('RGB',(1600,1400),'white');d=ImageDraw.Draw(sheet)
  for k,im in enumerate(fs[st:st+100]):x=k%10*160;y=k//10*140;sheet.paste(im,(x,y));d.text((x,y+120),str(st+k),fill='black')
  sheet.save(r/f'{p.stem}_{st:04d}.jpg',quality=80)
 with (r/(p.stem+'_pts.csv')).open('w',newline='') as h:w=csv.DictWriter(h,fieldnames=pts[0]);w.writeheader();w.writerows(pts)
 recs.append({**m,'url':u,'payload_range':[start,start+m['compressed']-1],'sha256':hashlib.sha256(raw).hexdigest(),'decoded_frames':len(fs),'width':s.width,'height':s.height,'rate':str(s.average_rate),'codec':s.codec_context.name,'first':pts[0],'last':pts[-1],'decode':'complete EOF; no exception','crc32':'verified'});c.close()
q=requests.get('https://zenodo.org/api/records/836749',timeout=30);(r/'firesense_record.json').write_bytes(q.content)
(r/'firesense_acquired.json').write_text(json.dumps(recs,indent=2));print(json.dumps(recs,indent=2))
