"""One documented OS recovery using its CLI only; no Store/controller edits.

Reimport exact existing provenance and the actual human decision after an
immutable, CSS-sensitive HRE assertion blocked r2. Never regenerate products or
concepts, copy a root-bound database, synthesize approval, or bypass a stage.
"""
import json
import os
import shutil
import subprocess
from pathlib import Path

os_root = Path("/mnt/d/templates/frontend-hackathon-os")
old_run = os_root / "production/runs/safewatch-20261024-first-pass-r2"
new_run = os_root / "production/runs/safewatch-20261024-working-r3"
inputs = Path("/mnt/d/templates/msk-promhack/safewatch-os-inputs")
if new_run.exists():
    raise SystemExit("Recovery target exists; never overwrite a run.")
brief = json.loads((inputs / "brief-r2.json").read_text())
brief["summary"] = "SafeWatch first working frontend review. Exact human-approved Signal Post DNA and actual independently built products are imported from r2 after a CSS-case-sensitive immutable capture assertion failed. No new research, generation, product selection or human approval. React18/Vite/TS; operator, incident, mobile master and camera/HUD; real generated REST/WS v1.0.0 contracts. Explicit synthetic fixtures for coherent business journeys while actual S0 business methods answer501. Preserve all original independent contexts, raw images, human element feedback and exact source hashes."
brief["assets"] += [str(Path("/mnt/d/templates/msk-promhack/safewatch-os-first-pass/contract") / name) for name in ("openapi.json", "ws.schema.json", "ws-examples.json")]
brief_path = inputs / "brief-working-r3.json"
brief_path.write_text(json.dumps(brief, ensure_ascii=False, indent=2))
env = dict(os.environ, PYTHONPATH="production", PYTHONDONTWRITEBYTECODE="1")
counter = 0


def cli(*args, initial=False):
    global counter
    counter += 1
    result = subprocess.run(["python3", "-B", "-m", "hackathon_os.cli", "--run", str(new_run), *args], cwd=os_root, env=env, capture_output=True, text=True)
    target = inputs / "init-working-r3-output.json" if initial else new_run / f"evidence/recovery-cli/{counter:02d}-{args[0]}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(result.stdout + result.stderr)
    if result.returncode:
        raise SystemExit(result.stderr[-2000:] or result.stdout[-2000:])
    return result.stdout


cli("init", "--brief", str(brief_path), "--config", str(inputs / "config-r2.json"), initial=True)
for folder in ("assets", "evidence", "operator"):
    shutil.copytree(old_run / folder, new_run / folder, dirs_exist_ok=True)
recovery = {
    "from": str(old_run), "to": str(new_run),
    "cause": "40/44 HRE variants and4 recordings captured; CSS text-transform changed takeover innerText to uppercase, so4 assertions failed. Original pinned recipe cannot be amended at this stage.",
    "diagnosis": "evidence/hre-takeover-assertion-diagnosis.json",
    "correction": "Only HRE takeover expectation changed to stable event ID #41. Same exact source and browser evidence imported via supported CLI.",
    "os_source_modified": False, "store_copied": False, "regeneration": False,
    "human_authority": "Exact previous explicit user message, originally registered against safewatch-concepts r3 manifest fabd34e7ee30d4802c8aefa4743a63b0266e4635aa84e8f699c29dea79d799f3; no new product approval inferred.",
}
(new_run / "evidence/working-review-recovery.json").write_text(json.dumps(recovery, ensure_ascii=False, indent=2))
cli("creative-receipt", "reference", "--file", str(new_run / "operator/reference-primary.json"))
for file in sorted((new_run / "operator").glob("reference-R*.json")):
    cli("creative-receipt", "reference", "--file", str(file))
cli("creative-receipt", "explosion", "--file", str(new_run / "operator/theses.json"))
for thesis in json.loads((new_run / "operator/theses.json").read_text()):
    candidate = thesis["id"]
    for kind, suffix in (("context", "context"), ("reference", "reference"), ("concept-import", "images")):
        cli("creative-receipt", kind, "--candidate", candidate, "--file", str(new_run / f"operator/{candidate}-{suffix}.json"))
cli("present-concepts")
cli("human-feedback", "--file", str(new_run / "operator/human-concept-feedback-20261024.json"), "--actor", "Пользователь SafeWatch — ранее полученное явное сообщение в Codex", "--reason", recovery["human_authority"])
fresh = json.loads(cli("next", "--template", "synthesis", "--output", "operator/r3-synthesis.json"))
previous = json.loads((old_run / "operator/synthesis-approved-signal.json").read_text())
fresh.update(coherent_thesis=previous["coherent_thesis"], evidence="evidence/r3-creative-synthesis.json")
for target, source in zip(fresh["element_decisions"], previous["element_decisions"]):
    assert target["feedback_element_id"] == source["feedback_element_id"]
    target["treatment"] = source["treatment"]
(new_run / "operator/r3-synthesis.json").write_text(json.dumps(fresh, ensure_ascii=False, indent=2))
(new_run / fresh["evidence"]).write_text(json.dumps(dict(synthesis=fresh, original_human_authority=recovery["human_authority"]), ensure_ascii=False, indent=2))
cli("creative-receipt", "synthesis", "--file", str(new_run / "operator/r3-synthesis.json"))
cli("creative-receipt", "reference", "--file", str(new_run / "operator/component-expedition.json"))
cli("creative-receipt", "interpretations", "--file", str(new_run / "operator/product-interpretations.json"))
for candidate in ("signal-post-command", "signal-post-response"):
    for kind in ("context", "reference"):
        cli("creative-receipt", kind, "--candidate", candidate, "--file", str(new_run / f"operator/{candidate}-{kind}.json"))
    cli("review-spec", "--candidate", candidate, "--file", str(new_run / f"operator/{candidate}-capture-spec-v2.json"), "--actor", "Codex — оператор, авторизованный пользователем", "--reason", "Corrected stable-ID assertion, exact unchanged products and actual human-approved DNA; first r2 capture remains preserved.")
print(json.dumps({"run": str(new_run), "stage": "FULL_PRODUCT_BUILDS", "next": "Register exact already-tested slice receipts after recipe preflight; automatic HRE capture then anti-slop and HUMAN_PRODUCT_REVIEW."}))
