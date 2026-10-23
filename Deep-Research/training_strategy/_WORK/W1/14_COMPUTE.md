# W1-14 — GPU, независимые trials, DDP и цена информации

Проверено 2026-10-23, 07:08–07:14 Europe/Moscow (UTC+3). Контроль времени clock: 04:08:36–04:13:43 UTC; это дата исследования и записи, не benchmark. Прочитаны Context-prompt.md, prompt-training-strategy.md, _WORK/PLAN.md, W1-14 в _WORK/AGENT_PROMPTS.md; для согласования pin просмотрен W1/12_OPTIMIZATION.md. Единственный результат ветки — этот файл. Поиск и открытие первичных docs/code выполнены; обучение, profiling, аренда, установка и измерение железа не выполнялись.

## Решение

При неизвестных данных и пределах модели сначала выгодно получить независимые ответы на разные содержательные вопросы: есть ли полезный исходный detector, покрывает ли разметка ошибки, помогает ли масштаб изображения, проходят ли веса путь целевого исполнения. Это наша условная рекомендация, а не экспериментально доказанный оптимальный scheduler. Несколько GPU позволяют ускорить получение таких ответов независимыми trials. DDP ускоряет один согласованный прогон; оно не проверяет несколько гипотез и не создаёт независимых повторений.

DDP имеет смысл после установления корректного baseline и рецепта, если именно продолжительность одного обязательного training находится на критическом пути, одна replica помещается на устройство, данные успевают загружаться, backend/сеть работают и измеренное ускорение окупает настройку. При малом датасете, коротких прогонах, слабой сети, CPU/дисковом bottleneck или ещё не закрытых вопросах разметки дополнительные независимые trials могут дать больше полезного знания. Число GPU само по себе не определяет выбор.

Известно только наличие RTX 4070, ноутбука и возможности облака. VRAM, ОС машины с GPU, RAM, CPU, диск, driver/CUDA/PyTorch, межсоединение и скорость неизвестны. PowerShell исследовательской среды не устанавливает ОС training-машины. Обязательный инференс на LinQ — отдельный gate; успех на CUDA не подтверждает его.

## Первичные источники и локаторы

Все источники открыты 2026-10-23; доступ успешен. Сетевой поиск использован для зацепок PyTorch DDP/profiler/loading, Ultralytics multi-GPU и CUDA timing. В итоговые факты вошли открытые страницы, не snippets. PyTorch `stable` фактически перенаправлялся на **2.14**; это версия документации, не установленного ПО. Дата публикации разделов без явной даты неизвестна. Ultralytics source pin **e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8**, версия **8.4.184**: согласован с W1-12; источники здесь открыты также непосредственно по commit. Дата commit 2026-10-22T20:27:18Z взята из W1-12-S13, самостоятельно metadata не запрашивалась.

