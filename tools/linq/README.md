# tools/linq — работа с LinQ TPU

Контракт и факты — `docs/linq/LINQ_CONTRACT.md`. Окружение — `docs/ENVIRONMENT.md`.

## Схема

```
ноутбук (Windows)                                       LinQ (10.0.114.0/24, через ssh-туннель к Матвею)
 .venv: export_onnx / reference_cpu / run_*             JupyterHub  127.0.0.1:8888  -> ~/work (наша папка mosprom_work/)
 WSL Ubuntu: ~/linq_sdk/venv (SDK, Python 3.12.11)      RabbitMQ    127.0.0.1:5672  -> TPU workers (exchange tpu.direct, queue input)
                                                        программы   /auto/cache/<login>/*.tpu
```

## Файлы

| Файл | Где запускать | Что делает |
|---|---|---|
| `tunnel/Connect-LinQ.cmd` | Windows | поднять туннель (Jupyter, RabbitMQ, Nextcloud) |
| `jupyter_remote.py` | Windows | `info / exec / py / pyfile / upload / download / ls` в LinQ Jupyter |
| `linq_tpu.py` | везде | клиент API TPU (`TpuClient.infer`, `submit/collect`), `ping`, `run` |
| `export_onnx.py` | Windows .venv | `.pt` → статический ONNX (opset 13, nms=False) + `.json` с контрактом |
| `reference_cpu.py` | Windows .venv | эталон onnxruntime FP32 с тем же пре/постпроцессингом |
| `yolo_io.py` | везде | letterbox-препроцессинг, decode/NMS, сверка рамок (`match_dets`) |
| `sdk/setup_sdk_wsl.sh` | WSL | поставить SDK `tpu_framework 2026.9.45` в `~/linq_sdk/venv` |
| `sdk/compile_yolo.py` | WSL venv | ONNX → (разрез) → калибровка → `.qm` → fake-quant проверка → `.tpu` |
| `upload_program.py` | Windows | `.tpu` → `/auto/cache/<login>/mosprom_*.tpu` (sha256-проверка, без перезаписи чужого) |
| `run_images.py` | Windows | картинки → TPU → детекции + сверка с CPU, время |
| `run_video.py` (+ `remote/video_worker.py`) | Windows | видео → загрузка в Jupyter → покадровый TPU-прогон там → JSONL сюда |
| `remote/smoke_resnet.py` | LinQ Jupyter | пример вендора resnet50 + замер |

## Команды (по порядку)

```powershell
tools\linq\tunnel\Connect-LinQ.cmd
.venv\Scripts\python.exe tools\linq\linq_tpu.py ping                       # брокер жив, сколько воркеров
.venv\Scripts\python.exe tools\linq\export_onnx.py --model yolov8n.pt --imgsz 640
wsl -d Ubuntu -- bash /mnt/d/msk-prom2026-mark/tools/linq/sdk/setup_sdk_wsl.sh     # один раз
wsl -d Ubuntu -- bash -c "cd /mnt/d/msk-prom2026-mark && ~/linq_sdk/venv/bin/python tools/linq/sdk/compile_yolo.py models/yolov8n_640_op13.onnx --preset O1"
.venv\Scripts\python.exe tools\linq\upload_program.py models\linq\yolov8n_640_op13_o1\yolov8n_640_op13_o1_b1_o1_h1m.tpu
.venv\Scripts\python.exe tools\linq\run_images.py --program mosprom_yolov8n_640_op13_o1_b1_o1_h1m.tpu --onnx models\yolov8n_640_op13.onnx IMG1 IMG2
.venv\Scripts\python.exe tools\linq\run_video.py data\videos\clip.mp4 --program mosprom_yolov8n_640_op13_o1_b1_o1_h1m.tpu --step 5
```

Секреты читаются из `.env` (`LINQ_JUPYTER_*`), в вывод не попадают. Брокер: `LINQ_AMQP_HOST`
(по умолчанию `127.0.0.1` через туннель, `10.0.114.30` внутри Jupyter).
