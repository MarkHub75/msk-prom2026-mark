from pathlib import Path
from urllib.parse import unquote, urlsplit
from collections import Counter
import datetime, hashlib, json, re
import yaml

root = Path(__file__).resolve().parent.parent
path = root / 'report_machine_behavioral_models_video_data.md'
text = path.read_text(encoding='utf-8')
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).isoformat(timespec='seconds')
text = re.sub(r"^checked_at: .*", "checked_at: '" + now + "'", text, count=1, flags=re.M)
path.write_text(text, encoding='utf-8', newline='\n')
parts = text.split('---', 2)
front = yaml.safe_load(parts[1])
body = parts[2]
required = ['topic', 'scope', 'not_covered', 'answers', 'keywords', 'entity_schema', 'takeaways', 'checked_at', 'context_version']
evidence_names = ['SOURCES.md', 'RAW_FACTS.md', 'CRITIC.md', 'OPEN_QUESTIONS.md']
cache = {name: (root / name).read_text(encoding='utf-8') for name in evidence_names}
evidence = '\n'.join(cache.values())
human = (root / 'report_human_behavioral_models_video_data.md').read_text(encoding='utf-8')
links = re.findall(r'(?<!!)\[[^\]]*\]\((<[^>]*>|[^\s)]+)\)', text)
failures = []
local_count = 0
for target in links:
    target = target.strip('<>')
    if urlsplit(target).scheme or target.startswith('//'):
        continue
    local_count += 1
    name, sep, anchor = target.partition('#')
    dest = root / unquote(name) if name else path
    if not dest.exists():
        failures.append({'missing_path': target})
    elif sep:
        target_text = dest.read_text(encoding='utf-8-sig')
        if not re.search(r'<a\s+id=[\'"]' + re.escape(unquote(anchor)) + r'[\'"]', target_text):
            failures.append({'missing_anchor': target})

refs = set(re.findall(r'\b[FSQKE]\d{3}\b', body))
refs -= {'K400', 'K600', 'K700'}  # Kinetics corpus names, not critic IDs.
canonical_anchors = set(re.findall(r'<a id="([FSQKE]\d{3})"></a>', evidence))
missing_refs = sorted(refs - canonical_anchors)
hexes = set(re.findall(r'\b[a-f0-9]{40,64}\b', body))
missing_hexes = sorted(h for h in hexes if h not in evidence and h not in human)
urls = set(re.findall(r'https?://[^\s<>)]*', body))
novel_urls = sorted(u for u in urls if u not in evidence and u not in human)

schemas = front['entity_schema']
expected = {name: item['fields'] for name, item in schemas.items()}
observed_tables = []
lines = body.splitlines()
for i, line in enumerate(lines[:-1]):
    if line.startswith('|') and re.match(r'^\|[-| :]+\|$', lines[i+1]):
        header = [v.strip() for v in line.strip('|').split('|')]
        count = 0
        for row in lines[i+2:]:
            if not row.startswith('|'):
                break
            count += 1
            if len(row.strip('|').split('|')) != len(header):
                failures.append({'table_row_width': row[:150]})
        observed_tables.append({'header': header, 'rows': count})
schema_match = {name: [t['rows'] for t in observed_tables if t['header'] == fields] for name, fields in expected.items()}
answers = {a.split(':',1)[0]: a for a in front['answers']}
coverage = {}
headings = list(re.finditer(r'^# (A\d{2}) — .+$', body, re.M))
for i, h in enumerate(headings):
    segment = body[h.end():headings[i+1].start() if i+1 < len(headings) else len(body)]
    coverage[h.group(1)] = {'words': len(segment.split()), 'has_fact_link': bool(re.search(r'RAW_FACTS.md#F\d{3}', segment))}

