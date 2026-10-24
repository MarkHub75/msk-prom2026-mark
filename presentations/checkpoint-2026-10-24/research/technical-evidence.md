# SafeWatch: проверка технических утверждений для checkpoint

Проверка: 24.10.2026, первоначально 08:12–08:20 МСК; повторная сверка после последнего полного `git fetch` в 08:28 МСК. Метод: read-only `git show`, история Git и сопоставление первичных JSON с текущими отчётами. Новых TPU-запросов, обучения, изменений продукта или повторного запуска его тестов в этом аудите нет. Снимки проверенных исходников и SHA256: [source-snapshots/source-index.json](source-snapshots/source-index.json). Эти снимки — источники презентации, а не новые результаты испытаний.

## Фиксация состояния после fetch

| Ветка | Проверенный commit | Значение |
|---|---|---|
| `origin/main` | `353c7f966a67c0797dbe88ec8f8eb99f6465f582` | 24.10 08:18 МСК, R10 закрыт, следующий S11, tech v3 |
| `origin/matvey_cv` | `1bdeeafcd74a696999cfd4af28c2ea598e3fe8f2` | 23.10 23:48 UTC / 24.10 02:48 МСК, frozen quality checkpoint |
| `origin/demo/checkpoint` | `9f652236589698857ba05eabbcf361b4ab3779b2` | 24.10 08:15 МСК, новый watch 08:11 по main S10; red/master/autoescalation проверены |
| `origin/front/control-room` | `8161719d687083c7a3578b0f5de8bc2043a95ce1` | 24.10 08:22 МСК; новые role tabs, journal period/filter/print, свежая съёмка — отдельный frontend audit |
| `origin/codex/safewatch-frontend-v1` | `2d19a40a` | Предыдущая UI-итерация; не источник актуальных скриншотов |

## Главные изменения относительно исходного задания

1. **`matvey_cv:docs/STATUS.md` устарел.** Его 113 тестов и `own_model_hardware_inference=NOT_RUN` в старом kit заменены более свежими `ml/PROGRESS.md`, `ml/EVAL_REPORT.md`, `ml/RELEASE_MANIFEST.json`, верхним разделом `RESUME.md`. Сейчас собственные Helmet и Split-Pose имеют сохранённые коррелированные ответы LinQ `status0`; итоговый отчёт фиксирует **335 программных тестов PASS**. Не писать, что собственные модели ещё не исполнялись на TPU.
2. Это **не подтверждает качество обнаружения нарушений**. Свежий отчёт явно: Fall quality `NOT_ACCEPTED`, независимый финальный тест `NOT_RUN`. На одном URfall01 аппаратный прогон дал 11 ответов, но пропустил одно эталонное падение. Не превращать факт выполнения модели в готовый recognizer.
3. `main` прошёл S10 и **R10**, следующий S11. В R10 исправлено сохранение extra-артефактов при recompute, параметры правил берутся из снимка; долг S10 больше не открыт. Журнал S12 и статистика S13 ещё заглушки. Сценарии S10 частично реализованы как правила и синтетические проверки; для огня/привязи/подвешенного груза нет подключённых классов моделей. Перенос груза — skeleton.
4. Проверенные baseline-результаты `21b24555` сохраняются. Более поздний R5 в интегрированном backend не получил ответ TPU; очередь 0–1 consumers остаётся открытой проблемой. Одно не отменяет другое: отдельный smoke работал, стабильный интегрированный прогон пока не доказан.

## Слайд 1 — продукт и роли

Источник `main:tech.md` L28–42. Архив/эмуляция потока: загрузка видео, нейросети внутри LinQ Jupyter, кэш детекций, эпизоды, оповещения и доказательства. Пять ролей L32: оператор/диспетчер, мастер смены, охрана труда, менеджмент, IT/администратор. Работник у станка интерфейсом не пользуется.

Безопасная формулировка: **«Оператор проверяет опасные события; мастер реагирует; охрана труда анализирует журнал»**. Последняя часть — роль/целевой процесс; актуальный real backend журнала ещё S12, демонстрационный журнал на моке.

## Слайд 2 — архитектура и различие действий

