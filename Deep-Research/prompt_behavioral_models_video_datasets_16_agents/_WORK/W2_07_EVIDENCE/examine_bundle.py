import pathlib,json,requests,bs4
p=pathlib.Path('_WORK/W2_07_EVIDENCE'); c=json.loads((p/'commit.json').read_text())['sha']
for path in ['official/vision/modeling/layers/nn_layers.py']:
 r=requests.get('https://raw.githubusercontent.com/tensorflow/models/'+c+'/'+path,timeout=40); (p/path.split('/')[-1]).write_bytes(r.content)
s=bs4.BeautifulSoup(pathlib.Path('_WORK/M08/movinetblog.txt').read_text(encoding='utf8'),'html.parser'); txt=s.get_text(' ',strip=True); (p/'blog_plain.txt').write_text(txt,encoding='utf8')
print([(a.get_text(' ',strip=True),a.get('href')) for a in s.find_all('a') if any(x in (a.get('href') or '') for x in ['tfhub','kaggle','tflite','lite-model'])])
n=json.loads((p/'movinet_tutorial.ipynb').read_text()); (p/'tutorial_cells.txt').write_text('\n\n'.join(''.join(x['source']) for x in n['cells']),encoding='utf8')
r=json.loads((p/'static_graph.json').read_text()); g=r['subgraphs'][0]; print('summary',len(g['inputs']),len(g['outputs']),g['tensor_count'],g['tensor_dtype_counts'],g['operators']); print('sig',[(x['key'],len(x['inputs']),len(x['outputs'])) for x in r['signatures']]); print('image/logits',[x for x in g['inputs']+g['outputs'] if 'image' in x['name'] or len(x['shape'])==2]); print('meta',r['metadata'])
