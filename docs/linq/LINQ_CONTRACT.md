# LinQ TPU — проверенный контракт (smoke test 2026-10-24)

Всё ниже проверено руками на сервисе. Где оценка — помечено «≈». Код — `tools/linq/` (README там же), сырые цифры — `results/linq_smoke/`.

## 1. Окружение

| | Локально (компиляция) | Удалённо (LinQ) |
|---|---|---|
| Где | WSL2 Ubuntu 24.04 на ноутбуке, `~/linq_sdk/venv` | JupyterHub `hackathon.lin-q.ru` (контейнер Ubuntu 22.04), пользователь = логин Jupyter |
| Python | **3.12.11** (требование SDK, колёса только `cp312-linux_x86_64`) | 3.11.6 conda; numpy 1.24.4, pika 1.4.4, protobuf 4.24.3, `tpu_pycloud_format` 0.0.1; ставим `--user`: `opencv-python-headless==4.10.0.84`, `onnxruntime==1.19.2` |
| SDK | `tpu_framework_bin 2026.9.45`, `tpu_compiler_bin 2026.9.493`, `dnn_quant_bin 2026.9.98`, `onnx_direct_bin 2026.8.23`, torch 2.9.1, onnx 1.16.2, onnxruntime 1.29.0 (pins из `requirements.txt` вендора) | SDK нет и не нужен |
| Ресурсы | компиляция 640: пик ≈2.5 ГБ RAM; 960 — больше (две параллельные компиляции на 16 ГБ ноутбуке убил OOM) | 64 видимых CPU, **но cgroup-квота 1.5 CPU** (`cpu.max 150000 100000`), 187 ГБ RAM, 1.7 ТБ диск, ffmpeg есть, интернет (PyPI/GitHub) есть |
| Сеть | — | Jupyter: `:80` (443 закрыт). TPU API: RabbitMQ `10.0.114.30:5672`, management `:15672`, `guest/guest` |

Экспорт ONNX — в отдельном env (Windows `.venv`): ultralytics 8.3.230, torch 2.5.1+cpu, **onnx 1.17.0** (ultralytics сам пытается переставить onnx и ломает его — пиннить).

Доступ с ноутбука: только ssh-туннель через машину с OpenVPN (`tools/linq/tunnel/`): `127.0.0.1:8888` Jupyter, `:5672`/`:15672` RabbitMQ, `:9443` cloud.lin-q.ru (SDK).

## 2. Конвейер ONNX → программа TPU

```
yolov8n.pt --export_onnx.py--> yolov8n_640_op13.onnx (+ .json контракт)
  --compile_yolo.py (WSL)-->  [cut] head.onnx + tail.onnx
                              preliminary_model_conditioning   (внутри поднимает opset 13 -> 17)
                              RegularModel(model).calibrate_torch({images: N×3×640×640 float32}, device="cpu", activation_percentile=99.99)
                              quantize(thresholds) -> .qm.onnx (+ scales.json, thresholds.json)
                              [проверка] as_torch_graph(batch_size=1, cache_word_length=128) + rescale(Input/Output) — fake-quant на CPU
                              Network.from_quantized_model(qm); set_batch(1)
                              compiler.compile_(TPU_H1M, network, O1) -> TpuProgram.from_executable(...).to_file(*_b1_o1_h1m.tpu)
  --upload_program.py-->      /auto/cache/<login>/mosprom_*.tpu   (Contents API в ~/work, затем cp; sha256 сверяется)
```

Точные команды:

```powershell
.venv\Scripts\python.exe tools\linq\export_onnx.py --model yolov8n.pt --imgsz 640          # opset 13, batch 1, static, fp32, nms=False, simplify
wsl -d Ubuntu -- bash -c "cd /mnt/d/msk-prom2026-mark && ~/linq_sdk/venv/bin/python tools/linq/sdk/compile_yolo.py models/yolov8n_640_op13.onnx --preset O1 --cut-at /model.22/dfl/conv/Conv_output_0,/model.22/Sigmoid_output_0 --activation-percentile 99.99 --tag det640_cut_ap9999"
.venv\Scripts\python.exe tools\linq\upload_program.py models\linq\det640_cut_ap9999\det640_cut_ap9999_b1_o1_h1m.tpu
```

