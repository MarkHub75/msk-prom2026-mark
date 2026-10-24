"""Snapshot an actual built SPA plus its sources for OS/HRE static capture.

The OS static server has no SPA fallback. Exact index entry points preserve the
existing React routes without modifying the OS or running a mutable dev server.
"""
import argparse
import json
import shutil
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("--frontend", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--candidate", required=True)
args = parser.parse_args()
frontend = args.frontend.resolve()
output = args.output.resolve()
if output.exists():
    raise SystemExit("Use a new immutable source directory.")
if not (frontend / "dist/index.html").is_file():
    raise SystemExit("An actual successful production build is required.")
shutil.copytree(frontend / "dist", output)
routes = ["operator", "master", "master/shift", "ohs/journal", "ohs/rules", "ohs/stats", "management", "admin/cameras", "admin/system"]
routes += [f"operator/sectors/{n}" for n in range(1, 7)]
routes += [f"operator/cameras/{n}" for n in range(1, 13)]
routes += [f"events/{n}" for n in (41, 42, 43, 44)]
routes += [f"master/events/{n}" for n in (41, 42, 43, 44)]
for route in routes:
    entry = output / route / "index.html"
    entry.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(output / "index.html", entry)
implementation = output / "_source/frontend"
implementation.mkdir(parents=True)
for folder in ("src", "public"):
    shutil.copytree(frontend / folder, implementation / folder)
for filename in ("package.json", "package-lock.json", "index.html", "tsconfig.json", "vite.config.ts", "eslint.config.js"):
    shutil.copy2(frontend / filename, implementation / filename)
shutil.copytree(frontend.parent / "contract", output / "_source/contract")
project = {
    "name": "SafeWatch · " + args.candidate,
    "build": [],
    "required_assets": ["index.html", "fixtures/factory-cutting.png", "fixtures/factory-welding.png", "fixtures/factory-replay.mp4", "fixtures/factory-welding-replay.mp4", "fonts/fonts.css"],
    "serve_dir": ".",
    "flows": [{
        "id": "red-confirm-handoff", "signature": True,
        "steps": [{"action": "click", "selector": "a[href*='/events/41']"}, {"action": "click", "selector": "button[data-action='confirm']"},
                  {"action": "fill", "selector": ".actor-dialog input", "value": "Проверка рабочего сценария"},
                  {"action": "click", "selector": ".actor-dialog button[type='submit']"}],
        "expect": {"selector": "[data-testid='event-status']", "contains": "Передано мастеру"},
    }],
    "required_flows": ["red-confirm-handoff"],
    "truth": {
        "source_refs": ["_source/contract/openapi.json", "_source/contract/ws.schema.json", "_source/contract/ws-examples.json"],
        "limitations": ["Explicit synthetic review fixtures; generated media/manual boxes are not model results.", "Real S0 backend health and WS hello verified; business views/actions return 501.", "This is the first working product review, not final human acceptance or completed OS engineering qualification."],
    },
    "demo": {"seed": "explicit-critical-fixture-v1", "route": "/operator/?review=critical&reset=1", "startup": []},
    "snapshot": {"source_frontend": str(frontend), "prebuilt": True, "static_route_entrypoints": routes, "note": "Actual npm run gate/build evidence is preserved in run/evidence; no build or backend is synthesized by this packaging step."},
}
(output / "project.json").write_text(json.dumps(project, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"candidate": args.candidate, "source": str(output), "route_entrypoints": len(routes)}, ensure_ascii=False))
