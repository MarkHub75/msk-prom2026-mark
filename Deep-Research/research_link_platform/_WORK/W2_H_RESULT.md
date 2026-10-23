# W2-H — аппаратные исполнения, память и multi-device mapping

Вопросы K010, аппаратная часть K002 и граница масштабирования K011. Проверка 23.10.2026 04:59–05:05 Europe/Moscow (UTC+3); исторический контекст подготовки тот же. До начала прочитаны исходное задание, CRITIC, W1-02 result/source extracts, guide, presentation p2/p3, RUN_SCENARIO и релевантный исходный код. Только исследование открытых источников; SDK не установлен, компиляция, подключение к ускорителю и inference не выполнялись. Получения доступа/устройства из RUN_STATE не следует.

## Решение и изменение относительно W1

**Существенный новый ответ:** две ёмкости HP действительно документированы для разных исполнений: HP1M-01 — 16 ГБ (2×8), HP1M-02 — 32 ГБ (2×16). Значит, нельзя считать любое упоминание HP16/32 внутренним противоречием одного SKU. Однако каталог подписывает общий 16-ГБ datasheet как HP1M-02; этот конкретный конфликт назначения ссылки остаётся. Оба руководства описывают PCIe2.0x8, что согласуется с presentation2026 p3 и не согласуется с общим datasheet Gen3.

**Второй ответ:** различием Active/Passive нельзя объяснить обнаруженные пределы мощности: руководства HPD1M-00 и -01 оба задают ≤100Вт; HPD1M-10 и -11 оба ≤150Вт; активные datasheet по-прежнему задают60/70 и120/140Вт. Три набора чисел (руководство / datasheet / presentation) нужно сохранять с областью и типом метрики, не усреднять и не выдавать за историю ревизий.

**Третий ответ:** найденный конкретный multi-device путь — репликация одного `.tpu` по устройствам с разделением набора изображений между subprocess. Это не пример распределения одного графа между DDR нескольких чипов. В guide `slicing_scheme` относится памяти одного микропроцессора; второй DDR описан в контексте его конвейеров. Способ использования одной моделью суммарной памяти карты не установлен, но утверждение «платформа не умеет» также не доказано.

K010: уточнена область, часть memory/SKU вопроса закрыта; actual target/card/BDF/runtime mapping остаётся открытым. K002: exact target должен происходить из поставки и metadata, имя HP/HPD не заменяет compiler hardware parameters. K011: для независимых реплик возможен throughput scaling; ни число `/dev`, ни этот код не доказывают ускорение одного запроса или линейность.

## Факты с границами доказательства

**W2-H-F01 (primary_documentation, text-only):** публичный каталог группирует HP1M-01 и -02 под HP; HPD1M-00 Active / -01 Passive под HPD; HPD1M-10 Passive / -11 Active под HPQ. Это уже прямой пример, почему префикс HPD1M без суффикса не означает ровно двухчиповую карту. S01.

**W2-H-F02 (primary_documentation, text-only):** HP1M-01 p5–6: ≤35Вт, ≥750МГц, одна H1M, DDR4ECC16ГБ, два канала по8ГБ/72bit, PCIe2.0x8 Endpoint; p12 ожидает одну строку2805:0006 rev08. HP1M-02 p5–6: тот же предел мощности/частоты, одна H1M, DDR4ECC32ГБ, два канала по16ГБ/72bit, PCIe2.0x8; p14 ожидает одну такую строку. S02/S03. Это разные документированные комплектации, без доказанной хронологии перехода01→02. В HP02 p3/p7 повторено одно и то же обозначение в двух позициях; не трактовать шаблонное дублирование как два чипа или две разные ревизии.

**W2-H-F03 (primary_documentation, text-only):** HPD1M-00 Active p5–6: ≤100Вт,32ГБ,2H1M, по16ГБ на чип, каждый2×8ГБ, PCIe3.0x16; p14 — два endpoint. HPD1M-01 Passive даёт ту же структуру/предел мощности. S04/S05. HPD active datasheet p2 даёт60/70Вт, как W1 passive datasheet. Следовательно, простая гипотеза «100Вт из-за вентилятора активной версии» не объясняет расхождение:100Вт написано и для пассивной.

