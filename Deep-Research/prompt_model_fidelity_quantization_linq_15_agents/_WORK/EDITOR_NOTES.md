# Редакторская передача human-отчёта

Редакторский этап завершён 2026-10-23 23:52:44 Europe/Moscow (20:52:44 UTC). Созданы только [report_human_model_fidelity_quantization.md](../report_human_model_fidelity_quantization.md) и этот служебный файл. Новых сетевых свидетельств, субагентов, установки/импорта SDK, model/export/import/PTQ/QAT/compiler/device/quality запусков не было. Это литературная и структурная редактура согласованного этапа, без новой исследовательской или финальной технической ревью-волны.

Входы: оба договора [Context-prompt.md](../Context-prompt.md) и [тематический промпт](../prompt_model_fidelity_quantization_linq_15_agents.md), [PROMPT_EDITOR](PROMPT_EDITOR.md), [DRAFT_HUMAN](DRAFT_HUMAN.md), [AUTHOR_NOTES](AUTHOR_NOTES.md), [AUTHOR_HANDOFF](AUTHOR_HANDOFF.md), [SYNTHESIS_REQUIREMENTS](SYNTHESIS_REQUIREMENTS.md), четыре доказательных реестра. Полные тексты прочитаны строгим UTF-8; редакторское сопоставление содержания опиралось на авторскую передачу, текущие W2 dispositions, определения статусов и адресные F/S/Q/E-ссылки. Проверки текста и путей ниже не являются проверками описанных моделей.

## Существенные редакторские решения

- Сохранена большая причинная композиция, не сведённая к пятнадцати обзорам. Карта симптомов B перенесена перед выбором восстановления: лестница → подготовка сравнимых входов/графов/численных стадий → классификация первой проблемы → методы исправления → чувствительные task/event slices → фактические условия LinQ. Подробное дерево D осталось после программы E как инструкция выбора следующего действия.
- Вступление теперь сразу сообщает срез доказательств и отсутствие запусков. Добавлены короткие определения source/candidate/parent/runtime/GT и указатель F/S/Q/E. Авторское время начала синтеза убрано из публичного вводного абзаца; дата среза не изменена. Авторская атрибуция визуального чтения кейса оркестратору сохранена.
- Переписаны вводные и причинные переходы, названия экспериментальных разделов, административные формулировки, численные примеры и наиболее плотные сравнительные строки. В таблицах симптомов и метрик служебные английские цепочки развёрнуты в действия и условия на русском. Общепринятые термины, названия API, версии, схемы и поисковые обозначения сохранены.
- В четырёх карточках опубликованных измерений расставлены разделители между моделью, версией, calibration, metric scale, числами и неизвестными. Wu partial/QAT и BRECQ recipes остаются независимыми сравнениями; YOLOX latency не перенесена на accuracy row; pose INT8 не превращён в доказательство сохранения событий.
- Статистические примеры изложены последовательно: fixed roster → iid Bernoulli / односторонний CP → отдельный HPP rate → lost/gained paired table. Все числа, формулы, предпосылки, α/2, n=0/T=0 и ограничения selection/clustering/optional stopping сохранены. Формулы не применены к AP/OKS/HOTA и не названы нашими результатами.
- Все сравнительные таблицы, необходимые для A–F, оставлены: стадии, симптомы, методы, семейства моделей и метрики решают разные задачи. Декоративных таблиц или новых конечных README/INDEX/SUMMARY не добавлено.
- При переносе в корень переназначены relative links согласно AUTHOR_NOTES: четыре реестра без `../`; case PDF, CASE_NOTES и AUTHOR_HANDOFF через `_WORK/`. Прямые primary URLs сохранены.

## Условия, которые редактура сохранила

Все 12 единых E001–E012 подробно раскрыты ровно по одному и остаются **PROPOSED / UNRUN**. Их роли samples не выданы за уже собранные IDs. Приоритеты E002/E003/E005 зависят от E001/Q001–Q003, а E005 — от E004. Пять независимых source/tensor/task/event/device gates, same-tensor и complete-media сравнения, absolute B quality и paired non-inferiority сохранены. HOLD, INCONCLUSIVE, UNAVAILABLE и узкий PASS(scope) не свёрнуты в общий PASS.

Сохранены: U8.3.230 commit и source-coherent contract; preparation parents; rect/dynamic/non-IMX; G01–G04/Pose corrections; BCN/no-objectness/decoded DFL и sigmoid/custom nc=1/2/3; final6 shortcut; NMS ties/in-place/caps/padding/time limit; onnxsim/verification bounds как чужие технические настройки; IR/opset/schema distinction; FP16 clipping versus representation; BF16 и storage/compute distinction; ORT/NNCF/LiteRT versus LinQ percentile scope; blanket TypeError retry; UNKNOWN target QDQ/QAT/mixed consumer; E007 до training; ORT ModelProto CPU versus model-path provider API и отдельный runtime version scope.

