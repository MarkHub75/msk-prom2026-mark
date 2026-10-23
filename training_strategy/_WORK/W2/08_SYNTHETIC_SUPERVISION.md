# W2-08 — Gen2Det: supervision, artifact gap и exposure contract

K008; P1. Исследование 23.10.2026, 04:37–04:47 UTC / 07:37–07:47 Europe/Moscow; access date 23.10.2026. Модель/роль: gpt-6.1-sol, medium, fresh context. Прочитаны Context-prompt.md, prompt-training-strategy.md, _WORK/PLAN.md, общий блок W2_TASKS и W2-08, общий вывод/внешние неизвестные CRITIC и K008, W1-11 полностью, W1-03 F13/F14/E02, W1-05 F06/F14/F21/F22. Выполнены primary web search/open, read-only HTTP авторских страниц, arXiv HTML и GitHub metadata. Training, генерация, masks, установка стека, inference/export и patch не выполнялись. E ниже — будущая поправка к существующей процедуре, не результат эксперимента.

## Ответ, меняющий решение

**Авторский implementation Gen2Det не установлен после содержательного поиска.** Paper v1 задаёт batch sampling и background-ignore на уровне алгоритма; публичный pinned trainer/config/annotation schema, позволяющий проверить каждую loss term, не найден. Нельзя назвать ordinary folder merge воспроизведением Gen2Det или написать предполагаемый loss patch и приписать его авторам. Доступный команде условный путь — полностью переразмеченный synthetic image pool как обычные supervised данные, после W1-11-E01 и с независимым real holdout W1-11-E02.

**Статус K008:** область уточнена; public-author-artifact gap локализован и остаётся открытым. Условие задания допускает этот результат. Новые первичные ограничения: ignore в paper затрагивает и RPN, и detector head; рабочее значение порога фактически выключает все synthetic background regions; `p` относится к целым batches; low-data COCO не использует filtering/background-ignore. Эти сведения не заменяют actual implementation evidence.

## W2-08-S — источники и фактическое получение