**W2-H-F04 (primary_documentation, text-only):** HPQ/HPD1M-11 Active p5–6: ≤150Вт,64ГБ,4H1M,16ГБ на чип,2×8ГБ на чип, PCIe3.0x16; p8PEX8747, p14 четыре endpoint2805:0006 rev08. Passive -10 также имеет4чипа/64ГБ/≤150Вт. В -11 p6 составная плата названа HPD1M-10, а встроенное ПО -11: возможная общая плата или шаблонный перенос текста, ни одно объяснение не доказано. Имя платы не является firmware/SDK compatibility manifest. S06/S07.

**W2-H-F05 (primary_documentation + inference):** H1M↔К1945ВМ3Я прямо задано presentation p2, как уже установлено W1; это не новый неизвестный. Там PCIe controller чипа Gen3x8. Presentation p3 при этом пишет HP2.0x8 и HPD/HPQ3.0x16. Возможность контроллера и спецификация реализации карты имеют разный scope; такое различие само по себе допустимо, но не доказывает Gen3 для фактической HP. Текст p3 даёт <30/<55/<105/<1150Вт для HP/HPD/HPQ/HPS, без условий режима. Новая сетeвая текстовая копия подтверждает W1 transcription, но визуальная проверка не выполнена. S08.

**W2-H-F06 (primary_documentation, text-only):** Framework guide p9 `compile_(hardware_parameters,network,parameters,slicing_scheme=None)` описывает slicing_scheme как распределение тензоров в памяти микропроцессора IVA H1. `get_hw_params(tpu_type)` и пример `128x128_asic` задают отдельное понятие target. p10 второйDDR, банки кеша, сроки жизни тензоров и слайсер слоёв описываются как оптимизации размещения/конвейеров. Это полезное прямое memory-planning свидетельство, но в этих разделах нет node/device ID, межчипового канала, remote allocation или правила суммы DDR. Нельзя переименовать этот механизм в multi-chip sharding. S09.

