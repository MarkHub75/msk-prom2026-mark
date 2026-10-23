# W1-07 — Смешивание источников, перенос домена и новая камера

Дата исследования: 2026-10-23, полученное время 03:49:24 UTC / 06:49:24 Europe/Moscow; сетевое чтение продолжалось после этой отметки. Это дата доступа, не дата публикации. Контекст: mosprom-research-v1. Ветка выполнена чтением первичных публикаций и авторского кода; обучение, инференс, скачивание весов и проверка LinQ не выполнялись. Полный кейс, реальные target-данные и SDK отсутствуют в переданном контексте.

## Решение для команды

**Наш вывод:** начать с проверки исходного детектора по камерам и сессиям. Если есть проверенная целевая разметка, первой проверкой сделать обычное target fine-tuning против source+target mixing. Если есть только целевое видео, отделить режим с доступным source от source-free: у них разные входы и реализации. Сложный domain-adaptive trainer оправдан после проверки таксономии, teacher errors и стоимости интеграции. Ни одна просмотренная работа не устанавливает выигрыш на PPE/промышленном CCTV, конкретном YOLO либо исполнимость на LinQ.

Под domain shift здесь понимается изменение изображения и условий наблюдения: ракурс, освещение, компрессия, размер объекта, фон, плотность людей. Отличие смысла labels — например, «каска» против «правильно надета каска» — нельзя автоматически устранить выравниванием признаков. Наличие нужного визуального сигнала и class-map является отдельным условием.

## Источники и точные локаторы

Все источники ниже открывались 2026-10-23. Статус «код» означает чтение, без запуска. SHA получены через GitHub API, затем использованы в raw URL. Наименования файлов и строк относятся к указанным ревизиям.

