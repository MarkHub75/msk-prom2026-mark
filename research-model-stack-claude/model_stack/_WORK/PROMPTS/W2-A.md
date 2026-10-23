# W2-A LINQ_PUBLIC — непрочитанные публичные материалы LinQ/IVA и методика вендорских измерений

Модель: Claude Sonnet 5.5, effort medium. Почему: адресный поиск и чтение конкретных документов и таблиц; анализ кода не требуется. Закрывает K007, K008, частично K006.

Прочитай `ROOT\_WORK\CONTEXT.md`, `ROOT\_WORK\CONTEXT_WAVE2.md`, в `ROOT\CRITIC.md` — K006, K007, K008, разделы «Достаточно установлено» и «Противоречия». Опорные материалы: `ROOT\_WORK\WAVE1\W1-12_QUANT_LINQ.md` (S03, S05, S11, S12, S18), `W1-12_files\2026_linq_presentation.txt`, `W1-14_METRICS.md` §3.3, `W1-01_FAMILIES.md`.

Результат: `ROOT\_WORK\WAVE2\W2-A_LINQ_PUBLIC.md`.

## Вопросы
1. Прочитать (скачать в SCRATCH, извлечь текст, кириллицу проверить) все ещё не прочитанные PDF на `lin-q.ru/docs` и связанные: `_HPact_manual_LINQ_HP1M_02.pdf`, руководства HPD/HPQ, `me2025/ds_LinqHP*`, полный `linq_hps_datasheet.pdf`, пресс-материалы `lin-q.ru/press` и аналогичные; реестр Минцифры `reestr.digital.gov.ru/reestr/546161`, `ht-dc.ru/fw_h`. Для каждого — что сказано о: формате входа модели (ONNX/TF, opset, layout), квантовании (per-channel, симметрия, percentile), списке операторов, Model Zoo, приёме QDQ, мультимодельности, batch, версиях Python/TF/Ubuntu, наличии примеров YOLO, методике измерений. Локаторы — страница/раздел.
2. Все PyPI-пакеты автора «IVA Technologies»/«IVA-Tech»/HiTech (pytpu, iva-applications, tpu-framework и т.п.): версии и даты (PyPI JSON API), что лежит в sdist/wheel (только список файлов и метаданные; код читает W2-B — передай ему пути в FLASH сразу).
3. MLCommons MLPerf Inference: есть ли подачи HiTech/IVA в раундах v1.0…v5.x (results repo `mlcommons/inference_results_v*`), какие модели, сценарии (SingleStream/Offline), метрика latency (p90/среднее), точность, входы. Какой вариант ResNet-50 стоит за «2,3 мс», «2,99 мс / 432,9 FPS», «460 FPS».
4. Методика таблицы презентации 2026: можно ли объяснить FPS > 1/latency (конвейеризация? Offline?); аномалии ssd_mobilenet_v2 b8 < b1, единицы anti_spoof/lenet5. Если не объясняется по источникам — сформулируй точный вопрос постановщику.
5. Любые публичные упоминания yolo5s/yolov8/yolo11 на LinQ (новости, вакансии, конференции, хабр, GitHub): что именно за граф/вход/точка среза.

Попытайся опровергнуть: «вендорская цифра yolov8n_pose означает, что C2f+DFL проходит компилятор» (K006) — найди, что именно было измерено, или зафиксируй, что это не установлено.

Ограничения: ничего не регистрировать, личные кабинеты не открывать. Если документ требует логина — фиксируй состояние доступа.
