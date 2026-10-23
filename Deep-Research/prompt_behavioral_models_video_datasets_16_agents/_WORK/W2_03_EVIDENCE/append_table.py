import json
from pathlib import Path
p=Path('_WORK/W2_03.md'); rows=json.loads(Path('_WORK/W2_03_EVIDENCE/phase_observability.json').read_text())
s='\n| Source interval | FPS | Samples, phase min–max | Random20%, min–max | Burst1s, min–max |\n|---|---:|---:|---:|---:|\n'
for r in rows:
 s+='| '+r['event']+' | '+str(r['fps'])+' | '+' | '.join('–'.join(map(str,r[k])) for k in ['phase_minmax','random20pct_100seeds_phase_minmax','one_second_burst_start_inside_event_minmax'])+' |\n'
s+='\nБез drops first opportunity delay ranges: native0s;1fps0–0.96s;2fps0–0.48s;5fps0–0.16s. Это **sampling opportunity delay**, не задержка распознавания/оповещения. При1fps random-mask test способен оставить0 observations даже для этих2–4s intervals; это демонстрация потери возможности увидеть эпизод в конкретных синтетических условиях, не оценка модели. Контроль Walk1 также теряет временную структуру; большее количество still frames не доказывает gait separation.\n'
p.write_text(p.read_text(encoding='utf-8')+s,encoding='utf-8')
