import datetime, hashlib, json, pathlib, urllib.request, concurrent.futures
ROOT=pathlib.Path(__file__).parent
URLS={
'PYPI_CURRENT.json':'https://pypi.org/pypi/pytpu/json',
'PYPI_SIMPLE.html':'https://pypi.org/simple/pytpu/',
'DOCS.html':'https://lin-q.ru/docs',
'SDK_HOME_HTTPS.html':'https://git.mmp.iva-tech.ru/tpu_sw/iva_tpu_sdk',
'SDK_HOME_HTTP.html':'http://git.mmp.iva-tech.ru/tpu_sw/iva_tpu_sdk',
'MLPERF_TREE.json':'https://api.github.com/repos/mlcommons/inference_results_v0.7/git/trees/89260c7a0bb2bb86f4adaf1d88e0307162eb602b?recursive=1',
'BENCH_TREE.json':'https://api.github.com/repos/sherstpasha/linq-cv-bench/git/trees/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140?recursive=1',
}
def fetch(item):
 name,url=item; row={'file':name,'url':url,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'LinQ-research/1.0'})
  with urllib.request.urlopen(req,timeout=25) as response:
   data=response.read(); row.update(status=response.status,final_url=response.url,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
  (ROOT/name).write_bytes(data)
 except Exception as e: row['error']=repr(e)
 return row
rows=list(concurrent.futures.ThreadPoolExecutor(max_workers=5).map(fetch,URLS.items()))
(ROOT/'HTTP_LOG.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(json.dumps(rows,indent=2))
