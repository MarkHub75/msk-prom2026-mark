# AUTHOR_BRIEF — передача автору cv_accuracy_vast

Сборщик завершил доказательную базу после всех 16 W1, независимого критика и 7 W2. Нового интернета, третьей волны, субагентов, model training/export/benchmark, аренды или LinQ run не было. Следующий этап root — отдельный автор report_human_cv_accuracy_vast.md, затем редактор и сжиматель. Не создавать дополнительный финальный README/INDEX/EXPERIMENTS или аудитора.

## Файлы и навигация

- [RAW_FACTS.md](../RAW_FACTS.md): F001–F020 — выбранные интеграционные решения и ограничения; E001–E012 — предложенные эксперименты; F021–F201 — подробный нормализованный материал всех 23 веток. Детальные веса, рецепты, опубликованные числа, отрицательные результаты, условия и процедуры сохранены.
- [SOURCES.md](../SOURCES.md): S001–S290. S001 — официальный кейс и визуальные наблюдения root; S002 — исходные поручения и сообщения команды; S003 — процесс; ещё 287 карточек источников W1/W2. Повторные URL разных readings не слиты. Access 2026-10-23 отделён от publication/commit; неизвестное явно unknown.
- [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md): Q001–Q024 с причиной, местом поиска, предложенным владельцем и observable closure. Actual data/account/SDK/artifact/experiment/organizer answer разделены.
- [CRITIC.md](../CRITIC.md): исходные K001–K011 не стёрты, после них добавлены результаты всех W2 и интеграции. K006 и K011 закрыты решением, runtime prerequisites остаются адресными Q.
- [ID_MAP.md](ID_MAP.md): branch S/F → global IDs, полный section index и E/Q mapping. COLLECTOR_INDEX.json фиксирует SHA и число полностью прочитанных символов каждого входа; это provenance сборки, не model test.

Не перенумеровывать IDs. Отчёт объясняет решения и ссылается на глубину; не обязан копировать всю базу. Веточные эксперименты являются библиотекой альтернатив. Активная очередь — только F003/F017/F019.

## Логика рассказа

Начать с одного узкого сквозного проверяемого пути, где GPU помогает устранить наблюдённую ошибку. Общий COCO AP и число вариантов не равны качеству промышленных оповещений. Data/runtime/license/env gates объясняют, когда один fine-tune действительно обоснован.

**A — pretrained frontend + причинные CPU правила/FSM/пороги, без нового обучения.** Первый observable scope — лежачее состояние человека в фиксированном ракурсе, одно уведомление на продолжающийся эпизод, только при разрешённых media и пригодном frontend. Не называть это готовым распознаванием падения, неподвижности или потери сознания. Exact URFD pair — candidate для NC feasibility; видео ещё не получены/не decoded, labels отсутствуют. При непринятом NC/use или неподходящем frontend один fallback scope — person в пользовательском полигоне после получения разрешённого team video. Без media возможна только synthetic logic feasibility. Полигон не доказывает физическую опасность.

**B — один fine-tune одной baseline recipe** после human-confirmed frontend error, exhaustive TRAIN labels, независимого DEV, принятых условий weights, согласованного stack/export/runtime и отдельно разрешённой actual 3090 qualification. **C — один conditional challenger либо вторая GPU** только с ready work и измеренным резервом. Не складывать spatial, augmentation, pose, verifier, ensemble и DDP в обязательную очередь.

Measurement contract F008: timely event recall, late/missed, semantic FP на eligible camera-hour, duplicates/wrong actor, delivery latency/coverage, counts и uncertainty по независимым группам. Episode, alert и track — разные identities. Одно сообщение на ongoing episode не означает global cooldown, подавляющий второго человека. 1 FPS нельзя принять универсально: важны source interval, фаза sampling, свежие наблюдения, confirmation и полный LinQ wall time. C01–C10 проверяют evaluator/FSM, не detector quality. На curated pair FP/hour лишь описательная частота либо N/A, не factory rate.

Один data-role contract F004: **TRAIN / DEV / LOCKBOX**; optional CAL/frozen SELECT только при достаточных группах. SELECT выбирает не более двух заранее frozen whole pipelines; tuning любого knob делает его DEV. Refit — новая artifact identity, старый lockbox pass другого checkpoint не переносится. Сейчас оба предложенных clips только DEV, TRAIN пуст и independent LOCKBOX отсутствует. Feasibility не повод делить соседние кадры.

