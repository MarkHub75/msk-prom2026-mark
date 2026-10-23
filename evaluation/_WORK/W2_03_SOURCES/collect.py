from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,urllib.request
root=Path(__file__).parent
urls={
 'S01_ht_section2':'https://www150.statcan.gc.ca/n1/pub/12-001-x/2013001/article/11831/section2-eng.htm',
 'S01_ht_main':'https://www150.statcan.gc.ca/n1/pub/12-001-x/2013001/article/11831-eng.htm',
 'S02_stratified':'https://www150.statcan.gc.ca/n1/pub/12-001-x/2019002/article/00006/02-eng.htm',
 'S03_small_ratio':'https://www150.statcan.gc.ca/n1/pub/12-001-x/2019003/article/00003-eng.htm',
 'S03_small_ratio_section2':'https://www150.statcan.gc.ca/n1/pub/12-001-x/2019003/article/00003/02-eng.htm',
 'S04_ratio_docs':'https://r-survey.r-forge.r-project.org/pkgdown/docs/reference/svyratio.html',
 'failed_ratio_lead':'https://www150.statcan.gc.ca/n1/pub/12-001-x/2013002/article/11869/section2-eng.htm'}
rows=[]
for name,url in urls.items():
 row={'id':name,'url':url,'access_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(url,timeout=35) as r:
   data=r.read();row.update(status=r.status,final_url=r.url,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
  (root/(name+'.html')).write_bytes(data)
  row['contains_unavailable_message']=b'website is currently unavailable' in data
 except Exception as e: row['error']=repr(e)
 rows.append(row)
(root/'retrieval.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps(rows,indent=2))
