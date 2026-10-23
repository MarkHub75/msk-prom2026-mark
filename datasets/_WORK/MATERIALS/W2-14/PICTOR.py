import pathlib,re,requests,json,collections
p=pathlib.Path(__file__).parent;h=(p/'PICTOR_Labels.html').read_text(encoding='utf8');h=re.sub(r'\\x([0-9a-fA-F]{2})',lambda m:chr(int(m[1],16)),h);rows=[]
for id,name in re.findall(r'\["([A-Za-z0-9_-]+)",\["17VMS2-EQAuB6CsCVDK5ScmxjrP-B2cgW"\],"([^"]+\.txt)"',h):
 r=requests.get('https://drive.google.com/uc',params={'export':'download','id':id},timeout=40);(p/name).write_bytes(r.content);rows.append({'id':id,'name':name,'status':r.status_code,'bytes':len(r.content),'content_type':r.headers.get('content-type')});print(rows[-1],r.text[:100],flush=True)
(p/'PICTOR_DOWNLOADS.json').write_text(json.dumps(rows,indent=2))
