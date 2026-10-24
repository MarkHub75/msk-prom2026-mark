# Окружение (ноутбук Марка), 2026-10-24

| Что | Значение |
|---|---|
| ОС | Windows 11 Pro 10.0.26200 |
| CPU / RAM | Intel Core i5-13420H (12 потоков) / 15.7 ГБ |
| GPU | Intel UHD Graphics (CUDA нет) |
| Диски | C: 20.8 ГБ свободно из 243; D: 227 ГБ свободно из 233 (репозиторий на D:) |
| Python | 3.11.9 (`python`), 3.14 (`py` по умолчанию), 3.9; uv 0.13.0; проектный venv: `.venv` (Python 3.11) |
| Node | v24.14.0 |
| git | 2.51.2.windows.1 |
| ffmpeg | **нет** (на удалённой LinQ-машине есть `/usr/bin/ffmpeg`) |
| Docker | Docker Desktop 28.5.1 установлен, демон по умолчанию не запущен |
| WSL2 | `Ubuntu` (24.04.4, Python 3.12.3, 7 ГБ RAM, 952 ГБ диска), `docker-desktop`; обе остановлены |
| Сеть | Happ (Xray TUN) на весь трафик; LinQ (`10.0.114.0/24`) только через SSH-туннель на ноутбук Матвея, см. `docs/linq/VPN_SETUP.md` и `tools/linq/tunnel/` |

## Удалённая LinQ-машина (Jupyter `hackathon70007`)

| Что | Значение |
|---|---|
| ОС | Ubuntu 22.04.3 в контейнере, ядро 6.8 |
| CPU / RAM / диск | 64 ядра / 187 ГБ / 1.7 ТБ свободно |
| Python | 3.11.6 (conda-forge, `/opt/conda`), numpy 1.24.4, pika 1.4.4, protobuf 4.24.3, Pillow 10.1, `tpu_pycloud_format` 0.0.1; cv2 нет; ffmpeg есть |
| Интернет | PyPI и GitHub доступны; `cloud.lin-q.ru` — таймаут |
| Корень Jupyter | `~/work` (`examples/`, `packages/`, наша папка `mosprom_work/`) |
| Программы TPU | `/auto/cache/hackathon70007/*.tpu` |
| Брокер TPU API | RabbitMQ 3.13.7 `10.0.114.30:5672`, management `:15672`, `guest/guest` |

## Как воспроизвести локальный venv

```powershell
uv venv .venv --python 3.11
uv pip install --python .venv-linq\Scripts\python.exe requests websocket-client python-dotenv "numpy<2" "protobuf>=4.21,<5" pika==1.4.4 pillow onnx onnxruntime vendor\linq\tpu_pycloud_format-0.0.1-py3-none-any.whl
# экспорт моделей (CPU):
uv pip install --python .venv-linq\Scripts\python.exe --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cpu "torch==2.5.1+cpu" "torchvision==0.20.1+cpu" "ultralytics==8.3.230" onnxslim opencv-python-headless
```

`tpu_pycloud_format` берётся из Jupyter: `packages/tpu_pycloud_format-0.0.1-py3-none-any.whl`
(`python tools/linq/jupyter_remote.py download packages/tpu_pycloud_format-0.0.1-py3-none-any.whl vendor/linq/tpu_pycloud_format-0.0.1-py3-none-any.whl`).
