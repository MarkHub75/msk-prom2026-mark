from bs4 import BeautifulSoup
from pathlib import Path
s=BeautifulSoup(Path('_WORK/W1_D12/pdestre_https.txt').read_text(encoding='utf-8'),'html.parser')
Path('_WORK/W1_D12/pdestre_text.txt').write_text(s.get_text('\n',strip=True),encoding='utf-8')
for a in s.select('a[href]'):
 h=a['href']
 if any(t in (h+' '+a.get_text()).lower() for t in ['download','zip','drive','license','annot','benchmark','paper','youtu']):print(a.get_text(' ',strip=True),h)
