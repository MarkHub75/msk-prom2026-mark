"""Package frozen image-slide evidence for the unchanged OS Human Review Engine.

New slides have no historical BEFORE. The package contains no human decisions.
Run only after final Craft captures and export verification have completed.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import shutil
import struct

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='review')
    parser.add_argument('--revision', type=int, default=1)
    parser.add_argument('--capture-report', default='evidence/craft/report.json')
    parser.add_argument('--browser-report', default='evidence/browser/report.json')
    parser.add_argument('--renderer-url', default='http://127.0.0.1:8725/frontend-hackathon-os/production/human_review/renderer/v1.1/index.html?manifest=/msk-promhack/safewatch-checkpoint-pptx/presentations/checkpoint-2026-10-24/review/manifest.json')
    args = parser.parse_args()
    output = ROOT / args.output
    if output.exists():
        raise SystemExit('Refusing to overwrite a sealed review. Use a new output/review revision.')
    report_file = ROOT / args.capture_report
    capture = read(report_file)
    exports = read(ROOT / 'evidence/exports/report.json')
    assert capture['status'] == 'CAPTURED' and capture['sourceStable'], 'Stable Craft capture required'
    assert not capture.get('runtimeErrors'), 'Capture runtime errors remain'
    assert exports['status'] == 'PASS' and exports['slides'] == 8
    raw_notes = read(ROOT / 'speaker-notes.json')
    scenes = raw_notes if isinstance(raw_notes, list) else raw_notes['slides']
    assert len(scenes) == 8
    expected_states = {f'{n:02d}' for n in range(1, 9)}
    seen = {(str(s['state']).zfill(2), str(s['height']), s['motion']) for s in capture['screenshots']}
    expected = {(state, vp, motion) for state in expected_states for vp in ['1080', '720'] for motion in ['normal', 'reduced']}
    assert seen == expected, 'Need all eight holds at both sizes and both motion preferences'
    (output / 'assets').mkdir(parents=True)
    (output / 'sources').mkdir()
    artifacts, ids, document_ids = [], {}, []
    supported = {'.png': 'image/png', '.webm': 'video/webm', '.md': 'text/markdown',
                 '.json': 'application/json', '.txt': 'text/plain'}

    def artifact(ident, source, kind='document', state=None, viewport=None, motion=None, notes='Recorded evidence; human acceptance pending.'):
        source = Path(source)
        suffix = source.suffix.lower()
        assert suffix in supported, 'Unsupported HRE artifact MIME: ' + str(source)
        dest = ('assets/' if kind in ['image', 'video'] else 'sources/') + ident + '-' + source.name
        shutil.copy2(source, output / dest)
        width = height = None
        if kind == 'image':
            width, height = struct.unpack('>II', source.read_bytes()[16:24])
        artifacts.append(dict(id=ident, kind=kind, path=dest, sha256=digest(source), mime=supported[suffix],
                              label=ident, revision_id='final' if state else None, state_id=state,
                              viewport_id=viewport, motion=motion, fixture_id='safewatch-checkpoint-20261024' if state else None,
                              capture_mode='viewport' if state else None, width=width, height=height,
                              provenance='VERIFIED', notes=notes))
        if kind == 'document':
            document_ids.append(ident)

    for shot in capture['screenshots']:
        state = str(shot['state']).zfill(2)
        ident = 'final-' + shot['id']
        source = report_file.parent / shot['path']
        assert digest(source) == shot['sha256'], 'Capture image changed: ' + ident
        ids[state, str(shot['height']), shot['motion']] = ident
        artifact(ident, source, 'image', state, str(shot['height']), shot['motion'],
                 notes='Actual Chromium capture of the final flattened image. Text inside PNG is outside the DOM critic coverage.')
    artifact('craft-report', report_file)
    artifact('exports-report', ROOT / 'evidence/exports/report.json')
    artifact('speaker-notes', ROOT / 'speaker-notes.json')
    for name in ['story.json', 'adapter.json']:
        file = ROOT / 'craft' / name
        if file.exists():
            artifact('craft-' + name.removesuffix('.json'), file)
    optional = [('powerpoint-report', ROOT / 'evidence/powerpoint/report.json'),
                ('browser-report', ROOT / args.browser_report),
                ('composition-report', ROOT / 'evidence/composition.json'),
                ('content-report', ROOT / 'evidence/content-report.json'),
                ('pdf-report', ROOT / 'evidence/pdf-report.json'),
                ('technical-audit', ROOT / 'research/technical-evidence.md'),
                ('frontend-audit', ROOT / 'research/frontend-evidence.md'),
                ('visual-audit', ROOT / 'research/independent-visual-review.md'),
                ('source-index', ROOT / 'research/source-snapshots/source-index.json'),
                ('fresh-mock-smoke', ROOT / 'research/smoke-mock-fresh.json')]
    for ident, file in optional:
        if file.exists():
            artifact(ident, file)
    documents = []
    for directory in [ROOT / 'docs', ROOT / 'sources']:
        if directory.exists():
            documents.extend(p for p in sorted(directory.rglob('*')) if p.is_file() and p.suffix.lower() in ['.md', '.json', '.txt'])
    documents.extend(p for p in sorted(ROOT.glob('*.md')) if p.is_file())
    for index, file in enumerate(documents, 1):
        artifact(f'doc-{index:02d}', file)
    for index in range(1, 9):
        file = ROOT / f'evidence/powerpoint/slide-{index:02d}.png'
        if file.exists():
            artifact(f'powerpoint-{index:02d}', file, 'image', notes='Actual installed PowerPoint raster export; native compatibility evidence.')
    # HRE MIME schema excludes PPTX/PDF. Describe downloads without mislabelling binaries.
    download_lines = ['SafeWatch checkpoint exports. Human visual acceptance remains pending.', '']
    for file in sorted((ROOT / 'exports').glob('*')):
        if file.is_file():
            download_lines.append(f'{file.name}\nbytes: {file.stat().st_size}\nSHA-256: {digest(file)}\n')
    download_file = output / 'sources/exports.txt'
    download_file.write_text('\n'.join(download_lines))
    artifact('export-index', download_file)
    download_file.unlink()
    items = []
    for index, scene in enumerate(scenes, 1):
        state = f'{index:02d}'
        variants = []
        for vp in ['1080', '720']:
            for motion in ['normal', 'reduced']:
                variants.append(dict(viewport_id=vp, motion=motion, state_id=state,
                    before=dict(image=None, video=None, missing_reason='New presentation: no verified historical slide baseline exists.'),
                    after=dict(image=ids[state, vp, motion], video=None, missing_reason='Static image slide. No per-slide motion recording is claimed.'),
                    compatibility=dict(status='INCOMPARABLE', reasons=['New slide without a historical BEFORE; no fabricated comparison.'])))
        qa = [dict(label='Projection captures and stable source hashes', status='PASS', artifact_id='craft-report',
                   notes='Both projection sizes and motion preferences were captured. Raster text requires separate visual and typography checks.'),
              dict(label='PPTX pixels, geometry and notes', status='PASS', artifact_id='exports-report',
                   notes='Eight exact embedded images with full-bleed geometry. Consult report for native PowerPoint test status.'),
              dict(label='Craft criticism and human visual acceptance', status='UNVERIFIED', artifact_id='craft-report',
                   notes='DOM text detection does not read the flattened PNG. Critic findings remain preserved; no human verdict is preselected.')]
        items.append(dict(id='slide-' + state, title=f'{state} · {scene["title"]}',
                          delta='New source-backed SafeWatch checkpoint slide, prepared for human visual review.',
                          changes=[dict(path=f'slides/slide-{state}.png', description='Final 1920×1080 image and matching native speaker notes.')],
                          notes=['HUMAN_SAFEWATCH_CHECKPOINT_PRODUCTION_REVIEW. Human acceptance pending.',
                                 'This review contains no human decision document.'],
                          references=list(document_ids) + ([f'powerpoint-{state}'] if (ROOT / f'evidence/powerpoint/slide-{state}.png').exists() else []),
                          qa=qa, variants=variants))
    inventory = {f'slides/slide-{n:02d}.png': digest(ROOT / f'slides/slide-{n:02d}.png') for n in range(1, 9)}
    snapshot = hashlib.sha256(json.dumps(inventory, sort_keys=True).encode()).hexdigest()
    manifest = dict(schema_version='1.0.0', renderer_version='1.0.0',
        review=dict(id='safewatch-checkpoint-20261024-production', revision=args.revision,
                    title='SafeWatch · технический чекпойнт · 8 слайдов',
                    description='HUMAN_SAFEWATCH_CHECKPOINT_PRODUCTION_REVIEW. Полная image-based презентация; решения человека не заполнены.',
                    created_at=datetime.datetime.now(datetime.timezone.utc).isoformat()),
        revisions=dict(baseline=dict(id='absent', label='No historical presentation baseline', git_commit=None,
                                     snapshot_sha256=None, provenance='UNVERIFIED', notes='New deck; no historical BEFORE is supplied.'),
                       current=dict(id='final', label='SafeWatch checkpoint image-slide production', git_commit=None,
                                    snapshot_sha256=snapshot, provenance='VERIFIED',
                                    notes='Eight source PNG hashes and stable Craft capture inventory; human approval pending.')),
        viewports=[dict(id=str(h), label=f'{w} × {h}', width=w, height=h, device_scale_factor=1) for w, h in [(1920, 1080), (1280, 720)]],
        states=[dict(id=f'{n:02d}', label=s['title'], description='One manually advanced static image slide.') for n, s in enumerate(scenes, 1)],
        artifacts=artifacts, items=items)
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (output / 'manifest.sha256').write_text(digest(output / 'manifest.json') + '\n')
    # Launcher only; all rendering remains in the unchanged shared OS renderer.
    import html
    url = html.escape(args.renderer_url, quote=True)
    (output / 'index.html').write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><link rel="icon" href="data:,"><title>SafeWatch human review</title><meta http-equiv="refresh" content="0;url=' + url + '"><a href="' + url + '">Open unchanged Human Review Engine v1.1</a></html>\n')
    print(json.dumps({'status': 'PACKAGED', 'items': len(items), 'artifacts': len(artifacts), 'output': str(output), 'human_acceptance': 'NOT ASSERTED'}))


if __name__ == '__main__':
    main()
