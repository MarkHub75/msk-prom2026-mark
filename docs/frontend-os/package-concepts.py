"""Package actual OS image concepts for the unchanged, approved HRE renderer.

This is a manifest author, not a renderer or a substitute for OS product review.
It never creates screenshots, product revisions, human decisions or approvals.
"""
import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--revision", type=int, default=1)
    args = parser.parse_args()
    run = args.run.resolve()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit("Output already exists; use a new review revision.")
    theses = json.loads((run / "operator/theses.json").read_text())
    receipts = {}
    for thesis in theses:
        candidate = thesis["id"]
        receipt = run / f"operator/{candidate}-images.json"
        if not receipt.is_file():
            raise SystemExit(f"Actual image receipt is missing: {candidate}")
        data = json.loads(receipt.read_text())
        if len(data["files"]) < 2:
            raise SystemExit(f"Two actual image frames are required: {candidate}")
        for path in data["files"]:
            source = (run / path).resolve()
            if not source.is_relative_to(run) or not source.is_file():
                raise SystemExit(f"Image is absent or outside run: {path}")
            with Image.open(source) as image:
                image.verify()
        receipts[candidate] = data
    output.mkdir(parents=True)
    artifacts, items, states = [], [], []
    viewports = {"concept-canvas": dict(id="concept-canvas", label="AI-концепты · не browser viewport", width=1600, height=1000, device_scale_factor=1)}
    copied = {}

    def artifact(identity, source, label, state=None, viewport=None):
        raw = source.read_bytes()
        sha = digest(raw)
        suffix = source.suffix.lower()
        media = suffix in (".png", ".jpg", ".jpeg", ".webp")
        path = ("assets/" if media else "sources/") + sha[:16] + "-" + source.name
        destination = output / path
        destination.parent.mkdir(exist_ok=True)
        if not destination.exists():
            shutil.copy2(source, destination)
        width, height = None, None
        if media:
            with Image.open(source) as image:
                width, height = image.size
        mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".webp": "image/webp", ".json": "application/json", ".md": "text/markdown"}.get(suffix, "text/plain")
        artifacts.append(dict(id=identity, kind="image" if media else "document", path=path,
                              sha256=sha, mime=mime, label=label,
                              revision_id="concept-batch-1" if state else None,
                              state_id=state, viewport_id=viewport, motion="normal" if state else None,
                              fixture_id=None, capture_mode=None, width=width, height=height,
                              provenance="UNVERIFIED",
                              notes="Actual file bytes hashed. AI design ideation or reference material; not a rendered SafeWatch implementation, browser capture, runtime fixture or integration proof."))
        copied[str(source.relative_to(run))] = sha
        return identity

    references = run / "evidence/reference-expedition"
    reference_doc = artifact("reference-index", references / "references.json", "12 конкретных визуальных источников и их перенос в SafeWatch")
    report_doc = artifact("reference-report", references / "REPORT.txt", "Что исследовано и ограничения доступа")
    process_doc = artifact("os-preflight", run / "evidence/preflight.json", "Настоящий preflight OS: browser readiness; не QA продукта")
    readiness_doc = artifact("product-readiness", run / "evidence/product-context/readiness.json", "Проверка настоящих контрактов и реализации: отсутствуют")
    critic_doc = artifact("independent-advisory", run / "evidence/concept-independent-review.json", "Независимое product-fit review · совет, не human approval")
    recovery_doc = artifact("os-recovery", run / "evidence/recovery.json", "Реальный сбой отчёта OS и исправленный import без изменения OS")
    reference_images = {}
    for key, filename, label in [
        ("milestone", "01-milestone-alarm-preview.png", "Milestone · alarm preview · общая экспедиция"),
        ("intenseye", "02-intenseye-evidence.webp", "Intenseye · evidence context · общая экспедиция"),
        ("vigilance", "06-vigilance-camera-grid.png", "Vigilance · видеокомпозиция · общая экспедиция"),
        ("behance", "07-behance-lms-life.png", "LMS LIFE · производственный контекст · общая экспедиция"),
        ("mobile", "10-avigilon-mobile-alerts.png", "Avigilon · mobile alerts · общая экспедиция"),
    ]:
        reference_images[key] = artifact("reference-" + key, references / "visuals" / filename, label)
    reference_map = {
        "signal-post": ["milestone", "vigilance"],
        "response-route": ["intenseye", "mobile"],
        "sector-atlas": ["behance", "vigilance"],
        "evidence-desk": ["milestone", "intenseye"],
        "shift-ribbon": ["mobile", "milestone"],
        "video-switchboard": ["vigilance", "milestone"],
    }
    for thesis in theses:
        candidate = thesis["id"]
        data = receipts[candidate]
        prompt_id = artifact(candidate + "-generation", run / data["generation_evidence"], "Исходный ответ image tool и точные промпты")
        variants = []
        for index, relative in enumerate(data["files"]):
            source = run / relative
            with Image.open(source) as image:
                width, height = image.size
            # One logical review frame keeps all directions visible together.
            # Original native pixel dimensions remain in each artifact above;
            # this is explicitly not a captured browser viewport.
            viewport = "concept-canvas"
            state = candidate + ("-dispatch" if index == 0 else "-incident-mobile" if index == 1 else f"-frame-{index+1}")
            label = "Диспетчерский пульт" if index == 0 else "Incident Focus и мобильный мастер" if index == 1 else f"Кадр {index+1}"
            states.append(dict(id=state, label=label, description="Сгенерированная визуальная гипотеза. Содержимое иллюстративно; API-контракт и реализация не подтверждены."))
            image_id = artifact(state + "-image", source, label + " · AI concept", state, viewport)
            variants.append(dict(viewport_id=viewport, motion="normal", state_id=state,
                                 before=dict(image=None, video=None, missing_reason="У нового направления нет baseline. Это первая концепция, не сравнение реализаций."),
                                 after=dict(image=image_id, video=None, missing_reason="Статичный AI-концепт; настоящего frontend capture, записи взаимодействия и reduced-motion evidence пока нет."),
                                 compatibility=dict(status="UNVERIFIED", reasons=["NO BASELINE. AI image concept, not a working product screenshot. No runtime/fixture equivalence is asserted."])))
        items.append(dict(id=candidate, title=thesis["operating_metaphor"],
                          delta=thesis["mental_model"],
                          changes=[dict(path=relative, description="Новый настоящий AI raster concept. Изменение визуальной гипотезы, не кода продукта и не working frontend screenshot.") for relative in data["files"]],
                          notes=[thesis["core_interaction"], "Почему: " + thesis["problem_fit"],
                                 "Запоминающийся момент: " + thesis["remembered_moment"],
                                 "HUMAN_CONCEPT_REVIEW: можно сохранить, убрать, усилить или сочетать отдельные элементы. Автоматического победителя и решения от имени человека нет.",
                                 "Все значения, состояние камер, события, footage и разметка на концепте иллюстративны. При реализации продуктовые источники и generated contracts имеют приоритет."],
                          references=[reference_doc, report_doc, prompt_id, readiness_doc, critic_doc, recovery_doc] + [reference_images[key] for key in reference_map[candidate]],
                          qa=[dict(label="Реализация, API, browser journeys", status="MISSING", artifact_id=readiness_doc,
                                   notes="До human concept feedback и появления реального OpenAPI/WS не заявляются."),
                              dict(label="OS browser readiness", status="PASS", artifact_id=process_doc,
                                   notes="Preflight реально запущен и отрендерил тестовую страницу. Это проверка инструментария OS, не SafeWatch.")], variants=variants))
    snapshot = digest(json.dumps(copied, sort_keys=True).encode())
    manifest = dict(schema_version="1.0.0", renderer_version="1.0.0",
                    review=dict(id="safewatch-concepts", revision=args.revision, title=f"SafeWatch · HUMAN_CONCEPT_REVIEW · v{args.revision}",
                                description="Шесть независимых направлений, по два настоящих AI raster frame. Это концептуальный checkpoint штатной OS, не готовый фронтенд. Скриншоты реализации 1440×900 / 390×844 и доказательства интеграции отсутствуют и не подменяются концептами.",
                                created_at=datetime.now(timezone.utc).isoformat()),
                    revisions=dict(baseline=dict(id="no-baseline", label="Первый проход: baseline отсутствует", git_commit=None, snapshot_sha256=None, provenance="UNVERIFIED", notes="Нет предыдущего принятого дизайна для сравнения."),
                                   current=dict(id="concept-batch-1", label="OS image concepts · batch 1", git_commit=None, snapshot_sha256=snapshot, provenance="UNVERIFIED", notes="Hash фиксирует байты реальных концепций и их provenance; served product revision не существует.")),
                    viewports=list(viewports.values()), states=states, artifacts=artifacts, items=items)
    raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
    (output / "manifest.json").write_bytes(raw)
    (output / "manifest.sha256").write_text(digest(raw) + "\n")
    (output / "source-inventory.json").write_text(json.dumps(copied, ensure_ascii=False, indent=2) + "\n")
    release = run.parents[1] / "human_review/renderer/v1.1/release.json"
    (output / "renderer-identity.json").write_text(json.dumps(dict(renderer_version="1.1.0", release_sha256=digest(release.read_bytes())), indent=2) + "\n")
    print(json.dumps(dict(package=str(output), review=manifest["review"]["id"], items=len(items), artifacts=len(artifacts), manifest_sha256=digest(raw), human_acceptance="NOT ASSERTED")))


if __name__ == "__main__":
    main()
