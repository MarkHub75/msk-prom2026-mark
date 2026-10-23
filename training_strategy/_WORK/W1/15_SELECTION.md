# W1-15 — Checkpoint, независимость сравнения и завершение адаптации

Дата исследования: 2026-10-23, начало сетевой проверки 04:09:22 UTC / 07:09:22 Europe/Moscow. Контекст: `mosprom-research-v1`. Это первая исследовательская волна training_strategy; training, benchmark, export и исполнение на LinQ не проводились. Целевые GT, полный кейс, SDK, фактическая конфигурация GPU отсутствуют. Поэтому ниже нет численных acceptance thresholds для нашего продукта и нет утверждения о достигнутом качестве.

Прочитаны Context-prompt.md, prompt-training-strategy.md, _WORK/PLAN.md, задание W1-15 и результат [W1-12](12_OPTIMIZATION.md). W1-12 уже разобрал optimizer/EMA/early stop/reload в Ultralytics 8.4.184, pin `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`. Здесь детали обучения не повторяются: предмет — как выбрать вмешательство и передать проверенный артефакт.

## Решение, которое меняет ветка

Передавать в интеграцию следует зафиксированную комбинацию weights + preprocessing + postprocessing + event rules, прошедшую независимый протокол. Имя `best.pt` и максимум mAP на многократно просмотренной validation не являются достаточным основанием. Нужно сохранить предыдущий пригодный bundle и различать статусы: перспективен на validation; подтверждён на закрытом материале; прошёл преобразование; реально выполнен на целевой платформе. Последние два статуса пока неизвестны.

В условиях малого бюджета полезнее одно причинно понятное парное сравнение с честным статусом неопределённости, чем несколько одновременно меняющихся recipe. Повторы назначаются по риску: stochastic optimization, выбор малой обучающей выборки и перенос между camera/session — разные вопросы. Ни один не закрывается универсальным «поставить seed=0».

## Источники и доступ

Все перечисленные первичные материалы открыты 2026-10-23. Дата публикации отделена от доступа; versions документации не являются версиями установленного окружения. Поиск выполнен по few-shot repeated samples, PyTorch reproducibility, model-selection bias, grouped validation, paired bootstrap; затем открыты paper/docs/author code. Репозитории не запускались.

