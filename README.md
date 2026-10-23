# MOSPROM 2026 · LinQ

Исследовательская база команды хакатона «Открой#Моспром» 2026: промышленная видеоаналитика безопасности с обязательным инференсом на LinQ.

Текущая точка — [RESUME.md](RESUME.md), исполняемый worker — [docs/VIDEO_MVP.md](docs/VIDEO_MVP.md), подключение Марка — [docs/BACKEND_HANDOFF.md](docs/BACKEND_HANDOFF.md) и [проверка API](docs/BACKEND_CHECK.md). Исследовательский указатель — [INDEX.md](INDEX.md); завершённые исследования не нужно повторять.

В [Deep-Research/](Deep-Research/) сохранены десять тематических исследований. Девять имеют итоговые отчёты на русском и английском; `model_stack` содержит незавершённые материалы и критический разбор. Исследовательские рекомендации сами по себе не подтверждают работоспособность прототипа.

## ML MVP

Реализация находится в `ml/`: детекция касок и pose, временные правила падения/лежания, LinQ-адаптер, видеоконвейер и надёжная доставка событий. Начните с [инструкции интеграции](docs/INTEGRATION.md) и [контрактов](docs/CONTRACTS.md). Параметры камеры: [configs/rules.example.json](configs/rules.example.json).

```bash
python -m unittest discover -s tests -v
python -m ml.pipeline.cli --help
```

```bash
bash scripts/linq_video_mvp.sh \
  --source /path/to/industrial.mp4 \
  --state-dir /workspace/artifacts/video-mvp/new-camera-01 \
  --sample-fps 2 --local-test-sink
```

`--local-test-sink` — тестовый получатель, не backend команды. Для настоящего сервиса задать подтверждённые `--backend-url` и `--evidence-base-url`; токен читается только из `MOSPROM_BACKEND_TOKEN`. Endpoint и media-префикс фиксируются хешем в outbox: повторную доставку нельзя незаметно переключить другому получателю. ACK требует `committed:true`, точные event_id и целочисленную revision.

ResNet50, Helmet и Split-Pose реально выполнялись на LinQ. Проверено сохранение UNKNOWN после управляемого отключения клиента и получение ответа того же UUID без повторной публикации. VPN/SSH не перенастраивались и не отключались. [Измерения](docs/PERFORMANCE.md): обычный Helmet-запрос занял 10.43 с, включая transport/setup/close. Исторические 0.046 FPS относятся к явно помеченному repeated-image control, не к работе в реальном времени.

Положительный промышленный эпизод и реальная интеграция с backend/frontend Марка пока не подтверждены: нужны доступные API/журнал/evidence и подходящий размеченный видеокейс. Локальный HTTP PASS или PyTorch/ONNX не заменяют эти проверки. Видео, модели, приватная конфигурация и runtime-отчёты остаются вне Git.
