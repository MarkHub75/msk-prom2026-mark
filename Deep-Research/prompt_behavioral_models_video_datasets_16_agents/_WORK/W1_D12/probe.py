exec(open('_WORK/W1_D12/fetch.py',encoding='utf-8-sig').read().split('a=list(')[0])
urls={'pdestre_tar':'https://p-destre.di.ubi.pt/datasets/dataset.tar','meccano_actions':'https://iplab.dmi.unict.it/sharing/MECCANO/MECCANO_action_annotations.zip','meccano_hands':'https://iplab.dmi.unict.it/sharing/MECCANO/MECCANO_hands_bounding_box_annotations.zip','meccano_active':'https://iplab.dmi.unict.it/sharing/MECCANO/MECCANO_active_object_bounding_box_annotations.zip','meccano_video':'https://iplab.dmi.unict.it/sharing/MECCANO/MECCANO_RGB_Videos.zip','100doh_file':'https://fouheylab.eecs.umich.edu/~dandans/projects/100DOH/downloads/file.zip','100doh_weight':'https://drive.google.com/file/d/166IM6CXA32f9L6V7-EMd9m8gin6TFpim/view'}
def probe(k,u):
 try:
  r=requests.get(u,headers={'Range':'bytes=0-1048575'},timeout=35,stream=True,verify=not('fouheylab' in u)); b=next(r.iter_content(1048576),b'');r.close();(p/(k+'.probe')).write_bytes(b)
  return dict(key=k,url=u,status=r.status_code,headers=dict(r.headers),bytes_read=len(b),time=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:return dict(key=k,url=u,error=str(e))
a=list(concurrent.futures.ThreadPoolExecutor(7).map(lambda kv:probe(*kv),urls.items()));(p/'probes.json').write_text(json.dumps(a,indent=2),encoding='utf-8');print(json.dumps([{k:v for k,v in x.items() if k!='headers'}|{'headers':{k:v for k,v in x.get('headers',{}).items() if k.lower() in ['content-length','content-range','content-type']}} for x in a],indent=2))
