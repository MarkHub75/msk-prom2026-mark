from pathlib import Path
from urllib.parse import unquote
from datetime import datetime
import json
import re
import yaml

root = Path(__file__).resolve().parent.parent
path = root / 'report_machine_evaluation.md'
value = path.read_text(encoding='utf-8')
header, body = value.split('\n---\n', 1)
# Editorial spacing outside inline code; literals inside code are preserved.
parts = re.split(r'(`[^`]*`)', body)
for i in range(0, len(parts), 2):
    parts[i] = re.sub(r',(?=\S)', ', ', parts[i])
    parts[i] = re.sub(r'(?<=[A-Za-z]):(?=\d)', ': ', parts[i])
for i in range(1, len(parts), 2):
    parts[i] = '`' + parts[i][1:-1].strip() + '`'
    if i and parts[i-1] and parts[i-1][-1].isalnum():
        parts[i-1] += ' '
    if i+1 < len(parts) and parts[i+1] and parts[i+1][0].isalnum():
        parts[i+1] = ' ' + parts[i+1]
body = ''.join(parts)
body = body.replace('A.777778, B.833333', 'A=.777778, B=.833333')
value = header + '\n---\n' + body
path.write_text(value, encoding='utf-8', newline='\n')
data = yaml.safe_load(header.removeprefix('---\n'))
required = ['topic', 'scope', 'not_covered', 'answers', 'keywords', 'entity_schema', 'takeaways', 'checked_at', 'context_version', 'materials_and_access', 'verification_state', 'evidence_files']
assert all(k in data for k in required)
assert data['topic'] == 'evaluation'
assert data['context_version'] == 'mosprom-research-v1'
assert data['entity_schema'] is None
assert all(isinstance(x, str) and x.endswith('?') for x in data['answers'])
assert datetime.fromisoformat(data['checked_at']).utcoffset().total_seconds() == 10800
assert '\ufffd' not in value
assert not re.search(r'\bturn\d+(?:search|view|fetch)\d+\b|[A-Z]:[\\/]', value)
bad = []
local = external = 0
for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', value):
    if re.match(r'https?://', target):
        external += 1
        continue
    local += 1
    name, _, fragment = unquote(target).partition('#')
    destination = (root / name).resolve() if name else path
    if not destination.exists():
        bad.append({'target': target, 'reason': 'missing path'})
    elif fragment and destination.is_file():
        text = destination.read_text(encoding='utf-8')
        if f'id="{fragment}"' not in text:
            bad.append({'target': target, 'reason': 'missing explicit anchor'})
ids = {}
for prefix, filename in [('F', 'RAW_FACTS.md'), ('S', 'SOURCES.md'), ('Q', 'OPEN_QUESTIONS.md'), ('E', 'OPEN_QUESTIONS.md'), ('K', 'CRITIC.md')]:
    found = set(re.findall(rf'\b{prefix}\d{{3}}\b', value))
    source = (root / filename).read_text(encoding='utf-8')
    missing = sorted(x for x in found if f'id="{x.lower()}"' not in source)
    ids[prefix] = {'unique_references': len(found), 'missing': missing}
assert not bad, bad
assert all(not row['missing'] for row in ids.values()), ids
assert len(re.findall(r'^---$', value, re.M)) == 2
print(json.dumps({'yaml': 'parsed; required fields, actual question strings and timezone checked', 'markdown_links': {'local': local, 'external': external, 'broken_local': bad}, 'normalized_ids': ids, 'utf8_replacement_characters': 0, 'temporary_absolute_or_browser_refs': 0, 'bytes': path.stat().st_size, 'lines': len(value.splitlines())}, ensure_ascii=False, indent=2))
