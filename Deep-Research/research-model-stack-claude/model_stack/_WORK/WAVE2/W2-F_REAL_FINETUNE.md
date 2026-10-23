# W2-F REAL_FINETUNE — реальные короткие дообучения на RTX 4070 (K013, K014)

## Шапка
- ID ячейки: W2-F (вторая волна), участок: K013, K014 (+K023-часть: аудит/использование construction-ppe).
- Запрошено: Claude Sonnet 5.5, effort high.
- Фактическая модель (из системного окружения): **Sonnet 5.5, model ID `claude-sonnet-5-5`**.
- Начало: 2026-10-23 ~05:30 MSK (по часам машины). Конец: см. в конце файла.
- Статус: в работе (файл пишется по ходу).

## FLASH (для соседних GPU-веток)

- **FLASH-1 (GPU-venv готов), 2026-10-23 ~05:32.** Путь: `C:\Users\User\AppData\Local\Temp\claude\C--Users-User-Documents-mosprom2026-hack-research-model-stack-claude\adce1a1a-fbbd-4ab7-b3bb-2b61dbc9d01b\scratchpad\w109\venv-gpu\Scripts\python.exe`. Состав (local_observation, `pip list`): `torch 2.14.1+cu126`, `torchvision 0.29.1+cu126` (не затронуты установкой), `ultralytics 8.4.184`, `ultralytics-thop 2.2.3`, `ultralytics-platform 0.1.91`, `onnx 1.23.2`, `onnxslim 0.1.98`, `onnxruntime 1.31.0` (CPU EP), `numpy 2.5.2`, `opencv-python 5.0.0.93`, `matplotlib 3.11.2`, `polars 2.0.0`, `psutil 7.2.2`, `nvidia-ml-py 13.615.71`, `PyYAML 6.0.3`. Лог установки: `W2-F_files\pip_install_gpu_venv.log`. **Другие ветки: ничего в этот venv не устанавливать** (если нужен иной пакет — свой venv).
- **FLASH-2 (construction-ppe готов).** Zip скачан с `https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip`, 178415813 B, **sha256 = `bef8dcb599aa4e9d9f5e602cb6fa7143d3c84d7f6a0ff40463d7f2a4c2632ccc`** (вычислен локально, совпадает с `bef8dcb5…` из W1-03-F13; local_observation). Распакован в `SCRATCH\w2f\datasets\construction-ppe\` (images/{train,val,test} = 1132/143/141; labels/ те же + LICENSE (AGPL-3.0 текст) + data.yaml). YAML с абсолютным путём (для `data=`; глобальные настройки Ultralytics не менялись): `SCRATCH\w2f\construction-ppe-abs.yaml`, т.е. `C:\Users\User\AppData\Local\Temp\claude\C--Users-User-Documents-mosprom2026-hack-research-model-stack-claude\adce1a1a-fbbd-4ab7-b3bb-2b61dbc9d01b\scratchpad\w2f\construction-ppe-abs.yaml`. Датасет только читать (не изменять, не удалять). Аудитор W1-08: 0 errors, 0 warnings (`W2-F_files\audit_construction_ppe.txt/.json`); метки: train 9098 боксов, val 1172, test 1251; гистограмма train: helmet 1341, gloves 1146, vest 1269, boots 1235, goggles 419, none 651, Person 1770, no_helmet 400, no_goggle 337, no_gloves 442, no_boots 88. В `labels/train` есть 10 «сиротских» файлов `imageNNN(1).txt` без изображений (Ultralytics их не читает).
