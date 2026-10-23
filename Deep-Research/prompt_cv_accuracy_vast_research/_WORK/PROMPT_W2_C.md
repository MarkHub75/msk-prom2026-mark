# Common researcher brief — cv_accuracy_vast
You are an independent internet researcher, gpt-6.1-sol medium, explicitly assigned through the agent tool. Read the assigned prompt completely. You may read Context-prompt.md and prompt_cv_accuracy_vast_research.md if needed. Team: five strong engineers, industrial-safety video analytics hackathon, after first checkpoint on 2026-10-23. Final neural inference MUST run on LinQ, reported server has CPU+TPU (team report, exact configuration unknown). Vast.ai 1–2 RTX 3090 24GB are only contemplated for training, no rental or spending authorized. Experts emphasized accuracy verbally; this is not an official formula and does not remove latency constraints. Case pages 5,7,13 require balanced quality, few-second alert latency, deduplication, LinQ inference with speed measurement; priority scenarios may be selected. No local training, export, benchmark or hardware execution has been performed. Do not fabricate these.
Use real internet tools (discover with ALL_TOOLS where needed), search and OPEN primary docs/papers/code; do not rely on snippets or only previous summaries. Record source URL, author, publication/version vs access date, precise locator, evidence kind, conditions, limitations. Current host date should be recorded honestly. Repository versions/commits and weights licenses must be pinned when material. A live docs page without version is not a pinned recipe. Distinguish published claims/measurements from your own observations and recommendations. No verbatim copying of sources: preserve concise paraphrases and locators respecting source word limits. Do not download large model weights or datasets. No credentials, account changes, payments, external messages, or changes outside your own assigned _WORK files. You may expand strong leads relevant to the decision. Do not spawn agents; root coordinates.
Protect split independence: train/validation/optional SELECT/lockbox, no neighboring frames or identical scenes/cameras across independence claim, no threshold/checkpoint/ensemble tuning on lockbox. A stated procedure is not a performed experiment. No invented prices, VRAM fit, runtimes, accuracy or success probabilities. Keep camera calibration, LinQ quantization, and exhaustive behavioral weights/datasets as handoffs to neighboring research.
Your completion condition is a useful substantiated decision with alternatives, failure conditions, a proposed discriminating experiment and clearly bounded unknowns; no arbitrary link quota. Write detailed Russian research with exact English literals as needed. Include: decision-first findings; technical detail; candidate/recipe/protocol comparisons where relevant; evidence records with branch-local S/F IDs; contradictions/negative findings; experiment question, inputs, procedure, metrics, artifacts, outcomes, what success does not prove; handoffs and precise open questions. Save detailed work to your assigned path. In final response give brief findings, consequences, source versions, proposed experiment, resource prerequisites without invented estimates, leakage risks, cross-cell handoffs, and file path.
Available previous reports are in sibling topic folders (datasets, evaluation, training_strategy, research_link_platform, violation_methods, video_architecture, operator_product, hackathon_strategy, market_deployment, LinQ-case-analytics-research); existence is not proof of completeness. Use as leads, verify primary evidence anew. Official raster case: ../LinQ-case-analytics-research/КЕЙС_LinQ.pdf. Root visually read all 20 pages via existing sheets. See _WORK/CASE_NOTES.md.


# Second-wave requirements
Your exact W2 assignment and linked K IDs will follow. Read CRITIC.md and the specified W1 evidence fully enough to understand the gap. Do not repeat a general survey; obtain NEW primary evidence or actively seek limiting/counterexamples. Answer the concrete missing question and identify the decision changed. Explicitly report whether each K is closed, applicability clarified, contradicted, still open, or moot. Preserve the original criticism; never rewrite history. No need to force closure of device/account/target-data questions with public search. Save your own detailed W2 file and any concise primary material under your own directory. Branch-local IDs W2-xx-S/F, source/date/version/access/locator/provenance/conditions, proposed experiments vs actual observations, handoffs. No spending, training/export/device runs, account mutation or subagents. Practical examples must be documented and unexecuted unless explicitly observed read-only metadata.

# Assignment W2-C: Detector evidence, exact weights and license scope
Exclusive output: _WORK/W2_C.md. Branch IDs W2-C-Sxx/Fxx.

