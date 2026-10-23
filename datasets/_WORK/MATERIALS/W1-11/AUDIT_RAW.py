"""Reproduce structural counts only; never infers semantic correctness."""
from pathlib import Path
import collections
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile

root = Path(__file__).resolve().parent
archive = root / 'SH17-raw.zip'
counts = collections.Counter()
filenames = []
parse_errors = []
geometry_errors = []
empty_xml = []
flags = collections.Counter()
with zipfile.ZipFile(archive) as bundle:
    for member in bundle.namelist():
        if not member.endswith('.xml'):
            continue
        try:
            tree = ET.fromstring(bundle.read(member))
            filenames.append(tree.findtext('filename'))
            width = int(tree.findtext('size/width'))
            height = int(tree.findtext('size/height'))
            objects = tree.findall('object')
            if not objects:
                empty_xml.append(member)
            for obj in objects:
                name = obj.findtext('name')
                counts[name] += 1
                box = obj.find('bndbox')
                values = [int(box.findtext(key)) for key in ('xmin','ymin','xmax','ymax')]
                flags[str((obj.findtext('truncated'), obj.findtext('difficult')))] += 1
                if (values[0] >= values[2] or values[1] >= values[3]
                        or min(values) < 0 or values[2] > width or values[3] > height):
                    geometry_errors.append({'file': member, 'name': name,
                                            'bbox': values, 'size': [width, height]})
        except Exception as exc:
            parse_errors.append([member, str(exc)])
result = {'archive_bytes': archive.stat().st_size,
          'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
          'xml_files': len(filenames), 'unique_image_filenames': len(set(filenames)),
          'object_count': sum(counts.values()), 'classes': dict(counts),
          'parse_errors': parse_errors, 'geometry_errors': geometry_errors,
          'empty_xml': empty_xml, 'flags': dict(flags)}
(root / 'RAW_REPRODUCED.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps({key: result[key] for key in ('xml_files','object_count','sha256')}))
