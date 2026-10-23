import requests, pathlib, datetime, hashlib, json
P=pathlib.Path(__file__).parent
urls={
'REPO.json':'https://api.github.com/repos/sherstpasha/linq-cv-bench',
'COMMITS.json':'https://api.github.com/repos/sherstpasha/linq-cv-bench/commits?per_page=100',
'ISSUES.json':'https://api.github.com/repos/sherstpasha/linq-cv-bench/issues?state=all&per_page=100',
'RELEASES.json':'https://api.github.com/repos/sherstpasha/linq-cv-bench/releases',
'TAGS.json':'https://api.github.com/repos/sherstpasha/linq-cv-bench/tags',
'AUTHOR_REPOS.json':'https://api.github.com/users/sherstpasha/repos?per_page=100',
'ULTRA_V830_OPS.py':'https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/utils/ops.py',
'ULTRA_V83200_NMS.py':'https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.200/ultralytics/utils/nms.py',
'YOLO5_V70_GENERAL.py':'https://raw.githubusercontent.com/ultralytics/yolov5/v7.0/utils/general.py',
'THESIS_INFO.html':'https://elib.spbstu.ru/dl/3/2026/vr/vr26-931.pdf/en/info',
'VENDOR_TECH.html':'https://lin-q.ru/tech',
'VENDOR_DOCS.html':'https://lin-q.ru/docs',
}
log=[]
for name,url in urls.items():
 row={'url':url,'file':name,'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  r=requests.get(url,timeout=25); row.update(status=r.status_code,final_url=r.url,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest()); (P/name).write_bytes(r.content)
 except Exception as e: row['error']=str(e)
 log.append(row)
(P/'HTTP_LOG.json').write_text(json.dumps(log,indent=2),encoding='utf8')
print(json.dumps(log,indent=2))
