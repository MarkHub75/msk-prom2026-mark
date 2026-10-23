import sys,zipfile,pickletools
f=sys.argv[1]
z=zipfile.ZipFile(f)
n=[x for x in z.namelist() if x.endswith('data.pkl')][0]
data=z.read(n)
toks=[]
for op,arg,pos in pickletools.genops(data):
    if op.name in('SHORT_BINUNICODE','BINUNICODE','UNICODE','BINSTRING','SHORT_BINSTRING','STRING','GLOBAL','STACK_GLOBAL') or op.name.startswith('BIN') and isinstance(arg,(int,float)):
        toks.append((op.name,arg))
S=[a for o,a in toks if isinstance(a,str)]
# print globals
glob=sorted({a for o,a in toks if o=='GLOBAL'})
print("GLOBALS(ultra/yolo-related):",[g for g in glob if 'ultra' in g.lower() or 'yolo' in g.lower() or 'models' in g.lower()][:15])
def after(key,k=30):
    for i,s in enumerate(S):
        if s==key:
            print(key,'->',S[i+1:i+1+k]); return
    print(key,'not found')
for key in ['names','date','version','license','docs','train_args','nc']: after(key,40 if key in('names','train_args') else 4)
