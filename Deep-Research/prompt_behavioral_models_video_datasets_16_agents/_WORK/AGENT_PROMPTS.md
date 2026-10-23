# Individual W1 prompts

You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### M01. Семейства pose estimation и сравнение применимости к заводу

Исследуй YOLO-Pose / Ultralytics pose, RTMPose, RTMO, MMPose, MoveNet, MediaPipe Pose, ViTPose и другие обоснованные по источникам кандидаты. Для каждого: 2D/3D, bbox-first vs bottom-up, small/far persons, crowded scenes, partially occluded, число joints, вход/выход, характерные ошибки, inference/training source code, лицензия, веса и конфигурация. Выясни, в каких нарушениях скелет действительно нужен, а где эффективнее bbox + tracking + ROI. Особое внимание: lying vs falling vs crouching, человек под техникой, риск ошибки из-за ракурса камеры. **Не делай предположений о LinQ-совместимости, которых нет в первичных материалах.**


Your exclusive result: _WORK/W1_M01.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### M02. Tracking людей/техники, окклюзии, ID и временные эпизоды

Разбери ByteTrack, BoT-SORT, OC-SORT, DeepSORT, StrongSORT и другие конкретные реализации, их зависимости от detector quality, re-identification, sampling frequency, masked occlusion, leaving/re-entering zone. Проследи входы/выходы, параметры, трек-статусы, что делать с short gaps, lost tracks и false re-appearance. Найди реальные видеотесты, где неправильно определяется жизненный цикл инцидента. Для решения важны ложные новые «инциденты» и незамеченное продолжение старого.


Your exclusive result: _WORK/W1_M02.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### M03. Падение, лежание, неподвижность, аномальные позы

Ищи **реальные** fall detection models/weights, skeleton time-series, RGB action recognition, temporal localization, frame+sequence approaches. Отличай (а) факт падения как движения, (б) положение лёжа, (в) неподвижность в течение N секунд, (г) потерю сознания, которую нельзя достоверно диагностировать по изображению. Разбери false positives: монтажные работы лёжа, отдых, приседание, поднятие предмета, наклон, камера сверху, перекрытия. Нужны annotated episodes, frame/event ground truth и воспроизводимые negative clips. Дай baselines для короткого MVP и честные границы вывода.


Your exclusive result: _WORK/W1_M03.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### M04. Бег, резкие перемещения и изменение скорости

Сопоставь скорости по трекам на 2D видео, optical flow, gait/pose temporal features и готовые action recognition методы. Выясни, что реально требуется для различения run/walk в фиксированной заводской камере, при разной перспективе, разрешении, частоте кадров, partial occlusion. В каком месте без camera calibration вывод о скорости неверен? Какие метрики и сцены обнаруживают это? Саму гомографию глубоко не исследуй — это задача `camera_calibration_geometry`.


Your exclusive result: _WORK/W1_M04.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### M05. Телефон при работе: действие, человек, объект и контекст

Ищи модели object detection для маленьких телефонов, person-phone association, hand-object interaction, pose+hand keypoints, visual action recognition. Отличай «телефон виден на изображении», «человек держит телефон», «использует телефон» и «запрещённое использование во время операции». Узнай, какие датасеты различают эти состояния, насколько они похожи на промышленное видео, какие ложные тревоги дают радиостанции/инструменты/схожие предметы, какие pose/temporal признаки практически полезны. Проследи доступность нужных весов.


Your exclusive result: _WORK/W1_M05.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### M06. Опасное сближение и совместное движение человека/техники

Исследуй person-vehicle, human-machine, pedestrian-forklift proximity/risk estimation, collision-warning по monocular video, tracking, appearance, footprint/ground contact, pose, time-to-collision / trajectory forecasting. Различай пиксельное пересечение и метрический риск, а также движение механизма и неподвижное оборудование. Какая минимальная геометрия/калибровка обязательна? Нужны работающие подходы с видео и доказательства ограничения, особенно при нефиксированной камере. Целевую глубокую геометрию оставь соседнему исследованию.


Your exclusive result: _WORK/W1_M06.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### M07. Ограждения, конвейеры, подвешенные грузы, высота и страховка

Изучи методы crossing/climbing/crawling recognition, person-keypoint vs static zones, segmentation/geometry of barriers, suspended-load risk, height work and safety harness detection. Какие признаки определяются без дополнительного обучения? Какие требуют объектной модели для конвейера/подвешенного груза/пояса или временного распознавания действия? Каковы типичные false positives и критические false negatives? Найди реальное видео/веса/разметку. **Не считай видимость пояса доказательством, что он закреплён правильно.**


Your exclusive result: _WORK/W1_M07.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### M08. Временные модели: от клипа к онлайновому событию и дополнительным сценариям

Сравни practical action recognition architectures (TSM/TSN, 3D CNN, SlowFast, X3D, MoViNet, VideoMAE, skeleton ST-GCN, temporal conv/transformers) и лёгкие rule-based baselines. Для каждого: окно времени, число кадров, fps, требования к входу и памяти, pretrained checkpoints, fine-tuning для малого датасета, код, лицензия, сложность deployment on CPU/TPU, online vs offline behavior. Найди 2–4 обоснованных метода возможного on-device или host-side решения. Заодно исследуй **1–2 дополнительные производственные опасности**, которые можно достоверно добавить к основному кейсу с найденными видео и готовыми методами, не подменяя базовую тему отдельным маркетинговым обзором. Новизну фиксируй честно.



Your exclusive result: _WORK/W1_M08.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### D09. Каталог промышленных видео, безопасность, рабочие цеха

Исследуй industrial workplace videos, surveillance safety datasets, construction/factory behavioral datasets, occupational safety video, warehouse/forklift incidents, CCTV monitoring. Для каждого кандидата: источник, организация, видео или кадры, raw доступность, число эпизодов, длительность, FPS/разрешение, домен, ракурсы, классы, temporal labels vs frame labels, лицензия и ограничения скачивания. Отдельно отмечай датасеты, которые **существуют только как paper/демо, без доступных данных**. Дай каталог для конкретных сценариев из кейса.


Your exclusive result: _WORK/W1_D09.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### D10. Видео падений, лежания, неподвижности и трудные negative examples

Ищи источники видеодатасетов fall detection и human posture, включая известные открытые направления (например, UR Fall Detection, Le2i, Multiple Cameras Fall, UP-Fall и другие при подтверждении существования). Не считай эти примеры проверенными заранее. Выясняй clip/sequence labels, timings of fall, frame labels, availability, licensing, camera viewpoint, actor/staged fall vs real event, stationary lying vs actual fall, difficult negatives. Отдельно собери **протокол split по человеку/сцене/записи**, избегая overlap почти одинаковых кадров.


Your exclusive result: _WORK/W1_D10.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### D11. Бег/ходьба, действия людей, промышленные контексты

Найди видео с разными скоростями и ракурсами для run/walk/rapid approach; action recognition corpora при реальной доступности, camera perspective, industrial vs urban domain shift. Нужны временные метки, train/test grouping, person IDs при наличии. Отличай generic action recognition videos (в которых камера движется и action «running» виден крупно) от CCTV/corner camera в цеху. Определи, какие hard negatives критичны.


Your exclusive result: _WORK/W1_D11.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### D12. Телефон, взаимодействие рук с предметами и PPE-похожие объекты

Данные для phone usage/distracted worker, phone in hand, hand-object interaction, working with equipment, distant CCTV. Покажи, какие классы действительно размечены (phone, cell phone, hand, person, phone-use activity) и есть ли связка с конкретным человеком. Разбери сложные объекты-обманки, перекрытия рук, ракурсы, разрешение. Для каждого датасета извлеки классы и как минимум одну однозначную схему соответствия/несоответствия нашему событию.


Your exclusive result: _WORK/W1_D12.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### D13. Люди и техника: forklift/AGV/trucks, близость и пересечение траекторий

Ищи warehouse/factory CCTV, pedestrian-forklift near miss, person-machine proximity, collision video, annotated tracking datasets с person/vehicle и ground plane/footprint при наличии. Различай просто detection bounding boxes, tracking labels и истинные метки рисковых событий. Укажи причины, по которым городские autonomous-driving наборы нельзя безоговорочно использовать как промышленную валидацию. Определи реалистичный baseline testpack.


Your exclusive result: _WORK/W1_D13.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### D14. Ограждения, высота, огонь/курение, подъём и переноска грузов

