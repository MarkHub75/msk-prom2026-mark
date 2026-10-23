import tflite,json,pathlib,collections,numpy as np
p=pathlib.Path('_WORK/W2_07_EVIDENCE'); b=(p/'movinet_a0_stream.tflite').read_bytes(); m=tflite.Model.GetRootAsModel(b,0)
types={v:k for k,v in vars(tflite.TensorType).items() if isinstance(v,int)}; ops={v:k for k,v in vars(tflite.BuiltinOperator).items() if isinstance(v,int)}
def s(x): return x.decode() if x else None
def tensor(g,i):
 t=g.Tensors(i); q=t.Quantization(); return dict(index=i,name=s(t.Name()),shape=t.ShapeAsNumpy().tolist(),shape_signature=t.ShapeSignatureAsNumpy().tolist() if t.ShapeSignatureLength() else [],dtype=types[t.Type()],buffer=t.Buffer(),quantization=None if not q else dict(scale=q.ScaleAsNumpy().tolist() if q.ScaleLength() else [],zero_point=q.ZeroPointAsNumpy().tolist() if q.ZeroPointLength() else [],quantized_dimension=q.QuantizedDimension()))
r=dict(identifier=b[4:8].decode(),version=m.Version(),description=s(m.Description()),subgraphs=[],signatures=[],metadata=[])
for j in range(m.SubgraphsLength()):
 g=m.Subgraphs(j); ts=[tensor(g,i) for i in range(g.TensorsLength())]; counts=collections.Counter()
 for i in range(g.OperatorsLength()):
  oc=m.OperatorCodes(g.Operators(i).OpcodeIndex()); counts[ops.get(oc.BuiltinCode(),str(oc.BuiltinCode()))+':v'+str(oc.Version())]+=1
 r['subgraphs'].append(dict(name=s(g.Name()),inputs=[tensor(g,int(i)) for i in g.InputsAsNumpy()],outputs=[tensor(g,int(i)) for i in g.OutputsAsNumpy()],tensor_count=len(ts),tensor_dtype_counts=dict(collections.Counter(t['dtype'] for t in ts)),quantized_tensors=[t for t in ts if t['quantization'] and t['quantization']['scale']],operators=dict(counts)))
for i in range(m.SignatureDefsLength()):
 d=m.SignatureDefs(i); r['signatures'].append(dict(key=s(d.SignatureKey()),subgraph=d.SubgraphIndex(),inputs=[dict(name=s(d.Inputs(k).Name()),index=d.Inputs(k).TensorIndex()) for k in range(d.InputsLength())],outputs=[dict(name=s(d.Outputs(k).Name()),index=d.Outputs(k).TensorIndex()) for k in range(d.OutputsLength())]))
for i in range(m.MetadataLength()):
 d=m.Metadata(i); data=m.Buffers(d.Buffer()).DataAsNumpy(); r['metadata'].append(dict(name=s(d.Name()),buffer=d.Buffer(),data=data.tolist() if not isinstance(data,int) else data))
(p/'static_graph.json').write_text(json.dumps(r,indent=2)); print(json.dumps(r,indent=2))
