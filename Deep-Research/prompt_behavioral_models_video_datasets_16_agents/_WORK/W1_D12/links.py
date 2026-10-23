from bs4 import BeautifulSoup
from pathlib import Path
for name in ['pdestre_download','100doh_download','meccano_page']:
 s=BeautifulSoup(Path('_WORK/W1_D12/'+name+'.txt').read_text(encoding='utf-8'),'html.parser')
 Path('_WORK/W1_D12/'+name+'_text.txt').write_text(s.get_text('\n',strip=True),encoding='utf-8')
 print('\n'+name)
 for a in s.select('a[href]'):
  h=a['href'];t=a.get_text(' ',strip=True)
  if any(v in (h+' '+t).lower() for v in ['zip','download','licen','annot','drive','readme','model']):print(t,h)
