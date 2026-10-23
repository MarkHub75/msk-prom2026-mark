"""Read saved W1 archives only; never import vendor code or install packages."""
from pathlib import Path
import hashlib, json, tarfile, datetime

root = Path(__file__).resolve().parents[1] / 'W1_13'
result = {'access_time': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'method':'read-only archive inspection; no imports or SDK execution', 'archives':[]}
for name in ['PYTPU-15.0.24.TAR.GZ', 'IVA_APPLICATIONS-11.0.1.TAR.GZ', 'IVA-TPU-11.2.6.TAR.GZ']:
    p = root / name
    record = {'file':str(p), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    with tarfile.open(p) as tf:
        names = tf.getnames()
        record['members']=names
        record['license_candidates']=[n for n in names if any(k in Path(n).name.lower() for k in ['license','copying','eula','notice'])]
        record['native_members']=[n for n in names if n.endswith(('.so','.dll','.deb','.rpm','.whl'))]
        record['metadata']={}
        for n in names:
            if n.endswith(('PKG-INFO','requires.txt','entry_points.txt','setup.py','LICENSE')):
                text=tf.extractfile(n).read().decode('utf-8',errors='replace')
                record['metadata'][n]=text
    result['archives'].append(record)
(Path(__file__).parent/'SAVED_ARCHIVE_INSPECTION.JSON').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{k:v for k,v in x.items() if k not in ['members','metadata']} for x in result['archives']],ensure_ascii=False,indent=2))
