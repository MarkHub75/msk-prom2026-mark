"""Bounded, explicit primary-source URFall development intake.

No test split is downloaded. Source IDs are frozen before reading annotations.
Native MP4s are small author-provided previews; verify RGB/frame alignment before
using author depth-frame posture labels as RGB episode ground truth.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

UR_BASE = 'https://fenix.ur.edu.pl/~mkepski/ds/'
OMNI_REPO = 'simplexsigil2/omnifall'
OMNI_REVISION = '83572a37b9e3081df8c06a56874b1d1f2a19386c'


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def _save(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n')


def fetch(url, path, remaining):
    """Download <=remaining bytes; partial files cannot masquerade as completed."""
    path = Path(path)
    if path.exists():
        return {'url': url, 'path': str(path), 'bytes': path.stat().st_size,
                'sha256': sha256(path), 'downloaded_now': False}, 0
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name+'.part')
    count = 0
    try:
        with urlopen(Request(url, headers={'User-Agent': 'MOSPROM-temporal-source-audit/1.0'}), timeout=45) as response:
            advertised = response.headers.get('Content-Length')
            if advertised is not None and int(advertised) > remaining:
                raise ValueError('file exceeds remaining download budget')
            with temp.open('wb') as stream:
                while True:
                    block = response.read(min(1024*1024, remaining-count+1))
                    if not block:
                        break
                    count += len(block)
                    if count > remaining:
                        raise ValueError('download budget exceeded')
                    stream.write(block)
            if advertised is not None and count != int(advertised):
                raise ValueError('truncated download')
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)
    return {'url': url, 'path': str(path), 'bytes': count,
            'sha256': sha256(path), 'downloaded_now': True}, count


def acquire(root, count=4, max_bytes=250_000_000, extend_selection=False):
    if not 1 <= count <= 10 or max_bytes <= 0 or max_bytes > 250_000_000:
        raise ValueError('count must be 1..10; cumulative budget at most 250000000 bytes')
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    sequence_ids = [f'{kind}-{i:02d}' for kind in ('fall', 'adl') for i in range(1, count+1)]
    selection_file = root/'selection.json'
    if selection_file.exists():
        selection = json.loads(selection_file.read_text())
        if selection['source_ids'] != sequence_ids:
            if not extend_selection or not set(selection['source_ids']).issubset(sequence_ids):
                raise ValueError('existing source selection is immutable without explicit monotone extension')
            history = root/'selection-history'
            history.mkdir(exist_ok=True)
            _save(history/(hashlib.sha256(selection_file.read_bytes()).hexdigest()+'.json'), selection)
            selection = {**selection, 'source_ids': sequence_ids,
                         'frozen_at': datetime.now(timezone.utc).isoformat(),
                         'extension_reason': 'explicit pre-prediction deterministic prefix expansion',
                         'previous_source_ids': selection['source_ids']}
            _save(selection_file, selection)
    else:
        selection = {'schema_version': 'temporal-intake-v1', 'source_ids': sequence_ids,
                     'frozen_at': datetime.now(timezone.utc).isoformat(),
                     'selection_policy': 'first source IDs in each class, frozen before model outputs',
                     'model_outputs_used_for_selection': False,
                     'split': 'validation', 'final_test': 'NOT_ACQUIRED_OR_EVALUATED',
                     'group_id': 'urfall-all-unknown-subjects-shared-cam0',
                     'subject_independent_split_claim': False}
        _save(selection_file, selection)
    ledger_file = root/'download-ledger.json'
    ledger = json.loads(ledger_file.read_text()) if ledger_file.exists() else {'downloaded_bytes': 0, 'artifacts': []}
    urls = [(UR_BASE+'uf.html', root/'raw/urfall/source.html')]
    for name in ('urfall-cam0-falls.csv', 'urfall-cam0-adls.csv'):
        urls.append((UR_BASE+'data/'+name, root/'raw/urfall'/name))
    for seq in sequence_ids:
        for name in (seq+'-cam0.mp4', seq+'-data.csv'):
            urls.append((UR_BASE+'data/'+name, root/'raw/urfall'/name))
    # Guidelines and repository metadata only. Do not download heldout annotations,
    # source videos, splits/test.csv or automatic parquet bundles for OmniFall.
    for name in ('README.md', 'LABELS.md', 'STRUCTURE.md', 'labels/label2id.csv'):
        urls.append((f'https://huggingface.co/datasets/{OMNI_REPO}/resolve/{OMNI_REVISION}/{name}',
                     root/'raw/omnifall-metadata'/name))
    for url, path in urls:
        prior = next((v for v in ledger['artifacts'] if v['path'] == str(path)), None)
        if prior and path.exists() and sha256(path) != prior['sha256']:
            raise ValueError('existing downloaded artifact changed')
        record, consumed = fetch(url, path, max_bytes-ledger['downloaded_bytes'])
        ledger['downloaded_bytes'] += consumed
        ledger['artifacts'] = [v for v in ledger['artifacts'] if v['path'] != str(path)] + [record]
        _save(ledger_file, ledger)
    return ledger


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', required=True)
    p.add_argument('--count', type=int, default=4)
    p.add_argument('--max-bytes', type=int, default=250_000_000)
    p.add_argument('--extend-selection', action='store_true', help='explicit prefix-only expansion before predictions')
    args = p.parse_args(argv)
    result = acquire(args.root, args.count, args.max_bytes, args.extend_selection)
    print(json.dumps({'artifacts': len(result['artifacts']), 'downloaded_bytes': result['downloaded_bytes'],
                      'final_test': 'NOT_ACQUIRED_OR_EVALUATED'}))


if __name__ == '__main__':
    main()
