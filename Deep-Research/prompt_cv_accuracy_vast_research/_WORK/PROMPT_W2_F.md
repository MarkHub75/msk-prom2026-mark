# Common researcher brief — cv_accuracy_vast
You are an independent internet researcher, gpt-6.1-sol medium, explicitly assigned through the agent tool. Read the assigned prompt completely. You may read Context-prompt.md and prompt_cv_accuracy_vast_research.md if needed. Team: five strong engineers, industrial-safety video analytics hackathon, after first checkpoint on 2026-10-23. Final neural inference MUST run on LinQ, reported server has CPU+TPU (team report, exact configuration unknown). Vast.ai 1–2 RTX 3090 24GB are only contemplated for training, no rental or spending authorized. Experts emphasized accuracy verbally; this is not an official formula and does not remove latency constraints. Case pages 5,7,13 require balanced quality, few-second alert latency, deduplication, LinQ inference with speed measurement; priority scenarios may be selected. No local training, export, benchmark or hardware execution has been performed. Do not fabricate these.
Use real internet tools (discover with ALL_TOOLS where needed), search and OPEN primary docs/papers/code; do not rely on snippets or only previous summaries. Record source URL, author, publication/version vs access date, precise locator, evidence kind, conditions, limitations. Current host date should be recorded honestly. Repository versions/commits and weights licenses must be pinned when material. A live docs page without version is not a pinned recipe. Distinguish published claims/measurements from your own observations and recommendations. No verbatim copying of sources: preserve concise paraphrases and locators respecting source word limits. Do not download large model weights or datasets. No credentials, account changes, payments, external messages, or changes outside your own assigned _WORK files. You may expand strong leads relevant to the decision. Do not spawn agents; root coordinates.
Protect split independence: train/validation/optional SELECT/lockbox, no neighboring frames or identical scenes/cameras across independence claim, no threshold/checkpoint/ensemble tuning on lockbox. A stated procedure is not a performed experiment. No invented prices, VRAM fit, runtimes, accuracy or success probabilities. Keep camera calibration, LinQ quantization, and exhaustive behavioral weights/datasets as handoffs to neighboring research.
Your completion condition is a useful substantiated decision with alternatives, failure conditions, a proposed discriminating experiment and clearly bounded unknowns; no arbitrary link quota. Write detailed Russian research with exact English literals as needed. Include: decision-first findings; technical detail; candidate/recipe/protocol comparisons where relevant; evidence records with branch-local S/F IDs; contradictions/negative findings; experiment question, inputs, procedure, metrics, artifacts, outcomes, what success does not prove; handoffs and precise open questions. Save detailed work to your assigned path. In final response give brief findings, consequences, source versions, proposed experiment, resource prerequisites without invented estimates, leakage risks, cross-cell handoffs, and file path.
Available previous reports are in sibling topic folders (datasets, evaluation, training_strategy, research_link_platform, violation_methods, video_architecture, operator_product, hackathon_strategy, market_deployment, LinQ-case-analytics-research); existence is not proof of completeness. Use as leads, verify primary evidence anew. Official raster case: ../LinQ-case-analytics-research/КЕЙС_LinQ.pdf. Root visually read all 20 pages via existing sheets. See _WORK/CASE_NOTES.md.


# Second-wave requirements
Your exact W2 assignment and linked K IDs will follow. Read CRITIC.md and the specified W1 evidence fully enough to understand the gap. Do not repeat a general survey; obtain NEW primary evidence or actively seek limiting/counterexamples. Answer the concrete missing question and identify the decision changed. Explicitly report whether each K is closed, applicability clarified, contradicted, still open, or moot. Preserve the original criticism; never rewrite history. No need to force closure of device/account/target-data questions with public search. Save your own detailed W2 file and any concise primary material under your own directory. Branch-local IDs W2-xx-S/F, source/date/version/access/locator/provenance/conditions, proposed experiments vs actual observations, handoffs. No spending, training/export/device runs, account mutation or subagents. Practical examples must be documented and unexecuted unless explicitly observed read-only metadata.

# Assignment W2-F: Narrow LinQ smoke/fallback and neural-node obligations
Exclusive output: _WORK/W2_F.md. Branch IDs W2-F-Sxx/Fxx.

## Exact task
Recheck only current primary public LinQ examples/docs and identity of historical yolo5s/other fallback for an early smoke. Try obtain official 2025 manual PDF and visually inspect critical pages/commands if possible; use pdf skill when reading PDF. No full new PTQ/QAT research. Categorize historically demonstrated/publicly documented/source-inferred/device-unverified. Exact probe bundle for issued SDK: graph ops/shapes/output decoding/backend execution/CPU interpretation/state/residency/burst/concurrency. CPU neural ban is not literal official case evidence. Unknown issued SDK/access stays open. No training/export/device run, no external messages.

## Existing evidence
_WORK/W1_02.md, _WORK/W1_10.md, _WORK/W1_13.md, _WORK/W1_16.md; CRITIC.md; _WORK/CASE_NOTES.md.

## Original criticism (preserve provenance)
### K009 — Публичный LinQ путь исторический; нет проверенного запасного baseline и не разрешён neural CPU boundary

**Приоритет / тип:** P0 до финального выбора; главным образом внешний unknown.

