# W1-04 — редкие классы, sampling и hard negatives

Статус: самостоятельная первая волна завершена; только исследование, чтение кода и первичных публикаций. Обучение, запуск sampler/loss и измерения на наших данных не выполнялись. Время исследования: 2026-10-23, начало проверки источников около 03:40 UTC / 06:40 Europe/Moscow; дата доступа ко всем источникам ниже — 2026-10-23. Контекст mosprom-research-v1. Полного кейса, target data, обязательной таксономии и SDK LinQ нет.

## Решение, которое меняет эта ветка

Сначала нужно установить единицу редкости: изображения, экземпляры, независимые события, камеры/условия либо положительные и отрицательные элементы loss. Только затем выбирать вмешательство. Для небольшого CCTV-набора первый кандидат — контролируемое изменение состава данных или умеренный sampling при сохранении репрезентативной проверки; универсально заменять loss на focal оснований нет. Ошибки на конкретных похожих предметах дают основание для проверенных hard negatives. Повторы одного нарушения не компенсируют отсутствие других людей, камер, освещения или способов ношения СИЗ. Это наши выводы W1-04-F12–F15, а не опубликованные измерения на промышленном видео.

Существенная актуальная находка: в прочитанном Ultralytics **8.4.184**, commit **e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8**, есть `cls_pw` для class weighting; утверждение, что такого механизма нет вообще, неверно для этой версии. Его применимость к выбранному командой checkpoint и установленной версии ещё нужно проверить. Сам класс `FocalLoss` присутствует в файле, но прочитанный `v8DetectionLoss` использует BCE. Distribution Focal Loss для координат не следует путать с focal classification loss.

## Причина → возможное вмешательство → обязательный контроль

Следующая таблица — **наша условная стратегия**, опирающаяся на F01–F11; это не результат эксперимента.

| Наблюдение | Что сначала проверить | Разумное вмешательство | Чем можно опровергнуть пользу |
|---|---|---|---|
| Редкий класс есть только в немногих кадрах | Есть ли независимые сцены и корректные полные labels; объект различим при рабочем разрешении? | Добыть разнообразные реальные примеры; затем ограниченный image/group sampling | Выигрыш только на знакомой сцене; ухудшение held-out камер; FP растут |
| Мало изображений, много объектов на каждом | Раздельные image count и instance count | Сравнить image-frequency sampling с instance-frequency weighting | Перевзвешивание усиливает шум плотных сцен; редкий класс вне них не улучшается |
| Одно длинное нарушение даёт тысячи кадров | Связать кадры с episode/track/session; найти near-duplicates | Ограничить вклад группы; отбирать различные фазы/ракурсы | Число уникальных событий неизменно, validation по соседним кадрам завышен |
| Поток почти всегда нормальный | Реальная prevalence, длительность normal footage и типы ложных тревог | Обучение можно обогатить позитивами; operating point выбирать на реальном normal/positive материале | Хороший AP на искусственно сбалансированных кадрах не выдерживает FP/hour |
| Повторяющиеся FP на похожем фоне/предмете | Это настоящий negative или пропущенный/неразличимый positive? | Размеченные трудные негативы с dedup и сохранением позитивов | Снижение FP на mining-пуле не переносится на другой negative-пул; падает recall |
| Loss доминируют лёгкие background locations | Какая assignment/loss реально используется | Focal/OHEM только в поддержанной архитектуре как отдельная абляция | Нет выигрыша в paired comparison либо высокие веса уходят в ошибки labels |
| Редкие категории подавлены межклассовым обучением | Градиенты/ошибки по классам, а не одна гистограмма | Class weighting; при обосновании специализированный long-tail loss | Общее качество/частые классы или false alarms выходят за согласованный предел |
| Класс имеет ноль положительных annotations | Семантика и доступность визуального сигнала | Собрать/разметить positive, изменить scope по правилам кейса | Sampling/reweighting не создаёт отсутствующий положительный пример |

## Первичные источники и извлечённые факты

Метки: **paper measurement** — измерение авторов; **code reading** — прочитано, не запущено; **documentation** — официальная документация; **our inference** — наш вывод; **proposed experiment** — будущая процедура. Все URL прямые; live docs не считаются версией установленной библиотеки.

