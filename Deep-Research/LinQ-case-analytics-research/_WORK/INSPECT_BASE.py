import ASSEMBLE_BASE as a
for k,v in sorted(a.records.items(),key=lambda kv:len(kv[1]['text']),reverse=True)[:22]:
 print(k,len(v['text']),v['text'][:100].replace('\n',' '))
print('facts chars',sum(len(v['text']) for v in a.records.values() if v['type'] in ['F','I']))
print('Q chars',sum(len(v['text']) for v in a.records.values() if v['type']=='Q'))
