import urllib.request,json,zipfile,io,pathlib
p=pathlib.Path(__file__).parent
data=json.load(urllib.request.urlopen('https://pypi.org/pypi/onnx/1.17.0/json'))
u=next(x['url'] for x in data['urls'] if 'cp311-cp311-win_amd64' in x['filename'])
b=urllib.request.urlopen(u).read(); z=zipfile.ZipFile(io.BytesIO(b))
for name in ['onnx/onnx_ml_pb2.py']:
 (p/'ONNX_ML_PB2.py').write_bytes(z.read(name))
print(u)
