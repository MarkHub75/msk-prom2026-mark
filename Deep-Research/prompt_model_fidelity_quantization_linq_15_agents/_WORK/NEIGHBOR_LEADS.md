# Соседние материалы: зацепки, не наши измерения

Обнаружены существующие отчёты ../research_link_platform/report_machine_linq_platform.md, ../prompt_cv_accuracy_vast_research/report_machine_cv_accuracy_vast.md, ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md, ../prompt_camera_calibration_geometry_6_agents/report_machine_camera_calibration_geometry.md, ../evaluation/report_machine_evaluation.md, ../datasets/report_machine_datasets.md. Их даты и статусы смотреть в шапках; это вторичные внутрикомандные источники. Мы их не запускали и не переписываем.

## Для W1-04/13/14/15

В linq_platform подробно разобран первичный сторонний репозиторий https://github.com/sherstpasha/linq-cv-bench/tree/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140 (commit 2026-04-03; автор Павел Шерстнев). Это не автоматически код производителя и не доказательство успешно исполненного собственного YOLO. Ищите первичный код заново/проверяйте сохранённый pinned checkout и локаторы. Его адаптер предполагает COCO84/85, что ломает custom nc1/2/3; возможны дополнительные ошибки output_tensor_name/uint8/class mapping/first-output selection. В соседнем исследовании выполнены shape-only/helper probes, но не LinQ inference. Нельзя присваивать их результаты нашей работе.

В том же материале: broad TypeError retry вокруг calibrate(percentile=...) способен скрывать effective parameter; guide/version seams; TinyYOLO3 public ONNX имеет другую встроенную NMS/anchors/preprocessing и не эквивалентен неизвестному .tpu. Проверяйте это как конкретные зацепки, не как заранее заданный вывод.

Официальная презентация 2026: https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf — указанные там TPU Runtime 16.18.6 и TPU Framework 2026.8.43 относятся к опубликованному benchmark, а не выданному команде окружению. На сайте сведения HX не переносить на LinQ H1.

Полный кейс найден и прочитан root; первичные локальные заметки: CASE_NOTES.md, оригинал INPUT/CASE_LINQ.pdf. Это уточняет прежнюю фразу «PDF нет»: в текущей папке первоначально не было, но нашли в соседней. VM/сервис обещаны на с.8, доступ здесь не получен.

## Дополнительные соседние зацепки

- evaluation (checked_at 2026-10-23T08:11:28+03:00) разбирает paired/cluster uncertainty, независимый GT, правильные знаменатели, late/duplicate/wrong-person события и FP/hour. Его исходный full-case unavailable устарел относительно найденного нами PDF; статистические/методические разделы можно использовать как зацепки к первичным источникам, не переносить исторический статус кейса.
- camera_calibration_geometry подчёркивает, что floor homography применима к точкам на своей плоскости; timestamp/PTS и фактическое sampling отделяются от throughput, а небольшое смещение ключевой точки может усиливаться перспективой. См. соседний report_machine для первичных ссылок; количественную потерю LinQ мы не измеряли.
- cv_accuracy_vast предупреждает: ошибки событий могут происходить на ownership/actor/rule уровне при правильных боксах; frozen source sampling и causal replay нужны для выделения модельного эффекта. Его 201 F/290 S — не наши собственные источники и не независимые подтверждения.
