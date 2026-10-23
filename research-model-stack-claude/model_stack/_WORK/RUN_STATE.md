# RUN_STATE — model_stack

Обновляется оркестратором при важных переходах. Время — MSK (UTC+3).

## Этапы
- [x] Этап 0 — план (2026-10-23 ~04:42): PLAN.md, CONTEXT.md, PROMPTS/W1-01..16.
- [x] Этап 1 — первая волна: 16 ячеек запущены одновременно ~04:43, все завершены к 05:08; сбоев и замен не было; фактические модели по самоотчётам совпали с запрошенными
- [x] Этап 2 — критик (Opus 5.5 / high, свежий контекст; самоотчёт `claude-opus-5-5`) — запуск 05:08, CRITIC.md готов (32 K, 15 предложенных заданий)
- [~] Этап 3 — вторая волна: 15 заданий W2-A…W2-O (PLAN_WAVE2.md) запущены одновременно 05:30
- [ ] Этап 4 — сборщик (SOURCES, RAW_FACTS, OPEN_QUESTIONS, дополнение CRITIC)
- [ ] Этап 5 — автор (черновик)
- [ ] Этап 6 — редактор (report_human_model_stack.md)
- [ ] Этап 7 — сжиматель (report_machine_model_stack.md)

## Ветки первой волны
| ID | Запрошено | Фактическая модель (самоотчёт агента) | Статус | Файл |
|---|---|---|---|---|
| W1-01 | sonnet / medium | Sonnet 5.5, `claude-sonnet-5-5` | готово (04:57); найден Framework_manual_H1.pdf, pytpu, linq-cv-bench — разосланы W1-10/11/12/15 | WAVE1/W1-01_FAMILIES.md |
| W1-02 | sonnet / medium | Sonnet 5.5, `claude-sonnet-5-5` | готово (04:57); ultralytics 8.4.184; изменения API export 8.4.80/8.4.142 разосланы W1-10/12 | WAVE1/W1-02_REPOS.md |
| W1-03 | sonnet / medium | Sonnet 5.5, `claude-sonnet-5-5` | готово (04:56); yolo11n.pt скачан (sha совпал), остальные .pt — data.pkl через HTTP Range + pickletools; FLASH про YOLO26 разослан W1-06/10/12/15 | WAVE1/W1-03_WEIGHTS.md |
| W1-04 | sonnet / medium | Sonnet 5.5, `claude-sonnet-5-5` | готово (04:49); 31 F, 29 S; не прочитаны: Roboflow HHW (403), PML 1.0, условия ImageNet | WAVE1/W1-04_LICENSES.md |
| W1-05 | sonnet / medium | Sonnet 5.5, `claude-sonnet-5-5` | готово (04:50); 10 .pt скачаны в SCRATCH, разобраны pickletools без десериализации; Roboflow 403 | WAVE1/W1-05_PPE_HELMET_VEST.md |
| W1-06 | sonnet / high | Sonnet 5.5, `claude-sonnet-5-5` | готово (05:06); контракты по коду; формы подтверждены через экспорты W1-10; оригинальный yolov5s.pt не экспортировался никем | WAVE1/W1-06_ARCH_INFER.md |
| W1-07 | sonnet / high | Sonnet 5.5, `claude-sonnet-5-5` | готово (04:58); локальные пробы переноса весов (yaml, random init, torch 2.9.1+cpu в SCRATCH), обучение не запускалось | WAVE1/W1-07_TRAINING.md |
| W1-08 | sonnet / high | Sonnet 5.5, `claude-sonnet-5-5` | готово (04:58); аудитор датасета (синтетика, 12 дефектов) в W1-08_files | WAVE1/W1-08_DATA_CONTRACTS.md |
| W1-09 | sonnet / medium | Sonnet 5.5, `claude-sonnet-5-5` | готово (05:05); установлен torch 2.14.1+cu126 в SCRATCH (venv-gpu 4,3 ГБ), CUDA на RTX 4070 работает; экспорт yolo11n/26n из yaml (random init) | WAVE1/W1-09_ENVIRONMENTS.md |
| W1-10 | opus / medium | Opus 5.5, `claude-opus-5-5` | готово (05:03); 23 экспорта (ultralytics 8.4.184, torch 2.14.1+cpu, onnx 1.23.2, ORT 1.31.0) + cut-графы; .onnx только в SCRATCH (непереносимы, скрипты в W1-10_files) | WAVE1/W1-10_EXPORT_ONNX.md |
| W1-11 | sonnet / high | Sonnet 5.5, `claude-sonnet-5-5` | готово (05:08); прогоны PT vs ONNX на CPU (bus, zidane), fake-quant выхода; кириллица PDF не извлеклась | WAVE1/W1-11_PRE_POST.md |
| W1-12 | opus / medium | Opus 5.5, `claude-opus-5-5` | готово (04:58); прочитан Framework_manual_H1.pdf; ORT static-quant эксперимент (сторонний runtime) — полный int8 обнуляет скоры, разрезанная голова сохраняет | WAVE1/W1-12_QUANT_LINQ.md |
| W1-13 | sonnet / high | Sonnet 5.5, `claude-sonnet-5-5` | готово (04:57); P1–P5 конфигурации; использовал выписку W1-12 из vendor-презентации (оригинал PDF не открывал) | WAVE1/W1-13_CASCADES.md |
| W1-14 | sonnet / high | Sonnet 5.5, `claude-sonnet-5-5` | готово (05:02); выписки даташитов HX/HPS; MDPI/CVPRW 403 | WAVE1/W1-14_METRICS.md |
| W1-15 | opus / medium | Opus 5.5, `claude-opus-5-5` | готово (04:59); маршруты R1–R6, противоречия C1–C12; ckpt метаданные stub-анпиклером; мануал LinQ — по выписке W1-12 | WAVE1/W1-15_E2E_CHAINS.md |
| W1-16 | sonnet / medium | Sonnet 5.5, `claude-sonnet-5-5` | готово (04:50); Kaggle/IEEE DataPort/Roboflow не открылись — только выдержки поиска | WAVE1/W1-16_PPE_RESP_SMOKE_ZONE.md |