| ID | Первичный источник, версия / дата | Прямой URL и локатор | Статус и назначение |
|---|---|---|---|
| W1-07-S01 | Chen et al., *Domain Adaptive Faster R-CNN for Object Detection in the Wild*, CVPR 2018; arXiv v1 2018-03-08 | https://arxiv.org/abs/1803.03243 ; https://arxiv.org/pdf/1803.03243 ; §§3–4, Fig.2 | Paper PDF открыт через arXiv; механизм UDA detection |
| W1-07-S02 | Автор yuhuayc/da-faster-rcnn, SHA `3193b657c06ac8a29f8a091a0367a75c599d4803`, commit 2019-10-09T15:37:19Z | https://raw.githubusercontent.com/yuhuayc/da-faster-rcnn/3193b657c06ac8a29f8a091a0367a75c599d4803/README.md ; Usage, lines 15–33 | Авторская реализация, Caffe/pycaffe |
| W1-07-S03 | Li et al., *Cross-Domain Adaptive Teacher for Object Detection*, CVPR 2022; arXiv:2111.13216 v3 2022-05-11, v1 2021-11-25 | https://arxiv.org/abs/2111.13216 ; авторский final PDF https://yujheli.github.io/projects/CVPR2022_assest/paper_adaptive_teacher_cvpr22.pdf ; §§3,4.1–4.5, Tables3–5 | Авторский PDF открыт. Его точная бинарная идентичность arXiv v3 не проверялась |
| W1-07-S04 | facebookresearch/adaptive_teacher, SHA `5256463ad9ec90fd5ba84ebb8d53bed56bd369df`, commit 2023-04-03T06:14:40Z | https://github.com/facebookresearch/adaptive_teacher ; README Prerequisites, tested environment, Results, License; https://api.github.com/repos/facebookresearch/adaptive_teacher/commits/main | Прочитаны README и metadata; архивирован 2023-10-31 |
| W1-07-S05 | AT, тот же SHA, `adapteacher/engine/trainer.py` | https://raw.githubusercontent.com/facebookresearch/adaptive_teacher/5256463ad9ec90fd5ba84ebb8d53bed56bd369df/adapteacher/engine/trainer.py ; `build_train_loader`, `threshold_bbox`, `run_step_full_semisup`, `remove_label`, lines343–346,378–430,452ff | Код: два домена, weak/strong, pseudo-label/EMA training |
| W1-07-S06 | AT, тот же SHA, `configs/faster_rcnn_VGG_cross_city.yaml` | https://raw.githubusercontent.com/facebookresearch/adaptive_teacher/5256463ad9ec90fd5ba84ebb8d53bed56bd369df/configs/faster_rcnn_VGG_cross_city.yaml ; весь файл, lines0–50 | Буквальная recipe, не универсальные defaults |
| W1-07-S07 | AT, тот же SHA, `train_net.py` | https://raw.githubusercontent.com/facebookresearch/adaptive_teacher/5256463ad9ec90fd5ba84ebb8d53bed56bd369df/train_net.py ; `main`, lines31–48 | Evaluation выбирает teacher из ensemble checkpoint |
| W1-07-S08 | AT, тот же SHA, `adapteacher/modeling/meta_arch/rcnn.py` | https://raw.githubusercontent.com/facebookresearch/adaptive_teacher/5256463ad9ec90fd5ba84ebb8d53bed56bd369df/adapteacher/modeling/meta_arch/rcnn.py ; `DAobjTwoStagePseudoLabGeneralizedRCNN.forward`, lines128–184 | Код: inference и domain branch; не проверка экспортера |
| W1-07-S09 | Saito et al., *Strong-Weak Distribution Alignment for Adaptive Object Detection*, CVPR2019; arXiv:1812.04798 v3 2019-04-05 | https://arxiv.org/html/1812.04798v3 ; §§1,3.3,4,4.1, Tables1–2 | Полный первичный HTML открыт; negative transfer и transductive protocol |
| W1-07-S10 | Xianfeng Li et al., *A Free Lunch for Unsupervised Domain Adaptive Object Detection without Source Data*, AAAI2021, публикация 2021-05-18; arXiv v1 2020-12-10 | https://ojs.aaai.org/index.php/AAAI/article/view/17029 ; https://cdn.aaai.org/ojs/17029/17029-13-20523-1-2-20210518.pdf ; Introduction, Proposed Approach, Implementation Details pp.8478–8479 | PDF и publisher page открыты; SFOD требует source-trained model, не source images при adaptation |
| W1-07-S11 | RoyChowdhury et al., *Automatic Adaptation of Object Detectors to New Domains Using Self-Training*, CVPR2019; arXiv:1904.07305, 2019-04-15 | https://arxiv.org/pdf/1904.07305 ; abstract, §§3–4 | Открыт PDF; tracking для hard positives, face/pedestrian boundaries |
| W1-07-S12 | Автор AruniRC/detectron-self-train, SHA `a5d0edc51aeab92b953948ef2401294e87efb719`, commit 2019-06-12T21:45:53Z | https://raw.githubusercontent.com/AruniRC/detectron-self-train/a5d0edc51aeab92b953948ef2401294e87efb719/README.md ; Requirements, BDD Hard Examples, Models | Авторская реализация и отсутствующий mining pipeline |

### Доступ и ограничения источников

CVF HTML и PDF для Chen2018 и Li2022, а также PDF Saito2019 возвращали инструменту `403 Forbidden`; вместо пересказа search snippets прочитаны arXiv PDF, авторский PDF и arXiv HTML соответственно. Авторский AT PDF доступен. Попытка screenshot страницы5 SFOD PDF завершилась `TimeoutError`; текст PDF доступен, численные результаты SFOD ниже не используются. Screenshot AT страницы6 получен инструментом, но численная база здесь опирается на извлечённый текст и code/README, без заявления о ручной визуальной сверке таблицы. Версии GitHub установлены локальным read-only запросом API; дата доступа отличается от даты commit. Для SFOD2021 авторский репозиторий по выполненным поискам не установлен; это не доказательство отсутствия кода.

## Факты, наблюдения и границы переноса

Легенда: **published** — опубликованное авторами описание/измерение; **code** — наше чтение конкретной ревизии; **local** — фактически выполненное здесь действие; **inference** — наш вывод; **proposed** — будущая проверка. Все результаты статей принадлежат авторам.

### W1-07-F01 — Классическая UDA detection требует двух доменов

**published**, S01 §§3–4: DA Faster R-CNN добавляет image- и instance-level domain classifiers с adversarial training и consistency regularization к двухэтапному детектору. Source размечен, target без supervised labels. **code**, S02 Usage: реализация основана на `py-faster-rcnn`, требует Caffe/pycaffe; source/target различаются префиксами имён. Это конкретная историческая training implementation, а не опция современного YOLO. **inference:** отключение source-loader не превращает этот метод в source-free. Отдельное доказательство совместимости trainer/backbone/head и экспорта требуется до практической очереди.

