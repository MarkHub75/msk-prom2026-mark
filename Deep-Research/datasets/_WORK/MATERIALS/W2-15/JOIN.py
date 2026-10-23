import pathlib,json,requests,csv,collections,re,pymupdf
p=pathlib.Path('_WORK/MATERIALS/W2-15');base=pathlib.Path('_WORK/MATERIALS/W1-06/PhysicalAI-Event-Videos');data=json.loads((base/'2026/train/labels.json').read_text());rules=json.loads((base/'anomaly-category-mapping.json').read_text())['rules'];manifest=list(csv.DictReader((base/'2026/train/video_manifest.csv').open()));print('manifest',manifest[:2]);print('parent',next(x for x in data if x['dataset'].startswith('NV')))
sel=[]
for par in data:
 for c in par['chunks']:
  family=next((r['family'] for r in rules if re.search(r['regex'],c.get('anomaly_type',''),re.I)), 'Other / ambiguous') if c.get('is_anomaly') else 'Normal'
  if family=='Smoking / vaping':sel.append({'dataset':par['dataset'],'video_id':par['video_id'],'source_video':par.get('source_video'),'video_path':par.get('video_path'),'fps':par.get('fps'),'duration':par.get('video_duration_sec'),'chunk':c})
(p/'SMOKING_JOIN.json').write_text(json.dumps(sel,indent=2),encoding='utf8');print('selection',len(sel),collections.Counter(x['dataset'] for x in sel),'parents',len(set((x['dataset'],x['video_id']) for x in sel)))
u='https://assets.ngc.nvidia.com/products/api-catalog/legal/Personas-Dataset-NVIDIA-Training-Dataset-License-Agreement-2025-11-26.pdf';r=requests.get(u,timeout=40);(p/'LICENSE.pdf').write_bytes(r.content);print('license',r.status_code,len(r.content));doc=pymupdf.open(stream=r.content,filetype='pdf');t='\n'.join(x.get_text() for x in doc);(p/'LICENSE.txt').write_text(t,encoding='utf8');print(t[:2000])
r=requests.get('https://cloud.google.com/terms/service-terms',timeout=40);(p/'GOOGLE.html').write_bytes(r.content);print('google',r.status_code,len(r.content))
