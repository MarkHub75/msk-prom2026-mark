import urllib.request,json,pathlib,struct,hashlib,zlib,datetime
P=pathlib.Path(__file__).parent
log=[]
def rng(url,start,end):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'Range':f'bytes={start}-{end}','User-Agent':'EvidenceResearch/1.0'}),timeout=40) as r:
  h=dict(r.headers); n=end-start+1; b=r.read(n+1)
  log.append({'url':url,'request_range':[start,end],'status':r.status,'headers':{k:v for k,v in h.items() if k.lower() in ['content-range','content-length','etag','last-modified']},'received':len(b),'sha256':hashlib.sha256(b).hexdigest()})
  if r.status!=206 or len(b)!=n:raise ValueError('bounded range not honoured')
  return b
try:
 z=json.loads((P/'zenodo.json').read_text()); url=z['files'][0]['links']['self']; size=z['files'][0]['size']
 tail=rng(url,size-65557,size-1); (P/'zenodo_tail.bin').write_bytes(tail)
 i=tail.rfind(b'PK\x05\x06'); vals=struct.unpack_from('<4s4H2LH',tail,i); count,cdsize,cdoff=vals[4:7]
 if cdsize>1024*1024:raise ValueError('directory exceeds cap')
 cd=rng(url,cdoff,cdoff+cdsize-1); (P/'zenodo_directory.bin').write_bytes(cd)
 entries=[]; pos=0
 while pos<len(cd):
  v=struct.unpack_from('<4s6H3L5H2L',cd,pos)
  if v[0]!=b'PK\x01\x02':raise ValueError('bad directory signature')
  fn,xl,cl=v[10:13]; name=cd[pos+46:pos+46+fn].decode('utf8'); entries.append({'name':name,'crc32':v[7],'compressed_size':v[8],'size':v[9],'method':v[4],'offset':v[16]}); pos+=46+fn+xl+cl
 (P/'zenodo_directory.json').write_text(json.dumps(entries,indent=2))
 pairs=[('Subject 1/Fall/11.mp4','_WORK/W1-09_samples/positive_S1_F11.mp4'),('Subject 3/ADL/08.mp4','_WORK/W1-09_samples/negative_S3_A08.mp4')]
 results=[]
 for suffix,local in pairs:
  e=next(e for e in entries if e['name'].endswith('/'+suffix)); off=e['offset']; header=rng(url,off,off+29); v=struct.unpack('<4s5H3L2H',header); start=off+30+v[-2]+v[-1]
  if e['compressed_size']>8*1024*1024 or e['size']>8*1024*1024:raise ValueError('member exceeds cap')
  packed=rng(url,start,start+e['compressed_size']-1); raw=zlib.decompress(packed,-15) if e['method']==8 else packed
  b=pathlib.Path(local).read_bytes(); results.append({'member':e,'local':local,'archive_sha256':hashlib.sha256(raw).hexdigest(),'local_sha256':hashlib.sha256(b).hexdigest(),'equal':raw==b,'crc_valid':(zlib.crc32(raw)&0xffffffff)==e['crc32']})
 (P/'gmd_identity.json').write_text(json.dumps(results,indent=2))
except Exception as e:log.append({'error':str(e)})
finally:
 (P/'range_log.json').write_text(json.dumps(log,indent=2)); print(json.dumps(log,indent=2))
j=json.loads((P/'mendeley_api.json').read_text()); out=[]
for n in ['0_te23.mp4','4_te1.mp4']:
 f=next(f for f in j['files'] if f['filename']==n); b=pathlib.Path('_WORK/W1-10_evidence',n).read_bytes(); out.append({'author_record':f,'local_sha256':hashlib.sha256(b).hexdigest(),'local_bytes':len(b),'sha256_match':hashlib.sha256(b).hexdigest()==f['content_details']['sha256_hash']})
(P/'mendeley_identity.json').write_text(json.dumps(out,indent=2)); print('Mendeley:',[(x['author_record']['filename'],x['sha256_match']) for x in out])
