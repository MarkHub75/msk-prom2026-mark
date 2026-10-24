"""Portable companion to the real, controller-produced HRE packages.

Copies approved renderer packages verbatim; never edits a manifest or records a
human decision. Run from the OS checkout after present-products.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--run', type=Path, required=True)
parser.add_argument('--prior-run', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()
r, prior, out = args.run.resolve(), args.prior_run.resolve(), args.output.resolve()
if out.exists():
    raise SystemExit('Use a fresh version; existing review evidence is immutable.')
status = json.loads((r / 'evidence/present-products-final.json').read_text())
if status['stage'] != 'HUMAN_PRODUCT_REVIEW':
    raise SystemExit('Expected the real product-review gate.')
out.mkdir(parents=True)
validations = []
for review in status['human_reviews'].values():
    if review['capture_status'] != 'COMPLETE' or review['decision_imported']:
        raise SystemExit('Expected complete captures with human review pending.')
    dest = out / 'products' / review['candidate']
    shutil.copytree(r / review['package'], dest)
    if hashlib.sha256((dest / 'manifest.json').read_bytes()).hexdigest() != review['manifest_sha256']:
        raise SystemExit('Package identity changed.')
    result = subprocess.run(['node', 'production/human_review/validate-package.mjs', str(dest)], capture_output=True, text=True, check=True)
    validations.append(json.loads(result.stdout))
shutil.copytree(prior / 'concept-review/v3', out / 'concepts-v3')
result = subprocess.run(['node', 'production/human_review/validate-package.mjs', str(out / 'concepts-v3')], capture_output=True, text=True, check=True)
validations.append(json.loads(result.stdout))
for candidate in ['signal-post-command', 'signal-post-response']:
    shutil.copytree(prior / f'work/{candidate}-static-r1', out / 'sources' / candidate)
for rel in [
    'operator/human-concept-feedback-20261024.json',
    'operator/synthesis-approved-signal.json',
    'operator/component-expedition.json', 'operator/product-interpretations.json',
    'evidence/primary-gate-final.log',
    'evidence/actual-s0-integration.json',
    'evidence/same-origin-backend-delivery.json',
    'evidence/integration-independent-qa.json',
    'evidence/working-review-recovery.json',
    'evidence/signal-post-command-r1-source-identity.json',
    'evidence/signal-post-response-r1-source-identity.json',
    'evidence/fixture-media/fixture-manifest.json',
    'evidence/handoff-audit.json', 'evidence/handoff-next.json',
    'evidence/final-browser/signal-post-command-r1',
    'evidence/final-browser/signal-post-response-r1',
    'evidence/anti-slop/signal-post-command-r1.json',
    'evidence/anti-slop/signal-post-response-r1.json',
    'evidence/hre-browser-working-command-v2',
    'evidence/hre-browser-working-response-v1',
    'evidence/signal-post-response/connection-followup-gate.log',
]:
    src, dest = r / rel, out / rel
    if not src.exists():
        raise SystemExit('Required evidence missing: ' + rel)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)
for name in ['FIRST-READ.md', 'VERIFICATION.md']:
    dest = out / 'docs' / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.repo / 'docs/frontend-os' / name, dest)
(out / 'package-validation.json').write_text(json.dumps(validations, ensure_ascii=False, indent=2) + '\n')
(out / 'README.md').write_text('''# SafeWatch working review v1

Real OS4/HRE packages, copied verbatim from the registered revisions. The controller
remains at HUMAN_PRODUCT_REVIEW. Product acceptance and a final base choice are
not asserted. Concept signal-post was approved by the human; original feedback
and synthesis are included. Six earlier visual directions remain in concepts-v3.

products/: two sealed HRE packages, each 44 PNG + 4 WebM + 3 provenance documents.
sources/: exact frozen runnable builds with implementation and real contracts.
evidence/: source-bound browser workflows, gate results, anti-slop and S0 proof.

Main source SHA256: 7294c13b3f04090065e1d964978cf9f63e0a9adbbd2f0f166f70e73a0a6cae9f
Alternate SHA256: 37006b1071544ce995e10dc18d85784e202f6e8984f97032cc0d8425cb08717a

Full business journeys use explicit stateful contract fixtures. Actual S0 health
and WS hello pass; business API returns 501. Media are synthetic static-image
replays with manual frame-matched boxes, not CCTV or model/LinQ results.

HRE renderer is the existing approved production/human_review/renderer/v1.1.
Canonical review-serve URLs and restart commands are in the repository's
 docs/frontend-os/FIRST-READ.md. This companion creates no replacement renderer.

Known metadata note: automatic HRE artifact notes say command-served source is
unverified. The source snapshots, capture bindings, independent file hashes and
served asset manifests verify these static builds. The original sealed note has
been preserved, not rewritten. Human quality judgment remains pending.
''')
inventory = {str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file()}
(out / 'inventory.sha256.json').write_text(json.dumps(inventory, indent=2) + '\n')
archive = shutil.make_archive(str(out), 'zip', root_dir=out.parent, base_dir=out.name)
print(json.dumps({'result': 'PASS', 'directory': str(out), 'zip': archive, 'files': len(inventory), 'validations': validations, 'human_acceptance': 'NOT ASSERTED'}))
