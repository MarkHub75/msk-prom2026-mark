import requests,pathlib,json,struct,zlib,hashlib
P=pathlib.Path(__file__).parent;s=requests.Session();rev='7f79b39fcd1ef1dc39f23f227cd8a9480d6077db'
url=f'https://huggingface.co/datasets/nvidia/PhysicalAI-Event-Videos/resolve/{rev}/2026/train/videos.zip'
log=[]
def get(a,b):
 r=s.get(url+f'?bounded_w204={a}',headers={'Range':f'bytes={a}-{b}'},timeout=60,stream=True)
 if r.status_code!=206: r.close();raise RuntimeError(f'Refuse non-range {r.status_code}')
 cr=r.headers.get('Content-Range');data=r.raw.read(b-a+2);r.close()
 if len(data)!=b-a+1:raise RuntimeError('wrong bounded response size')
 log.append(dict(start=a,end=b,content_range=cr,bytes=len(data)));(P/'range_log.json').write_text(json.dumps(log,indent=2));return data
size=7954992209
tail=get(size-131072,size-1);pos=tail.rfind(b'PK\x05\x06');assert pos>=0
e=struct.unpack_from('<4s4H2LH',tail,pos);cdsize=e[5];cdoff=e[6]
if cdoff==0xffffffff or cdsize==0xffffffff:
 zp=tail.rfind(b'PK\x06\x06');assert zp>=0
 zh=struct.unpack_from('<4sQ2H2L4Q',tail,zp);cdsize=zh[-2];cdoff=zh[-1]
assert cdsize<2000000 and cdoff< size
cd=get(cdoff,cdoff+cdsize-1);(P/'zip_central_directory.bin').write_bytes(cd)
entries=[];i=0
while cd[i:i+4]==b'PK\x01\x02':
 h=struct.unpack_from('<4s6H3L5H2L',cd,i);n,ex,co=h[10:13];name=cd[i+46:i+46+n].decode();x=dict(name=name,method=h[4],crc=h[7],compressed=h[8],uncompressed=h[9],offset=h[16]);extra=cd[i+46+n:i+46+n+ex];j=0
 while j+4<=len(extra):
  tag,ln=struct.unpack_from('<HH',extra,j);v=extra[j+4:j+4+ln];j+=4+ln
  if tag==1:
   k=0
   for field in ['uncompressed','compressed','offset']:
    if x[field]==0xffffffff:x[field]=struct.unpack_from('<Q',v,k)[0];k+=8
 entries.append(x);i+=46+n+ex+co
(P/'zip_members.json').write_text(json.dumps(entries,indent=2));print('entries',len(entries))
for target in ['videos/video_00238.mp4','videos/video_00298.mp4']:
 x=next(q for q in entries if q['name']==target);assert x['compressed']<15000000
 off=x['offset'];header=get(off,off+29);h=struct.unpack('<4s5H3L2H',header);start=off+30+h[-2]+h[-1]
 data=get(start,start+x['compressed']-1);out=zlib.decompress(data,-15) if x['method']==8 else data
 assert len(out)==x['uncompressed'] and zlib.crc32(out)==x['crc'];(P/pathlib.Path(target).name).write_bytes(out)
 print(target,len(out),hashlib.sha256(out).hexdigest())