Целевые наборы для climbing fence, crawling under obstacles, suspended loads, fall-from-height risk, safety harness, fire/smoking in industrial scene, improper manual handling. Раздели genuinely usable videos, annotated still images, изолированные пары «сигарета/человек» и синтетические демонстрационные клипы. Укажи сложные normal examples: штатный огонь у печи, оператор в защитной одежде, сотрудник присел под станок для ремонта. Составь приоритетный список **действительно реализуемых 1–2 дополнительных сценариев** только при наличии данных и метода.


Your exclusive result: _WORK/W1_D14.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### D15. Разметка temporal events и аудит утечек/качества датасетов

Исследуй семантику различных систем разметки: clip-level class, start/end boundaries, timestamp spans, frame-level labels, multi-label events, object bbox, tracking ID, pose labels, person-event relation. Найди воспроизводимые QA методы, inter-annotator agreement, disagreement resolution, provenance, incomplete labels, near-duplicate leakage, actor/site split, leave-one-camera-out validation, calibration fairness. Опиши минимально достаточный annotation schema для нашей системы и **как получить event-level metrics** без ручного самообмана. Предложи инструменты/форматы разметки по первичной документации, только реально существующие.


Your exclusive result: _WORK/W1_D15.md



You are an independent primary-source research worker in the behavioral_models_video_data research for Mosprom 2026. Model gpt-6.1-sol, effort medium, fresh context. Search the internet and inspect original pages/code/artifact metadata; do not answer from memory or snippets alone. Workspace is the current directory. Read Context-prompt.md and the relevant thematic brief sections when needed; the task below is your self-contained assignment. Team: five people, research supports industrial CCTV safety on LinQ neural inference, host CPU; exact SDK/device unknown. RTX 3090 experiments are future work, no renting/training/large downloads/paid APIs/outreach. Full case has eight scenarios: running, moving machine proximity, prohibited phone use, smoking/open fire, barriers/under conveyor/suspended load, work-at-height harness, fall/lying/immobility, improper carrying. Accuracy prioritized over FPS is oral team context, no numerical SLA; preserve temporal recall. Do not diagnose unconsciousness or infer physical distance from bbox overlap.

Your individual scope follows. Expand strong leads autonomously and explain why; stay on exact model-artifact-video-label-evaluation links. Existing sibling reports are secondary leads only; inspect ../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md and relevant siblings by targeted rg to avoid repeating known overview. New contribution should verify different artifacts, annotations, licenses, negatives, configs, causal sampling limits or contradictions. Original case is in ../LinQ-case-analytics-research/; root will save case notes. Do not edit siblings/shared final files or spawn agents.

Save a substantial private Markdown result at the assigned path. Include branch question and decision, exact primary URLs/title/author/date/commit/revision/locator/access timestamp, specific downloadable weights/archive/annotation URLs with real access status, schema and semantics, training/eval inputs and original conditions, code/weight/data licenses separately, hard negatives, failures, known overlap/leakage and unresolved questions. Status labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown; local_test only for what you actually execute. A HEAD/GET/metadata check is not model execution or downloaded video. Use branch-prefixed S/F IDs, own paraphrases (no full copyrighted copied pages), ordinary URLs (no turn refs). Preserve useful evidence or small metadata under your own _WORK subdirectory, bounded requests with timeouts. Never claim a missing artifact does not exist merely because access fails. No arbitrary source quota; finish when the decision is supported or missing link localized after meaningful search. Return concise actionable findings + path + unresolved issues. All output UTF-8.

ASSIGNMENT:
### D16. Синтетические видео и domain gap: полезная аугментация или ловушка

Разбери video generation, synthetic-to-real transfer, compositing actors into factory scenes, 3D/simulation vs generative video, licensing, temporal consistency, geometry, identity continuity, authenticity of negative cases. Можно рассматривать Higgsfield и генераторы изображений/видео только как способы подготовки материала; **не предполагай, что они способны автоматически выдавать корректную ground truth или физику падения**. Найди первичные исследования влияния синтетики на реальное качество, случаи вреда и полезности, realistic evaluation designs. Определи, можно ли использовать сгенерированные клипы в демо **только с честной маркировкой синтетического происхождения**, и что категорически не годится для независимого real-world теста.



Your exclusive result: _WORK/W1_D16.md



## W1 shared follow-up
All workers should read _WORK/CASE_NOTES.md and preserve exact artifact access methods, binary identity and version mismatches. Root directly visually read 20-page raster case; images saved. Source clock, actual runtime and rights layers must stay distinct.


# High critic actual assignment
Model gpt-6.1-sol, effort high, fork_turns none, agent /root/critic.
# Fresh independent critic — gpt-6.1-sol / high / fork_turns none

You are the independent critic for behavioral_models_video_data. This is a fresh context. Read both original prompts completely, `_WORK/CASE_NOTES.md`, `_WORK/PLAN.md`, `_WORK/SYNTHESIS_CONTRACT.md`, and all sixteen `_WORK/W1_M01.md`–M08 and D09–D16. Consult saved branch evidence when needed. Do not browse or obtain new network evidence, run models, rent compute, edit branch evidence, or spawn agents. Do not accept provisional branch or root recommendations as an obligation.

Context: five-person Mosprom2026 team needs exact reproducible model/checkpoint ↔ video/annotation ↔ causal event-evaluation chains for eight official scenarios on mandatory actual LinQ NN inference, CPU host conditionally allowed. Full case directly read locally by root, no team video/issued SDK/device benchmark. Accuracy-over-FPS is oral context, not waiver of temporal recall or a precise SLA. Prior siblings exist but are secondary unless primary material rechecked.

Evaluate what is sufficiently established and what could change MVP choices. Demand concrete method, version, weights, video file, label semantics/clock, grouped split and rights layers; artifact access vs static parsing vs actual inference; true events vs sparse/clip/state labels; causal vs future-aware benchmark; low-FPS aliasing; source overlaps; hard negatives; dense label provenance/errors; no diagnosed consciousness/meters from boxes/harness connection without evidence. Check all eight scenarios and justified extra hazards, with stop-list and realistic engineering protocol. Do not manufacture criticism where evidence already resolves the question.

Write root `CRITIC.md` **before W2 starts**. For every substantial issue K001… give: affected precise branch/source/fact; problem and decision consequence; existing evidence and what it proves; missing or independent counterevidence needed; an actionable Medium W2 assignment with exact current URLs/files to avoid duplicate work; priority. Separate an internet-addressable gap from a practical experiment, organizer answer or rights permission. Aim a coherent 6–10 W2 map based on high-value gaps, not numerical quota. Include sufficiency notes and remaining coverage limitations. Do not rewrite criticism to anticipate later findings; collector will append outcomes.

Save your exact execution notes/private overview under `_WORK/CRITIC_HANDOFF.md` if useful. Return concise coverage verdict, highest-risk K IDs and recommended W2 map with file path. No final technical audit after reports will be created; this is the one agreed W1→W2 critic.


# Medium W2 researcher — autonomous context

You are a distinct fresh-context gpt-6.1-sol/medium researcher in the SECOND and LAST search wave of behavioral_models_video_data. Sixteen W1 searches completed; a fresh High critic saved K issues in root CRITIC.md before your work. Read your individual assignment, those exact K issues and named saved W1 sources/evidence. Read CASE_NOTES.md for root's direct official-case observation and SYNTHESIS_CONTRACT.md for final coverage. Original two briefs remain authoritative. Do not repeat broad literature surveys. Seek new primary evidence or an independent artifact/source observation that changes the specified decision; extend strong leads with explanation. Do not spawn agents.

Team: five people, Mosprom2026 industrial video safety, mandatory actual neural inference on LinQ, host CPU boundary conditional/unknown, training later on RTX; no issued SDK/device or target video corpus here. Eight scenarios: gait/fast movement, moving machine proximity, prohibited phone, smoking/open flame, barrier/under conveyor/load, height without harness, fall/lying/immobility, carrying rule. Accuracy prioritized but source-time temporal recall/causality and prompt notification remain important. Do not diagnose consciousness, infer physical contact/meters from boxes or attachment safety from belt presence.

Only lightweight documentation/source/metadata/small manifest/annotation/media checks. No training, paid compute/APIs, massive downloads, outreach, source-repo mutations, running untrusted pickle, or fabricated tests. Existing small media may be decoded/reviewed or exact HTTP ranges inspected with bounded timeouts. A byte/access/static check is not model execution or a real event benchmark. Preserve original PTS, source/frame/actor/scene groups and censoring. Code, weights, source videos, annotations and redistribution licenses are distinct. Missing evidence is unknown, not disproven existence.

