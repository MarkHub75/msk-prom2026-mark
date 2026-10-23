exec(open('_WORK/MATERIALS/W2-02/GET_SAMPLE.py',encoding='utf-8-sig').read().split('selected={}')[0])
from PIL import Image,ImageDraw
selected={}
for t in ['halmet-off-yellow','halmet-on-yellow']:
 cand=[x for x in rows if any(a==t for a,b in x[2])];cand.sort(key=lambda x:-max((b[2]-b[0])*(b[3]-b[1])/(int(x[1].findtext('size/width'))*int(x[1].findtext('size/height'))) for a,b in x[2] if a==t));x=cand[0];selected[x[0]]={'reasons':[t+' largest relative box'],'xml':x[1],'objects':x[2]}
exec(open('_WORK/MATERIALS/W2-02/GET_SAMPLE.py',encoding='utf-8-sig').read().split('def f(item):')[1].split('res=list')[0].join(['def f(item):','']))
res=list(concurrent.futures.ThreadPoolExecutor(2).map(f,selected.items()));old=json.loads((p/'SAMPLE_SELECTION.json').read_text());res=old+res
for d in res:
 im=Image.open(p/d['filename']).convert('RGB');d['decoded_size']=im.size
 sx=720/im.width;out=im.resize((720,round(im.height*sx))); dr=ImageDraw.Draw(out)
 for idx,(a,b) in enumerate(d['objects']):
  if any(t in a for t in ['glov','glass','halm','helm','face-mask','face-guard','vest']):dr.rectangle([v*sx for v in b],outline='red',width=3);dr.text((b[0]*sx,b[1]*sx),str(idx)+':'+a,fill='red')
 out.save(p/('overlay_'+pathlib.Path(d['filename']).stem+'.jpg'))
(p/'SAMPLE_SELECTION.json').write_text(json.dumps(res,indent=2));print([(x['filename'],x['decoded_size']) for x in res])
