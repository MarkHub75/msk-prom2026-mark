# Контракт «ML ↔ приложение SafeWatch»

Для ML-части (Матвей и его Codex). Проверено по коду `main` на 2026-10-24, исходный коммит `5d940ba22ebebb2255ff7b12252268c3d9d393ab` (`tech.md` v4, включая дополнения 6.8–6.10). Ссылки `файл:строка` ниже относятся к исходному коду этой ревизии; текущая правка меняет только этот документ.

Совместимая модель подключается без правок кода с обеих сторон: положить файлы, добавить запись в `config/models.yaml` и переключить `pipeline` в конфиге. Это работает для описанных ниже ABI и существующих сценариев; произвольная архитектура или новая логика СИЗ автоматически не подключатся. Всё, что требует правки приложения, вынесено в раздел 9. SafeWatch сам формирует эпизоды и пишет их в свою БД; Матвею не нужен отдельный отправитель событий в REST API (`src/safewatch/services.py:825`, `src/safewatch/analysis/pipeline.py:143`).

Опорные места кода (ссылки открываются из репозитория): [ModelSpec — types.py:279](../src/safewatch/types.py#L279), [реестр — registry.py:15](../src/safewatch/registry.py#L15), [FrameDetections — types.py:810](../src/safewatch/types.py#L810), [LinQ — linq.py:139](../src/safewatch/inference/linq.py#L139), [local — local.py:59](../src/safewatch/inference/local.py#L59), [выдача extra — pipeline.py:107](../src/safewatch/analysis/pipeline.py#L107), [статусы сценариев — rules/__init__.py:45](../src/safewatch/rules/__init__.py#L45), [eval — evaluate.py:17](../src/safewatch/evaluate.py#L17).

## 1. Что приложение ждёт от модели

### 1.1 Файлы

| Файл | Где лежит | Кто читает | Обязателен |
| --- | --- | --- | --- |
| программа TPU `*.tpu` | на LinQ: `/auto/cache/<login>/<имя>.tpu` (`linq.programs_dir: /auto/cache/{login}`, `config/default.yaml:191`) | воркер на LinQ, `program_uri` (`tools/linq/linq_tpu.py:60-65`) | для бэкенда `linq` |
| хвост `*_tail.onnx` | локально в репо, путь из `linq_tail`, например `models/linq/<tag>/<tag>_tail.onnx` | `LinqBackend` грузит его на LinQ в `~/work/baseline/tails/<имя файла>` перед каждым прогоном (`src/safewatch/inference/linq.py:149`) | для бэкенда `linq`: **да**, без хвоста — `model_missing` (`linq.py:141-143`) |
| полный ONNX | локально в репо, путь из `local_onnx`, например `models/<name>_640_op13.onnx` | `LocalBackend`, onnxruntime на CPU (`src/safewatch/inference/local.py:43-52`) | для бэкенда `local` |

- Пути `linq_tail` и `local_onnx` — относительно корня репо (`ROOT / path`, `linq.py:141`, `local.py:43`).
- `models/*` в git не попадает (`.gitignore:34-35`). Файлы передаются вне git: положить в `models/` на машине, где работает сервер.
- `linq_program` — **голое имя файла** в `/auto/cache/<login>/`. `LinqBackend.check` сверяет его с выводом `ls -1 /auto/cache/<login>` (`linq.py:270-281`), поэтому абсолютный путь проверку не пройдёт, хотя воркер его бы принял.
- `linq.programs_dir` используется для проверки наличия, но `program_uri` строит runtime-путь от жёсткого `/auto/cache/<login>` (`tools/linq/linq_tpu.py:36`, `:60-65`). Менять только `programs_dir` для размещения в другом каталоге нельзя.
- Имя хвоста должно быть уникальным: все хвосты ложатся в одну папку `~/work/baseline/tails/`.

### 1.2 Имена и префиксы

- Свои программы называй **`mosprom_matvey_<модель>_<размер>_<версия>_b1_o1_h1m.tpu`**, например `mosprom_matvey_fire640_v1_b1_o1_h1m.tpu`. `upload_program.py` добавляет `mosprom_`, если его ещё нет (`tools/linq/upload_program.py:27-30`). Поэтому `--name matvey_fire640_v1_b1_o1_h1m.tpu` фактически создаст `mosprom_matvey_fire640_v1_b1_o1_h1m.tpu`; именно итоговое имя нужно в `linq_program`.
- Общие существующие `mosprom_det*`, `mosprom_pose*` и другие `mosprom_*_cut_ap9999*.tpu` не перезаписывать. Общий префикс `mosprom_` не означает, что файл принадлежит Матвею. `baseline_*` и `~/work/baseline/` принадлежат приложению.
- `id` модели в реестре — `<что>-<архитектура>`, например `fire-yolov8n`. `version` — `<размер>-<тег>`, например `640-v1`. Ссылка на модель в конфиге: `id@version` (`src/safewatch/registry.py:20-26`).
- **Переобучил — подними `version`.** Ключ кэша артефактов — `sha256(jsonl-v1|video_sha256|id|version|input_size|step|backend|fake)` (`src/safewatch/inference/artifacts.py:14-21`). Веса, программа и классы в ключ не входят. Новые веса под старым `id@version` приложение не запустит: оно отдаст детекции из кэша.
- То же правило при замене хвоста, изменении порядка классов, `conf` или `iou`: они тоже не входят в ключ. Публикуй новую запись/версию и уникальные имена файлов; не подменяй уже выданный комплект (`src/safewatch/services.py:574-578`).

Пример **будущей согласованной загрузки**, не команда для автоматического запуска во время разработки документа:

```bash
python tools/linq/upload_program.py models/linq/matvey_fire640_v1/matvey_fire640_v1_b1_o1_h1m.tpu --name mosprom_matvey_fire640_v1_b1_o1_h1m.tpu
```

Не использовать `--force`. Загрузчик проверяет SHA256 конечного файла: одинаковый файл даёт `SAME`, другой под тем же именем — отказ (`upload_program.py:38-47`). Он **сначала** загружает staging-файл в `~/work/mosprom_work/programs/`, затем копирует в `/auto/cache/<login>/` (`:35-41`); существующий файл staging тоже нельзя переиспользовать под новые байты. Это исключение из обычной папки Матвея, заданное текущим загрузчиком; отдельный Matvey-only staging без изменения загрузчика не поддержан.

### 1.3 Вход, препроцессинг, выход

Препроцессинг общий для LinQ и local. Сначала вызывающий код делает BGR→RGB (`tools/linq/remote/video_worker.py:112`, `src/safewatch/inference/local.py:92`); сама `yolo_io.preprocess` принимает **уже RGB**, не меняет каналы (`tools/linq/yolo_io.py:29-45`). Далее letterbox до `input_size × input_size`, пропорции сохраняются, размер округляется через `round`, левый/верхний padding = целая половина остатка, цвет 114, `/255`, HWC→CHW, contiguous float32 `[1,3,S,S]`. Второй раз BGR→RGB делать нельзя.

| | LinQ | local |
| --- | --- | --- |
| Имя входа | `images`, жёстко: воркер берёт `--input-name` по умолчанию (`tools/linq/remote/video_worker.py:48`), бэкенд его не передаёт | любое: первый вход сессии (`local.py:66`) |
| Что на TPU | «голова» до decode: например `/model.22/dfl/conv/Conv_output_0` и `/model.22/Sigmoid_output_0` (`docs/linq/LINQ_CONTRACT.md` §3) | — |
| Decode | в хвосте на CPU: `tail.run(None, {i.name: outputs[i.name] for i in tail.get_inputs()})[0]` (`video_worker.py:85-86`). Имена входов хвоста = имена выходов программы | внутри графа (экспорт `nms=False`) |
| Выход декодера | первый выход, `[1, 4+nc(+51), A]`: `cx, cy, w, h` в пикселях входа, затем `nc` вероятностей после сигмоиды, **без objectness**; у pose ещё 17×3 точек `x, y, conf` | первый выход сессии, тот же формат (`local.py:95`) |
| NMS | `yolo_io.postprocess` (`yolo_io.py:64-106`): argmax класса, порог `ModelSpec.conf`, class-aware NMS с `ModelSpec.iou`, `max_det=300`, обратный letterbox в пиксели исходного кадра | то же |

Форма выхода проверяется явно: `4 + nc (+51)` каналов, иначе `ValueError` (`yolo_io.py:74-79`). Транспонированный `[1, A, 4+nc]` принимается. Порог записи строгий: `score > conf` (`:83`), не `>=`; NMS делается ровно один раз после хвоста. Исключение в воркере LinQ → задача `remote_error`, в local → `internal`.

Откуда берётся `nc` (это главное ограничение):

| Роль модели | `nc` на LinQ | `nc` на local | Фильтр классов |
| --- | --- | --- | --- |
| `pipeline.detector` | **80** (`video_worker.py:61`) | **80** (`local.py:67`) | `--classes` = ключи `classes` (`linq.py:166-167`) |
| `pipeline.pose` | 1, точки `(17, 3)` | 1, точки `(17, 3)` | нет |
| `pipeline.extra` | `--nc len(classes)` (`linq.py:164-165`) | `len(classes)` (`local.py:69-70`) | нет, все классы модели |

Отсюда: основной детектор обязан сохранять голову **80 классов и исходный порядок COCO**. `classes` в его записи — только подмножество нужных приложению ID, а не число выходных каналов: существующая запись из шести имён всё равно требует 80 каналов. Погрузчик размечается как `truck`, ID 7. Новые `fire`, `smoke`, `cigarette`, `no_harness`, `suspended_load` выдаются отдельными `extra`-детекторами, с ровно этими именами и полным плотным порядком ID `0..nc-1` для каждой модели. Подробнее в разделе 9.

В `extra` не помещать модель одновременно с её ссылкой в `detector`/`pose`: бэкенды определяют роль по наличию `id@version` в списке extra, а не по отдельному полю роли (`linq.py:164-167`, `local.py:67-70`). Четыре раздельных выхода существующей Matvey Split-Pose несовместимы с этим ABI: нужен хвост, возвращающий единый `[1,56,A]`. Это формат SafeWatch, не пересмотр предыдущих ML-контрактов (`video_worker.py:85-89`).

Кастомную модель компилировать так же, как базовую (`docs/linq/LINQ_CONTRACT.md` §2): `tools/linq/export_onnx.py` (opset 13, batch 1, static, `nms=False`) → `tools/linq/sdk/compile_yolo.py --cut-at <выходы dfl/conv и Sigmoid> --activation-percentile 99.99` → программа `*_b1_o1_h1m.tpu` и хвост. Имена тензоров разреза зависят от версии ultralytics и архитектуры: сверять по графу. Поддерживает ли компилятор YOLO11, неизвестно (`LINQ_CONTRACT.md` §8, вопрос 7).

## 2. Запись в `config/models.yaml`

`ModelSpec` (`src/safewatch/types.py:279`, `tech.md` 5.2):

| Поле | Тип | Что значит |
| --- | --- | --- |
| `id` | str | имя модели |
| `version` | str | версия; вместе с `id` образует ссылку `id@version` и входит в ключ кэша |
| `task` | `detect` \| `pose` | задача; `extra` — только `detect` (ключевые точки extra-моделей анализ не читает) |
| `input_size` | int | сторона квадрата letterbox: 640 или 960 |
| `conf` | float | нижний порог, с которым детекции пишутся в JSONL; пороги правил — в `class_conf` |
| `iou` | float | IoU для NMS |
| `classes` | dict[int, str] | id класса → имя, по которому его ищут правила. У `extra` — **все** классы модели подряд, `0..nc-1`: `nc = len(classes)` |
| `linq_program` | str \| null | имя программы в `/auto/cache/<login>/` |
| `linq_tail` | str \| null | локальный путь хвоста; с S29 `null` — программа с полным графом, воркер без `--tail` |
| `local_onnx` | str \| null | локальный путь полного ONNX |
| `nc` | int \| null | с S29: число классов головы детектора не из COCO-80 → `--nc <nc>`, `--classes` в пределах `0..nc-1`; `null` — 80 |
| `input_name` | str | с S29: имя входа программы, по умолчанию `images`; другое → `--input-name` |

Реальная запись (`config/models.yaml:1-11`):

```yaml
models:
  - id: det-yolov8n
    version: 640-ap9999
    task: detect
    input_size: 640
    conf: 0.1
    iou: 0.45
    classes: {0: person, 2: car, 5: bus, 6: train, 7: truck, 67: cell phone}
    linq_program: mosprom_det640_cut_ap9999_b1_o1_h1m.tpu
    linq_tail: models/linq/det640_cut_ap9999/det640_cut_ap9999_tail.onnx
    local_onnx: models/yolov8n_640_op13.onnx
```

Запись extra-модели огня (по образцу `tests/test_plugin_status.py:30-41`, этот путь покрыт тестом `test_extra_model_enables_fire_without_code`):

```yaml
  - id: fire-yolov8n
    version: 640-v1
    task: detect
    input_size: 640
    conf: 0.1
    iou: 0.45
    classes: {0: fire, 1: smoke}
    linq_program: mosprom_matvey_fire640_v1_b1_o1_h1m.tpu
    linq_tail: models/linq/matvey_fire640_v1/matvey_fire640_v1_tail.onnx
    local_onnx: models/fire-yolov8n_640_op13.onnx
```

### 2.1 Как сделать модель активной

Секция `pipeline` (`config/default.yaml:15-20`):

```yaml
pipeline:
  target_analysis_fps: 12
  min_analysis_fps: 5
  detector: det-yolov8n@640-ap9999   # обязателен, голова COCO-80
  pose: pose-yolov8n@640-ap9999      # или null: анализ без ключевых точек
  extra: []                          # список id@version дополнительных детекторов
```

- Переключать в `config/user.yaml`: он перекрывает `default.yaml` поключево (`src/safewatch/config.py:297-303`), его нет в git (`.gitignore:49`), и тесты его не читают. Образец — `config/user.example.yaml`.
- Активные модели = `detector` + `pose` + `extra` (`registry.py:29-32`). Ссылка, которой нет в `models.yaml`, останавливает старт сервера: `ValueError: model <ref> is not in config/models.yaml` (`registry.py:26`).
- Конфиг читается один раз при старте (`@cache`): после правки перезапусти сервер (`uv run safewatch stop`, затем `uv run safewatch serve`).
- Порядок переопределений: `default.yaml` → `user.example.yaml` → `user.yaml`; списки, в частности `pipeline.extra`, заменяются целиком, а не дополняются (`config.py:280-285`, `:296-304`).
- Порядок прогона в задаче: детектор → каждая extra-модель (стадия `inference_detect`) → pose (`src/safewatch/services.py:825-841`). Шаг кадров у всех один: `step = max(1, floor(fps / target_analysis_fps))` (`services.py:536-538`). Кадры extra-моделей сопоставляются с детектором по `frame_idx`. В обычной задаче только ошибки pose `remote_error`/`bad_output` допускают анализ без точек (`:839-842`); остальные ошибки не дают такого отката. В `eval` отката pose нет (`:2407-2410`).

Пример `config/user.yaml` на вечер:

```yaml
pipeline:
  detector: det-yolov8n@960-ap9999
  pose: pose-yolov8n@640-ap9999
  extra: [fire-yolov8n@640-v1, cig-yolov8n@640-v1, harness-yolov8n@640-v1, load-yolov8n@640-v1]
class_conf:
  fire: 0.4
```

Это пример после добавления **всех четырёх** extra-записей. Пока готова только запись огня выше, используй `extra: [fire-yolov8n@640-v1]`: ссылка на ещё не зарегистрированную модель остановит старт.

С S29 (`tech.md` 8.30):

- Класс extra-модели из `pipeline.vehicle_classes` (по умолчанию `[car, bus, truck, train]`) — техника с трекингом: её видят `proximity` и HUD. `proximity` активен при `person` и хотя бы одном классе из этого списка.
- Ошибка extra-модели `remote_error`, `bad_output` или `model_missing` (нет программы, хвоста или ONNX) не валит задачу: анализ идёт без неё, `error_text` задачи — `extra <id@version>: <текст>`, её сценарии в этом анализе `model_missing`.
- `Job.metrics` (`GET /api/jobs`) показывает и extra-модели.
- `local.providers` (по умолчанию `[CPUExecutionProvider]`) уходит в onnxruntime; на GPU-машине: `[CUDAExecutionProvider, CPUExecutionProvider]`.
- Детекции, посчитанные вне приложения (Vast, GPU): `uv run safewatch import-artifact FILE.jsonl --video <id> --model <id@version> [--backend linq|local] [--fake]`. Файл проверяется `read_jsonl`, строка `artifacts` получает ключ кэша этого бэкенда; следующая задача видео на нём берёт её из кэша. Коды: 2 — плохой JSONL или модели нет в реестре, 3 — нет файла или видео.

#### Модели Матвея: новая версия — новая запись

Файлы лежат вне git в `models/matvey/<id>/<version>/`. Каждая переобученная модель — новая запись `config/models.yaml` с новым `version`; в `config/user.yaml` меняется одна ссылка в `pipeline.pose` или `pipeline.extra`, кэш различает версии. Образец включения — `config/user.matvey.example.yaml`, проверка файлов — `uv run safewatch doctor`.

Промежуточная модель огня и дыма `matvey-fire-smoke-yolov8n@640-s04-v1-4c9f5d05c4d4` (пакет video-first v2, классы `{0: smoke, 1: fire}`) записана в реестр без `linq_program`: программы TPU нет, гонять её на `INFERENCE_BACKEND=local`. На `linq` задача и `safewatch eval` идут без неё (`error_text` задачи `extra ...`, у eval строка в логе); `demo build` с ней на `linq` падает целиком (пакет без полупрогонов, 8.19): уберите её из `pipeline.extra` или собирайте пакет на `local`.

Известные проблемы качества промежуточных моделей (пакет video-first v2):

- огонь путает фары с `fire` (контрольный ролик s04-headlight: ложное событие на 5,6 с); дым идёт с причиной «Открытый огонь» (семантика приложения);
- pose Матвея на сцене S07 (ur-adl-10) путает падение с лежанием на кровати;
- падение ur-fall-03 не находит ни pose Матвея, ни COCO pose (проверка R30 на `local`). Причина не в размере кадра: рост человека ~230 px при 320×240. Человек падает на 6,05 с, ролик кончается на 7,17 с, а `scenarios.fall.confirm_s = 2,0` с: даже ровное «лежит» до конца ролика не набирает удержание. Вдобавок угол торса после падения скачет: «лежит», «не ясно» (30–60°), на 6,40–6,47 с «стоит» (< 30° при рамке шире высоты в 1,8 раза), а `N` сбрасывает кандидата (8.4). При `confirm_s = 0,2` эпизод есть (6,10–6,30 с). Для демо падения нужен ролик, где человек лежит после падения не меньше 2 с;
- каска Матвея на сцене PPE_industrial4tr6 (1920×1080, R30 на `local`): центры касок на 0,09 высоты рамки человека (p50, p90 0,22), голова `head_frac = 0,35` их накрывает; но score `helmet` p50 0,22 при пороге `class_conf.helmet = 0,35` (проходят 128 из 476), поэтому у большинства людей `U head_unseen`, а не `N`. `no_helmet` выше порога — 6 кадров, эпизода нет (`hold_s = 3`).

### 2.2 640 ↔ 960

В реестре уже есть `det-yolov8n@640-ap9999` и `det-yolov8n@960-ap9999` (`config/models.yaml:2-21`). Переключение — одна строка `pipeline.detector`. `input_size` входит в ключ кэша, поэтому старые артефакты 640 не подхватятся. Цена 960 — примерно ×2,5 времени на кадр (5,3 против 12,2 запроса/с при 4 в полёте, `LINQ_CONTRACT.md` §4). Pose 960 в реестре нет.

### 2.3 Пороги по классам

`class_conf` (`config/default.yaml:22-32`) задаёт порог по имени класса, ниже которого детекция в анализ не идёт. Класса нет в `class_conf` — берётся `ModelSpec.conf` модели (`src/safewatch/analysis/pipeline.py:102`, `:110`), то есть обычно 0,1. Новые классы добавляй в `class_conf` в `config/user.yaml`. Уже заданы: `fire 0.35`, `smoke 0.3`, `cigarette 0.25`, `no_harness 0.35`, `suspended_load 0.35`, техника 0,35, `cell phone 0.3`. Для `person` порог свой — `tracker.low_thresh` (0,1).

## 3. Классы → сценарии

Как имена классов попадают в анализ (`pipeline.py:95-115`):

- **Детектор:** `person` → люди с трекингом. `car`, `bus`, `truck`, `train` (жёсткий список `VEHICLES`, `pipeline.py:26`) → техника с трекингом. Любое другое имя → нетрекаемый объект `ObjectState`.
- **Extra-модели:** **любое** имя, включая `person` и `truck`, → только `ObjectState` (`pipeline.py:107-111`). Людьми и техникой extra-классы не становятся.
- **Pose:** берутся только детекции с именем `person` (`pipeline.py:113-115`). Точки в порядке COCO-17: плечи 5 и 6, бёдра 11 и 12 (угол корпуса), лодыжки 15 и 16 (`src/safewatch/analysis/features.py:12-13`), запястья 9 и 10 (`src/safewatch/rules/base.py:30`).

Статус сценария (`src/safewatch/rules/__init__.py:45-62`): собираются имена классов всех активных моделей (`registry.py:35-39`). Нет хотя бы одного из `required_classes` → статус `model_missing`, точный текст «Нет модели с классами: <классы>» (`src/safewatch/texts.py:187`), плагин в анализе не участвует. Это заглушка «Модель не подключена» по смыслу, но не буквальная надпись. Исключение — `fire_smoking`: ему хватает одного класса из списка (`ANY_CLASS`, `rules/__init__.py:28`). Статус `active` проверяет наличие имён в конфигурации, не файлы, не точность и не то, что класс пришёл из подходящей роли модели.

| Сценарий (`id`) | Ждёт имена классов | Откуда сейчас | Что ещё нужно | Нет классов |
| --- | --- | --- | --- | --- |
| `running` | `person` (`rules/running.py:39`) | детектор COCO | зоны `danger`, `vehicle_path` — для красного; техника из детектора — для «рядом с техникой» | `model_missing` |
| `proximity` | `person`, `car`, `bus`, `truck`, `train`, **все пять** (`rules/proximity.py:66`) | детектор COCO | техника только из детектора | `model_missing` (детектор без `train` выключит сценарий) |
| `phone` | `person`, `cell phone` (`rules/phone.py:20`) | детектор COCO (id 67); объект `cell phone` из extra тоже подойдёт | привязка к руке/верху рамки: `scenarios.phone.upper_frac`, `wrist_dist_bh` | `model_missing` |
| `fall` | `person` (`rules/fall.py:20`) | детектор + необязательный pose | pose даёт суставные признаки; без pose — по рамке. Улучшение точности требует оценки | `model_missing` |
| `fence_crossing` | `person` | детектор | зона-линия `fence` | `model_missing` |
| `restricted_under` | `person` | детектор | зона `under_load` | `model_missing` |
| `fire_smoking` | `fire`, `smoke`, `cigarette`, **любой** (`rules/fire.py:54`) | **ML: extra** | огонь/дым: центр вне зон `fire_allowed` (`rules/fire.py:16`, `:19-42`); сигарета привязывается к человеку как телефон, по параметрам `scenarios.phone` (`rules/fire.py:62-63`) | `model_missing` |
| `no_harness` | `person`, `no_harness` (`rules/harness.py:20`) | person из detector, no_harness из extra | класс — **негатив** «человек без привязи». Рамка `no_harness` пересекается с рамкой человека (`ioa > 0`), и `anchor` человека в зоне `height` (`rules/harness.py:26-34`). Без зоны `height` эпизодов не будет | `model_missing` |
| `suspended_load` | `person`, `suspended_load` (`rules/suspended_load.py:19`) | **ML: extra** | `anchor` человека ниже нижнего края рамки груза и в её горизонтальных границах (`rules/suspended_load.py:25-29`) | `model_missing` |
| `load_carrying` | — | — | логики нет | `skeleton` всегда (`rules/load_carrying.py:16`) |

Имена классов для ML-части — **точно так, строчными, с подчёркиванием**:

| Что обучено | Имя в `classes` | Роль модели |
| --- | --- | --- |
| огонь | `fire` | extra |
| дым | `smoke` | extra |
| сигарета | `cigarette` | extra |
| человек без привязи | `no_harness` | extra |
| подвешенный груз | `suspended_load` | extra |
| телефон (если дообучен) | `cell phone` (с пробелом) | extra или детектор |
| погрузчик и техника | `truck` / `car` / `bus` / `train`, **только внутри COCO-80 детектора** | detector |
| каска, жилет | сценария нет; имя любое, например `no_helmet`, `no_vest` — анализ примет объект, но ни одно правило его не читает | extra |
| человек, точнее | `person`, **только внутри COCO-80 детектора** | detector |
| поза, точнее | `{0: person}`, 17 точек COCO | pose |

Погрузчик без правки кода подключается одним способом: дообучить COCO-80 детектор с сохранением всех 80 имён и размечать погрузчик как `truck` (id 7). Тогда `proximity` и `running` увидят его как технику, в тексте будет «грузовиком» (`src/safewatch/texts.py:225`). Отдельный класс `forklift` в extra-модели станет объектом, которого ни один сценарий не читает.

Подписи объектов на HUD — `texts.OBJECT_LABELS` (`texts.py:157`). Для неизвестного имени выводится само имя.

## 4. Артефакт детекций (JSONL, `FrameDetections`)

Одна строка — один обработанный кадр (каждый `step`-й). `frame_idx` строго растёт. Координаты — пиксели исходного кадра (`types.py:810-821`, `tech.md` 5.3):

Валидная строка детектора COCO (не pose):

```json
{"frame_idx":12,"ts_ms":480.0,"detections":[{"cls":0,"name":"person","score":0.91,"bbox_xyxy":[143.6,372.1,289.8,635.1],"kpts":null}]}
```

Валидная строка extra-модели огня с `classes: {0: fire, 1: smoke}`:

```json
{"frame_idx":12,"ts_ms":480.0,"detections":[{"cls":0,"name":"0","score":0.85,"bbox_xyxy":[400.0,250.0,520.0,430.0]}]}
```

Пустой обработанный кадр тоже занимает строку:

```json
{"frame_idx":13,"ts_ms":520.0,"detections":[]}
```

- `Detection`: `cls: int`, `name: str`, `score: float`, `bbox_xyxy: [x1, y1, x2, y2]`, `kpts: [[x, y, conf] × 17] | null`.
- Pose выдаёт **17 числовых троек** COCO в пикселях исходного кадра, а не строковые многоточия, нормализованные координаты или раздельные массивы. Для pose с `nc=1` воркер пишет `name: "0"`, приложение сопоставляет `cls=0` с `person`. Порядок: нос, левый/правый глаз, ухо, плечо, локоть, запястье, бедро, колено, лодыжка (`tools/linq/yolo_io.py:100-106`, `src/safewatch/analysis/features.py:12-13`, `rules/base.py:30`). HUD нормализует координаты позже; ML не делает этого в JSONL.
- `name` из JSONL приложение **не использует**: имя берётся из `ModelSpec.classes[cls]`. Для не-COCO моделей воркер пишет `"name": "<cls>"` строкой (`yolo_io.py:100`).
- Проверка (`artifacts.py:24-38`): каждая строка валидна по схеме, `frame_idx` растёт, число строк = `frames_processed` из `*.summary.json`. Иначе `bad_output`.
- Лежит в `data/app/artifacts/<cache_key>.jsonl` (+ `.summary.json`), строка в таблице `artifacts`.

**Импорта внешних детекций нет.** Ни CLI, ни API не принимают JSONL, посчитанный вне приложения (например, на GPU Vast). Артефакт создаёт только `services._infer` через бэкенд `linq` или `local` (`services.py:557-611`), и кэш находится по строке в базе, а не по файлу. Положить файл в `artifacts/` недостаточно. Для сравнения моделей вне LinQ есть два пути:

- бэкенд `local` (раздел 5) на любой машине: только CPU (`CPUExecutionProvider`, `local.py:52`);
- `tools/linq/reference_cpu.py` и `yolo_io.match_dets` — сверка рамок на картинках без приложения.

## 5. Как проверить модель без LinQ

### 5.1 Бэкенд `local` (настоящие детекции, CPU)

1. Положить полный ONNX (экспорт `nms=False`, выход `[1, 4+nc, A]`) по пути `local_onnx`.
2. Добавить запись в `config/models.yaml`, ссылку — в `pipeline.extra` (`config/user.yaml`).
3. Выбрать бэкенд: `INFERENCE_BACKEND=local` в `.env` или в окружении команды (`config.py:220`). `SAFEWATCH_FAKE` на `local` не действует.
4. Проверить, что приложение видит файл:

```bash
INFERENCE_BACKEND=local uv run safewatch doctor          # строка "ok   модель fire-yolov8n@640-v1: есть"
```

5. Прогнать видео одним из двух способов:

```bash
# а) без сервера, сразу с метриками (раздел 6)
INFERENCE_BACKEND=local uv run safewatch eval config/eval.ml.yaml
# б) через сервер и UI
INFERENCE_BACKEND=local uv run safewatch serve
uv run safewatch import data/videos/fire_01.mp4 --camera 1   # ставит задачу в очередь сервера
```

`GET /api/models` показывает активные и все модели реестра (`api.py:259`); это не список статусов сценариев. Статусы смотри на экране правил камеры. Проверка файлов — `POST /api/system/backend-check` (`api.py:254`); `ok` подтверждает наличие файлов и ответ Jupyter, но не реальный инференс или качество.

### 5.2 Режим fake (`SAFEWATCH_FAKE=1`, бэкенд `linq`)

Подменяет Jupyter синтетическими сценами по имени файла (`src/safewatch/fakes/remote.py`). Для extra-моделей fake отдаёт кадры **без детекций** (`fakes/remote.py:122-123`). Поэтому fake проверяет только проводку: запись в реестре, наличие хвоста, статус сценария `active`, что задача доходит до `done`. Качество так не проверить.

```bash
INFERENCE_BACKEND=linq SAFEWATCH_FAKE=1 uv run safewatch doctor
INFERENCE_BACKEND=linq SAFEWATCH_FAKE=1 uv run safewatch serve --seed
```

Хвост по пути `linq_tail` должен существовать и в fake: `LinqBackend.run` проверяет его до любой удалённой команды (`linq.py:141-143`).

Команды выше — Bash/Git Bash. Для Windows PowerShell эквивалент первого локального запуска:

```powershell
$env:INFERENCE_BACKEND = 'local'
$env:SAFEWATCH_FAKE = '0'
uv run safewatch doctor
uv run safewatch eval config/eval.ml.yaml --out data/app/eval/fire-v1-local
```

Для fake в этой же оболочке установи `INFERENCE_BACKEND='linq'`, `SAFEWATCH_FAKE='1'`; перед настоящим LinQ-прогоном явно верни `SAFEWATCH_FAKE='0'`. В документировании этого контракта команды, меняющие сервер, выполняющие инференс или загружающие программы, не запускались.

## 6. Как оценить качество: `safewatch eval`

Файл разметки (`config/eval.example.yaml`, схема `EvalLabels`, `types.py:935-950`). Пути видео — от корня репо:

```yaml
deadline_s: 5                 # необязательно, иначе eval.deadline_s (5.0)
videos:
  - path: data/videos/fire_01.mp4
    camera_id: 3              # необязательно: калибровка, зоны и правила этой камеры
    expected:
      - {scenario: fire_smoking, start_s: 12.0, end_s: 30.0}
      - {scenario: no_harness, start_s: 41.5, end_s: 55.0}
```

`scenario` — `id` из таблицы раздела 3. Без `camera_id` нет зон: `no_harness` и `restricted_under` эпизодов не дадут, огонь будет «вне разрешённой зоны» всегда. Для них укажи камеру с нарисованными зонами.

```bash
uv run safewatch eval config/eval.ml.yaml --out data/app/eval/fire-v1
```

- Инференс идёт через выбранный бэкенд с тем же кэшем артефактов, затем анализ (`services.py:2460-2495`). Запускать при остановленном сервере: оба процесса пишут в одну базу.
- Совпадение: тот же сценарий, `start_s ≤ confirm_s < end_s`, задержка `confirm_s − start_s ≤ deadline_s`. Сопоставление жадное по задержке. Лишние эпизоды того же эталона — `duplicates`, позже дедлайна — `late`, прочие — FP (`src/safewatch/evaluate.py:17-49`).
- Вывод: путь папки и таблица `report.md` по сценариям и итог `*`: `expected, episodes, tp, fn, fp, duplicates, late, precision, recall, f1, fp_per_hour, delay p50/p95, n`. Файлы: `data/app/eval/<YYYYMMDD-HHMMSS>/report.json` (`EvalReport`) и `report.md`. Recall честный только при полной разметке видео.
- Без `--out` выбирается timestamp-папка; с указанным выше `--out` файлы будут в `data/app/eval/fire-v1/`. `precision = TP/(TP+FP)`, `recall = TP/(TP+FN)`, `fp_per_hour = FP/часы всех видео`; **duplicates и late не входят в FP и знаменатель precision**, хотя выводятся отдельно (`services.py:2428-2455`). Сопоставление не учитывает личность человека/track ID. Это качество эпизодов по текущему scorer, не mAP детектора, actor-level recall или задержка доставки уведомления.
- Коды выхода (`src/safewatch/cli.py:131-145`): `0` — готово; `2` — ошибка разметки или видео не читается; `3` — нет файла или камеры; `4` — `InferenceError` любой модели, включая pose и extra.

Сравнение двух версий модели: два прогона `eval`, между ними меняется `pipeline.extra` в `config/user.yaml`, у версий разные `version`.

## 7. Правила работы на LinQ для ML-части

Из `tech.md` 3.1 и `CLAUDE.md`:

- Аккаунт Jupyter один на команду. Обычная папка ML-части — `~/work/matvey/`, свои скрипты и артефакты — с префиксом `matvey_`. Для **TPU-программ через существующий загрузчик** действует исключение из раздела 1.2: уникальные `mosprom_matvey_*`, staging `~/work/mosprom_work/programs/`, итог `/auto/cache/<login>/`. Имя `matvey_*` без `mosprom_` не сохранится в таком виде. Папка приложения — `~/work/baseline/`, файлы `baseline_*`: не трогать, приложение само туда грузит хвосты и видео.
- Общие программы `mosprom_*_cut_ap9999*.tpu` не перезаписывать и не удалять; готовый проверенный baseline допустимо использовать без изменения. Новые байты — только новое уникальное имя `mosprom_matvey_*`, без `--force` (`upload_program.py:29-47`).
- Квота CPU контейнера — 1,5 на всех. В любом своём скрипте: `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `cv2.setNumThreads(1)`, onnxruntime `intra_op_num_threads = inter_op_num_threads = 1` (как `video_worker.py:22-28`, `:55-58`). Код воркера использует `setdefault`, поэтому уже заданные большие лимиты нужно исправить в **своём** процессе, не менять окружение чужих процессов.
- Приложение имеет `linq.inflight: 4` (`config/default.yaml:192`), CLI воркера по умолчанию 8 (`video_worker.py:44`). Это не разрешение на параллельный ML-прогон: Матвей согласует слот с капитаном, не запускает одновременно с приложением и ограничивает собственную диагностику одним запросом в полёте (`--inflight 1`). Общие VPN/SSH/маршруты и службы не перенастраивать, чужие ядра не останавливать.
- Брокер RabbitMQ общий для 37 команд: чужие очереди и программы не читать и не трогать.
- Компилировать и обучать на ноутбуке капитана нельзя. Компиляции — строго по одной (две параллельно уже вызвали OOM).
- Секреты только в `.env` (`LINQ_*`): не печатать и не коммитить.

## 8. Что ML-части НЕ надо делать

- Менять код приложения (`src/`, `tools/linq/remote/video_worker.py`, `tools/linq/yolo_io.py`): воркер и постпроцессинг общие для LinQ и local.
- Менять контракт фронта `contract/openapi.json`, схему БД (`src/safewatch/migrations/`) и `tech.md`.
- Переименовывать или удалять существующие записи `config/models.yaml`: на `det-yolov8n@640-ap9999` и `pose-yolov8n@640-ap9999` ссылаются `config/default.yaml` и тесты. В реестр — только добавлять.
- Переключать `pipeline` в `config/default.yaml`: для этого есть `config/user.yaml`.
- Коммитить веса и программы: `models/*` в git не идёт.

### 8.1 Комплект, который передать Марку

1. Новый `id@version`, роль (`detector`, `pose` или `extra`), точные `classes`, размер, `conf`/`iou` и готовая **добавляемая** запись реестра со всеми десятью полями `ModelSpec` (`types.py:279-290`).
2. Полный ONNX для local и локальный хвост с уникальным basename; TPU-программа уже под уникальным итоговым именем на LinQ. Передать фактические пути, версии экспортёра/SDK и SHA256 трёх файлов вне записи `ModelSpec`: полей для хешей в ней нет.
3. Отдельно сообщить вход `images`, формы/имена выходов TPU и входов хвоста, число классов; приложить результаты проверки полного ONNX против head+tail на одинаковом RGB-входе. Для pose — 17 COCO-точек и единый выход хвоста `[1,56,A]`.
4. Передать конфигурационный diff для `config/user.yaml`, видео/разметку с разрешённым использованием и отчёт `eval` с составом выборки. Новые файлы под старыми именами и одной старой `version` не передавать.
5. Марк добавляет записи, кладёт локальные файлы, переключает конфиг и перезапускает приложение. `doctor`/проверка наличия → local-eval → отдельно согласованный LinQ-прогон. Компиляция, симуляция, наличие файлов и настоящий TPU-ответ — разные проверки; ни одна не устанавливает промышленное качество сама по себе.

## 9. Пробелы: чего не хватает для гладкой интеграции

Список с предложениями ML-части; решение по каждому пункту — `tech.md` 8.30, строка «Итог» под пунктом.

1. **Нет импорта внешних артефактов.** Детекции с GPU Vast в приложение не попасть. Предложение: `safewatch import-artifact <video> <id@version> <file.jsonl>`. Команда проверяет файл через `read_jsonl` и пишет строку `artifacts` с тем же `cache_key`.
   Итог: S29: CLI `safewatch import-artifact FILE --video ID --model REF [--backend linq|local] [--fake]` поверх `artifact_import`; провенанс — `--backend` и `--fake` (раздел 2.1).
2. **Основной детектор жёстко COCO-80.** `nc = 80` в `video_worker.py:61` и `local.py:67`, свой `nc` есть только у `extra`. Предложение: брать `--nc len(classes)` у любого детектора, ключи которого не из COCO, или ввести поле `nc` в `ModelSpec` (через `CONTRACT GAP`).
   Итог: S29: поле `ModelSpec.nc`; детектор с `nc` получает `--nc <nc>`, `--classes` в пределах `0..nc-1`; без `nc` — как раньше (80).
3. **Техника и люди — только из детектора, имена техники зашиты.** `VEHICLES = ("car", "bus", "truck", "train")` (`pipeline.py:26`), extra-классы → только `ObjectState` (`pipeline.py:107-111`). Погрузчик из extra-модели не видят ни `proximity`, ни `running`. Предложение: ключ конфига `vehicle_classes` и трекинг extra-классов из этого списка.
   Итог: S29: ключ `pipeline.vehicle_classes`; класс из списка у extra-модели — техника с трекингом.
4. **`proximity` требует все пять имён** (`rules/proximity.py:66`). Детектор без `train` или с одним «погрузчиком» выключит сценарий. Предложение: добавить `proximity` в `ANY_CLASS` для классов техники при обязательном `person`.
   Итог: S29: `proximity` активен при `person` и хотя бы одном классе из `pipeline.vehicle_classes`.
5. **Нет сценария СИЗ (каска, жилет).** Классы примутся, но правило их не читает. Предложение: плагин `no_ppe` по образцу `no_harness` с негативными классами `no_helmet` и `no_vest`.
   Итог: S20: плагины `no_helmet` и `no_respirator` (`tech.md` 8.22).
6. **`no_harness` ждёт негативный класс.** Позитивный `harness` («привязь есть») этот сценарий не читает. Предложение: обучать наблюдаемый `no_harness` либо отдельно спроектировать оценку покрытия/видимости с `unknown`. Простое отсутствие bbox `harness` не доказывает отсутствие привязи; текущий плагин этого вывода не делает (`rules/harness.py:26-34`).
   Итог: оставлено осознанно: отсутствие рамки привязи не доказывает её отсутствие; ML-часть обучает `no_harness`.
7. **Хвост обязателен.** Программа с полным графом без хвоста → `model_missing` (`linq.py:141-143`). Предложение: `linq_tail: null` означает запуск воркера без `--tail`.
   Итог: S29: `linq_tail: null` → воркер без `--tail`, проверка хвоста пропускается.
8. **Имя входа программы жёстко `images`.** Бэкенд не передаёт `--input-name`. Предложение: необязательное поле в реестре.
   Итог: S29: поле `ModelSpec.input_name` → `--input-name` (по умолчанию аргумента нет, воркер берёт `images`).
9. **Кэш не знает о весах.** В ключе нет хэша программы, хвоста и классов (`artifacts.py:14-21`). Сейчас правило «переобучил — подними `version`». Предложение: добавить в ключ sha256 файлов модели.
   Итог: оставлено: смена `CACHE_SCHEMA` обнулит кэш демо-пакета и истории; правило «переобучил — подними `version`» в силе.
10. **Падение extra-модели валит всю задачу.** У pose есть откат на анализ без точек (`services.py:832-842`), у extra нет (`services.py:828-831`). Предложение: такой же откат, сценарий модели на этот анализ — `model_missing`.
   Итог: S29: `remote_error`/`bad_output` extra-модели → анализ без неё, `error_text = "extra <ref>: <текст>"`, её классы не входят в `active_classes` снимка (сценарии — `model_missing` в этом анализе); тем же путём `model_missing` (строка `GAP` S29).
11. **Метрики extra-моделей не видны.** `Job.metrics` — только детектор и pose (`tech.md` 6.9, S10). Предложение: показывать extra в `/api/jobs` (добавление в openapi).
   Итог: S29: `Job.metrics` включает extra-модели (по `AnalysisConfig.extra_artifact_ids` анализа задачи).
12. **`upload_program.py` навязывает префикс `mosprom_` и папку `mosprom_work`** (`upload_program.py:29-35`). Текущий совместимый путь — уникальные `mosprom_matvey_*` (раздел 1.2). Предложение: настраиваемые prefix/staging-dir и отказ до staging-upload при занятом имени; до этого не обещать изолированную загрузку только в `matvey/`.
   Итог: оставлено: инструмент ML-части и общая инфраструктура LinQ, прогон его не меняет (`tech.md` 3.1).
13. **Fake не умеет extra-классы:** пустые кадры (`fakes/remote.py:122-123`), сценарии огня, привязи и груза на демо без LinQ не показать. Предложение: сцены fake с классами по имени из `ModelSpec.classes`.
   Итог: оставлено: демо огня и груза — через демо-пакет с настоящими детекциями (`tech.md` 8.19).
14. **`local` только на CPU** (`local.py:52`). На GPU Vast медленно. Предложение: ключ `local.providers` (`CUDAExecutionProvider`).
   Итог: S29: ключ `local.providers` уходит в onnxruntime.
15. **Pose зашит на 1 класс и 17 точек COCO** (`video_worker.py:61`, `local.py:67`). Другая схема точек не подключится.
   Итог: оставлено: других схем точек нет.
16. **Файлы моделей передаются вне git** без проверки целостности. Предложение: манифест `models/MANIFEST.yaml` с sha256, `doctor` сверяет.
   Итог: оставлено: манифест — у ML-части (`MATVEY_MANIFEST.json`); `doctor` проверяет наличие файлов.
17. **`active` не проверяет роль источника класса.** Имена из extra/pose могут включить сценарий, хотя людей и технику анализ берёт из detector (`rules/__init__.py:45-62`, `analysis/pipeline.py:95-115`). Предложение: проверять требуемые роли и tensor ABI при регистрации модели; плотность extra ID и task сейчас тоже не гарантируются схемой `ModelSpec`.
   Итог: оставлено частично: с S29 техника из extra трекается (п. 3); людей даёт только детектор.
18. **Ограничения scorer.** Текущий eval не сопоставляет actor ID, а `duplicates`/`late` исключены из precision и FP/час (`evaluate.py:17-49`, `services.py:2428-2455`). Предложение: отдельные actor-aware метрики, нагрузка всеми уведомлениями и строгая проверка полноты GT; текущие цифры всегда сопровождать этими ограничениями.
   Итог: оставлено: метрики ML-части; отчёт сохраняет сноску о полноте разметки.
19. **Калибровка compile-helper привязана к COCO128/person.** `tools/linq/sdk/compile_yolo.py:37-48`, `:131-138` выбирает картинки из `data/coco128`, а CLI не принимает manifest калибровки. Команда компиляции из контракта доказывает маршрут, но не достаточность такой калибровки для огня/сигареты/груза. Предложение: отдельно согласовать вход calibration-manifest в подготовительном ML-инструменте; до этого передавать происхождение фактических calibration-групп и не заявлять их пригодность автоматически.
   Итог: оставлено: инструмент компиляции ML-части, на ноутбуке капитана компиляция запрещена (`tech.md` 3.1).
