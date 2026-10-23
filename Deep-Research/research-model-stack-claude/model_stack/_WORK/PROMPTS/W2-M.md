# W2-M HOST_BUDGET_TRACKER — бюджет CPU-хоста, TrackTrack, эталонные скорости RTX 4070/CPU

Модель: Claude Sonnet 5.5, effort medium. Почему: измерения по готовым скриптам и чтение одного трекера — точная, но прямолинейная работа. Закрывает K027, K028, K030.

Прочитай `ROOT\_WORK\CONTEXT.md`, `ROOT\_WORK\CONTEXT_WAVE2.md` (GPU-блокировка), в `ROOT\CRITIC.md` — K027, K028, K030, проверку 4. Опорные: `W1-10_EXPORT_ONNX.md` (6.4), `W1-11_PRE_POST.md` (Q8, скрипты декода), `W1-13_CASCADES.md` (F17–F23, §3.2, E4), `W1-12_QUANT_LINQ.md` (F17 — pytpu FULL), `W1-14_METRICS.md` (§6.4, E3), `W1-09_ENVIRONMENTS.md` (F30 — CPU хоста). Читай FLASH `W2-F_REAL_FINETUNE.md` (GPU-venv готов?).

Результат: `ROOT\_WORK\WAVE2\W2-M_HOST_BUDGET_TRACKER.md` (+ `W2-M_files\`: скрипты, json p50/p95).

## Что сделать
1. CPU-замеры (p50/p95, warmup, ≥100 повторов, версии библиотек, модель CPU из системы): letterbox+нормализация 1080p→640 (cv2), numpy и torch декод 8400 якорей (DFL для v8/11; reg_max=1 для 26; anchor-based v5), class-aware NMS (torchvision и cv2.dnn), декод pose 17 точек, 8/16 кропов 224 + нормализация, `BYTETracker.update` и TrackTrack при N = 5/20/50 детекций, float32↔int8 конверсия тензора выхода как у pytpu (оценка).
2. ORT-CPU latency yolov8n/yolo11n/yolo26n при 640 (запасной путь без LinQ).
3. RTX 4070 (по блокировке, GPU-venv после FLASH W2-F): PyTorch fp32/fp16 и ORT CUDA для yolov8n/yolo11n/yolo26n при 640 — раздельно preprocess/inference/postprocess, драйвер/CUDA версии. TensorRT — только если ставится быстро, иначе пропусти с причиной.
4. TrackTrack (K028): `ultralytics/cfg/trackers/tracktrack.yaml` и реализация в 8.4.184 — параметры, учёт FPS, ReID/GMC, зависимости, контракт входа/выхода; отличие от ByteTrack; как явно выбрать трекер.
5. Итог: сколько камер × FPS выдерживает хост при одной модели на LinQ (с неизвестной латентностью LinQ как параметром).

Попытайся опровергнуть: «узкое место — LinQ, а не хост».
