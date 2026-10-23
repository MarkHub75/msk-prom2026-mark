import io,requests,zipfile,pathlib,json,hashlib,datetime
p=pathlib.Path('_WORK/W1_D12');u='https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades_v1_480.zip';log=[]
class Remote(io.RawIOBase):
 def __init__(self):self.pos=0;self.size=16339546533;self.s=requests.Session();self.total=0
 def seekable(self):return True
 def readable(self):return True
 def tell(self):return self.pos
 def seek(self,offset,whence=0):self.pos=offset if whence==0 else self.pos+offset if whence==1 else self.size+offset;return self.pos
 def read(self,n=-1):
  if n<0:n=self.size-self.pos
  if n>6000000:raise RuntimeError('bounded request exceeded')
  r=self.s.get(u,headers={'Range':f'bytes={self.pos}-{self.pos+n-1}'},timeout=25)
  if r.status_code!=206:raise RuntimeError(str(r.status_code))
  b=r.content;log.append({'offset':self.pos,'n':n,'got':len(b),'status':r.status_code});self.pos+=len(b);self.total+=len(b);return b
r=Remote()
with zipfile.ZipFile(r) as z:
 n=next(n for n in z.namelist() if n.endswith('/2RFLZ.mp4') or n=='2RFLZ.mp4');info=z.getinfo(n);print(n,info.file_size,info.compress_size)
 if info.file_size>6000000:raise RuntimeError('member too large')
 b=z.read(n);(p/'charades_2RFLZ.mp4').write_bytes(b)
meta=dict(url=u,member=n,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),total_http_bytes=r.total,requests=log,access_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());(p/'charades_media_access.json').write_text(json.dumps(meta,indent=2));print(meta)
