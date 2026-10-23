import requests,pathlib,json
p=pathlib.Path('_WORK/W2_07_EVIDENCE'); r=requests.get('https://api.github.com/repos/tensorflow/models/commits?until=2021-07-22T00:00:00Z&per_page=1',timeout=30); (p/'july2021_commit.json').write_text(r.text); c=r.json()[0]['sha']; print(c)
for path in ['official/vision/beta/projects/movinet/movinet_layers.py','official/vision/beta/modeling/layers/nn_layers.py','official/vision/beta/projects/movinet/export_saved_model.py','official/vision/beta/projects/movinet/movinet.py']:
 r=requests.get('https://raw.githubusercontent.com/tensorflow/models/'+c+'/'+path,timeout=30); print(path,r.status_code,len(r.content)); (p/('july2021_'+path.split('/')[-1])).write_bytes(r.content)