Pose: тот же вызов на `yolov8n-pose_640_op13.onnx` с `--cut-at /model.22/dfl/conv/Conv_output_0,/model.22/Sigmoid_output_0,/model.22/Concat_output_0`.

Время (ноутбук i5-13420H, WSL 7.8 ГБ): conditioning ≈1 с; калибровка 150 кадров 640 — 17 с по умолчанию, **190 с с `activation_percentile`**; quantize 3 с; компиляция O1: 28–35 с (640), 61 с (pose полный граф), 63 с (960). Программа ≈2.8–2.9 МБ. Пресеты: `O1` (безопасный, используем), `O3`, `O5` (может дать невалидную программу; не пробовали).

**Калибровка:** реальные кадры с людьми (coco128: 50 фото × {оригинал, h-flip, центр-кроп 0.8} = 150 кадров; для 960 — 34 × 3 = 102 из-за памяти), тот же letterbox-препроцессинг. Отложенная выборка для оценки — 8 других фото с людьми + 4 без людей + пустой серый кадр. Запрошенные и фактически принятые параметры пишутся в `*.report.json` (проверка по сигнатуре `calibrate_torch`, без try/except-ретраев); то, что параметр реально применён, видно по разным результатам fake-quant.

## 3. API инференса

Транспорт — **RabbitMQ** (не HTTP). Клиент — `tools/linq/linq_tpu.py` (`TpuClient.infer` / `submit`+`collect`), работает и в Jupyter, и с ноутбука через туннель.

| | |
|---|---|
| Брокер | `10.0.114.30:5672`, vhost `/`, `guest/guest` (из примера вендора; общий для всех команд) |
| Запрос | `basic_publish(exchange="tpu.direct", routing_key="input", body=serialize(PyTask({name: ndarray})))` |
| Заголовки | `uri = "file:///auto/cache/<login>/<prog>.tpu?raw=False"`; `response_routing_keys = '["<наша очередь>"]'` (JSON-список); `tpu_pycloud_message_id = <id>` (возвращается как есть) |
| Ответ | в нашу очередь (declare + bind к `tpu.direct` с routing key = имя очереди); `deserialize(body) -> (outputs: {name: ndarray}, metadata, worker)`; `worker.status_code == 0` — успех, иначе `error_message` (пример: `-3 … TPU program file is not readable …`) |
| Авторизация | нет; «своя» программа = путь в `/auto/cache/<login>/` (воркер видит каталоги всех 37 команд) |
| Режим | асинхронный; можно держать N запросов в полёте, ответы сопоставлять по message id |
| Воркеры | 16 консьюмеров на `input`; ответы приходят от pid 6/7/8 (хост `cloud02`) |
| Батч | программа компилируется под фиксированный batch (`_b1_`); батч >1 = отдельная программа (не проверяли) |

**Тензоры на границе программы (raw=False):** float32, layout и имена — как у ONNX-«головы»; масштабы/zero-point применяет сам рантайм, клиенту ничего делать не надо.

| Программа | Вход | Выходы |
|---|---|---|
| детектор, полный граф | `images` f32 [1,3,640,640] | `output0` f32 [1,84,8400] |
| детектор, разрез (рекомендуем) | `images` f32 [1,3,640,640] | `/model.22/dfl/conv/Conv_output_0` f32 [1,1,4,8400] (ltrb-расстояния после DFL), `/model.22/Sigmoid_output_0` f32 [1,80,8400] (вероятности классов) |
| pose, разрез | `images` f32 [1,3,640,640] | `…/dfl/conv/Conv_output_0` [1,1,4,8400], `…/Sigmoid_output_0` [1,1,8400], `/model.22/Concat_output_0` [1,51,8400] (сырые kpt до decode) |
| 960 — так же, A = 18900 | `images` [1,3,960,960] | |

**Препроцессинг** (`yolo_io.preprocess`): BGR→RGB, letterbox до S×S с сохранением пропорций, паддинг 114 по центру, `/255`, HWC→CHW, float32. **Постпроцессинг:** для разреза — `*_tail.onnx` (Sub/Add/Div/Mul/Concat/Slice/Reshape, 170 КБ) в onnxruntime на CPU → `[1, 4+nc(+51), A]`; дальше `yolo_io.postprocess`: формат **4+nc без objectness** (не 5+nc), argmax класса, conf 0.25, class-aware NMS IoU 0.45, обратный letterbox. Карта классов — COCO-80 (`person`=0, `car`=2, `bus`=5, `truck`=7, `cell phone`=67).

