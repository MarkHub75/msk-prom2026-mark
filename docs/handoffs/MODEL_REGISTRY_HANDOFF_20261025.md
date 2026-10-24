# Модели для Марка

Код Argus не менялся. Проверен main f6b5358afee60d1190f5b5e9decc77292b9087c9; более нового ML_INTEGRATION не получено. Добавления только к реестру/собственному config/user.yaml. Веса не менялись, training/compile новых моделей0.

| Роль | id@version | Классы | Граф |
|---|---|---|---|
|detector|coco-reference-yolov8n@640-v1-a6a8c37f7e45|COCO80, потребляемые0:person/2:car/5:bus/6:train/7:truck/67:cell phone|[1,84,8400], full COCO80, не Matvey-trained, TPU compile/execution отсутствует|
|pose|matvey-pose-yolov8n@640-v1-acc5f51228b9|0:person,17COCO triples|tail[1,56,8400], historical program SHA c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b|
|extra|matvey-helmet-yolov8n@640-v1-5c3af1f3b855|0:helmet,1:no_helmet; source bare_head→no_helmet only|[1,6,8400], historical program SHA408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa|

Точные веса, все локальные ONNX/head/tail/TPU SHA, классы, export/compile statuses: `models/MODEL_REGISTRY.json`. Уже проверенный Pose/Helmet tar: `models/matvey_safewatch_delivery_v2.tar.gz`, SHA7cfcf125189f4e0034d1de7a88033d465c0c6be453cee5f145a3ca3755f3892b. Он содержит только две модели. **COCO reference отдельно**: `models/coco_reference/models/`; скопировать этот `models/` в корень приложения дополнительно к распаковке tar. Этот пробел обнаружен фактическим local test v1/model_missing, исправлен в v2.

Минимальное подключение для проверенного local пути:

1. В собственном checkout Argus распаковать tar в корень, затем скопировать содержимое `models/coco_reference/models/` в `<Argus>/models/` с сохранением структуры. Проверить SHA по MODEL_REGISTRY.json.
2. Добавить ещё отсутствующие записи из `models/matvey_registry_additions.local.yaml` в config/models.yaml. Записи содержат все10 ModelSpec fields, `linq_program:null` намеренно: это local-only config. Не переименовывать baseline и не подменять старые версии.
3. Применить `models/matvey_pipeline.local.yaml` к собственному config/user.yaml, сохраняя остальные extras при необходимости (список заменяется целиком). `INFERENCE_BACKEND=local SAFEWATCH_FAKE=0 uv run safewatch doctor`. Дальнейший запуск приложения выполняет Марк; эта передача не запускает сервер.
4. Импортировать `scenes/S01_3_tr45/original.mp4` через штатный импорт в реальную настроенную камеру. Пример: `uv run safewatch import <полный-путь-к-MP4> --camera <camera_id>`. Не импортировать наши JSONL напрямую в cache/DB: внешнего импортера нет. Argus посчитает собственные результаты.

Артефакты `scenes/*/argus/*.jsonl` — действительный FrameDetections (frame_idx,ts_ms,detections{cls,name,score,bbox_xyxy,kpts}). ModelSpec.classes определяет имена; COCO67=`cell phone`, техника только car/bus/train/truck в primary. Extra forklift не поддержан. Helmet принимается как ObjectState, но PPE rule не существует. S08 load_carrying skeleton. Правила/события/зоны изменяет Марк.

Реестр conf.1 vs полный saved GPU export conf.25; raw local tensors не сохранены, ниже.25 восстановить нельзя. Current app OpenCV INTER_LINEAR /255, saved native/historical Pillow bilinear ×1/255. Это разные входы, не обещать bitwise parity. Actual local job v2 использовал настоящий OpenCV и conf.1. Для replay создаётся отдельный hash-versioned ModelSpec; артефакты не внедряются в кэш.

Кэш Argus не включает file/class/threshold SHA. Любые новые bytes/tail/class map/conf/iou требуют новой version. `ml.argus_replay.fingerprint` учитывает эту идентичность; тест и реальные cache_key проверки подтвердили invalidation при смене version. Новые модели не выпускались.

**LinQ live пока BLOCKED:** own matvey staging receipts отсутствуют. Canonical tar содержит старые локальные mosprom_matvey filenames; это не разрешение на remote placement. Не использовать стандартный uploader, который пишет mosprom_work/baseline/root-cache. Новые own remote файлы толькоmatvey/, именаmatvey_, максимум1 own request, без legacy unisolated bindings. Изменение namespace поддержки приложения остаётся у Марка. Исторический successful TPU reply не доказывает новое размещение.
