"""Summarize saved night experiments and render shareable, media-free figures.

Reads fixed numeric reports only. Performs no inference, training or network I/O.
Run with the existing main Python environment (matplotlib is already installed).
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = Path('/workspace/artifacts/night-20261024')
REPORTS = ROOT / 'ml/reports'


def main():
    sources = {}
    def read(relative):
        path = ARTIFACTS / relative
        blob = path.read_bytes()
        sources[relative] = hashlib.sha256(blob).hexdigest()
        return json.loads(blob)

    helmet = read('E001/summary.json')
    split = read('E005/summary.json')
    edf = read('E002/edf-resolution-v1/paired-analysis.json')
    partial = read('E004/fall-partial-torso-v1/decision-summary.json')
    running = read('E003/caviar-running-v1/comparison.json')
    helmet_models = helmet['models'] | {'split_data8': split['models']['split_data8']}
    edf_variants = {name: {key: value for key, value in item.items() if key != 'per_window'}
                    for name, item in edf['variants'].items()}
    summary = {
        'evidence': 'NATIVE_AND_SIMULATED_DEVELOPMENT_NOT_INDEPENDENT_TEST',
        'source_artifacts_sha256': sources,
        'new_real_linq_requests': 0,
        'new_training_runs': 0,
        'helmet': {'dataset': 'quality-v3-52;44complete/class;source-photo-overlap',
                   'gt_file_sha256': '346f74cab99ddc2cc9c0f18b3efd95027a0b1ea782738469f502bc771dfd27e0',
                   'models': helmet_models, 'selected': 'existing hardware-verified baseline',
                   'new_hypotheses': 2, 'improved': False,
                   'note': 'Vendor quantized CPU simulation is not actual TPU execution.'},
        'fall_edf': {'dataset': 'edf-native-fall-source3/v1-20261024',
                     'variants': edf_variants, 'total_gpu_job_seconds': edf['total_gpu_job_seconds'],
                     'note': 'Source-positive support-window coverage only. Outside UNKNOWN; not incident recall.'},
        'fall_partial_torso': partial,
        'running': running,
        'independent_test': 'NOT_AVAILABLE_NOT_USED',
        'new_hypothesis_budget_per_direction': 2,
        'baseline_replaced': False,
    }
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / 'night-20261024.json').write_text(json.dumps(summary, indent=2, allow_nan=False) + '\n')
    # Long-form, graph-ready data preserve endpoint/evidence/scope distinctions.
    rows = []
    def add(exp, variant, endpoint, metric, value, evidence):
        rows.append(dict(exp_id=exp, variant=variant, endpoint=endpoint, metric=metric,
                         value='' if value is None else value, evidence=evidence,
                         independent_test='false'))
    for variant, result in helmet_models.items():
        evidence = 'NATIVE_SAVED' if variant == 'existing_native' else ('FLOAT_ONNX_CPU' if variant == 'float_onnx' else 'SIMULATED_CPU')
        for name, metrics in result['classes'].items():
            for metric, value in metrics.items():
                add('E001/E005', variant, name, metric, value, evidence)
        add('E001/E005', variant, 'macro', 'f1', result['macro_f1'], evidence)
    for variant, result in edf_variants.items():
        for metric in ('frames_with_full_torso_fraction', 'frame_pose_unknown_or_missing_rate',
                       'support_hit_coverage_lower', 'confirmation_hit_coverage_lower'):
            add('E002', variant, 'source_positive_diagnostic', metric, result[metric], 'NATIVE_GPU')
    for variant, result in partial['primary'].items():
        for metric, value in result.items():
            add('E004', variant, 'UR20_source_reference_events_2fps', metric, value, 'OFFLINE_REPLAY_SAVED_NATIVE')
    for variant, result in running['policies'].items():
        for metric, value in result['episode_metrics'].items():
            add('E003', variant, 'CAVIAR_source_scoped_running_windows', metric, value, 'NATIVE_GPU_THEN_CPU_RULE')
    with (REPORTS / 'night-20261024-metrics.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    figure_dir = ARTIFACTS / 'figures'
    figure_dir.mkdir(exist_ok=True)
    labels = ['Native', 'Float ONNX', 'Baseline PTQ', 'E001 data8', 'E005 split']
    variants = list(helmet_models)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), constrained_layout=True)
    for ax, metric in zip(axes, ('precision', 'recall', 'f1')):
        for name, color in (('helmet', '#3479af'), ('bare_head', '#d27719')):
            ax.plot(labels, [helmet_models[v]['classes'][name][metric] for v in variants], 'o-', label=name, color=color)
        ax.set_ylim(0, 1.03); ax.set_title(metric); ax.tick_params(axis='x', rotation=30); ax.grid(alpha=.2)
    axes[0].legend()
    fig.suptitle('Helmet: fixed development GT; PTQ is SIMULATED, no independent test')
    for suffix in ('png', 'svg', 'pdf'):
        fig.savefig(figure_dir / ('helmet-comparison.' + suffix), dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
    for name in ('helmet', 'bare_head'):
        axes[0].plot(labels, [helmet_models[v]['classes'][name]['fp'] for v in variants], 'o-', label=name)
        axes[1].plot(labels, [helmet_models[v]['classes'][name]['fn'] for v in variants], 'o-', label=name)
    for ax, title in zip(axes, ('False positive objects', 'Missed objects')):
        ax.set_title(title); ax.tick_params(axis='x', rotation=30); ax.grid(alpha=.2); ax.legend()
    fig.suptitle('Counts on the same reviewed development scope; not alerts/hour')
    fig.savefig(figure_dir / 'helmet-errors.png', dpi=160); plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
    for metric, label in (('frames_with_full_torso_fraction', 'full torso / sampled frames'),
                          ('frame_pose_unknown_or_missing_rate', 'unknown or missing pose / frames')):
        axes[0].plot(['Original RGB', 'Half then restored'], [v[metric] for v in edf_variants.values()], 'o-', label=label)
    axes[0].set_ylim(0, 1); axes[0].set_title('EDF observability, not event accuracy'); axes[0].legend(fontsize=8)
    axes[1].bar(['Baseline', 'H1 body height', 'H2 bbox anchor'], [0, 0, 0], color='#3479af')
    axes[1].set_ylim(0, 1); axes[1].set_ylabel('Source-window recall'); axes[1].set_title('CAVIAR: 0/3 running windows in every policy')
    axes[1].text(.5, .4, '0/46 running actor-frames matched\nP undefined; F1=0\nNo independent industrial test', transform=axes[1].transAxes, ha='center')
    fig.suptitle('Native development diagnostics; no new TPU execution')
    for suffix in ('png', 'svg', 'pdf'):
        fig.savefig(figure_dir / ('temporal-diagnostics.' + suffix), dpi=160)
    plt.close(fig)
    checksums = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(figure_dir.iterdir()) if p.is_file() and p.name != 'checksums.json'}
    (figure_dir / 'checksums.json').write_text(json.dumps(checksums, indent=2) + '\n')
    print(json.dumps({'summary': str(REPORTS / 'night-20261024.json'), 'metrics_rows': len(rows), 'figures': str(figure_dir)}))


if __name__ == '__main__':
    main()
