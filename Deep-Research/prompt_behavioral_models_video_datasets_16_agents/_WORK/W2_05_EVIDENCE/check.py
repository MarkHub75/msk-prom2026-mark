import requests, pathlib, json, hashlib, datetime
p=pathlib.Path(__file__).parent
rev='2cbe9563cbe9f47f846e5c871ee994572bbbc60e'
base=f'https://huggingface.co/datasets/nvidia/PhysicalAI-SmartSpaces/resolve/{rev}/'
urls={
'current_api.json':'https://huggingface.co/api/datasets/nvidia/PhysicalAI-SmartSpaces',
'README.md':base+'README.md',
'croissant.json':base+'croissant.json',
'detector_README.md':'https://huggingface.co/keremberke/yolov8n-forklift-detection/resolve/d8b594f321dd4c64eda16e435601fd266089fc32/README.md',
'detector_api.json':'https://huggingface.co/api/models/keremberke/yolov8n-forklift-detection/revision/d8b594f321dd4c64eda16e435601fd266089fc32',
'publisher_README.md':'https://raw.githubusercontent.com/keremberke/awesome-yolov8-models/fb4b7895a92913023ef222fdf0957b8ce2015766/README.md',
'publisher_LICENSE':'https://raw.githubusercontent.com/keremberke/awesome-yolov8-models/fb4b7895a92913023ef222fdf0957b8ce2015766/LICENSE',
'Camera_0000.mp4':base+'MTMC_Tracking_2026/test/Warehouse_026/videos/Camera_0000.mp4',
}
log=[]
for name,url in urls.items():
 try:
  r=requests.get(url,timeout=(20,60))
  b=r.content
  (p/name).write_bytes(b)
  log.append(dict(name=name,url=url,status=r.status_code,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),type=r.headers.get('Content-Type'),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 except Exception as e: log.append(dict(name=name,url=url,error=str(e)))
(p/'access.json').write_text(json.dumps(log,indent=2),encoding='utf8')
print(json.dumps(log,indent=2))
