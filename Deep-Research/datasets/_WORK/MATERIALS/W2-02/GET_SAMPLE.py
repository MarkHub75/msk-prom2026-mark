import pathlib,zipfile,xml.etree.ElementTree as E,json,requests,concurrent.futures,collections
p=pathlib.Path('_WORK/MATERIALS/W2-02'); z=zipfile.ZipFile('_WORK/MATERIALS/W1-11/SH17-raw.zip'); rows=[]
for n in z.namelist():
 if not n.endswith('.xml'):continue
 r=E.fromstring(z.read(n)); objs=[(o.findtext('name'),[float(o.findtext('bndbox/'+x)) for x in ['xmin','ymin','xmax','ymax']]) for o in r.findall('object')]; rows.append((n,r,objs))
targets=['helmet-off','helmet-on','gloves-off','gloves-on','glasses-safety-off','glasses-safety-on','glasses-vision-off','glasses-vision-on','face-mask-medical-off','face-mask-medical-on','safety-vest-off','face-guard-off']
print('helmet names',collections.Counter(a for _,_,o in rows for a,b in o if 'helm' in a or 'halm' in a))
urls={u.split('/')[-1]:u for u in pathlib.Path('_WORK/MATERIALS/W1-02/list_of_all_urls.csv').read_text().splitlines()}
selected={}
for t in targets:
 cand=[x for x in rows if any(a==t for a,b in x[2])]
 if not cand:continue
 # choose informative object comparatively large, moderate people (not first arbitrary)
 cand.sort(key=lambda x: -max(((b[2]-b[0])*(b[3]-b[1])/(int(x[1].findtext('size/width'))*int(x[1].findtext('size/height')))) for a,b in x[2] if a==t))
 x=cand[0]; selected.setdefault(x[0],{'reasons':[],'xml':x[1],'objects':x[2]})['reasons'].append(t+' largest relative box')
# crowded image with PPE
cand=[x for x in rows if sum('person' in a for a,b in x[2])>=8 and any('glasses' in a or 'helm' in a for a,b in x[2])]
if cand:
 x=sorted(cand,key=lambda x:-sum('person' in a for a,b in x[2]))[0];selected[x[0]]={'reasons':['most person-literal objects among >=8 persons and PPE'],'xml':x[1],'objects':x[2]}
def f(item):
 n,d=item;r=d.pop('xml');name=r.findtext('filename');url=urls.get(name);d.update(xml=n,filename=name,declared=[int(r.findtext('size/width')),int(r.findtext('size/height'))],url=url);(p/(pathlib.Path(n).name)).write_bytes(z.read(n))
 if url:
  try:
   res=requests.get(url,timeout=50);d.update(status=res.status_code,bytes=len(res.content));
   if res.status_code==200:(p/name).write_bytes(res.content)
  except Exception as e:d['error']=str(e)
 return d
res=list(concurrent.futures.ThreadPoolExecutor(5).map(f,selected.items()));(p/'SAMPLE_SELECTION.json').write_text(json.dumps(res,indent=2));print([(x['filename'],x['reasons'],x.get('status')) for x in res])
