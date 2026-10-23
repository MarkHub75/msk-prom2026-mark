"""Creation checks for this compressor's artifact; no network/product audit."""
from pathlib import Path
from collections import Counter
from urllib.parse import unquote, urlsplit
from datetime import datetime
import json
import re
import yaml

root = Path(__file__).resolve().parent.parent
report_path = root / 'report_machine_case_analytics.md'
report = report_path.read_text(encoding='utf-8', errors='strict')
human = (root / 'report_human_case_analytics.md').read_text(encoding='utf-8')
errors = []
match = re.match(r'\A---\n(.*?)\n---\n', report, re.S)
assert match, 'YAML front matter missing'

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'Duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
meta = yaml.load(match.group(1), Loader=UniqueLoader)
required = {'topic', 'scope', 'not_covered', 'answers', 'keywords', 'entity_schema',
            'takeaways', 'checked_at', 'context_version', 'case_material',
            'actually_checked', 'human_report', 'evidence_files', 'open_questions'}
assert required <= set(meta), f'Missing YAML fields: {required - set(meta)}'
assert meta['topic'] == 'case_analytics'
assert meta['context_version'] == 'mosprom-research-v1'
assert datetime.fromisoformat(meta['checked_at']).utcoffset().total_seconds() == 10800
for key in ('scope', 'not_covered', 'answers', 'keywords', 'takeaways'):
    assert isinstance(meta[key], list) and meta[key], key

def anchors(text):
    explicit = set(re.findall(r'<a\s+id="([^"]+)"', text))
    generated = {re.sub(r'[^\w\-\s]', '', heading.lower()).replace(' ', '-')
                 for heading in re.findall(r'^#{1,6} (.+)$', text, re.M)}
    return explicit | generated

for answer in meta['answers']:
    assert set(answer) == {'question', 'section'}
    assert answer['question'].endswith('?')
    assert answer['section'] in anchors(report), answer

evidence = {name: (root / name).read_text(encoding='utf-8') for name in
            ('SOURCES.md', 'RAW_FACTS.md', 'CRITIC.md', 'OPEN_QUESTIONS.md')}
canonical = set()
for text in evidence.values():
    canonical.update(re.findall(r'^#{1,3} ([SFQKE]\d{3})(?:\s|$)', text, re.M))
ids = set(re.findall(r'\b[SFQKE]\d{3}\b', report))
for identifier in sorted(ids - canonical):
    errors.append('Unknown canonical ID: ' + identifier)

links = re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', report)
local_count = external_count = 0
for target in links:
    if target.startswith(('https://', 'http://')):
        external_count += 1
        if not any(target in text for text in evidence.values()):
            errors.append('URL absent from preserved evidence: ' + target)
        continue
    local_count += 1
    filename, _, anchor = target.partition('#')
    dest = (root / unquote(filename)).resolve() if filename else report_path
    if not dest.exists():
        errors.append('Missing file: ' + target)
    elif anchor and anchor not in anchors(dest.read_text(encoding='utf-8')):
        errors.append('Missing anchor: ' + target)

metadata_paths = [meta['human_report'], meta['open_questions'], meta['compression_notes'],
                  meta['case_material']['source'], meta['case_material']['notes'],
                  *meta['evidence_files'].values()]
for target in metadata_paths:
    filename, _, anchor = target.partition('#')
    dest = root / filename
    if not dest.exists():
        errors.append('Missing metadata path: ' + target)
    elif anchor and anchor not in anchors(dest.read_text(encoding='utf-8')):
        errors.append('Missing metadata anchor: ' + target)

notes_path = root / '_WORK/COMPRESSION_NOTES.md'
notes = notes_path.read_text(encoding='utf-8', errors='strict')
notes_links = re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', notes)
for target in notes_links:
    filename, _, anchor = target.partition('#')
    dest = (notes_path.parent / unquote(filename)).resolve() if filename else notes_path
    if not dest.exists():
        errors.append('Missing notes link: ' + target)
    elif anchor and anchor not in anchors(dest.read_text(encoding='utf-8')):
        errors.append('Missing notes anchor: ' + target)

