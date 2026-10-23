from pathlib import Path
import datetime, re
p = Path(__file__).resolve().parent/'RUN_STATE.md'
t = p.read_text(encoding='utf-8-sig')
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).isoformat(timespec='seconds')
t = re.sub(r'^2026-10-24T00:38:26\+03:00: Separate fresh High compressor COMPLETE', now + ': Separate fresh High compressor COMPLETE', t, count=1, flags=re.M)
p.write_text(t, encoding='utf-8', newline='\n')
print(now)
