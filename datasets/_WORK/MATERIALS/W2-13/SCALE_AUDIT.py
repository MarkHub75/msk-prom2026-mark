import pathlib,json,zipfile,xml.etree.ElementTree as E,collections,csv,hashlib
import numpy as np
P=pathlib.Path('_WORK/MATERIALS'); OUT=P/'W2-13';OUT.mkdir(exist_ok=True)
rows=[]; inputs=[]
def inp(p):
 inputs.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
def add(ds,im,c,w,h,b):
 x,y,bw,bh=map(float,b);s=min(640/w,640/h)
 rows.append(dict(dataset=ds,image=str(im),category=c,image_width=w,image_height=h,x=x,y=y,width=bw,height=bh,area=bw*bh,min_axis=min(bw,bh),width640=bw*s,height640=bh*s,area640=bw*bh*s*s,min_axis640=min(bw,bh)*s,area_fraction=bw*bh/(w*h),out_of_bounds=x<0 or y<0 or x+bw>w or y+bh>h,positive=bw>0 and bh>0))
p=P/'W1-03/SFCHD-SCALE/dataset_SFCHD/annotations/all_data.json';inp(p);j=json.loads(p.read_text()); ims={x['id']:x for x in j['images']};cats={x['id']:x['name'] for x in j['categories']}
for a in j['annotations']:
 im=ims[a['image_id']];add('SFCHD_allCOCO',a['image_id'],cats[a['category_id']],im['width'],im['height'],a['bbox'])
p=P/'W1-11/SH17-raw.zip';inp(p); z=zipfile.ZipFile(p); manifest=json.loads((P/'W2-01/MANIFEST_PROGRESS.json').read_text());released={pathlib.Path(x['name']).stem for x in manifest['files'] if x['name'].startswith('labels/')}
for n in z.namelist():
 if not n.endswith('.xml'):continue
 r=E.fromstring(z.read(n));w=int(r.findtext('size/width'));h=int(r.findtext('size/height'))
 for o in r.findall('object'):
  a,b,c,d=[float(o.findtext('bndbox/'+k)) for k in ['xmin','ymin','xmax','ymax']];add('SH17_raw_all8102',pathlib.Path(n).stem,o.findtext('name'),w,h,[a,b,c-a,d-b])
  if pathlib.Path(n).stem in released:add('SH17_raw_release_members',pathlib.Path(n).stem,o.findtext('name'),w,h,[a,b,c-a,d-b])
p=P/'W1-04/hf_first_rows.json';inp(p);j=json.loads(p.read_text());cats=['Coverall','Face_Shield','Gloves','Goggles','Mask']
for a in j['rows']:
 r=a['row'];o=r['objects']
 for c,b in zip(o['category'],o['bbox']):add('CPPE_HF_test29',r['image_id'],cats[c],r['width'],r['height'],b)
fields=list(rows[0]);
with (OUT/'BOXES.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
groups=collections.defaultdict(list)
for r in rows:groups[r['dataset'],r['category']].append(r)
metrics=['width','height','area','min_axis','width640','height640','area640','min_axis640','area_fraction'];quant=[0,.1,.25,.5,.75,.9,1];bins=[0,4,8,16,32,64,128,256,640,float('inf')];summary=[]
for (ds,c),rr in sorted(groups.items()):
 valid=[r for r in rr if r['positive']];out=dict(dataset=ds,category=c,n=len(rr),positive=len(valid),out_of_bounds=sum(r['out_of_bounds'] for r in rr),images=len(set(r['image'] for r in rr)))
 out['quantiles']={m:{str(q):float(v) for q,v in zip(quant,np.quantile([r[m] for r in valid],quant,method='linear'))} for m in metrics}
 out['min_axis640_histogram']=list(map(int,np.histogram([r['min_axis640'] for r in valid],bins)[0]));out['area_threshold_counts']={str(th):sum(r['area_fraction']<th for r in valid) for th in [.001,.0012,.002]};out['large_gt_0.002']=sum(r['area_fraction']>.002 for r in valid);summary.append(out)
(OUT/'SCALE_SUMMARY.json').write_text(json.dumps({'inputs':inputs,'quantile_method':'numpy linear','quantiles':quant,'min_axis640_bins_left_closed_right_open':bins[:-1]+['inf'],'transform':'s=min(640/W,640/H); no clipping, no +1 to VOC xyxy; no scaleup cap; continuous dimensions; padding has no dimensional effect','groups':summary},indent=2),encoding='utf-8')
with (OUT/'QUANTILES.csv').open('w',newline='',encoding='utf-8') as f:
 names=['dataset','category','n','images','out_of_bounds']+[m+'_q'+str(q) for m in metrics for q in quant];w=csv.DictWriter(f,fieldnames=names);w.writeheader()
 for r in summary:w.writerow({**{k:r[k] for k in names[:5]},**{m+'_q'+str(q):r['quantiles'][m][str(q)] for m in metrics for q in quant}})
print('rows',len(rows),'groups',len(groups));
for r in summary:
 if r['dataset']!='SH17_raw_release_members' and (r['dataset']!='SH17_raw_all8102' or any(x in r['category'] for x in ['halmet','glasses','mask','gloves'])):print(r['dataset'],r['category'],r['n'],'q10/50/90 min640',[round(r['quantiles']['min_axis640'][str(q)],2) for q in [.1,.5,.9]],r['area_threshold_counts'])