tables = re.findall(r'(?:^\|.*\n?)+', report, re.M)
catalog_tables = 0
schema = meta['entity_schema']['product_comparison']['columns']
for index, table in enumerate(tables, 1):
    rows = [[cell.strip() for cell in line.strip().strip('|').split('|')]
            for line in table.splitlines()]
    if len({len(row) for row in rows}) != 1:
        errors.append(f'Inconsistent table {index} columns')
    if rows[0][0] == 'Product / type':
        catalog_tables += 1
        if rows[0] != schema:
            errors.append(f'Catalog {index} differs from declared columns')
        if any(not cell for row in rows for cell in row):
            errors.append(f'Empty cell in catalog {index}')
assert catalog_tables == 2

for pattern in (r'turn\d+(?:search|view|fetch|file)', r'\uFFFD',
                r'(?<!\w)[A-Za-z]:[/\\]', r'\b(?:TODO|TBD|FIXME)\b',
                r'\.\.\.', r'[\x00-\x08\x0b\x0c\x0e-\x1f]'):
    if re.search(pattern, report):
        errors.append('Text hygiene match: ' + pattern)

expected = {'SOURCES.md', 'RAW_FACTS.md', 'CRITIC.md', 'OPEN_QUESTIONS.md',
            'report_human_case_analytics.md', 'report_machine_case_analytics.md'}
root_files = {path.name for path in root.iterdir() if path.is_file()}
inputs = {'Context-prompt.md', 'prompt-linq-case-analytics.md'}
pdfs = {name for name in root_files if name.lower().endswith('.pdf')}
if root_files != expected | inputs | pdfs or len(pdfs) != 1:
    errors.append('Unexpected final-root inventory: ' + str(sorted(root_files)))

# Explicit preservation cues; this is not a semantic or external-source audit.
cues = ['separate dispatcher', 'willingness to pay', 'as-is reconstruction',
        '20-30 minutes', '42 professional', '31 students', '122 professional',
        '495 conflict', '94 independent samples', '23,461', '5,334', '2,053',
        '20.8 thousand', '1.07 thousand', '5,974', '22.75%', '19.02%',
        '17.51%', '3.67%', '2.93 million', '770,400 RUB', '61,600 RUB',
        'Google Viewer', 'Byte identity', 'real-time classification',
        'K007', 'K008', 'H-A', 'H-B', 'T_on', 'T_clear',
        'one-to-one', 'N = T + F + U + X', 'confidence interval',
        'cutoff-L', 'A - P - O', 'q_saved', 'q_added', 'NOT RUN']
for cue in cues:
    if cue not in report:
        errors.append('Preservation cue missing: ' + cue)
assert set(f'E{i:03}' for i in range(1, 12)) <= ids

result = {
    'artifact': report_path.name,
    'yaml_parser': f'PyYAML {yaml.__version__} SafeLoader with duplicate-key rejection',
    'yaml_required_fields_checked': sorted(required),
    'answer_sections': len(meta['answers']),
    'words_report': len(report.split()), 'words_body': len(report[match.end():].split()),
    'words_human': len(human.split()),
    'bytes_utf8_report': len(report.encode('utf-8')),
    'bytes_utf8_human': len(human.encode('utf-8')),
    'local_links': local_count, 'external_url_occurrences': external_count,
    'notes_links': len(notes_links),
    'ids_by_prefix': {p: len([i for i in ids if i.startswith(p)]) for p in 'SFQKE'},
    'tables': len(tables), 'catalog_tables': catalog_tables,
    'catalog_rows': sum(len(t.splitlines()) - 2 for t in tables if '| Product / type |' in t),
    'final_root_files': sorted(root_files),
    'preservation_cues_checked': len(cues),
    'token_count': 'Not measured; no token compression ratio claimed.',
    'errors': errors,
    'scope': 'Own artifact creation checks only. No network, product run, legal approval, or independent final audit.'
}
(root / '_WORK/COMPRESSION_CHECK.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=True, indent=2))
if errors:
    raise SystemExit(1)