## Журнал межветочных передач
- 05:0x: оркестратор разослал FLASH из W1-03 (YOLO26 end2end в assets v8.4.0; урезанные .pt; различие одноимённых .pt HF/GitHub; ONNX Model Zoo ↔ список LinQ) → W1-06, W1-10, W1-12; сводку W1-03/04/05/16 → W1-15.
- 04:57: FLASH из W1-01 (Framework_manual_H1.pdf, pytpu 15.0.24, linq-cv-bench) → W1-10, W1-11, W1-12, W1-15; FLASH из W1-02 (API export 8.4.x) → W1-10, W1-12.

## Наблюдения оркестратора о среде (local_observation)
- 04:58: на машине, где выполняется research, `nvidia-smi` → NVIDIA GeForce RTX 4070, 12282 MiB, driver 610.88; ОС Windows 10 Pro 10.0.19045. CUDA toolkit/torch-CUDA не проверялись. Совпадает ли эта машина с «ПК команды с RTX 4070» — не установлено (вероятно, но не подтверждено пользователем).
- 05:03: примечание для сборщика — W1-07 использовал torch 2.9.1+cpu, W1-10 — torch 2.14.1+cpu (разные venv); версии указывать для каждого наблюдения отдельно.
- 05:05: для сборщика — W1-09 называет commit e6d5fc5 для 8.4.184 (это SHA main по W1-02), W1-02/07/08/10 — tag commit f7dd275e; нормализовать.

## Ветки второй волны (запрошено; фактическая модель — по самоотчёту)
| ID | Запрошено | Фактическая модель | Статус | Файл |
|---|---|---|---|---|
| W2-A | sonnet / medium | — | запущено | WAVE2/W2-A_LINQ_PUBLIC.md |
| W2-B | sonnet / high | — | запущено | WAVE2/W2-B_VENDOR_CODE.md |
| W2-C | opus / medium | — | запущено | WAVE2/W2-C_TF_PATH_SDK_ENV.md |
| W2-D | sonnet / high | — | запущено | WAVE2/W2-D_FIRST_HOUR_KIT.md |
| W2-E | opus / medium | — | запущено | WAVE2/W2-E_INT8_SURROGATE.md |
| W2-F | sonnet / high | — | запущено | WAVE2/W2-F_REAL_FINETUNE.md |
| W2-G | sonnet / high | — | запущено | WAVE2/W2-G_YOLOV5_ANCHOR.md |
| W2-H | sonnet / high | — | запущено | WAVE2/W2-H_VENDOR_FALLBACK.md |
| W2-I | sonnet / high | — | запущено | WAVE2/W2-I_CROP_CLASSIFIER.md |
| W2-J | sonnet / medium | — | запущено | WAVE2/W2-J_TERMS_VERBATIM.md |
| W2-K | sonnet / medium | — | запущено | WAVE2/W2-K_DATA_AUDIT.md |
| W2-L | sonnet / high | — | запущено | WAVE2/W2-L_SMALL_OBJECTS_MEMORY.md |
| W2-M | sonnet / medium | — | запущено | WAVE2/W2-M_HOST_BUDGET_TRACKER.md |
| W2-N | sonnet / high | — | запущено | WAVE2/W2-N_OP_REPLACEMENT_MAP.md |
| W2-O | sonnet / medium | — | запущено | WAVE2/W2-O_OV_TEACHER.md |