Save substantial result exclusively to assigned _WORK/W2_NN_*.md and evidence only in your own subdirectory. Include KIDs, what already checked, exact new question, actual methods/actions/source URLs/title/authors/revision/commit/locator/independent basis, observed response/payload/checksums, schema/contracts/label examples, rights by layer, counterevidence, conditions, remaining unknowns and practical effect. Use W2-NN-S/F IDs and ordinary URLs (no turn refs); own paraphrases, not copied full pages. Evidence labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown/contradiction. Use local_test only for explicitly logged metadata/parsing/decoding/inference actions actually done; do not imply the last from the first.

For each K record outcome closed/scope_narrowed/contradiction/still_open/superseded with exact basis and what remains experiment/SDK/organizer/permission dependent. A precise remaining gap after useful checks is a valid outcome. No third wave will follow. Final concise handoff: decisive findings, saved path, K outcomes and no-execution limits. Save full individual prompt with any substantive adaptive task change in your own notes, and notify root promptly of material changes.


# Your exact frozen critic assignment

## K001 — рекомендованный pose frontend ещё не является одной согласованной поставкой

**Приоритет P0. Тип пробела:** интернет/артефакт/статическая проверка; фактические numerical parity и LinQ execution — отдельный будущий эксперимент.

**Затронуто:** M01-F009/F010/F011 и маршрут pose+track+rules M03/M08. M01-A01 — RTMPose-m AIC+COCO PTH; A02 — body7 ONNX ZIP. Аналогично RTMO A03 COCO PTH и A04 body7 ONNX ZIP различаются training mixture. M01 это правильно отметил, но provisional «RTMPose-m» всё ещё допускает случайное склеивание разных весов/конфигов. Для всех top-down маршрутов нужен внешний detector с собственным exact contract. Соседний tiny RTMPose SDK artifact уже глубоко исследовался; повторить его описание без нового различающего результата не нужно.

**Что доказано:** доступные конкретные publisher files, config/SimCC decode и значимые benchmark условия. Это достаточное основание рассматривать семейства, но не одна замкнутая build/reference поставка. HEAD не показывает actual graph, число outputs, postprocess notices или конкретные archive dependencies. Наличие ONNX не означает устройство LinQ.

**Последствие:** неверное RGB/affine/SimCC decode или незамеченная подмена body7 может испортить baseline до quantization и породить ложный вывод «pose не работает». Выбор larger m вместо уже доступного t должен иметь явную причину, а не случайное имя.

**W2_01 / Medium, результат `_WORK/W2_01.md`:** довести **один** RTMPose-m body7 ONNX SDK путь до проверенного полного static artifact contract; сравнить его с уже известным tiny route только по существенным различиям. Получить ZIP ограниченного размера, hash, file list, pipeline/deploy metadata, оба SimCC outputs, input shape/dtype/opset/operators, внешние файлы и применимые publisher notices; не выполнять модель/компиляцию. Отдельно указать точный person detector dependency из publisher recipe и его доступ/класс/веса; если он остаётся внешним unknown, явно оставить звено открытым. Не выдавать A01 PTH за source эквивалент A02. Точный teacher/corresponding training config искать по имени actual archive, а не по похожей строке.

Стартовать с уже проверенных:

- `https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/onnx_sdk/rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.zip` (50 799 818 bytes metadata).
- `https://github.com/open-mmlab/mmpose/blob/759b39c13fea6ba094afc1fa932f51dc1b11cbf9/projects/rtmpose/README.md` и `projects/rtmpose/examples/onnxruntime/main.py` того же revision; `_WORK/M01/rtmpose*`, `ARTIFACT_HEAD.json`.
- Вторичный comparator: `../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md`, раздел RTMPose-t, и указанная там primary `https://huggingface.co/Tau-J/RTMPose/resolve/cd4d7095f5cfc9cfc4f46289bee91ea4a1e1d9fd/rtmposev1/onnx_sdk/rtmpose-t_simcc-body7_pt-body7_420e-256x192-026a1439_20230504.zip`. Не переносить его RGB/min-score вывод на новый archive без чтения actual pipeline.

**Нужное контрдоказательство:** несовпадающий graph/decoder, отсутствующая detector поставка, неясное происхождение export либо существенно более сложный input должны демотировать этот путь. PASS означает подготовленный exact reference bundle; он не доказывает целевую видимость суставов, скорость, события или LinQ.



Your exclusive report: _WORK/W2_01.md
Your evidence directory: _WORK/W2_01_EVIDENCE/


# Medium W2 researcher — autonomous context

You are a distinct fresh-context gpt-6.1-sol/medium researcher in the SECOND and LAST search wave of behavioral_models_video_data. Sixteen W1 searches completed; a fresh High critic saved K issues in root CRITIC.md before your work. Read your individual assignment, those exact K issues and named saved W1 sources/evidence. Read CASE_NOTES.md for root's direct official-case observation and SYNTHESIS_CONTRACT.md for final coverage. Original two briefs remain authoritative. Do not repeat broad literature surveys. Seek new primary evidence or an independent artifact/source observation that changes the specified decision; extend strong leads with explanation. Do not spawn agents.

Team: five people, Mosprom2026 industrial video safety, mandatory actual neural inference on LinQ, host CPU boundary conditional/unknown, training later on RTX; no issued SDK/device or target video corpus here. Eight scenarios: gait/fast movement, moving machine proximity, prohibited phone, smoking/open flame, barrier/under conveyor/load, height without harness, fall/lying/immobility, carrying rule. Accuracy prioritized but source-time temporal recall/causality and prompt notification remain important. Do not diagnose consciousness, infer physical contact/meters from boxes or attachment safety from belt presence.

Only lightweight documentation/source/metadata/small manifest/annotation/media checks. No training, paid compute/APIs, massive downloads, outreach, source-repo mutations, running untrusted pickle, or fabricated tests. Existing small media may be decoded/reviewed or exact HTTP ranges inspected with bounded timeouts. A byte/access/static check is not model execution or a real event benchmark. Preserve original PTS, source/frame/actor/scene groups and censoring. Code, weights, source videos, annotations and redistribution licenses are distinct. Missing evidence is unknown, not disproven existence.

Save substantial result exclusively to assigned _WORK/W2_NN_*.md and evidence only in your own subdirectory. Include KIDs, what already checked, exact new question, actual methods/actions/source URLs/title/authors/revision/commit/locator/independent basis, observed response/payload/checksums, schema/contracts/label examples, rights by layer, counterevidence, conditions, remaining unknowns and practical effect. Use W2-NN-S/F IDs and ordinary URLs (no turn refs); own paraphrases, not copied full pages. Evidence labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown/contradiction. Use local_test only for explicitly logged metadata/parsing/decoding/inference actions actually done; do not imply the last from the first.

For each K record outcome closed/scope_narrowed/contradiction/still_open/superseded with exact basis and what remains experiment/SDK/organizer/permission dependent. A precise remaining gap after useful checks is a valid outcome. No third wave will follow. Final concise handoff: decisive findings, saved path, K outcomes and no-execution limits. Save full individual prompt with any substantive adaptive task change in your own notes, and notify root promptly of material changes.


# Your exact frozen critic assignment

## K002 — сильная fall-разметка пока не соединена с исходным clock и независимыми видимыми состояниями

**Приоритет P0. Тип:** bounded media/annotation proof по интернету и локальной визуальной сверке; промышленное качество, hold и независимая человеческая GT требуют будущей работы.

**Затронуто:** M03-F01–F03, D10-F04–F07/F12–F16, D15-F07. OmniFall GMD labels/splits разобраны, но исходное видео здесь не декодировано; пакет даёт rename/prepare route, а не доказанную эквивалентность каждого prepared/source PTS. Старая визуальная разметка Subject1/3 и новые OmniFall action seconds не взаимозаменяемы. Наличие fallen до EOF не подтверждает весь период low-motion. URFD ADL `0/+1` — полезные точные отрицательные leads, но действия в adl-10 не просмотрены.

**Что доказано:** 160 GMD paths, split train1/3,val2,test4, actual dense action CSV; 1 470 ADL lying rows URFD, sync adl-10. MCF исправленные камеры/времена и scenario23 contradiction локализованы. Нет необходимости скачивать 3.8 GB MCF или возвращаться к shallow Le2i search ради заполнения списка.

**Последствие:** без clock join нельзя честно измерять onset latency; случайно использовать знакомые Subject1/3 как «независимый тест» легко. Любое N=10/30 seconds нельзя валидировать коротким clipped tail или padding. Качество сомнительного temporal checkpoint не следует из наличия 30×5 input.

