import requests,pathlib,concurrent.futures
p=pathlib.Path(r'D:\msk-prom2026-mark\Deep-Research\LinQ-case-analytics-research\_WORK\W2_04_MATERIALS')
urls={'Trud_2025.pdf':'https://rosstat.gov.ru/storage/mediabank/Trud_2025.pdf','catalog.html':'https://rosstat.gov.ru/working_conditions'}
def get(k,u):
 try:
  r=requests.get(u,timeout=25);(p/k).write_bytes(r.content); print(k,r.status_code,len(r.content))
 except Exception as e: print(k,str(e))
with concurrent.futures.ThreadPoolExecutor() as ex:list(ex.map(lambda kv:get(*kv),urls.items()))
