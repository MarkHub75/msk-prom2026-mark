import tarfile,zipfile,pathlib
p=pathlib.Path('_WORK/W1_D12')
try:
 with tarfile.open(p/'pdestre_tar.probe',mode='r:') as t:
  for i,m in enumerate(t):
   print('TAR',m.name,m.size,m.offset,m.offset_data)
   if m.isfile() and m.size<1000000:
    d=t.extractfile(m).read();(p/'pdestre_tar_first.txt').write_bytes(d);print(d[:1000])
   if i>15:break
except Exception as e:print(type(e).__name__,e)
with zipfile.ZipFile(p/'meccano_actions.probe') as z:
 print(z.namelist())
 for n in z.namelist():
  if not n.endswith('/'):
   b=z.read(n);print(n,len(b),b[:1500]);(p/('action_'+pathlib.Path(n).name)).write_bytes(b)
