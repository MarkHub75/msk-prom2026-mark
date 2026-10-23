from pathlib import Path
from collections import Counter
import re
from urllib.parse import unquote, urlsplit
import json

root = Path(__file__).resolve().parent.parent
report = (root / 'report_human_case_analytics.md').read_text(encoding='utf-8')
draft = (root / '_WORK/AUTHOR_DRAFT.md').read_text(encoding='utf-8')
errors = []
files = {name: (root / name).read_text(encoding='utf-8') for name in
         ('RAW_FACTS.md', 'SOURCES.md', 'CRITIC.md', 'OPEN_QUESTIONS.md')}
canonical = {}
for content in files.values():
    for match in re.finditer(r'^#{1,3} ([SFQKE]\d{3})(?:\s|$)', content, re.M):
        canonical[match.group(1)] = True

links = re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', report)
local_count = external_count = 0
for target in links:
    if target.startswith(('https://', 'http://')):
        external_count += 1
        if target not in files['SOURCES.md'] and target not in files['RAW_FACTS.md']:
            errors.append('External URL absent from preserved base: ' + target)
        continue
    local_count += 1
    filename, _, anchor = target.partition('#')
    dest = (root / unquote(filename)).resolve() if filename else root / 'report_human_case_analytics.md'
    if not dest.exists():
        errors.append('Missing file: ' + target)
        continue
    if anchor:
        content = dest.read_text(encoding='utf-8')
        headings = re.findall(r'^#{1,6} (.+)$', content, re.M)
        anchors = {re.sub(r'[^\w\-\s]', '', heading.lower()).replace(' ', '-') for heading in headings}
        if anchor not in anchors:
            errors.append('Missing anchor: ' + target)

ids = set(re.findall(r'\b[SFQKE]\d{3}\b', report))
for identifier in sorted(ids):
    if identifier not in canonical:
        errors.append('Unknown canonical ID: ' + identifier)

draft_ids = set(re.findall(r'\b[SFQKE]\d{3}\b', draft))
lost_ids = sorted(draft_ids - ids)
if lost_ids:
    errors.append('Identifiers lost in editing: ' + ', '.join(lost_ids))

def urls(content):
    return Counter(re.findall(r'\]\((https?://[^)\n]+)\)', content))
lost_urls = urls(draft) - urls(report)
if lost_urls:
    errors.append('Direct URLs lost: ' + str(lost_urls))

def numbers(content):
    content = re.sub(r'\]\([^\n)]+\)', ']', content)
    content = re.sub(r'\b[SFQKE]\d{3}\b', '', content)
    return Counter(re.findall(r'(?<!\w)\d+(?:[.,]\d+)*(?:[%₽]|\b)', content))

# Verify every Markdown table has a consistent number of cells.
blocks = re.findall(r'(?:^\|.*\n?)+', report, re.M)
for block_no, block in enumerate(blocks, 1):
    cells = [len(line.strip().strip('|').split('|')) for line in block.splitlines()]
    if len(set(cells)) != 1:
        errors.append(f'Uneven table {block_no}: {cells}')

for pattern in (r'\]\(\.\./', r'\]\(CASE_NOTES\.md', r'turn\d+(?:search|view|fetch)', r'(?<!\w)[A-Za-z]:[/\\]'):
    if re.search(pattern, report):
        errors.append('Forbidden or unmoved path/token pattern: ' + pattern)

result = {
    'artifact': 'report_human_case_analytics.md',
    'words_draft': len(draft.split()), 'words_report': len(report.split()),
    'bytes_utf8': len(report.encode('utf-8')),
    'local_links': local_count, 'external_links': external_count,
    'ids_by_prefix': {prefix: len([i for i in ids if i.startswith(prefix)]) for prefix in 'SFQKE'},
    'tables': len(blocks), 'lost_ids': lost_ids,
    'numeric_literals_removed': dict(numbers(draft) - numbers(report)),
    'numeric_literals_added': dict(numbers(report) - numbers(draft)),
    'errors': errors,
    'scope': 'Own-artifact link/identifier/preservation check; no network or product tests.'
}
(root / '_WORK/EDITOR_CHECK.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
if errors:
    raise SystemExit(1)
