import urllib.request, json, pathlib, hashlib, concurrent.futures, datetime
P=pathlib.Path(__file__).parent
urls={
'zenodo.json':'https://zenodo.org/api/records/13354453',
'mendeley.html':'https://data.mendeley.com/datasets/xjmtb22pff/1',
'mendeley_api.json':'https://data.mendeley.com/public-api/datasets/xjmtb22pff',
'hf_media_card.md':'https://huggingface.co/datasets/Voxel51/Safe_and_Unsafe_Behaviours/raw/7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5/README.md',
'rtmpose_card.md':'https://huggingface.co/Tau-J/RTMPose/raw/cd4d7095f5cfc9cfc4f46289bee91ea4a1e1d9fd/README.md',
'yolox_LICENSE':'https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/LICENSE',
'yolox_tag_LICENSE':'https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/e1052df71842031413f6030723c3607b839c80ce/LICENSE',
'rtmlib_LICENSE':'https://raw.githubusercontent.com/Tau-J/rtmlib/03a1693e59e4f7cd84582c0fb30459b3bf18ad42/LICENSE',
'mmpose_LICENSE':'https://raw.githubusercontent.com/open-mmlab/mmpose/537bd8e543ab463fb55120d5caaa1ae22d6aaf06/LICENSE',
'mmpose_modelzoo.md':'https://raw.githubusercontent.com/open-mmlab/mmpose/537bd8e543ab463fb55120d5caaa1ae22d6aaf06/docs/en/model_zoo.md',
'ultra_license.html':'https://www.ultralytics.com/license',
'cc.html':'https://creativecommons.org/licenses/by/4.0/legalcode.en',
'gmd_tag.json':'https://api.github.com/repos/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/commits/v2.1',
}
def get(item):
 name,url=item; out={'name':name,'url':url,'access_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'EvidenceResearch/1.0'}),timeout=40) as r:
   b=r.read(4*1024*1024+1)
   if len(b)>4*1024*1024: raise ValueError('body exceeds cap')
   (P/name).write_bytes(b); out.update(status=r.status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:out['error']=str(e)
 return out
if __name__=='__main__':
 result=list(concurrent.futures.ThreadPoolExecutor(8).map(get,urls.items()))
 (P/'sources.json').write_text(json.dumps(result,indent=2),encoding='utf8')
 print(json.dumps(result,indent=2))