## 4. Что работает

Сверка «TPU vs CPU FP32 onnxruntime с тем же пре/постпроцессингом» на 13 отложенных кадрах (recall/precision — доля совпавших рамок того же класса при IoU≥0.5).

| Что | Статус | recall | prec. | IoU | Δscore | Время (в Jupyter) |
|---|---|---|---|---|---|---|
| resnet50 вендора | ✅ класс 257 верный | — | — | — | — | 18 мс/запрос; 78 req/s при 32 в полёте |
| детектор 640, полный граф, O1 | ✅ | 0.86 | 0.90 | 0.86 | 0.080 | — |
| детектор 640, разрез, O1 | ✅ | 0.86 | 0.92 | 0.92 | 0.079 | — |
| **детектор 640, разрез, act-pct 99.99, O1** | ✅ **рекомендуем** | **0.91** | 0.90 | **0.93** | 0.053 | 162 мс одиночный, 12.2 req/s при 4 в полёте |
| детектор 960, разрез, act-pct 99.99 | ✅ | 0.93 | 0.96 | 0.94 | 0.069 | 411 мс одиночный, 5.3 req/s при 4 в полёте |
| pose 640, полный граф | ✅ | 0.99 | 0.99 | 0.87 | 0.027 | kpt-ошибка 2.0 % диагонали рамки |
| **pose 640, разрез, act-pct 99.99** | ✅ | 0.94 | 0.94 | 0.94 | 0.018 | kpt 1.4 %; 141 мс одиночный |
| видео → LinQ → JSONL (детектор 640) | ✅ | 0.96* | 0.99* | 0.91* | 0.042* | **21 кадр/с**, 400 кадров 1280×720 за 19 с; весь путь с загрузкой 31 с |
| видео pose (каждый 2-й кадр) | ✅ | — | — | — | — | 19.6 кадра/с; 200 кадров, весь путь 22 с |
| несколько устройств | ⚠️ частично | | | | | 1→4 в полёте: 6→12 req/s, ответы от 2–3 разных воркеров; число чипов неизвестно |

\* видео: 40 кадров (каждый 10-й) против CPU на тех же кадрах, классы person/car/bus/truck/cell phone.

**Время на кадр.** Полный цикл одного запроса из Jupyter для 640 = 162 мс, из них почти всё — пересылка: RTT растёт ≈19 мс на МБ (вход+выход): resnet 0.6 МБ → 18 мс, det640 7.7 МБ → 162 мс, det960 17.5 МБ → 411 мс. ≈ Чистый TPU для 640 — порядка 10–20 мс (вендор заявляет 21.5 мс для yolov8n_pose). Поле ответа `worker.inference_time` не годится как метрика (≈50 мс для любой модели; часы воркера сдвинуты на секунды). Пре/постпроцессинг в Jupyter — 4 + 3 мс на кадр (после фикса потоков).
С ноутбука через туннель тот же запрос 640 — ≈3.7 с (тензор идёт через ssh + чужой VPN) — для видео не годится.

## 5. Точность и потеря от квантования

- int8-квантование YOLOv8n даёт ощутимую потерю относительно FP32: лучший вариант 640 — recall 0.91, IoU 0.93, средняя разница скоров 0.05; потери — в основном объекты со скором у порога 0.25 (маленькие/частично видимые люди в толпе: на 000000000564.jpg 28 CPU-рамок против ~15 TPU).
- **Fake-quant на CPU (SDK `as_torch_graph` + `rescale`) совпадает с TPU практически точно** (recall 0.856 = 0.856, 0.907 = 0.907, 0.9375 = 0.9375). Подбирать квантование можно офлайн, без TPU.
- Что помогло: разрез перед decode (IoU 0.85 → 0.92), `activation_percentile=99.99` (recall 0.86 → 0.91). Хуже: 99.9, 99.999, `samplewise_percentile=99`.
- 960 даёт лучшие рамки (IoU 0.94) — важно для мелких объектов, — ценой ×2.5 времени.

## 6. Рекомендация для адаптера `linq` в baseline

