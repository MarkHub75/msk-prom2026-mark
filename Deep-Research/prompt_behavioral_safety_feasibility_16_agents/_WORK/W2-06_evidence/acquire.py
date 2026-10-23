import requests,pathlib,json
r=pathlib.Path('_WORK/W2-06_evidence')
u='https://api.github.com/repos/steffensbola/furg-fire-dataset/git/trees/6aff09d7baa27425f31d1df685284c26cbffe7af?recursive=1'
j=requests.get(u,timeout=30).json();(r/'tree.json').write_text(json.dumps(j,indent=2))
print([(x['path'],x.get('size')) for x in j['tree'] if x['path'].endswith('.mp4')])