six = evidence_names + ['report_human_behavioral_models_video_data.md', 'report_machine_behavioral_models_video_data.md']
root_markdown = sorted(p.name for p in root.glob('*.md'))
allowed_inputs = ['Context-prompt.md', 'prompt_behavioral_models_video_datasets_16_agents.md']
unexpected = sorted(set(root_markdown) - set(six) - set(allowed_inputs))
boundaries = {
 'no_model_or_device_execution': 'No neural inference, tracker/event execution, training, export, compilation, benchmark reproduction or LinQ run occurred.' in text,
 'phone_work_or_movement': 'or movement through the workshop' in text,
 'phone_reserve_concurrence': 'concurrent walking/use not established' in text and 'phone reserve' in text,
 'mist_unconfirmed': 'Mist video UNCONFIRMED' in text,
 'four_file_horizon_not_corpus': 'these four' in text and 'not corpus-wide' in text,
 'source_test_demoted': 'now development' in text,
 'fall_stream_relative': '(PTS−stream.start_time)*time_base' in text and 'missing-tail diagnosis is superseded' in text,
 'gait_repeated_pts_new_images': 'new images' in text and 'synthetic evaluation time, not recovered capture time' in text,
 'behave_group_labels': 'group interactions, not dense individual gait' in text,
 'positive_grants_and_scope': 'Positive CC BY4/card/download evidence coexists' in text and 'GMD repository MIT/Zenodo CC BY4' in text,
 'upt_bsd_utility_mit': 'UPT code BSD-3-Clause; HICO utility MIT is separate' in text,
 'routine_truck_not_risk': 'routine passage/co-presence' in text and 'not certified near-miss' in text,
 'movinet_architecture_io_prefix': 'Different architecture from float' in text and 'buffers/logits FLOAT32, counters INT32' in text and 'prefix since reset' in text,
 'proposed_eight_stages': all(f'**[E{i:03}]' in text for i in range(1,9)),
 'five_questions': all(re.search(rf'^{i}\. ', body, re.M) for i in range(1,6)),
 'root_settings_not_claimed_changed': 'could not be switched in-session' in text,
 'no_extra_hazard_invented': 'no second complete extension is established' in text,
 'no_arbitrary_budget': 'no arbitrary percentage is invented' in text,
}
duplicates = dict(Counter(re.findall(r'<a id="([^"]+)"></a>', text)))
duplicates = {k:v for k,v in duplicates.items() if v > 1}
checks = {
 'checked_at': now,
 'role': 'Final compressor own text/schema/integrity checks; not a separate final auditor or model test',
 'bytes': path.stat().st_size,
 'words_whitespace': len(text.split()),
 'human_bytes': len(human.encode('utf-8')),
 'human_words_whitespace': len(human.split()),
 'yaml_parsed': isinstance(front, dict),
 'yaml_missing_required_fields': sorted(set(required) - set(front)),
 'topic_and_context_correct': front['topic'] == 'behavioral_models_video_data' and front['context_version'] == 'mosprom-research-v1',
 'checked_at_timezone': str(front['checked_at']).endswith('+03:00'),
 'answers_body_coverage': coverage,
 'answers_missing_heading': sorted(set(answers) - set(coverage)),
 'schema_table_matches': schema_match,
 'all_tables_declared': all(t['header'] in expected.values() for t in observed_tables),
 'table_row_counts': observed_tables,
 'markdown_links': len(links),
 'local_links_checked': local_count,
 'link_or_table_failures': failures,
 'missing_canonical_references': missing_refs,
 'duplicate_explicit_ids': duplicates,
 'full_hashes_commits_not_in_evidence': missing_hexes,
 'external_urls_not_in_saved_evidence': novel_urls,
 'six_final_names_exist': {n: (root/n).is_file() for n in six},
 'unexpected_root_markdown': unexpected,
 'placeholder_patterns': re.findall(r'\b(?:TODO|TBD|FIXME)\b|\{\{[^}]+\}\}|(?<!\.)\.\.\.(?!\.)', text),
 'semantic_boundary_checks': boundaries,
 'inputs_sha256': {n: hashlib.sha256((root/n).read_bytes()).hexdigest() for n in evidence_names+['report_human_behavioral_models_video_data.md']},
 'not_verified': ['model inference/quality', 'tracker or event execution', 'export parity', 'compilation', 'LinQ execution', 'target data or SDK access', 'external URL freshness beyond saved Oct23 observations', 'new legal clearance'],
}
(root/'_WORK/COMPRESSOR_CHECKS.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(checks, ensure_ascii=False, indent=2))
errors = bool(failures or missing_refs or missing_hexes or novel_urls or duplicates or unexpected or checks['placeholder_patterns'])
errors |= not all(boundaries.values())
errors |= bool(checks['yaml_missing_required_fields'] or checks['answers_missing_heading'])
errors |= not all(schema_match.values()) or not checks['all_tables_declared']
errors |= not all(checks['six_final_names_exist'].values())
raise SystemExit(1 if errors else 0)
