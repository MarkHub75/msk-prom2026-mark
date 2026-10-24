"""Portable copy of the real OS/HRE targeted review, with separate QA evidence."""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--run', type=Path, required=True)
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
r, repo, out = args.run.resolve(), args.repo.resolve(), args.output.resolve()
if out.exists():
    raise SystemExit('Preserve immutable delivery; choose a new version.')
status = json.loads((r / 'evidence/integrated-final-product-registration.json').read_text())
if status['stage'] != 'HUMAN_FINAL_PRODUCT_REVIEW':
    raise SystemExit('Actual final product review checkpoint required.')
review = status['human_reviews']['hre-signal-post-integrated-v1-b1-r0']
if review['capture_status'] != 'COMPLETE' or review['validation'] != 'PASS':
    raise SystemExit('Complete validated canonical HRE package required.')
out.mkdir(parents=True)
shutil.copytree(r / review['package'], out / 'product')
shutil.copytree(r / 'work/signal-post-integrated-v1-static', out / 'source')
# Exact approved renderer, including its v1 contract dependency and release seal.
hre = Path('production/human_review')
shutil.copytree(hre / 'renderer', out / 'human_review/renderer')
shutil.copytree(hre / 'schemas', out / 'human_review/schemas')
shutil.copy2(hre / 'validate-package.mjs', out / 'human_review/validate-package.mjs')
validation = subprocess.run(['node', str(out / 'human_review/validate-package.mjs'), str(out / 'product')], capture_output=True, text=True, check=True)
(out / 'package-validation.json').write_text(validation.stdout)
for rel in [
    'operator/human-product-keep-completion.json',
    'operator/signal-post-integrated-v1-capture-spec.json',
    'operator/signal-post-integrated-v1-final-product.json',
    'evidence/human-product-review-keep-20261024.md',
    'evidence/signal-post-integrated-v1-source-identity.json',
    'evidence/integration-targeted-gate.log',
    'evidence/final-browser/signal-post-integrated-v1',
    'evidence/external-mock-v2',
    'evidence/real-backend-targeted-v1',
    'evidence/final-anti-slop-integrated-v1',
    'evidence/targeted-ui-final-dev-r2',
    'evidence/hre-browser-integrated-v1',
    'evidence/fixture-media/fixture-manifest.json',
]:
    src, dest = r / rel, out / rel
    if not src.exists():
        raise SystemExit('Missing required evidence: ' + rel)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)
for name in ['FIRST-READ.md', 'FRONTEND_STATUS.md', 'INTEGRATION_REVIEW_v2.md']:
    dest = out / 'docs' / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(repo / 'docs/frontend-os' / name, dest)
(out / 'README.md').write_text('''# SafeWatch targeted working review v2

Real OS4 final-product package, copied verbatim; original approved HRE renderer
1.1 and schemas included with release verification. 12 corrected states,
48 browser screenshots and four actual master-workflow recordings.
No new visual concepts. Actual human KEEP and targeted correction brief retained.
Final acceptance is NOT ASSERTED: controller is at HUMAN_FINAL_PRODUCT_REVIEW.

Run a local read-only server from this directory:
python3 -m http.server 8195 --bind 127.0.0.1
Open http://127.0.0.1:8195/human_review/renderer/v1.1/index.html?manifest=../../../product/manifest.json

This portable copy supplements the canonical OS review-serve; it does not replace
the controller or invent decisions. Canonical review ID and manifest seal are in
product/manifest.json. Do not edit sealed artifacts. Import real human exports
through the original run's review-import, never fabricate an export.

source/: exact frozen app, implementation and real contracts. Source SHA256:
1b93f388841ce64793e175ba639ef6443ba86033fbe3ddf8b55e7a5445d0efb9

To rebuild the archived implementation, use source/_source/frontend (npm ci and
npm run gate). For the external mock provide its explicit nonsecret URLs:
VITE_API_BASE=http://127.0.0.1:4010 VITE_WS_URL=ws://127.0.0.1:4011/ws npm run dev:mock
The mock itself remains in its separate demo/checkpoint worktree.

Evidence scopes are separate: HRE uses deterministic local UI fixtures;
external-mock-v2 is actual REST4010/WS4011 browser E2E PASS8/8 with25 captures;
real-backend-targeted-v1 proves S0 health/WS and business501, not full integration.
The attempted newer S5 runtime lacked cv2; latest R5 was not runtime verified.
Gate passed19 tests, lint, TypeScript, generated contract check and build.

Media are explicitly synthetic, with manual frame-matched boxes. No CV/LinQ/live
CCTV quality claim. Unsuitable fall evidence was removed rather than presented.
Known P2:15px of the expanded desktop closed-history journal link are clipped;
the normal journal navigation works. Player refresh may remount to replay state.

Automatic HRE artifact notes retain the existing generic command-served-source
wording. Actual static served manifests and all115 source hashes were verified
independently; original sealed notes are preserved unchanged.
''')
inventory = {str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file()}
(out / 'inventory.sha256.json').write_text(json.dumps(inventory, indent=2) + '\n')
archive = shutil.make_archive(str(out), 'zip', root_dir=out.parent, base_dir=out.name)
print(json.dumps({'result': 'PASS', 'zip': archive, 'files': len(inventory), 'manifest_sha256': review['manifest_sha256'], 'validation': json.loads(validation.stdout), 'human_acceptance': 'NOT ASSERTED'}))