Источники `main:tech.md` L30–34, L2901–2985 и L3056–3060; `contract/openapi.json`, `contract/ws.schema.json`. Поддерживается схема: файл → LinQ Jupyter → TPU модель → JSONL кэш → CPU tracking/rules → episode → серверный эфир → WS → оператор → мастер → история действий. Это анализ записи и эмуляция эфира, **не RTSP реальных заводских камер**.

Одно продолжающееся нарушение — эпизод; повышение жёлтого до красного сохраняет эпизод (L2911), идемпотентность публикации по `pub_key` (L2927,L2932). Отдельные циклы replay намеренно создают новые события; тезис «одно нарушение — одно оповещение» не означает отсутствие повторов при повторном проигрывании ролика.

Действия L2944–2952: `view` только просмотр; `confirm` жёлтого → confirmed; красного → две записи confirmed и sent_to_master; `send_to_master` отдельное действие; мастер `accept`, затем `resolve` с обязательными мерами. Поэтому «подтверждение / передача / устранение» различаются даже когда красный confirm технически сразу инициирует передачу.

Контракт-first: OpenAPI и WS JSON Schema заморожены; типы frontend генерируются; продуктовая логика в backend; frontend заменяемый по той же границе. Отдельный stateful-мок имеет REST+WS и переходы состояний; обычный Prism stateless его не заменяет.

Прочитаны реальные JSON-контракты: OpenAPI `SafeWatch API`1.0.0,42paths (не число готовых маршрутов); действие `/api/events/{event_id}/actions` получает `ActionIn`, отдаёт `EventDetail`/ApiError, роль X-Role. WS — объект WsMessage с типами/payload-схемами в $defs; это отдельная от OpenAPI схема. Наличие маршрута в контракте не доказывает его реализацию: незакрытые слайсы возвращают501.

**45 секунд:** `main:config/default.yaml` L149–152: enabled=true, timeout_s=45, tick_ms=500. `main:services.py` L1638–1653 реализует передачу мастеру; `tech.md` L2961–2968: красное new/viewed/confirmed без решения оператора после red_at; просмотр решением не считается; пометка «Не подтверждено оператором». Тесты границы существуют `tests/test_escalation.py`. Свежий `demo:watch/last-real.json` и WATCH_LOG 08:11/08:20 подтверждают реальную backend-эскалацию за **45,2с** на синтетическом событии. В stateful-моке по умолчанию **выключено**, включается `--escalation`/SW_MOCK_ESCALATION=1 (`demo:GAPS.md` A15). Поэтому на компактной архитектуре число лучше опустить либо подписать «backend default; mock — отдельный флаг». В пользовательской среде config/user.yaml не прочитан, фактическое переопределение неизвестно.

## Слайд 3 — LinQ baseline на TPU

Ключевой commit **`21b245555e544ad5b92ae6128ae0773adf7478b6`**, 24.10 02:46:32 МСК. Результат `main:docs/linq/LINQ_CONTRACT.md` не менялся после него; последующие изменения tools/linq — диагностика R5 и --nc S10, без нового успешного baseline-замера.

