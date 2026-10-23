import pathlib, json, collections, zipfile, hashlib, pickletools
R=pathlib.Path(__file__).parent
def var(b,p):
 v=0
 for i in range(10):
  x=b[p];p+=1;v|=(x&127)<<(7*i)
  if x<128:return v,p
 raise ValueError('varint bound')
def fields(b):
 p=0
 while p<len(b):
  t,p=var(b,p);n,w=t>>3,t&7
  if w==0:v,p=var(b,p)
  elif w in (1,5):s=8 if w==1 else 4;v=b[p:p+s];p+=s
  elif w==2:s,p=var(b,p);v=b[p:p+s];p+=s
  else:raise ValueError(w)
  if p>len(b):raise ValueError('length')
  yield n,w,v
def vals(b,n):return [v for k,w,v in fields(b) if k==n]
def s(b):return b.decode('utf8','replace')
def vi(b):
 typ=vals(b,2)[0];tt=vals(typ,1)[0];dims=[]
 for d in vals(vals(tt,2)[0],1):dims.append(vals(d,1)[0] if vals(d,1) else s(vals(d,2)[0]))
 return {'name':s(vals(b,1)[0]),'elem_type':vals(tt,1)[0],'dims':dims}
def tensor(b):
 return {'name':s(vals(b,8)[0]) if vals(b,8) else '', 'dtype':vals(b,2), 'external_data':[{s(vals(e,1)[0]):s(vals(e,2)[0])} for e in vals(b,13)],'data_location':vals(b,14)}
def graph(b):
 nodes=vals(b,1);init=vals(b,5);ops=collections.Counter();nested=[];attrs=[]
 for nd in nodes:
  op=s(vals(nd,4)[0]);domain=s(vals(nd,7)[0]) if vals(nd,7) else '';ops[domain+'::'+op]+=1
  for a in vals(nd,5):
   name=s(vals(a,1)[0]); attrs.append((op,name))
   for g in vals(a,6)+vals(a,11):nested.append(graph(g))
 return {'name':s(vals(b,2)[0]) if vals(b,2) else '', 'inputs':[vi(v) for v in vals(b,11)],'outputs':[vi(v) for v in vals(b,12)],'node_count':len(nodes),'operators':dict(sorted(ops.items())),'initializers':len(init),'external_tensors':[t for t in map(tensor,init) if t['external_data'] or t['data_location']==[1]],'nested_graphs':nested,'attribute_inventory':dict(collections.Counter(op+':'+name for op,name in attrs))}
def model(b):
 return {'ir_version':vals(b,1),'producer_name':[s(v) for v in vals(b,2)],'producer_version':[s(v) for v in vals(b,3)],'opsets':[{'domain':s(vals(o,1)[0]) if vals(o,1) else '', 'version':vals(o,2)} for o in vals(b,8)],'graph':graph(vals(b,7)[0]),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
result={'yolox_nano':model((R/'yolox_nano.onnx').read_bytes())}
with zipfile.ZipFile(R/'rtmpose-t.zip') as z:
 result['rtmpose_zip_entries']=[{'name':i.filename,'bytes':i.file_size,'compressed':i.compress_size,'crc32':format(i.CRC,'08x')} for i in z.infolist()]
 for i in z.infolist():
  if i.file_size>16*1024*1024:raise ValueError('zip expansion bound')
  if i.filename.endswith('.onnx'):
   b=z.read(i);(R/'rtmpose-t.onnx').write_bytes(b);result['rtmpose']=model(b)
  elif i.filename.endswith('.json'):
   b=z.read(i);(R/pathlib.Path(i.filename).name).write_bytes(b);result[pathlib.Path(i.filename).name]=json.loads(b)
with zipfile.ZipFile(R/'yolov8n-pose.pt') as z:
 result['pose_zip_entries']=[{'name':i.filename,'bytes':i.file_size} for i in z.infolist()]
 p=[i for i in z.infolist() if i.filename.endswith('data.pkl')][0]
 assert p.file_size<1024*1024
 b=z.read(p);ops=list(pickletools.genops(b))
 # Disassembly is static; GLOBAL/REDUCE instructions are printed, never executed.
 with (R/'pose_pickle_disassembly.txt').open('w',encoding='utf8') as f:pickletools.dis(b,out=f)
 result['pose_pickle']={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'op_count':len(ops),'global_references':sorted(set(str(a) for o,a,pos in ops if o.name=='GLOBAL'))}
(R/'static_metadata.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k in ('yolox_nano','rtmpose','pose_pickle')},indent=2))
