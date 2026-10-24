# Запуск восьми сценариев

Все сценарии используют один существующий ML-конвейер. Это opt-in прототипы; специальные детекторы/действия и site policy пока не квалифицированы. Default-конфиги намеренно не придумывают цех, зоны и наблюдаемые состояния.

## Одной командой — 24 явно синтетические проверки

```bash
cd /workspace/project
/workspace/.venvs/linq-client/bin/python -m ml.scenarios.cli \
  --state-dir /workspace/artifacts/matvey-scenarios/NEW-acceptance \
  --synthetic-all --synthetic-evidence
```

Каждая из восьми групп получает positive/negative/unknown вход. Чёрные JPEG подписаны SYNTHETIC; модель/видео не запускаются. `coverage-acceptance.json` не является accuracy. Проверенный freeze-run: `/workspace/artifacts/matvey-scenarios/freeze-acceptance-v1/`.

## Реальное видео и сохранённые native наблюдения — без нового инференса

```bash
/workspace/.venvs/linq-client/bin/python -m ml.scenarios.cli \
  --state-dir /workspace/artifacts/matvey-scenarios/NEW-fall06-replay \
  --config configs/scenarios/suite.example.json \
  --input /workspace/artifacts/matvey-scenarios/ur07-video-evidence-v1/fall-06-cam0/inputs.observations.jsonl \
  --source-video /workspace/datasets/quality/temporal/processed/urfall/fall-06-cam0-rgb.mp4
```

Этот пример уже проверен: подозреваемое падение с start1500ms/confirm2500ms, evidence originalframe75. Наблюдения созданы native-моделью ранее; повтор не вызывает ни GPU, ни LinQ. Это не новая аппаратная проверка. Ordinary reference ADL01 (10observations) не дал кандидатов. Полный отчёт: `/workspace/artifacts/matvey-scenarios/ur07-video-evidence-v1/check.json`.

Без --source-video evidence честно unavailable. С видео требуются совпадающие source SHA256, размер, исходный frame index и encoded PTS. Frame provider читает последовательно по ordinal, не полагается на приблизительный seek. Nonzero origin сохраняется:6_tr15 encodedfirst39.028ms, не OpenCV-relative0. Нужен уже установленный ffprobe; нет автоматического timestamp/FPS fallback.

## Свежий видеоинференс через существующий LinQ клиент

Команда готова как путь интеграции, **пока заблокирована предпосылками**, а не объявлена выполненной:

```bash
# Только после ownMatvey staging и проверенного namespace-aware manifest:
# runtime secrets загрузить в процесс из private connection.env без set -x/печати.
/workspace/.venvs/linq-client/bin/python -m ml.pipeline.cli \
  --state-dir /workspace/artifacts/matvey-scenarios/NEW-live-linq \
  --scenario-config /path/to/reviewed-site-suite.json \
  video --source /path/to/approved-real-video.mp4 --camera-id REVIEWED-CAMERA \
  --backend linq --manifest /path/to/verified-matvey-pose-manifest.json \
  --linq-runner-factory ml.linq.video:create_runner --sample-fps 2
```

Подключаются те же preprocess/decoder/transport/admission; GPU fallback не добавлен. Specialist model manifests добавляются только после проверки checkpoint/ONNX/compile/PTQ/ABI/LinQ. Исходный Pose TPU уже работал, но это не доказательство отсутствующих phone/машина/harness/action моделей. GMD4fold temporal heads — export-only; они не включены автоматически.

Не запускать эту команду со старым root-cache program_name. `docs/JUPYTER_RUNBOOK.md` описывает отдельный Matvey bootstrap; он подготовлен, не опубликован. Сеть, VPN, SSH и очереди капитана не перенастраивать. Весь новый remote контент только matvey/, имена matvey_, собственная очередь с полным UUID, max1ownactiveTPUtask.

## Конфигурация и наблюдаемость

Восемь модулей и8JSON лежат в ml/scenarios/rules и configs/scenarios. Suite example объединяет их; копировать для конкретной камеры. Любая site-policy требует camera_id и original image_size. Geometry/policy source/revision должны отражать реальную площадку. Для image-motion01/02 требуется stationary_camera_declared плюс camera_policy_source; неизвестная камера возвращает UNKNOWN, а не бег/движение механизма. Pixels/body-heights не являются метрами или физической скоростью.

Нормализованные observations остаются v1. Дополнительные facts описаны в SCENARIO_RUNTIME_CONTRACT: уникальный track/object, текущие кадр/PTS, confidence и источник. Для non-synthetic обязательны camera_id/stream_epoch и source_sha256 при известном media hash. Неправильный источник/дубликат/stale fact не используется. Повторяющиеся object IDs изолируются, их coverage становится unknown. Синтетическая поблажка допустима только с backend=synthetic-test и остаётся явно маркированной.

Правила требуют фактически наблюдаемых action/ownership/visibility, которые будущие qualified модели должны поставить. Источник модели не подменяется GT, именем файла или отсутствующей аннотацией. Harness present сам по себе не означает in_use; bed lying не равно lying on floor; дымка не равно smoking/fire; overlap/linecrossing не равно climbing.

## Выходы и контракт

- `events.sqlite`: общий атомарный checkpoint, legacy outbox и отдельные scenario_candidates/scenario_diagnostics.
- `candidates.jsonl`: внутренний EventCandidate schema ml/contracts/schemas/event_candidate.schema.json; candidate_id/revision/camera/epoch/track/scenario/subrule/start/confirm/evidence/provenance/qualification. Confidence может быть null; это не calibrated probability.
- `scenario-diagnostics.jsonl`: POSITIVE/NEGATIVE/UNKNOWN/BLOCKED по каждому обработанному наблюдению; gap не является compliance.
- `evidence/*.jpg` и sidecarJSON: source frame/PTS, RGB/media/snapshot hashes.
- `scenario-summary.json`: режим replay, suite/component hashes, число эпизодов; не нейросетевая производительность.

Внешний EventMutation v1 не расширялся. Новые кандидаты не отправляются в HTTP endpoint Марка; старые missing_helmet/suspected_fall/prolonged_lying продолжают прежний путь. Для будущего внешнего транспорта нужен отдельно согласованный mapping, а не отправка новых типов в старый validator. 07кандидаты одной исходной legacy-истории содержат episode_group_id для последующей группировки.

Один state-dir — один writer-lock до чтения checkpoints. Event/candidate/behavior/suite/video состояние коммитятся одной SQLite транзакцией. Перезапуск повторно не добавляет UUID/revision, изменённый уже принятый frame input отклоняется. UNKNOWN прерывает подтверждение; продолжение не получает длительность пропуска. Не удалять state/journal для повторения неопределённого LinQ запроса.

## Требуемые образцы

Для каждого недоступного сценария нужен короткий continuous положительный эпизод и обычный/трудный отрицательный с actor/time/unknown/occlusion разметкой, правами и source-group split.02: техника/человек/движение и утверждённая опасная геометрия;03: видимый ownedphone+use+activity;04: отличимые cigarette/flame/steam и разрешённые места;05: отдельные crossing/underpass и состояние оборудования;06: высотная зона+наблюдаемое use/attachment;08: ownedload и конкретное правило. Объёмы/annotation fields/checkpoint/ABI перечислены в Training requirements; не скачивать или обучать из неподходящего READY.