### W1-07-F02 — Adaptive Teacher: сильное измерение с узкими условиями

**published**, S03 §§3–4, Table3: AT соединяет teacher/student, weak/strong augmentation и adversarial alignment. Cityscapes→Foggy Cityscapes: Faster R-CNN/VGG16, ImageNet initialization, 8 классов; source train2975, target train без labels, target validation500. Авторы сообщают mAP50.9% против source-only23.5% и своего target-supervised oracle42.7%. Paper: shorter side600, SGD LR0.04, source warm-up10k + mutual learning50k, EMA0.9996, threshold0.8; 8V100, batch16. Точный checkpoint-selection protocol не установлен. Table4 отдельно исследует unseen artistic domain, шесть общих классов, R101. **Граница:** обычная адаптация к target и domain generalization — разные эксперименты; «oracle» здесь лишь конкретная supervised baseline.

### W1-07-F03 — Цена воспроизведения AT и ограничения лицензии

**code / author documentation**, S04: README указывает `Detectron2 == 0.3`, Python≥3.6, PyTorch≥1.5; tested environments8V100 и4×2080Ti. Лицензия проекта указана CC-BY-NC4.0. Часть весов/результатов в README обозначена `coming soon`, для internal weights предупреждается о несовпадении key names. **inference:** наличие репозитория не подтверждает загрузку совместимого checkpoint. Лицензионную применимость к сдаче/дальнейшему продукту нужно решить отдельно, до заимствования кода; это не установленный запрет нашего кейса.

### W1-07-F04 — Actual recipe отличается от paper

**code**, S06: `META_ARCHITECTURE: DAobjTwoStagePseudoLabGeneralizedRCNN`, `PseudoLabRPN`, `StandardROIHeadsPseudoLab`, `NUM_CLASSES: 8`; `IMG_PER_BATCH_LABEL: 16`, `IMG_PER_BATCH_UNLABEL: 16`, `BASE_LR: 0.04`, `MAX_ITER: 100000`, `BURN_UP_STEP: 20000`, `BBOX_THRESHOLD: 0.8`, `EMA_KEEP_RATE: 0.9996`, `UNSUP_LOSS_WEIGHT: 1.0`. Datasets: `cityscapes_fine_instance_seg_train`, `cityscapes_foggy_train`; test `cityscapes_foggy_val`; `EVAL_PERIOD: 1000`. Файл содержит повторный ключ `DATASETS:` — значение parsing здесь не запускалось. **inference:** paper10k+50k и текущий config20k/100k нельзя объединять в одну якобы воспроизведённую recipe. При повторении фиксировать commit и реально resolved config.

### W1-07-F05 — Training loop и итоговый inference артефакт AT

**code**, S05: loader выдаёт labeled/unlabeled strong/weak views; до `BURN_UP_STEP` идёт supervised burn-in; после него teacher копируется/обновляется, target labels снимаются, pseudo boxes фильтруются confidence threshold. В lines572–589 `loss_rpn_loc_pseudo` и `loss_box_reg_pseudo` умножаются на0, discriminator losses — на `DIS_LOSS_WEIGHT`. Это изменения loader, trainer и loss, а не смешивание YAML-путей. **code**, S07: `--eval-only` строит teacher/student ensemble для загрузки checkpoint и вызывает `Trainer.test(...modelTeacher)`. **code**, S08: при eval `forward` переходит в `self.inference`; domain-loss branch отдельно. **inference:** при deploy нужен выбранный teacher detector и корректное извлечение весов. Не нужен онлайн adaptation loop по этому evaluation пути, но экспорт, удаление training-only state и исполнение такого графа нами не проверены. У других DA методов ситуация иная: S09 §3.3 явно использует context vectors при test; нельзя объявлять все domain branches удаляемыми.

### W1-07-F06 — Negative transfer существует в object detection, включая source degradation