### W1-04-S01 — LVIS, расширенная версия с repeat-factor ablations

Agrim Gupta, Piotr Dollár, Ross Girshick. *LVIS: A Dataset for Large Vocabulary Instance Segmentation*. CVPR 2019; arXiv v1 2019-08-08, **v2 2019-09-15**, расширение про release v0.5.

- [Версия и история](https://arxiv.org/abs/1908.03195v2), [открытый полный текст](https://arxiv.org/html/1908.03195v2).
- Локаторы: Appendix B.1–B.2, Table 3a–b, footnote 5. Использовано для F01–F03.
- CVF PDF `https://openaccess.thecvf.com/content_CVPR_2019/papers/Gupta_LVIS_A_Dataset_for_Large_Vocabulary_Instance_Segmentation_CVPR_2019_paper.pdf` через web.open вернул 403; независимо открыт arXiv HTML v2. Это также нужная расширенная версия, а не только исходная конференционная статья.

**W1-04-F01 — paper measurement.** LVIS v0.5, Mask R-CNN ResNet-50-FPN с ImageNet pretraining; train v0.5 (~57k изображений), validation v0.5; mask AP, не box AP. Table 3b, среднее±SD пяти запусков: без resampling AP **21.0±0.17**, AP_r **3.2±0.35**, AP_f **27.7±0.12**; RFS `t=0.001`: **23.2±0.21 / 13.4±0.80 / 27.1±0.07**. CAS: **18.7±0.46 / 8.5±1.56 / 22.3±0.19**. Больший `t=0.01`: AP **21.8±0.25**, AP_r **9.8±1.27**. Значит, усиление балансировки не давало монотонного выигрыша.

**W1-04-F02 — paper protocol.** B.1–B.2: SGD, batch16, 90k updates (60k/20k/10k при LR .02/.002/.0002), momentum .9, weight decay .0001, warmup1000, короткая сторона800, horizontal flip, без TTA; Table 3b сохраняет score threshold0 и max300 detections/image. GPU и правило выбора checkpoint здесь не установлены. Отдельный label budget отсутствует: полный train release.

**W1-04-F03 — paper observation / our caution.** Table 3a отдельно меняет inference threshold и лимит detections; эти изменения нельзя записывать как эффект sampling. В тексте B.2 есть перевёрнутое неравенство относительно порога; формула и код S02 задают oversampling при `f_c<t`. Не копировать ошибочную прозу как рецепт.

### W1-04-S02 — Detectron2 RepeatFactorTrainingSampler

Meta/Facebook Research. Commit **b0fe2f0a5bb6496f65246ef35687a386a9f19202**, committer date **2026-10-20T11:03:57Z** (получено GitHub API `/repos/facebookresearch/detectron2/commits/main`).

- [Pinned distributed_sampler.py](https://github.com/facebookresearch/detectron2/blob/b0fe2f0a5bb6496f65246ef35687a386a9f19202/detectron2/data/samplers/distributed_sampler.py#L116), [raw](https://raw.githubusercontent.com/facebookresearch/detectron2/b0fe2f0a5bb6496f65246ef35687a386a9f19202/detectron2/data/samplers/distributed_sampler.py).
- Локаторы: `RepeatFactorTrainingSampler`, `repeat_factors_from_category_frequency` L143–191, `_get_epoch_indices` L192–212, `_infinite_indices` L216+.

**W1-04-F04 — code reading.** Частота `f_c` — доля изображений, содержащих хотя бы одну annotation класса; несколько экземпляров в кадре считаются один раз. По умолчанию `sqrt=True`: `r_c=max(1,sqrt(t/f_c))`; image factor — максимум классов кадра, для пустого изображения1. Stochastic rounding реализует дробные повторы в ожидании; размер очередного «epoch» меняется. Distributed slicing делит общий поток между rank. Параметр меняет обучение, не inference graph.

**W1-04-F05 — code reading / our calculation.** Докстрока «frequency half threshold → repeated twice» неверна при default sqrt: формула даёт `sqrt(2)`, а2 получается при `f=t/4`. Реальный код важнее этой фразы. `t` нужно выбирать после просмотра фактической частоты; LVIS `.001` для малого набора может вообще ничего не повторить. Отсутствующий класс не появляется в `category_freq`.

### W1-04-S03 — Detectron2 loader и defaults

Тот же pinned commit и дата, что S02.

- [build.py](https://github.com/facebookresearch/detectron2/blob/b0fe2f0a5bb6496f65246ef35687a386a9f19202/detectron2/data/build.py), локаторы `get_detection_dataset_dicts` L198–265; `_train_loader_from_config` L431–478; `_build_weighted_sampler` L372–429.
- [defaults.py](https://github.com/facebookresearch/detectron2/blob/b0fe2f0a5bb6496f65246ef35687a386a9f19202/detectron2/config/defaults.py#L123), L123–128.

**W1-04-F06 — code reading.** `DATALOADER.SAMPLER_TRAIN="RepeatFactorTrainingSampler"` выбирает RFS через loader; defaults `REPEAT_THRESHOLD=0.0`, `REPEAT_SQRT=True`. `FILTER_EMPTY_ANNOTATIONS=True` по умолчанию, и loader применяет фильтр изображений без не-crowd instances. Для mining настоящих пустых кадров необходимо проверить, что они не исчезли до sampler. Доступны также dataset weights и `WeightedCategoryTrainingSampler`: последняя перемножает dataset- и category-repeat factors. Название не означает CAS из LVIS. IterableDataset имеет другую ветку и не получает этот sampler автоматически.

### W1-04-S04 — Focal Loss paper

Tsung-Yi Lin et al. *Focal Loss for Dense Object Detection*, ICCV2017; arXiv v1 **2017-08-07**, v2 **2018-02-07**.

- [Версия](https://arxiv.org/abs/1708.02002v2), [полный текст](https://arxiv.org/html/1708.02002v2), §3.2–3.3, §4.1, Table1a–b, §5.1.
- CVF PDF через web.open: 403; arXiv HTML открыт независимо. Не переносим численные результаты из отличающихся версий автоматически.

**W1-04-F07 — method / paper measurement.** Focal loss умножает CE на `(1-p_t)^gamma`, подавляя лёгкие примеры; исходная мотивация — foreground/background dense detection. RetinaNet R50-FPN, ImageNet initialization, COCO trainval35k (~115k train images), minival5k, scale600: Table1, balanced CE31.1 AP, focal34.0 AP, выигрыш2.9 AP; `gamma=2`, `alpha=.25` (alpha подбирали для каждого gamma). 90k SGD updates, batch16 на8 GPU, LR.01 со снижением60k/80k, momentum.9, WD.0001, horizontal flips; prior foreground probability.01 при initialization. Это box COCO AP; полного отдельного малого label budget нет. Конкретный checkpoint-selection rule не установлен. Результат не доказывает исправление class-to-class long tail в любой YOLO.

### W1-04-S05 — Ultralytics class weighting: trainer

Ultralytics **8.4.184** (`ultralytics/__init__.py` L3), commit **e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8**, committer date **2026-10-22T20:27:18Z**, получено GitHub API `/repos/ultralytics/ultralytics/commits/main`.

- [DetectionTrainer](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/models/yolo/detect/train.py#L151): `get_class_counts`, `compute_class_weights`, `set_class_weights`, L151–181.
- [BaseTrainer](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/engine/trainer.py#L455): вызов `set_class_weights` после loader и до EMA.
- [Pinned default.yaml](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/cfg/default.yaml#L105): `cls_pw: 0.0`.
- Официальные live docs открыты: [train](https://docs.ultralytics.com/modes/train), раздел Training on Imbalanced Dataset; [API trainer](https://docs.ultralytics.com/reference/models/yolo/detect/train). Версию docs из URL определить нельзя; версионное основание — pinned source.

**W1-04-F08 — code reading.** `get_class_counts` считает **экземпляры** из train labels, не изображения или события. Для присутствующего класса вес `(1/count)^cls_pw`, нормируется к среднему1; `cls_pw` ограничен `[0,1]`,0 отключает вычисление. Отсутствующий класс получает средний предварительный вес, после normalization1, а не бесконечность. При отсутствии всех counts функция возвращается. Веса устанавливаются на модель, при distillation — на `student_model`. Это доступный training mechanism, не доказательство улучшения и не подтверждение наличия в старом локальном релизе.

### W1-04-S06 — Ultralytics фактический classification loss

Те же версия/commit/дата, что S05.

- [loss.py](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/utils/loss.py): `FocalLoss` L61+, `v8DetectionLoss.__init__` L354–390, classification calculation L463–467.
- [Live API](https://docs.ultralytics.com/reference/utils/loss), открыта; сам источник docs указывает на main, поэтому основание фиксируем по commit.

**W1-04-F09 — code reading.** `v8DetectionLoss` создаёт `BCEWithLogitsLoss(reduction="none")`. `class_weights` имеет broadcast shape `(1,1,nc)` и умножает BCE до суммирования и деления на `target_scores_sum`. Поэтому вес класса усиливает **всю его BCE-компоненту, включая отрицательные target entries**, а не только rare positives. `FocalLoss(gamma=1.5,alpha=.25)` существует отдельно; из этого не следует включённый focal loss в прочитанном detection criterion. `dfl` относится к bbox loss. Подменять BCE focal-модулем без проверки reduction/soft targets/normalization — отдельное изменение кода.

### W1-04-S07 — Ultralytics missing/empty labels

Те же версия/commit/дата, что S05.

- [data/utils.py](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/data/utils.py#L439), `verify_image_label` L439–516, особенно500–505.

**W1-04-F10 — code reading.** И пустой label file, и отсутствующий label file превращаются в пустой массив labels; счётчики `ne`/`nm` различаются. Это не проверка реального отсутствия объектов. **Our inference:** случайно потерянная annotation и проверенный background проходят этот участок с одинаковой пустой разметкой. Для hard-negative pool требуется явный provenance/статус проверки, а не только наличие пустого txt.

### W1-04-S08 — Online Hard Example Mining

Abhinav Shrivastava, Abhinav Gupta, Ross Girshick. CVPR2016; arXiv v1 **2016-04-12**.

- [Версия](https://arxiv.org/abs/1604.03540v1), [открытый PDF](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Shrivastava_Training_Region-Based_Object_CVPR_2016_paper.pdf).
- Локаторы §4.1–4.2, §5.1, Table3 (VOC2007), pp.3–6 PDF. Полный PDF успешно открыт.

**W1-04-F11 — method / paper measurement.** OHEM выбирает наиболее loss-heavy **RoIs**, включая foreground и background, внутри Fast R-CNN; это не offline сбор только negative кадров. Для устранения коррелированных областей авторы делают loss-based NMS с IoU.7. VGG16, VOC2007 trainval→test, single scale, bbox regression: reproduced baseline67.2→69.9 mAP (Table3). SGD80k, LR.001, decay×.1 каждые30k, N2 images/B128 RoIs; отдельного малого label budget нет. В §5.1 preprocessing отослан к Fast R-CNN defaults; полностью здесь не восстановлен. Точное GPU и checkpoint-selection rule не установлены. Применимость к современному YOLO и стоимость интеграции не подтверждены.

### W1-04-S09 — EQLv2 как граница «просто увеличить вес класса»

Jingru Tan et al. *Equalization Loss v2: A New Gradient Balance Approach for Long-tailed Object Detection*, CVPR2021. arXiv v1 **2020-12-15**, v2 **2021-04-01**.

- [Версия](https://arxiv.org/abs/2012.08548v2), [полный текст](https://arxiv.org/html/2012.08548v2), §3.1–3.2.
- CVF HTML вернул403; arXiv HTML открыт. Связанный авторский код: `https://github.com/tztztztztz/eqlv2` — **не проверен и не запущен**, не выдаётся за готовую интеграцию.

**W1-04-F12 — paper method, без переноса чисел.** EQLv2 рассматривает положительные и отрицательные градиенты каждого классификатора отдельно; накопленное отношение задаёт разные веса positives/negatives. Авторы подчёркивают, что одно количество примеров не определяет баланс градиентов: много лёгких негативов могут влиять меньше нескольких трудных позитивов. Это содержательно отличается от единственного множителя всей class BCE в F09. Метод — кандидат при диагностированном gradient imbalance; здесь не восстановлен его полный репликационный путь, поэтому численные выигрыши abstract не используются как основание назначения нам.

## Выводы для CCTV и пределы переноса

**W1-04-F13 — our inference: четыре счётчика до любой балансировки.** Нужна таблица `class × {source,camera,session,episode}` с image count, instance count, independent positive group count и длительностью нормального материала. Десять объектов одного класса в одном кадре изменят S05 weights, но почти не изменят S02 RFS; соседние кадры одного эпизода могут изменить оба, не добавляя разнообразия. Показать гистограммы исходного набора и фактического sampled stream. Выбор group-aware sampler вместо RFS — наша гипотеза, не встроенная подтверждённая возможность прочитанного trainer.

**W1-04-F14 — our inference: цена false alarms.** Обогащённая positive training distribution может быть полезна для обучения, но не задаёт рабочую prevalence. На потоке с редкими событиями даже небольшой FP rate может давать много тревог. Поэтому рядом с rare-class AP/recall нужны FP на отрицательный frame и, после неизменной логики объединения, false alarms per camera-hour, длительность просмотренного normal footage и event recall с числом независимых событий. Нельзя доказать приемлемость тревог тестом, искусственно поровну набранным из positives/negatives. Ноль FP на коротком видео не устанавливает нулевую частоту ложных тревог.

**W1-04-F15 — our inference: hard-negative loop без отравления supervision.** Mining-пул берётся из разрешённого train/adaptation материала. Для каждой находки фиксируется predicted class/score, frame/time, камера/эпизод и человек проверяет весь кадр по полной рабочей таксономии. Настоящие positives получают boxes; неоднозначное/невидимое состояние не объявляется negative. Нельзя оставить в полноразмерном кадре другие видимые рабочие классы без labels, чтобы «наказать только эту FP». Если loader не поддерживает ignore/partial labels, доразметить кадр либо исключить его. Сохранять отдельно look-alike negatives и обычный фон, распределять quota по причинам, ограничивать повторы одного эпизода; параллельно сохранять позитивный rehearsal-набор. Рост уверенного FP может требовать знания зоны/связи с человеком/времени, которое этот single-frame loss не даёт.

**W1-04-F16 — our inference: сравнение по бюджету.** При sampling «одинаковые epochs» могут означать разное число optimizer updates/показанных изображений. Сопоставить фиксированный update/image-exposure budget; отдельно записать wall-clock и повторную экспозицию каждому классу/группе. Если sampler меняет число итераций и schedule, различие качества нельзя приписать одной балансировке. Сначала пробовать одно вмешательство: sampling **или** weights **или** negatives. Их комбинация может быть полезна, но скрывает причину и может дважды усилить один noisy rare example.

**W1-04-F17 — our inference: inference/export.** RFS/offline mining меняют данные обучения; прочитанные weights/FocalLoss относятся к training criterion. Они сами не требуют новой архитектуры детектора. Но checkpoint, фактический exporter и граф после export всё равно нужно проверить, а inference на LinQ остаётся отдельным неизвестным. Успех обучения/ONNX не доказывает LinQ.

## Предлагаемые небольшие E-процедуры

Все процедуры **не выполнены**. Число кадров, прогоны и допустимые деградации назначаются после выдачи кейса по данным и бюджету; здесь не обещается время RTX4070.

### W1-04-E01 — установить, какой дисбаланс существует

- **Решение/гипотеза:** sampling полезен, только если исходная нехватка экспозиции отличается от нехватки независимых визуальных примеров.
- **Входы:** versioned train annotations, source/camera/session/time, возможность выделить episode/track; исходный checkpoint и fixed preprocessing от model_stack. Отдельно замороженные validation и lockbox, разделённые по подходящим независимым группам.
- **Действия:** посчитать четыре вида покрытия F13; вручную проверить редкие/нулевые классы, near-duplicates и label completeness. Без обучения построить ожидаемые и фактические class/group exposures из выбранного sampler с фиксированным seed. Проверить empty frames на выходе loader.
- **Контроль/метрики:** натуральная очередь против кандидата; image/instance/group frequencies, повторения на episode, доля background, доля камер и sources. Прогнозируемый RFS — формула S02, не выдуманный CLI-флаг.
- **Артефакты:** split manifest, class map, histogram, список groups, factors, sampled indices/seed, примеры labels и список исключений.
- **Исходы:** если RFS не меняет ничего — выбирать threshold по реальной частоте или отказаться; если усиливает один эпизод — доразметка независимых сцен/group cap; если rare positives неверны — исправлять labels раньше loss.
- **Stop rule:** нет надёжной семантики/group metadata или отсутствуют positives — остановить подбор balancing parameters до устранения причины.
- **Предел:** правильные exposures не подтверждают generalization и false alarms.

### W1-04-E02 — один контролируемый balancing trial

- **Решение/гипотеза:** умеренное усиление недостаточно представленных классов улучшает независимый rare recall при допустимой цене частым классам/FP.
- **Входы:** результаты E01, согласованные критичные классы и допуски; checkpoint/version/trainer от model_stack. Для Detectron2 — pinned RFS; для Ultralytics — сначала проверить локальное наличие S05–S06. Эти стеки — альтернативы, не сопоставимая архитектурная абляция.
- **Сравнение:** baseline natural sampler + default loss против **одного** кандидата: RFS с обоснованным threshold либо `cls_pw>0` в диапазоне поддержки. Начальные значения — гипотеза после histogram, не универсальный рецепт. В обеих ветках одинаковые train split, initialization, augmentation, input size, update budget, scheduler и checkpoint-selection criterion; зафиксировать seed и hash labels.
- **Действия:** короткий пилот на проверку labels/loaders/gradients, затем ограниченный paired training. Проверить сырые per-class predictions при одинаковых postprocessing settings; отдельно построить PR/recall при согласованной FP-нагрузке. Порог выбирать по validation одинаковой процедурой, не по lockbox.
- **Метрики:** per-class box AP50:95 (или фактическая метрика кейса), critical recall, frequent-class degradation, PR, FP/hour после fixed event logic; время, updates, exposures. Показать знаменатели независимых positives и negative camera-hours.
- **Артефакты:** оба config, versions, seeds, input/split hashes, sampler trace/weights, logs, validation predictions, checkpoint selection и checkpoint hash.
- **Исходы:** выигрыш при выполненных допусках — проверить ключевую пару на другом seed/независимой группе по доступному бюджету; выигрыш только train/familiar scene — возвращаться к данным; recall↑ и FP↑ — смотреть PR и operating point, не объявлять победу по одному recall.
- **Stop rule:** вред критичному классу/FP выше заранее назначенного допуска; ненадёжная разметка; отсутствие улучшения на полезной независимой группе. Не запускать широкую сетку t/gamma/alpha только из-за наличия GPU.
- **Предел:** даже повторение пары не устанавливает качество на неизвестной камере, после quantization или на LinQ.

### W1-04-E03 — hard negatives против такого же объёма обычной доразметки

- **Решение/гипотеза:** конкретные look-alike ошибки устраняются targeted negatives эффективнее, чем случайными новыми кадрами того же человеческого бюджета.
- **Входы:** замороженный baseline, отдельный разрешённый mining pool, список причин FP, аннотатор; independent negative validation и positive event set. Lockbox не участвует в mining.
- **Действия:** baseline inference на mining pool; группировка FP по эпизоду и причине; проверка F15; фиксированный quota по типам. Сравнить baseline, добавление проверенных hard-negative кадров и контрольное добавление разнообразных обычных кадров при сопоставимом annotation effort. Все рабочие классы на добавленном кадре должны быть полностью размечены либо корректно ignored поддержанным loader. Не добавлять выдуманный класс `background` в bbox taxonomy.
- **Контроль/метрики:** одинаковый checkpoint/update budget/positive exposure; FP по причинам и на час нормального видео, rare/critical recall, precision на выбранном validation threshold; human minutes и число независимых новых scenes. Mining-pool FP — диагностическая метрика, а не independent результат.
- **Артефакты:** mining model hash, prediction dump, candidate/review decisions, reason taxonomy, annotations, dedup/group manifest, configs/checkpoints и paired predictions.
- **Исходы:** перенос на новые negative episodes без потери recall — принять данные; эффект только на mining scenes — расширить причины/домены; потеря recall — проверить false-negative labels, quotas и экспозицию positives; недостаток визуального сигнала — передать violation_methods.
- **Stop rule:** mining поставляет преимущественно дубликаты/неоднозначные cases; трудозатраты не дают новых причин; ухудшение critical recall; ложные тревоги определяются другой event logic.
- **Предел:** не доказывает универсального эффекта OHEM и не устанавливает реальную prevalence всего deployment.

## Открытые вопросы и адресные передачи

| Q-ID | Что неизвестно и что уже установлено | Кому / как закрыть | Какое решение меняет |
|---|---|---|---|
| W1-04-Q01 | Фактические классы, critical error costs, нормальный поток и положительные независимые события отсутствуют; пороги редкости нельзя назначить | datasets / постановщик; inventory E01 | Нужен ли balancing, что считать negative, какой допустим FP/hour |
| W1-04-Q02 | Локальная модель/версия trainer неизвестны; class weighting подтверждён только pinned Ultralytics8.4.184, RFS — Detectron2 commit выше | model_stack: показать package/commit, criterion и loader output | Готовый параметр против изменения кода; не переносить новые flags в старое окружение |
| W1-04-Q03 | Annotation coverage смешанных источников и ignore semantics неизвестны | datasets + W1-03: audit coverage; model_stack: partial-label pathway | Допустимы ли hard negatives/oversampling вообще |
| W1-04-Q04 | Нет camera/session/episode IDs и гарантии независимого split | datasets + evaluation: построить группы/проверить near duplicates | Не спутать повторы кадров с ростом данных и переобучение с переносом |
| W1-04-Q05 | Приемлемый rare-recall/FP trade-off и event grouping не заданы | evaluation + violation_methods: fixed event protocol и denominator | Acceptance balancing/mining; AP не заменяет эксплуатационный критерий |
| W1-04-Q06 | EQLv2 не проверен на нашем head/soft targets, код не закреплён и не запущен; полного преимущества над простым sampling для нас нет | model_stack, только если E01/E02 подтверждают gradient problem; отдельная будущая интеграция | Стоит ли сложный loss своей цены; сейчас не приоритет по умолчанию |
| W1-04-Q07 | Экспорт выбранного обученного checkpoint и LinQ не проверены | model_stack + linq_platform; реальные export/compile/run artifacts | Готовность результата к обязательной платформе |

→ **datasets:** хранить negatives как подтверждённые отсутствия объектов, а не как missing files; приоритет — новые независимые позитивные эпизоды и разные причины FP. F10/F13/F15.

→ **evaluation:** сравнение sampling при одинаковом update budget, одинаковый threshold/NMS protocol, natural negative footage и per-class/event denominators; rare AP сильно зависит от покрытия. F01/F03/F14/F16.

→ **model_stack:** проверить существующий criterion, поддержку `cls_pw`, empty-image filtering и несовместимость OHEM-RoI с прямой подстановкой в YOLO. Веса S06 умножают и negative targets, что отличается от EQLv2. F06/F08–F12.

→ **violation_methods:** если FP — неверная связь СИЗ с человеком, неверная зона или одиночный неоднозначный кадр курения, оформить причину до назначения нового loss. F15.

→ **linq_platform / video_architecture:** sampling/mining сами не добавляют inference branches; проверка финального checkpoint/export остаётся обязательной. Никаких утверждений о поддержке LinQ на основании этой ветки. F17.

## Фактические ограничения выполнения

Выполнены web search и открытия первичных материалов, чтение pinned raw кода, получение commit dates/версии через API/исходник. PowerShell `Invoke-WebRequest` без `-UseBasicParsing` дал локальный NullReferenceException на raw GitHub; повтор с `-UseBasicParsing` успешно получил нужные файлы. Это сбой клиентского пути чтения, не недоступность кода. Другие файлы workspace не изменялись. Отдельные недоступные CVF пути описаны в S01/S04/S09; независимые arXiv варианты открыты. Методы и числа не проверены нами на target data, инженерные процедуры остаются предложениями.
