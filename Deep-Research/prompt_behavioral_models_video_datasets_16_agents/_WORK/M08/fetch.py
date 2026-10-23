import requests,json,concurrent.futures,pathlib,datetime
out=pathlib.Path('_WORK/M08');s=requests.Session()
urls={
'movinet':'https://raw.githubusercontent.com/tensorflow/models/master/official/projects/movinet/README.md',
'x3d':'https://raw.githubusercontent.com/facebookresearch/pytorchvideo/main/pytorchvideo/models/hub/x3d.py',
'x3dhub':'https://raw.githubusercontent.com/pytorch/hub/master/facebookresearch_pytorchvideo_x3d.md',
'movinetblog':'https://blog.tensorflow.org/2022/04/video-classification-on-edge-devices.html',
'mmaction_tree':'https://api.github.com/repos/open-mmlab/mmaction2/git/trees/main?recursive=1',
'movinet_commit':'https://api.github.com/repos/tensorflow/models/commits/master',
'x3d_commit':'https://api.github.com/repos/facebookresearch/pytorchvideo/commits/main',
'ava':'https://research.google.com/ava/download.html',
'ava_labels':'https://raw.githubusercontent.com/cvdfoundation/ava-dataset/main/ava_action_list_v2.2_for_activitynet_2019.pbtxt',
'kinetics':'https://github.com/cvdfoundation/kinetics-dataset',
}
def get(k,u):
 try:
  r=s.get(u,timeout=30);(out/(k+'.txt')).write_text(r.text,encoding='utf-8');return dict(key=k,url=u,status=r.status_code,final=r.url,bytes=len(r.content),time=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:return dict(key=k,url=u,error=str(e))
a=list(concurrent.futures.ThreadPoolExecutor(8).map(lambda kv:get(*kv),urls.items()));(out/'access.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