**published**, S09 §§1,4–4.1 Tables1–2: Faster R-CNN/R101, ImageNet, VOC2007+2012 trainval→Clipart,20 классов. В авторском сравнении target mAP source-only27.8%, global BDC25.6%; source VOC77.5%→73.6%. Strong matching глобальной сцены может вредить при различии layout/object co-occurrence. Short side600,70k iterations (50k LR0.001 +20k LR0.0001), minibatch1source+1target; reported final checkpoint. Hardware/seeds не установлены. Строка DA-Faster19.8% — их reimplementation без consistency, а не исходное измерение Chen. **Критично:** все1000 Clipart images участвуют в unlabeled training и testing; это transductive оценка. Её нельзя выдавать за независимую новую камеру. IoU convention по прочитанному фрагменту точно не установлена: сохраняем авторское mAP, не переименовываем в COCO AP50:95.

### W1-07-F07 — Source-free не означает отсутствие исходного знания и не гарантирует quality gate

**published**, S10: SFOD2021 использует source-trained Faster R-CNN/VGG16 с ImageNet initialization; source samples нужны на pretrain, при adaptation не используются. SED выбирает pseudo-label threshold через self-entropy, затем Mosaic моделирует трудные пропуски. Авторы отдельно указывают noisy pseudo-labels и false negatives малых/окклюдированных объектов. Implementation: short side600, SGD LR0.001, batch1; source-only/oracle оцениваются на target validation. Compute/checkpoint-selection в этом чтении не установлены. **inference:** self-entropy — внутренняя proxy, не независимая проверка recall/FP. Для промышленной эксплуатации отсутствие target labels не позволяет доказать полезность adaptation по одному снижению entropy. Реализация под наш detector не установлена.

### W1-07-F08 — Temporal mining может искать пропуски, но готовый trainer не равен всей pipeline

**published**, S11 abstract/§§3–4: авторы используют confident detections, tracking для hard positives и soft-label distillation; задачи — лица WIDER→surveillance и pedestrians BDD clear/day→другие условия. Это основание рассмотреть временной сигнал, а не доказательство переноса person tracks на каску/сигарету.

**author documentation**, S12: hard-positive mining на100k videos занял у авторов около недели на UMass GPU cluster; pipeline mining не включён, предлагаются извлечённые frames/pseudo-labels. Train scripts рассчитаны на4GPU; README single-model results отличаются от paper averages over5 rounds. **inference:** нельзя обещать готовый быстрый end-to-end mining по наличию training scripts. В нашем случае tracker может продлевать ошибочный объект; временная устойчивость не подтверждает правильный класс.

### W1-07-F09 — Локальный статус проверки

**local:** выполнены primary search+open, прочитаны перечисленные PDF/HTML/raw code, получены SHA/dates через GitHub API. Не выполнялись: training/benchmark, установка авторских зависимостей, проверка complete dataset files, download weights, inference/export, измерение VRAM или LinQ. **inference:** ниже — порядок принятия решений и предложенные абляции, без обещания процента выигрыша или времени на RTX4070.

## Условная карта source/target

Это **proposed / inference**, основанное на различии постановок F01–F08. «Source доступен» означает право и техническую возможность читать изображения с корректными annotations; наличие checkpoint само по себе недостаточно.

| Реальные входы | Первый полезный маршрут | Следующая ветка при положительном gate | Что запрещено считать доказанным |
|---|---|---|---|
| Нет target images; есть source или готовые weights | Source-only baseline; целевые условия пока только гипотезы | Собрать независимый camera/session audit после выдачи данных | Domain adaptation уже выполнена; robustness на новой камере |
| Target labels есть, source доступен | Target-only fine-tuning против mixing; одинаковый стартовый checkpoint | Менять sampling source/target только по validation; проверить forgetting на old domains | Больше source всегда полезнее; общий mAP заменяет camera/class slices |
| Target labels есть, source недоступен | Target fine-tuning с сохранением frozen исходного кандидата | Distillation/replay-free regularization только при отдельной реализации и gate | Возможно измерить source forgetting без source/old-domain holdout |
| Target labels нет, source доступен | Аудит frozen detector и небольшая target разметка для измерения; adaptation pool отдельно | UDA teacher/student либо audited offline pseudo-labeling, если trainer реально поддержан | Unlabeled target можно загрузить как обычные полностью отрицательные изображения |
| Target labels нет, source недоступен, source weights доступны | Frozen baseline; ручная выборочная проверка target ошибок | Source-free self-training как рискованная отдельная ветка | AT без source является тем же алгоритмом; entropy доказывает качество |
| Нет target labels и нельзя создать независимые labels даже для проверки | Можно исследовать доступность/покрытие prediction и сохранять frozen fallback | Только предварительная демонстрация, с явно непроверенным quality improvement | Доказано улучшение recall, безопасность или снижение FP |

