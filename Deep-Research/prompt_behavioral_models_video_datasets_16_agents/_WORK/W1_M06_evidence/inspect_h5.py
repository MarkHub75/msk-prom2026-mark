import sys, io, requests, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent/'deps'))
import h5py
p=pathlib.Path(__file__).parent
class Remote(io.RawIOBase):
 def __init__(self): self.pos=0; self.cache={0:(p/'6ImageTest.h5.head').read_bytes()}; self.log=[]; self.total=65536
 def readable(self): return True
 def seekable(self): return True
 def tell(self): return self.pos
 def seek(self,o,w=0):
  self.pos=o if w==0 else self.pos+o if w==1 else 937501056+o
  return self.pos
 def readinto(self,b):
  d=self.read(len(b));b[:len(d)]=d;return len(d)
 def read(self,n=-1):
  if n<0: raise RuntimeError('bounded reads only')
  out=b''
  while n:
   start=self.pos//65536*65536
   if start not in self.cache:
    if self.total+65536>1048576: raise RuntimeError('metadata budget')
    end=min(937501055,start+65535)
    r=requests.get('https://drive.usercontent.google.com/download?id=10uIEuqmaYnjtt3wGCTm7tmbdBmhQBigm&export=download&confirm=t',headers={'Range':f'bytes={start}-{end}'},timeout=30)
    if r.status_code!=206 or r.headers.get('Content-Range')!=f'bytes {start}-{end}/937501056': raise RuntimeError('invalid range')
    self.cache[start]=r.content;self.total+=len(r.content);self.log.append([start,end,len(r.content)])
   off=self.pos-start;d=self.cache[start][off:off+n]
   if not d: break
   self.pos+=len(d);n-=len(d);out+=d
  return out
r=Remote();o={}
try:
 with h5py.File(r,'r') as f:
  for k in f.keys():
   x=f[k];o[k]={'shape':list(x.shape),'dtype':str(x.dtype),'offset':x.id.get_offset()}
   if k in ['Mean','Variance']:o[k]['value']=x[()].tolist()
   if k=='labels':
    a=x[()];o[k]['min']=float(a.min());o[k]['max']=float(a.max());o[k]['first10']=a[:10].tolist();o[k]['mean']=float(a.mean());o[k]['negative_count']=int((a<0).sum())
except Exception as e:o['error']=repr(e)
o['reads']=r.log;o['total_bytes']=r.total
(p/'near_h5_schema.json').write_text(json.dumps(o,indent=2),encoding='utf8')
print(json.dumps(o,indent=2))