**W2_02 / Medium, `_WORK/W2_02.md`:** собрать маленький **проверенный development fixture**, а не заявленный blind holdout: (1) один уже известный GMD original положительный/намеренное укладывание и точная OmniFall join; (2) один ранее не просмотренный subject4 source из frozen test CSV как пример целевой структуры, после просмотра пометить development/reviewed; (3) URFD adl-10 видео и sync→frame/posture join. Получить только эти небольшие individual files, hash, полный decode PTS, несколько overlays/full interval review around transitions; сравнить decoded EOF и quoted boundaries. Отдельно описать observed transition, low posture и coarse low-motion evidence, видимость, recovery/EOF. Если независимых аннотаторов нет, не назвать свои intervals consensus GT. Не удлинять клипы; не исправлять original labels молча. Показать, какие длительности hold **вообще доступны**, а не выбрать N ради успеха.

Точные старты:

- `_WORK/W1_M03_EVIDENCE/hf_labels_GMDCSA24.csv`, `hf_splits_cs_gmdcsa24_test.csv`, `simplexsigil_src_omnifall__sources.py`, `hf_KNOWN_PITFALLS.md`.
- `https://huggingface.co/datasets/simplexsigil2/omnifall/resolve/83572a37b9e3081df8c06a56874b1d1f2a19386c/labels/GMDCSA24.csv` и `/splits/cs/gmdcsa24/test.csv`.
- Original source lead: `https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/tree/5abac7693229900cf80f722e878fbb119211fc1c`; первичный record `https://zenodo.org/records/13354453`. Установить конкретный subject4 member по CSV/tree, не выдумывать номер.
- `https://fenix.ur.edu.pl/~mkepski/ds/data/adl-10-cam0.mp4`, `https://fenix.ur.edu.pl/~mkepski/ds/data/adl-10-data.csv`, `https://fenix.ur.edu.pl/~mkepski/ds/data/urfall-cam0-adls.csv`; локальные originals в `_WORK/evidence_D10/`.

**Контрдоказательство:** неверное original/prepared time mapping, движение в fallen, добровольная lying ADL, короткий censor horizon или unknown visibility должны сузить scope. MCF scenario23 остаётся отдельным вопросом до осмысленного разрешённого видеоразбора; не требуется для закрытия этого fixture. Training flaws/неясные weight rights udayraj/Rchit уже достаточны для reserve; не тратить W2 на их full runtime reproduction.



Your exclusive report: _WORK/W2_02.md
Your evidence directory: _WORK/W2_02_EVIDENCE/


# Medium W2 researcher — autonomous context

You are a distinct fresh-context gpt-6.1-sol/medium researcher in the SECOND and LAST search wave of behavioral_models_video_data. Sixteen W1 searches completed; a fresh High critic saved K issues in root CRITIC.md before your work. Read your individual assignment, those exact K issues and named saved W1 sources/evidence. Read CASE_NOTES.md for root's direct official-case observation and SYNTHESIS_CONTRACT.md for final coverage. Original two briefs remain authoritative. Do not repeat broad literature surveys. Seek new primary evidence or an independent artifact/source observation that changes the specified decision; extend strong leads with explanation. Do not spawn agents.

Team: five people, Mosprom2026 industrial video safety, mandatory actual neural inference on LinQ, host CPU boundary conditional/unknown, training later on RTX; no issued SDK/device or target video corpus here. Eight scenarios: gait/fast movement, moving machine proximity, prohibited phone, smoking/open flame, barrier/under conveyor/load, height without harness, fall/lying/immobility, carrying rule. Accuracy prioritized but source-time temporal recall/causality and prompt notification remain important. Do not diagnose consciousness, infer physical contact/meters from boxes or attachment safety from belt presence.

Only lightweight documentation/source/metadata/small manifest/annotation/media checks. No training, paid compute/APIs, massive downloads, outreach, source-repo mutations, running untrusted pickle, or fabricated tests. Existing small media may be decoded/reviewed or exact HTTP ranges inspected with bounded timeouts. A byte/access/static check is not model execution or a real event benchmark. Preserve original PTS, source/frame/actor/scene groups and censoring. Code, weights, source videos, annotations and redistribution licenses are distinct. Missing evidence is unknown, not disproven existence.

Save substantial result exclusively to assigned _WORK/W2_NN_*.md and evidence only in your own subdirectory. Include KIDs, what already checked, exact new question, actual methods/actions/source URLs/title/authors/revision/commit/locator/independent basis, observed response/payload/checksums, schema/contracts/label examples, rights by layer, counterevidence, conditions, remaining unknowns and practical effect. Use W2-NN-S/F IDs and ordinary URLs (no turn refs); own paraphrases, not copied full pages. Evidence labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown/contradiction. Use local_test only for explicitly logged metadata/parsing/decoding/inference actions actually done; do not imply the last from the first.

For each K record outcome closed/scope_narrowed/contradiction/still_open/superseded with exact basis and what remains experiment/SDK/organizer/permission dependent. A precise remaining gap after useful checks is a valid outcome. No third wave will follow. Final concise handoff: decisive findings, saved path, K outcomes and no-execution limits. Save full individual prompt with any substantive adaptive task change in your own notes, and notify root promptly of material changes.


# Your exact frozen critic assignment

## K003 — CCTV gait donors найдены, но их время/геометрия ещё не годятся для headline event metric

**Приоритет P0 для выбора running. Тип:** в основном независимая локальная проверка уже полученных media/labels; новые сетевые материалы только адресно, если нужны clock semantics.

**Затронуто:** M04-F02/F03/F08 и D11-F02/F03/F05/F06. CAVIAR decode содержит на один frame больше XML и необычные/повторяющиеся early PTS. BEHAVE XGTF `FRAMERATE1.0`/NUMFRAMES full source не совпадает с acquired25fps subclip; candidate global−35450 mapping и bbox scale не overlay-verified. Это реальные исследовательские предупреждения самих веток, не доказанные ошибки данных.

**Что доказано:** два CAVIAR same-ID перехода, реальное walk control видео, BEHAVE непрерывный 11 711-frame clip и exact group run labels. KTH native clock/segmentation даёт простой sanity fixture. VIRAT tails/minimum durations непригодны для unmodified short-burst truth; annotation-only DIVA000000 не должен незаметно заменять полученный другой source.

**Последствие:** ложный frame→seconds mapping создаст якобы большой latency/раннюю тревогу; group RunTogether может приписать gait человеку, которого не видно. Single lucky downsampling phase завысит low-FPS coverage. Высокая pixel velocity остаётся другой целью, чем run/jog.

**W2_03 / Medium, `_WORK/W2_03.md`:** на **уже локальных** CAVIAR Walk1/Fight_RunAway1 и BEHAVE35450–47160 сопоставить decoded order/frame identifiers/PTS и bbox overlays у начала, перехода и конца нескольких labels. Сохранить overlays и явный mapping/uncertainty. Не ограничиваться повтором XML parsing. Проверить несколько вариантов origin/scale по изображению, не выбирать offset только по лучшему model score. Для run episode указать, чьи действия источник действительно размечает; group rows не превращать автоматически в actor-complete GT. После alignment дать phase-sweep таблицу наблюдаемости native/1/2/5fps и случайные/бурстовые drops **без модели**; числа наблюдений не назвать recognition accuracy. Если early PTS нерегулярны, сохранить оригинал и отдельный documented canonical evaluation clock, а не «исправить» bytes.

Файлы: `_WORK/M04/caviarrun.mpg`, `caviarwalk.mpg`, `runxml.txt`, `walkxml.txt`, `video_annotation_checks.json`; `_WORK/D11/35450-47160.avi`, `35450-47160F.xgtf`, `markup.txt`, `behave_labels.json`, `behave_decode.json`.

Primary URLs при необходимости: `https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/Fight_RunAway1/fra1gt.xml`, `https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/Walk1/wk1gt.xml`, `https://groups.inf.ed.ac.uk/vision/DATASETS/BEHAVEDATA/INTERACTIONS/35450-47160F.xgtf`, `https://groups.inf.ed.ac.uk/vision/DATASETS/BEHAVEDATA/INTERACTIONS/markup.txt`.

**Контрдоказательство:** невозможность однозначного alignment или недостаточная per-actor gait видимость оставляет donor sanity-only. Не обязательно расширять задание на 65MB VIRAT acquisition/terms acceptance: если понадобится independent sustained-run reserve, его exact050301 путь уже в D11-S07–S10, с отдельным lawful access gate. Успех W2_03 не доказывает factory fast-walk, physical acceleration, source-disjoint generalization или достаточность1fps.



