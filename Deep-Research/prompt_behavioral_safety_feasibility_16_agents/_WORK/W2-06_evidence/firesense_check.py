import requests,json,pathlib
r=pathlib.Path('_WORK/W2-06_evidence');u='https://zenodo.org/api/records/836749/files/fire_videos.1406.zip/content'
q=requests.get(u,headers={'Range':'bytes=622611309-622676844'},stream=True,timeout=30);rec={'url':u,'requested':'bytes=622611309-622676844','status':q.status_code,'headers':dict(q.headers)}
if q.status_code==206:
 b=q.raw.read(65537);rec['actual_bytes']=len(b);(r/'firesense_tail.bin').write_bytes(b)
else:rec['body']='not consumed; refused full archive'
q.close();(r/'firesense_range.json').write_text(json.dumps(rec,indent=2));print(json.dumps(rec,indent=2))
