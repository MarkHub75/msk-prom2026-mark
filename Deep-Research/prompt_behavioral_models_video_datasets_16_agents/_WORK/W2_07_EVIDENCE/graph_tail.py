import pathlib,tflite,json
p=pathlib.Path('_WORK/W2_07_EVIDENCE'); out={}; ops={v:k for k,v in vars(tflite.BuiltinOperator).items() if isinstance(v,int)}
for file in ['movinet_a0_stream.tflite','int8_1.tflite']:
 b=(p/file).read_bytes(); m=tflite.Model.GetRootAsModel(b,0);g=m.Subgraphs(0); rows=[]
 for j in range(max(0,g.OperatorsLength()-22),g.OperatorsLength()):
  op=g.Operators(j); rows.append(dict(index=j,op=ops[m.OperatorCodes(op.OpcodeIndex()).BuiltinCode()],inputs=[dict(i=int(i),name=g.Tensors(int(i)).Name().decode()) for i in op.InputsAsNumpy() if i>=0],outputs=[dict(i=int(i),name=g.Tensors(int(i)).Name().decode()) for i in op.OutputsAsNumpy()]))
 out[file]=rows
(p/'graph_tail.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out['int8_1.tflite'][-13:],indent=2))
