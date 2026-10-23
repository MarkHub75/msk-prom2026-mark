from pathlib import Path
Path('_WORK/W2-15.md').write_text('''# W2-15 — PhysicalAI: точный smoking join и условия synthetic donor

K015; W2-C. Доступ23.10.2026; продолжение clock03:40:57UTC/06:40:57Europe/Moscow. **K015 — область уточнена.** Subset остаётся дополнительной synthetic event-plumbing гипотезой, не основным industrial holdout. Media samples намеренно не получались: metadata/provenance/terms уже меняют решение; visual quality не проверялась.

## Источники и версии

| ID | Первичный источник | Сохранённое / locator |
|---|---|---|
| W2-15-S01 | NVIDIA *PhysicalAI-Event-Videos* v1.0, creation15.06.2026, HF revision `7f79b39fcd1ef1dc39f23f227cd8a9480d6077db` https://huggingface.co/datasets/nvidia/PhysicalAI-Event-Videos/tree/7f79b39fcd1ef1dc39f23f227cd8a9480d6077db | W1-06/PhysicalAI-Event-Videos: README, repo.json,2026/provenance.json, train/labels.json, video_manifest.csv, anomaly-category-mapping.json. Новый W2 анализ ранее полученных файлов, не независимая публикация. |
| W2-15-S02 | NVIDIA Dataset License Agreement https://assets.ngc.nvidia.com/products/api-catalog/legal/Personas-Dataset-NVIDIA-Training-Dataset-License-Agreement-2025-11-26.pdf | Реально получен PDF293509bytes, `MATERIALS/W2-15/LICENSE.pdf`, `LICENSE.txt`; текст version November21,2025, имяURL November26 — разные даты. §§1–5,12.3. Доступ23.10.2026. |
| W2-15-S03 | Google Cloud Service Specific Terms https://cloud.google.com/terms/service-terms | HTTP200, HTML1,053,191bytes `GOOGLE.html`, извлечение `GOOGLE_EXTRACT.txt`; §17 Use Restrictions for AI/ML Services. Mutable page, дата доступа отдельно от version NVIDIA. |
| W2-15-S04 | Наш executed join `AUDIT_JOIN.py` | `EXACT_JOIN.json`, `JOIN_SUMMARY.json`; прежний `SMOKING_JOIN.json` — предварительная selection, не замена original source labels. |

## Факты и воспроизводимое правило

**W2-15-F01 — выполненный deterministic family selection S01/S04.** Для каждого chunk: is_anomaly=false → Normal; иначе первая сработавшая regex из ordered mapping по anomaly_type; default Other. Отбирается только derived family `Smoking / vaping`. Получено **282labeled chunks у157уникальных parents**:143chunks NV-VAD-v1 и139 NV-VAD-v1.1. Это точный family subset; прежние W1substring187parents относятся к другому candidate scope и не заменяют157. Все282 имеют bundled source; external0. Все `(dataset,video_id,chunk_index)` уникальны.

**W2-15-F02 — выполненный join S04.** CSV содержит filename,dataset,chunk_count; video_id колонки нет. Ключ: dataset+basename(parent.video_path) ↔ dataset+manifest.filename. У каждого selected chunk ровно1matching parent manifest row. Packaging следует из source_video.access=bundled и public media policy, но ZIP directory/member existence/bytes **не проверены**. Documented packaging отличается от скачанного payload.

**W2-15-F03 — temporal metadata consistency S04.** У всех selected parents declared FPS24.0. Нет неположительных окон, start<0 или end за video_duration_sec(+0.001s). Это анализ metadata, не media measurement. Примеры:

| Parent | Source / window | Frames / chunk |
|---|---|---|
| NV-VAD-v1/video_00375 | videos/video_00375.mp4, parent8s/192frames; chunk[0,5]s | frames0..119,chunk_000.mp4; type `vaping smoking` |
| NV-VAD-v1.1/video_01415 | videos/video_01415.mp4, parent7.875s/189frames; chunk[2.875,7.875]s | frames69..188,chunk_001.mp4; type `person vaping visible smoke` |

Endframe inclusive согласуется с этими двумя examples, а не объявляется универсальным author protocol. Windows могут перекрываться; unique chunk keys не снимают scenario/near-duplicate leakage. Captions первых records описывают industrial loading dock и retail liquor store; это source text, не наш visual просмотр.

**W2-15-F04 — documentary packaging/provenance S01.** Полный release:1612parent records/3796labeled chunks. Packaged media:1486NVIDIA parents/2939chunks =2919labeled+20unlabeled QC-excluded. Эти20 не присваиваются smoking family: source labels для них нет. CHAD/VAD-R1 external pointers присутствуют в общем release, но не в точном smoking family. Captions/queries частично model-generated; human review исправлял выбранные поля, не весь текст. Provenance указывает Gemma4-31b-it, temperature0.7. anomaly_type free-text; family — reporting aid. Card предупреждает о near-duplicate generation scenarios. Supplied scenario group IDs не получены; нельзя выдумывать их по caption. Train only, official val/test нет.

## Точные условия и их практическое значение

**W2-15-F05 — прочитанный NVIDIA legal text S02, не общее юридическое заключение.** §1: limited, revocable, non-transferable, non-sublicensable grant на download/use/reproduce/modify/derivative works solely для training/development AI Solutions. §2: authorized users — employees/contractors/affiliates через secure network, не общее public sharing. §3.2 запрещает sell/rent/sublicense/transfer/distribute/embed/host dataset whole or part/otherwise make available to others. §3.3 сохранять notices; §3.4 не делать dataset subject to open-source licence. §4 отсылает к Trustworthy AI Terms; §12.3 — trade/export conditions. Полный текст сохранён, Trustworthy terms отдельно не разобраны, поэтому не заявляется полный compliance clearance.

Практическое изменение: raw media, crops и annotations не включать в публичный repo/demo asset bundle на основании одного этого grant. Слово redistributable в card описывает поставку NVIDIA и не равно нашему праву повторного распространения. Разрешённые локальные training/development действия и public delivery необходимо хранить раздельно. Вопрос конкретного deployment/командного доступа сохраняется условным, а не blanket commercial_ok.

**W2-15-F06 — additional generation conditions S01/S03.** Card говорит о Veo3 и Cosmos3Super; Veo-generated videos также subject to applicable Google terms. Прочитанный §17a ограничивает AI/ML Service или Generated Output для similar/competing product/service. §17b — substitute/replace/circumvent Google Model или create/improve similar models, с описанным fine-tuning/distillation exception. Selected parent metadata не даёт per-video Veo/Cosmos assignment; следовательно, нельзя объявить все selected chunks свободными от additional conditions. Применимость к конкретной цели требует уточнения, не общей гарантии.

## Q, retrieval и handoff

W2-15-Q01: per-video generation model/scenario IDs и допустимые действия для конкретной training/deployment/demo цели. W2-15-Q02: exact archive membership и20unlabeled records до media sampling. При необязательном synthetic scope **отложить media acquisition**: реальное Önal replay и своё target GT приоритетнее.

Подготовленный retrieval, не выполненный download: pinned revision `2026/train/videos.zip` и `2026/train/chunks.zip`; EXACT_JOIN даёт parent path и `(dataset,video_id,chunk_file)` для documented layout. Сначала получить ZIP directory/range, а не весь multi-GB payload; проверить права и только затем небольшой member. Media throughput/visual transfer/точность event boundaries не измерялись.

→ video_architecture: declared24FPS windows для plumbing после получения media; → evaluation: synthetic train-only не camera-hour holdout; → training_strategy: caption errors, overlapping scenarios и Veo conditions; → rights collector: local training grant, redistribution restrictions и unknown per-video generator сохранять раздельно.
''',encoding='utf8')
