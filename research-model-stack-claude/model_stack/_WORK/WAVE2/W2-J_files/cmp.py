import json,re,ast
n=json.load(open('names_objv1.json'))['names']
src=open('mm365.py',encoding='utf-8').read()
v1=src[src.index('class Objects365V1Dataset'):src.index('class Objects365V2Dataset')]
m=re.search(r"'classes':\s*\((.*?)\)\s*,\s*'palette'",v1,re.S)
mm=ast.literal_eval('('+m.group(1)+')')
y=open('o365.yaml',encoding='utf-8').read()
yn=[]
for l in y.split('names:')[1].splitlines():
    mt=re.match(r'\s+(\d+):\s*(.+?)\s*$',l)
    if mt: yn.append(mt.group(2))
print(len(n),len(mm),len(yn))
print('objv1==mmdetV1 (exact order):',n==list(mm))
print('objv1==ultralytics Objects365.yaml:',n==yn)
d=[(i,a,b) for i,(a,b) in enumerate(zip(n,mm)) if a!=b]
print(len(d),d[:15])
d2=[(i,a,b) for i,(a,b) in enumerate(zip(n,yn)) if a!=b]; print(len(d2),d2[:15])
print(n[:5],n[-3:])
