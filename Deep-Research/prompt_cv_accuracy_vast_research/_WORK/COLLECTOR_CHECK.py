"""In-stage collector ID/source/link integrity, no external calls or execution tests."""
from pathlib import Path
import re, json

root=Path(__file__).resolve().parent.parent
index=json.loads((root/'_WORK/COLLECTOR_INDEX.json').read_text(encoding='utf-8'))
raw=(root/'RAW_FACTS.md').read_text(encoding='utf-8')
sources=(root/'SOURCES.md').read_text(encoding='utf-8')
questions=(root/'OPEN_QUESTIONS.md').read_text(encoding='utf-8')
critic=(root/'CRITIC.md').read_text(encoding='utf-8')
source_defs=set(re.findall(r'^## (S\d{3}) —',sources,re.M))
fact_defs=set(re.findall(r'^## (F\d{3}) —',raw,re.M))
question_defs=set(re.findall(r'^### (Q\d{3}) —',questions,re.M))
assert len(source_defs)==290, len(source_defs)
assert fact_defs=={f'F{i:03}' for i in range(1,202)}
assert question_defs=={f'Q{i:03}' for i in range(1,25)}
assert set(re.findall(r'\bS\d{3}\b',raw))<=source_defs
assert set(re.findall(r'\bF\d{3}\b',sources+questions))<=fact_defs
assert set(re.findall(r'\bQ\d{3}\b',raw+questions+critic))<=question_defs
for key,entry in index['branch_inputs'].items():
    text=(root/'_WORK'/entry['file']).read_text(encoding='utf-8-sig')
    assert set(re.findall(re.escape(key)+r'-S\d{2}',text))<=set(index['sources'])
    assert set(re.findall(re.escape(key)+r'-F\d{2}',text))<=set(index['facts'])
assert not re.findall(r'W[12]-[A-Z0-9]{1,2}-[SF]\d{2}',raw)
assert not re.findall(r'turn\d+(?:search|view|fetch)\d+',raw+sources+questions)
missing=[]
for name in ['SOURCES.md','RAW_FACTS.md','OPEN_QUESTIONS.md','_WORK/AUTHOR_BRIEF.md','_WORK/ID_MAP.md']:
    path=root/name
    for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8-sig')):
        if re.match(r'https?://|mailto:|#',target): continue
        target=target.split('#')[0]
        if target and not (path.parent/target).exists(): missing.append((name,target))
assert not missing,missing
assert len(re.findall(r'^### K\d{3} —',critic,re.M))==22
result={'source_ids':len(source_defs),'fact_ids':len(fact_defs),'question_ids':len(question_defs),
        'branches':len(index['branch_inputs']),'mapped_branch_sources':len(index['sources'])-3,
        'mapped_branch_facts':len(index['facts']),'local_markdown_missing':missing,
        'status':'PASS — document/ID/link integrity only, no model/runtime tests'}
print(json.dumps(result,ensure_ascii=False))