**W2-H-F07 (source_code, static inspection; not execution):** pinned benchmark commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`, RUN_SCENARIO дата2026-03-25, §8 сообщает о четырёх обнаруженных на сервере `/dev/tpu3…0` и использует labelHPD1M. `run_resnet50_parallel_direct.py` L202–325: для каждого `(device,shard_path)` запускает subprocess одного `run_resnet50_accuracy.py`, передавая одинаковый `--program-path` и отдельный `--device`; ожидает все процессы, суммирует число изображений и делит на полное wall time. `run_resnet50_accuracy.py` L296–315 выбирает device и делает `Device.open(device_id)`/`load(program_path)`. Это data parallel replication. Таймер direct пути захватывает запуск и завершение subprocess; его aggregate FPS нельзя называть чистым device compute. S10. Remote bytes именно parallel_direct независимо получены и совпали с W1 SHA256.

**W2-H-F08 (source_code + inference):** build_resnet50_program.py L262/L364 использует `TPU_128x128_PARAMS`, а не SKU HPD1M; один и тот же target ещё не гарантирует совместимость со всеми ёмкостями памяти/поставками. Исторический pytpu15.0.24 `_bindings.py` L180–229 перечисляет имена файлов `/dev` по regex и длине и передаёт выбранный путь native `tpu_create_device`; Python-listing не возвращает физический SKU/BDF/серийный номер. Эта старая реализация не доказывает поведение Runtime16.18.6, но демонстрирует конкретную причину не считать `list_devices()` inventory физической карты. S11.

## Таблица конфликтов и текущий статус

| Вопрос | Документированные значения и scope | Вердикт / что закроет |
|---|---|---|
| HP16/32ГБ | HP01=16; HP02=32; общий datasheet=16, каталог подписывает02 | **Частично разрешено SKU.** Ёмкости01/02 установлены; неправильность ссылки либо иной scope datasheet неизвестны. Нужна этикетка/SKU поставки и matching datasheet |
| HP PCIeGen3/2 | общий datasheetGen3; HP01/02 guides2.0x8;2026p3=2.0x8; чип p2Gen3x8 | **Уточнена область.** Чип capability не карта; конфликт общего datasheet остаётся. Нужны actual LnkCap/LnkSta каждого segment и ответ вендора |
| HPD60/70,≤100,<55Вт | Active+Passive datasheet60/70; оба guides≤100; presentation<55 | **Не разрешён.** Active/Passive не объясняет. Режим/метод/ревизия/граница измерения неизвестны |
| HPQ120/140,≤150,<105Вт | Active+Passive datasheet120/140; оба guides≤150; presentation<105 | **Не разрешён.** Разные формы спецификации могут сосуществовать, но соответствие условиям не дано |
| HPS1000/1150/1500Вт | W1 семейная таблица до1000;2026p3<1150; собственный datasheet режимы до1500 | **Не разрешён.** Нельзя вывести исправленную величину или историю поколения из годов URL/title |
| HPD/Q «8линий» против x16 | datasheet проза8; таблицаx16; guides внешнийx16+PEX8747; чипx8 | **Уточнены уровни.** Внешний x16 не противоречит x8 чипа; конкретная проза не локализует link. Не выдавать8линий за upstream topology |
| HPD1M +4 `/dev` | §8 четырёхпроцессный пример; HPD01 два endpoint, HPQ10/11 четыре | **Открыт physical mapping.** Может быть HPQ с общим префиксом, две HPD, иной host/label; ни одна версия не выбрана без BDF/serial tree |
| Сумма DDR одной модели | физическая память разнесена; guide slicing только одного микропроцессора; пример реплик | **Открыто**, не установлен запрет. Нужны documented multi-chip graph/sample и planner/runtime proof |

Числа мощности — опубликованные спецификации/заявления, не наши измерения. Различие «типовая/пиковая» против «не более» само по себе не логическое опровержение; оно не даёт разрешения использовать меньший предел для электропитания или обещать частоту.

## Mapping: что документировано и какой переход ещё надо измерить

| Карта/исполнение | Чипы и локальная DDR | Host-side hardware discovery из РЭ | Runtime mapping |
|---|---|---|---|
| HP1M-01 |1H1M,16ГБ=2×8 |1×2805:0006 rev08; внешнийPCIe2.0x8 |BDF↔`/dev/tpuN` не опубликовано в изученном contract |
| HP1M-02 |1H1M,32ГБ=2×16 |1×тот же ID; внешний2.0x8 |то же; ёмкость32 не выводится из ID |
| HPD1M-00/01 |2H1M,каждый16ГБ;32всего |2×тот же ID заPEX8747; внешний3.0x16 |один runtime context на выбранный путь в примере; число разрешённых contexts/quota неизвестно |
| HPQ/HPD1M-10/11 |4H1M/К1945ВМ3Я,каждый16ГБ;64всего |4×тот же ID заPEX8747; внешний3.0x16 |нужна фактическая привязка всех четырёх путей к одной карте |

Цепочка доказательства: **этикетка/серийный номер карты → upstream switch и BDF-tree → BDF чипа → driver device node → runtime device info → loaded artifact/target → inference context/request**. Таблица не утверждает установленную биекцию BDF↔node для отсутствующего драйвера. Сам PCI ID одинаков у разных исполнений и недостаточен для установления объёма памяти. Число endpoint не включает мосты/switch functions; число строк всей `lspci` нельзя сравнивать напрямую с числом чипов.

## Первый inventory после реального доступа (предлагаемый протокол, не выполнен)

1. Зафиксировать access mode, host/container, точные разрешённые устройства и квоту. Получить SKU, ревизию платы, serial и matching release manifest от оператора; для service-only запросить эквивалентную inventory запись. Наличие4устройств на host ещё не означает, что4даны команде.
2. На разрешённом Linux host сохранить `lspci -Dnn`, `lspci -t`, затем `lspci -Dvv -s <observed-BDF>` для chip и upstream ports. Разделить LnkCap и LnkSta, upstream и downstream; сохранить состояние нагрузки/энергосбережения. Команды здесь стандартные read-only host diagnostics, не LinQ CLI; не запускались в этом исследовании.
3. Для реальных `/dev/tpu*` сохранить major/minor, sysfs/udev association если экспортируется драйвером, и сопоставить с BDF. Не угадывать путь `/sys/class/...` до inventory. Если связи нет, запросить driver mapping у поставщика; container node может скрывать host topology.
4. Через API именно выданной версии сохранить device info и program metadata полностью, без выдуманного списка обязательных полей; отдельно выделить target, доступную DDR, служебный резерв/лимит allocation, clock/power mode, driver/firmware/native library versions. Старый `Device.info()` — зацепка, не гарантия current schema.
5. Один known-good артефакт сначала на одном разрешённом устройстве: planner report (weights/activations/scratch/cache и максимум per DDR/channel), load footprint, correctness. Затем независимые реплики на2/4: запросы с frame IDs, per-device logs, p50/p95 и end-to-end FPS. Не проверять pooled memory через OOM на shared host.
6. Если заявлен graph partitioning: взять vendor sample, где один граф явно распределён по двум чипам и превышает доступную память одного; получить partition manifest, transfer edges, planner allocations и выводы correctness на каждом этапе. Физический peer-to-peer через switch сам по себе не доказывает поддержку compiler/runtime.

Решающий эксперимент: inventory + одинаковый корректный graph на1/2/4 независимых устройствах с подтверждённым mapping и одним набором timing boundaries. Это снимает опасное смешение числа физических карт, числа чипов и эффективного throughput. Проверка graph partitioning — отдельный эксперимент только после документированного подтверждения API.

## Источники и происхождение

Все source URLs ниже реально запрошены23.10.2026 около05:01–05:03MSK. Издатель hardware/guide — ООО«ХайТэк»/LinQ; даты/редакции руководств не установлены. Content extraction TinyFish — сетевое текстовое свидетельство PDF, **не локальные PDF bytes, не визуальный просмотр**. Полные JSON с actual responses сохранены в `_WORK/W2_H/PRIMARY_FETCH.json`, `ACTIVE_FETCH.json`, `CONTROL_FETCH.json`; поле published_date=null. Заголовок HPD datasheet содержит2025.03, но это не проверенная видимая дата редакции.

| ID | Прямой первичный локатор и заголовок | Место / версия |
|---|---|---|
| W2-H-S01 |https://lin-q.ru/docs — LinQ_Документация |группыHP/HPD/HPQ;каталог/ссылки |
| W2-H-S02 |https://files.lin-q.ru/tpu/docs/_HPact_manual_LINQ_HP1M_01.pdf — РЭHP1M-01 |p5–6,8,12;19стр |
| W2-H-S03 |https://files.lin-q.ru/tpu/docs/_HPact_manual_LINQ_HP1M_02.pdf — РЭHP1M-02 |p5–8,14;21стр |
| W2-H-S04 |https://files.lin-q.ru/tpu/docs/_HPDact_manual_LINQ_HPD1M_00.pdf — РЭHPD1M-00 |p5–6,14 |
| W2-H-S05 |https://files.lin-q.ru/tpu/docs/_HPDpass_manual_LINQ_HPD1M_01.pdf — РЭHPD1M-01 |p5–6,8,14 |
| W2-H-S06 |https://files.lin-q.ru/tpu/docs/_HPQact_manual_LINQ_HPD1M_11.pdf — РЭHPD1M-11 |p5–6,8,14 |
| W2-H-S07 |https://files.lin-q.ru/tpu/docs/_HPQpass_manual_LINQ_HPD1M_10.pdf — РЭHPD1M-10 |p5–6,8,14 |
| W2-H-S08 |https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf — Решения для ускорения работы искусственных нейронных сетей на базе процессоровLinQ |p2/p3;на обложке2026;metadata author СеврюковСергей |
| W2-H-S09 |https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf — Руководство оператора.Фреймворк |RU.РМДВ.04.06.014-03 34 01;p9–10,p22–23 sample;не current ABI guarantee |
| W2-H-S10 |https://github.com/sherstpasha/linq-cv-bench/tree/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140 |автор repo — handle `sherstpasha`; RUN_SCENARIO §8; parallel_direct L202–325; accuracy L296–315; third-party первичный код |
| W2-H-S11 |https://pypi.org/project/pytpu/15.0.24/ |saved sdist `_bindings.py`L180–229;историческая версия15.0.24,не current native library |
| W2-H-S12 |https://files.lin-q.ru/tpu/me2025/ds_LinqHPD_act.pdf и https://files.lin-q.ru/tpu/me2025/ds_LinqHPQ_act.pdf |active datasheets p2;совпадение чисел с W1passive,не proof byte identity |
| W2-H-S13 |https://files.lin-q.ru/tpu/datasheet/linq_hp_datasheet.pdf |p2:16ГБ/Gen3/25–35Вт;подпись каталогаHP1M-02 не внутриPDF |

Remote source S10 independently downloaded at2026-10-23T02:03:02Z: https://raw.githubusercontent.com/sherstpasha/linq-cv-bench/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/classification/run_resnet50_parallel_direct.py ;15728bytes;SHA256`2a3c63f932a2acbc4aa4f75258674ad1e9f3d2a88746e9b0777d48545f6a7992`, совпадает с W1. Saved RUN_SCENARIO SHA256`39eac9f06cfed3592ad5e077b865d812ffffa195d9428c8854dbc27d926f4446`;это hash локального сохранённого файла, не новый удалённый fetch RUN_SCENARIO. Code provenance и проверка исполнения различаются.

## Отрицательные попытки, фальсификация и оставшиеся неизвестные

- web.open HP02/presentation/docs вернул not accessible/Internal Error. TinyFish fetch вернул содержательное текстовое представление тех же URL и дополнительных variant manuals; таким образом live binary availability не приравнена отсутствию документа.
- curl.exe HTTPSHP02: schannel handshake failure. Независимый urllib verifiedTLSHTTPS: SSLEOFError; HTTP: remote disconnected. Exact methods/times/headers/source hash в `RETRIEVE_PROBE.py`/`RETRIEVE_PROBE_RESULT.json`. PDFbytes не получены; PDFmetadata CreationDate/ModDate, SHA256PDF и screenshots отсутствуют. PDF skill прочитан для read-only review; render невозможен без bytes; ни URL, ни returned screenshot link не выданы за просмотр.
- Targeted TinyFish queries `site:lin-q.ru (память OR памяти) (распределение OR граф OR multi OR HP1M)` дали только/sol,/tech; `site:files.lin-q.ru LinQ распредел памяти` —0. Queries `LinQ TPU multi-chip`, `LinQ memory planner`, `LinQ HP1M-02` дали преимущественно омонимы. Сырые ответы SEARCH*.json сохранены; отсутствие релевантных search hits — ограничение индекса, не отрицательное доказательство capability. Broad web queries model parallel/shared memory/graph partition также дали .NET омонимы и не использовались как технические источники.
- Гипотеза«ёмкость просто опечатка» ослаблена явными01/02; «различие100/150Вт только из-заActive» опровергается парными руководствами; «slicing_scheme доказывает память карты» не выдерживает scope одного микропроцессора; «четыре/dev доказывают одну двухчиповуюHPD» не выдерживает ни каталога, ни отсутствия BDF inventory.
- Revision/BOM chronology остаётся неизвестна. Нужны паспорт выделенной карты, versioned matching PDFs, release/board revision и настройки. Presentation2026 не считается автоматически более точной аппаратной нормой, поскольку не идентифицирует SKU и режим мощности.
- Нет доказанного single-graph DDR limit, резерва runtime, current memory-planner output, remote memory, graph partitioning, peer transfer API, current context concurrency. Требуется matchingSDKreference/example и actual targeted experiment; новый source search не закрывает это догадкой.

## Компактная передача

Для root: заменить общее «HP 16/32 — конфликт» на «HP01 = 16 ГБ, HP02 = 32 ГБ; общий datasheet под ссылкой02 пока даёт16 ГБ». HP PCIe2.0 подтверждён двумя manuals и presentation text; Gen3 остаётся capability чипа/старого family datasheet. Добавить power controls: Active и Passive имеют одинаковые maxima100/150 Вт; обе разновидности охлаждения не снимают конфликт с datasheet/presentation. Четыре устройства — server inventory claim из third-party §8; префикс HPD1M не даёт числа чипов. Multi-device исходник показывает независимые реплики, не pooling. W2-G/J/M: не полагаться на старый list_devices для физического inventory; полный mapping и versioned info надо получить у actual driver/runtime. W2-I: direct parallel timer включает subprocess lifecycle, число карт и выигрыш задержки одного запроса из него не следуют.
