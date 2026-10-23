import pathlib,json,requests,struct,zlib,time
p=pathlib.Path('_WORK/W2_06_EVIDENCE');base='https://ndownloader.figshare.com/files/53696243';logs=[];members=[];blocks=[];cache={0:(p/'rar_first64k.bin').read_bytes()};total=65536;session=requests.Session(); signed=None;signed_at=0

def vint(b,i):
 n=0;s=0
 while True:
  c=b[i];i+=1;n|=(c&127)<<s
  if c<128:return n,i
  s+=7

def get(pos):
 global total,signed,signed_at
 for a,b in cache.items():
  if a<=pos and pos+1024<=a+len(b):return b[pos-a:]
 if total+4096>2097152:raise RuntimeError('2MiB metadata bound')
 r=session.get(signed if signed and time.monotonic()-signed_at<7 else base,headers={'Range':f'bytes={pos}-{min(4929210009,pos+4095)}'},timeout=20);r.raise_for_status();assert r.status_code==206
 if r.history:signed=r.url;signed_at=time.monotonic()
 b=r.content;total+=len(b);cache[pos]=b;logs.append({'offset':pos,'bytes':len(b),'status':r.status_code,'range':r.headers.get('Content-Range')});(p/'rar_manual_ranges.json').write_text(json.dumps(logs,indent=2));return b
pos=8
if (p/'mmodalfire_manifest.json').exists():
 old=json.loads((p/'mmodalfire_manifest.json').read_text());members=old['members'];blocks=old['blocks'];total=old['total_range_bytes'];last=blocks[-1];pos=last['offset']+last['header_size']+last['data_size'];print('RESUME',len(members),pos,flush=True)
try:
 for count in range(400):
  b=get(pos);hs,i=vint(b,4);end=i+hs;typ,i=vint(b,i);flags,i=vint(b,i);extra=0;data=0
  if flags&1:extra,i=vint(b,i)
  if flags&2:data,i=vint(b,i)
  h={'offset':pos,'header_size':end,'type':typ,'flags':flags,'extra':extra,'data_size':data,'crc_ok':zlib.crc32(b[4:end])==struct.unpack('<I',b[:4])[0]};blocks.append(h)
  if typ==1:
   af,i=vint(b,i);h['archive_flags']=af
  if typ==2:
   ff,i=vint(b,i);size,i=vint(b,i);mode,i=vint(b,i)
   if ff&2:i+=4
   crc=None
   if ff&4:crc=struct.unpack('<I',b[i:i+4])[0];i+=4
   cf,i=vint(b,i);host,i=vint(b,i);nl,i=vint(b,i);name=b[i:i+nl].decode('utf8');m={**h,'filename':name,'uncompressed':size,'compression_flags':cf,'solid':bool(cf&64),'method':(cf>>7)&7,'directory':bool(ff&1),'crc':crc,'data_offset':pos+end};members.append(m);print(name,size,data,flush=True)
  (p/'mmodalfire_manifest.json').write_text(json.dumps({'complete':typ==5,'members':members,'blocks':blocks,'total_range_bytes':total},ensure_ascii=True,indent=2))
  if typ==5:break
  assert end+data>0;pos+=end+data
except Exception as e:(p/'manual_manifest_error.txt').write_text(repr(e));print(repr(e))

