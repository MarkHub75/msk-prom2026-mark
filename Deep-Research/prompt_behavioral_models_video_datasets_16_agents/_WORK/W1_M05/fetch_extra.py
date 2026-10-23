import requests,pathlib,json,datetime,concurrent.futures
p=pathlib.Path('_WORK/W1_M05')
urls={'hico_annotations':'https://raw.githubusercontent.com/fredzzhang/hicodet/9dd59c1/instances_train2015.json','hico_doc':'https://raw.githubusercontent.com/fredzzhang/hicodet/9dd59c1/DOC.md','upt_inference':'https://raw.githubusercontent.com/fredzzhang/upt/main/inference.py','upt_actions':'https://raw.githubusercontent.com/fredzzhang/upt/main/assets/actions.txt','upt_github':'https://github.com/fredzzhang/upt','upt_weights_page':'https://drive.google.com/file/d/1lvopTC_JlGHdKOyyEZTUp2VtFfCQ-08z/view','upt_weights_binary':'https://drive.usercontent.google.com/download?id=1lvopTC_JlGHdKOyyEZTUp2VtFfCQ-08z&export=download','ava_config22':'https://raw.githubusercontent.com/open-mmlab/mmaction2/main/configs/detection/slowfast/slowfast_kinetics400-pretrained-r50_8xb6-8x8x1-cosine-10e_ava22-rgb.py','ava_loading':'https://raw.githubusercontent.com/open-mmlab/mmaction2/main/mmaction/datasets/transforms/loading.py','hico_original':'https://ywchao.github.io/hico/','hico_det_original':'https://ywchao.github.io/hico-det/'}
def fetch(k,u):
 try:
  r=requests.get(u,timeout=25,stream=True);body=b''
  for chunk in r.iter_content(65536):
   body+=chunk
   if len(body)>8_000_000:break
  (p/(k+'.txt')).write_bytes(body);return {'key':k,'url':u,'final_url':r.url,'status':r.status_code,'content_type':r.headers.get('Content-Type'),'content_length':r.headers.get('Content-Length'),'saved_bytes':len(body),'time':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 except Exception as e:return {'key':k,'url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:out=list(ex.map(lambda a:fetch(*a),urls.items()))
(p/'access_extra.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
