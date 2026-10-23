# LinQ smoke test — статус

Обновлено: 2026-10-24, после этапа 2.

## Сделано

- **Этап 0.** Папки `data/videos/`, `vendor/linq/`, `models/`, `results/linq_smoke/` с README; `.gitignore` (vendor, модели, видео, raw); `.env.example`; `docs/ENVIRONMENT.md`. Скрипты туннеля перенесены в `tools/linq/tunnel/`, добавлен проброс RabbitMQ.
- **Этап 1 (частично).**
  - `tools/linq/jupyter_remote.py`: логин в JupyterHub (`_xsrf` хаба и сервера раздельно), `exec`/`py` через kernel websocket, `upload` чанками, `download`, `ls`. Проверен.
  - Разведка удалённой машины — `docs/ENVIRONMENT.md`.
  - **API TPU = RabbitMQ** `10.0.114.30:5672` (`guest/guest`), exchange `tpu.direct`, очередь `input`, формат `tpu_pycloud_format` (protobuf). 16 консьюмеров на `input`.
  - **API доступен с нашей машины** через туннель (`127.0.0.1:5672`). Jupyter нужен только для загрузки `.tpu` в `/auto/cache/<login>/`.
  - `tools/linq/linq_tpu.py`: клиент TPU (sync `infer`, конвейер `submit/collect`), работает и в Jupyter, и локально.
- **Этап 2.** Пример вендора resnet50: класс 257 — верно.
  - В Jupyter: полный цикл медиана 29 мс, p90 246 мс (n=20); 32 запроса в полёте — 78 req/s, ответы от 3 воркеров (pid 6/7/8).
  - Локально через туннель: 300–600 мс на запрос (тензор 600 КБ туда-обратно через ssh + VPN Матвея).

## Найдено

- В `/auto/cache/hackathon70007/` уже лежат `helmet-v1.tpu`, `pose-split-v1.tpu` (загружены 23.10 21:23 не нами — конвейер команды на Vast/у Матвея). Не трогаю.
- `examples/Untitled.ipynb` содержит загрузчик, который берёт код из очереди RabbitMQ и исполняет его. Брокер общий, `guest/guest` — это риск; не трогаю, сообщить владельцу.
- Поле `worker.inference_time` ненадёжно как метрика (медиана 70 «мс» при полном цикле 29 мс) — время мерить на клиенте.

## Блокеры

- **SDK (`tpu_framework`) не скачан:** `cloud.lin-q.ru` недоступен ни с нашей машины (Happ → TLS обрыв), ни из Jupyter (таймаут). Нужно: `curl.exe` в «напрямую» Happ, либо Матвей кладёт архивы в Jupyter `mosprom_work/vendor/`.

## Следующий шаг

Экспорт YOLO11n/YOLOv8n в ONNX (CPU, ultralytics 8.3.230) и эталон onnxruntime; как только будет SDK — квантование и компиляция в WSL2 Ubuntu.
