import pathlib,zipfile,xml.etree.ElementTree as E,json
p=pathlib.Path('_WORK/W2_06_EVIDENCE');f=next((p/'metadata').rglob('*.xlsx'));z=zipfile.ZipFile(f);ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
ss=[]
if 'xl/sharedStrings.xml' in z.namelist():
 for si in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns):ss.append(''.join(t.text or '' for t in si.iter('{'+ns['s']+'}t')))
res={}
for n in z.namelist():
 if n.startswith('xl/worksheets/sheet') and n.endswith('.xml'):
  rows=[]
  for row in E.fromstring(z.read(n)).findall('.//s:row',ns):
   cells={}
   for c in row.findall('s:c',ns):
    v=c.find('s:v',ns);val=v.text if v is not None else ''.join(c.itertext());cells[c.attrib['r']]=ss[int(val)] if c.attrib.get('t')=='s' else val
   rows.append(cells)
  res[n]=rows
(p/'settings_cells.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf8')
for k,v in res.items():
 print(k)
 for row in v:print(row)
f=next((p/'metadata').rglob('Readme.txt'));b=f.read_bytes()
for enc in ['utf8','gb18030']:
 try:print('README',enc,b.decode(enc));break
 except UnicodeDecodeError:pass
