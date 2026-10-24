# SafeWatch image-slide tooling

This is the supported Presentation Craft 1.0.0 raster-slide route, adapted from
`production/presentation_factory/cinematic-ppt-v1/final-production` in Frontend
Hackathon OS. The deliverable is a native image-based PowerPoint. The browser
harness is used only for projection evidence and human review.

Inputs owned by the presentation director:

- `slides/slide-01.png` … `slides/slide-08.png`, exactly 1920×1080.
- `speaker-notes.json`, an array of eight `{id, title, speech, notes?, sources?, duration?}`
  objects. `id` is `01` … `08`; `sources` is text or an array of source strings.
- `craft/story.json`, `craft/adapter.json`, and `craft/capture.html?slide=1` … `8`.
- Technical source ledger and visual/composition checks in `docs/` or `sources/`.

Local isolated toolchain:

- Python: `/tmp/safewatch-pptx-toolchain/bin/python` (Pillow, fonttools, brotli,
  PyMuPDF, numpy; product dependencies are untouched).
- PptxGenJS 4.0.1: `/tmp/safewatch-pptx-toolchain/node_modules/pptxgenjs/dist/pptxgen.es.js`.
  This exact version is pinned in the OS Jury Defense package lock.
- Existing OS Playwright:
  `/mnt/d/templates/frontend-hackathon-os/evals/creative-app/e2e-03-mosaic/node_modules/playwright/index.mjs`.
- Existing Chromium:
  `/home/egor/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome`.

Run from the presentation directory after final images and notes exist:

```bash
SAFEWATCH_PPTXGENJS_MODULE=/tmp/safewatch-pptx-toolchain/node_modules/pptxgenjs/dist/pptxgen.es.js \
node scripts/exports.mjs
```

The exporter writes `exports/SafeWatch_Checkpoint_2026-10-24.pptx`: eight full-bleed
PNGs and native speaker notes. Internal raster content is not separately editable.

Actual installed desktop PowerPoint open/render verification (from WSL):

```bash
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass \
  -File 'D:\templates\msk-promhack\safewatch-checkpoint-pptx\presentations\checkpoint-2026-10-24\scripts\powerpoint-check.ps1'
/tmp/safewatch-pptx-toolchain/bin/python scripts/verify-exports.py --require-powerpoint
```

The COM script closes only the presentation it opened. It quits PowerPoint only
when there were no presentations before the check. It does not certify manual
dialog observation or auditorium projection conditions.

Serve the presentation root on 8724, then run the unchanged OS Craft capture:

```bash
CRAFT_PLAYWRIGHT_MODULE=/mnt/d/templates/frontend-hackathon-os/evals/creative-app/e2e-03-mosaic/node_modules/playwright/index.mjs \
CRAFT_CHROMIUM=/home/egor/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome \
node /mnt/d/templates/frontend-hackathon-os/production/presentation_factory/craft/v1/capture.mjs \
  craft/adapter.json evidence/craft
```

`evidence/craft` must be new. The adapter uses `root: ".."`,
`baseUrl: "http://127.0.0.1:8724/"`, `runtime: "dom"`, and one hold per slide.
The harness marks its settled image with `[data-craft-settled="true"]` only after
the actual PNG has decoded. The standard capture produces 32 screenshots plus
glance derivatives. DOM `missing-assertion` findings are expected for raster
text and must remain in the report; exact typography and legibility require
separate checks. Do not add hidden assertion text to manufacture a PASS.

For the Human Review Engine, serve the common source root separately:

```bash
python3 -m http.server 8725 --bind 127.0.0.1 --directory /mnt/d/templates
/tmp/safewatch-pptx-toolchain/bin/python scripts/package-review.py
node /mnt/d/templates/frontend-hackathon-os/production/human_review/validate-package.mjs review
```

Open the review through the common server:

`http://127.0.0.1:8725/msk-promhack/safewatch-checkpoint-pptx/presentations/checkpoint-2026-10-24/review/`

The launcher references the unchanged shared OS HRE v1.1 renderer. The package
has eight new slides, no fabricated historical BEFORE, no selected verdict and
no human decision document. `--capture-report` and `--renderer-url` can override
the evidence location and server URL. A sealed review refuses overwrite.

Final checkpoint: `HUMAN_SAFEWATCH_CHECKPOINT_PRODUCTION_REVIEW`. Artifact
delivery and technical checks may complete before this checkpoint. Human
visual acceptance remains pending until an actual user decision arrives.

The final delivery uses revision 2 after a chronology clarification in one
speaker note. The eight slide PNGs are byte-identical between revisions.
The first sealed review and receipts remain historical evidence. Use these
paths/commands for the final revision:

```bash
CRAFT_PLAYWRIGHT_MODULE=/mnt/d/templates/frontend-hackathon-os/evals/creative-app/e2e-03-mosaic/node_modules/playwright/index.mjs \
CRAFT_CHROMIUM=/home/egor/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome \
node /mnt/d/templates/frontend-hackathon-os/production/presentation_factory/craft/v1/capture.mjs \
  craft/adapter.json evidence/craft-r2

/tmp/safewatch-pptx-toolchain/bin/python scripts/package-review.py \
  --output review-r2 --revision 2 --capture-report evidence/craft-r2/report.json \
  --browser-report evidence/browser-r2/report.json \
  --renderer-url 'http://127.0.0.1:8725/frontend-hackathon-os/production/human_review/renderer/v1.1/index.html?manifest=/msk-promhack/safewatch-checkpoint-pptx/presentations/checkpoint-2026-10-24/review-r2/manifest.json'

node /mnt/d/templates/frontend-hackathon-os/production/human_review/validate-package.mjs review-r2
SAFEWATCH_CRAFT_EVIDENCE=evidence/craft-r2 \
SAFEWATCH_BROWSER_EVIDENCE=evidence/browser-r2 \
SAFEWATCH_REVIEW_URL=http://127.0.0.1:8725/msk-promhack/safewatch-checkpoint-pptx/presentations/checkpoint-2026-10-24/review-r2/ \
node scripts/browser-qa.mjs
```

Capture and review output directories are immutable; a further revision needs
new directories and an incremented review revision, not an overwrite.

After source PNGs/notes are frozen, Craft capture has completed, and the review
package is served, run the independent browser QA:

```bash
node scripts/browser-qa.mjs
```

This uses a new context for each inspection scope, checks all eight image states
at both projection sizes, verifies the four HRE viewport/motion variants and
opens one image inspector. It never selects a verdict. It then records a full
silent sequence with 280 seconds of holds from `speaker-notes.json`, logging a
heartbeat at least every 15 seconds. Run the process with short tool yields so
the presentation director can keep communicating. Output is
`evidence/browser/report.json` and `complete-280s-sequence.webm`; navigation
overhead is measured, and spoken rehearsal is explicitly unverified. An existing
browser report is never overwritten.
