import requests, pathlib, json, datetime, hashlib
P=pathlib.Path(__file__).parent
targets={
 'DOCS_HTML':'https://lin-q.ru/docs',
 'SOL_HTML':'https://lin-q.ru/sol',
 'GUIDE':'https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf',
 'REPO':'https://api.github.com/repos/sherstpasha/linq-cv-bench',
 'COMMITS':'https://api.github.com/repos/sherstpasha/linq-cv-bench/commits?per_page=5',
 'TREE':'https://api.github.com/repos/sherstpasha/linq-cv-bench/git/trees/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140?recursive=1',
 'MLPERF_QUANT':'https://raw.githubusercontent.com/mlcommons/inference_results_v0.7/master/open/IVATech/code/mobilenet/v1/quantize/quantize.sh',
 'BUILDER':'https://raw.githubusercontent.com/sherstpasha/linq-cv-bench/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/build_yolov8_program.py',
}
log=[]
for name,url in targets.items():
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=requests.get(url,timeout=25)
  b=r.content
  ext='.pdf' if b.startswith(b'%PDF') else '.TXT'
  (P/(name+ext)).write_bytes(b)
  log.append(dict(name=name,url=url,time=t,status=r.status_code,type=r.headers.get('content-type'),length=len(b),sha256=hashlib.sha256(b).hexdigest()))
 except Exception as e: log.append(dict(name=name,url=url,time=t,error=str(e)))
(P/'HTTP_LOG.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(log,ensure_ascii=False,indent=2))
