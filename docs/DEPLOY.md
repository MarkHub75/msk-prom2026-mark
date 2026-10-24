# Развёртывание Argus на другой машине

Инструкция для стационарного компьютера, который держит демо весь показ. Публичный адрес даёт сервис Феди с выделенным IP: он смотрит на порт 8000 этой машины. Его настройка, HTTPS и обратный прокси сюда не входят.

## Требования

- Windows 10/11 или Linux с Docker Desktop (Linux: Docker Engine с плагином compose). Docker Desktop запущен: `docker info` отвечает без ошибки.
- Свободный порт 8000. Локальный сервер Argus на этой машине остановлен: `uv run --no-sync safewatch stop`.
- Интернет на время первой сборки: образ тянет `node:24-slim`, `python:3.12-slim`, `uv` и колёса Python (ffmpeg приходит колесом `imageio-ffmpeg`, отдельно не ставится).
- Python, Node и uv на хосте не нужны.

## Что скопировать

1. Репозиторий: `git clone https://github.com/MarkHub75/msk-prom2026-mark.git`, ветка `main`.
2. Демо-пакет `data/demo/<name>/` целиком (`manifest.json`, `videos/`, `artifacts/`) в ту же папку клона. Пакет не лежит в git. Имя по умолчанию `argus` (`demo.pack` в `config/default.yaml`); другое имя — `demo.pack` в `config/user.yaml`.
3. При нужде `models/`: файлы `*.onnx` для `INFERENCE_BACKEND=local` и модели Матвея из `config/models.yaml`. Демо-пакету модели не нужны: детекции уже в `artifacts/`.

## `.env`

Файл в корне клона, шаблон `.env.example`. В образ он не попадает, compose передаёт его переменными. Без `.env` контейнер тоже стартует: сид и демо-пакет ключей не требуют.

- `SAFEWATCH_FAKE=1` — показ только демо-пакета, без LinQ. Рекомендуется для стенда.
- `INFERENCE_BACKEND` — `linq` (по умолчанию) или `local` (onnxruntime на CPU, нужны `models/*.onnx`).
- `LINQ_*` нужны только для кнопки «Загрузить своё видео» на LinQ. Jupyter LinQ контейнер видит через туннель на хосте: compose сам ставит `LINQ_JUPYTER_URL=http://host.docker.internal:8888`, туннель `tools\linq\tunnel\Connect-LinQ.cmd` запускается на хосте до загрузки видео.

## Команды

Из корня клона:

```
docker compose up -d --build
```

Первая сборка идёт несколько минут, следующие берут слои из кэша. Контейнер стартует с `serve --seed`: создаёт демо-мир и импортирует демо-пакет. Готовность: `docker compose ps` показывает `healthy` (проверка `GET /api/health`), в браузере открывается `http://127.0.0.1:8000`, пакет виден в `GET /api/demo/packs`.

- Логи: `docker compose logs -f`.
- Остановка: `docker compose down` (данные остаются в `data/app`).
- После `git pull` или замены фронта: снова `docker compose up -d --build`.

## Данные

- `./data/app` — том данных: база `safewatch.db`, загруженные видео, артефакты, кадры доказательств. Переживает `down` и пересборку.
- `./data/demo` монтируется только для чтения, `./models` тоже.
- Сброс базы: `docker compose down`, удалить папку `data/app`, `docker compose up -d`. Сид и демо-пакет импортируются заново.

## Фронт Егора

Образ собирает фронт из папки `frontend/` клона. Чтобы показать фронт Егора, перед сборкой замените содержимое `frontend/` его версией (`package.json`, `package-lock.json`, `src/` и остальное; сборка `npm run build` должна класть файлы в `frontend/dist`), затем `docker compose up -d --build`. Бэкенд и контракт `contract/openapi.json` при этом не меняются.