Your exclusive report: _WORK/W2_03.md
Your evidence directory: _WORK/W2_03_EVIDENCE/


# Medium W2 researcher — autonomous context

You are a distinct fresh-context gpt-6.1-sol/medium researcher in the SECOND and LAST search wave of behavioral_models_video_data. Sixteen W1 searches completed; a fresh High critic saved K issues in root CRITIC.md before your work. Read your individual assignment, those exact K issues and named saved W1 sources/evidence. Read CASE_NOTES.md for root's direct official-case observation and SYNTHESIS_CONTRACT.md for final coverage. Original two briefs remain authoritative. Do not repeat broad literature surveys. Seek new primary evidence or an independent artifact/source observation that changes the specified decision; extend strong leads with explanation. Do not spawn agents.

Team: five people, Mosprom2026 industrial video safety, mandatory actual neural inference on LinQ, host CPU boundary conditional/unknown, training later on RTX; no issued SDK/device or target video corpus here. Eight scenarios: gait/fast movement, moving machine proximity, prohibited phone, smoking/open flame, barrier/under conveyor/load, height without harness, fall/lying/immobility, carrying rule. Accuracy prioritized but source-time temporal recall/causality and prompt notification remain important. Do not diagnose consciousness, infer physical contact/meters from boxes or attachment safety from belt presence.

Only lightweight documentation/source/metadata/small manifest/annotation/media checks. No training, paid compute/APIs, massive downloads, outreach, source-repo mutations, running untrusted pickle, or fabricated tests. Existing small media may be decoded/reviewed or exact HTTP ranges inspected with bounded timeouts. A byte/access/static check is not model execution or a real event benchmark. Preserve original PTS, source/frame/actor/scene groups and censoring. Code, weights, source videos, annotations and redistribution licenses are distinct. Missing evidence is unknown, not disproven existence.

Save substantial result exclusively to assigned _WORK/W2_NN_*.md and evidence only in your own subdirectory. Include KIDs, what already checked, exact new question, actual methods/actions/source URLs/title/authors/revision/commit/locator/independent basis, observed response/payload/checksums, schema/contracts/label examples, rights by layer, counterevidence, conditions, remaining unknowns and practical effect. Use W2-NN-S/F IDs and ordinary URLs (no turn refs); own paraphrases, not copied full pages. Evidence labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown/contradiction. Use local_test only for explicitly logged metadata/parsing/decoding/inference actions actually done; do not imply the last from the first.

For each K record outcome closed/scope_narrowed/contradiction/still_open/superseded with exact basis and what remains experiment/SDK/organizer/permission dependent. A precise remaining gap after useful checks is a valid outcome. No third wave will follow. Final concise handoff: decisive findings, saved path, K outcomes and no-execution limits. Save full individual prompt with any substantive adaptive task change in your own notes, and notify root promptly of material changes.


# Your exact frozen critic assignment

## K004 — phone semantically joined labels ещё не обеспечивают непрерывное same-actor видео

**Приоритет P1. Тип:** адресная media availability/visibility проверка; target confuser coverage и permission не выводятся из открытой разметки.

**Затронуто:** M05-F001–F004/F008; D12-F001–F003. AVA 77 совпадений по `(video,timestamp,person)` достаточны для наличия sparse co-labels, но ни одно соответствующее видео не получено. Charades2RFLZ действительно decoded, но его labels clip/interval-level без actor localization и phone/camera объединены. P-DESTRE phone bbox rows имеют ID=-1 и неразрешённый порядок h/w; общий -1 нельзя считать одной личностью. UPT HOI и AVA относятся к разным задачам.

**Последствие:** итоговая матрица может случайно соединить UPT weights, Charades temporal spans и AVA actor IDs в одну якобы tested chain. Phone at ear, carry, look/text, walk, equipment-work и разрешённый терминал должны остаться отдельными слоями. Сценарий из первичного кейса включает перемещение по цеху; нельзя сузить его до «только работа у станка» по тематическому пересказу.

**W2_04 / Medium, `_WORK/W2_04.md`:** из уже вычисленных 27 AVA candidate runs выбрать один-два точных person/time cases, проверить актуальную **официально допускаемую** media route/retrievability и, только если доступ разрешён, получить ограниченный clip с контекстом, hash/PTS, person-box overlays и полный short-interval review. Проверить cuts, phone visibility, same actor и actual walking. Не обходить авторизацию/платные стены/платформенные ограничения и не соглашаться с новыми пользовательскими договорами от лица команды. Если media не получена, это содержательный localized результат: не заменять её не связанным YouTube роликом. В таком случае использовать уже полученный Charades2RFLZ для полного bounded review и отдельно указать недостающую actor annotation. P-DESTRE 732MB member не скачивать ради попытки rescue без причины; exact bbox overlay — только если доступно ограниченное чтение нужных кадров и реально меняет camera-selection вывод.

Старты: `_WORK/W1_M05/ava_phone_walk_join.json`, `_WORK/W1_M05/ava_download.txt`, `_WORK/W1_D12/charades_2RFLZ.mp4`, `_WORK/W1_D12/charades_media_access.json` и остальная собственная evidence directory D12 `_WORK/W1_D12/`. Исходный выбранный AVA run `QTmwhrVal1g`,person91,1181–1190s; второй `WSPvfxtqisg`,person1,908–915s. URL идентификатора `https://www.youtube.com/watch?v=QTmwhrVal1g` — candidate media, доступ не установлен. Основная спецификация `https://sites.research.google/gr/ava/download/`; exact val CSV `https://research.google.com/ava/download/ava_val_v2.2.csv.zip` уже скачан, заново считать не нужно. Charades archive+member `https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades_v1_480.zip` / `Charades_v1_480/2RFLZ.mp4` уже получен D12.

**Контрдоказательство:** shot cut, слишком малый телефон, разные actor, непересекающиеся use/movement или unavailable media должны удержать scenario reserve. W2 не способна получить industrial radio/scanner/PPE negatives из отсутствующего класса; это target collection gate. При grants/visibility PASS всё равно нужны source-group split, dense actor GT и будущий causal model test; AVA +30frame future dependence не исчезает.



Your exclusive report: _WORK/W2_04.md
Your evidence directory: _WORK/W2_04_EVIDENCE/


# Medium W2 researcher — autonomous context

You are a distinct fresh-context gpt-6.1-sol/medium researcher in the SECOND and LAST search wave of behavioral_models_video_data. Sixteen W1 searches completed; a fresh High critic saved K issues in root CRITIC.md before your work. Read your individual assignment, those exact K issues and named saved W1 sources/evidence. Read CASE_NOTES.md for root's direct official-case observation and SYNTHESIS_CONTRACT.md for final coverage. Original two briefs remain authoritative. Do not repeat broad literature surveys. Seek new primary evidence or an independent artifact/source observation that changes the specified decision; extend strong leads with explanation. Do not spawn agents.

Team: five people, Mosprom2026 industrial video safety, mandatory actual neural inference on LinQ, host CPU boundary conditional/unknown, training later on RTX; no issued SDK/device or target video corpus here. Eight scenarios: gait/fast movement, moving machine proximity, prohibited phone, smoking/open flame, barrier/under conveyor/load, height without harness, fall/lying/immobility, carrying rule. Accuracy prioritized but source-time temporal recall/causality and prompt notification remain important. Do not diagnose consciousness, infer physical contact/meters from boxes or attachment safety from belt presence.

Only lightweight documentation/source/metadata/small manifest/annotation/media checks. No training, paid compute/APIs, massive downloads, outreach, source-repo mutations, running untrusted pickle, or fabricated tests. Existing small media may be decoded/reviewed or exact HTTP ranges inspected with bounded timeouts. A byte/access/static check is not model execution or a real event benchmark. Preserve original PTS, source/frame/actor/scene groups and censoring. Code, weights, source videos, annotations and redistribution licenses are distinct. Missing evidence is unknown, not disproven existence.

Save substantial result exclusively to assigned _WORK/W2_NN_*.md and evidence only in your own subdirectory. Include KIDs, what already checked, exact new question, actual methods/actions/source URLs/title/authors/revision/commit/locator/independent basis, observed response/payload/checksums, schema/contracts/label examples, rights by layer, counterevidence, conditions, remaining unknowns and practical effect. Use W2-NN-S/F IDs and ordinary URLs (no turn refs); own paraphrases, not copied full pages. Evidence labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown/contradiction. Use local_test only for explicitly logged metadata/parsing/decoding/inference actions actually done; do not imply the last from the first.

