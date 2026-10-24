# Источники и границы технических утверждений

Проверено **24 октября 2026, 08:12–08:20 МСК; повторно после последнего полного `git fetch origin` в 08:28 МСК**. Факты сверены по Git, текущему коду, сохранённым отчётам и первичным JSON. Новых запусков TPU и повторного запуска ML/backend-тестов при подготовке презентации не было. Время окончательной браузерной съёмки, точный frontend SHA и действия — в [frontend-evidence.md](research/frontend-evidence.md) и [manifest PNG](research/screenshots-manifest.json).

## Проверенные состояния Git

| Ветка | Зафиксированный commit |
|---|---|
| main | `353c7f966a67c0797dbe88ec8f8eb99f6465f582` |
| matvey_cv | `1bdeeafcd74a696999cfd4af28c2ea598e3fe8f2` |
| demo/checkpoint | `9f652236589698857ba05eabbcf361b4ab3779b2` |
| front/control-room | `8161719d687083c7a3578b0f5de8bc2043a95ce1` |
| codex/safewatch-frontend-v1 | `2d19a40a1d467bc6713eb6267e93d8cefb83c8a5` — предыдущая итерация, не источник новых скриншотов |

Каждый сохранённый source blob имеет commit, Git blob ID, SHA256 исходника и SHA256 снимка в [source-index.json](research/source-snapshots/source-index.json). В выдержках сохранены оригинальные номера строк. Сетевые и credential-строки LinQ намеренно не копировались.

## Утверждения на слайдах

| Слайд / утверждение | Проверяемый источник и локальный снимок | Граница утверждения |
|---|---|---|
| 1. Продукт и пять ролей | main `tech.md` §2, L28–42; [выдержка](research/source-snapshots/main__tech.md.excerpt.txt) | Роли и целевой процесс; не готовность всех пяти рабочих мест |
| 2. Файл → LinQ Jupyter → TPU → JSONL → CPU → эпизоды → серверный эфир → WS → люди | main `tech.md` §2,8.4–8.8; [выдержка](research/source-snapshots/main__tech.md.excerpt.txt) | Архитектура анализа записи и эмуляции; не live RTSP |
| 2. Контракт-first, заменяемый frontend | main `tech.md` §8.15; [OpenAPI](research/source-snapshots/main__contract__openapi.json), [WS-схема](research/source-snapshots/main__contract__ws.schema.json) | Наличие маршрута в контракте не означает реализацию; незакрытые слайсы дают501 |
| 3. Baseline YOLOv8n / YOLOv8n-pose выполнены на TPU | **`21b245555e544ad5b92ae6128ae0773adf7478b6`**, `docs/linq/LINQ_CONTRACT.md` L75–92; [выдержка](research/source-snapshots/main__docs__linq__LINQ_CONTRACT.md.excerpt.txt) | Отдельный smoke baseline; не все собственные модели и не стабильность интегрированного backend |
| 3. 400 кадров за19с, ≈21кадр/с,31с с загрузкой | `results/linq_smoke/synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json`; [первичный JSON](research/source-snapshots/main__results__linq_smoke__synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json) | Точно:400/400,19.09с,20.95FPS,total31.0с,inflight8. Разрешение1280×720 указано в LinQ contract. Тестовый COCO-ролик, не производственная камера |
| 3. Recall/IoU — сохранность после квантования | `det640_cut_ap9999.json` summary: recall .9068362193,IoU .9307762455; `pose640_cut_ap9999.json`:recall .9375; [det](research/source-snapshots/main__results__linq_smoke__det640_cut_ap9999.json.excerpt.txt), [pose](research/source-snapshots/main__results__linq_smoke__pose640_cut_ap9999.json.excerpt.txt) | Сравнение с исходной FP32, не точность промышленных нарушений.21FPS — throughput записи, не event-to-alert latency |
| 3. Интегрированный backend пока нестабилен | main `progress.md` L17–24 и R5 log; [снимок](research/source-snapshots/main__progress.md) | Более поздний R5: TPU timeout120с,0кадров,0–1consumer; успешный отдельный smoke не отменяется |
| 4. ONNX, CPU/CUDA FP32↔ONNX, SDK2026.9.45 TPU_H1M | matvey_cv `docs/STATUS.md` L8–13 и `docs/validation/2026-10-23.json`; [STATUS](research/source-snapshots/matvey_cv__docs__STATUS.md) | `atol=rtol=1e−3` на одном smoke-кадре; не абсолютная гарантия ошибки≤1e−3 на любых данных |
| 4. Собственные Helmet/Split-Pose имеют реальные ответы LinQ | matvey_cv `ml/RELEASE_MANIFEST.json` L73–76,L177–180; [manifest](research/source-snapshots/matvey_cv__ml__RELEASE_MANIFEST.json), [свежий EVAL_REPORT](research/source-snapshots/matvey_cv__ml__EVAL_REPORT.md) L42–46 | Сохранены коррелированные status0-captures; raw-тензоры находятся вне этого checkout. Аудит презентации не повторял вызовы |
| 4. Исправление pose confidence и аппаратная проверка | SDK simulation в STATUS L12–13; позже [pose-linq-ur01-parity.json](research/source-snapshots/matvey_cv__ml__reports__pose-linq-ur01-parity.json) | Split-выходы сохраняют confidence; на11входах аппаратные данные совпали с SDK reference. Это не устранение всей PTQ-потери относительно FP32 |
| 4. 335 программных тестов PASS | [EVAL_REPORT](research/source-snapshots/matvey_cv__ml__EVAL_REPORT.md) L54; [PROGRESS](research/source-snapshots/matvey_cv__ml__PROGRESS.md) L5,L31; manifest L238–243 | Итоговый сохранённый отчёт; software checks, не измерения качества CV |
| 4. Единственное падение URfall01 пропущено | EVAL_REPORT L34,L44; [latest RESUME](research/source-snapshots/matvey_cv__RESUME.md.excerpt.txt) |11реальных status0-ответов,TP0/FP0/FN1 на одном development clip. Исполнение модели не означает готовое качество нарушения |
| 5. Backend прошёл S10 и R10, следующий S11 | main [progress.md](research/source-snapshots/main__progress.md); [services.py](research/source-snapshots/main__src__safewatch__services.py.excerpt.txt) | В R10 исправлено сохранение extra-артефактов при recompute; остаются другие долги. ЖурналS12,statsS13,evalS14,deliveryS15 ещё NotImplementedError |
| 5. Правила и ограничения сценариев | main rules modules; [plugin gating](research/source-snapshots/main__src__safewatch__rules____init__.py), [model registry](research/source-snapshots/main__config__models.yaml), [load_carrying skeleton](research/source-snapshots/main__src__safewatch__rules__load_carrying.py) | Логика синтетически проверена; огонь/привязь/подвешенный груз требуют моделей. Перенос груза — skeleton. Каска matvey_cv ещё не подключена в main |
| 5–6. Актуальная диспетчерская, Incident Focus, мастер и журнал | [frontend-evidence.md](research/frontend-evidence.md), [browser raw](research/frontend-capture-raw.json), [SHA256 PNG](research/screenshots-manifest.json) | Настоящий frontend; конечная съёмка привязана к последнему SHA в этих отчётах. Камера и evidence внутри интерфейса синтетические |
| 5. Свежий smoke мока30/30 | [smoke-mock-fresh.json](research/smoke-mock-fresh.json) | PASS30/FAIL0/SKIP0;26REST и32WS по схемам. Это не smoke настоящего backend и не LinQ |
| Дополнительная проверка backend без TPU | demo9f652236 [WATCH_LOG](research/source-snapshots/demo-checkpoint__tools__checkpoint-demo__WATCH_LOG.md), [last-real.json](research/source-snapshots/demo-checkpoint__tools__checkpoint-demo__watch__last-real.json) | Watch08:11 по main2f6e097c:PASS24/FAIL1(жёлтое сценыG9)/SKIP4. Красное→мастер→resolved и историяPASS; журнал501; autoescalation45,2сPASS. Детекции синтетические, хвосты ONNX в scratch — заглушки |
| 7–8. Открытые задачи и вопросы LinQ | main progress open; matvey_cv EVAL_REPORT/PROGRESS/RELEASE_MANIFEST; LinQ contract §8 | Качество Fall NOT_ACCEPTED, независимый test NOT_RUN, event-to-alert и false-alerts/camera-hour не измерены; chip-only timing неизвестен |

