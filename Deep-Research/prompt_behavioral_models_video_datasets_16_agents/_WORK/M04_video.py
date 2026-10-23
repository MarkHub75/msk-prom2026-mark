import requests, pathlib,json,datetime,hashlib,xml.etree.ElementTree as E,collections
import av
from PIL import Image,ImageDraw
p=pathlib.Path('_WORK/M04'); results=[]
videos={
'kthwalk':'https://www.csc.kth.se/cvap/actions/person15_walking_d1_uncomp.avi',
'kthjog':'https://www.csc.kth.se/cvap/actions/person15_jogging_d1_uncomp.avi',
'kthrun':'https://www.csc.kth.se/cvap/actions/person15_running_d1_uncomp.avi',
'caviarwalk':'https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/Walk1/Walk1.mpg',
'caviarrun':'https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/Fight_RunAway1/Fight_RunAway1.mpg',
}
for k,u in videos.items():
 try:
  r=requests.get(u,timeout=35,stream=True); r.raise_for_status(); data=bytearray()
  for chunk in r.iter_content(65536):
   data.extend(chunk)
   if len(data)>9_000_000:raise ValueError('bounded download exceeded 9MB')
  f=p/(k+('.avi' if 'kth' in k else '.mpg')); f.write_bytes(data)
  container=av.open(str(f)); stream=container.streams.video[0]; fps=float(stream.average_rate); count=0; ts=[]; shape=None
  for frame in container.decode(video=0):
   count+=1; ts.append(float(frame.time)*1000 if frame.time is not None else None);shape=[frame.height,frame.width]
  container.close()
  results.append(dict(key=k,url=u,status=r.status_code,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),time=datetime.datetime.now(datetime.timezone.utc).isoformat(),fps=fps,decoded_frames=count,shape=shape,first_msec=ts[:4],last_msec=ts[-4:]))
 except Exception as e:results.append(dict(key=k,url=u,error=str(e)))
# Parse labels without pretending annotation is model performance.
for name in ['runxml','walkxml']:
 root=E.parse(p/(name+'.txt')).getroot(); by=collections.defaultdict(list); ctr=collections.Counter()
 for f in root.findall('frame'):
  for obj in f.findall('./objectlist/object'):
   m=obj.find('.//movement'); label=m.text if m is not None else None
   if label:ctr[label]+=1;by[(obj.get('id'),label)].append(int(f.get('number')))
 intervals=[]
 for (obj,label),seq in by.items():
  start=prev=seq[0]
  for n in seq[1:]+[None]:
   if n is None or n!=prev+1:
    intervals.append(dict(actor=obj,label=label,start=start,end=prev,count=prev-start+1))
    start=n
   prev=n
 results.append(dict(key=name,frames=len(root.findall('frame')),counts=dict(ctr),intervals=intervals))
(p/'video_annotation_checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
