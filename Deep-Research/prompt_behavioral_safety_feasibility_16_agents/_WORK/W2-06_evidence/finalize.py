from pathlib import Path
import json,hashlib
r=Path('_WORK/W2-06_evidence');p=Path('_WORK/W2-06.md');s=p.read_text(encoding='utf-8-sig');s=s.replace('31823966 / полный SHA в downloads.json','31823966 / `5ebaf97bd9cea68804d3da5872de778261c23a7ff8ae6299d8830e0f3fcafb60`');s=s.replace('FIRESENSE database of videos for flame and smoke detection, v1, DOI10.5281/zenodo.836749, CC BY4.0;','Nikos Grammalidis, Kosmas Dimitropoulos, Enis Cetin — FIRESENSE database of videos for flame and smoke detection, v1 (31.07.2017), DOI10.5281/zenodo.836749, CC BY4.0 (https://creativecommons.org/licenses/by/4.0/);');s=s.replace('creator names взять без сокращения из сохранённого metadata при упаковке credits.','Creator names сверены с primary metadata и включены выше.');p.write_text(s,encoding='utf-8')
(r/'README.md').write_text('''# W2-06 evidence, 2026-10-23
Only static research. No model inference, torch.load, pickle.load, export, compiler, device calls, or application. Existing PyAV/PIL decoded media; own scripts downloaded bounded source/media and statically disassembled ZIP pickle instructions.

- downloads.json: full FURG MP4/XML and HF PT/card URLs, bytes, SHA256.
- decode_manifest.json + *_pts.csv + all-frame sheets + *_detail.jpg: full FURG decode, original XML overlays; original GT retained, known errors are described in ../W2-06.md.
- checkpoint_static.json + metadata_locators.json + *_dis.txt: safe static PT inspection; GLOBAL/REDUCE printed, not executed.
- sources.json + versioned source files: primary source dependencies, AGPL license, export/head/letterbox references.
- firesense_range.json/members.json/acquired.json + firesense_record.json: primary ZIP Range extraction, member CRC/hash/decode and CC BY4 metadata. Whole ZIP not acquired or hashed.
- r3e6_tree.json: full pinned tree; no license/copying/notice paths found. Reference only.
- artifact_hashes.json: current local non-image evidence hashes; not a publisher signature.

Video/model/license grants remain artifact/action specific; do not automatically publish this folder. See ../W2-06.md for review observations, rights scope, scenario contract, and open gates.
''',encoding='utf-8')
files=[{'file':q.name,'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for q in sorted(r.iterdir()) if q.is_file() and q.name!='artifact_hashes.json'];(r/'artifact_hashes.json').write_text(json.dumps(files,indent=2))
print('report',p.stat().st_size,'evidence files',len(files));print('replacement char',s.count('\ufffd'))
