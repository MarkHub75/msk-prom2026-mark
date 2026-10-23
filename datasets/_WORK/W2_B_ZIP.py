import requests,io,zipfile,pathlib,json,struct,collections,sys
R=pathlib.Path(__file__).parent/'MATERIALS'
IDS={'04':'1-2z7r3J4sZdLvVt5mllvSEwAFO49Y-zj','05':'1qWm7rrwvjAWs1slymbrLaCf7Q-wnGLEX','06':'1fdGn67W0B7ShpBDbbQpUF0ScPQa4DR0a'}
class Remote(io.RawIOBase):
 def __init__(self,num):
  self.url=f'https://drive.usercontent.google.com/download?id={IDS[num]}&export=download&confirm=t';self.pos=0;self.log=[];self.s=requests.Session();q=self.s.get(self.url,headers={'Range':'bytes=-65536'},timeout=45);q.raise_for_status();self.n=int(q.headers['Content-Range'].split('/')[-1]);self.cache={(self.n-len(q.content),self.n):q.content};self.log.append({'range':'tail','bytes':len(q.content),'status':q.status_code})
 def seek(self,p,w=0):self.pos=p if w==0 else self.pos+p if w==1 else self.n+p;return self.pos
 def tell(self):return self.pos
 def seekable(self):return True
 def read(self,n=-1):
  if n<0:n=self.n-self.pos
  start=self.pos;end=min(self.n,start+n);self.pos=end
  for (a,b),data in self.cache.items():
   if a<=start and end<=b:return data[start-a:end-a]
  q=self.s.get(self.url,headers={'Range':f'bytes={start}-{end-1}'},timeout=60);q.raise_for_status()
  if q.status_code!=206:raise ValueError('Range not honored')
  data=q.content;self.cache[(start,end)]=data;self.log.append({'start':start,'end':end,'bytes':len(data),'status':q.status_code});return data
def run(num):
 o=R/f'W2-{num}';o.mkdir(exist_ok=True,parents=True);f=Remote(num);z=zipfile.ZipFile(f);m=[{'name':x.filename,'size':x.file_size,'compressed':x.compress_size,'crc32':x.CRC} for x in z.infolist()];(o/'ARCHIVE_MANIFEST.json').write_text(json.dumps({'url':f.url,'archive_bytes':f.n,'entries':m},indent=2));print(num,len(m),f.n,collections.Counter(pathlib.Path(x['name']).suffix for x in m),flush=True)
 names=[x.filename for x in z.infolist() if not x.is_dir()];small=[n for n in names if any(k in pathlib.Path(n).name.lower() for k in ['readme','license','classes','train.txt','test.txt','val.txt','trainval.txt']) or n.endswith(('.yaml','.names'))]
 # all text annotations for CHV affordable; SHWD select 36 spaced label pairs, SFCHD select by all7 class coverage later
 labels=[n for n in names if n.endswith(('.xml','.txt')) and n not in small]
 if num=='05':selected=labels[::max(1,len(labels)//32)][:32]
 elif num=='06':selected=[n for n in labels if not n.startswith('__MACOSX/')][:80];small=[n for n in names if not n.startswith('__MACOSX/') and (n.endswith('README.md') or '/data split/' in n)]
 else:selected=[]
 (o/'pairs').mkdir(exist_ok=True)
 for n in small+selected:
  if z.getinfo(n).file_size>3000000:continue
  p=o/'pairs'/pathlib.Path(n).name
  if not p.exists():p.write_bytes(z.read(n))
 if num=='05':
  for n in selected:
   stem=pathlib.Path(n).stem;im=next((x for x in names if pathlib.Path(x).stem==stem and pathlib.Path(x).suffix.lower() in ['.jpg','.jpeg','.png']),None)
   if im:(o/'pairs'/pathlib.Path(im).name).write_bytes(z.read(im))
 (o/'RANGE_LOG.json').write_text(json.dumps(f.log,indent=2));print('done',num,len(f.log),flush=True)
if __name__=='__main__':run(sys.argv[1])
