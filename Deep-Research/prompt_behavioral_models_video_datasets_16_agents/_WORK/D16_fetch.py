import requests, pathlib, json, hashlib, datetime, concurrent.futures
from bs4 import BeautifulSoup
p=pathlib.Path('_WORK/D16_evidence');p.mkdir(exist_ok=True)
urls={
'synapt_readme':'https://raw.githubusercontent.com/mintjohnkim/SynAPT/4473b40b6a603b0f7a21c34fe7b8051942ad8963/README.md',
'synapt_paper.pdf':'https://proceedings.neurips.cc/paper_files/paper/2022/file/e8507db80464ced5658d16b49bd458b9-Paper-Datasets_and_Benchmarks.pdf',
'surreact_readme':'https://raw.githubusercontent.com/gulvarol/surreact/73a1851b01dffb79d5b1d7afa08a6bfe91646954/README.md',
'surreact_training':'https://raw.githubusercontent.com/gulvarol/surreact/73a1851b01dffb79d5b1d7afa08a6bfe91646954/training/README.md',
'surreact_license':'https://raw.githubusercontent.com/gulvarol/surreact/73a1851b01dffb79d5b1d7afa08a6bfe91646954/LICENSE',
'surreact_paper.pdf':'https://arxiv.org/pdf/1912.04070v3',
'remag_page':'https://humansensinglab.github.io/REMAG/',
'remag_paper.pdf':'https://openaccess.thecvf.com/content/WACV2024/papers/Panev_Exploring_the_Impact_of_Rendering_Method_and_Motion_Quality_on_WACV_2024_paper.pdf',
'videophy_readme':'https://raw.githubusercontent.com/Hritikbansal/videophy/01d366c979e4a82875852adbf427ccc036e7373a/README.md',
'videophy_paper':'https://arxiv.org/html/2406.03520v2',
'mdpi_paper':'https://www.mdpi.com/2079-9292/15/16/3712',
}
def get(kv):
 k,u=kv
 try:
  r=requests.get(u,timeout=35); b=r.content
  rec=dict(name=k,url=u,status=r.status_code,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
  if r.status_code==200 and len(b)<15000000:
   (p/k).write_bytes(b)
   if 'html' in r.headers.get('Content-Type',''): (p/(k+'.txt')).write_text(BeautifulSoup(r.text,'html.parser').get_text(' ',strip=True),encoding='utf-8')
  return rec
 except Exception as e:return dict(name=k,url=u,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: out=list(ex.map(get,urls.items()))
(p/'access.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
for row in out:print(row['name'],row.get('status'),row.get('bytes'),row.get('error',''))
try:
 import fitz
 for f in p.glob('*.pdf'):
  doc=fitz.open(f); (p/(f.stem+'.txt')).write_text('\n'.join(f'PAGE {i+1}\n'+pg.get_text() for i,pg in enumerate(doc)),encoding='utf-8')
except Exception as e:print(e)
