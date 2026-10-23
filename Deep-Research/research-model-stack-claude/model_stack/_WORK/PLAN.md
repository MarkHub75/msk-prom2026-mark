# PLAN — model_stack research

Создан: 2026-10-23 ~04:42 MSK (UTC+3), оркестратор Claude Opus 5.5 (`claude-opus-5-5`, effort high — сессия Claude Code 2.1.309).

## Среда (установлено оркестратором, local_observation)
- Время старта: `date` → 2026-10-23 04:33:52 +0300.
- Рабочая папка: `research-model-stack-claude/`; создан `model_stack/` (ранее не существовал, предыдущих результатов нет). Соседняя папка `../research-linq-platform/` содержит только промпт — отчётов linq_platform нет.
- Сеть: github.com API, huggingface.co API, lin-q.ru — HTTP 200. `gh` авторизован. Python 3.13.9 через `py`; pip/venv по умолчанию не настроены (venv создаётся в scratch).
- Переменные `CLAUDE_CODE_EFFORT_LEVEL`, `CLAUDE_CODE_SUBAGENT_MODEL`, `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_*_MODEL` не заданы. В `~/.claude/settings.json`: `"model": "opus"`, `"effortLevel": "high"` (для основной сессии). Глобальные настройки не менялись.
- Механизм назначения: инструмент Agent с параметрами `model` (`sonnet` | `opus`) и `effort` (`medium` | `high`). Параметр `model` принимает только алиасы, поэтому фактическая модель каждого агента фиксируется по его самоотчёту: агент записывает точное название и model ID из своего системного окружения в шапку файла результата. Эти данные собираются в RUN_STATE.md.
- Вложенное делегирование исследователями не используется: все задачи создаёт корневой оркестратор.

## Публичный контекст LinQ (снят до запуска, см. CONTEXT.md §2)
LinQ H: int8, систолический массив 128×128, 16 МБ on-chip, «PyTorch через ONNX», компилятор с «DNN Quant, Graph Optimizer»; список «поддерживаемых сетей» включает `yolo5s`, `yolo8`, `yolo11`, `ssd_mobilenet_v1/v2`, `tiny_yolo2/3`, `scrfd 2.5g`, классификаторы. Это меняет фокус: в первую очередь разбираем семейства из списка (YOLOv5/v8/11, SSD-MobileNet) и их экспорт, остальные — как альтернативы с обоснованием.

## Первая волна: 16 ячеек
Ячейка 05 из исходной программы разделена на 05 (каски/жилеты/person) и 16 (респиратор, курение, огонь, опасные зоны), потому что у этих сценариев разные данные и разные модельные пути. Остальные ячейки соответствуют программе.

