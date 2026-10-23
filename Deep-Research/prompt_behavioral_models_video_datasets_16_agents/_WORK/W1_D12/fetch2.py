exec(open('_WORK/W1_D12/fetch.py',encoding='utf-8-sig').read().split('a=list(')[0])
urls={'pdestre_download':'https://p-destre.di.ubi.pt/download.html','meccano_page':'https://iplab.dmi.unict.it/legacy/MECCANO/','meccano_readme':'https://raw.githubusercontent.com/fpv-iplab/MECCANO/master/README.md','dmd':'https://dmd.vicomtech.org/','100doh_license':'https://raw.githubusercontent.com/ddshan/hand_object_detector/master/LICENSE','100doh_config':'https://raw.githubusercontent.com/ddshan/hand_object_detector/master/cfgs/res101.yml'}
a=list(concurrent.futures.ThreadPoolExecutor(6).map(lambda kv:fetch(*kv),urls.items()))
try:
 r=requests.get('https://fouheylab.eecs.umich.edu/~dandans/projects/100DOH/download.html',timeout=25,verify=False);(p/'100doh_download.txt').write_text(r.text,encoding='utf-8');a.append(dict(key='100doh_download',status=r.status_code,tls_verify=False,bytes=len(r.content)))
except Exception as e:a.append(dict(error=str(e)))
(p/'access2.json').write_text(json.dumps(a,indent=2),encoding='utf-8');print(json.dumps(a,indent=2))
