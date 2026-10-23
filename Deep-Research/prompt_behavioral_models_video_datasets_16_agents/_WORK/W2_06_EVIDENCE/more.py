import requests,pathlib,json,concurrent.futures
from bs4 import BeautifulSoup
p=pathlib.Path('_WORK/W2_06_EVIDENCE')
us={'table2':'https://www.nature.com/articles/s41597-026-06810-6/tables/2','table3':'https://www.nature.com/articles/s41597-026-06810-6/tables/3','mmodal_repo':'https://api.github.com/repos/SiliconSisyphus/MultiModal-fire-detection','mmodal_tree':'https://api.github.com/repos/SiliconSisyphus/MultiModal-fire-detection/git/trees/main?recursive=1'}
def g(t):
 k,u=t
 try:r=requests.get(u,timeout=25);(p/(k+'.txt')).write_bytes(r.content);print(k,r.status_code,len(r.content));return {'name':k,'url':u,'status':r.status_code,'bytes':len(r.content)}
 except Exception as e:return {'name':k,'error':str(e)}
x=list(concurrent.futures.ThreadPoolExecutor(4).map(g,us.items()));(p/'more_access.json').write_text(json.dumps(x,indent=2))
for k in ['table2','table3']:
 s=BeautifulSoup((p/(k+'.txt')).read_text(encoding='utf8'),'html.parser').get_text(' ',strip=True);(p/(k+'_plain.txt')).write_text(s,encoding='utf8');print(k,s[:9000])
