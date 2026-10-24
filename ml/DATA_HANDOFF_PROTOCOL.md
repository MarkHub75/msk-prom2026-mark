# Frozen dataset handoff — night cycle

Data Orchestrator owns /workspace/shared/dataset-handoff/READY.json and its immutable dataset-release-v1 manifests. ML never rewrites that pointer, merges its branch automatically or modifies its worktree. ML requests are in the separate shared ML_REQUIREMENTS.json. A changing producer worktree blocks ad-hoc ingestion; use the published immutable release instead.

`ml.quality.handoff.load_producer_ready` verifies the pointer's dataset/version/status, exact manifest file SHA256, every pinned file's bytes/SHA256, relative paths, class/split files and checksums registry. Callers must request an EXACT producer-approved use. A source-box diagnostic release cannot silently become training, independent test, wearer GT or exhaustive event evaluation. New producer schemas/versions require inspection, not automatic assumptions.

Previously frozen ML data has its own consumer-scoped snapshot: /workspace/shared/dataset-handoff/ml-baseline-night-v1/READY.json, version night-ml-baseline-snapshot-20261024-v1. It includes existing Helmet52 validation, Mendeley8 calibration and UR20 preview/source-reference data. This is hash/role verification of existing data, not a new Data Orchestrator endorsement or independent data audit. The separate consumer schema mosprom-dataset-handoff-v1 records rights scope, exact input groups/splits and task capabilities.

Before any model experiment call `load_ready(..., dataset_id=..., capability=...)`. READY for annotation is not READY for event_quality. Test inference needs an explicit final-evaluation gate; known group/source hashes cannot cross splits. Quarantined media permits metadata inspection only. All source bytes remain outside Git.

Integrity distinction: Helmet quality-v3 semantic digest is39e13db80621e4901f0eb0aa15d27b2f9b1cc8e2da951cb107b279532820de6a. Its serialized JSON FILE SHA256 is346f74cab99ddc2cc9c0f18b3efd95027a0b1ea782738469f502bc771dfd27e0. The semantic digest excludes the digest field and uses canonical JSON; it must never be used as a file byte checksum. Previous summary fields conflated these identities; no source GT/prediction or metric changed when correcting the documentation.

Current producer releases received: SHEL5K diagnostic19 (source-label QA only; UNKNOWN raw person attributes; no training/final-test approval), Mendeley factory replay16 (development/calibration/replay only; whole source is calibration-known). Native UR RGB and Running/Zone event labels are requested through handoff; nothing is inferred from a download directory or clip class.

No direct source discovery/download is done by ML. Files are opened only after scoped READY verification. Hash verification is repeated at experiment start, not assumed from an earlier mutable path. Missing or changing data is recorded as BLOCKED/NOT_MEASURABLE and does not trigger a network/storage workaround.
