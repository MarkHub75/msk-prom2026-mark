"""Local editorial checks for the machine report; no network or dataset execution."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import re
import unicodedata
from urllib.parse import unquote
import yaml

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / 'report_machine_datasets.md'

class UniqueLoader(yaml.SafeLoader):
    pass

def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'Duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)

def slug(value):
    value = re.sub(r'<[^>]+>', '', value)
    value = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', value)
    value = value.replace('`', '').lower().strip()
    value = ''.join(c for c in value if c in '-_ ' or unicodedata.category(c)[0] in 'LN')
    return re.sub(r'\s', '-', value)

def anchors(path):
    s = path.read_text(encoding='utf-8-sig')
    found = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', s))
    counts = collections.Counter()
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', s, re.M):
        a = slug(title)
        n = counts[a]
        counts[a] += 1
        found.add(a + (f'-{n}' if n else ''))
    return found

def run():
    s = REPORT.read_text(encoding='utf-8')
    match = re.match(r'\A---\n(.*?)\n---\n', s, re.S)
    assert match, 'Missing front matter'
    front = yaml.load(match[1], Loader=UniqueLoader)
    body = s[match.end():]
    required = ['topic', 'scope', 'not_covered', 'answers', 'keywords', 'entity_schema',
                'takeaways', 'checked_at', 'timezone', 'context_version', 'research_snapshot',
                'case_material_state', 'actual_checks', 'files', 'human_freeze']
    assert all(k in front for k in required)
    assert front['topic'] == 'datasets' and front['context_version'] == 'mosprom-research-v1'
    assert datetime.datetime.fromisoformat(front['checked_at']).utcoffset() is not None
    assert front['timezone'] == 'Europe/Moscow'
    for field in ['answers', 'not_covered', 'keywords', 'takeaways']:
        assert isinstance(front[field], list) and all(isinstance(v, str) and v for v in front[field])
    assert len(front['answers']) == len(set(front['answers']))
    for path in front['files'].values():
        assert (ROOT / path).is_file(), path

    errors = []
    local_links = 0
    for label, raw in re.findall(r'\[([^\]]*)\]\(([^)]+)\)', s):
        target = raw.strip().strip('<>')
        if re.match(r'https?://', target):
            continue
        assert not re.match(r'(?:[A-Za-z]:|file:|/)', target), target
        path, _, anchor = unquote(target).partition('#')
        dest = (ROOT / path) if path else REPORT
        local_links += 1
        if not dest.exists():
            errors.append(f'Missing local target: {target}')
        elif anchor and (not dest.is_file() or anchor not in anchors(dest)):
            errors.append(f'Missing anchor: {target}')

    ids = {kind: sorted(set(re.findall(rf'\b{kind}\d{{3}}\b', s))) for kind in 'FSQEK'}
    registry = {'F': 'RAW_FACTS.md', 'S': 'SOURCES.md', 'Q': 'OPEN_QUESTIONS.md',
                'E': 'OPEN_QUESTIONS.md', 'K': 'CRITIC.md'}
    for kind, values in ids.items():
        allowed = set(re.findall(rf'\b{kind}\d{{3}}\b', (ROOT / registry[kind]).read_text(encoding='utf-8')))
        errors.extend(f'Unknown ID: {v}' for v in values if v not in allowed)
    assert not re.search(r'\bturn\d+(?:search|fetch|view)\d+', s)
    assert not re.search(r'(?:D:|C:)[/\\]', s)
    fences = re.findall(r'^```([^\n]*)$', body, re.M)
    assert len(fences) % 2 == 0
    for code in re.findall(r'^```yaml\n(.*?)^```', body, re.M | re.S):
        yaml.load(code, Loader=UniqueLoader)

    tables = []
    lines = body.splitlines()
    index = 0
    while index < len(lines):
        if lines[index].startswith('|'):
            rows = []
            start = index
            while index < len(lines) and lines[index].startswith('|'):
                rows.append([v.strip() for v in lines[index].strip().strip('|').split('|')])
                index += 1
            width = len(rows[0])
            assert all(len(r) == width and all(r) for r in rows), f'Table width/empty at {start}'
            tables.append({'header': rows[0], 'rows': len(rows) - 2})
            schema = next((name for name, value in front['entity_schema'].items()
                           if list(value['fields']) == rows[0]), None)
            if schema:
                fields = front['entity_schema'][schema]['fields']
                for row in rows[2:]:
                    record = dict(zip(rows[0], row))
                    if schema == 'mapping_record':
                        assert record['relation'] in {'conditional', 'partial', 'incompatible', 'not_annotated'}
                    for name, typ in fields.items():
                        if typ == 'integer':
                            assert re.fullmatch(r'\d+', record[name])
                        elif typ == 'number':
                            float(record[name])
                    if 'facts' in record:
                        assert re.search(r'\[F\d{3}\]\(RAW_FACTS.md#f\d{3}\)', record['facts'])
                tables[-1]['schema'] = schema
        else:
            index += 1
    for name in front['entity_schema']:
        assert sum(t.get('schema') == name for t in tables) == 1, f'Schema table mismatch: {name}'

    evidence_freeze = json.loads((ROOT / '_WORK/COLLECTOR_FREEZE.json').read_text(encoding='utf-8-sig'))
    frozen = {}
    for path, record in evidence_freeze['files'].items():
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        frozen[path] = actual == record['sha256']
        assert frozen[path], f'Frozen evidence changed: {path}'
    human = (ROOT / front['files']['human']).read_bytes()
    assert hashlib.sha256(human).hexdigest() == front['human_freeze']['sha256']
    assert len(human) == front['human_freeze']['bytes']
    assert len(human.decode('utf-8').splitlines()) == front['human_freeze']['lines']
    assert len(human.decode('utf-8').split()) == front['human_freeze']['whitespace_words']
    result = {
        'freeze': not errors,
        'checked_at': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).isoformat(),
        'role': 'machine compressor, integrated local editorial checks; no separate auditor',
        'report': REPORT.name, 'bytes': REPORT.stat().st_size,
        'lines': len(s.splitlines()), 'whitespace_words': len(s.split()),
        'sha256': hashlib.sha256(REPORT.read_bytes()).hexdigest(),
        'yaml_required_fields_and_duplicate_keys': 'passed',
        'answers_count': len(front['answers']), 'schemas_and_tables': tables,
        'manual_answer_coverage': 'All 14 indexed questions reviewed against the body; unresolved answers explicitly linked to Q001-Q020.',
        'local_links_checked': local_links, 'link_errors': errors,
        'identifier_counts': {k: len(v) for k, v in ids.items()},
        'frozen_human_unchanged': True, 'frozen_evidence_unchanged': frozen,
        'token_counts': None,
        'limits': 'No tokenization, network revalidation, visual Markdown rendering, dataset audit, model run or legal clearance performed by compressor.'
    }
    (ROOT / '_WORK/COMPRESSION_FREEZE.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    assert not errors, errors

if __name__ == '__main__':
    run()