| Показатель | Подтверждение | Формулировка |
|---|---|---|
| YOLOv8n 640 и YOLOv8n-pose 640 скомпилированы и исполнялись на TPU | LINQ_CONTRACT L79–87; compile_reports/*; `det640_cut_ap9999.json`, `pose640_cut_ap9999.json` | «Baseline-модели выполнены на TPU» |
| 400 кадров, 1280×720, около 19 с | raw `synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json`: frames_total=400, frames_processed=400, wall_s=19.09; разрешение в LINQ_CONTRACT L86 | «400 кадров за 19 с» |
| около21 кадра/с | тот же raw: throughput_fps=20.95 | «≈21 кадр/с обработки тестовой записи» |
| с загрузкой31с | raw end_to_end_s upload=6.9, remote_run_incl_poll=22.2, total=31.0 | «31 с вместе с загрузкой» |
| Detector recall0.91, IoU0.93 | raw summary mean_recall_vs_cpu=.9068362193, mean_iou=.9307762455; contract L75,L82 | Только «сохранность относительно FP32 после квантования» |
| Pose recall0.94 | raw pose summary mean_recall_vs_cpu=.9375; contract L85 | То же сравнение с FP32, не pose/violation accuracy |
| Один Jupyter запрос162мс; пре/пост4+3мс; обмен≈19мс/МБ | LINQ_CONTRACT L92 | В notes, как задокументированные smoke-результаты, без chip-time claim |

Важная настройка: именно raw detector video-run использовал **inflight=8**, хотя дальнейшая рекомендация/интеграция uses4. Не приписывать21FPS конфигурации inflight4. Исходная запись `synthetic_coco_40x1s.mp4` — тестовый ролик на основе COCO, не промышленное видео и не камеры завода.

**Обязательные подписи:**

- «Показатели recall/IoU относятся к сравнению с исходной моделью при квантовании, а не к точности обнаружения нарушений на производстве».
- «21 кадр/с — пропускная способность обработки тестовой видеозаписи, а не время доставки тревоги оператору».

**Позднейшее ограничение:** `main:progress.md` L17–24 и R5 log: Jupyter/backend_check доступен,2/2 программы видимы, загрузка/старт воркера прошли, но TPU timeout120с,0 кадров; очередь `input`0–1 consumer, при smoke было16. Стабильный общий конвейер с TPU ещё не подтверждён; причина в среде предположена командой, этим аудитом не установлена.

## Слайд 4 — собственные модели: свежая доказательная цепочка

**Рекомендуемый заголовок:** «Собственные модели уже выполнились на LinQ». Не смешивать их с YOLO baseline21FPS.

| Стадия | Подтверждение | Ограничение |
|---|---|---|
| Каска и pose экспортированы в static ONNX | `matvey_cv:docs/STATUS.md` L8; `docs/validation/2026-10-23.json` содержит hashes и paired reports | Одна paired smoke-картинка |
| CPU/CUDA FP32 vs ONNX проходят atol=rtol1e−3 | те же sources, паритетные JSON | Не универсальный максимум абсолютной ошибки всех тензоров/входов |
| Оба графа TPU_H1M O1, SDK2026.9.45 | STATUS L9 и compile reports с hashes в validation; RELEASE_MANIFEST содержит TPU artifacts | Компиляция сама по себе не запуск |
| Mixed-pose confidence bug исправлен split outputs | STATUS L12–13: исходный кандидат REJECTED; float split bit-identical на smoke image; SDK simulation сохраняет confidence | Это сначала был SDK-only результат; позже есть hardware evidence |
| Helmet и Split-Pose реально исполнялись | `ml/RELEASE_MANIFEST.json` L73–76,L177–180: CORRELATED_STATUS0_CAPTURES; `RESUME.md` latest и `ml/EVAL_REPORT.md` L42–46 | Raw captures находятся вне Git `/workspace/artifacts/linq-rpc/…`; этот аудит проверяет сохранённые отчёты и hashes, не делает live rerun |
| Новый Split-Pose TPU прогон | `ml/reports/pose-linq-ur01-parity.json`:11 paired frames,9 matched people, equal counts, score/box/keypoint-confidence diff0; status11correlated status0 | Один URfall development clip; модель выполнилась, но падение пропущено |
| 335 software tests PASS | `ml/EVAL_REPORT.md` L54, `ml/PROGRESS.md` L5,L31, RELEASE_MANIFEST L238–243; reported5.851s | Не335 измерений качества и не только тесты правил; локальный test-log вне Git, в этой сессии не запускался |

**Крупная оговорка:** «Исполнение на TPU подтверждено. Качество распознавания нарушений — открытый гейт». Допустимо компактно: «URfall01:11 ответов TPU; падение пропущено». Так не скрывается отрицательный результат.

Заметки докладчика по свежему ML checkpoint:

- Helmet fixed quality-v3:52 development изображения,44 complete/class, AI review без независимого human expert; установлен overlap с upstream pretraining source. Helmet P.6333/R.76, bare_head P.7667/R.71875 — **object-box diagnostics**, не качество нарушений/владельца каски. В основные слайды цифры не нужны.
- Fall:20 URFall development clips,3274original-PTS frames,10 source-reference fall episodes. Native full cadence TP0/FP0/FN10; matched2FPS225frames TP1/FP0/FN9, recall.10/F1.1818. Разная частота выборки не является улучшением. GT coarse/sampled AI-reviewed; prolonged-lying positive support0, поэтому его recall undefined.
- Реальный TPU URfall01:11unique correlated status0 replies,0events,1miss;131.018с,processedFPS.083958,RPCp50=10.630с/p95=18.967с. Это transport-inclusive RPC при concurrency1, **не время непосредственно на чипе и не сравнимый benchmark с baseline21FPS**. На слайд можно не выносить timing; полные параметры остаются здесь и в notes.
- Две семьи гипотез Helmet/Fall не дали нужного улучшения; baseline сохранён frozen с improvement=false; Fall quality NOT_ACCEPTED. Новая PTQ-калибровка не promoted, кандидат на LinQ не запускался — это не опровергает запуск исходных собственных Helmet/Split-Pose.
- Running/Zone в matvey_cv — offline UNVALIDATED_PROTOTYPE, без реального GT/полигонов NOT_EVALUATED/null. Это отдельная ветка от main rules S10.
- Сохраняется independent final test NOT_RUN и неизвестна delivered-alert latency. Старое113/NOT_RUN — историческая стадия, а не текущий статус.

## Слайд 5 — матрица готовности

| Группа | Безопасный статус сейчас | Источник |
|---|---|---|
| Backend: upload/queue/cache, tracking/episodes, replay/WS, action transitions/master, zones/calibration | «Работает на синтетике; LinQ-интеграция нестабильна» | main progress S0–S10, реализованные services/tests; R5 долг |
| OpenAPI + WS schemas | «Работает: контракт зафиксирован» | contract files, tech8.15 |
| Бег/падение | «Правила на синтетике» | main rules/running.py,fall.py; S5 log. Stateful demo работает, real fake-scene жёлтое сейчас G9 FAIL |
| Сближение, телефон, ограждение, зона под грузом | «Правила на синтетике» | S10 log/tests, rules modules; default model classes person/car/bus/truck/train/cellphone имеются |
| Огонь/дым/курение, отсутствие привязи, подвешенный груз | «Правила на синтетике; модели не подключены» | rules/__init__.py L45–62 gating; config/models.yaml только COCO baseline+pose; pipeline.extra=[] |
| Перенос груза | «В работе» | rules/load_carrying.py L1,L16,L23–27: skeleton/empty observe |
| СИЗ: каска | «Модель выполнена на TPU; интеграция/качество открыты» | matvey latest manifest/scenarios; в main model registry каски нет |
| Frontend actions + journal | «На моке» до конкретного browser подтверждения frontend-агента | current control-room + isolated stateful mock |
| Real backend journal/filter/CSV | «В работе» | services.py L1951–1960 raises slice12 |
| Real stats/eval/webhook delivery | «В работе» | services.py L1963–1982 raises slice13–15 |
| Демо-контур smoke | «На моке: свежий PASS30/FAIL0/SKIP0» | research/smoke-mock-fresh.json,26REST/32WS по схемам; не LinQ/backend smoke |

**Обновление R10:** долг S10 по recompute extra **закрыт**. `AnalysisConfig.extra_artifact_ids` хранится в config_json; `_analysis_inputs` читает сохранённые extra-артефакты, а расширенный `test_extra_model_enables_fire_without_code` проверяет новую версию анализа без новых inference-запусков. Это программная проверка, не доказательство качества fire-модели или её подключения в default-конфигурации. S11–S15 не помечать готовыми по плану: в main на snapshot nextS11. HUD для pair/zone/fire и другие оговорки перенесены в R15.

## Слайд 6 — живая демонстрация

Для требуемых трёх шагов подходит **изолированный stateful-мок**, не real backend synthetic replay. В real fake-сцене main G9 нет жёлтого бега, красное — «Человек лежит неподвижно10с», а journal501. В моке yellow running → confirm → red fall → focus/evidence → confirm/sent_to_master → mobile accept → resolve с мерами → journal есть; актуальный вид и действия подтверждаются новым frontend browser evidence.

Обязательная видимая подпись: **«Демонстрационные данные. Кадры синтетические. Рамки размечены вручную»**. Не выдавать ручной score1.0 bbox за уверенность модели. Снимки synthetic evidence показывают UI, не качество CV.

`demo:WATCH_LOG.md`07:55 исправляет ложные failures07:45: за90с ожидания жёлтого backend autoescalation45с уже передавал старое красное мастеру; smoke теперь ждёт свежееevent.created. **Свежий watch08:11 по main2f6e097c:** PASS24/FAIL1(yellowG9)/SKIP4, первичный `watch/last-real.json` теперь актуален и совпадает с correction. Красный takeover, подтверждение, master accept/resolve и полная история действий — PASS; журнал `/api/events` — SKIP501. Дополнительный PASS — автоэскалация45,2с. Контракт24REST/141WS без расхождений; это не число проверок fresh mock. Watch также фиксирует e2e front/control-room7d218abb10/10, но после последнего fetch фронт8161719d снимается заново отдельным frontend-агентом; только его новый отчёт определяет происхождение окончательных PNG.

## Слайды 7–8 — оставшаяся работа и вопросы

Обновить «запуск собственных моделей» на **«Интеграция собственных моделей в общий backend-конвейер и квалификация на целевых видео»**, так как их TPU execution уже есть. Остальное: стабильный интегрированный LinQ прогон; независимый размеченный test и эпизодные P/R; ложные тревоги на камеро-час; event-to-notification latency; оставшиеся сценарии/extra/recompute и журнал.

Вопрос очереди остаётся актуальным в более позднем main R5: «Как обеспечить стабильную обработку очереди при0–1 активном обработчике?» Можно сохранить общий вопрос о стабильности, подробность0–1vs16 в notes. Честное chip-time также открыто: LINQ_CONTRACT L92,L128 отвергает worker.inference_time как достоверную метрику.

Четыре вопроса: (1) какое подтверждение LinQ примет жюри; (2) какие стадии обязаны идти на TPU; (3) как стабилизировать очередь и доступность обработчиков; (4) как измерить непосредственно TPU execution time. Не называть335 tests или21FPS доказательством правильности всех сценариeв.

## Что намеренно не заявляем

- Точность91%, заводские live-камеры, все модели на LinQ, отсутствие ложных тревог, снижение травматизма/окупаемость/автоостанов станков.
- Что собственные модели только скомпилированы/не выполнялись: это уже опровергнуто свежими Git-источниками.
- Что113 — актуальный итог тестов; что335 — качество CV.
- Что hardware PASS означает accurate Fall. Negative development evidence сохранено.
- Что21FPS baseline — latency alerts, chip-only timing, throughput своих моделей или гарантированная скорость текущего интегрированного backend.
- Что real journal/backend demo полностью готовы: эти функции на текущем snapshot различаются между main и stateful-моком.


## Правка r3 по запросу владельца

Проверено 2026-10-24T09:10:24.495622+03:00. Текущие refs: main `b4fb994c63f3ce187d22491080f75ffac37797c3`, front/control-room `1b8822ef86e7d5540967e73e9e4c606e926d01c1`, demo `053683dadd65d15b1d2b9df9ee5ba8ef382ad025`. В слайде оставлена запрошенная основа S0–S11; свежий progress уже продвинулся дальше. Устаревшие заявления о неготовом журнале сняты. Новые численные метрики не добавлялись.

IVA CV поддерживает LinQ(TPU) по официальной [странице платформы](https://ivacv.ru/platforma/). «Ближайший конкурент» — позиционирование команды из запроса владельца, не измеренный рейтинг. Перечень отличий не означает отсутствие аналогичных функций у конкурента.

Снимки: текущий Premiere-скин, быстрые действия и сводка смены; frontend http://localhost:5173, мок4010/4011; reset → next → next --force. Источники новой готовности: [r3 source-index](research/revision-r3/source-index.json). Предыдущие разделы ниже/выше описывают историческую ревизию и не подменяют этот актуальный update.
