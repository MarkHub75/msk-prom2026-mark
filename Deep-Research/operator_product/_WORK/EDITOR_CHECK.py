from pathlib import Path
from urllib.parse import unquote
import re
from collections import Counter

root = Path(__file__).resolve().parent.parent
p = root / 'report_human_operator_product.md'
raw = p.read_bytes()
text = raw.decode('utf-8', errors='strict')
draft = (root / '_WORK/AUTHOR_DRAFT.md').read_text(encoding='utf-8')
assert '\ufffd' not in text and '\x00' not in text
links = re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', text)
errors = []
local = []
for target in links:
    if re.match(r'^[a-z]+://', target, re.I):
        continue
    path, _, anchor = target.partition('#')
    resolved = (p.parent / unquote(path)).resolve() if path else p
    local.append(target)
    if not resolved.is_file():
        errors.append('Missing file: ' + target)
        continue
    if anchor:
        body = resolved.read_text(encoding='utf-8')
        if not re.search(r'<a\s+id=[\"\']' + re.escape(unquote(anchor)) + r'[\"\']', body):
            errors.append('Missing explicit anchor: ' + target)

def ids(s):
    return set(re.findall(r'\b[FSQE]\d{3}\b', s))
missing = sorted(ids(draft) - ids(text))
assert not missing, missing
expected_e = {f'{i:03}' for i in range(1,16)}
paragraphs = re.findall(r'^\*\*Проверка E(\d{3})[^\n]*', text, re.M)
assert set(paragraphs) == expected_e and len(paragraphs) == 15
assert len(re.findall(r'^\*\*Проверка E\d{3}[^\n]*; не выполнена\.\*\*', text, re.M)) == 15
groups = re.findall(r'^\| (\d+)\. [MC]:', text, re.M)
assert groups == [str(i) for i in range(1,18)], groups
headings = re.findall(r'^#{1,6} (.+)$', text, re.M)
repeated = [h for h,n in Counter(headings).items() if n > 1]
assert not repeated, repeated
assert not errors, errors
print(f'UTF8 OK: {len(raw)} bytes, {len(text)} chars, {len(text.split())} words')
print(f'Links OK: {len(links)} total, {len(local)} local targets/anchors; no network checks')
print(f'IDs preserved: {len(ids(draft))} original distinct F/S/Q/E; all 15 proposed checks; all 17 data groups')
print(f'Unique headings: {len(headings)}')
