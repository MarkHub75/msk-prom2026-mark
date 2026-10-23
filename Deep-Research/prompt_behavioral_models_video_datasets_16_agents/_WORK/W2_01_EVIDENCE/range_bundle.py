import requests,io,zipfile,json,pathlib,hashlib,datetime,onnx,collections
P=pathlib.Path(__file__).parent
URL='https://download.openmmlab.com/mmpose/v1/projects/rtmpose/rtmpose-cpu.zip'
SIZE=54564140
log=[]
class Remote(io.RawIOBase):
 def __init__(self): self.pos=0;self.total=0
 def seekable(self): return True
 def readable(self): return True
 def tell(self): return self.pos
 def seek(self,off,whence=0):
  self.pos=off if whence==0 else self.pos+off if whence==1 else SIZE+off
  return self.pos
 def read(self,n=-1):
  if n<0:n=SIZE-self.pos
  if n==0:return b''
  if n>6000000 or self.total+n>15000000: raise ValueError('byte bound exceeded')
  end=min(SIZE-1,self.pos+n-1)
  r=requests.get(URL,headers={'Range':f'bytes={self.pos}-{end}'},timeout=(15,45),stream=True)
  if r.status_code!=206: r.close();raise ValueError(f'expected206 got {r.status_code}')
  b=r.content
  if len(b)!=end-self.pos+1:raise ValueError('length')
  log.append(dict(range=f'{self.pos}-{end}',status=r.status_code,content_range=r.headers.get('Content-Range'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
  self.pos+=len(b); self.total+=len(b)
  return b
f=Remote();z=zipfile.ZipFile(f)
manifest=[dict(name=i.filename,size=i.file_size,compressed=i.compress_size,header_offset=i.header_offset,crc=i.CRC) for i in z.infolist()]
(P/'CPU_BUNDLE_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
for i in z.infolist():
 if i.is_dir():continue
 if i.filename.endswith('.json') or ('rtmdet' in i.filename and i.filename.endswith('.onnx')):
  b=z.read(i.filename); t=P/'cpu_selected'/i.filename;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(b)
(P/'CPU_RANGE_ACCESS.json').write_text(json.dumps(log,indent=2))
print(json.dumps(manifest,indent=2)); print('total network bytes',f.total)
