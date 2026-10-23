# W2-O OV_TEACHER — open-vocabulary teacher для авторазметки на RTX 4070

Модель: Claude Sonnet 5.5, effort medium. Почему: установка и прогон документированных моделей на небольшом наборе кадров с замерами — прямолинейная работа. Закрывает K029.

Прочитай `ROOT\_WORK\CONTEXT.md`, `ROOT\_WORK\CONTEXT_WAVE2.md` (GPU-блокировка; `trust_remote_code` запрещён), в `ROOT\CRITIC.md` — K029. Опорные: `W1-13_CASCADES.md` (F24–F27, P5, E3), `W1-01_FAMILIES.md` (open-vocab), `W1-04_LICENSES.md`. Читай FLASH `W2-F_REAL_FINETUNE.md` (путь к construction-ppe, состояние GPU-venv).

Результат: `ROOT\_WORK\WAVE2\W2-O_OV_TEACHER.md` (+ `W2-O_files\`: json с метриками, небольшие превью).

## Что сделать
1. Модели: YOLOE (Ultralytics, вариант, реально доступный в 8.4.184 — проверь имена весов), Grounding DINO tiny (HF transformers, Apache-2.0), OWLv2 (HF transformers). Florence-2 — не использовать (требует `trust_remote_code`). Собственный venv (CPU-venv + CUDA-torch только при необходимости; лучше — если W2-F разрешит в FLASH, читай состав `w109\venv-gpu`; не устанавливай в него пакеты).
2. Набор: 30–50 кадров construction-ppe val/test с разметкой (helmet/no_helmet/vest/Person и т.п.) + несколько кадров с сигаретой/маской, если найдутся с понятной лицензией.
3. Промпты: «hard hat», «safety helmet», «person without helmet», «safety vest», «respirator», «face mask», «cigarette» — VRAM, с/кадр, precision/recall против разметки при нескольких порогах (только как ориентир).
4. YOLOE: проверить, что `set_classes` + экспорт «запекает» классы в обычную голову (инвентарь ONNX, наличие текстового энкодера в графе) — по коду и экспорту.
5. Рекомендация: какой teacher и с какими промптами реально ускорит разметку в первые часы хакатона, какие классы ему не по силам.

Попытайся опровергнуть: «open-vocab teacher сэкономит разметку касок/респираторов».
