# План training_strategy

Цель: условная стратегия быстрой адаптации детекторов промышленного CCTV при неизвестных целевых данных, примерно 45 часах кейса и обязательном последующем инференсе на LinQ. Сильный результат связывает наблюдаемую ошибку, вмешательство, независимую проверку и пригодный артефакт.

## Первая волна

| Ячейка | Вопрос и решение | Первичные направления | Файл |
|---|---|---|---|
| 01 | Готовые веса, данные или обучение: выбор baseline | detection recipes, диагностика ошибок | W1/01_BASELINE.md |
| 02 | Предобучение, head-only, full fine-tuning, BN | TFA, detection transfer, trainer | W1/02_FINETUNING.md |
| 03 | Few-shot и partial labels | TFA, sparse annotation detection | W1/03_FEWSHOT_PARTIAL.md |
| 04 | Редкие классы и hard negatives | repeat factor sampling, focal loss, LVIS | W1/04_IMBALANCE.md |
| 05 | Аугментации CCTV | implementation docs/code, bbox transforms | W1/05_AUGMENTATION.md |
| 06 | Разрешение, crops и каскады | small object detection, sliced inference | W1/06_SCALE.md |
| 07 | Смешивание доменов, новые камеры | DA detection, source-free, forgetting | W1/07_DOMAIN.md |
| 08 | Отбор на доразметку | active learning detection, CVAT | W1/08_ACTIVE.md |
| 09 | Pseudo-labels и semi-supervision | Soft Teacher, Unbiased Teacher | W1/09_PSEUDO.md |
| 10 | Offline teachers, VLM и distillation | author repos, actual trainer support | W1/10_TEACHER.md |
| 11 | Синтетика и copy-paste | domain randomization, Simple Copy-Paste | W1/11_SYNTHETIC.md |
| 12 | Диагностика и настройка оптимизации | pinned recipes, trainer, defaults | W1/12_OPTIMIZATION.md |
| 13 | PTQ/QAT, pruning и LinQ | ORT, primary compression tools, vendor | W1/13_COMPRESSION.md |
| 14 | GPU, DDP и очередь trials | PyTorch DDP/profiler, trainer | W1/14_COMPUTE.md |
| 15 | Checkpoint, variance, принятие изменения | few-shot evaluation, splits, export | W1/15_SELECTION.md |

Ячейки не обещают одинакового объёма. Каждая восстанавливает область применимости сильных источников и локализует неизвестные; общие советы без первичного основания не считаются завершением.

## Последующие роли

1. Критик gpt-6.1-sol/high без истории: конкретные K-ID и задания второй волны; сохранение CRITIC.md.
2. Вторая волна gpt-6.1-sol/medium: новые доказательства по K-ID, ограничения и попытки опровержения. Отдельные файлы W2.
3. Сборщик gpt-6.1-sol/high: стабильные S/F/Q/E-ID, SOURCES.md, RAW_FACTS.md, OPEN_QUESTIONS.md; состояния K-ID.
4. Автор high: большой русский черновик _WORK/AUTHOR_DRAFT.md.
5. Редактор high: report_human_training_strategy.md; сохраняет факты и ограничения.
6. Сжиматель high: report_machine_training_strategy.md на английском с YAML-шапкой; завершает конвейер.

## Общие критерии

Первичные страницы открываются; сниппет — только зацепка. Сохраняются дата/версия/commit, локатор, протокол, baseline, данные, метрика и реальный статус чтения/запуска. Публикационное измерение не является нашим тестом. Неизвестные SDK, данные, классы и железо остаются неизвестными. Команды допустимы только с найденным основанием; иначе процедурный псевдокод. Каждый полезный E-ID содержит входы, контроль, измерения, артефакты, варианты исхода, stop rule и предел подтверждения.
