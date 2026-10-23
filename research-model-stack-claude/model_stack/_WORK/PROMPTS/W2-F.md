# W2-F REAL_FINETUNE — реальные короткие дообучения на RTX 4070 с официальными весами

Модель: Claude Sonnet 5.5, effort high. Почему: многоступенчатая проверка уже прочитанного кода (перенос весов, cls_remap, strip, resume, экспорт) реальным прогоном, с аккуратной интерпретацией логов и тензоров. Закрывает K013, K014.

Прочитай `ROOT\_WORK\CONTEXT.md`, `ROOT\_WORK\CONTEXT_WAVE2.md` (особенно GPU-блокировку), в `ROOT\CRITIC.md` — K013, K014, K023, «Противоречия» п. 7. Опорные: `W1-07_TRAINING.md` (§9, E1–E6, I01–I08, `W1-07_files\`), `W1-08_DATA_CONTRACTS.md` (cls_remap, аудитор), `W1-03_WEIGHTS.md` (sha, objv1-150, oiv7), `W1-09_ENVIRONMENTS.md` (X1, GPU-venv `<SCRATCH>\w109\venv-gpu`).

Результат: `ROOT\_WORK\WAVE2\W2-F_REAL_FINETUNE.md` (+ `W2-F_files\`: логи, json со сравнением тензоров, args.yaml). Ты — **единственный**, кто устанавливает пакеты в `w109\venv-gpu`: первым делом поставь туда `ultralytics==8.4.184` (и то, что нужно экспорту: onnx, onnxslim, onnxruntime) и запиши в FLASH «GPU-venv готов: состав …» — другие GPU-ветки ждут этого.

## Что сделать (каждый прогон — минуты; держи GPU-блокировку только на время прогона)
1. Данные: Ultralytics `construction-ppe` (скачать через `data=construction-ppe.yaml` или по URL из assets; проверить sha `bef8dcb5…` по W1-03), прогнать аудитор W1-08 `audit_yolo_dataset.py`; записать путь в FLASH для W2-E/K/N/L.
2. Официальные `yolo11n.pt`, `yolov8n.pt`, `yolo26n.pt` (sha по W1-03): 1–3 эпохи при imgsz 640, nc≠80. Зафиксировать строки лога `Transferred/Remapped/Overriding`, ширину `cv3` после загрузки, побайтовое сравнение тензоров головы с источником (какие скопированы, какие новые), s/it, VRAM (`torch.cuda.max_memory_allocated` и nvidia-smi), `check_amp` офлайн и онлайн, содержимое last.pt/best.pt до и после strip, resume прерванного прогона, resume после strip (ожидаемая ошибка), один прогон imgsz 960 для стоимости.
3. K014 тёплый старт: список совпадений имён классов construction-ppe/SH17/наших вероятных классов с `yolo26n-objv1-150.pt` и `yolov8n-oiv7.pt` (names — из метаданных/загрузки официальных весов); короткая абляция (одинаковые эпохи) COCO-старт vs objv1-150/oiv7-старт при совпадающих и несовпадающих именах — mAP по классам на ранних эпохах. Только как порядок эффекта.
4. Экспорт дообученной модели: `full` и raw (скрипты W1-10/номенклатура W2-D), проверка формы `[1,4+nc,8400]`, `metadata_props.names`, паритет PT↔ORT на одном кадре с `rect=False`.

Попытайся опровергнуть: «Transferred N/N обманчив» и «cls_remap даёт тёплый старт» — при каких условиях эффекта нет.
