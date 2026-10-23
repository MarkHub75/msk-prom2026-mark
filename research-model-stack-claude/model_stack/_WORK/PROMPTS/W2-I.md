# W2-I CROP_CLASSIFIER — классификатор кропов для каскада и ROI по pose

Модель: Claude Sonnet 5.5, effort high. Почему: связка нескольких контрактов (кроп из детектора/pose → нормализация → классификатор → экспорт), где тихое рассогласование нормализации ломает результат; нужен проверяемый рецепт с прогонами. Закрывает K017, поддерживает K005.

Прочитай `ROOT\_WORK\CONTEXT.md`, `ROOT\_WORK\CONTEXT_WAVE2.md`, в `ROOT\CRITIC.md` — K005, K017, K019. Опорные: `W1-13_CASCADES.md` (F01–F14, P2, P3, E2), `W1-15_E2E_CHAINS.md` (R6), `W1-12_QUANT_LINQ.md` (F07 — вендорский пример нормализации), `W1-11_PRE_POST.md` (6.4), `W1-05_PPE_HELMET_VEST.md` (таксономии). Читай FLASH `W2-D_FIRST_HOUR_KIT.md` (pose-графы) и `W2-F_REAL_FINETUNE.md` (GPU-venv, construction-ppe).

Результат: `ROOT\_WORK\WAVE2\W2-I_CROP_CLASSIFIER.md` (+ `W2-I_files\`).

## Что сделать
1. Кроп-набор: из construction-ppe (боксы Person + helmet/no_helmet и т.п.) собрать квадратные кропы головы/верха тела (правило ROI: верхняя часть person-бокса; альтернатива — ROI по pose-точкам nose/eyes/ears/shoulders из yolov8n-pose); RGB/BGR явно; классы «каска есть/нет» (и, если данные позволяют, мультиметочно helmet/vest).
2. Обучение (минуты, GPU по блокировке или CPU): torchvision `mobilenet_v2` и `efficientnet_b0` собственным коротким циклом; сравни с Ultralytics `YOLO("mobilenet_v2")`/`ClassificationTrainer` — что реально подаётся на вход (/255 vs ImageNet mean/std, CenterCrop vs letterbox) — по коду и прогону.
3. Варианты нормализации: снаружи; вшита в первый Conv; uint8 0..255 вход как в вендорском примере. Экспорт ONNX, инвентарь (Clip/ReLU6, GlobalAveragePool, Gemm), паритет PT↔ORT, batch 1 и 8.
4. Мультиметочная голова (BCE) vs однометочная — что проще для LinQ и для правил.
5. Стоимость каскада на хосте (кропы, resize, нормализация на N людей) — короткий замер на CPU (детальный бюджет — W2-M).

Попытайся опровергнуть: «каскад person→crop→классификатор лучше единого детектора для каски» — при каких размерах голов и плотности людей он проигрывает.