Если новый target содержит отсутствующий в head класс, это прежде всего supervised class extension / другая модель. Closed-set domain adaptation не даёт новой семантики из отсутствующего сигнала. Если источники различаются полнотой разметки, class-map и exhaustive/partial status проверяются до смешивания; иначе background loss может наказывать реальные неразмеченные объекты. Детальный loader/partial-label путь передаётся W1-03/model_stack.

## Протокол новой камеры и transductive exposure

**W1-07-F10 — proposed protocol, не результат статьи.** В manifest у каждого файла нужны `camera_id`, `session_id`, временной диапазон, source dataset, group/track identifiers при наличии, доступность labels и роли использования. Разбить до отбора кадров, pseudo-labeling, аугментаций и ручного mining. Соседние кадры одного эпизода не распределять случайно по ролям. Хэш-дубликаты и одно и то же исходное видео должны оставаться в одной группе; производные (crop/translated/augmented) наследуют её.

Роли следует различать:

1. **Adaptation pool:** данные разрешены для gradient updates, teacher pseudo-labels, style/BN statistics, image translation и любого выбора обучающих примеров.
2. **Selection validation:** отдельные размеченные sessions для выбора mixing ratio, threshold, checkpoint и решения о продолжении. Если labels здесь существуют, режим не следует описывать как полностью zero-target-label model selection.
3. **Independent new-session test:** поздняя/другая сессия адаптируемой камеры, изображения которой не использовались ни в adaptation, ни в настройке.
4. **Independent new-camera test:** камера, исключённая полностью, включая unlabeled exposure. Только этот режим поддерживает вывод о переносе на ещё одну камеру; при одной камере его сделать невозможно.
5. **Old-domain retention:** отдельный holdout исходных/ранее работающих камер, если сохранение их качества требуется.

Можно отдельно измерить transductive режим, когда test images использованы без labels. Тогда явно сообщать, какие изображения и statistics были видны модели и как. Не объединять его число с independent новым-camera результатом. Если real deployment предполагает предварительный доступ ко всем неразмеченным видео данной камеры, transductive режим может быть релевантен этой постановке, но не подтверждает перенос на неизвестную будущую сессию. Пороговые настройки событий и геометрия опасной зоны также относятся к camera-specific adaptation: фиксировать их отдельно от обучения detector.

При слабом количестве независимых sessions полезнее честно показать paired differences по группам и характер ошибок, чем объявлять тысячи соседних кадров большим independent test. Набор ручного аудита pseudo-labels внутри adaptation pool служит контролю data quality; он не заменяет independent validation/test.

## Предлагаемые практические процедуры

Ни одна процедура не запускалась. Значения budget/steps и минимального выигрыша ниже команда задаёт **до** просмотра validation outcomes, исходя из действительных классов и времени. Это исключает выдуманный универсальный schedule. Выполняемые CLI не приводятся: реальный model_stack и окружение неизвестны.

### W1-07-E01 — Target fine-tuning или source+target mixing

**Гипотеза / решение:** source replay помогает сохранить старые камеры, но может мешать target; сравнить с target-only прежде, чем внедрять adversarial trainer.

**Входы:** проверенный model/checkpoint/version от model_stack; target train с исчерпывающей разметкой, class-map source/target, source train с правами использования, selection validation и old-domain retention, полностью скрытые new-session/new-camera группы. Если source недоступен — оставить только frozen и target-only; это другая процедура сравнения, без утверждения об эффекте mixing.

**Контроль:** один initialization, head, preprocessing/resolution, augmentation family, optimizer, total update budget, seeds, validation schedule и NMS. Основная сетка — frozen baseline; продолжение source-only на том же update budget; target-only; mixing с заранее заданной долей target (например0.5) плюс один target-heavy вариант (например0.75). Эти доли — проект эксперимента, не paper-recommended optimum. У всех обучаемых кандидатов зафиксировать число source/target exposures и уникальных групп; mixing при фиксированных updates меняет target exposure, что является частью вмешательства. При спорном результате сделать отдельный exposure-matched контроль, не объявляя его тем же cost-matched опытом.

