#!/usr/bin/env python3
"""Freeze reviewed presentation sources from immutable Git commits. No product writes."""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO = Path('/mnt/d/templates/msk-promhack/msk-prom2026-mark')
OUT = Path(__file__).parent / 'source-snapshots'
OUT.mkdir(parents=True, exist_ok=True)
FROZEN = {
    'origin/main': '353c7f966a67c0797dbe88ec8f8eb99f6465f582',
    'origin/matvey_cv': '1bdeeafcd74a696999cfd4af28c2ea598e3fe8f2',
    'origin/demo/checkpoint': '9f652236589698857ba05eabbcf361b4ab3779b2',
    'origin/front/control-room': '8161719d687083c7a3578b0f5de8bc2043a95ce1',
}

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

sources = [
    ('origin/main', 'progress.md', None),
    ('origin/main', 'docs/linq/LINQ_CONTRACT.md', [(1, 12), (19, 45), (62, 108), (110, 123), (126, 130), (132, 134)]),
    ('origin/main', 'results/linq_smoke/synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json', None),
    ('origin/main', 'results/linq_smoke/synthetic_coco_40x1s_mosprom_pose640_cut_ap9999_b1_o1_h1m_s2.summary.json', None),
    ('origin/main', 'results/linq_smoke/det640_cut_ap9999.json', [(1760, 1766)]),
    ('origin/main', 'results/linq_smoke/pose640_cut_ap9999.json', [(5009, 5015)]),
    ('origin/main', 'tech.md', [(28, 54), (2705, 2734), (2901, 2985), (3056, 3060)]),
    ('origin/main', 'config/default.yaml', [(149, 157)]),
    ('origin/main', 'config/models.yaml', None),
    ('origin/main', 'contract/openapi.json', None),
    ('origin/main', 'contract/ws.schema.json', None),
    ('origin/main', 'src/safewatch/rules/__init__.py', None),
    ('origin/main', 'src/safewatch/rules/load_carrying.py', None),
    ('origin/main', 'src/safewatch/services.py', [(744, 761), (1638, 1653), (1951, 1982)]),
    ('origin/matvey_cv', 'docs/STATUS.md', None),
    ('origin/matvey_cv', 'docs/validation/jupyter-kit.json', None),
    ('origin/matvey_cv', 'ml/PROGRESS.md', None),
    ('origin/matvey_cv', 'ml/EVAL_REPORT.md', None),
    ('origin/matvey_cv', 'ml/RELEASE_MANIFEST.json', None),
    ('origin/matvey_cv', 'RESUME.md', [(1, 18)]),
    ('origin/matvey_cv', 'ml/SCENARIOS.md', None),
    ('origin/matvey_cv', 'ml/reports/pose-linq-ur01-parity.json', None),
    ('origin/matvey_cv', 'ml/reports/running-zone-readiness.json', None),
    ('origin/demo/checkpoint', 'tools/checkpoint-demo/README.md', None),
    ('origin/demo/checkpoint', 'tools/checkpoint-demo/WATCH_LOG.md', None),
    ('origin/demo/checkpoint', 'tools/checkpoint-demo/GAPS.md', None),
    ('origin/demo/checkpoint', 'tools/checkpoint-demo/watch/last-real.json', None),
]
records = []
for ref, path, ranges in sources:
    commit = FROZEN[ref]
    raw = git('show', f'{commit}:{path}')
    label = ref.removeprefix('origin/').replace('/', '-')
    name = f'{label}__{path.replace("/", "__")}'
    if ranges:
        lines = raw.decode('utf-8-sig').splitlines()
        selected = ['# Excerpts with ORIGINAL source line numbers. See source-index.json.']
        for start, end in ranges:
            selected += [f'{n}: {lines[n-1]}' for n in range(start, min(end, len(lines)) + 1)]
        data = ('\n'.join(selected) + '\n').encode()
        name += '.excerpt.txt'
    else:
        data = raw
    (OUT / name).write_bytes(data)
    records.append({
        'ref_at_verification': ref, 'commit': commit, 'path': path,
        'git_blob': git('rev-parse', f'{commit}:{path}').decode().strip(),
        'original_sha256': hashlib.sha256(raw).hexdigest(),
        'snapshot': name, 'snapshot_sha256': hashlib.sha256(data).hexdigest(),
        'original_line_ranges': ranges,
    })

(OUT / 'source-index.json').write_text(json.dumps({
    'verified_at_utc': datetime.now(timezone.utc).isoformat(),
    'last_fetch_review_msk': '2026-10-24 08:28; final full source fetch before presentation source freeze',
    'frozen_heads': FROZEN,
    'repo': str(REPO),
    'mode': 'read-only git show; reports reviewed; no live TPU or software test rerun',
    'linq_contract_network_lines_omitted': 'Avoid copying shared broker credentials/account/network locators; factual result and method lines retained.',
    'sources': records,
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Frozen {len(records)} immutable source snapshots at {OUT}')
