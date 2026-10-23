import requests, pathlib, json, hashlib, datetime, concurrent.futures
root=pathlib.Path(__file__).parent/'M04'; root.mkdir(exist_ok=True)
urls={
'kth':'https://www.csc.kth.se/cvap/actions/',
'kthseq':'https://www.csc.kth.se/cvap/actions/00sequences.txt',
'meva':'https://mevadata.org/',
'mevalicense':'https://mevadata.org/resources/MEVA-data-license.txt',
'mevadownload':'https://mevadata.org/resources/README-meva-kf1-data.html',
'mevatree':'https://gitlab.kitware.com/api/v4/projects/meva%2Fmeva-data-repo/repository/tree?per_page=100',
'mevadefs':'https://gitlab.kitware.com/meva/meva-data-repo/-/raw/master/documents/MEVA-Annotation-Definitions.pdf',
'hmdb':'https://serre-lab.clps.brown.edu/resource/hmdb-a-large-human-motion-database/',
'slowonlyreadme':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v1.2.0/configs/recognition/slowonly/README.md',
'hmdbclasses':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v1.2.0/tools/data/hmdb51/label_map.txt',
'k400classes':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v1.2.0/tools/data/kinetics/label_map_k400.txt',
'avaclasses':'https://research.google.com/ava/download/ava_action_list_v2.2_for_activitynet_2019.pbtxt',
'slowonlyconfig':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v1.2.0/configs/recognition/slowonly/slowonly_k400-pretrained-r50_8xb16-8x4x1-40e_hmdb51-rgb.py',
'mmlicense':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v1.2.0/LICENSE',
}
def fetch(k,u):
 try:
  r=requests.get(u,timeout=35); ext='.pdf' if 'application/pdf' in r.headers.get('Content-Type','') else '.txt'; p=root/(k+ext); p.write_bytes(r.content)
  return dict(key=k,url=u,final=r.url,status=r.status_code,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest(),time=datetime.datetime.now(datetime.timezone.utc).isoformat(),file=str(p),type=r.headers.get('Content-Type'))
 except Exception as e:return dict(key=k,url=u,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: results=list(ex.map(lambda kv:fetch(*kv), urls.items()))
(root/'access.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
