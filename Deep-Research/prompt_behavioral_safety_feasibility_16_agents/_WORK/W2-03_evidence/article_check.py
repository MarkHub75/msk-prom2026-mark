from pathlib import Path
import requests,xml.etree.ElementTree as E
u='https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11416611/fullTextXML'; r=requests.get(u,timeout=30); r.raise_for_status(); p=Path('_WORK/W2-03_evidence/article.xml'); p.write_bytes(r.content); root=E.fromstring(r.content)
for s in root.iter('sec'):
 t=' '.join(s.itertext())
 if 'Ethics Statement' in t or ('consent' in t.lower() and len(t)<18000): print(t[:11000])
print('bytes',len(r.content))
