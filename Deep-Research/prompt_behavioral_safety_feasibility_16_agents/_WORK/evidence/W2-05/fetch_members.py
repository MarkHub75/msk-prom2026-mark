import urllib.request,struct,json,zlib,hashlib,pathlib
out=pathlib.Path('_WORK/evidence/W2-05')
base='https://www.wisdom.weizmann.ac.il/~vision/VideoAnalysis/Demos/SpaceTimeActions/DB/'
def rng(url,a,b):
 req=urllib.request.Request(url,headers={'Range':f'bytes={a}-{b}','User-Agent':'Research'})
 with urllib.request.urlopen(req,timeout=30) as r:
  if r.status!=206: raise ValueError(f'Range not honored: {r.status}; refused body')
  data=r.read(b-a+2)
  if len(data)!=b-a+1: raise ValueError('range length mismatch')
  return data,dict(r.headers)
records=[]
for action,size in [('walk',51996002),('run',30591544)]:
 url=base+action+'.zip'
 tail,headers=rng(url,size-65536,size-1)
 eocd=tail.rfind(b'PK\x05\x06')
 disk,cdisk,n1,n2,cdsize,cdoffset,comment=struct.unpack_from('<4H2IH',tail,eocd+4)
 if cdoffset<size-65536: raise ValueError('CD out of tail')
 p=cdoffset-(size-65536); members=[]
 while tail[p:p+4]==b'PK\x01\x02':
  v=struct.unpack_from('<6H3I5H2I',tail,p+4)
  method=v[3]; crc=v[6]; comp=v[7]; uncomp=v[8]; nl,xl,cl=v[9:12]; off=v[15]
  name=tail[p+46:p+46+nl].decode('ascii'); members.append(dict(name=name,method=method,crc=crc,compressed=comp,size=uncomp,offset=off)); p+=46+nl+xl+cl
 print(action, members)
 chosen=next(x for x in members if x['name']=='daria_'+action+'.avi')
 if chosen['compressed']>7000000 or chosen['size']>20000000: raise ValueError('size budget')
 off=chosen['offset']; head,h=rng(url,off,off+29)
 hv=struct.unpack('<4s5H3I2H',head); dataoff=off+30+hv[-2]+hv[-1]
 compressed,h=rng(url,dataoff,dataoff+chosen['compressed']-1)
 data=zlib.decompress(compressed,-15) if chosen['method']==8 else compressed
 if len(data)!=chosen['size'] or (zlib.crc32(data)&0xffffffff)!=chosen['crc']: raise ValueError('CRC')
 path=out/chosen['name'];path.write_bytes(data)
 records.append(dict(action=action,url=url,archive_size_head=size,tail_range=[size-65536,size-1],range_headers=headers,members=members,selected=chosen,data_range=[dataoff,dataoff+chosen['compressed']-1],actual_avi_bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
(out/'range_manifest.json').write_text(json.dumps(records,indent=2),encoding='utf8')
