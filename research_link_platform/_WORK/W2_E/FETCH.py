import concurrent.futures, datetime, hashlib, json, pathlib, urllib.request
ROOT=pathlib.Path(__file__).parent
URLS={
 'HF_API.JSON':'https://huggingface.co/api/models/onnxmodelzoo/tiny-yolov3-11',
 'ONNX_API.JSON':'https://api.github.com/repos/onnx/models/commits/main',
 'DARKNET_API.JSON':'https://api.github.com/repos/pjreddie/darknet/commits/master',
 'tiny-yolov3-11.onnx':'https://huggingface.co/onnxmodelzoo/tiny-yolov3-11/resolve/main/tiny-yolov3-11.onnx',
 'yolov3-tiny.weights':'https://data.pjreddie.com/files/yolov3-tiny.weights',
 'yolov3-tiny.cfg':'https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg',
 'DARKNET_IMAGE.C':'https://raw.githubusercontent.com/pjreddie/darknet/master/src/image.c',
 'DARKNET_LICENSE':'https://raw.githubusercontent.com/pjreddie/darknet/master/LICENSE',
 'ONNX_README.MD':'https://raw.githubusercontent.com/onnx/models/main/validated/vision/object_detection_segmentation/tiny-yolov3/README.md',
 'HF_README.MD':'https://huggingface.co/onnxmodelzoo/tiny-yolov3-11/raw/main/README.md',
 'OMZ_README.MD':'https://raw.githubusercontent.com/openvinotoolkit/open_model_zoo/master/models/public/yolo-v3-tiny-onnx/README.md',
}
def fetch(item):
 name,url=item; r={'file':name,'url':url,'started':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Research-source-inspection'}),timeout=60) as response:
   data=response.read(80*1024*1024); r.update(status=response.status,final_url=response.url,size=len(data),sha256=hashlib.sha256(data).hexdigest()); (ROOT/name).write_bytes(data)
 except Exception as e:r['error']=repr(e)
 r['finished']=datetime.datetime.now(datetime.timezone.utc).isoformat(); return r
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: results=list(pool.map(fetch,URLS.items()))
(ROOT/'FETCH_LOG.JSON').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps([{k:v for k,v in r.items() if k!='final_url'} for r in results],indent=2))