**Действия:** проверить loader/class coverage; выполнить небольшой controlled run; выбрать checkpoint только по selection validation; разложить ошибки по классам, размеру объектов, камерам и освещению. На независимый test выпускать только выбранного кандидата и frozen baseline. До старта согласовать target primary metric и допустимую потерю old-camera качества; event metrics рассчитывать при одинаковых правилах событий.

**Метрики:** detection AP с явно фиксированным IoU convention; critical-class recall при фиксированном приемлемом FP уровне либо FP/hour при фиксированном recall; old-domain delta; per-camera/session paired delta; unique groups, annotations/объекты, GPU wall-clock и ручные затраты. Если event labels отсутствуют, не выдавать detection FP за FP/hour события.

**Артефакты:** split manifest с ролями и hashes; class mapping/annotation coverage; resolved config; checkpoint и selection criterion; seeds; exposure counts; логи; prediction files на одних и тех же кадрах; ошибки old/target; environment versions.

**Исходы / stop rule:** mixing выигрывает target и соблюдает retention gate — оставить; target-only выигрывает без запрещённого forgetting — выбрать его; выигрыш находится только на адаптационных кадрах — считать memorization/leakage warning, вернуться к группировке. Остановить ветку при нарушении semantics/labels, критическом падении класса, превышении заранее установленного integration/training budget, либо отсутствии целевого улучшения сверх выбранного practically meaningful threshold после запланированной сетки. Не продолжать ratios до случайного попадания в validation. Положительный результат ещё не подтверждает LinQ, unseen site, rare class reliability или устойчивость ко всем сменам камеры.

### W1-07-E02 — UDA / source-free целевое видео

**Гипотеза / решение:** дополнительное неразмеченное target видео может дать полезное обучение только если исходный detector покрывает нужные классы и pseudo-label noise контролируем. Цель — решить, стоит ли тратить ресурсы на этот путь вместо ручной разметки.

**Входы:** frozen source model с revision/classes; adaptation pool из отдельных target sessions; доступ к source для UDA либо явно source-free setting; небольшой ручной аудит pseudo boxes внутри adaptation pool и independent labeled selection validation. Если даже independent labels нет, эксперимент ограничен feasibility и аудитом, улучшение качества не подтверждается. Потребны trainer/plugin code review и измерение фактической памяти/скорости; RTX4070 конфигурация неизвестна.

**Контроль / действия:** сравнить frozen baseline с audited offline self-training. UDA AT-подобный вариант добавить лишь после прохождения implementation gate: два loader streams, augmentation bbox correctness, source loss, teacher EMA и checkpoint extraction. Source-free не имитировать занулением source loss AT; выбрать отдельную проверенную реализацию или отказаться от сложной ветки. В первом пилоте не использовать online test-time updates. На случайном и failure-oriented audit проверить precision, missed GT objects, class frequencies, object sizes и пустые кадры, включая negatives. Не маркировать все области вне pseudo boxes достоверным фоном без разбора loss. Не использовать validation/test для mining.

**Метрики / артефакты:** те же независимые detection/event gates, что E01; отдельно pseudo-label precision/recall на аудите, доля кадров без labels, class coverage, class/size distribution shift, FP/FN examples, teacher/student selection, integration time. Сохранить parent checkpoint, raw predictions, threshold policy, teacher version, provenance каждого pseudo-label и человеческую правку. Entropy/confidence записываются как diagnostics, а не accuracy.

**Исходы / stop rule:** если pseudo-label audit показывает систематические пропуски критичного класса, не повышать только confidence threshold; направить эти случаи на доразметку/другой teacher. Если независимо выбранный adapted model хуже frozen по критичной метрике либо удачный aggregate скрывает недопустимое падение камеры/класса — откатить. Остановиться после заранее ограниченного числа циклов self-training без независимого выигрыша или при превышении integration budget. Положительный результат доказывает пользу только для данной модели, размеченных условий и протокола exposure, а не автоматическое распознавание неизвестных классов или совместимость LinQ.

### W1-07-E03 — Что именно переносится на новую камеру

**Вопрос / решение:** нужен ли новый detector checkpoint на каждой камере, либо большая часть ошибки относится к scene rules/preprocessing.

