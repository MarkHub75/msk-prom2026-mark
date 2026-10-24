# Запуск АРГУС в Docker

Из корня репозитория, на машине с Docker и Compose v2:

```sh
docker compose up --build
```

Открыть <http://127.0.0.1:8000>. Для фонового запуска: `docker compose up -d --build`.
Образ собирает фронт из `frontend/` и раздаёт `frontend/dist` тем же сервером, что REST API и WebSocket.

Compose явно включает `SAFEWATCH_FAKE=1` и `INFERENCE_BACKEND=linq`:
инференс синтетический, подключение к LinQ и ключи не требуются. Создавать `.env` не нужно.
Команда `serve --seed` создаёт 4 сектора, 8 камер и историю из 240 демособытий.
Сид не содержит видео: их можно загрузить через интерфейс камеры. Демособытия сида видны в журнале и статистике;
операторская лента показывает события обработки видео.

База, загрузки и артефакты сохраняются в `./data/app`. Повторный запуск не дублирует сид.
`./models` и `./data/demo` подключаются только для чтения; при первом запуске Compose создаст отсутствующие каталоги.
Если подготовлен пакет `data/demo/argus`, сервер импортирует его после сида.
`.env`, пользовательский конфиг, модели, данные и исследовательские каталоги исключены из контекста образа.

```sh
curl --fail http://127.0.0.1:8000/api/health
docker compose logs -f
docker compose down
```

Контейнер проверяет `/api/health` встроенным healthcheck. `docker compose down` сохраняет данные на хосте.

## Облачная проверка

Workflow `.github/workflows/docker.yml` запускается при push в `build/docker` и вручную.
На GitHub runner выполняются `docker build` и `docker compose up --build --detach --wait`.
Проверки требуют HTTP 200 от `/api/health`, `/` и собранного JavaScript, фейк-режим в `/api/meta`,
4 сектора, 8 камер и 240 событий. Логи контейнера выводятся и при ошибке; контейнеры затем останавливаются.
Локальный Docker для этой проверки не нужен:

```sh
gh run list --workflow docker.yml --branch build/docker
gh run watch RUN_ID --exit-status
gh run view RUN_ID --log
```
