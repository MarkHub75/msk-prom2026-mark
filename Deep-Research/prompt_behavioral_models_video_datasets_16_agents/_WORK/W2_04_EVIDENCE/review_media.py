import json,re,pathlib,av,hashlib
from PIL import Image,ImageDraw
from bs4 import BeautifulSoup
p=pathlib.Path('_WORK/W2_04_EVIDENCE');res=[]
for i in (1,2):
 t=p.joinpath(f'http_{i}.html').read_text(encoding='utf8');m=re.search(r'ytInitialPlayerResponse\s*=\s*(\{.*?\});',t)
 if m:
  j=json.loads(m.group(1));res.append({'case':i,'playabilityStatus':j.get('playabilityStatus'),'videoDetails':j.get('videoDetails'),'streamingData_keys':list(j.get('streamingData',{}))});p.joinpath(f'player_{i}.json').write_text(json.dumps(res[-1],indent=2))
 else:res.append({'case':i,'player_response_found':False,'phrases':re.findall('.{0,70}(?:unavailable|Sign in|LOGIN_REQUIRED).{0,100}',t)[:10]})
for i in (0,3):p.joinpath(f'page_{i}.txt').write_text(BeautifulSoup(p.joinpath(f'http_{i}.html').read_bytes(),'html.parser').get_text(' ',strip=True),encoding='utf8')
print(json.dumps(res,indent=2)[:10000])
fpath=pathlib.Path('_WORK/W1_D12/charades_2RFLZ.mp4');c=av.open(str(fpath));s=c.streams.video[0];frames=[];records=[]
for ix,f in enumerate(c.decode(video=0)):
 frames.append(f.to_image());records.append({'index':ix,'pts':f.pts,'time_base':str(f.time_base),'source_seconds':float(f.pts*f.time_base)})
for start in range(0,len(frames),56):
 sheet=Image.new('RGB',(1920,8*164),'white');d=ImageDraw.Draw(sheet)
 for ix in range(start,min(start+56,len(frames))):
  im=frames[ix].resize((240,135));x=((ix-start)%8)*240;y=((ix-start)//8)*164;sheet.paste(im,(x,y+22));d.text((x+2,y+3),f'{ix} PTS={records[ix]["source_seconds"]:.4f}',fill='black')
 sheet.save(p/f'all_frames_{start:03}.jpg',quality=95)
meta={'sha256':hashlib.sha256(fpath.read_bytes()).hexdigest(),'frame_count':len(frames),'stream_time_base':str(s.time_base),'average_rate':str(s.average_rate),'start_time':s.start_time,'duration_ticks':s.duration,'duration_s':float(s.duration*s.time_base),'width':s.width,'height':s.height,'frames':records}
p.joinpath('decode_pts.json').write_text(json.dumps(meta,indent=2));print({k:v for k,v in meta.items() if k!='frames'})