**Входы и контроль:** минимум две камеры либо одна камера в нескольких независимых sessions; общий class semantics, frozen baseline и лучший E01/E02 кандидат. Если cameras достаточно, leave-one-camera-out: исключать всю камеру из adaptation/selection; если cameras мало — явно ограничить вывод new-session. Настройки геометрии опасных зон, thresholds и event temporal logic хранить отдельными версиями.

**Действия:** сначала запустить одинаковый detector/preprocessing на всех holdouts; затем отдельно оценить camera-specific rules с неизменным detector; затем проверить detector adaptation при фиксированных правилах. Так изменение зоны не приписывается training. Слепая независимая оценка проводится после заморозки настроек.

**Метрики / артефакты:** detector per-class AP/recall, event FP/hour/recall при event GT, камера/сессия, масштаб и visibility; версии rules и weights, group-level prediction deltas, примеры ошибок. **Stop rule:** если ошибка вызвана невидимым объектом/неразличимым классом либо geometry mapping, не продолжать detector training без нового сигнала. Если adaptation улучшает одну камеру, ухудшая held-out, выбрать camera-specific deployment либо frozen shared candidate, обозначив дополнительную стоимость модели. Успех на одной withheld camera не доказывает любой новый завод, сезон или физический перенос камеры.

## Открытые вопросы и передачи

| ID | Неизвестное и решение | Что уже известно / как закрыть |
|---|---|---|
| W1-07-Q01 | Можно ли пользоваться unlabeled target/test video для adaptation? | S09 показывает, насколько это меняет смысл цифры. Получить прямое правило кейса; manifest должен различать exposed/unseen images. При запрете исключить любое test-image statistics/training |
| W1-07-Q02 | Есть ли target labels, сколько независимых cameras/sessions и какие source images доступны? | Ничего из этого не установлено. Инвентаризация после выдачи кейса выбирает строку карты решений; не считать checkpoint доступом к source |
| W1-07-Q03 | Совпадают ли label semantics и exhaustive coverage? | До mixing сравнить guidelines и audit реальных кадров. datasets/model_stack должны подтвердить partial-label masking либо отказ от небезопасного merge |
| W1-07-Q04 | Какой trainer реально поддерживает выбранный detector и source-free режим? | AT code — конкретный Detectron2/Faster R-CNN, S05–S08. model_stack: предъявить pinned implementation, dry-run loss/loader test, извлечение одного teacher, exporter compatibility. Поддержка YOLO не установлена |
| W1-07-Q05 | Какой old-domain retention обязателен и есть ли независимые данные? | Без old-domain holdout forgetting не измеряется; source-free не решает это автоматически. evaluation/постановщик: согласовать gate по критичным классам/камерам |
| W1-07-Q06 | Применима ли CC-BY-NC4.0 авторского AT к намеренному использованию? | S04 README. Решить для конкретного способа заимствования/поставки; исследование статьи и копирование кода имеют разные последствия |
| W1-07-Q07 | Допускает ли LinQ граф выбранного detector и teacher extraction/export? | Здесь не установлено. linq_platform/model_stack: реальный compile+inference check, parity и timing после заморозки weights/preprocessing |

**→ evaluation:** F06/F10 — отдельно transductive, independent new-session и independent new-camera; source retention; selection labels делают model selection target-supervised. Нужен gate по критичным классам, а не только mean AP.

**→ datasets:** Q02/Q03 — нужны camera/session/source provenance, annotation coverage и class-map до mixing. Неразмеченные кадры не становятся negative GT.

**→ model_stack:** F03–F05 — historical dependencies, реальный loader/trainer, config/paper discrepancy, eval teacher extraction; не переносить рецепт на YOLO по сходству названия.

**→ linq_platform / video_architecture:** F05/Q07 — AT оценка использует один teacher detector, но graph/export не проверены. Новая camera-specific модель требует версии preprocessing/rules и маршрутизации weights; online adaptation не входит в предложенный первый pilot.

**→ violation_methods:** E03 — отсутствие сигнала, неправильная привязка СИЗ к человеку или зона камеры могут требовать иного вмешательства, чем fine-tuning.

Главное ограничение этой ветки: primary literature устанавливает существование и условия методов; выбранная практическая стратегия остаётся гипотезой до получения наших данных, модели, допустимого протокола доступа к target и независимой проверки.
