import requests,io,rarfile,pathlib,json,time
p=pathlib.Path('_WORK/W2_06_EVIDENCE'); access=json.loads((p/'rar_access.json').read_text()); url='https://ndownloader.figshare.com/files/53696243'; logs=[]
class Remote(io.RawIOBase):
 def __init__(self): self.pos=0;self.size=4929210010;self.cache={};self.total=0
 def readable(self):return True
 def seekable(self):return True
 def tell(self):return self.pos
 def seek(self,n,w=0):self.pos=n if w==0 else self.pos+n if w==1 else self.size+n;return self.pos
 def read(self,n=-1):
  if n<0 or n>65536:raise RuntimeError(f'read bound {n}')
  if not n:return b''
  start=self.pos;end=min(self.size,start+max(n,4096))-1
  for a,b in self.cache.items():
   if a<=start and start+n<=a+len(b):self.pos+=n;return b[start-a:start-a+n]
  if self.total+end-start+1>2097152:raise RuntimeError('2MiB total metadata bound')
  r=requests.get(url,headers={'Range':f'bytes={start}-{end}'},timeout=25,stream=True)
  if r.status_code!=206: r.close();raise RuntimeError(f'range status {r.status_code}')
  b=r.content;self.total+=len(b);self.cache[start]=b;logs.append({'start':start,'end':end,'status':r.status_code,'content_range':r.headers.get('Content-Range'),'bytes':len(b)});self.pos+=min(n,len(b));return b[:n]
f=Remote()
try:
 a=rarfile.RarFile(f);members=[]
 for i in a.infolist():
  members.append({k:getattr(i,k,None) for k in ['filename','file_size','compress_size','header_offset','header_size','data_offset','compress_type','flags','CRC','date_time','file_compress_flags']})
 (p/'mmodalfire_manifest.json').write_text(json.dumps({'solid':a.is_solid(),'members':members,'total_range_bytes':f.total},ensure_ascii=False,indent=2));print(json.dumps({'solid':a.is_solid(),'members':len(members),'bytes':f.total,'first':members[:8]},ensure_ascii=False,indent=2))
except Exception as e:print(type(e).__name__,str(e));(p/'manifest_error.txt').write_text(repr(e))
finally:(p/'rar_header_ranges.json').write_text(json.dumps(logs,indent=2))