| ID | Тема | Модель / effort | Почему такой уровень | Ожидаемые доказательства | Зависимости | Файл |
|---|---|---|---|---|---|---|
| W1-01 | Карта семейств и вариантов | Sonnet 5.5 / medium | широкий поиск и каталогизация | статьи, repo, конфиги, таблицы | — | WAVE1/W1-01_FAMILIES.md |
| W1-02 | Канонические repo, версии, fork (включая NPU-fork) | Sonnet 5.5 / medium | фиксация релизов, тегов, SHA | releases, tags, commits, issues | — | WAVE1/W1-02_REPOS.md |
| W1-03 | Базовые веса и артефакты | Sonnet 5.5 / medium | метаданные артефактов | release assets, HF API, LFS sha | W1-01 (мягко) | WAVE1/W1-03_WEIGHTS.md |
| W1-04 | Лицензии кода / весов / данных | Sonnet 5.5 / medium | точный поиск первичных документов | LICENSE, model cards, terms | W1-05/16 (чтение) | WAVE1/W1-04_LICENSES.md |
| W1-05 | Доменные веса: каска, голова, жилет, person | Sonnet 5.5 / medium | поиск и прослеживание артефактов | HF/GitHub/Roboflow метаданные, data.yaml | — | WAVE1/W1-05_PPE_HELMET_VEST.md |
| W1-16 | Респиратор, курение, огонь, зоны, падения | Sonnet 5.5 / medium | то же для других сценариев | то же | W1-13 (передача) | WAVE1/W1-16_PPE_RESP_SMOKE_ZONE.md |
| W1-06 | Архитектура и inference path (train/eval/export) | Sonnet 5.5 / high | многофайловое чтение реализации | source_code с commit | W1-10 (чтение) | WAVE1/W1-06_ARCH_INFER.md |
| W1-07 | Обучение и жизненный цикл checkpoint | Sonnet 5.5 / high | trainer/loader/EMA/resume через несколько модулей | source_code, issues | W1-08 | WAVE1/W1-07_TRAINING.md |
| W1-08 | Data loaders, разметка, class mapping | Sonnet 5.5 / high | «тихие» ошибки по цепочке модулей | source_code, issues | — | WAVE1/W1-08_DATA_CONTRACTS.md |
| W1-09 | Окружения и зависимости | Sonnet 5.5 / medium (эскалация до high при ABI-конфликтах) | официальные матрицы, файлы зависимостей | pyproject, матрицы, pip dry-run | — | WAVE1/W1-09_ENVIRONMENTS.md |
| W1-10 | Exporter, ONNX-граф, переносимость + локальный CPU-экспорт | Opus 5.5 / medium | согласование кода, режимов и реального графа | source_code + local_observation (экспорт, инвентарь операторов, ORT) | — (поставщик для 06/11/12/15) | WAVE1/W1-10_EXPORT_ONNX.md |
| W1-11 | Пред/постобработка и численная согласованность | Sonnet 5.5 / high | сравнение нескольких реализаций одной процедуры | source_code, примеры, issues | W1-10 | WAVE1/W1-11_PRE_POST.md |
| W1-12 | Квантование и стык с LinQ | Opus 5.5 / medium | int8-only устройство с закрытым компилятором; разделение фактов и аналогий | PDF LinQ, docs ORT/NNCF, NPU-прецеденты, local_observation | W1-10 | WAVE1/W1-12_QUANT_LINQ.md |
| W1-13 | Каскады, pose, трекинг, open-vocab | Sonnet 5.5 / high | контракты нескольких взаимодействующих моделей | source_code, веса | W1-16 | WAVE1/W1-13_CASCADES.md |
| W1-14 | Метрики и сопоставимость | Sonnet 5.5 / high | анализ условий измерений и валидатора | таблицы, код валидатора | W1-05/16 | WAVE1/W1-14_METRICS.md |
| W1-15 | Сквозные цепочки и разрывы | Opus 5.5 / medium | соединение компонентов и межкомпонентные противоречия | собственная перепроверка первичных источников | все (чтение) | WAVE1/W1-15_E2E_CHAINS.md |

Распределение: 8 × Sonnet medium, 6 × Sonnet high, 3 × Opus medium (W1-10, W1-12, W1-15). Opus medium — только там, где пересекаются несколько форматов и закрытая платформа.

Задания: `_WORK/PROMPTS/W1-XX.md` + общий `_WORK/CONTEXT.md`. Параллельность: все 16 запускаются в фоне одновременно, при отказе по лимиту — очередью.

## Дальнейший конвейер
Критик (Opus 5.5 / high, свежий контекст: получает только исходный промпт, CONTEXT, PLAN и файлы WAVE1) → CRITIC.md (K001…) → вторая волна (задачи по K-ID, сложность назначается заново, файлы WAVE2/W2-XX_*.md) → сборщик (Opus 5.5 / high) → SOURCES.md, RAW_FACTS.md, OPEN_QUESTIONS.md, дополнение CRITIC.md → автор (Opus 5.5 / high) → черновик `_WORK/STAGES/DRAFT_HUMAN.md` → редактор (Opus 5.5 / high) → report_human_model_stack.md → сжиматель (Opus 5.5 / high) → report_machine_model_stack.md. Финального проверяющего нет.
