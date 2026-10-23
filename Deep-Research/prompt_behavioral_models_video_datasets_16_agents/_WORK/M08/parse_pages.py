from bs4 import BeautifulSoup
import pathlib
for key in ['ava','kinetics']:
 s=BeautifulSoup(pathlib.Path('_WORK/M08/'+key+'.txt').read_text(encoding='utf-8'),'html.parser')
 print(key,s.get_text(' ',strip=True)[-18000:])
 print('\nLINKS\n', '\n'.join(a.get('href','') for a in s.find_all('a') if any(w in a.get('href','') for w in ['csv','zip','pbtxt','json','tar','license'])))