## Exact task
Investigate only YOLO26s baseline, D-FINE-M challenger and YOLOX-s permissive fallback; RF-DETR alternative only if needed for a specific resolution. Compare native split/input/pretrain/train exposure/size-occlusion evidence and constraints; downgrade ranking where noncomparable. Verify primary license/model card/release scope for exact weights/backbone, lightweight availability/redirect/content-type, no large binary downloads. Separate code license from explicit/project claim/unresolved weight grants. No target superiority claims.

## Existing evidence
_WORK/W1_02.md, _WORK/W1_06.md, _WORK/W1_08.md, _WORK/W1_16.md; CRITIC.md; _WORK/CASE_NOTES.md.

## Original criticism (preserve provenance)
### K003 — Лицензия и доступность конкретных весов ещё не закрывают практический shortlist

**Приоритет / тип:** P0 до передачи/распространения; признанный, но существенный пробел.

**Материал и доказательство.** W1-02-F06 хорошо различает AGPL/Enterprise, Apache-designated RF-DETR и non-commercial DEIMv2/EdgeCrafter. Но для D-FINE/RT-DETRv2/YOLOX остаётся code LICENSE вместо полного provenance выбранных checkpoint/backbone; RTMPose-s в W1-03 имеет точный URL, но отдельный grant не установлен. Часть весов найдена лишь как авторские ссылки; бинарная доступность и содержимое не проверены. RF Large legacy/current различены, но нельзя растянуть найденный grant на произвольный variant или dependency.

**Последствие.** Команда может выбрать permissive код и получить неустановленные условия initialization, backbone или данных; либо потратить integration window на недоступный asset. С другой стороны, автоматически исключать модель лишь из-за отсутствия отдельного weight LICENSE тоже было бы необоснованно: нужен конкретный статус, а не юридическая догадка.

**Точно недостающее доказательство.** Для фактически retained весов — первичный model card/release/license scope, способ получения, revision/имя, notices и известный training lineage; какие условия прямо распространяются на веса, а какие лишь на код. Отдельно выбранный способ поставки AGPL-кандидата. Не требуется юридически доказывать разрешённость всех upstream фотографий интернета.

**Задание второй волны / закрытие.** W2-C закрывает detector weights, W2-E — один specialist. Проверить точный asset и легковесные metadata/redirect/content-type, не загружая большие бинарники без нужды; сохранить grant locators. Итоговая таблица: `explicit grant / project-level claim / unresolved / incompatible with chosen use`, без автоматического вывода «все .pth Apache». Реальный SHA256 байтов и окончательное принятие условий остаются gate получения артефакта. Нерешённый кандидат сохраняется условно, а не под видом проверенно permissive.



### K004 — Приоритет detector challengers пока основан на удобстве и общем benchmark, а не на сопоставимом evidence для доминирующей ошибки

**Приоритет / тип:** P1; пробел обоснования порядка, не обнаруженное ложное ранжирование.

**Материал и доказательство.** W1-02 назначает YOLO26s первым baseline, D-FINE-M основным challenger, RF-DETR-M альтернативой; W1-06/11 наследуют этот порядок. Таблица аккуратно разделяет dense/e2e, COCO/O365, T4/V100 и разные input. Но нет согласованного разбора сравнимых малых объектов/окклюзии для этой пары и цены родного short fine-tune. Опубликованные AP не дают оснований ожидать именно phone/PPE event improvement. W1 это признаёт; критик не превращает отсутствие собственных данных в требование уже назвать победителя.

**Последствие.** Сильная условная рекомендация может быть прочитана как технически доказанный accuracy ranking. При одном полезном challenger run команда должна понимать, почему он, а не higher-resolution/crop/label fix текущей модели, меняет нужное решение.

**Точно недостающее доказательство.** Минимальная like-for-like таблица для baseline и одного challenger: evaluator/split/input/head/pretraining/train exposure и доступные size/occlusion/domain results. Где контролируемого сравнения нет — явный `not comparable`. Нужна одна конкретная гипотеза ошибки, а не ещё десять архитектур.

**Задание второй волны / закрытие.** W2-C искать ограничивающее evidence в авторских papers/configs/ablation, особенно AP_small/разрешение/дополнительное pretraining и target adaptation. Либо подтвердить содержательное основание конкретного challenge, либо понизить его до «проверяем по инженерной удобности» и поставить перед ним spatial/data ablation. Закрытие не требует и не допускает объявить COCO ranking заводским. Финальный порядок меняется после DEV error audit, target superiority остаётся unknown до будущего опыта.

