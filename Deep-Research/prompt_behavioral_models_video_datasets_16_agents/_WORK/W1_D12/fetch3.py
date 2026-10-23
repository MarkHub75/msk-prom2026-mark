import requests,pathlib,json,concurrent.futures
p=pathlib.Path('_WORK/W1_D12')
urls={'100doh_agreement':'https://fouheylab.eecs.umich.edu/~dandans/projects/100DOH/agreement.html?pascal_voc_format','100doh_util':'https://raw.githubusercontent.com/ddshan/hand_object_detector/master/lib/model/utils/net_utils.py','100doh_core_config':'https://raw.githubusercontent.com/ddshan/hand_object_detector/master/lib/model/utils/config.py','100doh_commit':'https://api.github.com/repos/ddshan/hand_object_detector/commits/master','meccano_commit':'https://api.github.com/repos/fpv-iplab/MECCANO/commits/master','meccano_config':'https://raw.githubusercontent.com/fpv-iplab/MECCANO/master/configs/active_object_recognition/meccano_active_objects.yaml'}
def f(x):
 k,u=x
 try:
  r=requests.get(u,timeout=20,verify=not 'fouheylab' in u);(p/(k+'.txt')).write_text(r.text,encoding='utf-8');return(k,r.status_code,len(r.content))
 except Exception as e:return(k,str(e))
print(list(concurrent.futures.ThreadPoolExecutor(6).map(f,urls.items())))
