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
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='review-13')
    parser.add_argument('--revision', type=int, default=1)
    parser.add_argument('--capture-report', default='evidence/craft-13/report.json')
    parser.add_argument('--browser-report', default='evidence/browser-13/report.json')
    parser.add_argument('--renderer-url', default='http://127.0.0.1:8745/frontend-hackathon-os/production/human_review/renderer/v1.1/index.html?manifest=/msk-promhack/argus-final-presentation/presentations/final-argus-release/review-13/manifest.json')
    args = parser.parse_args()
    output = ROOT / args.output
    if output.exists():
        raise SystemExit('Refusing to overwrite a sealed review. Use a new output/review revision.')
    report_file = ROOT / args.capture_report
    capture = read(report_file)
    exports = read(ROOT / 'evidence/exports-13/report.json')
    assert capture['status'] == 'CAPTURED' and capture['sourceStable'], 'Stable Craft capture required'
    assert not capture.get('runtimeErrors'), 'Capture runtime errors remain'
    assert exports['status'] == 'PASS' and exports['slides'] == 13
    raw_notes = read(ROOT / 'speaker-notes.json')
    scenes = raw_notes if isinstance(raw_notes, list) else raw_notes['slides']
    assert len(scenes) == 13
    expected_states = {f'{n:02d}' for n in range(1, 14)}
    seen = {(str(s['state']).zfill(2), str(s['height']), s['motion']) for s in capture['screenshots']}
    expected = {(state, vp, motion) for state in expected_states for vp in ['1080', '720'] for motion in ['normal', 'reduced']}
    assert seen == expected, 'Need all thirteen holds at both sizes and both motion preferences'
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
            with Image.open(source) as decoded:
                width,height=decoded.size
                actual_mime=Image.MIME[decoded.format]
        else:
            actual_mime=supported[suffix]
        artifacts.append(dict(id=ident, kind=kind, path=dest, sha256=digest(source), mime=actual_mime,
                              label=ident, revision_id='final' if state else None, state_id=state,
                              viewport_id=viewport, motion=motion, fixture_id='argus-final-release' if state else None,
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
    artifact('exports-report', ROOT / 'evidence/exports-13/report.json')
    artifact('speaker-notes', ROOT / 'speaker-notes.json')
    for name in ['story.json', 'adapter.json']:
        file = ROOT / 'craft' / name
        if file.exists():
            artifact('craft-' + name.removesuffix('.json'), file)
    optional = [('source-index-current', ROOT / 'research/source-index.json'),
                ('visual-review', ROOT / 'evidence/visual-review.json'),
                ('powerpoint-report', ROOT / 'evidence/powerpoint-13/report.json'),
                ('browser-report', ROOT / args.browser_report),
                ('composition-report', ROOT / 'evidence/composition.json'),
                ('content-report', ROOT / 'evidence/content-report.json'),
                ('pdf-report', ROOT / 'evidence/pdf-report.json'),
                ('technical-audit', ROOT / 'research/technical-evidence.md'),
                ('frontend-audit', ROOT / 'research/frontend-evidence.md'),
                ('visual-audit', ROOT / 'research/visual-review-r3.json'),
                ('frontend-r3', ROOT / 'research/frontend-r3-summary.md'),
                ('source-index-r3', ROOT / 'research/revision-r3/source-index.json'),
                ('source-index', ROOT / 'research/source-snapshots/source-index.json'),
                ('fresh-mock-smoke', ROOT / 'research/smoke-mock-fresh.json')]
    optional += [('frontend-tests',ROOT/'evidence/frontend-tests.json'),('frontend-provenance',ROOT/'evidence/frontend-provenance.json'),('linq-proof-index',ROOT/'research/linq-proof-index.json'),('linq-handoff-summary',ROOT/'research/linq-proof__ml__reports__video-handoff-20261024.json'),('dataset-attribution',ROOT/'exports/ATTRIBUTION.txt')]
    for ident, file in optional:
        if file.exists():
            artifact(ident, file)
    documents = []
    for directory in [ROOT / 'docs', ROOT / 'sources']:
        if directory.exists():
            documents.extend(p for p in sorted(directory.rglob('*')) if p.is_file() and p.suffix.lower() in ['.md', '.json', '.txt'])
    # Final browser/HRE QA is written after sealing; keep its live report outside the immutable package.
    documents.extend(p for p in sorted(ROOT.glob('*.md')) if p.is_file() and p.name != 'VERIFICATION.md')
    for index, file in enumerate(documents, 1):
        artifact(f'doc-{index:02d}', file)
    for index in range(1, 14):
        file = ROOT / f'evidence/powerpoint-13/slide-{index:02d}.png'
        if file.exists():
            artifact(f'powerpoint-{index:02d}', file, 'image', notes='Actual installed PowerPoint raster export; native compatibility evidence.')
    # HRE MIME schema excludes PPTX/PDF. Describe downloads without mislabelling binaries.
    download_lines = ['Final presentation release exports. Human visual acceptance remains pending.', '']
    for file in sorted((ROOT / 'exports').glob('*')):
        if file.is_file():
            download_lines.append(f'{file.name}\nbytes: {file.stat().st_size}\nSHA-256: {digest(file)}\n')
    download_file = output / 'sources/exports.txt'
    download_file.write_text('\n'.join(download_lines))
    artifact('export-index', download_file)
    download_file.unlink()
    artifact('source-linq-image',ROOT/'assets/linq/ARGUS_linq_tpu_frame0.png','image',notes='Exact original user-supplied source image; all annotations preserved.')
    items = []
    for index, scene in enumerate(scenes, 1):
        state = f'{index:02d}'
        variants = []
        for vp in ['1080', '720']:
            for motion in ['normal', 'reduced']:
                variants.append(dict(viewport_id=vp, motion=motion, state_id=state,
                    before=dict(image=None, video=None, missing_reason='Earlier eight-scene skeleton uses a different narrative; no paired BEFORE supplied for the final twelve-scene release.'),
                    after=dict(image=ids[state, vp, motion], video=None, missing_reason='Static image slide. No per-slide motion recording is claimed.'),
                    compatibility=dict(status='INCOMPARABLE', reasons=['Different sequence and scene count; no fabricated historical pairing.'])))
        qa = [dict(label='Projection captures and stable source hashes', status='PASS', artifact_id='craft-report',
                   notes='Both projection sizes and motion preferences were captured. Raster text requires separate visual and typography checks.'),
              dict(label='PPTX pixels, geometry and notes', status='PASS', artifact_id='exports-report',
                   notes='Thirteen exact embedded images with full-bleed geometry. Consult report for native PowerPoint test status.'),
              dict(label='Craft criticism and human visual acceptance', status='UNVERIFIED', artifact_id='craft-report',
                   notes='DOM text detection does not read the flattened PNG. Critic findings remain preserved; no human verdict is preselected.')]
        items.append(dict(id='slide-' + state, title=f'{state} · {scene["title"]}',
                          delta='Final product narrative with authentic supplied UI captures and source-scoped technical claims.',
                          changes=[dict(path=f'slides/slide-{state}.png', description='Final 1920×1080 image and matching native speaker notes.')],
                          notes=['HUMAN_ARGUS_FINAL_REVIEW. Human acceptance pending.',
                                 'This review contains no human decision document.'],
                          references=list(document_ids) + (['source-linq-image'] if index == 9 else []) + ([f'powerpoint-{state}'] if (ROOT / f'evidence/powerpoint-13/slide-{state}.png').exists() else []),
                          qa=qa, variants=variants))
    inventory = {f'slides/slide-{n:02d}.png': digest(ROOT / f'slides/slide-{n:02d}.png') for n in range(1, 14)}
    snapshot = hashlib.sha256(json.dumps(inventory, sort_keys=True).encode()).hexdigest()
    manifest = dict(schema_version='1.0.0', renderer_version='1.0.0',
        review=dict(id='argus-final-release-production', revision=args.revision,
                    title='Финальная презентация · 13 слайдов',
                    description='HUMAN_ARGUS_FINAL_REVIEW. Полная image-based презентация; решения человека не заполнены.',
                    created_at=datetime.datetime.now(datetime.timezone.utc).isoformat()),
        revisions=dict(baseline=dict(id='unpaired', label='Earlier eight-scene skeleton: not paired', git_commit=None,
                                     snapshot_sha256=None, provenance='UNVERIFIED', notes='An earlier eight-slide skeleton exists; its sequence is not paired to this twelve-slide release.'),
                       current=dict(id='final', label='Final presentation release image-slide production', git_commit=None,
                                    snapshot_sha256=snapshot, provenance='VERIFIED',
                                    notes='Thirteen source PNG hashes and stable Craft capture inventory; human approval pending.')),
        viewports=[dict(id=str(h), label=f'{w} × {h}', width=w, height=h, device_scale_factor=1) for w, h in [(1920, 1080), (1280, 720)]],
        states=[dict(id=f'{n:02d}', label=s['title'], description='One manually advanced static image slide.') for n, s in enumerate(scenes, 1)],
        artifacts=artifacts, items=items)
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (output / 'manifest.sha256').write_text(digest(output / 'manifest.json') + '\n')
    # Launcher only; all rendering remains in the unchanged shared OS renderer.
    import html
    url = html.escape(args.renderer_url, quote=True)
    (output / 'index.html').write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><link rel="icon" href="data:,"><title>Human review</title><meta http-equiv="refresh" content="0;url=' + url + '"><a href="' + url + '">Open unchanged Human Review Engine v1.1</a></html>\n')
    print(json.dumps({'status': 'PACKAGED', 'items': len(items), 'artifacts': len(artifacts), 'output': str(output), 'human_acceptance': 'NOT ASSERTED'}))


if __name__ == '__main__':
    main()