For each K record outcome closed/scope_narrowed/contradiction/still_open/superseded with exact basis and what remains experiment/SDK/organizer/permission dependent. A precise remaining gap after useful checks is a valid outcome. No third wave will follow. Final concise handoff: decisive findings, saved path, K outcomes and no-execution limits. Save full individual prompt with any substantive adaptive task change in your own notes, and notify root promptly of material changes.


# Your exact frozen critic assignment

## K005 — приоритетный moving-machine сценарий нельзя ни подтвердить, ни окончательно снять без просмотра наиболее сильного real donor

**Приоритет P0. Тип:** интернет/media/release-scope; реальная near-miss GT, surveyed calibration и permitted test data — внешние gates.

**Затронуто:** M06-F01–F09, D13-F01–F05/F10; D09-F11. NearCollision реально содержит ordered windows/labels/checkpoint, но camera ego target и нет pair IDs/source groups; FP-TTC observation-plane TTC — другая задача. SmartSpaces eleven real video prefixes доступны, но ни один clip не decoded; положительные/отрицательные pair controls неизвестны. Публичный real media release противоречит privacy/Croissant тексту той же revision. D13 правильно различил challenge manual-label rule и универсальную data-license область; исходный unresolved статус нельзя превращать ни в blanket запрет, ни в беспрепятственное разрешение training/relabeling.

**Последствие:** можно ошибочно отказаться от действительно полезного real routine footage либо опереться на несуществующий driver/stationary-near control. Синтетические3D boxes и calibration reprojection «units» не дают независимую real safety GT/метры.

**W2_05 / Medium, `_WORK/W2_05.md`:** (1) по pinned release/current official change log/terms установить точную область real-video release и исключений вне AI City challenge; сохранить противоречие, если первичные тексты не разрешают его; не писать автору. (2) Если grant позволяет такой read/review, получить один-два individual MP4 **одной сцены**, сначала Camera0000, полный hash/decode/PTS и bounded full timeline review. Сохранить фактически видимых людей/технику, motion/stationary/driver-like/occluded segments как preliminary observed inventory, а не certified event GT. Выбирать вторую camera только для полезного наблюдения той же физической сцены; не считать её новым событием или независимыми exposure hours. Не добавлять manual challenge-test annotations для участия и не превращать challenge lockbox в training.

Точные старты: `_WORK/D13/real_tree.json`, `access.json`, `croissant.txt`, `smart_paper.txt`, оба calibration files; base `https://huggingface.co/datasets/nvidia/PhysicalAI-SmartSpaces/resolve/2cbe9563cbe9f47f846e5c871ee994572bbbc60e/MTMC_Tracking_2026/test/Warehouse_026/`, `videos/Camera_0000.mp4` (19 802 011 bytes), `calibration.json`; pinned `README.md`/`croissant.json` у repo root. Official scope sources `https://www.aicitychallenge.org/2026-faqs/` GeneralQ9 и `https://www.aicitychallenge.org/2026-track1/`. Бounded access при404/403 сохранять отдельно от отсутствия объекта.

Для detector звена взять **как вторичный lead** exact `https://huggingface.co/keremberke/yolov8n-forklift-detection/resolve/d8b594f321dd4c64eda16e435601fd266089fc32/best.pt` и publisher `https://github.com/keremberke/awesome-yolov8-models/tree/fb4b7895a92913023ef222fdf0957b8ce2015766`: первично сверить model map0forklift/1person и scope grant/recipe, не повторять всю старую feasibility disassembly. Никакой инференс не требуется.

**Контрдоказательство:** отсутствие separate pedestrians/moving machines или неразрешимый reuse scope оставляет reserve и точный внешний вопрос. Даже если moving-near виден, это не independently certified collision/near-miss/policy violation. Нужны target stationary-near/moving-far/driver/turn/reverse/occlusion controls, ground envelope и actor-pair GT. Forklift-mounted request-only/non-profit paper не закрывается интернет-поиском; не расходовать W2 на его повторное чтение.



Your exclusive report: _WORK/W2_05.md
Your evidence directory: _WORK/W2_05_EVIDENCE/


# Medium W2 researcher — autonomous context

You are a distinct fresh-context gpt-6.1-sol/medium researcher in the SECOND and LAST search wave of behavioral_models_video_data. Sixteen W1 searches completed; a fresh High critic saved K issues in root CRITIC.md before your work. Read your individual assignment, those exact K issues and named saved W1 sources/evidence. Read CASE_NOTES.md for root's direct official-case observation and SYNTHESIS_CONTRACT.md for final coverage. Original two briefs remain authoritative. Do not repeat broad literature surveys. Seek new primary evidence or an independent artifact/source observation that changes the specified decision; extend strong leads with explanation. Do not spawn agents.

Team: five people, Mosprom2026 industrial video safety, mandatory actual neural inference on LinQ, host CPU boundary conditional/unknown, training later on RTX; no issued SDK/device or target video corpus here. Eight scenarios: gait/fast movement, moving machine proximity, prohibited phone, smoking/open flame, barrier/under conveyor/load, height without harness, fall/lying/immobility, carrying rule. Accuracy prioritized but source-time temporal recall/causality and prompt notification remain important. Do not diagnose consciousness, infer physical contact/meters from boxes or attachment safety from belt presence.

Only lightweight documentation/source/metadata/small manifest/annotation/media checks. No training, paid compute/APIs, massive downloads, outreach, source-repo mutations, running untrusted pickle, or fabricated tests. Existing small media may be decoded/reviewed or exact HTTP ranges inspected with bounded timeouts. A byte/access/static check is not model execution or a real event benchmark. Preserve original PTS, source/frame/actor/scene groups and censoring. Code, weights, source videos, annotations and redistribution licenses are distinct. Missing evidence is unknown, not disproven existence.

Save substantial result exclusively to assigned _WORK/W2_NN_*.md and evidence only in your own subdirectory. Include KIDs, what already checked, exact new question, actual methods/actions/source URLs/title/authors/revision/commit/locator/independent basis, observed response/payload/checksums, schema/contracts/label examples, rights by layer, counterevidence, conditions, remaining unknowns and practical effect. Use W2-NN-S/F IDs and ordinary URLs (no turn refs); own paraphrases, not copied full pages. Evidence labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown/contradiction. Use local_test only for explicitly logged metadata/parsing/decoding/inference actions actually done; do not imply the last from the first.

For each K record outcome closed/scope_narrowed/contradiction/still_open/superseded with exact basis and what remains experiment/SDK/organizer/permission dependent. A precise remaining gap after useful checks is a valid outcome. No third wave will follow. Final concise handoff: decisive findings, saved path, K outcomes and no-execution limits. Save full individual prompt with any substantive adaptive task change in your own notes, and notify root promptly of material changes.


# Your exact frozen critic assignment

## K006 — fire/open-flame MVP пока наследует старую supply chain, а новые необходимые negatives не получены

**Приоритет P0, если open fire входит в shortlist; иначе P1. Тип:** адресный первичный artifact/media audit; target authorization policy и реальные factory controls — внешний эксперимент.

**Затронуто:** D14-F02–F05, M01-F012, D09-F13 и provisional fire preference, которую легко импортировать из соседнего feasibility. D14 дал новый smoking/action и MmodalFire lead, но не rechecked fire model+continuous test chain. Это не дефект его работы: ветка сознательно избегала повторения. Синтез текущего research обязан сохранить различие между текущей первичной проверкой и старым отчётом.

**Что доказано:** реальные HMDB smoke videos доступны/decoded, но это не открытый огонь и не dense smoking event GT; маленький smoking model имеет pose/timestamp/split flaws. MmodalFire public metadata/CC BY/4.93GB listed archive и описанные dry-ice/humidifier controls — primary evidence, но actual member/labels ещё не инспектированы. Предыдущий feasibility подробно показывал defects FURG XML, постоянное пламя от начала до конца и отсутствие smoke-only control; повторение тех же5 clips не исправит ignition/cessation/rearm gap.

**W2_06 / Medium, `_WORK/W2_06.md`:** независимо довести **одну** выбранную flame-perception supply chain до exact current primary card/labels/weight grant и bounded static payload confirmation; старые результаты использовать для адресного ограничения, не повторять generic fire detector catalog. Затем получить полный archive manifest и маленький подходящий nonfire mist/dry-ice member MmodalFire, если RAR/non-solid доступ позволяет bounded extraction, проверить labels/clock/полный short interval. Если all files huge/solid/условия мешают — остановить extraction и сохранить exact members/status. Найти в этом же release наличие настоящего onset/clear transition: binary sequence label не трактовать как dense interval. Новая ручная preliminary разметка должна быть отделена от original labels. Огонь на разрешённой печи/сварке, factory steam и inactive/active permit остаются target gates; laboratory mist их не заменяет.