**Материал и доказательство.** W1-16-F06 нашёл manual IVA H1 2025 с ONNX→TF→quantized→TPU и tested `yolo5s`; полный текст сохранён через extract, PDF bytes/screenshots не получены. Это реальное документальное основание, но не operator matrix актуального сервера. Основной YOLO26s и запасной YOLOX-s не являются испытанными на LinQ в этой работе. W1-10/16 правильно требуют учёта всех neural nodes, а допустимость neural CPU внутри LinQ-сервера оставляют организаторам. Последнее — консервативная плановая обязанность, **не найденная буквальная формула кейса «каждая сеть только на TPU»**.

**Последствие.** Поздний отказ TopK/Gather/shape/export может оставить команду без финального neural path. С другой стороны, чрезмерно строгая трактовка CPU запретит допустимую архитектуру без основания. Повторный полный research LinQ здесь нарушит границы и всё равно не заменит закрытый SDK.

**Точно недостающее доказательство.** Узкое публичное подтверждение применимого примера/артефакта и точная identity исторического fallback; визуальная проверка критичных страниц manual/команд, если PDF удастся получить. Отдельно — delivered SDK/SKU/operators, разрешённый neural CPU/fallback path, model residency/concurrency и фактическое выполнение каждого retained node. Последнее публичным поиском может не решаться.

**Задание второй волны / закрытие.** W2-F проверить первичные текущие публичные docs/examples ровно для раннего smoke и fallback; разнести `historically demonstrated / publicly documented / source-inferred / device-unverified`. Не объявлять YOLOv5 совместимым серверу 2026 по одному старому manual и не заменять baseline автоматически. Выдать точный bundle handoff и краткую последовательность probes для владельца выданного SDK, включая multi-model burst/residency и CPU boundary. Если actual package нет, K009 закрывается **уточнением границы**, а execution остаётся открытым Q. Полное PTQ/QAT исследование не запускать.



### K002 — Есть pinned base image, но нет согласованного training/export recipe одного кандидата

**Приоритет / тип:** P0; локализованный пробел воспроизводимости, не утверждение об ошибочности новых версий.

**Материал и доказательство.** W1-13-F01 предлагает PyTorch `2.14.1-cuda12.6-cudnn9-runtime` и digest, прямо называя его candidate. W1-02/06 используют текущий Ultralytics и RF-DETR dev snapshot, D-FINE — другую dependency историю. W1-16 отдельно показывает, что YOLO wrapper задаёт `dynamo=False`, а D-FINE exporter не фиксирует mode и наследует Torch default. W1-13 приводит generic API Torch и признаёт отсутствие final lock/derived image. Ни один результат не предъявляет единую разрешённую комбинацию Python/Torch/vision/exporter/ONNX/ORT для первого baseline и запасного пути.

**Последствие.** Сборка наиболее нового base, native requirements и экспортного инструмента может потребовать отдельной отладки уже на оплачиваемом host. «Все SHA закреплены» не означает, что такие пакеты совместимы друг с другом. Случайная замена Torch ради exporter создаст другой recipe и может изменить checkpoint loading или serialized graph.

**Точно недостающее доказательство.** Для одного baseline и одного нужного challenger — объявленные первичными проектами ограничения и конкретный выбранный compatibility envelope; explicit exporter implementation/mode/flags; путь резервного более консервативного стека; список зависимостей, которые ещё только предстоит разрешить/проверить. Фактический installed lock может появиться только при сборке и не должен быть подменён выдуманным.

**Задание второй волны / закрытие.** W2-B: проверить requirements/pyproject, native training/export docs, релевантные официальные release notes и несовместимые API для **выбранных** snapshots. Выдать два коротких recipe manifests с exact entrypoints и статусом каждого поля, разделить training и export environment при необходимости. Не строить универсальный образ для всех семейств. Документальная часть закрывается source-backed envelope; imports/forward/backward/export/24GB peaks — `not run`, с последовательностью smoke после отдельного поручения.



### K008 — Для temporal/verifier части shortlist содержит архитектуры, но не конкретных воспроизводимых кандидатов

**Приоритет / тип:** P1; неполнота обязательного shortlist, частично оправданная границами темы.

**Материал и доказательство.** RTMPose-s в W1-03 имеет config/checkpoint; W1-04 прямо говорит, что TSM/MoViNet/SlowFast/PoseC3D — архитектурные основания, а не выбранные deployment weights. W1-10 crop specialist описан без family/checkpoint/trainer. Теория proposal ceiling и условного вызова хороша, но команда пока не может оценить цену запуска **одного** такого кандидата. Полный поиск поведенческих весов вынесен отдельно и здесь не нужен.

**Последствие.** «Добавим лёгкий verifier» может оказаться новой разработкой модели, loss/data contract, export и runtime state вместо небольшого улучшения. Distillation тоже не является готовой запасной кнопкой; первая волна это верно признаёт, но shortlist всё ещё выглядит более готовым, чем набор её артефактов.

**Точно недостающее доказательство.** Один конкретный initialization/recipe для компактного crop classifier и один ограниченный causal temporal вариант **либо** явное решение отложить neural temporal branch. Для retained кандидата: source/config, weights/license, input preprocessing/classes, native export boundary, state/reset и train-data requirements. Отсутствие phone-use/fall классов в generic pretraining писать явно.

**Задание второй волны / закрытие.** W2-E выбрать по механизму ошибки K005 максимум один verifier и один representative temporal route; не обозревать всё action recognition. Проверить official model card/config/weights и online-vs-offline checkpoint semantics, особенно возможность ошибочно выдать bidirectional pretrained за causal. Результат — конкретная карточка «готовый initialization для будущего fine-tune» или «architecture-only, не включать в первые runs» с причинами. Наличие лицензированного generic веса не доказывает target ability, 24GB fit и LinQ pass.

