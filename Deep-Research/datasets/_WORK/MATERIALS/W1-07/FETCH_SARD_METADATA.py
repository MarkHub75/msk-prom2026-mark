"""Read only ZIP directories and one small annotation member, never video archives."""
import io,json,pathlib,requests,zipfile
ROOT=pathlib.Path(__file__).parent
class Remote(io.RawIOBase):
    def __init__(self,url,n): self.url,self.n,self.pos,self.total=url,n,0,0
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos
    def seek(self,n,w=0):
        self.pos=n if w==0 else self.pos+n if w==1 else self.n+n
        return self.pos
    def read(self,n=-1):
        if n<0: n=self.n-self.pos
        n=min(n,self.n-self.pos)
        if n<=0: return b''
        if n>4000000: raise ValueError('Large reads deliberately disabled')
        r=requests.get(self.url,headers={'Range':f'bytes={self.pos}-{self.pos+n-1}'},timeout=40)
        r.raise_for_status()
        if r.status_code!=206: raise ValueError('Range unsupported')
        self.pos+=len(r.content);self.total+=len(r.content)
        return r.content
name='ComplementarySet.zip'
r=Remote('https://zenodo.org/api/records/19926448/files/'+name+'/content',35002552520)
z=zipfile.ZipFile(r)
raw=z.read('ComplementarySet/4.txt')
(ROOT/'SARD_4.txt').write_bytes(raw)
lines=raw.decode('utf8').splitlines()
report={'member':'ComplementarySet/4.txt','uncompressed_bytes':len(raw),'lines':len(lines),'network_bytes':r.total,'first_lines':lines[:5]}
(ROOT/'SARD_4_observation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,indent=2))
