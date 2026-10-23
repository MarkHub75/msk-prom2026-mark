"""W2-02-X01/X02: source-level and own accounting arithmetic only; no system test."""
import ast
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE / 'ActEV_Scorer-b8d82c094f5c2896eb0eba1061321bf1d82ad13c'
spec = importlib.util.spec_from_file_location('sparse_signal', ROOT / 'lib/sparse_signal.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
S = mod.SparseSignal
tree = ast.parse((ROOT / 'lib/metrics.py').read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'fa_meas_v2')
ns = {}
exec(compile(ast.Module(body=[fn], type_ignores=[]), 'pinned_metrics_excerpt', 'exec'), ns)
ref = S({20: 1, 40: 0})
nonref = ref.not_sig(100)
sys = ref + S({25: 1, 35: 0}) + S({50: 1, 60: 0})
tfa = ns['fa_meas_v2']([{'c': ref}, {'c': nonref}, {'c': nonref.area()}], {}, {'c': sys})
assert tfa['tfa_numer'] == 20 and tfa['tfa_denom'] == 80 and tfa['tfa'] == .25
empty = ns['fa_meas_v2']([{'c': ref}, {'c': S()}, {'c': 0}], {}, {'c': sys})
assert empty['tfa'] is None

# All times seconds; source PTS and receiver monotonic coincide only in this
# explicitly constructed, speed=1 fixture. Origin is immutable per logical ID.
records = [
    dict(id='v0', logical='L0', anchor=-5, delivered=10, outcome='false'),
    dict(id='v1', logical='L1', anchor=10, delivered=12, outcome='timely'),
    dict(id='v2', logical='L2', anchor=95, delivered=105, outcome='false'),
    dict(id='v3', logical='L3', anchor=98, delivered=109, outcome='late'),
    dict(id='v4', logical='L4', anchor=70, delivered=72, outcome='timely'),
    dict(id='v4retry', logical='L4', anchor=70, delivered=115, outcome='duplicate'),
    dict(id='v5', logical='L5', anchor=80, delivered=108, outcome='false', timeout=85, result=107),
    dict(id='v7', logical='L7', anchor=60, delivered=65, outcome='unknown'),
    dict(id='v8', logical='L8', anchor=100, delivered=110, outcome='false'),
]
def summarize(close):
    seen = [r for r in records if r['delivered'] <= close]
    owned = [r for r in seen if 0 <= r['anchor'] < 100]
    counts = {k: sum(r['outcome'] == k for r in owned)
              for k in ('timely', 'late', 'duplicate', 'false', 'unknown')}
    assert sum(counts.values()) == len(owned)
    assert len(seen) == len(owned) + sum(not 0 <= r['anchor'] < 100 for r in seen)
    return dict(close=close, visible_all=len(seen), source_owned=len(owned),
                unique_logical_delivered=len({r['logical'] for r in owned}),
                source_outcomes=counts, source_pending_logical=['L6'],
                wall_main=sum(0 <= r['delivered'] < 100 for r in seen),
                wall_drain=sum(100 <= r['delivered'] < 112 for r in seen),
                wall_after_close=sum(112 <= r['delivered'] for r in seen),
                H_source=100/3600, semantic_false_rate=counts['false']/(100/3600),
                known_strict_unmatched_rate=(counts['false']+counts['late']+counts['duplicate'])/(100/3600))
at112, at120 = summarize(112), summarize(120)
assert (at112['source_owned'], at120['source_owned']) == (6, 7)
assert (at112['wall_main'], at112['wall_drain']) == (4, 4)
assert at120['unique_logical_delivered'] == 6

# Scheduled playback changes speed continuously at PTS=50, no discontinuity.
def due(pts):
    return 1000 + pts if pts <= 50 else 1050 + (pts - 50)/2
replay = dict(pts=80, speed_after50=2, due=due(80), delivered=1068,
              replay_lag=1068-due(80), wrong_fixed_speed_lag=1068-(1000+80))
assert replay['replay_lag'] == 3 and replay['wrong_fixed_speed_lag'] == -12
out = dict(status='local arithmetic / extracted function execution only',
           actev=dict(numerator=tfa['tfa_numer'], denominator=tfa['tfa_denom'],
                      tfa=tfa['tfa'], zero_nonreference=empty['tfa'],
                      union_false_active_outside_ref=10, frames=100),
           ledger=records, snapshots=[at112, at120], replay=replay)
(HERE / 'fixture_results.json').write_text(json.dumps(out, indent=2), encoding='utf8')
print(json.dumps({k: v for k, v in out.items() if k != 'ledger'}, indent=2))