| ID | Источник / URL | Точный локатор, версия и граница |
|---|---|---|
| W1-14-S01 | [PyTorch DistributedDataParallel](https://docs.pytorch.org/docs/2.14/generated/torch.nn.parallel.DistributedDataParallel.html) | Class introduction, Notes, `no_sync()`; 2.14; sharding, replica, reduction и синхронизация |
| W1-14-S02 | [PyTorch torch.profiler](https://docs.pytorch.org/docs/2.14/profiler.html) | Overview; `schedule`; `supported_activities`; `profile`; overhead note; last updated 2026-05-11 |
| W1-14-S03 | [PyTorch torch.utils.data](https://docs.pytorch.org/docs/2.14/data.html) | Multi-process data loading; platform-specific behaviors; Memory Pinning; DistributedSampler и set_epoch; 2.14 |
| W1-14-S04 | [PyTorch Reproducibility](https://docs.pytorch.org/docs/2.14/notes/randomness.html) | Opening warning; deterministic algorithms; DataLoader; updated 2026-05-14 |
| W1-14-S05 | [Ultralytics trainer.py, pin](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/engine/trainer.py) | BaseTrainer.train L217–239; _build_train_pipeline L276–310; _setup_train L409–419; _do_train L468–526, L563; code read, not executed |
| W1-14-S06 | [Ultralytics data/base.py, pin](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/data/base.py) | BaseDataset._ImageCache L69–98; init L157–169; load_image L233 onward; cache_images/cache_images_to_disk L302–327 |
| W1-14-S07 | [Ultralytics data/build.py, pin](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/data/build.py) | InfiniteDataLoader L42–80; build_dataloader L319–384; concrete sampler/workers/prefetch/pinning |
| W1-14-S08 | [Ultralytics Train](https://docs.ultralytics.com/modes/train) | Multi-GPU Training / Windows / Custom Code; Train Settings `profile`; live docs, publication/update date not established |
| W1-14-S09 | [PyTorch CUDA semantics](https://docs.pytorch.org/docs/2.14/notes/cuda.html) | Asynchronous execution L592–607; updated 2026-07-17 |
| W1-14-S10 | [PyTorch BatchNorm2d](https://docs.pytorch.org/docs/2.14/generated/torch.nn.modules.batchnorm.BatchNorm2d.html) | Class semantics: per-mini-batch statistics, running estimates; 2.14; page date unknown |

## Факты и ограничения

**W1-14-F01 — DDP не объединяет память в одну GPU.** Документация S01 описывает синхронизацию градиентов между replicas и рекомендует отдельный процесс на GPU; входы необходимо распределять sampler-ом. Из этого следует: обычное DDP не решает случай, когда одна модель/её состояния не помещаются на одном устройстве; это уже вопрос другого memory strategy. Дополнительные GPU делят работу над данными, а не автоматически слой/параметры. Тип: documentation → наш вывод.

**W1-14-F02 — accumulation и коммуникация различаются.** S01: `no_sync()` подавляет gradient synchronization в накопительных проходах; forward тоже должен быть внутри context. DDP усредняет градиенты, поэтому суммируемый и усредняемый loss требуют различать. Это интерфейс PyTorch, а не обещание его применения любым trainer. Тип: documentation.

**W1-14-F03 — конкретный trainer меняет смысл сравнения.** По S05: global batch делится на world size; AutoBatch `<1` отвергается в multi-GPU, `rect=True` принудительно становится False. Nominal accumulate = max(round(nbs/global_batch),1), затем есть ограничение длительностью; warmup меняет accumulate. Перед backward distributed loss умножается на world size. В прочитанном `_do_train` нет `no_sync`: backward выполняется каждый microbatch, optimizer — по accumulate. Нельзя обещать сокращение all-reduce до одного на update; проверять trace. Тип: code observation, без запуска.

**W1-14-F04 — effective batch — бухгалтерия экспозиций, не гарантия эквивалентности.** При полных равных microbatches приблизительно B_update = world_size × local_microbatch × accumulation. Для S05 global batch уже включает world size: второй раз умножать `args.batch` на число GPU нельзя. Хвосты, padding sampler, warmup и retries требуют журналировать фактические sample IDs/optimizer steps. S10: BatchNorm считает статистики по mini-batch в forward. Наш вывод: накопление нескольких forwards не превращает их BN-statistics в статистики одного большого batch. Даже при равном B_update могут измениться порядок примеров, stochastic augmentation, число обновлений, LR schedule и численные ошибки. Детали optimizer/AMP/EMA — W1-12, не повторяются как новый recipe.

**W1-14-F05 — sampler имеет цену корректности.** По S03 DistributedSampler при drop_last=False добавляет индексы до делимости по replicas; при True отбрасывает хвост. Для нового shuffle нужен `set_epoch` до итерации. По S07 train использует DistributedSampler при shuffle, loader ограничивает фактический batch размером dataset; S05 вызывает set_epoch. Наш вывод: считать уникальные кадры, processed images и optimizer updates отдельно, особенно на tiny set; DDP не создаёт новые независимые сцены. Тип: docs/code → inference.

**W1-14-F06 — workers/prefetch — измеряемые настройки.** S07 сохраняет workers между итерациями InfiniteDataLoader; фактическое число ограничено CPU/device count, запрошенными workers и числом batches; при единственном batch workers=0. Prefetch factor при workers>0 равен 4 для shuffle и 2 иначе; pin_memory включается только при доступном accelerator. S03 предупреждает о дополнительной памяти процессов и OS-dependent multiprocessing; pin_memory ускоряет передачу поддержанных tensors в CUDA. Больше workers не является универсальным ускорением. Тип: code/docs.

**W1-14-F07 — cache имеет прогрев, объём и версии.** По S06 disk cache пишет декодированный `.npy`, проверяя mtime; существующий свежий `.npy` может читаться даже при другом cache mode. RAM cache пакуется в `_ImageCache`: contiguous tensor, sharing с loader workers; при недостаточном Linux `/dev/shm` сериализация может перейти к копированию. Есть предупреждение о nondeterministic RAM caching. Это не доказательство единственного cache на все DDP ranks: dataset создаётся процессами. Наш вывод: cache=False не равнозначен доказанному холодному диску; измерять RAM по процессам, shared memory, disk bytes и начало run отдельно. Не применять старые issues о копировании памяти к новой версии без проверки.

**W1-14-F08 — profiler изменяет наблюдаемую систему.** S02 даёт CPU/CUDA activities, расписание wait/warmup/active, trace export. `record_shapes`/`with_stack` добавляют overhead; сохранение shapes может удерживать ссылки на tensors и менять память. Для CUDA trace нужен поддержанный backend/CUPTI; отсутствие kernel trace не доказывает отсутствие GPU работы. Наш вывод: локализовать bottleneck trace-ом, итоговый throughput повторить без profiler. Тип: docs → inference.

**W1-14-F09 — корректный timing должен дождаться GPU.** S09: CUDA operations асинхронны, поэтому CPU timer вокруг enqueue без synchronization недостоверен. Документация показывает CUDA Events и synchronize. Наш вывод: для end-to-end окна дождаться устройства на границах; для device-only времени использовать events. Не вставлять synchronize после каждой операции при измерении обычного pipeline: это меняет overlap. Тип: docs → instrumentation proposal.

**W1-14-F10 — seed не гарантирует перенос повторяемости.** S04 не обещает идентичность между релизами, commits, платформами, CPU/GPU даже при одинаковом seed; детерминизм может снижать скорость. Наш вывод: одинаковый seed на local/cloud нужен как контроль, но не служит доказательством равенства обучения. Повтор seed на одном split изучает training randomness; повтор независимых камер/сессий отвечает на другой вопрос. Тип: docs → inference; протокол качества передать evaluation/W1-15.

**W1-14-F11 — живая документация требует environment gate.** S08 сообщает ограничение Windows multi-GPU с official PyTorch wheels >=2.4 из-за libuv/TCPStore и предлагает Linux/WSL2. Она также предупреждает: custom trainer/dataset/augmentation не переносятся автоматически во внутренний DDP subprocess, нужен явный distributed launch пользовательского script. Это vendor documentation, не локальная проверка и не утверждение об ОС команды. Поле `profile` описано как ONNX/TensorRT speed profiling; оно не заменяет исследование loading/backward/communication и не измеряет LinQ.

## Очередь по value of information: предлагаемое решение, не факт статьи

**W1-14-F12 — распределять ресурс по ожидаемому изменению решения.** Рабочая карточка каждого trial: «неизвестное → две различимые причины → один изменяемый фактор → что решаем при каждом исходе → цена → срок полезности результата». Не запускать пять отличающихся многими параметрами recipes только ради занятых GPU. Не назначать численные вероятности успеха без данных. Приоритет выше у проверки, которая открывает или закрывает несколько последующих веток и успевает повлиять на интеграцию.

| Альтернатива | Когда её знание ценнее | Реальные статьи затрат, которые измерить | Условие продолжения |
|---|---|---|---|
| Независимые hypotheses, по одному GPU | Причина ошибки неизвестна: labels, scale, source/target, sampling | Подготовка каждого config, перенос dataset, короткий train, validation и разбор | Кандидат меняет нужный error slice при контролях; затем подтверждение |
| Дополнительные seeds | Разница кандидатов мала/нестабильна, выбор уже сужен | Полные paired repeats обоих кандидатов, оценка; не только выигравшего | Эффект согласован с правилом W1-15; иначе сохраняем неопределённость |
| Более длинный run | Проверены pipeline и labels, validation ещё улучшает нужные метрики | Дополнительные epochs плюс validation/checkpoint и позднее изменение recipe | Улучшение не ограничено train loss и не съедает время export/integration |
| DDP одного run | Установленный рецепт слишком медленен на критическом пути | Setup, all-reduce, sampler/BN checks, storage, дополнительные GPU-hours | Измеренное end-to-end ускорение даёт полезный результат раньше дедлайна |
| Ручная разметка/QA | Ошибки отражают missing/wrong labels, новый домен, мало разнообразия | Отбор, annotation, adjudication, export и повтор train; считать минуты и независимые группы | Ошибки исправлены и улучшение на нетронутом материале |
| Teacher/offline prelabel | Teacher закрывает нужный пробел с проверяемыми labels/student | Setup, inference по пулу, storage, ручная коррекция, student train/validation | Пригодный student улучшен; teacher AP сам по себе недостаточен |

DDP и независимые trials могут сочетаться: сначала небольшие раздельные проверки, затем распределённый финальный кандидат. Это не фиксированный план по часам. Для пяти человек общий дефицит может быть в review/annotation/доступе SDK: ещё один GPU не ускоряет последовательное согласование класса и compile gate. Резерв на validation/export/демо задаётся по реальному критическому пути, не по выдуманной универсальной доле времени.

### Измеримая экономика без выдуманных тарифов

Обозначить T_setup (env/data transfer/cache/DDP startup), T_train, T_validation, T_save, T_export_verify и H_review/H_annotation в person-minutes. Полезный результат приходит через T_ready = T_queue + T_setup + T_train + T_validation + T_save + T_export_verify + T_decision. Некоторые части перекрываются: хранить и timestamps, и critical path, а не механически складывать все задачи команды.

Для N одинаково оплачиваемых GPU: GPU-hours = N × оплачиваемое wall time в часах; денежная цена = GPU-hours × подтверждённый тариф + storage/network/минимальный billing interval/неудалённый instance. Тариф и условия доступа здесь не получены, поставщик не выбран. Учесть charging setup/idle/failure и срок жизни диска по реальным условиям будущего провайдера. Не объявлять локальный GPU бесплатным в смысле доступности: он может блокировать demo/debug.

Для одинакового объёма работы S_N=T_1/T_N и efficiency=S_N/N. Это только throughput comparison при сопоставимом workload, не quality scaling. DDP быстрее по wall-clock, но при S_N<N расходует больше GPU-hours. Для k одинаковых trials на k GPU независимый режим может дать k результатов примерно за длительность одного trial только при отсутствии очереди и общей CPU/storage/network конкуренции. Проверить это E03, а не обещать.

Кэш окупается по времени, если T_build + R×T_epoch_cached < R×T_epoch_uncached для реального числа повторов R; расходы на хранение/копирование и инвалидирование учитываются отдельно. При короткой проверке T_build может превышать всю экономию. При облачном cache на network filesystem требуются реальные read/write throughput и persistence; локальный SSD не предполагается.

## Предлагаемые проверки: не выполнены

Общее для E01–E05: пригодный checkpoint и repo revision от model_stack; snapshot данных и class map от datasets; отдельные train/validation по камерам/сессиям; fixed metrics/thresholds/selection от evaluation. Не использовать lockbox для выбора trials. У каждого run уникальный output directory, config diff, dataset hashes, seed, версии Python/torch/CUDA/driver, GPU model/VRAM фактического устройства, OS/CPU/RAM/storage, startup/finish timestamps и владелец. Успешное выполнение не доказывает inference на LinQ.

### W1-14-E01 — Найти bottleneck до масштабирования

- Входы/контроль: рабочий single-GPU train; тот же dataset/config/precision/seed; representative object counts и размеры, включая тяжёлые batches. Сначала correctness gate W1-12. Разрешение и модель не менять ради красивого throughput.
- Действия: записать cold setup отдельно; после прогрева ограниченное окно обычного train, затем короткий CPU/CUDA profiler с wait/warmup/active. Разметить получение batch, preprocessing, H2D, forward/loss, backward, update, validation/save. Для реального throughput повторить окно без profiler; дождаться GPU на границах (S02/S09).
- Метрики: processed images/s и unique images; step p50/p95, update count, loader wait, CPU/RAM/disk/network, peak allocated/reserved VRAM, kernel/communication timeline. Stage times при overlap не суммировать как независимые расходы.
- Артефакты: trace JSON, key averages, hardware/software manifest, timestamps и обычный throughput log; cold/warm и profiler on/off различены.
- Исходы: loader stalls → E02; GPU compute → кандидаты batch/precision из W1-12; communication только после DDP → E03. Нет CUDA trace → проверить supported activities/CUPTI, не угадывать bottleneck.
- Stop: заранее ограниченное диагностическое окно (например, до 100 измеряемых batches как предлагаемый cap, не факт скорости); OOM/NaN/ошибка labels немедленно прекращают performance-ветку. Достаточно локализованного bottleneck, не нужен полный train. Предел: профиль окна не предсказывает весь run с validation/close_mosaic/разными object counts.

### W1-14-E02 — Workers и cache с учётом старта

- Входы/контроль: E01, неизменные model/data/augmentation/precision; записанное состояние `.npy`, filesystem cache, RAM и shared memory. Изолировать от других jobs. Не удалять пользовательский cache ради теста: отдельная snapshot-копия/каталог по согласованной инженерной процедуре.
- Действия: сравнить baseline с небольшим увеличением workers; затем отдельно False/disk/ram при достаточном ресурсе. Менять один фактор, включать build time; повторить warm window. Образцы реально полученных images/labels проверить на равенство контракта.
- Метрики/артефакты: startup, first epoch, steady images/s, RSS/PSS где доступно, shared memory, disk bytes/I/O, actual workers/prefetch, warning logs; manifest cache mode и mtime/содержимого. Если ОС не даёт PSS, явно указать ограничение RSS и double counting shared pages.
- Исходы: выбрать минимальную сложность с полезным T_ready; RAM, вызывающий swapping, отвергнуть; cache, который не окупается на числе плановых epochs/trials, не включать ради максимума images/s.
- Stop: превышение заранее установленного headroom RAM/disk/shared-memory или деградация окна → остановка варианта; cap числа вариантов до запуска. Предел: faster loading не гарантирует quality; RAM warning о determinism остаётся существенным.

### W1-14-E03 — Один run DDP против независимой очереди

- Входы: реально доступные несколько GPU, compatible OS/backend и доступ к одному snapshot; workload после E01/E02. Сначала фиксировать доступный topology и failed-launch budget. Аренда не разрешена этим исследованием и не выполнялась.
- Контроль: одинаковый global batch и measured optimizer updates/sample exposure; fixed model, resolution, precision, recipe. Если local batch/BN/order/rect/accumulation неизбежно меняются, отметить это и проводить отдельное quality comparison, а не заявлять чистую hardware абляцию.
- Действия: короткий single-GPU и N-GPU workload, учесть startup/validation/save; trace каждого rank с уникальным именем; проверить actual sampler indices/update/accumulate и reductions. Отдельно N независимых trials с назначенными GPU и общим I/O нагрузить только в рамках малого диагностического окна.
- Метрики/артефакты: T_ready, S_N/efficiency, GPU-hours, per-rank utilization/VRAM/loader wait/collectives; logs env/rendezvous/backend и effective config, качество smoke-validation. Порты/output dirs отдельные; любые custom objects должны быть доступны subprocess.
- Исходы: DDP сокращает критический путь при принятой цене → финальный established recipe; contention/communication/startup съедают выигрыш → independent trials либо single GPU. Несколько слабых/разных машин через сеть не считать одним быстрым узлом.
- Stop: failed startup/расхождение данных/collective hang/time cap → прекратить диагностику, сохранить traceback; не тратить остаток подготовки на неизвестный distributed stack. Предел: короткий scaling-test не доказывает одинаковую сходимость и не переносится на RTX 4070/облако другой конфигурации.

### W1-14-E04 — Цена доразметки против ещё одного compute trial

- Входы: установленный тип ошибки на development-пуле; несколько независимых новых сцен, не test; annotation specification и независимый validation. Число кадров не назначено до появления данных. Контроль A — прежние данные и такой же рецепт; B — проверенная добавка данных; C при необходимости — продолжение A с сопоставимой дополнительной compute exposure.
- Действия: зафиксировать budget в person-minutes, images/objects и независимых scenes; учесть QA и correcting prelabels. Обучить B с тем же checkpoint и одинаковым правилом selection, сравнить A/C по ранее выбранному error slice и общим классам. Compute и annotation бюджеты отчитывать раздельно: это разные единицы.
- Метрики/артефакты: quality delta/FP/recall редких классов с поддержкой по группам, annotation/review/transfer/train elapsed, label changelog, frozen splits и predictions; paired repeats только когда требуется W1-15.
- Исходы: B закрывает пробел → следующая обоснованная порция labels; C лучше → исследовать learning limitation; ни один → пересмотреть visual signal/постановку. Stop: невалидная или неоднозначная разметка сначала разрешается, train прекращается; после исчерпания предзаданного budget без полезного эффекта ветка не расширяется автоматически. Предел: одна порция не устанавливает универсальную learning curve.

### W1-14-E05 — Условия назначения seeds, teacher и длинного run

- Входы/контроль: узкая очередь максимум нескольких объяснимых кандидатов, текущая стоимость E01, независимый validation. Записать решение, минимально полезный эффект и предел wall-clock до начала. Для teacher нужен подтверждённый путь к конечному student от W1-10/model_stack.
- Действия: если ranking близок к observed training noise, paired seeds A/B, а не «ещё seed только победителю»; если ошибка domain coverage — annotation E04; если teacher даёт полезные prelabels, учитывать ручную коррекцию и student training; если validated learning curve ещё полезно растёт — продление с сохранением recipe/selection.
- Метрики/артефакты: per-seed и per-group результаты, teacher QA/student delta, время людей и GPU, decision log и оставшийся integration path. Seed/split протокол не изобретать вместо W1-15/evaluation.
- Исходы/stop: продолжать только ветку, которая ещё может изменить конечный выбор до срока. Нет времени получить validation/export artifact — сохранить лучший уже проверенный кандидат. Stop по data leakage, невоспроизводимому config, потерям критичных классов или исчерпанию заранее назначенного budget. Предел: повтор seed не устанавливает перенос на новую камеру; teacher успех не проверяет student/LinQ.

## Открытые вопросы и адресные передачи

- **W1-14-Q01 → model_stack, приоритет первый:** какой checkpoint/trainer/image shape реально выбран и сколько памяти занимает один полный training step вместе с optimizer/EMA/объектами? От этого зависит batch, accumulation и вообще смысл DDP. Получить manifest и E01, не выводить из названия RTX 4070.
- **W1-14-Q02 → training owner/окружение:** какая ОС, torch wheel/backend, GPU count/topology, CPU/RAM/shared memory, local/network storage и доступ? S08 даёт конкретный Windows compatibility gate, но окружение неизвестно. Способ ответа — inventory и bounded startup E03; не покупка ресурсов.
- **W1-14-Q03 → datasets/W1-08:** сколько независимых сцен нужно для полезной добавки labels, каков реальный QA throughput и покрытие ошибок? Закрывается E04, не количеством соседних кадров.
- **W1-14-Q04 → evaluation/W1-15:** какой эффект меняет решение, какие slices критичны, сколько paired repeats оправдано? Seeds не должны замещать независимые группы. Источники F10 и proposed E05.
- **W1-14-Q05 → W1-12/model_stack:** требуется ли изменение цикла accumulation для no_sync и как проверить loss normalization, BN и хвосты? S05 показывает текущее поведение, но правка trainer здесь не сделана и её выгодность не установлена. Нужен trace E03 и correctness comparison до изменения.
- **W1-14-Q06 → linq_platform/video_architecture:** какое время нужно на фактический export/compile/upload/inference verification и какие входы/модели допустимы? Этот последовательный gate должен участвовать в T_ready; RTX profiling и Ultralytics `profile` его не измеряют.
- **W1-14-Q07 → hackathon_strategy:** какие подтверждённые сроки checkpoint/integration и какой человек принимает quality решение? Параллельность GPU ограничена доступным review; рекомендации этой ветки не являются обещанным расписанием.

Главная оставшаяся неопределённость эмпирическая: неизвестен workload и bottleneck. Первичные документы достаточны для выбора измерений и обнаружения скрытых изменений recipe, но не дают честной численной оценки скорости/стоимости нашей команды.
