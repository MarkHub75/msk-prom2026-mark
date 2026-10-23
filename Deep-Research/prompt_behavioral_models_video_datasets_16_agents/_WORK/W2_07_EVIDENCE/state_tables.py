import pathlib,json,collections,numpy as np,tflite
p=pathlib.Path('_WORK/W2_07_EVIDENCE')
for stem in ['static_graph','int8_static_graph']:
 r=json.loads((p/(stem+'.json')).read_text()); sig=r['signatures'][0]; g=r['subgraphs'][0]; ins={x['index']:x for x in g['inputs']}; outs={x['index']:x for x in g['outputs']}; om={x['name']:x['index'] for x in sig['outputs']}; lines=['| State / input | Input index | Output index | Shape | Dtype | Match |','|---|---:|---:|---|---|---|']; counts=collections.Counter(); size=0
 for x in sig['inputs']:
  name=x['name']; ti=ins[x['index']]; oi=om.get(name); to=outs.get(oi); match=to is not None and ti['shape']==to['shape'] and ti['dtype']==to['dtype']; lines.append(f"| `{name}` | {x['index']} | {oi} | `{ti['shape']}` | {ti['dtype']} | {'yes' if match else 'image only'} |"); counts['identity_states' if oi==x['index'] else 'different_index']+=1
  if name!='image': size+=int(np.prod(ti['shape']))*4
 (p/(stem+'_state_table.md')).write_text('\n'.join(lines)); print(stem,counts,'state_bytes',size); print('identity',[x['name'] for x in sig['inputs'] if om.get(x['name'])==x['index']]); print('logits',[(x,outs[x['index']]) for x in sig['outputs'] if x['name']=='logits'])