| ID | Первичный материал, дата/версия и URL | Локатор и поддерживаемые факты |
|---|---|---|
| W1-15-S01 | Wang et al., *Frustratingly Simple Few-Shot Object Detection*, ICML/PMLR 119, 2020; arXiv v1 2020-03-16. [Страница](https://proceedings.mlr.press/v119/wang20j.html), [PDF v1](https://arxiv.org/pdf/2003.06957) | §4.2 Revised Benchmarks, Fig.3/4, Appendix A/B pp.10–12 PDF; F01. PDF прочитан, Fig.3 дополнительно запрошена screenshot страницы 6. PMLR PDF web-инструмент отказался получить: `Content length is too large: 15467493`; независимый arXiv PDF доступен. PMLR proceedings и arXiv v1 не объявляются побайтово одинаковыми |
| W1-15-S02 | Авторский FsDet, pin `148a039af7abce9eff59d5cdece296ad1d2b8aa0`; commit date 2021-10-27T16:53:42Z. [datasets/README.md](https://raw.githubusercontent.com/ucbdrive/few-shot-object-detection/148a039af7abce9eff59d5cdece296ad1d2b8aa0/datasets/README.md), [run_experiments.py](https://raw.githubusercontent.com/ucbdrive/few-shot-object-detection/148a039af7abce9eff59d5cdece296ad1d2b8aa0/tools/run_experiments.py), [metadata](https://api.github.com/repos/ucbdrive/few-shot-object-detection/commits/148a039af7abce9eff59d5cdece296ad1d2b8aa0) | Few-shot datasets/Pascal VOC/COCO; `get_config`, строки 215–224; F02. SHA/date получены независимым HTTP GitHub API; pinned raw открыт через web. Это позднейшее дерево авторского кода, не доказанная точная версия paper run |
| W1-15-S03 | PyTorch Contributors, [Reproducibility, 2.9](https://docs.pytorch.org/docs/2.9/notes/randomness.html); страница Created 2018-09-11, Last Updated 2024-11-26 | Intro, Controlling sources of randomness, Avoiding nondeterministic algorithms, DataLoader; F03. Взята versioned документация, не неоднозначный stable |
| W1-15-S04 | Cawley & Talbot, *On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation*, JMLR 11:2079–2107, published July 2010. [PDF](https://jmlr.csail.mit.edu/papers/volume11/cawley10a/cawley10a.pdf) | §1 pp.2079–2081, §4/5; F04. Методологическая работа, основная экспериментальная постановка kernel ridge classification; не detector benchmark |
| W1-15-S05 | scikit-learn developers, [Cross-validation, 1.7.2](https://scikit-learn.org/1.7/modules/cross_validation.html); дата публикации страницы не установлена | §3.1, §3.1.2.4 grouped data, §3.1.2.6 time series; F05 |
| W1-15-S06 | SciPy developers, [scipy.stats.bootstrap, 1.15.1](https://docs.scipy.org/doc/scipy-1.15.1/reference/generated/scipy.stats.bootstrap.html); дата страницы не установлена | `paired`, `rng`, `method`, Notes / DegenerateDataWarning; F06. Не готовая реализация cluster-bootstrap для detection |
| W1-15-S07 | COCO API authors Piotr Dollár, Tsung-Yi Lin; code header 2015, toolbox 2.0. Pin `8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9`, commit 2020-02-20T17:25:28Z. [cocoeval.py](https://raw.githubusercontent.com/cocodataset/cocoapi/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py), [metadata](https://api.github.com/repos/cocodataset/cocoapi/commits/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9) | `COCOeval` header, `accumulate`, `summarize/_summarize`, `Params.setDetParams`; F07. SHA/date получены HTTP GitHub API, pin открыт web |
| W1-15-S08 | Ultralytics 8.4.184, pin `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`, commit date 2026-10-22T20:27:18Z по W1-12-S13. [metrics.py](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/utils/metrics.py), [trainer.py](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/engine/trainer.py) | `Metric.maps`, `Metric.fitness`, `BaseTrainer.save_model`, `validate`; F08. Нужные функции самостоятельно открыты; версия/date и подробное optimizer поведение унаследованы как локальная передача W1-12, не новый независимый эксперимент |
| W1-15-S09 | scikit-learn developers, [Tuning the decision threshold, 1.7.2](https://scikit-learn.org/1.7/modules/classification_threshold.html); дата страницы не установлена | §3.3, §3.3.1, §3.3.1.2; F09. Пример classification; разграничение score/decision полезно, API не переносится автоматически на detector/events |

## Проверенные факты и их пределы

### W1-15-F01 — TFA проверяет variance по training shots

**Основание: опубликованный протокол S01, не наш тест.** Для Faster R-CNN few-shot detection авторы меняют группы размеченных training shots, сообщают base AP, novel AP и overall AP. Revised benchmark усредняет 30 групп для PASCAL VOC и 10 для COCO; Appendix A задаёт half-width `1.96*s/sqrt(n)` для среднего. Fig.3 показывает нестабильность первых runs на VOC, Fig.4 — generalized evaluation по base и novel. Единица shot — размеченный экземпляр объекта, не независимая камера. Эти числа характеризуют протокол статьи; это не предписание запускать 30 наших trials. Здесь не заимствуются численные выигрыши TFA и не задаются compute, скорость или ожидаемый AP нашего CCTV. Протокол не устанавливает отдельно variance только от optimizer RNG.

### W1-15-F02 — Название seed в FsDet не означает только seed обучения

**Основание: code/documentation S02.** `datasets/README.md` описывает 29 дополнительных VOC training-shot групп к исходной, COCO — 10 групп с exactly K instances/category. В `get_config(seed, shot)` seed включается в имя `DATASETS.TRAIN`; для output/config создаются отдельные пути. Значит, механически перенести сравнение «много seeds» как повтор одного неизменного train set было бы неверно. Само чтение этой функции не устанавливает все RNG всего trainer.

**Наш вывод из F01/F02:** в manifest отдельно хранить `training_sample_seed`, `training_manifest_hash`, `optimization_seed`, `split_manifest_hash`, `evaluation_resampling_seed`. Смена sample при том же optimization seed отвечает на иной вопрос. При нескольких clips одного эпизода K boxes нельзя интерпретировать как K независимых наблюдений.

### W1-15-F03 — Reproducibility ограничена окружением

**Основание: документация S03.** Идентичный seed не гарантирует совпадение между releases/commits/platforms либо CPU и GPU. PyTorch, Python, NumPy и отдельные NumPy Generator имеют свои источники случайности; DataLoader требует осознанного worker/generator seeding. Отключение cuDNN benchmark не равно включению deterministic algorithms; детерминированный режим может замедлять и выдавать ошибку для неподдержанной операции.

**Наш вывод:** сохранять среду и фактические настройки; утверждение «воспроизводится» ограничивать зафиксированной средой и измеренным допуском. Детерминизм нужен для диагностики пары, а повтор optimization seeds — для оценки чувствительности; это разные цели.

### W1-15-F04 — Validation становится частью выбора модели

**Основание: методологическая работа S04.** Оптимизация noisy finite-sample model-selection criterion может переобучиться сама; выбор и оценка на одном материале дают selection bias. Авторская рекомендация рассматривать model-selection procedure как часть обучения мотивирует независимую внешнюю оценку. Эксперименты статьи не дают количественной оценки bias нашего detection pipeline.

**Наш вывод:** checkpoint/epoch, architecture, data mixture, confidence, NMS и temporal rule — всё, что меняют по результатам набора, входит в selection. Набор после многократного просмотра ошибок является рабочей validation. Назвать его test и зафиксировать seed недостаточно. Lockbox после открытия для диагностики больше не закрытая независимая проверка будущих исправлений.

### W1-15-F05 — Единица независимости должна соответствовать задаче переноса

**Основание: документация S05.** Group-wise validation не допускает одну группу в train и validation; обычное i.i.d. разбиение некорректно для зависимых групп. Близкие во времени наблюдения коррелированы; time-aware проверка отвечает на другой вопрос, чем случайный split.

**Наш протокол для CCTV:** camera/session/episode IDs строятся до извлечения frames/crops. Все потомки кадра и одного эпизода наследуют partition. Для новой камеры удерживается camera целиком; для будущего времени на известной камере удерживается более поздняя session с временным разрывом. Разные временные куски той же камеры не подтверждают unseen-camera перенос. Exact/perceptual duplicate audit дополняет IDs. Если камер мало, несколько «session groups» не превращают их в большое число независимых cameras. Target unlabeled adaptation тоже раскрывается: использованные потоки нельзя молча назвать полностью unseen.

### W1-15-F06 — Парность сохраняется и при оценке неопределённости

**Основание: API documentation S06.** `paired=True` использует одинаковые resampled indices для всех входных массивов; обычное независимое resampling разрушает соответствие пары. Документация предупреждает о degenerate bootstrap distributions, для которых BCa interval может быть NaN.

**Наш проект процедуры:** для одинаковых camera/session groups сравнивать `Delta=M(candidate)-M(baseline)`, resample независимые группы с возвращением и включать обе модели для каждого выбранного group. Для AP заново агрегировать GT/predictions всей resample с корректными уникальными image IDs, а не усреднять image-AP; для rates пересчитывать сумму counts/сумму exposure. Интервал bootstrap характеризует наблюдаемый домен/выбранную единицу; несколько камер и нулевые rare positives не дают надёжного population claim. Frame bootstrap здесь не заменяет group bootstrap. Этот cluster-specific алгоритм не обещается одной готовой командой SciPy.

### W1-15-F07 — Сводный AP не свидетельствует о классе без GT

**Основание: COCO code S07.** bbox evaluation имеет отдельные IoU thresholds `.5:.05:.95`, recall grid, area ranges и `maxDets`. Precision/recall для settings без GT обозначаются `-1`, summary усредняет только `s>-1`. Следовательно, среднее может выглядеть приемлемо при неподтверждённом обязательном классе. Нельзя заменять missing support нулём или приписывать отсутствующему классу доказанное качество. COCO matching — detection matching, не event protocol и не SLA.

**Наш вывод:** рядом с AP писать positive objects, independent positive episodes/groups, negatives и проверенную video exposure. При нуле positive episodes recall — N/A; при нуле evaluable exposure FP/hour — N/A. Для редких событий хранить TP/FN/FP и matching/censoring rules; 0 FP на просмотренном отрезке не доказывает нулевую будущую частоту. Пустые/неполные annotations требуют отдельного annotation contract.

### W1-15-F08 — Встроенный best и per-class convenience output требуют проверки

**Основание: code S08.** `Metric.fitness` использует веса `[0,0,0,1]` для `[P,R,mAP50,mAP50:95]`. `save_model` пишет best при `best_fitness==fitness`; последний tie может обновить файл. `Metric.maps` сначала заполняет все `nc` общим `self.map`, затем заменяет entries из `ap_class_index` измеренным AP. Поэтому `maps[class_id]` само по себе не доказывает, что класс имел оцениваемый GT. Использовать `ap_class_index` и support counts, а не только эту convenience array. Это конкретное поведение pin; перенос на другой version/task требует проверки.

W1-12-F05 дополнительно установил EMA validation и stripping итогового checkpoint: inference artifact не равен точной resume point. Здесь не вводится новый default trainer. Если выбранная event цель отличается от detector mAP, нужно заранее сохранить нужные epoch artifacts и проверять их на validation по одному правилу; нельзя после завершения обещать восстановить уже перезаписанный checkpoint.

### W1-15-F09 — Порог меняет решение без обучения

**Основание: classification documentation S09.** Для неизменных scores изменение decision threshold меняет labels; ROC/PR curves исходных scores остаются теми же в приведённом примере. Threshold tuning тоже может переобучиться; docs запрещают использовать training data для настройки такого порога.

**Наш перенос с ограничением:** в detection после confidence filtering/NMS/caps состав predictions и даже измеряемый AP могут изменяться, поэтому нельзя обещать инвариантность AP к любому postprocessing. Для событий меняются association, dwell time, cooldown и зона; улучшение итоговых тревог от этих правил полезно, но не является улучшением learned weights. Сравнивать 2 оси по E02.

## Контракт принятия без вымышленных чисел

Следующее — **предложенная политика команды**, а не установленное требование кейса. После получения GT/evaluation contract до trials заполнить параметры `primary_metric`, минимальный практически значимый выигрыш `delta_min`, допустимую регрессию базовых классов/камер `epsilon_c`, критичные recall floors `R_min,c`, FP budget и единицу exposure, uncertainty procedure, maximum candidates/repeats, integration reserve. Пока значения не утверждены из кейса и baseline, результат обозначается exploratory, без binary safety acceptance.

Полезна constrained selection: сначала исключить candidate, нарушающие критичные ограничения; среди оставшихся сравнить основную метрику и стоимость. Для подтверждённого выигрыша можно заранее потребовать lower confidence bound парной Delta выше `delta_min`; для каждого критичного degradation — выдержанный non-inferiority margin. Это строгий вариант, требующий достаточного материала и обоснованного interval. Положительная Delta с интервалом, пересекающим ноль/практический margin, означает «данных недостаточно», а не автоматическую ничью или доказательство бесполезности. При большом числе trials post-selection interval на той же validation не является независимым доказательством; подтверждение — закрытым материалом.

Если objective — fixed FP budget, thresholds каждой модели настраиваются на рабочей validation по одинаковому заранее заданному алгоритму/бюджету; на lockbox они уже фиксированы. Нельзя на lockbox подбирать порог каждой модели, чтобы сравнить «при одинаковом числе FP». Одновременно сохранить результат при общих settings: так видно, переносит ли candidate прежнюю конфигурацию.

Stop/rollback имеют несколько оснований. Немедленный stop дорогого пути: leakage/class-map/annotation corruption; отсутствующий пригодный artifact; неустранённые NaN/reload failures по W1-12. Остановка гипотезы: заранее исчерпан candidate/repeat budget без достаточного выигрыша либо регресс критичных сценариев; сохранить baseline и конкретное знание. Остановка улучшений: лучший допустимый bundle заморожен до integration reserve, новые изменения не успевают пройти тот же протокол. Rollback: деградация после export/quantization/target runtime ведёт к предыдущему прошедшему bundle или к точной локализации преобразования, а не к молчаливой подстройке порога на test.

## E-процедуры будущей практической волны

Все E ниже **не выполнены**. Доступы: локальная подтверждённая training/evaluation среда, разрешённые данные; LinQ появляется только в E04 при реальном доступе. Начальный baseline выбирает model_stack. Бюджеты должны быть вписаны до опыта, исходя из оставшегося времени и реально измеренной цены W1-14; здесь не предполагаются минуты RTX 4070 или объём VRAM.

### W1-15-E01 — Зафиксировать выбор и независимые partitions

**Гипотеза/решение:** данные позволяют сравнивать адаптацию в нужном режиме переноса. **Входы:** source/target inventory, GT schema/coverage, camera/session/episode/time IDs, checkpoint SHA256/commit; требования evaluation. **Контроль:** untouched lockbox исключён из training, active/pseudo/calibration/threshold pools; patient-like group principle F05 адаптируется к camera/session. **Действия:** определить operational population; сформировать train, рабочую val, lockbox по группам до frames/crops; проверить hashes/duplicates/time overlap и происхождение labels; зафиксировать selection objective, constraints и число candidates. Для одной камеры явно ограничить claim будущими sessions; если independent holdout невозможен — exploratory protocol.

**Метрики/артефакты:** partition manifests с hashes и ролями данных, overlap audit, per-class objects/episodes/groups/exposure, selection contract, журнал доступа к lockbox. **Исходы:** независимость и support достаточны → E02; leak → пересобрать до training; rare support отсутствует → доразметка/сбор отдельного материала и N/A в текущем отчёте. **Stop:** не начинать подтверждающий trial при leak/неопределённом matching; не обещать покрытие отсутствующего класса. **Предел:** audit не доказывает полноту labels и не гарантирует перенос за пределы представленных камер/условий.

### W1-15-E02 — Отделить обучение от порога/NMS/правила

**Гипотеза/решение:** candidate улучшает weights, а не только настройки решения. **Входы:** A baseline, B один обученный candidate с уже пройденными W1-12 gates; одинаковая val E01, зафиксированный evaluator. **Контроль:** в первом сравнении preprocessing, confidence/NMS/caps, event rule и matching одинаковы; всё различающееся в train recipe/данных записано как intervention. **Действия:** сохранить predictions/scores; сравнить A и B при общих settings. Отдельно на рабочей validation выбрать `theta_A` и `theta_B` одинаковой процедурой; измерить таблицу A/B × theta_A/theta_B, если семантика settings совместима. Если новое preprocessing/crop/graph необходимо, назвать опыт bundle comparison и добавить изолированную абляцию, иначе причинного вывода о training нет.

**Метрики:** detector AP с полными settings, per-class measured AP/support, operating recall/precision, event TP/FN/FP, FP/exposure, базовые/редкие классы и камеры. **Артефакты:** raw/retained predictions, evaluator/version, configs, PR data, error gallery и таблица четырёх combinations. Если export скрывает pre-NMS tensors, ограничение фиксируется. **Исходы:** B лучше при общих settings → E03; выигрывает только настроенное правило → принять как rule improvement и оценить отдельно; общий gain скрывает critical regression → не promote. **Stop:** заранее заданное число threshold/rule candidates; одинаковый trial budget для A/B, никакого lockbox tuning. **Предел:** одна val/один training run не доказывают устойчивость; object AP не подтверждает event recall.

### W1-15-E03 — Условные парные повторы и grouped uncertainty

**Гипотеза/решение:** преимущество сильного кандидата устойчиво к главному источнику неопределённости. **Входы:** A/B E02, fixed grouped val, runnable recipe, фактическая стоимость запуска. **Контроль:** одни training manifests/source weights/budget и selection criterion внутри пары; одинаковые group indices при анализе. **Действия:** сначала выделить вопрос. (a) Optimization sensitivity — повторить A/B на тех же данных с другим optimization seed; по возможности paired seeds, но одинаковый номер не гарантирует одинаковые RNG streams при разных графах. (b) Few-shot sample sensitivity — другая training-shot группа из train pool с тем же label budget; A/B используют одинаковую новую группу, optimization RNG записан отдельно. (c) Camera transfer — заранее заданный дополнительный development group split; внутри него selection повторяется без доступа к внешнему lockbox. Не называть эти три проверки одной величиной seed variance.

Для каждой пары сохранить Delta; сообщить все pair results, median/range и число repeats, включая неудачи. При достаточном числе независимых evaluation groups выполнить paired group bootstrap F06 с заранее заданными confidence/method/resamples/RNG, пересчитывая статистику. Для nested cameras/sessions выбрать resampling level по claim; нельзя считать sessions независимыми cameras. При нескольких seeds на одной val не умножать число независимых scenes на число seeds. При degenerate/too-small support report interval unavailable и raw counts, без выдуманной точности.

**Артефакты:** отдельные sample/optimization/split/resampling seeds, train hashes, все checkpoints и выбора epoch, paired metrics/deltas, group counts, resampling indices и валидность CI. **Исходы:** стабильный практически значимый выигрыш без критичных регрессий → заморозить bundle; смена знака → сохранить baseline и исследовать coverage/ошибки; неопределённость из-за малого числа scenes → добавить реальные независимые данные, а не бесконечные optimizer seeds. **Stop:** до запуска записать максимум repeats и reserve; после его исчерпания результат inconclusive либо provisional. Не добавлять runs только до первого значимого результата. **Предел:** редкий повторный seed не даёт надёжного population CI; bootstrap val не оценивает training-sample variance сам по себе и не исправляет selection bias.

### W1-15-E04 — Заморозка, lockbox и цепочка FP → export → quant → target

**Гипотеза/решение:** выбранный bundle сохраняет качество и пригодность после реального пути преобразования. **Входы:** frozen A/B и выбранные settings, untouched GT lockbox E01, отдельный calibration/train material, actual exporter/compiler/runtime versions. **Контроль:** одинаковые canonical input frames, class map, geometry/color/normalization, NMS/caps/rules и evaluator; никаких новых labels/threshold tuning по lockbox. **Действия:** сначала на рабочей parity validation сравнить source FP с reloaded FP, затем FP export, quantized artifact и целевой runtime последовательно, чтобы локализовать изменение. Сохранять raw outputs где доступны, decoded predictions, error/matching differences. Отдельно измерить качество каждого этапа; numerical closeness полезна для debugging, но не заменяет GT metrics. После выбора реального deployment bundle выполнить заранее запланированную финальную lockbox оценку против замороженного baseline; получить решение по контракту.

**Метрики/артефакты:** numerical deltas с dtype-specific допуском, bbox/class/count differences, paired detector/event metrics/support; exporter flags/opset, quant calibration IDs/hash, compiler options/logs, runtime/device identity, unsupported ops/fallbacks, bundle checksums. Latency/throughput/end-to-end exposure — по video_architecture на реальном устройстве отдельно от quality. **Исходы:** FP хорошо, export плохо → preprocessing/decoder/export gate; quant плохо → calibration/precision/W1-13; целевое исполнение отсутствует → статус target-unverified; все gates проходят → promotion/rollback bundle фиксируется. **Stop:** любой неподтверждённый class map/output contract, критичный quality regression или невыполненное обязательное target execution; не продолжать адаптацию на lockbox. Если по его ошибкам исправили систему, набор стал development: новая независимая проверка нужна для нового claim. **Предел:** ORT/RTX/source FP успех не доказывает LinQ; один lockbox не подтверждает industrial safety/SLA или другие камеры.

## Manifest пригодного результата и rollback

Это предлагаемый набор полей артефакта, не готовая команда или обязательный формат конкретного framework. Сохранять manifest рядом с неизменяемыми файлами; пути и SHA256 должны позволять восстановить **конкретный bundle**, а не искать «последний best».

| Раздел | Обязательные сведения |
|---|---|
| Identity/lineage | run ID, UTC timestamps, owner, hypothesis, parent baseline ID, git SHA/dirty patch, model/task/architecture, source weight hash, class IDs/names/order, license/provenance |
| Data | dataset/annotation revisions и hashes, coverage/ignore rules, train/val/lockbox/calibration/unlabeled roles, camera/session/episode/time mapping, selection history, label budget в objects/images/independent groups |
| Training | effective config, transforms/sampling, all RNG seeds/worker handling, trainable mask, optimizer/update/batch/accumulation/precision, actual budget/retries, environment lock/OS/driver/CUDA/GPU/VRAM; детали по W1-12 |
| Selection | primary/constraints/delta margins, candidate budget, выбранный epoch и criterion, EMA vs online, results всех candidates/seeds, evaluator commit/settings, support/exposure, uncertainty method, lockbox access log |
| Files | inference checkpoint hash, отдельно resume checkpoint и состояние optimizer/scaler/RNG/loader насколько реально сохранены; stripped artifact не объявлять точным resume, actual reload validation |
| Inference | shape/layout/dtype, color/resize/letterbox/normalization/inverse geometry, decoder, confidence/NMS/caps, track/association/zone/temporal rules, dependencies и rule config hashes |
| Export/target | source→export→quant→compiled hashes, opset/flags/calibration subset, compiler/runtime/SDK/device versions и logs, точное место исполнения и known fallbacks, parity/GT results с status |
| Decision/rollback | approved/provisional/rejected/target-unverified и основания, открытые ограничения, ссылка на прежний прошедший bundle, действие переключения model+preprocess+rules+runtime вместе, smoke inputs и критерий восстановления |

Rollback не равен замене одного файла weights при оставшихся новых class map/NMS/rules. Старый bundle не перезаписывать. Прежде чем считать восстановление рабочим, повторить фиксированные smoke inputs и убедиться в соответствии manifest; smoke не заменяет повтор quality на новом домене. После заморозки новые идеи складываются в backlog; внесённое изменение создаёт новую ревизию и возвращается к соответствующему gate.

## Открытые вопросы и адресные передачи

| ID / адресат | Что неизвестно и зачем | Как получить ответ |
|---|---|---|
| W1-15-Q01 → evaluation / постановщик | Реальная primary metric, event matching, critical recall/FP budget, practical delta и non-inferiority margins. Без них нельзя честно задать numerical acceptance | Полный кейс, GT/exposure/support baseline; согласовать E01 contract до tuning |
| W1-15-Q02 → datasets | Достаточно ли независимых cameras/sessions/rare events, исчерпывающие ли labels, нет ли пересечений open/source/target | Inventory/annotation contract/duplicate audit; E01. Few-shot boxes не равны разнообразию сцен |
| W1-15-Q03 → model_stack / W1-12 | Как сохранить epoch, оптимальный по нужной цели; где online/EMA/stripped/resume artifacts и RNG state | Проверить hooks/save cadence/reload выбранного version; F08 и W1-12-F05. Не полагаться на имя best.pt |
| W1-15-Q04 → evaluation | На каком уровне resampling отвечает operational claim; достаточен ли rare support для interval | Задать camera/session hierarchy и metric estimator; E03. Нельзя получить значимое n из кадров одного события |
| W1-15-Q05 → violation_methods / operator_product | Что именно изменялось: признаки объекта или связь/длительность/зона/cooldown; как трактовать repeated alarms | Полный event contract и E02 factorial table; gains rules сообщать отдельно от training |
| W1-15-Q06 → linq_platform / model_stack / W1-13 | Actual export/quant/compiler path, decoding/NMS location, outputs/precision/fallbacks и устройство | SDK/device access + E04. Здесь нет проверенного LinQ quality/speed и нет гарантии поддержанного графа |
| W1-15-Q07 → W1-14 / hackathon_strategy | Какой repeat и integration reserve реально помещаются по измеренным затратам | Короткое profiling/стоимость baseline; заранее cap E03. «Сделать 30 seeds» не вытекает из TFA для 45 часов |

Ветка завершена на уровне источников и проектирования протокола: причинные риски локализованы, реальные acceptance values/GT и target execution остаются внешними входами. Следующая работа — E01 после получения данных, затем E02 для одной конкретной гипотезы; эта запись не является результатом выполненной адаптации.
