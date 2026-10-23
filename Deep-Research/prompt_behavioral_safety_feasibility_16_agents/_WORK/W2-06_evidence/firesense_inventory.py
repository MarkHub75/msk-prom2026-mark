import struct,json,pathlib
r=pathlib.Path('_WORK/W2-06_evidence');b=(r/'firesense_tail.bin').read_bytes();e=b.rfind(b'PK\x05\x06');disk,cdisk,n1,n2,sz,off,comment=struct.unpack_from('<4H2IH',b,e+4);p=off-622611309;rec=[]
while b[p:p+4]==b'PK\x01\x02':
 v=struct.unpack_from('<6H3I5H2I',b,p+4);name=b[p+46:p+46+v[9]].decode();rec.append({'name':name,'method':v[3],'crc32':v[6],'compressed':v[7],'uncompressed':v[8],'offset':v[15]});p+=46+v[9]+v[10]+v[11]
(r/'firesense_members.json').write_text(json.dumps(rec,indent=2));print(json.dumps(sorted(rec,key=lambda x:x['compressed'])[:15],indent=2))