LinQ guide/current source/old README/vendor benchmark не склеены в одну среду. Сохранены lazy native ABI, return/preset/platform uncertainties, ONNX value/node/TF port mapping, отдельный float importer gate, FULL/PRE/POST/RAW mode versus RAW program, byte pointer versus numerical dtype, view versus dequantization, historical Codec dependency и неизвестная текущая completion semantics. Vendor TinyYOLO3, self-build YOLOv8 и performance extraction имеют отдельное происхождение. Warmup seam не приписан native MLPerf или всей vendor table. RT-DETR и RTMPose остаются conditional admission routes, с operator/dependency/crop/outputs/flip constraints и неполученными weights bytes.

Не сокращены small-object observability/classes/source+input-size, critical pose/visibility/missing people, actor ownership, tracking pools/dt/PTS/epochs, causal versus future interpolation, все GT episodes в denominator, полные alert/status ledgers, union source-camera-hours, late/miss/duplicate/false/unknown и независимые splits. Pack 24–40 frames / 8–12 clips и E011 до шести semantic regions + двух boundary/interaction probes остаются согласуемыми proposal budgets, а не нормами достаточности.

## Встроенные редакторские проверки

На момент завершения human: **160450 bytes, 13086 whitespace-delimited words, 523 строки**; UTF-8 без BOM, 0 U+FFFD. Объём немного вырос из-за расстановки пробелов и развёртывания телеграфных формулировок; техническая глубина не сжималась до summary.

В human проверены **313 Markdown links**, включая **263 relative targets/anchors**: 0 missing files и 0 missing anchors. Все F/S/Q/E explicit anchors разрешаются в сохранённых реестрах. В сравнении с DRAFT:

- multiset всех исходных inline-code literals совпадает полностью;
- multiset всех исходных primary URLs совпадает полностью;
- ни одно исходное F/S/Q/E вхождение не потеряно; добавлены только навигационные/повторные E-вхождения;
- набор числовых литералов не изменён;
- E001–E012 существуют ровно по одному как подробные разделы.

Четыре evidence files не менялись: SHA256 до и после редакторских действий совпали.

| Файл | SHA256 |
|---|---|
| RAW_FACTS.md | `50e4f845f8c910a286f357f51fff8642af2993443c4b493f63011ed37c35a8de` |
| SOURCES.md | `e5ecde7f6f129c96ea579ed3fa9033d5c911601681496f19364efc059ee8ef79` |
| OPEN_QUESTIONS.md | `dc5a78ac043b1b8331cd5d69079cda564647f34e56f3be209fa0fc10ddd26366` |
| CRITIC.md | `f68362cfd502be18074ae861014034c1f1a07a1a42fb5ed517b175ad534302cc` |

## Передача root и сжимателю

Готовый human находится в корне: [report_human_model_fidelity_quantization.md](../report_human_model_fidelity_quantization.md). Машинный отчёт — следующий согласованный этап. Для него нужно сохранить те же версии, условия, единый реестр E и разделение source/code/vendor/published/LOCAL/proposal/UNKNOWN; редактор не создавал новую фактическую базу.

Ключевые ограничения остаются открытыми: фактический grant, совместимый bundle, checkpoint/weights, licensed independent GT, numerical consumer, completion/placement и утверждённый AR01 отсутствуют. MEASURED — none; δ/floors/caps/D/α и scope — TEAM_DECISION_PENDING. Документальные закрытия K003/K006/K008 не равны device closure. Полный кейс и его hash существуют, но guide/performance PDF использованы через атрибутированные извлечения без нового визуального подтверждения. Историческое окно 45 часов не перезапускалось. Ни одна редакторская правка не закрывает Q001–Q019 вместо получения конкретного артефакта или решения владельца.

## Узкое уточнение атрибуции чтения кейса

По запросу root исправлена одна фраза вводного абзаца human: полное визуальное чтение 20 страниц принадлежит root; W2-07 дополнительно самостоятельно прочитал страницы 5/7/13/19 по существующим рендерам ([S003](../SOURCES.md#S003)). Это отдельное чтение внутри той же первичной цепочки PDF/рендеров, не новое происхождение документа и не пятнадцать независимых повторных проверок. Прежняя категорическая формулировка об отсутствии дополнительного чтения снята. Другие факты, primary URLs и inline literals не менялись. Это адресная редакторская коррекция по существующему реестру, без нового research/audit.