Точные primary starts:

- `https://huggingface.co/rabahdev/fire-smoke-yolov8n/resolve/13017fe8af477c25f5298d168e2dfede4b000753/best.pt` и card этого revision. Это **вторичный lead** из соседнего report, не W1 locally run model. Opposite label maps в чужих fire releases — причина проверить actual map, а не предположить0fire.
- `https://api.figshare.com/v2/articles/28804448`, `https://ndownloader.figshare.com/files/53696243`, `https://www.nature.com/articles/s41597-026-06810-6`; `_WORK/W1_D14_EVIDENCE/mmodalfire_figshare.txt`, `mmodalfire_article.txt`.
- Existing comparison evidence `../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md`, раздел #4, и сохранённые там exact FURG/FIRESENSE locators. Не объявлять этих исходников независимым holdout от D-Fire-trained detector без provenance проверки.

**Контрдоказательство:** нет отдельного model grant/input map, mist визуально слишком иной, labels sparse/sequence-only или отсутствие onset/clear удерживают только narrow flame-region dev path. Даже полный PASS не показывает cigarette/smoker ownership, allowed industrial flame handling, tiny ignition recall, device export или real FP/hour. Smoking и open fire в итоговой матрице — две наблюдаемые задачи внутри одного case пункта.



Your exclusive report: _WORK/W2_06.md
Your evidence directory: _WORK/W2_06_EVIDENCE/


# Medium W2 researcher — autonomous context

You are a distinct fresh-context gpt-6.1-sol/medium researcher in the SECOND and LAST search wave of behavioral_models_video_data. Sixteen W1 searches completed; a fresh High critic saved K issues in root CRITIC.md before your work. Read your individual assignment, those exact K issues and named saved W1 sources/evidence. Read CASE_NOTES.md for root's direct official-case observation and SYNTHESIS_CONTRACT.md for final coverage. Original two briefs remain authoritative. Do not repeat broad literature surveys. Seek new primary evidence or an independent artifact/source observation that changes the specified decision; extend strong leads with explanation. Do not spawn agents.

Team: five people, Mosprom2026 industrial video safety, mandatory actual neural inference on LinQ, host CPU boundary conditional/unknown, training later on RTX; no issued SDK/device or target video corpus here. Eight scenarios: gait/fast movement, moving machine proximity, prohibited phone, smoking/open flame, barrier/under conveyor/load, height without harness, fall/lying/immobility, carrying rule. Accuracy prioritized but source-time temporal recall/causality and prompt notification remain important. Do not diagnose consciousness, infer physical contact/meters from boxes or attachment safety from belt presence.

Only lightweight documentation/source/metadata/small manifest/annotation/media checks. No training, paid compute/APIs, massive downloads, outreach, source-repo mutations, running untrusted pickle, or fabricated tests. Existing small media may be decoded/reviewed or exact HTTP ranges inspected with bounded timeouts. A byte/access/static check is not model execution or a real event benchmark. Preserve original PTS, source/frame/actor/scene groups and censoring. Code, weights, source videos, annotations and redistribution licenses are distinct. Missing evidence is unknown, not disproven existence.

Save substantial result exclusively to assigned _WORK/W2_NN_*.md and evidence only in your own subdirectory. Include KIDs, what already checked, exact new question, actual methods/actions/source URLs/title/authors/revision/commit/locator/independent basis, observed response/payload/checksums, schema/contracts/label examples, rights by layer, counterevidence, conditions, remaining unknowns and practical effect. Use W2-NN-S/F IDs and ordinary URLs (no turn refs); own paraphrases, not copied full pages. Evidence labels author_claim/primary_docs/artifact_found/artifact_access_checked/local_test/inference/hypothesis/unknown/contradiction. Use local_test only for explicitly logged metadata/parsing/decoding/inference actions actually done; do not imply the last from the first.

For each K record outcome closed/scope_narrowed/contradiction/still_open/superseded with exact basis and what remains experiment/SDK/organizer/permission dependent. A precise remaining gap after useful checks is a valid outcome. No third wave will follow. Final concise handoff: decisive findings, saved path, K outcomes and no-execution limits. Save full individual prompt with any substantive adaptive task change in your own notes, and notify root promptly of material changes.


# Your exact frozen critic assignment

## K007 — «каузальный streaming frontend» ещё не даёт task-specific temporal baseline

**Приоритет P1. Тип:** интернет/полный небольшой artifact/static graph; классификация событий, устойчивость state reset и CPU/LinQ стоимость — будущие эксперименты.

**Затронуто:** M08-F01–F06 и conditional route2. MoViNet-A0 Stream обоснован как causal architecture, но получены только headers15MB archive/27MB TFLite, не actual state signature/labels. README construction/current-legacy distinction и численные blog quantized условия не относятся автоматически к checked float binary. K600 classes не разложены на конкретные case semantics; готовый causal network не является pretrained industrial hazard detector. STGCN++/X3D точные sampling-contract flaws уже хорошо установлены; их не нужно заново обозревать.

**Последствие:** команда может выбрать сложный stateful classifier без релевантного head, перепутать per-scene с per-person state, принять накопленную10s classification за onset detector либо объявить blog int8 speed размером реально полученного float binary. Состояния/накопленное pooling могут переживать прекращение действия; causal не равно краткое/локальное/своевременное.

**W2_07 / Medium, `_WORK/W2_07.md`:** получить одну из двух небольших official поставок MoViNet-A0 Stream (предпочтительно TFLite для exact input/state contract), hash/version/storage generation, статически перечислить model signatures, state tensors, их matching input/output shape/dtype, quantization metadata/operators, class-map provenance и relevant/nonmatching case labels. Прочитать exact streaming/export/pooling/reset source pinned revision, объяснить что score фактически аккумулирует и как документация задаёт new-video reset. Не запускать TensorFlow/TFLite inference, модель/benchmark или генерацию ONNX. Отдельно найти, существует ли соответствующая advertised int8 file и explicit grant; если нет, не делать это причиной полного провала float reference. Показать один воспроизводимый first-run контракт и перечень future controls: cold-start, long normal prefix→event→clear, crop/actor/stream reset, state interruption, cadence change.

Точные старты: `https://storage.googleapis.com/tf_model_garden/vision/movinet/movinet_a0_stream.tflite` (27 141 832 bytes); альтернативный `https://storage.googleapis.com/tf_model_garden/vision/movinet/movinet_a0_stream.tar.gz` (15 165 440); `_WORK/M08/movinet.txt`, `artifact_heads.json`, `movinetblog.txt`; `https://github.com/tensorflow/models/tree/master/official/projects/movinet` как mutable locator, затем установить commit exact fetched source. Historical blog `https://blog.tensorflow.org/2022/04/video-classification-on-edge-devices.html` не текущий performance benchmark.

**Контрдоказательство:** signatures требуют неописанный state/layout, отсутствуют relevant labels, source/binary версии расходятся или score имеет неподходящую memory semantics — оставить generic training donor. PASS не показывает целевую superiority над rules, не создаёт target training data и не даёт LinQ поддержки. Nearest class name нельзя переименовать в policy violation.



Your exclusive report: _WORK/W2_07.md
Your evidence directory: _WORK/W2_07_EVIDENCE/


# High collector actual assignment
Agent /root/collector; model gpt-6.1-sol; effort high; fork_turns none. Both waves complete; no new internet evidence.
# Evidence collector — gpt-6.1-sol / high / fork_turns none

Read both original prompts completely, `_WORK/CASE_NOTES.md`, `_WORK/SYNTHESIS_CONTRACT.md`, all 16 W1 reports, all W2 reports, CRITIC.md and task/run logs. You are a separate High assembler after two completed research waves, not a third researcher. No new network calls, inference/training, paid compute, outreach or subagents. Read saved raw evidence as needed.

Sequential ownership: create root SOURCES.md, RAW_FACTS.md, OPEN_QUESTIONS.md; append actual K outcomes to CRITIC.md preserving original criticism verbatim. Do not edit input/branch/sibling files. Six final files total, human/machine reports written by later roles. All other assembly helpers only under `_WORK/`.

