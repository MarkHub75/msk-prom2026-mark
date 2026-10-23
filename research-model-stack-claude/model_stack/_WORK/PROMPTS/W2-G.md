# W2-G YOLOV5_ANCHOR — anchor-based YOLOv5s: v7.0 против master, окружение, пробный train/export

Модель: Claude Sonnet 5.5, effort high. Почему: многофайловый дифф двух состояний репозитория с выводом «влияет/не влияет на веса, граф, метки» и подтверждающие прогоны. Закрывает K015; поддерживает K009.

Прочитай `ROOT\_WORK\CONTEXT.md`, `ROOT\_WORK\CONTEXT_WAVE2.md`, в `ROOT\CRITIC.md` — K009, K015, «Противоречия» п. 4, 6. Опорные: `W1-02_REPOS.md` (F12–F15), `W1-07_TRAINING.md` (F31, FLASH-7, H05), `W1-09_ENVIRONMENTS.md` (F29), `W1-10_EXPORT_ONNX.md` (F28–F30, патч dynamo=False), `W1-15_E2E_CHAINS.md` (R3a, FLASH-3, E2), `W1-06_ARCH_INFER.md` (F02, F40–F45).

Результат: `ROOT\_WORK\WAVE2\W2-G_YOLOV5_ANCHOR.md` (+ `W2-G_files\`).

## Что сделать
1. Дифф `ultralytics/yolov5` `v7.0` (`915bbf29…`) .. master (`af08ba15…`, проверено критиком) по путям `models/`, `utils/loss.py`, `utils/autoanchor.py`, `utils/dataloaders.py`, `utils/augmentations.py`, `train.py`, `val.py`, `export.py`, `requirements.txt`: что влияет на формат чекпойнта, обучение, метки, граф экспорта (opset 12 vs 17, onnxslim/onnxsim), зависимость master от `ultralytics>=8.4.164`.
2. Пробные прогоны 1 эпоха на coco8 (или construction-ppe, путь — FLASH W2-F) с `yolov5s.pt` v7.0 (sha из W1-03): (а) master в окружении с ultralytics 8.4.184; (б) v7.0 + torch 2.5.1 (CPU-venv допустим; GPU — по блокировке и только если GPU-venv уже без конфликтов, иначе CPU). Зафиксировать ошибки и обходы (например, `weights_only`, `dynamo=False`).
3. Экспорт обоих: инвентарь, формы (`[1,25200,85]` и cut-логиты 3 выхода), численная сверка ONNX с PT на одном тензоре (полный граф v7.0 vs PT ещё не сравнивался — K024).
4. Рекомендация окружения для anchor-based YOLOv5s с минимальным риском и lock-файл.

Попытайся опровергнуть: «master эквивалентен v7.0 по весам и графу».
