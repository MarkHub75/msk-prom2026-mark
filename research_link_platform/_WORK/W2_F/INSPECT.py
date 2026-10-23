from pathlib import Path
import json,hashlib,datetime,re
P=Path(__file__).parent
R=P.parent
specs={
 'BUILDER':(P/'BUILDER.TXT',r'percentile|thresholds|summary =|metadata_out|memmap|calibration_data|quantized_model.save'),
 'BINDINGS':(R/'W1_13/SOURCE/pytpu-15.0.24/pytpu/_bindings.py',r'class ProcessingMode|RAW =|FULL =|def _run|def sync|def _load_inference|def _get_inference|def _is_raw|user_dtype|user_shape|mode.value'),
 'DEQUANTIZATION':(R/'W1_13/SOURCE/iva_applications-11.0.1/src/iva_applications/dequantization.py',r'def |pos_scale|pos_shift|return '),
 'GUIDE':(R/'W1_03/Framework_manual_H1_extracted.txt',r'percentile|rescale|HardwareNetwork|SoftwareNetwork|load\(|save\(|TLM|порог'),
}
out={}
for key,(path,pattern) in specs.items():
 data=path.read_bytes()
 txt=data.decode('utf-8')
 out[key]={'path':str(path),'sha256':hashlib.sha256(data).hexdigest(),'locators':[{'line':i,'text':l} for i,l in enumerate(txt.splitlines(),1) if re.search(pattern,l)]}
out['HEAD']=json.loads((P/'COMMITS.TXT').read_text())[0]['sha']
out['generated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(P/'LOCAL_LOCATORS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('Saved LOCAL_LOCATORS.json; no SDK execution')
