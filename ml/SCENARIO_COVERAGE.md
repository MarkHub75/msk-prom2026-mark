## Video-first final integration — 2026-10-24 19:31 UTC

Current package: `/workspace/artifacts/matvey-final-20261025/video-first-v2/`.
See `docs/handoffs/VIDEO_FIRST_FINAL_20261025.md` and
`ml/reports/video-first-final-20261025.json`. Main f6b5358a and its ML contract
remain unchanged. New real pretrained smoke0/fire1 model is integrated locally;
no training or new TPU execution. Seven new full scenes:2648frames/5296calls
(3966GPU,1330CPU). Selected package includes three prior scenes:10/3297/7243.
New actual Argus CPU smoke job:408calls,204/407frames/model, event1/evidence1,
API200,48.434s. No app/rule/backend changes. Source DFire30 detector F1 smoke.8333,
fire.8966; overlap/exhaustiveness UNKNOWN, not independent industrial/event GT.
Fire headlight false alert retained. Current S07 Fall03 missed/bedADL10 alert;
not accepted as a successful fall demo.528testsPASS(4skipped). Latest Data
research forklift/person and cigarette ABI candidates are recorded, not promoted.
All assigned agents completed; no own compute jobs. No new automatic experiment.

## Final current-Argus matrix — 2026-10-24

See ml/reports/final-scenario-coverage-20261025.json and final evidence handoff.
Current main f6b5358a unmodified:01/02/03/07 RUNNABLE+PROTOTYPE;04/06/08 BLOCKED;
05PROTOTYPE+BLOCKED (configured spatial subcases vs true climbing/load semantics).
Independent event quality NOT_MEASURED for all8. PPE additional object module,
no Argus rule. Actual local02event1/evidence1/API200, not GT-confirmed violation.
Old8rule synthetic technical freeze below is historical, not proof of current
application/fullscenario TPU quality. Mark alone owns current rules/app.

## Full-scene neural inputs — 24October continuation

7whole GPU videos/770frames/2310calls now available in scene-packs-20261024.
S02:2vehicle/person contexts, S07:2laboratory fall references; S04:2haze contexts
with no specialist, S01:1factory context without running head. This is complete
input observation coverage, NOT qualified event coverage; S08manualcargo blocked.
Only11historicalUR01Poseframes on TPU; other scene/model pairs no LinQ.
Runbook docs/handoffs/SCENE_PACKS_20261024.md; small summary reports/scene-packs-20261024.json.

# Восемь исполняемых прототипов — текущий технический checkpoint

Приоритет изменён срочной директивой пользователя. Точная транскрипция страницы4 официального кейса и SHA источника: `ml/scenarios/catalog.json`. Helmet — дополнительный прежний модуль, вне восьми групп. Полная история baseline сохранена в EXPERIMENTS/EVAL_REPORT и предыдущих Git-коммитах.

Все восемь модулей `evaluate(context, config)` выполняются в одном opt-in конвейере: один существующий BehaviorEngine/трекер людей, общая ассоциация объектов, original-frame координаты, encoded PTS, текущие sourced facts, общий EventCandidate, temporal/dedup, evidence и атомарный SQLite checkpoint. Внешний EventMutation v1 не изменён; новые кандидаты не отправляются Марку как неподдерживаемые типы.