Model части F005/F006: YOLO26s — инженерная исходная точка, не target winner. D-FINE-M — условный C после label/visibility/input-pixel audit и одной spatial alternative baseline. Pose/TSM/MoViNet/SlowFast/PoseC3D не готовые causal violation weights. Есть один конкретный timm crop initialization, но он deferred; ImageNet logits не PPE/fall/phone-use классы. Объяснить proposal ceiling и отдельные обязательства второго neural node.

Vast F007/F010–F016: source-backed envelope остаётся UNRUN; public offers — timestamped snapshots; whole-offer cost/storage нельзя считать дважды. Running/stopped/loading/offline/expired/destroyed/volume различны. Immutable external archive проверяется bytes/hash/trusted load. Одна GPU — default, две только с ready work и measured joint contention. DDP не pool48GB. Native EMA recovery approximate, OOM/NaN/save repair не clean trial; неизвестные actual updates не заменяются epochs×dataset. Exact replay/controller не новый обязательный проект.

LinQ F013: delivered vendor sample → same-head floating ONNX → actual compiler/placement/parity → полный causal pipeline с реальной доставкой и замером скорости. Каждый runtime neural node получает свой gate. Геометрия/PTQ/QAT/behavioral datasets остаются отдельными темами с адресными передачами. Дать 3–5 решений до аренды и короткий порядок E001/E002/E003/E004.

## Восемь обязательных исправлений

1. **Actual Vast wheel не legacy vast.py.** F012/F196–F201, S276–S290. Реально получен CLI wheel v1.9.0, 324493 bytes, SHA256 dfa2349701a2302bdf2ea902bc0548609870da2888167883ab32eec954eed98b, entry vastai.cli.main:main, Python>=3.10. Modular copy использует argv list, **не shell=True**; unchecked returncode и StrictHostKeyChecking=no остались. Destroy имеет y/N prompt; CLI default search не включает rented=false. Explicit local:path dispatch отличается от unprefixed Unix path; native Windows pip не предоставляет rsync. Exit0 не backup. Будущие команды брать из W2-G.
2. **LinQ manual worked ResNet50 classification.** F013/F189–F195, S273–S275. yolo5s лишь tested-name p22; current tech yolo8/yolo11 тоже family claims. Exact detection fallback unknown. PDF bytes/visual не получены, full extract есть. Historical2025 environment не inventory сервера2026, TLM estimate не wall latency. Буквальный CPU neural ban не найден; policy и placement — отдельные gates.
3. **YOLO26 не COCO-only.** F005/F167–F172, S240–S254. Author recipe O365v1 pretrain150→COCO S70, не наша binary train_args inspection. Dense AP48.6/APsmall29.5 нельзя склеить с e2e AP47.8/latency. D-FINE-M COCO52.3/33.2 либо O365→COCO55.1/37.9 — разные exposure/recipes/capacity, не controlled pair. Paper и native schedules различаются.
4. **D-FINE HF grant сильнее code LICENSE, но не universal clearance.** Exact HF revision19214e91f5ce4c1e609022c38b1fc953c47404e7/dfine_m_coco.pth, 79108938 bytes, LFS SHA256 b44a7586bf490858c7b8bce9e44bd025cb88724df9a07a8deb3ae1c12e608195, model-repo Apache. Actual weights bytes не получены, GitHub/HF byte identity не проверена. Native B2 stage1 grant/init-download chain unresolved. YOLOX code Apache не checkpoint grant, issue не grant. Objects365 terms не автоматический запрет trained weights. AGPL форма поставки ещё не принята.
5. **Один timm V условный, license conflict реален.** Code Apache; exact HF card Apache против pinned project ImageNet weights notice. Итог unresolved. Initializer не готовая target3-head модель; neural temporal deferred. Native exporter dynamic-batch trap и proposed explicit adapter UNRUN.
6. **Native recovery/save может скрыть нечистый trial.** F010/F153–F159, S210–S217. OOM retry, NaN, EMA/half repair и pending accumulation. Reserved callback names не dispatch. Applied updates unknown не EMA/epochs. Proposed guard ещё не создан, negative drill/RPO не выполнены.
7. **Env source-backed, не установлен.** F007/F160–F166, S218–S239. Py3.11.9/Torch2.5.1/vision0.20.1, isolated cu124 train/CPU export, NumPy1.26.4/ONNX1.17/ORT1.20.1/OpenCV4.10.0.84. Resolver/lock/import UNRUN. D-FINE simplify store_true/defaultTrue не выключается отсутствием flag; нужен proposed static1 adapter. Torch2.6 weights_only default change — риск, не выполненный failure.
8. **Loading billing current-current conflict остаётся.** F011/F200–F201, S282–S290. Current FAQ включает loading storage, current Billing/Manage говорят no charge. Current offline exemption отделён от legacy claim. Actual Charges/units/payment unknown. Stopped storage может быть дороже running; destroy instance не delete volume. Не писать «loading полностью бесплатно».