Normalize stable S001/F001/K001/Q001/E001 IDs with explicit anchors and working relative links. Preserve a branch→canonical ID map under `_WORK/ID_MAP.md`. Link every significant fact to concrete primary sources and locators, timestamps, commits/revisions and observed access; no internal turn references, no temporary absolute paths, no model-execution claims from source reads. Distinguish inference/hypothesis/unknown/contradiction and source provenance. Dates of publication/access/version are separate. Positive grants and separate unresolved scopes both survive.

SOURCES: exact URLs, authors/title, publication/version/commit, locator, evidence type/status, actual access timestamp, supported F IDs; separately explicit checkpoint/archive/annotation URLs and what was actually retrieved. Do not count copied releases as independent confirmations.

RAW_FACTS: substantial detailed knowledge, all required method/weights/dataset fields from thematic §8 (unknown explicitly), concrete annotation examples and source-to-target semantics, model/video compatibility for all 8 scenarios, negatives, rights/lineage/overlap, causal timing/tracker limits, original benchmark conditions, contradictions and proposed tests. Preserve genuinely useful branch detail; not a short summary with most facts delegated to pointers. A structured table can carry repeated unknown/default fields and long record paragraphs can explain conditions; no need fabricate metrics/VRAM/runtime. Include three conditional method routes and 2–3 candidate MVP shortlist grounded in actual availability/readiness, 1–2 extras only if supported, stop-list and concrete handoffs. A ready development pack is not a blind target industrial holdout.

OPEN_QUESTIONS: precise unresolved Q IDs with priority, what checked and why open, impacted engineering choice, closure via download/license/experiment/SDK/organizer; short first-hours list. Full eight-stage proposed experimental roadmap E IDs: artifact/rights, grouped dataset and negatives, reference CPU/RTX baseline, causal event metrics, ablations, PTS-preserving low FPS/drop tests, geometry/policy controls, later LinQ/export quality delta. Each inputs/actions/expected observations/decision gates/failures/evidence/what PASS does not prove. No arbitrary quality percentage or timing promises.

CRITIC outcomes: closed/scope_narrowed/contradiction/still_open/superseded, exact W2 basis and changed decision. Do not claim documentary closure for an unresolved actual test. Save `_WORK/COLLECTOR_HANDOFF.md` with concise decision picture, registry counts, unresolved contradictions, source-status boundaries and author instructions. Perform appropriate checks as part of your own assembly: unique IDs, known references, links, six-file naming; no separate final auditor. Append actual stage/settings/completion timestamp to RUN_STATE.md. Return paths and findings.


# High author actual assignment
/root/author; gpt-6.1-sol; high; fork_turns none. After complete collector; sources only.
# Russian report author — gpt-6.1-sol / high / fork_turns none

You are the separate author after two waves and High evidence assembly. Read both original briefs fully, CASE_NOTES.md, SYNTHESIS_CONTRACT.md, COLLECTOR_HANDOFF.md, SOURCES.md, RAW_FACTS.md, CRITIC.md, OPEN_QUESTIONS.md; read private branch details as needed. No new internet evidence, paid compute, experiments, source invention, delegation or sibling edits. Write only `_WORK/HUMAN_DRAFT.md`, plus stage log. Later separate editor owns final human report.

Create a substantial connected Russian research narrative for a strong five-person Mosprom2026 team choosing concrete behavioral methods and video evidence on LinQ. Start with consequential established findings and risks, then explain method-artifact-video-label links, limits, eight case scenarios, negatives/data splits, original benchmark conditions, three practical routes and conditional shortlist/stop-list. Include exact checkpoints and direct data URLs where useful but keep full catalogs in RAW_FACTS. Important claims have canonical F IDs/ordinary source links; no claim stronger than assembler evidence. Be candid about rights, domain shift, sampling, future-aware evaluation, actual-test absence and exact LinQ uncertainty.

Provide central eight-scenario matrix with observables, baseline/challenger gates, weights/code, actual video+label/rights, missing negatives, test metrics, FPS/camera/ROI dependence, conditional host/device boundary and first action/stop gate. Explain 2–3 MVP choices and reserves based on evidence, not scenario novelty. Only supported extra hazards; the same generic zone logic is one feature. Integrate proposed eight-stage experiments (inputs, actions, observations, meaningful gates, failures, evidence, what success doesn't prove) and first-hours steps, 3–5 organizer questions and topic handoffs. No arbitrary target accuracy percentages, VRAM or completion guesses; proposed != executed.

Structure freely for comprehension. Clear prose, precise terms, tables for comparisons, no repeated summary boilerplate, no massive disconnected bullet dump, no ungrounded marketing. Preserve all critical status distinctions, open Q and K outcomes, original/access dates and actual roles/limitations. Relative links must remain portable. Self-check coverage and IDs as part of authoring, not a new audit. Save detailed draft, log completion and return concise handoff.


# High editor actual assignment
/root/editor; gpt-6.1-sol; high; fork_turns none. Separate literary editing after author FINAL; no network/audit.
# Russian literary editor — gpt-6.1-sol / high / fork_turns none

You are a separate High editor, not a researcher or final technical auditor. Read both original briefs fully, `_WORK/HUMAN_DRAFT.md`, `_WORK/COLLECTOR_HANDOFF.md`, the four evidence files and `_WORK/CASE_NOTES.md`. Consult saved detail if needed. No network search, new experiments, extra agents or sibling changes.

Own the final `report_human_behavioral_models_video_data.md`. Improve the draft's connected explanation, practical decision clarity and readable Russian. You may restructure substantially but retain factual depth, exact versions/URLs/tensor/class literals/numbers/conditions and canonical F/Q/K/E references. Do not shorten a large useful report into an executive summary. Remove repetition, bureaucratic prose and formulaic AI phrasing; tables for real comparisons; meaningful transitions. Preserve actual checks versus proposed tests, target-data/LinQ unknowns, positive grants versus separate rights questions, benchmark context, all eight scenario coverage, 3 routes, conditional MVP/stop-list, eight-stage experiments and handoffs. Resolve inconsistent prose only from saved evidence; otherwise preserve unknown.

As part of editing, ensure final relative links and ID references are valid and no placeholders/draft comments remain. This is within role, not a new auditor stage. Save final human text, append timestamp/role/status to `_WORK/RUN_STATE.md`, write concise `_WORK/EDITOR_HANDOFF.md` for compressor. Return path and key editorial caveats.


# High compressor actual assignment
/root/compressor; gpt-6.1-sol; high; fork_turns none. Final agreed stage after editor FINAL, no network or separate auditor.
# English machine report compressor — gpt-6.1-sol / high / fork_turns none

You are the separate final compressor in the agreed pipeline, no extra final auditor. Read both original briefs fully, final Russian human report, four evidence files, `_WORK/EDITOR_HANDOFF.md`, `_WORK/COLLECTOR_HANDOFF.md`, `_WORK/RUN_STATE.md` and CASE_NOTES.md. No network research/new tests or subagents. Save root `report_machine_behavioral_models_video_data.md` only; service notes/check outputs under `_WORK/`.

Compact English report with required valid YAML front matter: topic behavioral_models_video_data; concrete scope; not_covered; answers (every item answered in body or explicit unknown/Q); keywords; entity_schema (consistent repeated record schemas or null); takeaways preserving critical conditions; checked_at with actual timezone; context_version mosprom-research-v1. Add accurate full-case provenance, actual verification and non-executed tests, actual role/task count and settings/limits, evidence file paths/human path. No ellipsis placeholders, internal turn refs, stale timestamps or invented source versions.

Preserve significant actionable knowledge in compact form: all eight-scenario compatibility (observables, exact methods/checkpoints and code/weight rights, real videos/annotation semantics/access/rights, missing negatives, tests, sampling/camera risks, host/device condition and kill gate), three routes, conditional 2–3 MVP and reserves/extras only as supported, stop-list, exact artifact/label/timing traps, leaks and splits, benchmark limits, causal event metrics and proposed 8-stage experiment program, first-hours decisions and 3–5 organizer questions, topic handoffs. Important assertions have uniform evidence labels and canonical F references. Each section independently understandable, exact literals preserved, uncertainty visible without Russian report.

Within your own role check YAML parse, answers/body coverage, unique/existing references, relative links, six final names, source/claim scope and no bogus execution. Log performed checks honestly and fix your output; this is not an independent technical audit or third wave. Do not alter sources/briefs/other reports without a specific factual typo requiring owner coordination. Update RUN_STATE with actual completion time and what remains untested; return concise final handoff and recommended user-facing findings. Root will deliver without another checker.
