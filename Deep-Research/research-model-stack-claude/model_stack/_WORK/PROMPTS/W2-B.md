# W2-B VENDOR_CODE — контракты YOLO в коде вендорских пакетов и полный разбор linq-cv-bench

Модель: Claude Sonnet 5.5, effort high. Почему: чтение чужого кода нескольких версий без запуска и вывод контрактов пред/пост, API и ошибок — нетривиальное многофайловое чтение. Закрывает K009, K010; поддерживает K003 (API для интроспектора).

Прочитай `ROOT\_WORK\CONTEXT.md`, `ROOT\_WORK\CONTEXT_WAVE2.md`, в `ROOT\CRITIC.md` — K003, K009, K010 и проверку 7 в шапке. Опорные: `W1-12_QUANT_LINQ.md` (F13–F19, S07, S10, S11), `W1-11_PRE_POST.md` (F29, 6.3–6.4), `W1-01_FAMILIES.md` (F06, F07), `W1-15_E2E_CHAINS.md` (C11, FLASH-7). Читай FLASH файла `ROOT\_WORK\WAVE2\W2-A_LINQ_PUBLIC.md` — он может найти новые пакеты.

Результат: `ROOT\_WORK\WAVE2\W2-B_VENDOR_CODE.md`.

## Вопросы
1. Все доступные версии `pytpu`, `iva-applications` и других пакетов автора на PyPI (скачать sdist/wheel в отдельный пустой каталог SCRATCH, распаковать как архив, **не устанавливать и не импортировать**): найти модули/функции пред- и постобработки для YOLO-семейств (`yolo2/3/4`, `tiny_yolo`, `yolo5*`, `yolov5*`, `yolov8*`, `yolo11*`), SSD, классификаторов: якоря, маски, порядок голов, имена выходов, letterbox (заливка 114 или 128), нормализация (/255, mean), раскладка NHWC/NCHW, NMS-параметры. Если для yolo5s/yolov8 ничего нет — зафиксировать охват поиска (какие версии, grep-шаблоны).
2. Публичный API фреймворка, видимый из кода пакетов и стенда: `onnx_to_tf`, `QuantizedModel`, `RegularModel`, `calibrate`, `quantize`, `compile_`, пресеты O1/O5, DEFAULT/STAGING, `TPU_128x128_PARAMS`, `tpu.Device`, `pytpu` режимы, формат `.tpu` (ZIP, `metadata.json`: `user_order`, `user_dtype`, `scales`) — сигнатуры с версиями и файлами. Это нужно W2-D для интроспектора и распаковщика (передай в FLASH как можно раньше).
3. `sherstpasha/linq-cv-bench`@3ad1b7aa (и все ветки/коммиты/issues/другие репозитории автора): полный обзор файлов через `gh api` (не запускать), особенно `scr/detection/*`, `RUN_SCENARIO.txt`, логи, сегментация O5 «did not produce a final reproducible result». Почему self-build YOLOv8s не вошёл в «Final TPU plan» — цитаты причин/ошибок, если есть; если нет — что можно установить косвенно (например, что скрипт содержит ошибку, неполный, не вызывается).
4. Кодовый поиск других пользователей фреймворка: `gh api search/code` (и веб-поиск) по `"onnx_to_tf"`, `"RegularModel" tpu`, `"TPU_128x128_PARAMS"`, `"onnx_direct"`, `"pytpu"`, `"tpu_framework"`, `"iva_applications"`. Результаты с репозиториями, commit, содержанием.

Попытайся опровергнуть: «yolo5s у LinQ = оригинальный anchor-based v7.0» — что в коде указывает на иное (u-версия, spp, другие якоря)?

Код linq-cv-bench не копируй в ROOT целиком (лицензия не заявлена): короткие цитаты с локаторами допустимы.
