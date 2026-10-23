"""Ordinary author checks for local artifact structure and references; no network."""
from pathlib import Path
import re
import json
import tomllib
import yaml

root = Path(__file__).resolve().parent.parent
names = ['SOURCES.md', 'RAW_FACTS.md', 'CRITIC.md', 'OPEN_QUESTIONS.md',
         'report_human_camera_calibration_geometry.md',
         'report_machine_camera_calibration_geometry.md']
docs = {name: (root/name).read_text(encoding='utf-8-sig') for name in names}
issues = []

def heading_anchors(content):
    anchors = set(re.findall(r'<a id="([^"]+)"', content))
    seen = {}
    for heading in re.findall(r'^#{1,6}\s+(.+)$', content, re.M):
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        index = seen.get(slug, 0)
        anchors.add(slug if index == 0 else f'{slug}-{index}')
        seen[slug] = index+1
    return anchors

for name, body in docs.items():
    if re.search(r'\bturn\d+(?:search|view|fetch)\d+', body):
        issues.append(f'{name}: internal browser reference')
    prose = re.sub(r'```.*?```', '', body, flags=re.S)
    prose = re.sub(r'`[^`]*`', '', prose)
    for url in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', prose):
        if url.startswith(('https://', 'http://', 'mailto:')):
            continue
        pathpart, _, anchor = url.partition('#')
        target = root/pathpart if pathpart else root/name
        if not target.exists():
            issues.append(f'{name}: missing local target {url}')
        elif anchor and target.suffix == '.md':
            if anchor not in heading_anchors(target.read_text(encoding='utf-8-sig')):
                issues.append(f'{name}: missing local anchor {url}')

for prefix, filename, count in [('f','RAW_FACTS.md',78), ('s','SOURCES.md',62)]:
    ids = re.findall(rf'<a id="({prefix}\d{{3}})"></a>', docs[filename])
    expected = [f'{prefix}{i:03}' for i in range(1,count+1)]
    if ids != expected:
        issues.append(f'{filename}: ID order/count mismatch')

machine = docs[names[-1]]
assert machine.startswith('---\n')
front = machine.split('---\n',2)[1]
metadata = yaml.safe_load(front)
required = {'topic','scope','not_covered','answers','keywords','entity_schema','takeaways',
            'checked_at','context_version','case_status','checks_performed',
            'human_report','evidence_files','open_questions_file'}
missing = required-set(metadata)
if missing:
    issues.append(f'YAML missing {sorted(missing)}')
if metadata['topic'] != 'camera_calibration_geometry':
    issues.append('YAML wrong topic')

pkg = json.loads((root/'_WORK/A06_EVIDENCE/opencv-python-headless_4.13.0.92_PYPI.json').read_text(encoding='utf-8-sig'))
norfair = tomllib.loads((root/'_WORK/A06_EVIDENCE/tryolabs_norfair_v2.3.0_pyproject.toml').read_text(encoding='utf-8-sig'))
result = {
    'issues': issues,
    'artifact_count': len(docs),
    'facts': 78, 'sources': 62,
    'yaml_valid': True,
    'answers': len(metadata['answers']),
    'opencv_numpy_manifest': [x for x in pkg['info']['requires_dist'] if x.lower().startswith('numpy')],
    'norfair_numpy_manifest': norfair['tool']['poetry']['dependencies']['numpy'],
    'files': {n: {'bytes': (root/n).stat().st_size, 'lines': len(t.splitlines())} for n,t in docs.items()}
}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(issues))