| ID | Первичный источник, дата/версия | URL и локатор | Что получено |
|---|---|---|---|
| W2-08-S01 | Saksham Suri et al., *Gen2Det: Generate to Detect*, arXiv v1, 07.12.2023; UMD/Meta; paper имеет CC BY 4.0 | [version metadata](https://arxiv.org/abs/2312.04566v1), [versioned HTML](https://arxiv.org/html/2312.04566v1), §§3.2–3.4/4.1/4.2.2, Tables 2/5/6, Supplement §6 | Реально открыт web reader; нужный текст дополнительно прочитан direct HTTP. Один paper+supplement, одна цепочка происхождения. Код автора не приложен найденной ссылкой |
| W2-08-S02 | Saksham Suri, author research page; live revision не указан, доступ 23.10.2026 | [UMD author page](https://www.cs.umd.edu/~sakshams/), запись Gen2Det | Web open и HTML просмотрены. У записи Gen2Det только Paper; соседние работы имеют явные Project Page/Code. Не выводим из этого запрет будущего release |
| W2-08-S03 | Animesh Sinha, author research page; live revision не указан, доступ 23.10.2026 | [author page](https://animesh-s.github.io/), запись Gen2Det | Web open/HTML: PDF без code/project. Старая [publication page](https://animesh-sinha.com/publication/) дала web HTTP 502; применён независимый действующий primary путь |
| W2-08-S04 | GitHub REST metadata, access snapshot 23.10.2026; GitHub platform и author account `saksham-s` | [repository-name search](https://api.github.com/search/repositories?q=Gen2Det), [author repositories](https://api.github.com/users/saksham-s/repos?per_page=100) | Direct HTTP JSON: name/description search `Gen2Det` — `total_count=0`; публичный список author account не содержит такого repo. Account установлен по Code-ссылкам author page на `saksham-s/lift` и `saksham-s/SparseDet`. Это metadata-наблюдение, не exhaustive code search |

Search log: точные запросы `"Gen2Det" github code Suri`, `"Gen2Det" project generate detect code`, `"Gen2Det" site:github.com`, `"Gen2Det" site:github.com/facebookresearch`, `"Gen2Det" "implementation" github training`, `"Gen2Det" "code release"`. Прослежены author/paper links и первый author GitHub account. Search выдавал каталоги/пересказы и чужие сравнения, но не author trainer; они не использованы как доказательство метода. Generic ссылки статьи на Detectron2, GLIGEN и XPaste — dependencies/baselines, не Gen2Det implementation. Точный repo SHA/path/function не указан потому, что такой artifact не установлен; подстановка SHA XPaste была бы ложной provenance.

## Новые факты и границы относительно W1

### W2-08-F01 — [LOCAL METADATA OBSERVATION] author release не найден

S02–S04 дают узкий отрицательный результат: открытые publication entries не ведут к Gen2Det code; exact-name repository search и публичный список первого автора не выявили implementation. Это не доказывает, что код никогда не публиковался, отсутствует под другим названием или не существует внутри Meta. Содержательный public поиск завершён при отсутствии новой primary зацепки. Недостающее звено — **author Detectron2/CenterNet2 fork + commit, trainer/config, filtering scripts и сериализованный sample annotations**, а не ещё одна общая статья о синтетике.

### W2-08-F02 — [PAPER] минимальный filtering/supervision contract

S01 §§3.3–3.4/4.1: image filter отбрасывает целое изображение. Instance filter удаляет annotation без достаточно уверенного overlapping detector prediction; pixels остаются, возможны extra instances. Background-ignore охватывает RPN и detector head; `τ_i=0` означает игнорирование всех synthetic background regions. Synthetic mask loss выключен. Это **не** утверждение о class-aware/spatial tensor implementation: class-match condition фильтра, normalization, порядок assignment/sampling/ignore, CenterNet2-specific terms и empty-valid-box handling не установлены.

### W2-08-F03 — [PAPER + OUR DERIVATION] знаменатели ratio различны

S01 §3.4.1/4.1: `p=0.2` — вероятность целиком synthetic batch среди training batches; остальные batches real. Это не доля synthetic objects, не synthetic/real pool ratio и не автоматически 20% файлов в combined folder. В Table 6(c) множитель synthetic data относится к объёму generated sample pool; в Table 6(a) `×` — training schedule. Точный config с абсолютным числом iterations, batch, sample draw/with-replacement, world-size synchronization и mapping этих осей на финальные строки не получен.

**Наша арифметика при явно условных предпосылках:** для `T` optimizer steps с одним batch одинакового размера `B` на step и Bernoulli выбором источника, без accumulation/skips, ожидаемые exposures `E_real=(1-p)TB`, `E_synth=pTB`. При `p=0.2`: synthetic:real exposures `1:4`, synthetic/all `1:5`. Это не равно pool size: даже большой pool может редко встречаться. Если изменение schedule `T0→2T0` действительно применяется к сравниваемому arm, ожидаемая real exposure относительно all-real `T0` равна `1.6`, synthetic — `0.4` baseline-exposure units. Это иллюстрация confound, **не восстановленный бюджет авторской строки**. При accumulation считать фактические source draws и optimizer updates отдельно.

### W2-08-F04 — [PAPER LIMIT] low-data результат не доказывает необходимость полного package

S01 Supplement §6 прямо исключает filtering и background-ignore в LD-COCO из-за малого числа изображений/instances. Поэтому low-data gains W1-11 не являются проверкой «без полного Gen2Det loss синтетика не работает». Напротив, это зависимый от режима recipe. Не переносить full-data setting на few-shot PPE без проверки; не выдавать случайные COCO image subsets за независимые камеры или shots/class.

### W2-08-F05 — [PUBLISHED ABLATION / PROVENANCE] ограничения causal reading

S01 Table 5, **LVIS Mask R-CNN**, box AP: real 22.29, naive mix 20.75, +sampling 23.49, +image filter 23.78, затем detector-filter-only 23.76, background-ignore-only 23.32, совместно 24.42. Здесь последние три arms отсчитываются от sampling+image-filter arm. Отдельные вмешательства не дают монотонного улучшения; нельзя приписать весь gain одному ignore или одному filtering. §4.1 задаёт ImageNet-1k initialization для Mask/Faster R-CNN; §6 — LR 0.04 LVIS, batch 4× default. Table 6 отдельно варьирует schedule. Absolute iterations/input dimensions/hardware, exact sample accounting и checkpoint selection для каждого row не установлены; не выдавать это за matched-budget causal experiment или PPE expected gain.

W1-11-F11 COCO CenterNet2 row происходит из S01 Table 2, не Table 5: авторы в §4.1 говорят, что COCO XPaste evaluation numbers заимствованы из-за отсутствующих соответствующих configs/details; LVIS XPaste rerun сделан ими. Поэтому COCO table — не подтверждение полностью воспроизведённого всеми arms local recipe. Это уточнение происхождения сравнения, не обвинение в недостоверности таблицы.

## Paper → artifact → metadata → assignment/loss: где цепочка обрывается

Таблица ниже — **audit contract и неизвестные**, не предлагаемый patch. С01 даёт словесный алгоритм. S02–S04 не дают проверяемой реализации. Нельзя считать строку «ignore background» доказательством, что вся цепочка работает на любой family.

| W2-08-F06: стадия / term | Что установлено | Какой artifact/metadata нужен; что неизвестно |
|---|---|---|
| Generate → image | Исходные image, boxes, class names обусловливают inpainting, S01 §3.2 | Generated image ID → source image/split, seed/model revision, source boxes. Реальный author schema не найден |
| Image filter | Отбрасывает изображение целиком, S01 §3.3.1 | Keep/drop ID и score/filter revision; нельзя сохранять его labels с другим image |
| Instance filter → annotations | Удаляет неподтверждённую annotation, S01 §3.3.2 | Mapping original→retained/discarded annotation, predictions/reasons; совпадение predicted class с class GT в фактическом code не известно. Текст описывает score+IoU, что не разрешает додумать class condition |
| Pixels discarded/extra objects | Остаются/могут появиться, S01 §3.4.2 | Positive labels не делают остальной кадр verified negative. Extra instances не «исчезают» после JSON filtering |
| Loader/batch source switch | Paper различает real/synthetic batches | Фактическое поле `is_synthetic` или иной equivalent provenance, mapper propagation, loss dispatch неизвестны. Название поля здесь не API автора |
| RPN assignment + objectness | Paper заявляет background-ignore для RPN | Где создаётся bg/fg label, меняется ли до/после anchor/proposal sampler; сохраняется ли count denominator; какие confident foreground scores используются — неизвестно. Нельзя объявить RPN negatives автоматически решёнными только по RoI mask |
| RPN box regression | Paper не даёт tensor trace | Какие positives остаются после filtering и способ normalization не проверены. Нельзя утверждать, что discarded regions дают нулевой градиент всем параметрам |
| RoI/detector classification | Paper заявляет detector-head bg-region ignore | Background sample ignore и suppress всех negative class entries на positive RoI — разные операции. Class-specific negatives, federated/softmax/sigmoid distinction и spatial scope вне retained positives не установлены |
| Detector box regression | Имеются retained box annotations; exact assignment не показан | Matching targets, sampling positives, ignored GT treatment, empty targets и reduction неизвестны |
| CenterNet2/иные stages | Paper использует адаптированный instance-segmentation CenterNet2 | First-stage heatmap/objectness, stages каскада, dense unmatched locations: actual modified terms не найдены. Нельзя приравнять к standard RPN или перенести на one-stage BCE/DFL |
| Synthetic mask loss | Выключен в paper | Должна отсутствовать попытка использовать старую маску после inpainting; exact conditional dispatch/reduction не известны. Real mask supervision не объявляется выключенным |
| Synthetic image без valid boxes | Paper не определяет реализацию edge case | Может loader отбросить кадр, head вернуть zero или он дать иной loss; ни один вариант не установлен. Не превращать в hard negative |
| Eval/final artifact | Описаны изменения данных/training, не новая inference branch, S01 §§3–4 | Paper-level ожидание обычного detector. Final eval graph/config/checkpoint extraction, отсутствие training-only dependencies при reload/export actual кодом не подтверждены |

**W2-08-F07 [OUR INFERENCE] spatial/class scope.** При `τ_i=0` словесный scope — все background regions synthetic image, а не только исходные discarded boxes или конкретные filtered classes. Это существенно шире «поставить ignore rectangle на удалённую annotation» и может охватывать hallucinated extra instances. Но bg-region определяется конкретным assigner; невозможно по этой фразе доказать отсутствие negative supervision для другого класса в retained positive region или другого stage. Для `τ_i>0` scope ещё зависит от confidence текущего detector. Указание RPN в paper опровергает удобное упрощение «достаточно поправить один classification head»; actual поведение остаётся Q01.

## W2-08-F08 — matrix допустимых маршрутов и final graph

| Route | Annotation/negative contract | Trainer и окончательный artifact | Решение сейчас |
|---|---|---|---|
| Fully reviewed synthetic | Reviewer проверяет весь кадр, все рабочие classes/instances, extra objects и состояния; исправляет boxes; mask только если реально переразмечена. Negative label допустим лишь после полного review в заданной policy | Обычный выбранный supervised detector с полностью поддержанным annotation format. Данные — единственное вмешательство; архитектура inference не меняется по нашему design. Final checkpoint должен пройти обычные reload/export/LinQ gates | Допустимый будущий data-only trial после real baseline; это наша процедура, не Gen2Det reproduction |
| Filtered pseudo synthetic, special loss | Неисчерпывающие labels; нужны source tag, surviving labels, mask availability и реально обработанный missing-object supervision во всех affected stages | Нужен author fork+commit/config или отдельно проверенная интеграция. Gen2Det paper задаёт intent, но available implementation/port не установлен; final graph также требует artifact inspection | Не ставить в тренировочную очередь до Q01 и hidden-GT correctness gate W1-03-E02 |
| Unsupported union filtered labels + ordinary closed-world trainer | Оставшиеся pixels и extra instances могут стать negatives; JPG/JSON conversion теряет provenance/coverage | Архитектура может остаться обычной, но это не делает supervision корректным | Не использовать как воспроизведение; перевести в fully reviewed route или остановить |

Fully reviewed означает исчерпывающе в заранее указанной annotation policy (class/ROI/visibility/size); не обещает знать невидимые PPE states. Если policy требует ignore unknown, а trainer его не поддерживает, crop/exclude весь sample по допустимой семантике либо доразметить; не молча записывать unknown как background. Group person+PPE semantic gate из W1-11 остаётся нашим предложением, не техникой Gen2Det.

Для data-only route генератор/filter/reviewer и их models не нужны во время inference. Это вывод из предложенного собственного route, где архитектура фиксирована, а не подтверждённый author export. Для paper route нет основания требовать diffusion model на inference, но нет и inspected artifact, доказывающего clean reload. Ни один маршрут не устанавливает LinQ compiler/operator compatibility или качество wearing/smoking.

## W2-08-E01 — контролируемое дополнение W1-11-E02, не отдельный обязательный grid

**Вопрос/решение:** даёт ли полностью reviewed synthetic pool новую информацию для заранее определённого real failure slice; не получен ли apparent gain из изменения real exposure, updates, masks или selection?

**Входы:** W1-11-E01 прошёл; выбранный model_stack checkpoint+hash, pinned supervised trainer, class/ignore convention и graph; один real train manifest; derived synthetic assets с train-only provenance и полноценным review; независимые real validation/lockbox camera/session/clip groups. Те же реальные splits, что в W1-11-E02. Masks не наследовать из исходного inpainted image. Если baseline segmentation требует масок, нужен подтверждённый mixed-supervision criterion либо новые verified masks; bbox data-only route не выдавать за segmentation recipe.

**Основные arms:** A real-only и B real+reviewed-synthetic; одинаковые initialization, input/preprocessing, effective batch, optimizer-update budget, augmentation policy, validation objective, inference thresholds/NMS/event rules. Сохранять **фактический** per-source draw ledger, не только `epochs` и список файлов. Не утверждать одновременно equal updates и equal real exposures при фиксированных batch и ненулевом synthetic replacement: эти constraints несовместимы без дополнительных изменений.

**Минимальная поправка accounting:** заранее выбрать primary estimand — gain при равном числе updates либо gain при равном real exposure. Записать `T_optimizer`, `N_real_draws`, `N_synth_draws`, real unique IDs, synthetic unique IDs/source-layout counts, empty/rejected batch counts, accumulation и skipped updates, LR progression, mask-active counts, human review minutes, `T_setup/T_train/T_validate/T_export`. Pool ratio `N_synth_unique/N_real_unique`, draw fraction `N_synth_draws/(N_synth_draws+N_real_draws)` и `p_batch` — три разных поля.

**Условный дополнительный контроль:** только если B меняет решение, но attribution неоднозначна, провести comparison с matched-real-exposure schedule и отдельным all-real update control, выбрав заранее, какая неопределённость важнее. Например для replacement sampling можно удлинить B до сохранения real draws A, но тогда обязательно указать большее число updates и изменённый LR path; это не «тот же бюджет». Не считать real oversampling волшебным способом одновременно выровнять все знаменатели. Сравнение по wall-clock — иной practically useful estimand, тоже маркировать отдельно. Не назначать все arms заранее.

**Наблюдения/артефакты:** как в W1-11-E02 — real critical recall/AP, false positives/alerts на real negatives, class/size/occlusion/camera slices; checkpoint selection только по real validation, final lockbox после принятия решения. Дополнительно source ledger, review decisions включая discarded/extra objects, annotation coverage после import, masks/labels overlays после final resize, config diff и candidate hash. Synthetic validation не заменяет real evaluation.

**Исходы/stop:** gain на real critical slice без недопустимого regression → candidate на обычный export/target gate; gain только на synthetic или неотличимый от repeats/schedule → синтетическая польза не установлена; broken semantics/partial coverage/unknown supervision → блокировать B до исправления данных. Если review/integration занимает больше полезного remaining critical path, выбрать real annotation, а не увеличивать pool. Успех подтверждает только данный reviewed dataset/recipe; не доказывает Gen2Det implementation, generalization новой камеры, событийную безопасность или LinQ execution.

**Будущий controlled amendment для special-loss route:** если получен Q01 artifact, использовать существующий W1-03-E02, без изобретённого patch. Добавить provenance switch real↔synthetic, retained/discarded/extra instances одного и разных classes, images с нулём retained GT, все RPN/first-stage/RoI/dense class negatives, regression/mask/reduction observables, assignment до/после sampling, final graph reload. Пройти correctness до quality trial. До получения артефакта это interface request, не реализованный протокол Gen2Det.

## Оставшиеся вопросы и адресная передача

| ID / тип / приоритет | Точный gap и как закрыть | Решение/получатель |
|---|---|---|
| W2-08-Q01 — author artifact, P1 | Получить author release/fork+commit, exact configs и filtering→serialized dataset examples; проследить class matching, empty images, source metadata, все affected losses/reductions, sampler и final checkpoint. Искали S01–S04; public code не найден. Новый поиск только при новой первичной ссылке/выдаче артефакта, не бесконечный поиск по тому же названию | → model_stack; special-loss synthetic сейчас не concrete recipe. K008 остаётся с этим gap |
| W2-08-Q02 — case/data, P0 для trial | Ontology, review scope, unknown/ignore/visible masks, независимый real holdout и допустимые train backgrounds ещё не получены. Нужны dataset audit/полный кейс и review pilot | → datasets/violation_methods; разрешает fully reviewed route либо делает real annotation первым выбором |
| W2-08-Q03 — experiment, P1 | Полезна ли синтетика относительно real correction/annotation при фактических human minutes и target failure slice? Закрывается W1-11-E01/E02 с W2-08-E01 accounting | → evaluation/очередь W2-12; publication AP не задаёт expected benefit или optimal ratio |
| W2-08-Q04 — artifact/SDK, P1 | Какой именно final detector graph и export реально принимает выданный LinQ? Нужны выбранный checkpoint/config и actual target toolchain; для special-loss author route сначала Q01 | → linq_platform/model_stack; data-only design сохраняет архитектуру, но не гарантирует исполнение |

Для сборщика: сохранить W1 отрицательный naive-mix результат; дополнить его stage scope и sampling denominator. Не подменять «код не найден» утверждением «loss невозможно реализовать». Low-data COCO — важная поправка универсальному толкованию package. W1-11-E02 остаётся основной future quality процедурой; W2-08-E01 уточняет её exposure controls и не увеличивает автоматически очередь trials.
