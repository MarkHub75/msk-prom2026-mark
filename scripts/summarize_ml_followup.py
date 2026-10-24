"""Render E006/E007 saved-output diagnostics; never runs neural models."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = Path('/workspace/artifacts/night-20261024')


def main():
    pinned = {}
    def read(relative):
        p = ARTIFACTS / relative
        blob = p.read_bytes(); pinned[relative] = hashlib.sha256(blob).hexdigest()
        return json.loads(blob)

    helmet = read('E006-helmet-drift-audit/audit-v2/summary.json')
    raw = read('E006-helmet-drift-audit/audit-v2/raw-comparison.json')
    motion = read('E007-caviar-observation-audit/report.json')
    ledger = read('E008-release-evidence/f99edc8d-review.json')
    transitions = helmet['pair_summary']['native_to_baseline_ptq']
    stats = raw['images']
    raw_summary = {
        'images': len(stats), 'binding': raw['binding'],
        'native_float_bitwise_equal_images': sum(r['comparisons']['native_to_float']['bitwise_equal'] for r in stats),
        'native_float_max_abs_diff_by_channel': [max(r['comparisons']['native_to_float']['max_abs_diff_by_channel'][i] for r in stats) for i in range(6)],
        'note': 'Anchor-level numerical differences are not object error counts or causal PTQ attribution.'}
    scoped_outside = {}
    for line in (ARTIFACTS / 'E007-caviar-observation-audit/actor-attribution.jsonl').read_text().splitlines():
        r = json.loads(line); b = r['source_box_xyxy']; w, h = r['image_size']
        if not (0 <= b[0] < b[2] <= w and 0 <= b[1] < b[3] <= h):
            key = r['source_movement'] + ':' + r['category']
            scoped_outside[key] = scoped_outside.get(key, 0) + 1
    summary = {
        'status': 'SAVED_OUTPUT_ERROR_ATTRIBUTION_NOT_NEW_MODEL_QUALITY',
        'source_artifacts_sha256': pinned, 'new_neural_calls': 0, 'new_remote_calls': 0,
        'candidate_budget_reset': False, 'weights_or_thresholds_changed': False,
        'helmet': {'native_to_baseline_ptq': transitions,
                   'fp_correspondence': helmet['fp_pair_counts']['native_to_baseline_ptq'],
                   'raw': raw_summary},
        'caviar': {k: motion[k] for k in ('checks', 'totals', 'limitations', 'existing_stages')},
        'scoped_outside_source_boxes': scoped_outside,
        'release_evidence': {'integrity_status': ledger['integrity_status'],
                             'checks': len(ledger['checks']), 'gates': ledger['gates'],
                             'quality_release': ledger['quality_release'], 'manifest_sha256': ledger['manifest_sha256']},
        'independent_quality': 'NOT_ESTABLISHED',
    }
    output = ROOT / 'ml/reports/night-followup-20261024.json'
    output.write_text(json.dumps(summary, indent=2, allow_nan=False) + '\n')
    rows = []
    for name, metrics in transitions.items():
        for kind, value in metrics['primary_complete_gt_transitions'].items():
            rows.append({'exp_id': 'E006', 'scope': name, 'category': kind, 'count': value})
    for key, value in motion['totals'].items():
        label, category = key.split(':', 1)
        rows.append({'exp_id': 'E007', 'scope': label, 'category': category, 'count': value})
    with (ROOT / 'ml/reports/night-followup-20261024.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['exp_id', 'scope', 'category', 'count'], lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    dest = ARTIFACTS / 'figures-followup'; dest.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 4), constrained_layout=True)
    x = ['helmet (25 GT)', 'bare_head (32 GT)']
    bottom = [0, 0]
    for kind, label, color in [('TP->TP', 'Retained TP', '#4c9a65'), ('FN->TP', 'Recovered TP', '#8ec5a2'),
                                ('TP->FN', 'Lost TP', '#b94141'), ('FN->FN', 'Still missed', '#d8b88a')]:
        values = [transitions[c]['primary_complete_gt_transitions'].get(kind, 0) for c in ('helmet', 'bare_head')]
        axes[0].bar(x, values, bottom=bottom, label=label, color=color)
        for i, v in enumerate(values):
            if v: axes[0].text(i, bottom[i] + v/2, str(v), ha='center', va='center')
        bottom = [a + b for a, b in zip(bottom, values)]
    axes[0].set_title('Helmet native -> SIMULATED PTQ\nSame reviewed development GT; not independent test')
    axes[0].set_ylabel('Annotated objects'); axes[0].legend(fontsize=8)
    labels = ['No decoded person', 'IoU below .5', 'Consumer .5 gate', 'Ambiguous', 'Anchor usable', 'Anchor/track gap']
    keys = ['no_decoded_person', 'localization_below_ownership_iou', 'consumer_score_gate', 'ambiguous_ownership', 'consumer_unique_anchor_observed', 'pose_anchor_or_track_gap']
    for offset, movement, color in [(-.2, 'running', '#b94141'), (.2, 'walking', '#3479af')]:
        values = [motion['totals'].get(movement + ':' + k, 0) for k in keys]
        axes[1].bar([i + offset for i in range(len(keys))], values, width=.4, label=movement, color=color)
    axes[1].set_xticks(range(len(keys)), labels, rotation=30, ha='right')
    axes[1].set_ylabel('Source actor-frames'); axes[1].set_title('CAVIAR existing-stage attribution\n46 running / 482 walking actor-frames; saved native outputs')
    axes[1].legend(fontsize=8)
    fig.suptitle('Postmortem only: no inference, tuning or new quality claim')
    for suffix in ('png', 'svg', 'pdf'):
        fig.savefig(dest / ('error-attribution.' + suffix), dpi=160)
    plt.close(fig)
    checksums = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.iterdir()) if p.is_file() and p.name != 'checksums.json'}
    (dest / 'checksums.json').write_text(json.dumps(checksums, indent=2) + '\n')
    print(json.dumps({'summary': str(output), 'rows': len(rows), 'figures': str(dest)}))


if __name__ == '__main__':
    main()
