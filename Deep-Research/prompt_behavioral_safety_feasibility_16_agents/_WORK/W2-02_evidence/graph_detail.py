from inspect_static import fields,vals,s,R
import json,struct
def attr(a):
 out={'name':s(vals(a,1)[0])}
 for num,label,fun in [(2,'float',lambda v:struct.unpack('<f',v)[0]),(3,'int',lambda v:v),(4,'string',s),(7,'floats',lambda v:v),(8,'ints',lambda v:v)]:
  v=vals(a,num)
  if v:out[label]=[fun(x) for x in v]
 return out
out={}
for name in ['yolox_nano.onnx','rtmpose-t.onnx']:
 b=(R/name).read_bytes();g=vals(b,7)[0];nodes=[]
 for n in vals(g,1):nodes.append({'name':[s(x) for x in vals(n,3)],'op':s(vals(n,4)[0]),'inputs':[s(x) for x in vals(n,1)],'outputs':[s(x) for x in vals(n,2)],'attrs':[attr(a) for a in vals(n,5)]})
 out[name]={'nodes':nodes,'sparse_initializers':len(vals(g,15)), 'local_functions':len(vals(b,25))}
(R/'graph_nodes.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps({'yolox_tail':out['yolox_nano.onnx']['nodes'][-6:],'resize':[n for n in out['yolox_nano.onnx']['nodes'] if n['op']=='Resize']},indent=2))