## Идентичность retained candidates

| Роль | Identity | Ограничение |
|---|---|---|
| Baseline D | Ultralytics8.4.184@de290d865035acbfa4bb24cc88960d8b52c26e45; assets v8.4.0/yolo26s.pt; metadataSHA256646f8bc3fe0a656803d95c294f7852321748cb29d13466a1af8862e2db384a1b | AGPL/Enterprise use unaccepted, O365 lineage, actual bytes/load/device UNRUN |
| Conditional C | D-FINE@956d1709314c2c6a4df6f34de232054578a7449f; exact HF M COCO выше | Model-level grant найден; B2 scope/init chain unresolved; target superiority unknown |
| Conditional fallback | YOLOX@6ddff4824372906469a7fae2dc3206c7aa4bbaee; release0.1.1rc0/yolox_s.pth | Code Apache, weight scope unresolved; current preprocess не legacy; device-unverified |
| Deferred V | timm v1.0.22@78c3724f4545c0067d0b4d2f7df6337196be01ce; HF MobileNetV3small@1824797e7887cbec1990e4adbd6675960a36c589/model.safetensors | ImageNet1000 init, future3-head, license conflict/train/export/device UNRUN |

## Индекс глубины

| Вопрос | F-индекс | Материал |
|---|---|---|
| Metrics/matching/coverage/uncertainty | F008,F021–F029 | W1-01, COCO/ActEV/HSE/NIST |
| Detector каталог/weights/licenses/export | F005–F007,F030–F040,F167–F172 | W1-02,W2-B/C |
| Pose config/checkpoint/quality mask | F041–F047 | W1-03, deferred в A |
| Sampling/FSM/gaps/tracking/association | F009,F048–F063 | W1-04/05 |
| Fine-tune/freezing/ontology retention | F064–F069,F160–F166 | W1-06,W2-B |
| Partial labels/mining/QA/annotation budget | F070–F079,F175–F177 | W1-07,W2-D |
| Augmentation/copy-paste/domain shift | F080–F084 | W1-08 |
| Calibration/threshold/NMS/WBF/small sample | F085–F093 | W1-09; split F004 |
| Cascade/proposal ceiling/KD/bursts | F094–F099,F182–F188 | W1-10,W2-E |
| HPO/ASHA/selection/window | F100–F109,F003/F017 | W1-11 |
| Vast quotes/full cost/security | F110–F117,F196–F201 | W1-12,W2-G |
| Env/checkpoint/recovery/registry | F118–F134,F153–F166 | W1-13/14,W2-A/B |
| 1vs2 GPU/DDP/multi-node risk | F135–F144,F016 | W1-15 |
| LinQ bundle/parity/head/multi-model | F145–F152,F189–F195,F013 | W1-16,W2-F |
| Data readiness/C01–C10/phase replay | F173–F181 | W2-D,S255–S258 |

## Время, роли и freeze

Для точки завершения W2 **23.10 20:50:48 MSK** до25.10 10:00 оставалось **37ч09м12с**. Автор указывает фактическое время своей сборки отдельно и не обещает эти часы заново. F017 предлагает пять owner slots: R1 data/labels/rights, R2 evaluation/FSM/reviewer/lockbox, R3 training/Vast/artifacts, R4 LinQ, R5 product/submission/coordinator. Это **не фактически назначенные люди**.

К24.10 11:00 — один end-to-end feasibility либо записанный blocker и сужение scope. После11:00 B/C expansion только при finished incumbent, ready inputs и measured reserve. К24.10 18:00 — freeze сценария/моделей/head/правил/sampling/evaluator и прекращение optional new runs. Далее mandatory parity/LinQ/evaluation/archive/UI/README/demo/teaser/slides/submission; blocking fix получает новый ID и повтор затронутой проверки. Пока обязательный резерв неизвестен или не обеспечен, optional run не начинается. Не придумывать training-hour оценки.

Нециркулярный rental path: документальные/data/доступные local CPU export checks → отдельно разрешённая первая paid qualification actual3090 → heavy training. Не требовать measured3090 fit до первой аренды. Exact replay/controller deferred, minimum native snapshot+external receipt первый.

На выходе research нет собственных target quality/VRAM/latency/RPO, будущей цены или подтверждённого SDK path. Завершённое исследование честно отделяет evidence от будущей практики. Сжиматель сохраняет IDs, unknown, восемь исправлений и YAML front matter из общего договора. Никаких выдуманных tokenizer/compression measurements.