## Что обновили и что убрали

- Старые `docs/STATUS.md`/portable-kit113 и own-model NOT_RUN **не использованы как текущий итог**. Более свежие Git-источники подтверждают реальные Helmet/Split-Pose ответы и335softwaretests.
- «Запустить собственные модели на TPU» обновлено до их интеграции и квалификации в общем конвейере. Конкретные промышленные Precision/Recall не заявляются.
- Не заявлены «точность91%»,21FPS времени тревоги, ноль ложных тревог, работа на заводских live-камерах, все модели на LinQ, эффективность/окупаемость и автоматическая остановка оборудования.
- Не заявлена готовность настоящего backend-журнала. Демонстрация operator→master→journal относится к stateful-моку.
- Старые скриншоты HRE заменены новой съёмкой актуального `front/control-room`.
- После второго fetch: R10 закрыт, ближайший этапS11; старый долг extra/recompute убран из открытых. Новых успешных интегрированных TPU-прогонов не появилось.
- Автоэскалация45с не вынесена на слайд: в backend default включена, в проверенном demo-runtime выключена. Новое независимое от презентационной съёмки watch-свидетельство фиксирует backend-передачу за45,2с. Поведение и источники описаны в [полном аудите](research/technical-evidence.md).

Все8смысловых блоков и отрицательные результаты разобраны подробно в [technical-evidence.md](research/technical-evidence.md). Синтетические демонстрационные кадры и сгенерированные промышленные иллюстрации не являются записями камер и не используются как доказательство качества нейросети.