| ID / официальный смысл | Модуль / конфиг | Статусы | Реальные данные и результат | Нейросетевой LinQ / блокер |
|---|---|---|---|---|
|01 Бег по цеху; резкие перемещения в зоне техники | rules/motion.py / 01.json | EXISTING motion helper; PROTOTYPE; RUNNABLE; NOT_EVALUATED current running-action model | CAVIAR run/walk,345saved native frames; новая rule-схема без action-модели возвращает UNKNOWN. Старый motion-proxy TP0/FP0/FN3. ROI E012 running0/46→0/46 — REJECT | Person/Pose раньше status0. Running-action head не квалифицирован; auto-motion требует статичной камеры и политики зоны |
|02 Опасное сближение с движущимися механизмами/транспортом | rules/machinery.py / 02.json | PROTOTYPE; RUNNABLE; BLOCKED full automatic recognition | В16промышленных видео найдены3контекста для review:3_tr45,7_te4,7_tr15. Опасность/GT не подтверждены | Person/Pose раньше status0; техника/движение/политика расстояния не квалифицированы. Stationary/compensated camera required for image translation; не м/с и не метры |
|03 Телефон при оборудовании или перемещении | rules/phone.py / 03.json | PROTOTYPE; RUNNABLE; BLOCKED detector/action | Наличие телефона и использование в просмотре не установлены; нужны owned phone, видимые wrist/head, use и activity context | Phone/use/ownership модель отсутствует; присутствие предмета не равно использованию |
|04 Курение / открытый огонь вне разрешённых мест | rules/fire_smoking.py / 04.json | PROTOTYPE; RUNNABLE; BLOCKED specialist/zone | Раздельные smoking/open_fire. Дымка5_tr19/6_tr15 — UNKNOWN, не огонь/курение. Source-positive не установлен | Нет квалифицированных cigarette/gesture/flame/steam discriminator и permitted-zone policy |
|05 Ограждения / под конвейером / подвешенным грузом | rules/barriers.py / 05.json | PROTOTYPE; RUNNABLE; BLOCKED action/geometry | Три независимых подправила fence_climb/under_conveyor/under_suspended_load; whole-body passage в реальном screen не установлен. Одного line crossing/overlap недостаточно | Person/Pose раньше status0; нужны собственные geometry/provenance + высота/поза/состояние оборудования и observed action |
|06 Высота без использования привязи | rules/height.py / 06.json | PROTOTYPE; RUNNABLE; BLOCKED visibility/use | Height/work region + harness_area_visible + absence/usage. Просто harness present→UNKNOWN; in_use→NEGATIVE, not_in_use/absence при наблюдаемости→POSITIVE. Реальный episode не установлен | Нет wearer-linked harness/use/attachment модели; скрытая привязь/отсутствие аннотации не доказывает нарушение |
|07 Падение / неподвижное лежание на полу / визуальные опасные признаки | rules/fall.py / 07.json | EXISTING; PROTOTYPE; RUNNABLE; EVALUATED source-reference only; quality BLOCKED | UR20same225native observations→1candidate. Fall06: native suspected_fall start1500/confirm2500ms, JPEGframe75 ready; ordinary ADL01→0. Лежание/неподвижность требуют наблюдаемого пола. Не диагноз | Split-Pose раньше status0. Положительный новый candidate — saved-native replay, не TPU на этом эпизоде. Старый hardwareUR01 11calls/0events. GMD4heads export-only, не production |
|08 Переноска груза с нарушением правила — дополнительный | rules/cargo.py / 08.json | PROTOTYPE; RUNNABLE; BLOCKED cargo/ownership/policy | Owned manual cargo + явная запретная carry-zone или наблюдаемое закрытие лица. Вес не выводится по видео. Forklift stacks не подменяют manual-cargo GT | Нет qualified cargo/carry/ownership модели и policy GT |

Пути правил относительно `ml/scenarios/`, конфигов — `configs/scenarios/`. У каждого есть positive/negative/insufficient синтетический тест; всего24приёмочных случая. Ни один сценарий целиком не получает статус LINQ_VERIFIED по одному лишь backbone. `EVALUATED` у07 означает ограниченный source-development endpoint, не промышленную независимую оценку.

## Выбор трёх направлений после покрытия

**07 → 02 → 01** — выбранные направления доведения, не три принятых по качеству распознавателя.

- 07: единственный реальный положительный native-кандидат с привязанным evidence; есть source-reference оценка и прежний LinQ Pose. Низкий baseline recall и отсутствие независимого test остаются.
- 02: реальные промышленные контексты с движением погрузчика и объяснимое правило; требует детектора техники и согласованной опасной геометрии. Это расширение за пределы прежней тройки, выбранное после просмотра.
- 01: доступна actor/time разметка run/walk и проверен backbone. Сейчас детекции бегущих отсутствуют; один заранее ограниченный CPU ROI-эксперимент не улучшил running coverage. Остаётся экспериментальным резервом, не убедительной текущей демонстрацией.

03/04/05/06/08 не выбраны из-за отсутствия подтверждённого действия/наблюдаемости/qualified моделей. Не подбирались «три зелёных» по синтетике. Трёх достоверных автоматических видеосценариев пока нет.

## Проверки и продолжение

480software tests PASS;24synthetic acceptance cases PASS. Реальный data-flow:2промышленных кадра с4сохранёнными correlated LinQ replies, без нового RPC; событие на них не установлено. Видео-screen16/84frames не является GT. Новый ROI1380CPUcalls/173.06s не принят; новых LinQ/GPU/training calls нет. Точность/P-R-F1 по всем восьми не измерена.

Запуск/поля/ручные предпосылки: docs/SCENARIO_RUNBOOK.md и docs/SCENARIO_RUNTIME_CONTRACT.md. Training requests: ml/scenarios/TRAINING_REQUIREMENTS.json + TRAINING_ADDENDUM.json; consumer pointer `/workspace/shared/training-handoff/ML_REQUESTS.json`, REQUEST_ONLY_NO_AUTOSTART. Data/Training worktree не изменены.

Свежий LinQ video-run остаётся заблокирован до own Matvey staging и namespace-aware manifest; старый verified manifest/receipt нельзя переименовать и считать новым размещением. Одна собственная активная задача, уникальные UUID/очереди, без изменений VPN/SSH/captain baseline.
