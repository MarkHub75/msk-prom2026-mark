exec(open('_WORK/M04_fetch.py',encoding='utf-8').read().split('urls=')[0])
from bs4 import BeautifulSoup
urls={
'caviar':'https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/',
'walkxml':'https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/Walk1/wk1gt.xml',
'runxml':'https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/Fight_RunAway1/fra1gt.xml',
'hmdbconfig024':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v0.24.1/configs/recognition/slowonly/slowonly_k400_pretrained_r50_8x4x1_40e_hmdb51_rgb.py',
'hmdbparent024':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v0.24.1/configs/recognition/slowonly/slowonly_k400_pretrained_r50_8x4x1_40e_ucf101_rgb.py',
'slowonly024':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v0.24.1/configs/recognition/slowonly/README.md',
'hmdblabels024':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v0.24.1/tools/data/hmdb51/label_map.txt',
'hmdbrgbdata024':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v0.24.1/tools/data/hmdb51/README.md',
'hmdbbase024':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v0.24.1/configs/_base_/models/slowonly_r50.py',
'avaclasses':'https://research.google.com/ava/download/ava_action_list_v2.2_for_activitynet_2019.pbtxt',
}
exec(open('_WORK/M04_fetch.py',encoding='utf-8').read().split('def fetch')[1].split('with concurrent')[0].join(['def fetch','']))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: results=list(ex.map(lambda kv:fetch(*kv),urls.items()))
heads={
'hmdbweights':'https://download.openmmlab.com/mmaction/recognition/slowonly/slowonly_k400_pretrained_r50_8x4x1_40e_hmdb51_rgb/slowonly_k400_pretrained_r50_8x4x1_40e_hmdb51_rgb_20210630-cee5f725.pth',
'kthwalk':'https://www.csc.kth.se/cvap/actions/person15_walking_d1_uncomp.avi',
'kthjog':'https://www.csc.kth.se/cvap/actions/person15_jogging_d1_uncomp.avi',
'kthrun':'https://www.csc.kth.se/cvap/actions/person15_running_d1_uncomp.avi',
}
for k,u in heads.items():
 try:
  r=requests.head(u,timeout=30,allow_redirects=True); results.append(dict(key=k,url=u,method='HEAD',status=r.status_code,headers=dict(r.headers),time=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 except Exception as e:results.append(dict(key=k,url=u,error=str(e)))
(root/'access_more.json').write_text(json.dumps(results,indent=2),encoding='utf-8'); print(json.dumps(results,indent=2))
