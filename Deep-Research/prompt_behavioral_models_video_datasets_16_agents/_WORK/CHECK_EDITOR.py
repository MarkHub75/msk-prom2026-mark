from pathlib import Path
from urllib.parse import unquote, urlsplit
from collections import Counter
import re, json
root = Path(__file__).resolve().parent.parent
path = root / 'report_human_behavioral_models_video_data.md'
draft = (root / '_WORK/HUMAN_DRAFT.md').read_text(encoding='utf-8')
text = path.read_text(encoding='utf-8')
links = re.findall(r'(?<!!)\[[^\]]*\]\((<[^>]*>|[^\s)]+)\)', text)
failures = []
local = 0
for target in links:
    target = target.strip('<>')
    if urlsplit(target).scheme or target.startswith('//'):
        continue
    local += 1
    name, sep, anchor = target.partition('#')
    dest = root / unquote(name) if name else path
    if not dest.exists():
        failures.append({'missing_path': target})
    elif sep and not re.search(r'<a\s+id=[\'"]' + re.escape(unquote(anchor)) + r'[\'"]', dest.read_text(encoding='utf-8')):
        failures.append({'missing_anchor': target})
code = lambda t: set(re.findall(r'`([^`\n]+)`', t))
url = lambda t: set(re.findall(r'https?://[^\s<>)]*', t))
hexes = lambda t: set(re.findall(r'\b[a-f0-9]{40,64}\b', t))
refs = lambda t: set(re.findall(r'\b[FQKE]\d{3}\b', t))
checks = {
 'bytes': path.stat().st_size,
 'words_whitespace': len(text.split()),
 'markdown_links': len(links),
 'local_links_checked_from_final_root': local,
 'link_failures': failures,
 'missing_original_inline_code': sorted(code(draft) - code(text)),
 'missing_original_external_urls': sorted(url(draft) - url(text)),
 'missing_original_full_hashes_commits': sorted(hexes(draft) - hexes(text)),
 'missing_original_canonical_refs': sorted(refs(draft) - refs(text)),
 'scenarios_tables': {str(i): text.count(f'| **{i}.') for i in range(1,9)},
 'experiment_headings': re.findall(r'^### (E\d{3})\.', text, re.M),
 'three_routes': all(f'**Маршрут {i}:' in text for i in range(1,4)),
 'five_questions': all(re.search(rf'^{i}\. ', text, re.M) for i in range(1,6)),
 'placeholders': re.findall(r'\b(?:TODO|TBD|FIXME)\b|\{\{[^}]+\}\}|<!--.*?-->', text),
 'h1_count': len(re.findall(r'^# ', text, re.M)),
 'source_media_only_no_inference': 'Модели не исполнялись' in text,
 'mist_literal': 'mist video UNCONFIRMED' in text,
}
(root / '_WORK/EDITOR_CHECKS.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(checks, ensure_ascii=False, indent=2))
