from pathlib import Path
root = Path(__file__).resolve().parent.parent
p = root/'report_machine_behavioral_models_video_data.md'
t = p.read_text(encoding='utf-8')
a = 'not77 events. `QTmwhrVal1g'
b = 'not77 events. Source answer-phone15 and text/look-phone57 are distinct; source IDs are not positions in a selected60-class head, and117 HOI verbs are not600 HICO interaction IDs. `QTmwhrVal1g'
assert t.count(a) == 1
t = t.replace(a,b)
a = 'DeepSORT/StrongSORT demos can emit predicted boxes;'
b = 'DeepSORT/StrongSORT have GPL code and separate embedding dependencies; their demos can emit predicted boxes;'
assert t.count(a) == 1
t = t.replace(a,b)
p.write_text(t, encoding='utf-8', newline='\n')