1. **Обработка видео — внутри Jupyter**, схема «загрузка файла → удалённый скрипт → опрос → JSONL»: `tools/linq/run_video.py` + `remote/video_worker.py`. Это соответствует «не стримить», а пересылка тензоров до TPU идёт внутри площадки (162 мс против 3.7 с с ноутбука). 21 кадр/с — с большим запасом против «хоть 1 FPS».
2. Прямой вызов API с бэкенда (через туннель) — только для отладки/одиночных кадров.
3. Постоянный воркер в Jupyter — следующий шаг, если нужны частые короткие ролики (сейчас накладные расходы на запуск воркера и опрос — ≈2.5 с на ролик). Не проверяли, переживает ли detached-процесс рестарт пользовательского сервера Jupyter.
4. Данность для baseline: программы `mosprom_det640_cut_ap9999_b1_o1_h1m.tpu`, `mosprom_pose640_cut_ap9999_b1_o1_h1m.tpu`, `mosprom_det960_cut_ap9999_b1_o1_h1m.tpu` лежат в `/auto/cache/hackathon70007/`; хвосты `*_tail.onnx` загружаются рядом с воркером (`mosprom_work/tails/`); формат JSONL: `{frame_idx, ts_ms, detections:[{cls, name, score, bbox_xyxy[, kpts:[[x,y,conf]×17]]}]}`.
5. В воркере обязательно `OMP_NUM_THREADS=1`, `cv2.setNumThreads(1)`, onnxruntime intra/inter = 1, 4 запроса в полёте.

## 7. Ловушки (проверено)

| Ловушка | Факт |
|---|---|
| Квота CPU контейнера 1.5 при 64 видимых ядрах | дефолтные пулы потоков → 0.59 кадра/с вместо 19.5. Ограничивать потоки. |
| Полный граф YOLO квантуется плохо | в `output0` склеены координаты 0..640 и вероятности 0..1 → общий int8-масштаб. Резать перед decode (так делает и вендор для `yolov8n_pose`). |
| `compile.py` вендора калибрует на `np.random.rand` | заменить реальными кадрами. |
| 4+nc vs 5+nc | v8: `[1, 4+nc, A]`, objectness нет; pose `[1, 4+1+51, A]`. Проверять форму явно, не угадывать транспонирование (у нас `ValueError`). Для nc=1 (pose) работает. |
| DFL/decode внутри графа | при `nms=False` — да; на TPU лучше оставить только до `dfl/conv`, decode — в tail ONNX. Имена тензоров зависят от версии ultralytics (у вендора `Mul_6/Concat_7`, у нас 8.3.230 — другие) — сверять по графу. |
| Версии | SDK: Python 3.12.11, torch 2.9.1, onnx 1.16.2, ort 1.29; экспорт: ultralytics 8.3.230 + onnx 1.17 в отдельном env; ultralytics авто-переустанавливает onnx и ломает его. SDK сам поднимает opset 13 → 17. |
| Тихий откат параметров квантования | в SDK 2026.9 не обнаружен: `calibrate_torch` принимает `activation_percentile`/`samplewise_percentile`, результат меняется. Наш скрипт отказывается запускаться при непринятом параметре. |
| `get_sub_model` | хвост тащит все веса модели (12.7 МБ вместо 170 КБ) — чистить неиспользуемые initializers. |
| `/auto/cache//…` | пустой логин в URI → `status=-3 ENOENT`. |
| Параллельные компиляции | 2 одновременно + 960 → OOM на 16 ГБ ноутбуке. По одной. |
| Туннель | зависит от OpenVPN на чужом ноутбуке; при обрыве ssh жив, а пробросы дают `Connection timed out`. |

## 8. Вопросы организаторам

1. Как получить честное время TPU на запрос? `inference_time` в ответе ≈50 мс для любой модели — что оно значит?
2. Можно ли компилировать программу с входом uint8 (вход 640 сейчас 4.9 МБ float32; пересылка — основная часть задержки)?
3. Сколько физических TPU за 16 консьюмерами очереди `input`, есть ли квоты на команду, батч >1 поддерживается сервисом?
4. Брокер общий с `guest/guest`, воркер читает `/auto/cache` всех команд — это ожидаемо? Нужно ли изолировать очереди/программы?
5. Второй VPN-логин на команду (один логин = одна сессия, второй участник не может подключиться).
6. Квота CPU контейнера Jupyter 1.5 — можно ли больше для пре/постпроцессинга видео?
7. Поддерживает ли компилятор YOLO11 (C2PSA/attention) и полный граф pose с decode — или разрез обязателен?
