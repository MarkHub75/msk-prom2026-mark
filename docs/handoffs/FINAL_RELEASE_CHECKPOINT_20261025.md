# MOSPROM-2026 — проверенная финальная передача

Код и измеренные результаты: fab9569db79e2bcdc547aca3fb9bf5b1bab25d4d, matvey_cv.
Основная сессия: docs/handoffs/FINAL_ML_EVIDENCE_20261025.md. Модели и подключение:
MODEL_REGISTRY_HANDOFF_20261025.md. Main не менялся, contract f6b5358a.

Для Егора:
- Preview13,061,488bytes: /workspace/artifacts/matvey-final-20261025/matvey_demo_preview_v1.zip
  SHA09bace977372f05876086f7882338c738acb75b11185be63b5c9758a82e00c27.
- Full291,139,722bytes: /workspace/artifacts/matvey-final-20261025/matvey_final_v1.zip
  SHA221d2fc1334d57ad3377087a93f571243c4c225506dd608867c6b97b211decc9.
- Главный actual CPU Argus demo: demos/S02_argus_local/annotated.mp4, event_frame_70.jpg.
- Остальные наборы: demos/S07_pose_and_fall/, demos/PPE_models/.

Для Марка: models/matvey_registry_additions.local.yaml, matvey_pipeline.local.yaml,
MODEL_REGISTRY_HANDOFF.md. В full ZIP включены и Pose/Helmet tar, и **отдельные COCO
reference files**, иначе primary local model_missing. Все ModelSpec types/class
maps прошли actual job:114CPU ONNX calls→event1/evidence1/GETAPI200,15.855s. FullCUDA
scenes12/2830frames отдельно, no skipped frames; actual CPU job38/75frames permodel.
Внешний JSONL importer отсутствует; не внедрять файлы в cache/DB. Пусть приложение
запустит штатный backend. Текущий PPE plugin отсутствует, S08skeleton — Марк owns.

Полный ZIP516members/515payload checksums проверен; распаковка и стандартный
VERIFY_PACKAGE.py в отдельном каталоге PASS без ML-пакетов.527testsOK(4skipped).
Main/чужие worktrees/сеть/службы/foreignqueues не менялись. GPUjob завершён,
16:53UTC snapshot GPU0/lockFREE. Новых моделей/training/compile0.

LinQ:15исторических completion на13source frames, raw→tail→actualArgusdecode/rules
MIXED replayPASS,0episodes/0freshTPU. Новые ownstaging/auth отсутствуют; liveLinQ→
appUI не проверен. Independent industrial event quality всех8 NOT_MEASURED.
Три demo sets не означают три принятых positive/negative quality pairs. S01running
upstream recall слаб, поэтому не основная демонстрация. Документы, JSON, метрики и
блокеры находятся в корне final pack. Модели заморожены без quality-promotion.

Shared pointer: /workspace/shared/ml-handoff/matvey-final-20261025/NOTICE.v1.json.
Фактическое прочтение/скачивание Марком/Егором не подтверждено. Local ZIP не является
проверенным off-Vast backup; внешний destination не предоставлен. Материалы не
публиковались. Если появится новый контракт/qualified producer release/ownstaging,
сверить его и выпускать новую версию, не менять выданный v1 и не повторять старые
исчерпанные гипотезы или legacy remote submissions.
