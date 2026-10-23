# RAW_FACTS — LinQ: нормализованная доказательная база

Актуальность источников:23.10.2026, 04:15–05:14 MSK. Это подробные наблюдения двух волн, не итоговый литературный отчёт. F-ID стабилен; S-ID ведёт к источнику и точному locator/provenance. Каждая карточка сохраняет отдельные evidence_type и actual_check. Дата проверки не является датой выпуска. W1 наблюдения остаются историей поиска; при расхождении действует явно указанная W2 disposition, а не удобная формулировка.

## Реально выполненные проверки

- Сетевое чтение/архивы/исходники/AST и helper-пробы; протоколы под `_WORK`.
- W2-E: скачаны реальные ONNX35,511,756B и weights35,434,956B; сравнены13conv kernels и2final biases; ONNX Runtime1.31.0 CPU: b1 success, b2 Squeeze failure; выполнена diagnostic head-only derivative. Это actual CPU model inference.
- W2-D/G: shape helper и fake-native host probes, включая output view ownership; native `.so` не загружалась.
- Не выполнены proprietary SDK installation/import/conversion/calibration/compile/TLM/LinQ inference. Пользовательский исход регистрации неизвестен. Не утверждается отсутствие возможностей у закрытой поставки.

## Обязательные W2 corrections для чтения W1

1. `tf.graph_util.import_graph_def` существует в upstreamTF2.14.1; `Session(graph=None)` использует default graph. Немедленный crash/отсутствующий namespace не доказаны; остаются return/type/import namespace/names seams.
2. Отсутствие output `.copy()` вpytpu15.0.24 не доказывает dangling: Python-owned backing удерживается base chain в host probe. Historical exception cleanup omission узко подтверждён mock, современный дефект не установлен.
3. ModelZooTinyYOLO3 — реальные fine masks1,2,3 и embeddedNMS .6/.5/max20, исходный Darknet/runner0,1,2; public conv lineage не равна full-graph parity и не касается невыданного vendor.tpu.
4. IVA CV `walkers-node:0.1.310` — склейка0.1.3+page10 по двум page-separated text extractions; visual/registry не подтверждены. Другие tags тоже склеены. Ниже W1 literal хранится только как история, не команда запуска.
5. HP01=16GB,HP02=32GB документированы отдельно; общий datasheet под ссылкой02 всё ещё16GB/Gen3. Multi-device sample — реплики, pooled-memory graph не установлен.
6. W1 blanket «никакого inference» относится W1/LinQ; W2 имеет actual public CPU inference.


## W1-01 — W1-01 — названия и происхождение LinQ

<a id="f001"></a>

### F001 — производитель и идентификаторы

- Исходный локатор: [W1-01-F01](_WORK/W1_01_RESULT.md), строка54; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S001](SOURCES.md#s001), [S018](SOURCES.md#s018)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F001](RAW_FACTS.md#f001): производитель и идентификаторы

Тип `vendor_statement`; статус `read_web`. На lin-q.ru указан ООО «ХайТэк», ИНН **7722826409**, ОГРН **5137746105712** [[S001](SOURCES.md#s001)]. Это надёжный способ отсечь одноимённые компании при поиске, но не выписка ЕГРЮЛ и не проверка корпоративных прав на 2026 год. Домашняя страница hi-tech.org сейчас описывает **ООО «Хайтэк-Интеграция»**, ИНН **7722350688**, ОГРН **5157746196482** [[S018](SOURCES.md#s018)]. Нельзя смешивать текущего владельца сайта/раздела и изготовителя процессора.

<a id="f002"></a>

### F002 — текущая спецификация чипа и память разных уровней

- Исходный локатор: [W1-01-F02](_WORK/W1_01_RESULT.md), строка58; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S002](SOURCES.md#s002)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F002](RAW_FACTS.md#f002): текущая спецификация чипа и память разных уровней

Тип `vendor_statement`; статус `read_web`. [S002](SOURCES.md#s002): чип LinQ H, 28 нм, BGA1296, RISC-V как управляющий процессор, 500–812 МГц; 16 МБ встроенной памяти, DDR4+ECC до 32 ГБ, PCIe Gen3 endpoint x8, систолический массив 128×128, int8. Это текущая рекламно-техническая страница без версии/даты ревизии. Нельзя считать 32 ГБ гарантированным объёмом любого модуля: конкретная плата может комплектоваться иначе. RISC-V относится к указанной текущей странице, а не автоматически к историческим IVA H.

<a id="f003"></a>

### F003 — исторические FW_TPU_H/E действительно существуют как разные продукты

- Исходный локатор: [W1-01-F03](_WORK/W1_01_RESULT.md), строка62; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation + vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S004](SOURCES.md#s004), [S005](SOURCES.md#s005), [S006](SOURCES.md#s006), [S007](SOURCES.md#s007)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F003](RAW_FACTS.md#f003): исторические FW_TPU_H/E действительно существуют как разные продукты

Тип `primary_documentation`/`vendor_statement`; статус `read_tinyfish`. Старые официальные страницы отдавали отдельные описания H и E, OEM-условия и ссылки на собственные руководства [[S004](SOURCES.md#s004), [S005](SOURCES.md#s005), [S006](SOURCES.md#s006), [S007](SOURCES.md#s007)]. Одинаковая общая схема «квантование → компиляция» и Python 3.8 API/CLI не доказывают совпадение наборов операций, ISA или готовых артефактов.

<a id="f004"></a>

### F004 — раннее руководство нельзя молча превратить в текущую спецификацию

- Исходный локатор: [W1-01-F04](_WORK/W1_01_RESULT.md), строка66; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S008](SOURCES.md#s008), [S018](SOURCES.md#s018)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F004](RAW_FACTS.md#f004): раннее руководство нельзя молча превратить в текущую спецификацию

Тип `primary_documentation`; статус `indexed_pdf_read`, без запуска. [S008](SOURCES.md#s008) прочитан как PDF из поискового индекса: 61 лист, титул 2021. Аннотация и §1.1 прямо определяют FW_TPU_H для IVA H. §1.3 перечисляет Ubuntu 18.04 LTS+, TensorFlow **2.4.1**, GCC **7.3.1**, cuDNN **8.0**, CUDA **11.0**, Python **3.8.6**, ≥32 ГБ RAM, ≥512 ГБ SSD/HDD; в комплекте `SMP.zip`, `installer.sh`, `dnn_quant.rst`; оглавление включает `dnn_quant`, TPU Frontend, `tcf`. Этого достаточно для идентификации поколения. Не предписывать эти версии команде до сверки с современным руководством. Текущая доступность самого PDF неоднозначна: повторный open вернул HTML системного интегратора [[S018](SOURCES.md#s018)].

<a id="f005"></a>

### F005 — современная связь IVA H1 с LinQ H явная

- Исходный локатор: [W1-01-F05](_WORK/W1_01_RESULT.md), строка70; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F005](RAW_FACTS.md#f005): современная связь IVA H1 с LinQ H явная

Тип `vendor_statement`; статус `read_web`. В [S003](SOURCES.md#s003), раздел ПО, название содержит **«IVA H1»**, целевая аппаратная OEM-система — **LinQ H**. На той же странице указаны Python 3.8 API/CLI и квантование/компиляция. Раздел получения ПО требует регистрации и верификации. Это подтверждает связь продукта/названия, не номер пакета или совместимость FW_TPU_H образца 2021. Публичная `/docs` найдена соседней веткой; ограничение раздела скачивания нельзя распространить на всю документацию.

<a id="f006"></a>

### F006 — H1 и H1М требуют выяснения, а не нормализации редактором

- Исходный локатор: [W1-01-F06](_WORK/W1_01_RESULT.md), строка74; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S015](SOURCES.md#s015)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F006](RAW_FACTS.md#f006): H1 и H1М требуют выяснения, а не нормализации редактором

Тип `vendor_statement`; статус `read_web`. [S015](SOURCES.md#s015) называет фреймворк **LinQ H1**, а аппаратную архитектуру **LinQ H1М**. Нужно сохранить обе строки, включая кириллическую М в последнем написании. Они могут означать разные уровни наименования/ревизии; утверждать опечатку или новое поколение оснований нет.

<a id="f007"></a>

### F007 — внешние авторские результаты относятся к неуточнённой старой среде

- Исходный локатор: [W1-01-F07](_WORK/W1_01_RESULT.md), строка78; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S017](SOURCES.md#s017), [S002](SOURCES.md#s002)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F007](RAW_FACTS.md#f007): внешние авторские результаты относятся к неуточнённой старой среде

Тип `reported_measurement`; статус `read_web`, не воспроизведено. Нефёдов и студенты ([S017](SOURCES.md#s017)) описывают IVA TPU, удалённый GUI, STAGING, batch 1/2/4/8; сообщают о сбоях компиляции/запуска сложных сетей и отличиях времени компиляции. Указанный ими теоретический предел — 16 трлн операций/с; современный [S002](SOURCES.md#s002) — 24 TOPS int8. В материале есть терминологические неточности (плавающая точка против целочисленной спецификации; процессор назван PCIe-изделием), нет полной ревизии устройства/SDK. Ценность — список будущих проверок STAGING/latency, а не доказательство сегодняшней ошибки LinQ. Ссылку на исходные таблицы облака в этой ветке не проверяли.

<a id="f008"></a>

### F008 — облачный сервис — отдельный программный слой

- Исходный локатор: [W1-01-F08](_WORK/W1_01_RESULT.md), строка82; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S014](SOURCES.md#s014)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F008](RAW_FACTS.md#f008): облачный сервис — отдельный программный слой

Тип `vendor_statement`; статус `read_web`. В вакансии на [S014](SOURCES.md#s014) описаны Python-прототип облачного inference-as-a-service и C++ пре-альфа. Дата вакансии отсутствует. Это след существования серверного ПО в дополнение к компилятору/драйверу, но не установленная конфигурация хакатонного доступа и не готовая спецификация REST/gRPC.

<a id="f009"></a>

### F009 — Карта объектов

- Исходный локатор: [W1-01-MATRIX-1](_WORK/W1_01_RESULT.md), строка17; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation + vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S001](SOURCES.md#s001), [S014](SOURCES.md#s014), [S002](SOURCES.md#s002), [S012](SOURCES.md#s012), [S013](SOURCES.md#s013), [S009](SOURCES.md#s009), [S010](SOURCES.md#s010), [S011](SOURCES.md#s011), [S004](SOURCES.md#s004), [S005](SOURCES.md#s005), [S006](SOURCES.md#s006), [S007](SOURCES.md#s007), [S008](SOURCES.md#s008), [S003](SOURCES.md#s003), [S015](SOURCES.md#s015)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Карта объектов

| Объект | Уровень | Установленное значение | Источник / тип / проверка |
|---|---|---|---|
| LinQ | Бренд/экосистема | Объединяет собственный процессор, модули и необходимое ПО | [S001](SOURCES.md#s001), [S014](SOURCES.md#s014) / vendor_statement / read_web |
| LinQ H | Микрочип, TPU | Текущий сайт: 28 нм, BGA1296, int8; это основание модулей, не готовый сервер | [S002](SOURCES.md#s002) / vendor_statement / read_web |
| LinQ HP | PCIe-модуль | Один LinQ H | [S001](SOURCES.md#s001) / vendor_statement / read_web |
| LinQ HPD | PCIe-модуль | Два LinQ H | [S001](SOURCES.md#s001) / vendor_statement / read_web |
| LinQ HPQ | PCIe-модуль | Четыре LinQ H | [S001](SOURCES.md#s001) / vendor_statement / read_web |
| LinQ HPS | Внешний высокоплотный ускоритель | До 10 HPD/HPQ, стойка 19 дюймов; не один чип | [S001](SOURCES.md#s001) / vendor_statement / read_web |
| LinQ HX | Одноплатная встраиваемая система | SBC 3,5 дюйма; LinQ H плюс RK3588 | [S001](SOURCES.md#s001) / vendor_statement / read_web |
| LinQ HPC | ПАК партнёров | Два HPS, PCIe-коммутация RSC ScaleStream-C, подключённый сервер | [S012](SOURCES.md#s012) / vendor_statement партнёра / read_web |
| GraLinQ AI | Серверный аппаратный комплекс | Сервер «Гравитон» с платой «Онега» и модулями HPD | [S013](SOURCES.md#s013) / vendor_statement партнёра / read_web |
| IVA TPU (исторически) | Архитектура/IP и коммерческое обобщение | В статье разработчиков — СФ-блок; в иных источниках — процессор/ускоритель как общее имя | [S009](SOURCES.md#s009), [S010](SOURCES.md#s010), [S011](SOURCES.md#s011) / разные типы, см. ниже |
| IVA H, IVA E | Исторические микросхемы | Две реализации IVA TPU с разными параметрами конфигурации; не взаимозаменяемые имена | [S009](SOURCES.md#s009) / primary author publication / search_extract_only |
| FW_TPU_H, FW_TPU_E | Историческое ПО | Разные целевые IVA H и IVA E | [S004](SOURCES.md#s004), [S005](SOURCES.md#s005), [S006](SOURCES.md#s006), [S007](SOURCES.md#s007), [S008](SOURCES.md#s008) / primary_documentation / read_tinyfish, indexed_pdf_read |
| IVA H1 / LinQ H1 / LinQ H1М | Имена в современной программной цепочке | IVA H1 фигурирует в названии OEM-ПО; новость использует LinQ H1 для framework и LinQ H1М для цели компиляции | [S003](SOURCES.md#s003), [S015](SOURCES.md#s015) / vendor_statement / read_web |

Пиковые показатели в карте нужны исключительно для распознавания уровня системы: H — 24 TOPS int8 [[S002](SOURCES.md#s002)], HPS — до 960 TOPS [[S001](SOURCES.md#s001)], HPC — 1920 TOPS [[S012](SOURCES.md#s012)], GraLinQ AI — 384 TOPS [[S013](SOURCES.md#s013)]. Это заявления разных конфигураций, а не противоречащие измерения одного чипа. Из них не следует количество видеокамер или задержка нашего сервиса.

<a id="f010"></a>

### F010 — Хронология: что датировано, а что только связано контекстом

- Исходный локатор: [W1-01-MATRIX-2](_WORK/W1_01_RESULT.md), строка37; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation / vendor_statement; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S010](SOURCES.md#s010), [S011](SOURCES.md#s011), [S008](SOURCES.md#s008), [S009](SOURCES.md#s009), [S016](SOURCES.md#s016), [S017](SOURCES.md#s017), [S013](SOURCES.md#s013), [S012](SOURCES.md#s012), [S015](SOURCES.md#s015), [S003](SOURCES.md#s003)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Хронология: что датировано, а что только связано контекстом

1. **2018 — представлен IVA TPU.** Ретроспективная презентация группы за март 2023 помещает это событие в 2018. Это первичное корпоративное сообщение о своей истории, а не независимо проверенная дата появления кремния. Та же презентация явно разделяет IVA UC — ООО «ИВКС» и IVA TPU — «ХайТэк» [[S010](SOURCES.md#s010)].
2. **30.06.2020 — IVA Technologies публично включает IVA TPU в направления своих продуктов.** Официальная новость о конференции Russia–UAE Technology Day; сообщает о представлении микропроцессора, без версии SDK [[S011](SOURCES.md#s011)].
3. **2021 — ранняя документация/разные реализации.** В титуле руководства FW_TPU_H стоит 2021; обозначение `RU.РМДВ.04.06.003-01 97 01`, программный продукт `RU.РМДВ.04.06.003-01` [[S008](SOURCES.md#s008)]. Статья Осипенко и Увкина 2021 описывает IVA H/E как две реализации IP-блока [[S009](SOURCES.md#s009)]. Презентация марта 2023 относит к 2021 завершение разработки и изготовления промышленных образцов IVA TPU 28 нм [[S010](SOURCES.md#s010)]. Это три разных утверждения, не дата современного SDK.
4. **Март 2023 — корпоративная карта направлений ещё использует IVA TPU.** В той же презентации «ХайТэк» и «ИВКС» разные юридические лица; поэтому формулировку СМИ «ХайТэк — бывшая IVA Technologies» нельзя превращать в установленное юридическое переименование [[S010](SOURCES.md#s010)].
5. **Контекст форума «Микроэлектроника-2024» — используется LinQ H.** Собственная публикация производителя говорит о готовности запускать серию, изготовленных процессорах/модулях, плановых 10 000 модулях в год и поставках с середины 2025 [[S016](SOURCES.md#s016)]. Это план 2024, не проверка реально произведённого количества в 2025/2026.
6. **30.03.2025 — авторский материал НИУ ВШЭ/VK продолжает использовать IVA TPU.** Материал Нефёдова называет разработчиком ООО «Хайтек», исследует удалённую среду, STAGING и batch; точную ревизию устройства/SDK не раскрывает [[S017](SOURCES.md#s017)]. Старые имена после появления LinQ продолжают встречаться; линейное «старое исчезло, новое появилось» неверно.
7. **09.06.2025 — GraLinQ AI.** Первичная новость «Гравитона» связывает серверный комплекс с HPD, называет программные инструменты `DNN Quant` и `Graph Optimizer` [[S013](SOURCES.md#s013)]. Эти названия — компоненты компилятора/оптимизации, а не модели процессора.
8. **23.09.2025 — LinQ HPC.** РСК описывает совместный ПАК с двумя HPS [[S012](SOURCES.md#s012)]. Поэтому HPC и HPS — разные уровни сборки.
9. **Новость о включении framework в реестр (календарная дата на открытом теле не найдена; поисковые перепечатки указывают 06.05.2026).** Текущий первичный текст содержит `LinQ H1` и `LinQ H1М` [[S015](SOURCES.md#s015)]. Для строгой хронологии точную дату следует подтвердить в реестре/метаданных; в ветке она не считается установленной первоисточником.
10. **На 23.10.2026 сайт одновременно содержит IVA H1 и LinQ H1/H1М.** Прямая связь имеется, но таблицы соответствия SKU, stepping и SDK нет [[S003](SOURCES.md#s003), [S015](SOURCES.md#s015)].

Дата юридического переименования, дата полного ребрендинга IVA TPU → LinQ, аппаратные изменения IVA H → IVA H1 → H1М и семантика суффикса М **не установлены**. Нельзя выводить их из последовательности газетных названий.


## W1-02 — W1-02. Аппаратные продукты LinQ

<a id="f011"></a>

### F011 — память нескольких TPU не доказана как единая память одной модели.

- Исходный локатор: [W1-02-F01](_WORK/W1_02_RESULT.md), строка36; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation / vendor_statement; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S023](SOURCES.md#s023), [S025](SOURCES.md#s025)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 scope update:** hardware variants/conflicts refined in [F272](RAW_FACTS.md#f272), [F279](RAW_FACTS.md#f279); do not repeat generic HP16/32 contradiction.

**[F011](RAW_FACTS.md#f011) — память нескольких TPU не доказана как единая память одной модели.** Тип inference; статус: вывод из прочитанных [S023](SOURCES.md#s023)/[S025](SOURCES.md#s025), не проверено на устройстве. Руководства физически распределяют DDR4 по микропроцессорам. Следовательно, 32/64 ГБ карты и 640 ГБ HPS не дают основания обещать размещение одной модели такого же размера. Неизвестны модель разделения графа, разрешённые сегменты и ограничения компилятора. Сначала надо получить лимит памяти на один исполняемый граф/контекст и отчёт memory planner.

<a id="f012"></a>

### F012 — int8 подтверждён, аппаратный fp16 не установлен.

- Исходный локатор: [W1-02-F02](_WORK/W1_02_RESULT.md), строка38; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S026](SOURCES.md#s026)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 scope update:** hardware variants/conflicts refined in [F272](RAW_FACTS.md#f272), [F279](RAW_FACTS.md#f279); do not repeat generic HP16/32 contradiction.

**[F012](RAW_FACTS.md#f012) — int8 подтверждён, аппаратный fp16 не установлен.** Тип primary_documentation для int8/перспективы, inference для инженерного ограничения; статус: [S026](SOURCES.md#s026) прочитан. Практический выбор модели должен включать проверку квантования и метрик качества на касках/респираторах. Возможность обучать/экспортировать floating-point модель не доказывает такой же режим исполнения на TPU. Параметры mixed precision, аккумуляторов и поддержка vector operations этой веткой не установлены.

<a id="f013"></a>

### F013 — interface generation имеет несколько уровней.

- Исходный локатор: [W1-02-F03](_WORK/W1_02_RESULT.md), строка40; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation / vendor_statement; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S022](SOURCES.md#s022), [S024](SOURCES.md#s024)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 scope update:** hardware variants/conflicts refined in [F272](RAW_FACTS.md#f272), [F279](RAW_FACTS.md#f279); do not repeat generic HP16/32 contradiction.

**[F013](RAW_FACTS.md#f013) — interface generation имеет несколько уровней.** Тип inference; статус: документы прочитаны. Gen4 вход HPS не делает каждый чип Gen4. Ширина внешнего x16 HPD/HPQ не противоречит x8 отдельного чипа, потому что карта содержит коммутатор. В [S022](SOURCES.md#s022)/[S024](SOURCES.md#s024) проза «8 линий» расходится с таблицей x16; это повод запросить топологию, а не рассчитывать throughput по наиболее выгодному варианту.

<a id="f014"></a>

### F014 — 960 и 1920 TOPS относятся разным системам.

- Исходный локатор: [W1-02-F04](_WORK/W1_02_RESULT.md), строка42; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S026](SOURCES.md#s026), [S028](SOURCES.md#s028)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 scope update:** hardware variants/conflicts refined in [F272](RAW_FACTS.md#f272), [F279](RAW_FACTS.md#f279); do not repeat generic HP16/32 contradiction.

**[F014](RAW_FACTS.md#f014) — 960 и 1920 TOPS относятся разным системам.** Тип vendor_statement + inference; статус: прочитаны [S026](SOURCES.md#s026)/[S028](SOURCES.md#s028). ПАК HPC нельзя выдавать за выделенную командe единицу HPS. При online API скрыта ещё одна граница: shared resource, scheduler и лимит одновременных задач. Физическая машина и выделенная квота — разные величины.

<a id="f015"></a>

### F015 — память CPU-хоста определяется выделенной машиной.

- Исходный локатор: [W1-02-F05](_WORK/W1_02_RESULT.md), строка44; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation / vendor_statement; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S027](SOURCES.md#s027), [S029](SOURCES.md#s029)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 scope update:** hardware variants/conflicts refined in [F272](RAW_FACTS.md#f272), [F279](RAW_FACTS.md#f279); do not repeat generic HP16/32 contradiction.

**[F015](RAW_FACTS.md#f015) — память CPU-хоста определяется выделенной машиной.** Тип inference; статус: [S027](SOURCES.md#s027)/[S029](SOURCES.md#s029) прочитаны. Максимум серверной платформы не говорит, сколько памяти установлено, сколько доступно в контейнере и кто хранит декодированные кадры. Для HX разделение LPDDR4/DDR4 раскрыто прямо; переносить эту схему на HPS без документации нельзя.

<a id="f016"></a>

### F016 — 2,3 мс не равно срок обработки кадра детектором.

- Исходный локатор: [W1-02-F06](_WORK/W1_02_RESULT.md), строка46; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation / vendor_statement; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S026](SOURCES.md#s026)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 scope update:** hardware variants/conflicts refined in [F272](RAW_FACTS.md#f272), [F279](RAW_FACTS.md#f279); do not repeat generic HP16/32 contradiction.

**[F016](RAW_FACTS.md#f016) — 2,3 мс не равно срок обработки кадра детектором.** Тип inference на основании [S026](SOURCES.md#s026); статус: опубликованное заявление просмотрено, собственного benchmark нет. Условия HPS ограничены ResNet-50 batch=1; не указаны входное разрешение, конкретные веса, границы таймера, transfer, preprocessing, quantization и версия compiler. Величина 1,5 мс дана как результат/возможность оптимизации, а не гарантированный режим. Эти числа повторяются у продуктов с разной суммарной мощностью и потому не показывают линейного ускорения одного запроса.

<a id="f017"></a>

### F017 — количество моделей не является количеством камер.

- Исходный локатор: [W1-02-F07](_WORK/W1_02_RESULT.md), строка48; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation / vendor_statement; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S019](SOURCES.md#s019), [S002](SOURCES.md#s002), [S020](SOURCES.md#s020), [S021](SOURCES.md#s021), [S022](SOURCES.md#s022), [S023](SOURCES.md#s023), [S024](SOURCES.md#s024), [S025](SOURCES.md#s025), [S026](SOURCES.md#s026), [S027](SOURCES.md#s027), [S013](SOURCES.md#s013), [S028](SOURCES.md#s028), [S029](SOURCES.md#s029), [S003](SOURCES.md#s003)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 scope update:** hardware variants/conflicts refined in [F272](RAW_FACTS.md#f272), [F279](RAW_FACTS.md#f279); do not repeat generic HP16/32 contradiction.

**[F017](RAW_FACTS.md#f017) — количество моделей не является количеством камер.** Тип inference; статус: не проверено. До 40 моделей HPS и более 16 GraLinQ — заявления о совместном запуске, без FPS/разрешений/загрузки. Одна модель может обслуживать несколько потоков, один поток — несколько моделей. Для сервиса необходимы профиль на собственной сети и предел задержки очереди.

<a id="f018"></a>

### F018 — декодер не следует считать встроенным в каждый LinQ.

- Исходный локатор: [W1-02-F08](_WORK/W1_02_RESULT.md), строка50; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S026](SOURCES.md#s026), [S027](SOURCES.md#s027)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 scope update:** hardware variants/conflicts refined in [F272](RAW_FACTS.md#f272), [F279](RAW_FACTS.md#f279); do not repeat generic HP16/32 contradiction.

**[F018](RAW_FACTS.md#f018) — декодер не следует считать встроенным в каждый LinQ.** Тип primary_documentation ([S026](SOURCES.md#s026)/[S027](SOURCES.md#s027)) и inference; статус: документы прочитаны. HPS описывает аппаратные видео-ASIC как дополнительную опцию. В HX присутствует видеоподсистема RK3588; её 6 TOPS NPU не являются TPU LinQ. Для проверки обязательного исполнения нужно привязать измерения к нужному вычислителю.

<a id="f019"></a>

### F019 — Сопоставление продуктов

- Исходный локатор: [W1-02-MATRIX-3](_WORK/W1_02_RESULT.md), строка13; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation + vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S002](SOURCES.md#s002), [S020](SOURCES.md#s020), [S021](SOURCES.md#s021), [S022](SOURCES.md#s022), [S023](SOURCES.md#s023), [S024](SOURCES.md#s024), [S025](SOURCES.md#s025), [S026](SOURCES.md#s026), [S027](SOURCES.md#s027), [S013](SOURCES.md#s013), [S028](SOURCES.md#s028), [S029](SOURCES.md#s029)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 scope update:** hardware variants/conflicts refined in [F272](RAW_FACTS.md#f272), [F279](RAW_FACTS.md#f279); do not repeat generic HP16/32 contradiction.

### Сопоставление продуктов

Числа в этой таблице — заявленные спецификации, не результаты наших тестов. Для каждой строки статус проверки: просмотрен первичный документ; исполнение на устройстве не проверялось.

| Объект | Память устройства и CPU-хоста | Интерфейс | Пик и формат | Частоты / питание | Источник и тип основания |
|---|---|---|---|---|---|
| Чип LinQ H | Встроенная память 16 МБ; контроллер внешней DDR4 ECC, 2×72 бит, до 32 «Гб». Память хоста не задана | PCIe Gen3 x8 Endpoint | 24 TOPS int8 | 500–812 МГц; литерал энергопотребления «<25-30ВТ» | [S002](SOURCES.md#s002), vendor_statement |
| HP, общий datasheet | 16 ГБ DDR4 ECC; host RAM не задана | x8 PCIe Gen3 | 24 TOPS int8 | 500–812 МГц; 25/35 Вт тип./пик | [S020](SOURCES.md#s020) стр.2, primary_documentation |
| HP1M-02, руководство | 32 ГБ DDR4 ECC, два канала по 16 ГБ; host RAM отдельно | PCIe **2.0** x8 Endpoint | 24 TOPS int8 | ≥750 МГц, ≤35 Вт | [S021](SOURCES.md#s021) стр.5–6, primary_documentation; противоречит [S020](SOURCES.md#s020) |
| HPD, passive datasheet | 32 ГБ DDR4 ECC | x16 PCIe Gen3 | 48 TOPS int8 | 500–812 МГц; 60/70 Вт | [S022](SOURCES.md#s022) стр.2, primary_documentation |
| HPD1M-01, руководство | 32 ГБ суммарно; **16 ГБ на каждую из 2 H1M** | PCIe 3.0 x16 Endpoint, коммутатор | 48 TOPS int8 | ≥750 МГц, ≤100 Вт | [S023](SOURCES.md#s023) стр.5–8, primary_documentation |
| HPQ, passive datasheet | 64 ГБ DDR4 ECC | x16 PCIe Gen3 | 96 TOPS int8 | 500–812 МГц; 120/140 Вт | [S024](SOURCES.md#s024) стр.2, primary_documentation |
| HPQ по /docs, исполнение HPD1M-10 в руководстве | 64 ГБ суммарно; **16 ГБ на каждую из 4 К1945ВМ3Я** | PCIe 3.0 x16 Endpoint, коммутатор | 96 TOPS int8 | ≥750 МГц, ≤150 Вт | [S025](SOURCES.md#s025) стр.5–8, primary_documentation |
| HPS, собственный datasheet | 640 ГБ DDR4 ECC; структура единого адресного пространства не раскрыта; host RAM не указана | 2×PCIe x16 Gen4, 3U | до 960 TOPS int8; fp16/bfloat16 только перспектива | до 1 ГГц; 300/600/900/1500 Вт в зависимости режима | [S026](SOURCES.md#s026) стр.1–2, primary_documentation |
| HX, SBC | CPU/RK3588: LPDDR4 до 16 ГБ, eMMC 32 ГБ; TPU: DDR4 до 16 ГБ | RJ45, USB, CSI и др.; это самостоятельная SBC | LinQ TPU 24 TOPS; отдельно NPU RK3588 6 TOPS | TPU 750 МГц; модуль <40 Вт | [S027](SOURCES.md#s027) стр.3–4, primary_documentation |
| GraLinQ AI | Host: сервер с платой «Онега», точная RAM в новости не задана | Карты LinQ HPD | 384 TOPS на комплекс; >16 сетей заявлено | Полная конфигурация и питание не раскрыты | [S013](SOURCES.md#s013), vendor_statement |
| LinQ HPC | Два HPS, 1280 ГБ DDR4 ECC в ПАК; не следует считать это RAM CPU | RSC ScaleStream-C + сервер С2122ИУ | 1920 TOPS int8 | заявлен TDP 3000 Вт | [S028](SOURCES.md#s028), vendor_statement |
| CPU-сервер С2122ИУ сам по себе | До 8 ТБ DDR5 в 32 DIMM — предел платформы, не установленная RAM хакатона | Серверная платформа 2U | CPU до 2 Intel Xeon Scalable 4/5 поколения; LinQ TOPS не свойство голого сервера | Мощность конкретной конфигурации не установлена | [S029](SOURCES.md#s029), vendor_statement |

«Гб» в описаниях контроллера оставлено буквально: это неоднозначная единица; в таблицах комплектации прямо написано «ГБ» или GB. Нельзя автоматически превращать предел контроллера в установленный объём памяти карты.


## W1-03 — W1-03 — публичный доступ к SDK, документации и среде LinQ

<a id="f020"></a>

### F020 — На главной есть предложение заказать демонстрацию и тестовую среду; demo-ссылка ведёт к `/footer#popup:linq`, а также встречается `/#popup:linq`.

- Исходный локатор: [W1-03-F01](_WORK/W1_03_RESULT.md), строка19; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement + local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S001](SOURCES.md#s001), [S034](SOURCES.md#s034)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F020](RAW_FACTS.md#f020) | На главной есть предложение заказать демонстрацию и тестовую среду; demo-ссылка ведёт к `/footer#popup:linq`, а также встречается `/#popup:linq`. | vendor_statement + local_observation ссылки | Просмотрены главная и список ссылок TinyFish | [S001](SOURCES.md#s001), [S034](SOURCES.md#s034); форма не отправлялась, выдача доступа не проверена |

<a id="f021"></a>

### F021 — `/sol#linq_soft` описывает Python API и CLI для квантования/компиляции. Там написано Python 3.8. Стоимость ПО включена в OEM-поставку аппаратуры; приведены контакты для запроса усл

- Исходный локатор: [W1-03-F02](_WORK/W1_03_RESULT.md), строка20; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F021](RAW_FACTS.md#f021) | `/sol#linq_soft` описывает Python API и CLI для квантования/компиляции. Там написано Python 3.8. Стоимость ПО включена в OEM-поставку аппаратуры; приведены контакты для запроса условий. | vendor_statement | Прочитана страница | [S003](SOURCES.md#s003), раздел ПО; ни цена, ни условия отдельной лицензии не установлены |

<a id="f022"></a>

### F022 — В разделе скачивания явно требуется регистрация в ЛК **и верификация**. Эти два этапа нельзя считать одним автоматическим действием.

- Исходный локатор: [W1-03-F03](_WORK/W1_03_RESULT.md), строка21; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F022](RAW_FACTS.md#f022) | В разделе скачивания явно требуется регистрация в ЛК **и верификация**. Эти два этапа нельзя считать одним автоматическим действием. | primary_documentation сайта | Прочитано требование | [S003](SOURCES.md#s003), блок «Скачать»; процедура и срок верификации не раскрыты |

<a id="f023"></a>

### F023 — Кнопки ведут на `/members/login` и `/members/signup/group/zu1sdzcxrlvhqmf-fw2`.

- Исходный локатор: [W1-03-F04](_WORK/W1_03_RESULT.md), строка22; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S031](SOURCES.md#s031), [S032](SOURCES.md#s032)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F023](RAW_FACTS.md#f023) | Кнопки ведут на `/members/login` и `/members/signup/group/zu1sdzcxrlvhqmf-fw2`. | local_observation | Переходы открыты | [S031](SOURCES.md#s031), [S032](SOURCES.md#s032) |

<a id="f024"></a>

### F024 — Регистрация запрашивает компанию, ФИО, email и телефон; в данных формы обязательны компания/email/телефон и согласие на обработку ПД. Публикуется ссылка на политику, а не лицензия 

- Исходный локатор: [W1-03-F05](_WORK/W1_03_RESULT.md), строка23; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S032](SOURCES.md#s032)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F024](RAW_FACTS.md#f024) | Регистрация запрашивает компанию, ФИО, email и телефон; в данных формы обязательны компания/email/телефон и согласие на обработку ПД. Публикуется ссылка на политику, а не лицензия SDK. | local_observation | Прочитано описание формы, без отправки | [S032](SOURCES.md#s032); поле ФИО присутствует, но в извлечённом JSON без `li_req:y` |

<a id="f025"></a>

### F025 — Страница входа показывает email, пароль, вход, регистрацию и восстановление пароля.

- Исходный локатор: [W1-03-F06](_WORK/W1_03_RESULT.md), строка24; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S031](SOURCES.md#s031)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F025](RAW_FACTS.md#f025) | Страница входа показывает email, пароль, вход, регистрацию и восстановление пароля. | local_observation | TinyFish HTML extraction | [S031](SOURCES.md#s031); web.open вернул пустой текст; вход не выполнялся |

<a id="f026"></a>

### F026 — `/docs` публично перечисляет datasheets, руководства эксплуатации модулей и framework guide.

- Исходный локатор: [W1-03-F07](_WORK/W1_03_RESULT.md), строка25; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S019](SOURCES.md#s019)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F026](RAW_FACTS.md#f026) | `/docs` публично перечисляет datasheets, руководства эксплуатации модулей и framework guide. | local_observation | Открыт индекс, проверена ссылка на framework | [S019](SOURCES.md#s019); не все hardware PDF прочитаны в этой ветке |

<a id="f027"></a>

### F027 — Framework guide: 2025; обозначение RU.РМДВ.04.06.014-03 34 01; версия программы `-03` описана как развитие `-02`. Условия: Ubuntu 20.04, Intel i7-7700, RAM ≥32 ГБ, Python 3.11. Пос

- Исходный локатор: [W1-03-F08](_WORK/W1_03_RESULT.md), строка26; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F027](RAW_FACTS.md#f027) | Framework guide: 2025; обозначение RU.РМДВ.04.06.014-03 34 01; версия программы `-03` описана как развитие `-02`. Условия: Ubuntu 20.04, Intel i7-7700, RAM ≥32 ГБ, Python 3.11. Поставка: `tpu_framework-py3-none-any.whl`, имя может включать версию. Установка локального wheel через pip; проверка — `import tpu_framework` и код возврата 0. Пример классификации ResNet-50 использует ONNX, Pillow, `pytpu`, TensorFlow, `onnx_direct`; ссылки на wheel и веса отсутствуют. | primary_documentation | PDF прочитан, текст извлечён; ничего не установлено | [S030](SOURCES.md#s030), титул, §1.2.1, §2, §3.4; это не полный dependency lockfile |

<a id="f028"></a>

### F028 — Официальная презентация **2026** называет в условиях опубликованного измерения **TPU Runtime 16.18.6**, **TPU Framework 2026.8.43**, Ubuntu 24.04, Intel i7-10700K.

- Исходный локатор: [W1-03-F09](_WORK/W1_03_RESULT.md), строка27; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F028](RAW_FACTS.md#f028) | Официальная презентация **2026** называет в условиях опубликованного измерения **TPU Runtime 16.18.6**, **TPU Framework 2026.8.43**, Ubuntu 24.04, Intel i7-10700K. | reported_measurement, только сведения о среде | Прочитана подпись к таблице | [S033](SOURCES.md#s033), PDF p4 / слайд 4; собственных измерений нет, выдача этих версий команде не подтверждена |

<a id="f029"></a>

### F029 — Та же презентация заявляет облачный сервис `Cloud TPU` в описании ПАК LinQ HPC.

- Исходный локатор: [W1-03-F10](_WORK/W1_03_RESULT.md), строка28; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F029](RAW_FACTS.md#f029) | Та же презентация заявляет облачный сервис `Cloud TPU` в описании ПАК LinQ HPC. | vendor_statement | Прочитан слайд | [S033](SOURCES.md#s033), PDF p9; endpoint/протокол/доступ не опубликованы в прочитанном фрагменте |

<a id="f030"></a>

### F030 — Datasheet HPS заявляет User Guide, Installation Guide, Developer SDK, Hardware Software Reference, портал разработчика, Model Zoo и образцы кода. Конкретного адреса портала или реп

- Исходный локатор: [W1-03-F11](_WORK/W1_03_RESULT.md), строка29; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S026](SOURCES.md#s026)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F030](RAW_FACTS.md#f030) | Datasheet HPS заявляет User Guide, Installation Guide, Developer SDK, Hardware Software Reference, портал разработчика, Model Zoo и образцы кода. Конкретного адреса портала или репозитория в этом блоке нет. Поддержка 24/7 относится к SLA корпоративных клиентов. | vendor_statement | Прочитан PDF | [S026](SOURCES.md#s026), PDF p4, «Заказ и поддержка»; нельзя переносить SLA на участников хакатона |

<a id="f031"></a>

### F031 — В текущем извлечении `/hr` описаны Python-прототип и C++ пре-альфа облачного inference-сервиса; gRPC/REST/protobuf упоминаются среди желательных компетенций.

- Исходный локатор: [W1-03-F12](_WORK/W1_03_RESULT.md), строка30; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S014](SOURCES.md#s014)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F031](RAW_FACTS.md#f031) | В текущем извлечении `/hr` описаны Python-прототип и C++ пре-альфа облачного inference-сервиса; gRPC/REST/protobuf упоминаются среди желательных компетенций. | vendor_statement | TinyFish прочитал страницу; search согласуется | [S014](SOURCES.md#s014); вакансия не является спецификацией действующего API |

<a id="f032"></a>

### F032 — web.open той же `/hr` возвратил другой вариант: вакансию разработки `dnn-model-zoo`, с препроцессингом/постпроцессингом.

- Исходный локатор: [W1-03-F13](_WORK/W1_03_RESULT.md), строка31; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S014](SOURCES.md#s014)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F032](RAW_FACTS.md#f032) | web.open той же `/hr` возвратил другой вариант: вакансию разработки `dnn-model-zoo`, с препроцессингом/постпроцессингом. | local_observation | Сопоставлены ответы двух каналов | [S014](SOURCES.md#s014); обнаружено расхождение выдачи/кеша, точная дата смены неизвестна |

<a id="f033"></a>

### F033 — На официальном сайте 2026 кейс LinQ требует выполнения inference на ускорителях LinQ и обещает участникам онлайн-доступ.

- Исходный локатор: [W1-03-F14](_WORK/W1_03_RESULT.md), строка32; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S035](SOURCES.md#s035)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F033](RAW_FACTS.md#f033) | На официальном сайте 2026 кейс LinQ требует выполнения inference на ускорителях LinQ и обещает участникам онлайн-доступ. | primary_documentation условий кейса | Прочитан публичный кейс | [S035](SOURCES.md#s035), раздел «Кейсы», LinQ; формат remote access не определён |

<a id="f034"></a>

### F034 — Расписание: 23.10 13:00 публикация полных заданий в ЛК, 16:30 открытие, 18:00 checkpoint; 24.10 11:00/18:00 checkpoints, 19:00–19:45 pitch; 25.10 10:00 сдача, 12:00–17:30 защиты.

- Исходный локатор: [W1-03-F15](_WORK/W1_03_RESULT.md), строка33; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S035](SOURCES.md#s035)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F034](RAW_FACTS.md#f034) | Расписание: 23.10 13:00 публикация полных заданий в ЛК, 16:30 открытие, 18:00 checkpoint; 24.10 11:00/18:00 checkpoints, 19:00–19:45 pitch; 25.10 10:00 сдача, 12:00–17:30 защиты. | primary_documentation мероприятия | Прочитан раздел расписания | [S035](SOURCES.md#s035); 45 часов между публикацией и сдачей — арифметический вывод |

<a id="f035"></a>

### F035 — Ссылка регистрации хакатона ведёт на `https://lk2026.otkroimosprom.ru/lk/event/115`.

- Исходный локатор: [W1-03-F16](_WORK/W1_03_RESULT.md), строка34; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S036](SOURCES.md#s036)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F035](RAW_FACTS.md#f035) | Ссылка регистрации хакатона ведёт на `https://lk2026.otkroimosprom.ru/lk/event/115`. | local_observation | Открыт URL, web не извлёк содержимое | [S036](SOURCES.md#s036); доступ к полному кейсу не получен |

<a id="f036"></a>

### F036 — На странице 2026 есть отдельная ретроспектива «Как это было в 2025»; сама по себе она не меняет год текущего расписания.

- Исходный локатор: [W1-03-F17](_WORK/W1_03_RESULT.md), строка35; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S035](SOURCES.md#s035)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание | Тип основания | Фактическая проверка | Источник / локатор / ограничение |
|---|---|---|---|---|
| [F036](RAW_FACTS.md#f036) | На странице 2026 есть отдельная ретроспектива «Как это было в 2025»; сама по себе она не меняет год текущего расписания. | local_observation | Прочитана структура страницы | [S035](SOURCES.md#s035); конкретная ранее просмотренная пользователем памятка 2025 не идентифицирована |


## W1-04 — W1-04 — Окружение и установка LinQ

<a id="f037"></a>

### F037 — Руководство 2025 обозначает программу `RU.РМДВ.04.06.014-03`, расширяющую `-02`.

- Исходный локатор: [W1-04-F01](_WORK/W1_04_RESULT.md), строка19; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F037](RAW_FACTS.md#f037) | Руководство 2025 обозначает программу `RU.РМДВ.04.06.014-03`, расширяющую `-02`. | primary_documentation | [S030](SOURCES.md#s030), §1.1–1.2, с.4 | Прочитан независимо через TinyFish. Номер документа не равен semver wheel. |

<a id="f038"></a>

### F038 — Требования framework: Linux Ubuntu 20.04; Intel Core i7-7700 @3.60 GHz; RAM не менее 32 ГБ; Python 3.11.

- Исходный локатор: [W1-04-F02](_WORK/W1_04_RESULT.md), строка20; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F038](RAW_FACTS.md#f038) | Требования framework: Linux Ubuntu 20.04; Intel Core i7-7700 @3.60 GHz; RAM не менее 32 ГБ; Python 3.11. | primary_documentation | [S030](SOURCES.md#s030), §2.1.1, с.5 | Это требования конкретного guide; RAM хоста не память ускорителя. Приведён CPU, но не исчерпывающая ISA/ABI-матрица. |

<a id="f039"></a>

### F039 — Комплект framework описан как wheel `tpu_framework-py3-none-any.whl`; допускается цифровой спецификатор версии.

- Исходный локатор: [W1-04-F03](_WORK/W1_04_RESULT.md), строка21; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F039](RAW_FACTS.md#f039) | Комплект framework описан как wheel `tpu_framework-py3-none-any.whl`; допускается цифровой спецификатор версии. | primary_documentation | [S030](SOURCES.md#s030), §2.1.2, с.5 | Сам wheel не получен, METADATA/WHEEL не просмотрены. Имя из руководства нельзя считать точным именем получаемого файла: версия в примере отсутствует. |

<a id="f040"></a>

### F040 — Установка через Linux terminal, venv и pip; проверка — импорт `tpu_framework` с exit code 0.

- Исходный локатор: [W1-04-F04](_WORK/W1_04_RESULT.md), строка22; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F040](RAW_FACTS.md#f040) | Установка через Linux terminal, venv и pip; проверка — импорт `tpu_framework` с exit code 0. | primary_documentation | [S030](SOURCES.md#s030), §2.2, с.5–6 | Команды прочитаны, не выполнялись. Успешный import сам по себе не доказывает доступ к устройству. |

<a id="f041"></a>

### F041 — `/sol` описывает Python API 3.8 и CLI, а также ограничение скачивания после регистрации и верификации.

- Исходный локатор: [W1-04-F05](_WORK/W1_04_RESULT.md), строка23; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F041](RAW_FACTS.md#f041) | `/sol` описывает Python API 3.8 и CLI, а также ограничение скачивания после регистрации и верификации. | vendor_statement | [S003](SOURCES.md#s003), раздел ПО | Прочитано web. Это не установленное ограничение Python для версии 2026.8.43. Не регистрировались и не видели закрытые файлы. |

<a id="f042"></a>

### F042 — Тот же guide, требующий Python3.11, содержит пример журнала с `/venv/lib/python3.8/site-packages/dnn_quant/...` и TensorFlow warning.

- Исходный локатор: [W1-04-F06](_WORK/W1_04_RESULT.md), строка24; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F042](RAW_FACTS.md#f042) | Тот же guide, требующий Python3.11, содержит пример журнала с `/venv/lib/python3.8/site-packages/dnn_quant/...` и TensorFlow warning. | primary_documentation | [S030](SOURCES.md#s030), §4, с.23 | Реальное внутреннее разновременное содержимое документа. Не доказывает, что Python3.11 ошибочен или что 3.8 поддерживается текущим SDK. |

<a id="f043"></a>

### F043 — В презентации 2026 условия benchmark: Intel Core i7-10700K @3.80 GHz, Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43.

- Исходный локатор: [W1-04-F07](_WORK/W1_04_RESULT.md), строка25; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F043](RAW_FACTS.md#f043) | В презентации 2026 условия benchmark: Intel Core i7-10700K @3.80 GHz, Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43. | reported_measurement | [S033](SOURCES.md#s033), слайд4, примечание | Условия прочитаны через TinyFish. Это авторский benchmark, не наш тест и не спецификация выданного SDK. Версия Python отсутствует. |

<a id="f044"></a>

### F044 — В примере guide исходный ONNX проходит `onnx_direct.onnx_to_tf`; используются TensorFlow, NumPy/PIL и компоненты `tpu_framework`.

- Исходный локатор: [W1-04-F08](_WORK/W1_04_RESULT.md), строка26; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F044](RAW_FACTS.md#f044) | В примере guide исходный ONNX проходит `onnx_direct.onnx_to_tf`; используются TensorFlow, NumPy/PIL и компоненты `tpu_framework`. | primary_documentation | [S030](SOURCES.md#s030), §3.3, с.11–20 | Имена модулей — зацепки для зависимостей, не проверенный requirements. Точных версий TF/ONNX/NumPy и нативных библиотек нет. |

<a id="f045"></a>

### F045 — Пример сначала компилирует и тестирует TLM, затем сохраняет `.tpu`; только после этого перечисляет и открывает реальные TPU.

- Исходный локатор: [W1-04-F09](_WORK/W1_04_RESULT.md), строка27; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F045](RAW_FACTS.md#f045) | Пример сначала компилирует и тестирует TLM, затем сохраняет `.tpu`; только после этого перечисляет и открывает реальные TPU. | primary_documentation | [S030](SOURCES.md#s030), с.17–21 | Документированная граница framework → `.tpu` → SDK. Не гарантирует независимость всех import-time зависимостей от runtime/платы. |

<a id="f046"></a>

### F046 — Для HP1M-02 после монтажа предусмотрено `lspci

- Исходный локатор: [W1-04-F10](_WORK/W1_04_RESULT.md), строка28; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S021](SOURCES.md#s021)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F046](RAW_FACTS.md#f046) | Для HP1M-02 после монтажа предусмотрено `lspci | grep MIPS`, ожидается одна запись `MIPS: Device 2805:0006 (rev 08)`, затем установка драйвера LINQ H1. | primary_documentation | [S021](SOURCES.md#s021), §2.4, с.14 | Прочитано через TinyFish. Никаких kernel module names, dkms-команд или версий драйвера не дано. |

<a id="f047"></a>

### F047 — Для четырёхпроцессорного HPQ/HPD1M-11 ожидается четыре такие записи, затем отдельные компоненты драйвера.

- Исходный локатор: [W1-04-F11](_WORK/W1_04_RESULT.md), строка29; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S039](SOURCES.md#s039)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F047](RAW_FACTS.md#f047) | Для четырёхпроцессорного HPQ/HPD1M-11 ожидается четыре такие записи, затем отдельные компоненты драйвера. | primary_documentation | [S039](SOURCES.md#s039), §2.4, с.14–15 | Количество PCIe-функций привязано к данному модулю, не универсальный health-check всех LinQ. |

<a id="f048"></a>

### F048 — В HPS datasheet заявлена интеграция с x86, ARM, Mips64, E2K.

- Исходный локатор: [W1-04-F12](_WORK/W1_04_RESULT.md), строка30; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S026](SOURCES.md#s026)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F048](RAW_FACTS.md#f048) | В HPS datasheet заявлена интеграция с x86, ARM, Mips64, E2K. | vendor_statement | [S026](SOURCES.md#s026), с.2 | Прочитан PDF web. Это заявление о гетерогенных системах, не доказательство доступности всех compiler/runtime wheels для каждой архитектуры. |

<a id="f049"></a>

### F049 — `/docs` публично ссылается на hardware manuals и Framework manual.

- Исходный локатор: [W1-04-F13](_WORK/W1_04_RESULT.md), строка31; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S019](SOURCES.md#s019)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F049](RAW_FACTS.md#f049) | `/docs` публично ссылается на hardware manuals и Framework manual. | local_observation | [S019](SOURCES.md#s019) | Независимое извлечение TinyFish с outbound links. Закрытая выдача ПО не делает guides закрытыми. |

<a id="f050"></a>

### F050 — В вакансии производителя облачный AI-inference назван Python-прототипом и C++ пре-альфа; Docker/Kubernetes указаны как направления проработки.

- Исходный локатор: [W1-04-F14](_WORK/W1_04_RESULT.md), строка32; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S014](SOURCES.md#s014)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F050](RAW_FACTS.md#f050) | В вакансии производителя облачный AI-inference назван Python-прототипом и C++ пре-альфа; Docker/Kubernetes указаны как направления проработки. | vendor_statement | [S014](SOURCES.md#s014), вакансия C++, блоки обязанностей | Прочитана страница. Дата вакансии не установлена; это не актуальный контракт облака и не доказательство отсутствия рабочего сервиса. |

<a id="f051"></a>

### F051 — По PyPA wheel tag состоит из Python/ABI/platform; `py3`, `none`, `any` описывают совместимость самого дистрибутива.

- Исходный локатор: [W1-04-F15](_WORK/W1_04_RESULT.md), строка33; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S040](SOURCES.md#s040)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Наблюдение, точные условия | Тип | Источник и локатор | Проверка / ограничения |
|---|---|---|---|---|
| [F051](RAW_FACTS.md#f051) | По PyPA wheel tag состоит из Python/ABI/platform; `py3`, `none`, `any` описывают совместимость самого дистрибутива. | primary_documentation | [S040](SOURCES.md#s040), Overview/Python Tag/ABI Tag | Прочитана спецификация. Тег не заменяет анализ зависимостей, `Requires-Python`, system libraries и ограничений поставщика. |

<a id="f052"></a>

### F052 — Отделение машин и компонентов

- Исходный локатор: [W1-04-MATRIX-4](_WORK/W1_04_RESULT.md), строка45; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation / vendor_statement; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S021](SOURCES.md#s021), [S039](SOURCES.md#s039), [S026](SOURCES.md#s026), [S019](SOURCES.md#s019), [S014](SOURCES.md#s014), [S040](SOURCES.md#s040), [S004](SOURCES.md#s004), [S005](SOURCES.md#s005)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Отделение машин и компонентов

| Контур | Что обосновано | Что остаётся неизвестным |
|---|---|---|
| Обычный Windows ПК/ноутбук | Подготовка данных и моделей; клиент разрешённого удалённого доступа — допустимый инженерный маршрут. | Есть ли Windows wheel/native runtime; нужен ли VPN, SSH, browser, REST/gRPC; поддержан ли WSL. |
| Linux CPU-хост подготовки | Официальный guide описывает Ubuntu, venv, framework; GPU не перечислен в требованиях. `.tpu` отделяет подготовку от исполнения. | Нужны ли runtime bindings/TLM package без платы; точные зависимости; доступность лицензии; совместимость модели. |
| Linux-хост с физической платой | PCIe enumeration, отдельный драйвер, SDK device API. | Поддержанные kernel/glibc, driver/runtime/firmware pairing, права на device nodes, udev, DKMS, reboot, контейнерный passthrough. |
| Выданное облачное окружение | Публично заявлен Cloud TPU и существует описание прототипа. | Что именно выдают участникам, кто компилирует, кто ставит драйвер, как доставляется `.tpu`, квоты, хранение, доступ к логам. |
| RTX4070 / облачная NVIDIA GPU | Может использоваться для обучения/экспорта в независимом ML-контуре (инженерный маршрут). | CUDA/cuDNN не установлены как требования LinQ framework; RTX не заменяет проверку LinQ inference. |

**Можно ли компилировать без платы?** Основание положительного ожидания: требования framework не перечисляют плату; compiler получает целевые hardware parameters; в примере compilation/TLM и сохранение файла предшествуют device API. Тип вывода — inference, а не выполненная компиляция. Надёжный ответ для выданного релиза даст изолированный CPU-only smoke-test с поставленным комплектом. Не путать «без платы» с «без SDK» и «бесплатно»: компоненты, лицензия и права всё равно нужны.

**Драйверы и runtime.** Hardware guide прямо требует отдельный драйвер; framework guide не даёт его install-команды. `pip install tpu_framework...` не следует объявлять установкой драйвера. Не найдены допустимые команды `modprobe`, имена `.ko`/deb/rpm и device paths; не подставлять типичные имена NPU. Для выданного API-сервиса установка драйвера на Windows-клиенте может вообще не требоваться; это зависит от контракта доступа.

**Docker.** Публичного проверенного Dockerfile или container digest этой платформы в данной ветке не найдено. Вакансия — полезная зацепка, но не runnable artifact. Не собирать «официальный образ» из предположительных apt/pip зависимостей. Запросить готовый image digest/registry и правила доступа к TPU либо точный wheelhouse/lock с host driver requirements. Контейнер compiler и контейнер runtime могут иметь разные требования; сейчас это проектная возможность, не документированный продукт.


## W1-05 — W1-05 — импорт модели и контракт model_stack

<a id="f053"></a>

### F053 — , primary_documentation, S01 p4: программа -03 названа доработанной и расширенной относительно -02. Следовательно, API из старого FW_TPU_H или -02 нельзя автоматически считать API 

- Исходный локатор: [W1-05-F01](_WORK/W1_05_RESULT.md), строка37; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F053](RAW_FACTS.md#f053), primary_documentation, [S030](SOURCES.md#s030) p4: программа -03 названа доработанной и расширенной относительно -02. Следовательно, API из старого FW_TPU_H или -02 нельзя автоматически считать API -03 либо Framework 2026.8.43.

<a id="f054"></a>

### F054 — , primary_documentation, S01 p7,14,25: вход — замороженный граф с обученными весами, форматы protobuf или ONNX. Для TensorFlow пример читает бинарный файл через GFile и ParseFromSt

- Исходный локатор: [W1-05-F02](_WORK/W1_05_RESULT.md), строка38; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F054](RAW_FACTS.md#f054), primary_documentation, [S030](SOURCES.md#s030) p7,14,25: вход — замороженный граф с обученными весами, форматы protobuf или ONNX. Для TensorFlow пример читает бинарный файл через GFile и ParseFromString в `tf.compat.v1.GraphDef`. Для ONNX — `onnx.load(GRAPH_PATH)`. Формальная документация квантователя принимает GraphDef. Не подтверждены `.pt`, TorchScript, state_dict, Keras H5, SavedModel directory как непосредственные входы этого API. Отсутствие доказательства не является доказательством невозможности другого актуального API.

<a id="f055"></a>

### F055 — , primary_documentation, S01 p11: конвертер из модуля `onnx_direct` принимает `onnx.ModelProto`; описаны TensorFlow-граф и служебный словарь переименования слоёв. Это собственный д

- Исходный локатор: [W1-05-F03](_WORK/W1_05_RESULT.md), строка39; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F055](RAW_FACTS.md#f055), primary_documentation, [S030](SOURCES.md#s030) p11: конвертер из модуля `onnx_direct` принимает `onnx.ModelProto`; описаны TensorFlow-граф и служебный словарь переименования слоёв. Это собственный документированный компонент; не надо подменять его сторонним onnx-tf/onnx2tf, совпадение назначения не означает эквивалентность.

<a id="f056"></a>

### F056 — , vendor_statement, S02 блоки ускорителей: PyTorch интегрируется через ONNX. В блоке HX указаны нижние границы PyTorch 2.0.0 и ONNX 1.15.0. Эти условия не являются opset=15 и не по

- Исходный локатор: [W1-05-F04](_WORK/W1_05_RESULT.md), строка40; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F056](RAW_FACTS.md#f056), vendor_statement, [S003](SOURCES.md#s003) блоки ускорителей: PyTorch интегрируется через ONNX. В блоке HX указаны нижние границы PyTorch 2.0.0 и ONNX 1.15.0. Эти условия не являются opset=15 и не показывают верхнюю совместимую версию. Для HP/HPQ такого числового диапазона на странице нет.

<a id="f057"></a>

### F057 — , vendor_statement, S06: HPS заявляет интеграцию TensorFlow 2.x и PyTorch через ONNX. Это совместимо с использованием `tf.compat.v1.GraphDef` внутри TensorFlow 2, но не доказывает 

- Исходный локатор: [W1-05-F05](_WORK/W1_05_RESULT.md), строка41; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S026](SOURCES.md#s026)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F057](RAW_FACTS.md#f057), vendor_statement, [S026](SOURCES.md#s026): HPS заявляет интеграцию TensorFlow 2.x и PyTorch через ONNX. Это совместимо с использованием `tf.compat.v1.GraphDef` внутри TensorFlow 2, но не доказывает прямой импорт любого SavedModel/Keras артефакта.

<a id="f058"></a>

### F058 — , reported_measurement, S05 p4: benchmark автора использует Ubuntu 24.04, Intel Core i7-10700K @3.80 GHz, TPU Runtime 16.18.6, TPU Framework 2026.8.43. В этой версии заявлены резул

- Исходный локатор: [W1-05-F06](_WORK/W1_05_RESULT.md), строка42; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F058](RAW_FACTS.md#f058), reported_measurement, [S033](SOURCES.md#s033) p4: benchmark автора использует Ubuntu 24.04, Intel Core i7-10700K @3.80 GHz, TPU Runtime 16.18.6, TPU Framework 2026.8.43. В этой версии заявлены результаты yolo5s batch1 и yolov8n_pose batch1. Размер входа, exporter, opset, веса и границы постобработки не раскрыты. Никакой локальный benchmark не проводился.

<a id="f059"></a>

### F059 — , primary_documentation, S07: стандарт отдельно версионирует IR, операторы и саму модель; release-пакета имеет ещё собственную схему версии. Inference: пакет ONNX≥1.15.0 из S02 не 

- Исходный локатор: [W1-05-F07](_WORK/W1_05_RESULT.md), строка43; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S041](SOURCES.md#s041), [S003](SOURCES.md#s003)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F059](RAW_FACTS.md#f059), primary_documentation, [S041](SOURCES.md#s041): стандарт отдельно версионирует IR, операторы и саму модель; release-пакета имеет ещё собственную схему версии. Inference: пакет ONNX≥1.15.0 из [S003](SOURCES.md#s003) не устанавливает допустимый opset/IR конкретного parser LinQ.

<a id="f060"></a>

### F060 — , unknown: поддерживаемые ONNX opsets/domains, maximum IR, custom ops, external tensor data, control flow и ограничения на initializers для поставки хакатона не установлены. Также 

- Исходный локатор: [W1-05-F08](_WORK/W1_05_RESULT.md), строка44; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030), [S003](SOURCES.md#s003), [S002](SOURCES.md#s002), [S019](SOURCES.md#s019), [S033](SOURCES.md#s033), [S026](SOURCES.md#s026), [S041](SOURCES.md#s041), [S042](SOURCES.md#s042), [S043](SOURCES.md#s043)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F060](RAW_FACTS.md#f060), unknown: поддерживаемые ONNX opsets/domains, maximum IR, custom ops, external tensor data, control flow и ограничения на initializers для поставки хакатона не установлены. Также не обнаружены публичные source code/commit для используемых `onnx_direct`, `tpu_framework`, `dnn_quant`.

<a id="f061"></a>

### F061 — , primary_documentation, S01 p7–9: `QuantizedModel.quantize` принимает исходный TF GraphDef, описание входных форм, выходных узлов и словарь калибровочных ndarray. Возвращаемый тип

- Исходный локатор: [W1-05-F09](_WORK/W1_05_RESULT.md), строка48; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F061](RAW_FACTS.md#f061), primary_documentation, [S030](SOURCES.md#s030) p7–9: `QuantizedModel.quantize` принимает исходный TF GraphDef, описание входных форм, выходных узлов и словарь калибровочных ndarray. Возвращаемый тип `_InMemoryQuantizedModel`. `save(file_path)` сохраняет модель; терминологический раздел именует архив `.qm`. `as_graph` отдаёт GraphDef для проверки; этот GraphDef не тождественен программе TPU.

<a id="f062"></a>

### F062 — , primary_documentation, S01 p8: аннотация `input_shapes` содержит Mapping имён в Tuple с `Optional[int]`, а `output_nodes` может быть списком имён, списком словарей или None. Не д

- Исходный локатор: [W1-05-F10](_WORK/W1_05_RESULT.md), строка49; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F062](RAW_FACTS.md#f062), primary_documentation, [S030](SOURCES.md#s030) p8: аннотация `input_shapes` содержит Mapping имён в Tuple с `Optional[int]`, а `output_nodes` может быть списком имён, списком словарей или None. Не даны полная схема словарей, правила inference shape, разрешённые None и ограничения рангов. Это недостаточно для вывода «LinQ поддерживает произвольные динамические H/W».

<a id="f063"></a>

### F063 — , primary_documentation, S01 p7–8: `batch_axis=0`, `explicit_batch_value=None`; explicit_batch_value предназначен для сетей, не поддерживающих неявный batch. `as_graph` имеет batch

- Исходный локатор: [W1-05-F11](_WORK/W1_05_RESULT.md), строка50; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F063](RAW_FACTS.md#f063), primary_documentation, [S030](SOURCES.md#s030) p7–8: `batch_axis=0`, `explicit_batch_value=None`; explicit_batch_value предназначен для сетей, не поддерживающих неявный batch. `as_graph` имеет batch_size и batch_axis. Пример на p16 описывает явный batch; p19 передаёт форму `(1,224,224,3)`. Термины explicit/implicit не раскрывают, меняется ли batch без перекомпиляции и какие batch sizes разрешены аппаратно.

<a id="f064"></a>

### F064 — , reported_measurement, S05 p3–4: автор приводит ResNet и ряд сетей при batch1 и batch8. Это свидетельство заявленных конкретных batch-режимов, не подтверждение универсального дина

- Исходный локатор: [W1-05-F12](_WORK/W1_05_RESULT.md), строка51; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F064](RAW_FACTS.md#f064), reported_measurement, [S033](SOURCES.md#s033) p3–4: автор приводит ResNet и ряд сетей при batch1 и batch8. Это свидетельство заявленных конкретных batch-режимов, не подтверждение универсального динамического batching. Для yolov8n_pose в таблице только batch1.

<a id="f065"></a>

### F065 — , primary_documentation, S08: ONNX различает целочисленные размерности, именованные символические размерности, неизвестные размерности и отсутствие shape. Inference: валидный ONNX 

- Исходный локатор: [W1-05-F13](_WORK/W1_05_RESULT.md), строка52; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S042](SOURCES.md#s042)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F065](RAW_FACTS.md#f065), primary_documentation, [S042](SOURCES.md#s042): ONNX различает целочисленные размерности, именованные символические размерности, неизвестные размерности и отсутствие shape. Inference: валидный ONNX с символическим N ещё не является контрактом компилятора; нужно раздельно выяснить допустимость symbol при импорте и изменение N у готовой TPU программы.

<a id="f066"></a>

### F066 — , primary_documentation, S01 p15 и25: демонстрационный calibration использует два изображения для простоты, терминологический раздел рекомендует 100 образцов. Это не минимально доп

- Исходный локатор: [W1-05-F14](_WORK/W1_05_RESULT.md), строка53; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F066](RAW_FACTS.md#f066), primary_documentation, [S030](SOURCES.md#s030) p15 и25: демонстрационный calibration использует два изображения для простоты, терминологический раздел рекомендует 100 образцов. Это не минимально допустимый размер и не доказательство достаточности 100 для промышленной камеры. Подготовка образцов должна повторять предобработку модели.

<a id="f067"></a>

### F067 — , primary_documentation, S01 p13–15: пример preprocess конвертирует изображение в RGB, делает центральный crop на 85% короткой стороны, resize 224×224, переводит в float32, вычитае

- Исходный локатор: [W1-05-F15](_WORK/W1_05_RESULT.md), строка57; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F067](RAW_FACTS.md#f067), primary_documentation, [S030](SOURCES.md#s030) p13–15: пример preprocess конвертирует изображение в RGB, делает центральный crop на 85% короткой стороны, resize 224×224, переводит в float32, вычитает `[123.68,116.779,103.939]`, добавляет ось0. Калибровка явно названа NHWC; concatenation axis0. Эти параметры относятся к показанному ResNet50, не рекомендуются автоматически для YOLO. Не показан общий переключатель layout и не описано, как конвертер обрабатывает исходный NCHW ONNX.

<a id="f068"></a>

### F068 — , primary_documentation, S01 p16: `rescale(data)` готовит вход квантованного TF-графа и возвращает выход к пользовательскому формату; фактический dtype определяется операциями кван

- Исходный локатор: [W1-05-F16](_WORK/W1_05_RESULT.md), строка58; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F068](RAW_FACTS.md#f068), primary_documentation, [S030](SOURCES.md#s030) p16: `rescale(data)` готовит вход квантованного TF-графа и возвращает выход к пользовательскому формату; фактический dtype определяется операциями квантованного графа. Float32 на границе исходной модели не означает FP32 аппаратное исполнение. Runtime-пример p20–21 передаёт исходный test_input_dict без явного rescale; значит нельзя копировать процедуру rescale квантованного TF-графа на SDK без сверки фактической metadata.

<a id="f069"></a>

### F069 — , vendor_statement, S03 и S06: основной аппаратный тип int8; HPS datasheet относит fp16/bfloat16 к перспективе (extraction искажает слово bfloat16 как `b/f_loat16`). Точные dtype в

- Исходный локатор: [W1-05-F17](_WORK/W1_05_RESULT.md), строка59; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S002](SOURCES.md#s002), [S026](SOURCES.md#s026)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F069](RAW_FACTS.md#f069), vendor_statement, [S002](SOURCES.md#s002) и [S026](SOURCES.md#s026): основной аппаратный тип int8; HPS datasheet относит fp16/bfloat16 к перспективе (extraction искажает слово bfloat16 как `b/f_loat16`). Точные dtype входа/выхода `.tpu`, accumulation, rounding, saturation и поддержка signed/unsigned не установлены.

<a id="f070"></a>

### F070 — , primary_documentation, S01 p17–21: показана граница имён: TensorFlow tensors имеют суффикс `:0`, SDK/TLM пользуются OP names; helper удаляет/добавляет нулевой суффикс. Переименов

- Исходный локатор: [W1-05-F18](_WORK/W1_05_RESULT.md), строка60; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F070](RAW_FACTS.md#f070), primary_documentation, [S030](SOURCES.md#s030) p17–21: показана граница имён: TensorFlow tensors имеют суффикс `:0`, SDK/TLM пользуются OP names; helper удаляет/добавляет нулевой суффикс. Переименование конвертером требует отдельного mapping. Не следует «обрезать всё после двоеточия» без проверки: документирован только `:0`, а пример INPUT_TENSOR_NAME extraction содержит необычное `' input:1'`.

<a id="f071"></a>

### F071 — , primary_documentation, S01 p15–21: входы/выходы исходной модели, квантованного графа, TLM и TPU проверяются одной процедурой. Демонстрационная проверка — top1 класса, не численно

- Исходный локатор: [W1-05-F19](_WORK/W1_05_RESULT.md), строка61; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F071](RAW_FACTS.md#f071), primary_documentation, [S030](SOURCES.md#s030) p15–21: входы/выходы исходной модели, квантованного графа, TLM и TPU проверяются одной процедурой. Демонстрационная проверка — top1 класса, не численное равенство всех значений. Для детектора нужен собственный parity protocol до NMS и task metrics после NMS.

<a id="f072"></a>

### F072 — , primary_documentation, S01 p9,19–20: `Network.from_quantized_model(quantized_model)` создаёт внутреннее представление. Компилятор принимает ModelParameters, Network, CompileParam

- Исходный локатор: [W1-05-F20](_WORK/W1_05_RESULT.md), строка65; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F072](RAW_FACTS.md#f072), primary_documentation, [S030](SOURCES.md#s030) p9,19–20: `Network.from_quantized_model(quantized_model)` создаёт внутреннее представление. Компилятор принимает ModelParameters, Network, CompileParameters и optional slicing_scheme; возвращает пару Executable и словарь TensorDescription. Последний важен для проверки контракта тензоров; его точные fields в manual не раскрыты.

<a id="f073"></a>

### F073 — , primary_documentation, S01 p9–10: `get_hw_params(tpu_type)` и preset `TPU_128x128_PARAMS` относятся к выбору hardware target. DEFAULT предлагается для новой сети, STAGING может д

- Исходный локатор: [W1-05-F21](_WORK/W1_05_RESULT.md), строка66; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F073](RAW_FACTS.md#f073), primary_documentation, [S030](SOURCES.md#s030) p9–10: `get_hw_params(tpu_type)` и preset `TPU_128x128_PARAMS` относятся к выбору hardware target. DEFAULT предлагается для новой сети, STAGING может давать неверные программы или слишком долго компилировать. Target FPGA и ASIC нельзя выбирать по дефолту из противоречивого snippet.

<a id="f074"></a>

### F074 — , primary_documentation, S01 p20: `TpuProgram.from_executable(*tlm_program)` и `to_file(...)` создают `.tpu`. Документ прямо проводит границу: Framework принимает исходную модель и

- Исходный локатор: [W1-05-F22](_WORK/W1_05_RESULT.md), строка67; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F074](RAW_FACTS.md#f074), primary_documentation, [S030](SOURCES.md#s030) p20: `TpuProgram.from_executable(*tlm_program)` и `to_file(...)` создают `.tpu`. Документ прямо проводит границу: Framework принимает исходную модель и выпускает TPU программу, SDK принимает TPU программу и исполняет на данных. `.qm` и `.tpu` — разные этапы. ONNX не показан как непосредственный вход `Device.load`.

<a id="f075"></a>

### F075 — , primary_documentation, S01 p20–21: пример SDK перечисляет устройства `tpu.Device.list_devices()`, открывает первое, загружает `.tpu`, создаёт inference context и вызывает `infere

- Исходный локатор: [W1-05-F23](_WORK/W1_05_RESULT.md), строка68; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- [F075](RAW_FACTS.md#f075), primary_documentation, [S030](SOURCES.md#s030) p20–21: пример SDK перечисляет устройства `tpu.Device.list_devices()`, открывает первое, загружает `.tpu`, создаёт inference context и вызывает `inference.sync(input_dict_with_op_names)`. Это локальный API устройства, а не публичный облачный REST/gRPC контракт. Автор guide описывает также TLM; симуляция не доказывает фактический LinQ inference.


## W1-06 — W1-06 — операторы, преобразования графа и компилятор LinQ

<a id="f076"></a>

### F076 — Руководство описывает ONNX→TF до квантования, затем внутреннюю модель для compiler и `.tpu` как границу Framework/SDK

- Исходный локатор: [W1-06-F01](_WORK/W1_06_RESULT.md), строка35; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F076](RAW_FACTS.md#f076) | Руководство описывает ONNX→TF до квантования, затем внутреннюю модель для compiler и `.tpu` как границу Framework/SDK | primary_documentation | просмотрен документ | [S030](SOURCES.md#s030) §§3.1–3.4 |

<a id="f077"></a>

### F077 — Compiler принимает `hardware_parameters`, `Network`, `CompileParameters`, optional `slicing_scheme`; возвращает executable + описания тензоров

- Исходный локатор: [W1-06-F02](_WORK/W1_06_RESULT.md), строка36; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F077](RAW_FACTS.md#f077) | Compiler принимает `hardware_parameters`, `Network`, `CompileParameters`, optional `slicing_scheme`; возвращает executable + описания тензоров | primary_documentation | просмотрен документ | [S030](SOURCES.md#s030) p9 |

<a id="f078"></a>

### F078 — Есть DEFAULT и STAGING; STAGING включает pipeline parallelism, второй DDR, cache placement, layer fusion и slicing

- Исходный локатор: [W1-06-F03](_WORK/W1_06_RESULT.md), строка37; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F078](RAW_FACTS.md#f078) | Есть DEFAULT и STAGING; STAGING включает pipeline parallelism, второй DDR, cache placement, layer fusion и slicing | primary_documentation | просмотрен документ | [S030](SOURCES.md#s030) p10 |

<a id="f079"></a>

### F079 — Документ предупреждает о недопустимых программах/долгой компиляции STAGING; рекомендует возврат DEFAULT и сообщение об ошибке

- Исходный локатор: [W1-06-F04](_WORK/W1_06_RESULT.md), строка38; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F079](RAW_FACTS.md#f079) | Документ предупреждает о недопустимых программах/долгой компиляции STAGING; рекомендует возврат DEFAULT и сообщение об ошибке | primary_documentation | просмотрен документ, не воспроизведено | [S030](SOURCES.md#s030) p10 |

<a id="f080"></a>

### F080 — SoftwareNetwork добавляет quantization/rescaling/graph operations; HardwareNetwork повторяет TPU-операции в TF

- Исходный локатор: [W1-06-F05](_WORK/W1_06_RESULT.md), строка39; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F080](RAW_FACTS.md#f080) | SoftwareNetwork добавляет quantization/rescaling/graph operations; HardwareNetwork повторяет TPU-операции в TF | primary_documentation | просмотрен документ | [S030](SOURCES.md#s030) pp7–8 |

<a id="f081"></a>

### F081 — Современный список содержит YOLO8/YOLO11, SSD MobileNet, SCRFD; p4 presentation приводит yolov8n_pose и yolo5s

- Исходный локатор: [W1-06-F06](_WORK/W1_06_RESULT.md), строка40; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement + reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033), [S002](SOURCES.md#s002)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F081](RAW_FACTS.md#f081) | Современный список содержит YOLO8/YOLO11, SSD MobileNet, SCRFD; p4 presentation приводит yolov8n_pose и yolo5s | vendor_statement / reported_measurement | прочитан источник, не запущено | [S033](SOURCES.md#s033) pp4–5, [S002](SOURCES.md#s002) |

<a id="f082"></a>

### F082 — Benchmark-контекст: Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43, i7-10700K

- Исходный локатор: [W1-06-F07](_WORK/W1_06_RESULT.md), строка41; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F082](RAW_FACTS.md#f082) | Benchmark-контекст: Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43, i7-10700K | reported_measurement | только просмотрен источник | [S033](SOURCES.md#s033) p4 |

<a id="f083"></a>

### F083 — Сторонний YOLOv8 export задаёт opset13 по умолчанию и `nms=False`; динамические оси включаются отдельным флагом

- Исходный локатор: [W1-06-F08](_WORK/W1_06_RESULT.md), строка42; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S044](SOURCES.md#s044), [S045](SOURCES.md#s045)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F083](RAW_FACTS.md#f083) | Сторонний YOLOv8 export задаёт opset13 по умолчанию и `nms=False`; динамические оси включаются отдельным флагом | source_code | просмотрен pinned файл | [S044](SOURCES.md#s044), [S045](SOURCES.md#s045) `scr/detection/export_yolov8s_to_onnx.py` |

<a id="f084"></a>

### F084 — Тот же build принудительно задаёт статическую форму `(1,3,H,W)`, calibrate/quantize, затем set_batch и compiler

- Исходный локатор: [W1-06-F09](_WORK/W1_06_RESULT.md), строка43; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S044](SOURCES.md#s044), [S045](SOURCES.md#s045)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F084](RAW_FACTS.md#f084) | Тот же build принудительно задаёт статическую форму `(1,3,H,W)`, calibrate/quantize, затем set_batch и compiler | source_code | просмотрен pinned файл | [S044](SOURCES.md#s044), [S045](SOURCES.md#s045) `build_yolov8_program.py` |

<a id="f085"></a>

### F085 — Runtime YOLOv8 после inference.sync выполняет NMS на host через PyTorch/Ultralytics

- Исходный локатор: [W1-06-F10](_WORK/W1_06_RESULT.md), строка44; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S044](SOURCES.md#s044), [S045](SOURCES.md#s045)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F085](RAW_FACTS.md#f085) | Runtime YOLOv8 после inference.sync выполняет NMS на host через PyTorch/Ultralytics | source_code | просмотрен код, без TPU запуска | [S044](SOURCES.md#s044), [S045](SOURCES.md#s045) `run_yolov8_tpu.py`:109–112, 279–290 |

<a id="f086"></a>

### F086 — Для этого кода TPU backend требует отдельные libtpu/tpu-dkms/pytpu/tpu_framework/mlperf; реальное устройство обязательно

- Исходный локатор: [W1-06-F11](_WORK/W1_06_RESULT.md), строка45; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S044](SOURCES.md#s044), [S045](SOURCES.md#s045)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F086](RAW_FACTS.md#f086) | Для этого кода TPU backend требует отдельные libtpu/tpu-dkms/pytpu/tpu_framework/mlperf; реальное устройство обязательно | primary_documentation автора | просмотрен RUN_SCENARIO | [S044](SOURCES.md#s044), [S045](SOURCES.md#s045) `RUN_SCENARIO.txt`:12–44 |

<a id="f087"></a>

### F087 — В YOLOv8 runtime есть атрибут args с тайскими символами вместо parser destination; likely AttributeError

- Исходный локатор: [W1-06-F12](_WORK/W1_06_RESULT.md), строка46; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S044](SOURCES.md#s044), [S045](SOURCES.md#s045)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F087](RAW_FACTS.md#f087) | В YOLOv8 runtime есть атрибут args с тайскими символами вместо parser destination; likely AttributeError | source_code + inference | локальный ast.parse подтвердил точный Unicode literal, не executed runtime | [S044](SOURCES.md#s044), [S045](SOURCES.md#s045) `run_yolov8_tpu.py`:206 |

<a id="f088"></a>

### F088 — Public operator matrix и автоматический CPU partitioning для получаемого SDK не установлены

- Исходный локатор: [W1-06-F13](_WORK/W1_06_RESULT.md), строка47; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030), [S046](SOURCES.md#s046), [S047](SOURCES.md#s047)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| [F088](RAW_FACTS.md#f088) | Public operator matrix и автоматический CPU partitioning для получаемого SDK не установлены | unknown | targeted search + просмотр перечисленных документов | [S030](SOURCES.md#s030)–[S046](SOURCES.md#s046), [S047](SOURCES.md#s047) |

<a id="f089"></a>

### F089 — Матрица конкретных операторов и границы вывода

- Исходный локатор: [W1-06-MATRIX-5](_WORK/W1_06_RESULT.md), строка67; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S044](SOURCES.md#s044), [S045](SOURCES.md#s045), [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Матрица конкретных операторов и границы вывода

| Узел/область | Что реально найдено | Что остаётся неизвестным | Предлагаемый тест после доступа |
|---|---|---|---|
| Resize | Никакого перечня modes/attributes для LinQ не найдено | nearest/bilinear, coordinate_transform, scales vs sizes, opset versions, динамический output | минимальные ONNX графы для атрибутов именно выбранного экспорта; сравнение чисел с эталоном |
| Gather | Нет таблицы support | constant/dynamic indices, axis, negative indices, shape graph handling | отдельно constant foldable и data-dependent варианты |
| NonMaxSuppression | [S044](SOURCES.md#s044), [S045](SOURCES.md#s045) избегает graph NMS (`nms=False`) и делает host NMS | поддержка ONNX NMS в compiler и конкретная семантика не установлены | сначала raw-head model и host NMS; затем отдельный NMS graph если нужен |
| Reshape | Общие API shapes; нет operator constraints | dynamic shape input, -1/0 semantics, compile-time folding | сравнить фиксированный экспорт и граф с shape tensor, не объявлять dynamic support заранее |
| Transpose | В терминах [S030](SOURCES.md#s030) транспонирование названо примером high-level слоя | какие permutations/ranks/dtypes компилируются | граф с перестановками из настоящей head; verify layout по контрольным значениям |
| Concat | В терминах [S030](SOURCES.md#s030) объединение названо примером слоя; operator matrix нет | axis/rank/alignment, mixed quant scales | реальные feature maps, несколько inputs, nontrivial quant ranges |
| Detector head | Списки сетей, benchmark yolov8n_pose; [S044](SOURCES.md#s044), [S045](SOURCES.md#s045) raw output boundary | включены ли decode/DFL/NMS, точные веса/exporter/input sizes | просить поддерживаемый vendor artifact + IO descriptors и воспроизвести его до custom export |

Все строки unknown — локализованное отсутствие доказательств, не ограничение самого процессора. Наличие семейства YOLO в списке не разрешает вывести поддержку каждого из этих операторов с произвольными атрибутами. Аналогично появление `np.transpose` или `np.concatenate` в runtime code означает host preprocessing/postprocessing, а не доказанную поддержку ONNX Transpose/Concat в TPU graph.


## W1-07 — W1-07. Квантование, калибровка и сохранение качества LinQ

<a id="f090"></a>

### F090 — Что подтверждено о разрядности

- Исходный локатор: [W1-07-F01](_WORK/W1_07_RESULT.md), строка35; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S002](SOURCES.md#s002), [S026](SOURCES.md#s026)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F090](RAW_FACTS.md#f090). Что подтверждено о разрядности

Тип: **vendor_statement**, источники [S002](SOURCES.md#s002), [S026](SOURCES.md#s026). Статус: страницы/извлечение прочитаны, аппаратно не проверено.

Производитель указывает int8 для вычислительного ядра и DNN Quant. В HPS datasheet fp16/bfloat16 отнесены к перспективе. Фраза о сохранении точности не сопровождается в этом разделе таблицей FP32→int8, датасетом или допустимой потерей качества. Из этих заявлений нельзя вывести разрядность каждого промежуточного тензора, accumulator, bias, конкретных входов/выходов программы или наличие mixed precision.

<a id="f091"></a>

### F091 — Исторический API квантизации

- Исходный локатор: [W1-07-F02](_WORK/W1_07_RESULT.md), строка41; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F091](RAW_FACTS.md#f091). Исторический API квантизации

Тип: **primary_documentation**, [S030](SOURCES.md#s030) §3.1. Статус: прочитан извлеченный документ; вызовы не выполнялись.

Документированный интерфейс: `dnn_quant.QuantizedModel.quantize(original_graph_def, input_shapes, output_nodes, calibration_dict, percentile=100.0, batch_axis=0, explicit_batch_value=None)`.

Калибровка задается словарем имен входных тензоров и ndarray. Получаются внутреннее представление, квантованные веса и граф с преобразованиями масштаба. Предусмотрены `.qm`, `as_graph(...)` и `rescale(data)`. Пример показывает выполнение исходного и квантованного TF-графов; вокруг квантованного TF-графа используются преобразования входов и выходов через `rescale`. Руководство объясняет это масштабированием и приведением типа; формула с zero-point, rounding rule и granularity не приведена.

Это **inference** о PTQ-пути: процедура принимает уже обученный frozen graph и калибровочные тензоры, не содержит optimizer/backprop/training. Само слово PTQ здесь не следует выдавать за точный vendor-термин. Прямого подтверждения QAT из описанного маршрута нет.

<a id="f092"></a>

### F092 — Калибровочные данные в руководстве

- Исходный локатор: [W1-07-F03](_WORK/W1_07_RESULT.md), строка51; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F092](RAW_FACTS.md#f092). Калибровочные данные в руководстве

Тип: **primary_documentation**, [S030](SOURCES.md#s030) с.15, 25. Статус: документ прочитан.

В терминах руководства калибровочный ndarray содержит N образцов обучающего набора с соответствующим предварительным преобразованием; рекомендация — 100. В примере взяты 2 изображения, объединенные по batch axis 0. Для демонстрационного ResNet50 использованы NHWC, RGB, crop/resize 224×224 и вычитание средних каналов. Это контракт демонстрационной модели, его нельзя переносить на YOLO или собственный exporter.

<a id="f093"></a>

### F093 — API стороннего примера отличается

- Исходный локатор: [W1-07-F04](_WORK/W1_07_RESULT.md), строка57; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S048](SOURCES.md#s048), [S030](SOURCES.md#s030), [S050](SOURCES.md#s050)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F093](RAW_FACTS.md#f093). API стороннего примера отличается

Тип: **source_code**, [S048](SOURCES.md#s048) L240–286. Статус: статический просмотр pinned файла; калибровка не запускалась.

Вместо единого вызова [S030](SOURCES.md#s030) код создает `RegularModel`, получает `thresholds = regular_model.calibrate(calibration_data=calibration_dict, percentile=args.percentile)` и вызывает `regular_model.quantize(thresholds)`. `.qm` сохраняется через `save(file_dir=..., file_name=...)`, а не старую сигнатуру `save(file_path)`.

Критический fallback L275–280: любой `TypeError` первого calibrate ловится и происходит повтор без `percentile`. **Inference:** успешное завершение скрипта не доказывает, что явно выбранный percentile применился. Причиной TypeError может быть и внутренний сбой; blanket fallback затрудняет диагностику. Не копировать этот прием молча в эксперимент по подбору threshold. [S050](SOURCES.md#s050) L308–312 и ResNet50 builder L340–348 используют аналогичный fallback.

<a id="f094"></a>

### F094 — Тензоры калибровки YOLOv8s

- Исходный локатор: [W1-07-F05](_WORK/W1_07_RESULT.md), строка65; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S048](SOURCES.md#s048), [S049](SOURCES.md#s049)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F094](RAW_FACTS.md#f094). Тензоры калибровки YOLOv8s

Тип: **source_code**, [S048](SOURCES.md#s048) L19–95, L304–324; [S049](SOURCES.md#s049) L215–282. Статус: статический просмотр.

Defaults: 500 изображений, `img_size=640`, `percentile=100.0`, chunk 128. Изображения сортируются и ограничиваются первыми N. Калибровка: letterbox, BGR→RGB, NCHW float32 /255. Полный тензор `(N,3,H,W)` хранится через memmap. Runtime делает такое же внешнее преобразование и подает float32 в `run`/`sync`; явного `quantized_model.rescale` в runner нет. Выход направляется в host-side NMS.

**Inference:** это полезный образец согласованной предобработки, но не доказательство всех dtype/scale внутри программы. Chunk уменьшает рабочий объем подготовки, а не обязательно память самого calibrate: ему передается весь memmap. При 500×3×640×640×4 байт backing store равен 2 457 600 000 байт (~2.29 GiB); промежуточные активации и копии требуют дополнительной памяти. Это расчет, не измерение RSS.

<a id="f095"></a>

### F095 — FCN использует другую нормализацию

- Исходный локатор: [W1-07-F06](_WORK/W1_07_RESULT.md), строка73; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S050](SOURCES.md#s050)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F095](RAW_FACTS.md#f095). FCN использует другую нормализацию

Тип: **source_code**, [S050](SOURCES.md#s050). Статус: статический просмотр.

Defaults: все доступные calibration-изображения (`--num-calibration-images=0`), размер 520×520, chunk 64, percentile 100.0. RGB bilinear resize → /255 → ImageNet mean/std → CHW float32. Тензор `(N,3,520,520)` передается тому же раздельному API calibrate/quantize. **Inference:** модельный preprocessing нужно версионировать вместе с калибровкой; нельзя иметь универсальный «LinQ preprocess» для всех сетей.

<a id="f096"></a>

### F096 — Разделение данных есть, стратификации нет

- Исходный локатор: [W1-07-F07](_WORK/W1_07_RESULT.md), строка79; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S051](SOURCES.md#s051)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F096](RAW_FACTS.md#f096). Разделение данных есть, стратификации нет

Тип: **source_code**, [S051](SOURCES.md#s051). Статус: только чтение.

Default calibration ratio 0.1 и seed 42. Список перемешивается, калибровочная и evaluation части разделены по image ID; COCO-аннотации фильтруются по выбранным изображениям. VOC берет исходный segmentation val split. В `split_items` не используются классы, площади объектов, камеры или сцены. **Inference:** это воспроизводимое случайное разбиение, но не гарантия покрытия редких/малых СИЗ и не защита от сходных соседних кадров одной камеры по обе стороны разделения.

<a id="f097"></a>

### F097 — Внешний контракт зависит от артефакта

- Исходный локатор: [W1-07-F08](_WORK/W1_07_RESULT.md), строка85; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S052](SOURCES.md#s052), [S053](SOURCES.md#s053)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F097](RAW_FACTS.md#f097). Внешний контракт зависит от артефакта

Тип: **source_code** и авторское заявление, [S052](SOURCES.md#s052), [S053](SOURCES.md#s053). Статус: README и код просмотрены; `.tpu` не запускался.

Для `tiny_yolo3_b8_o5_128x128_asic.tpu` автор указывает `input_1:0`, `(8,416,416,3)`, NHWC, float32 0..1. Это отличается от YOLOv8s NCHW. Существование int8-ядра не является указанием подавать сырые int8-байты в Python runtime. Параметры `unit_float`/`uint8` runner — варианты внешней подготовки, их наличие само по себе не доказывает, что любой `.tpu` принимает оба диапазона.

<a id="f098"></a>

### F098 — Что известно о качестве

- Исходный локатор: [W1-07-F09](_WORK/W1_07_RESULT.md), строка91; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation + source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030), [S049](SOURCES.md#s049), [S052](SOURCES.md#s052), [S053](SOURCES.md#s053), [S054](SOURCES.md#s054)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F098](RAW_FACTS.md#f098). Что известно о качестве

Тип: **primary_documentation** для [S030](SOURCES.md#s030) §4; **source_code** для [S049](SOURCES.md#s049)/[S052](SOURCES.md#s052), [S053](SOURCES.md#s053); статус: прочитано, собственных измерений нет.

Пример руководства сохраняет top-1 класс одного изображения, но ранжирование остальных классов меняется между исходным, квантованным и TLM/TPU путями. Это проверка одного случая, не accuracy всего датасета. В репозитории есть COCOeval runner и отдельные ONNX-ветки; наличие скриптов означает доступный механизм будущего сравнения, не найденный численный результат FP32→int8. Отсутствие результатов в tracked файлах согласуется с [S054](SOURCES.md#s054), но не доказывает, что автор никогда их не получал.

<a id="f099"></a>

### F099 — Современная презентация не закрывает численную семантику

- Исходный локатор: [W1-07-F10](_WORK/W1_07_RESULT.md), строка97; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement + reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F099](RAW_FACTS.md#f099). Современная презентация не закрывает численную семантику

Тип: **vendor_statement** / **reported_measurement**, [S033](SOURCES.md#s033) с.3–4; статус: извлечение прочитано.

Презентация 2026 сохраняет int8-позиционирование. В опубликованном performance-контексте названы Runtime 16.18.6 и Framework 2026.8.43, однако не опубликованы нужные нам результаты качества до/после quantization, scales/zero-point, состав calibration set и точная схема quantizer. Нет основания объявлять эти версии установленными на обещанном онлайн-сервере.


## W1-08 — W1-08 — модели, YOLO и сила доказательств

<a id="f100"></a>

### F100 — Официальный перечень не является Model Zoo с артефактами

- Исходный локатор: [W1-08-F01](_WORK/W1_08_RESULT.md), строка35; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S002](SOURCES.md#s002), [S003](SOURCES.md#s003), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S044](SOURCES.md#s044), [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), [S049](SOURCES.md#s049), [S056](SOURCES.md#s056), [S053](SOURCES.md#s053), [S057](SOURCES.md#s057), [S058](SOURCES.md#s058), [S059](SOURCES.md#s059), [S060](SOURCES.md#s060), [S061](SOURCES.md#s061), [S062](SOURCES.md#s062)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F100](RAW_FACTS.md#f100). Официальный перечень не является Model Zoo с артефактами

Тип: vendor_statement; проверка: /tech реально открыт и прочитан web; presentation text прочитан TinyFish. На /tech есть перечисление моделей, но просмотренный блок не даёт checkpoint URLs, hashes, input/output manifests или compiler logs. На /sol Model Zoo перечислен как компонент комплекта ПО. Это подтверждает существование предложения производителя, но не доступность комплекта нам. Точные «YOLO8» и «YOLO11» не задают размер модели, task, input, exporter или версию пакета.

Guide2025 §3.4 использует более сильную формулировку «протестированных с использованием фреймворка IVA H1», но также без конфигураций. Дополнительные имена guide: FCN_8s (назван классом U-Net), seresnet50, flownet, REGNET_Y_800MF, anti_spoof_mn. Не подменять FCN_8s современным torchvision FCN-ResNet50.

<a id="f101"></a>

### F101 — Современное vendor-измерение относится к pose

- Исходный локатор: [W1-08-F02](_WORK/W1_08_RESULT.md), строка41; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S002](SOURCES.md#s002), [S003](SOURCES.md#s003), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S044](SOURCES.md#s044), [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), [S049](SOURCES.md#s049), [S056](SOURCES.md#s056), [S053](SOURCES.md#s053), [S057](SOURCES.md#s057), [S058](SOURCES.md#s058), [S059](SOURCES.md#s059), [S060](SOURCES.md#s060), [S061](SOURCES.md#s061), [S062](SOURCES.md#s062)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F101](RAW_FACTS.md#f101). Современное vendor-измерение относится к pose

Тип: reported_measurement производителя; проверка: прочитан извлечённый текст первичного PDF, не собственный benchmark. Presentation2026 p4 содержит `yolo5s` и `yolov8n_pose`, оба b1. Общая сноска: Intel Core i7-10700K @3.80GHz, Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43, заявленная методика MLCommons MLPerf. Значения приведены в матрице. Нет веса/разрешения/числа потоков/raw logs/точного режима MLPerf/качества. У HPQ throughput ровно4x HP, latency сохранена — не выводить из этого end-to-end скорость одной видеокамеры. Фраза методики не доказывает официальный submitted MLPerf result.

<a id="f102"></a>

### F102 — Происхождение стороннего репозитория установлено до commit

- Исходный локатор: [W1-08-F03](_WORK/W1_08_RESULT.md), строка45; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S002](SOURCES.md#s002), [S003](SOURCES.md#s003), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S044](SOURCES.md#s044), [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), [S049](SOURCES.md#s049), [S056](SOURCES.md#s056), [S053](SOURCES.md#s053), [S057](SOURCES.md#s057), [S058](SOURCES.md#s058), [S059](SOURCES.md#s059), [S060](SOURCES.md#s060), [S061](SOURCES.md#s061), [S062](SOURCES.md#s062)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F102](RAW_FACTS.md#f102). Происхождение стороннего репозитория установлено до commit

Тип: source_code + local_observation; проверка: прочитан checkout W1-06, `git rev-parse HEAD` и `git show -s --format=fuller HEAD` выполнены. HEAD `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`; автор/committer `sherstpasha`; 2026-04-03 12:44:54 +0700. Сообщение: Add error handling for device detection in parallel MLPerf scripts. Это пользовательский primary code и свидетельство его собственных инженерных попыток. Не обнаружено основания называть его официальным LinQ SDK или гарантированной конфигурацией хакатона.

`.gitignore` исключает `*.json`, `*.onnx`, `*.pt`, `*.weights`, `*.h5`, `data/`, `artifacts/`, `experiments*/`, `third_party/`, а также `POYASNITELNAYA_ZAPISKA_LinQ_RESULTS.md`. Поэтому наличие упоминаний результатов в сценарии не означает их публикацию. В checkout есть код и RUN_SCENARIO, отсутствуют сами model binaries/compiler logs/results summaries. Нельзя извлечь количественный benchmark из перечисленных путей.

<a id="f103"></a>

### F103 — YOLOv8: точный экспорт и неприкреплённые версии

- Исходный локатор: [W1-08-F04](_WORK/W1_08_RESULT.md), строка51; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S002](SOURCES.md#s002), [S003](SOURCES.md#s003), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S044](SOURCES.md#s044), [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), [S049](SOURCES.md#s049), [S056](SOURCES.md#s056), [S053](SOURCES.md#s053), [S057](SOURCES.md#s057), [S058](SOURCES.md#s058), [S059](SOURCES.md#s059), [S060](SOURCES.md#s060), [S061](SOURCES.md#s061), [S062](SOURCES.md#s062)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F103](RAW_FACTS.md#f103). YOLOv8: точный экспорт и неприкреплённые версии

Тип: source_code; проверка: прочитаны `export_yolov8s_to_onnx.py`, `build_yolov8_program.py`, `run_yolov8.py`, `run_yolov8_tpu.py`.

Exporter default: `YOLO('yolov8s.pt')`; ONNX `imgsz=640`, `opset=13`, `batch=1`, `dynamic=False`, `simplify=False`, `nms=False`. `YOLO_AUTOINSTALL=False`. При существующем локальном пути использует его; для встроенных n/s/m/l/x передаёт имя Ultralytics. Иного immutable asset URL/version/SHA код не фиксирует. Sidecar JSON сохраняет weights string/source, opset, batch, img size, flags, input/output names/shape, но не package versions и checksum checkpoint/ONNX.

requirements: `numpy==1.26.4`, `onnx~=1.16.0`, `onnxruntime~=1.18.0`, `tensorflow==2.14.1`, `setuptools<81`; torch/torchvision без версии; ultralytics вообще не включён в requirements (runner требует установить отдельно). `tf2onnx` для strict exporter тоже отдельная зависимость. Это не воспроизводимый lockfile. Актуальные online Ultralytics docs уже показывают более новые поколения/изменения default export flags; нельзя ими подменять неизвестную версию автора апреля2026.

<a id="f104"></a>

### F104 — YOLOv8: build contract

- Исходный локатор: [W1-08-F05](_WORK/W1_08_RESULT.md), строка59; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S002](SOURCES.md#s002), [S003](SOURCES.md#s003), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S044](SOURCES.md#s044), [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), [S049](SOURCES.md#s049), [S056](SOURCES.md#s056), [S053](SOURCES.md#s053), [S057](SOURCES.md#s057), [S058](SOURCES.md#s058), [S059](SOURCES.md#s059), [S060](SOURCES.md#s060), [S061](SOURCES.md#s061), [S062](SOURCES.md#s062)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F104](RAW_FACTS.md#f104). YOLOv8: build contract

Тип: source_code; проверка: только чтение. В build вход ONNX принудительно статизируется `[1,3,640,640]`; calibration RGB, NCHW, float32 /255, letterbox. Общий helper: OpenCV INTER_LINEAR, padding114, rounded scaled width/height, symmetric integer padding. Вызов `onnx_to_tf` пробует namespace tpu_framework, затем onnx_direct; варианты `try_simplify=True`, False, без параметра. Это адаптационный код, не документированный универсальный контракт SDK.

После RegularModel/calibrate/quantize сохраняется `.qm`; default percentile100, 500 calibration images, chunk128; `Network.from_quantized_model`, `network.set_batch`, `compiler.compile_(hardware_parameters=TPU_128x128_PARAMS, ..., parameters=O1)`, `TpuProgram.from_executable(...).to_file(...)`; defaults batches1/8. `128x128` — параметр аппаратного массива, не разрешение входного изображения. Детальную компиляцию/калибровку исследуют W1-06/W1-07; здесь важен model contract, а не подтверждение результата.

<a id="f105"></a>

### F105 — YOLOv8 runner: конкретная блокирующая ошибка

- Исходный локатор: [W1-08-F06](_WORK/W1_08_RESULT.md), строка65; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual AST/isolated helper check; no full runner/model/device execution.

- Sources: [S002](SOURCES.md#s002), [S003](SOURCES.md#s003), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S044](SOURCES.md#s044), [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), [S049](SOURCES.md#s049), [S056](SOURCES.md#s056), [S053](SOURCES.md#s053), [S057](SOURCES.md#s057), [S058](SOURCES.md#s058), [S059](SOURCES.md#s059), [S060](SOURCES.md#s060), [S061](SOURCES.md#s061), [S062](SOURCES.md#s062)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F105](RAW_FACTS.md#f105). YOLOv8 runner: конкретная блокирующая ошибка

Тип: source_code + local_observation; проверка: AST без импортов и аппаратного запуска. В `run_yolov8_tpu.py:206` вызывается `args.output_tensอร์_name`; parser определяет `--output-tensor-name`, то есть `output_tensor_name`. В середине фактического атрибута стоят U+0E2D/U+0E23/U+0E4C. В нормальном исполнении после прохождения ранних проверок это приводит к AttributeError до `tpu.Device.list_devices()`. Сохранён протокол `_WORK/W1_08/yolov8_runner_ast_audit.json`. Это вывод из синтаксиса, не зарегистрированный аппаратный error log.

Дополнительно: input probing пробует несколько tensor names и `run`/`sync`, output selection может взять первый rank≥3 tensor. Это полезные эвристики при диагностике, но для acceptance нужен manifest с единственным правильным output. Код принимает формы `[B,84,N]`/`[B,N,84]` и также85; это COCO80-specific предположение. После обучения на N иных классов ширина4+N не пройдёт проверку. Даже принятие85 не доказывает корректную семантику objectness для другой версии YOLO.

Postprocessing выполняется на host: `ultralytics.utils.nms.non_max_suppression`, conf0.001, IoU0.65, max_det300, преобразование координат обратно после letterbox, COCO80→91 categories. Для касок/респираторов нужно убрать фиксированную COCO mapping и явно задать class count. Наличие CPU torch для NMS не означает CPU исполнения backbone; это отдельная стадия.

Timing обрамляет только `run_once`, не preprocessing/NMS/декодирование/видео. Warmup вычитается числом изображений; при пересечении границы warmup внутри batch может учитываться полный batch time с меньшим числом measured images. Поэтому скриптовый FPS нельзя выдавать за end-to-end FPS или строгий latency benchmark без проверки методики.

<a id="f106"></a>

### F106 — TinyYOLO3: три разных маршрута

- Исходный локатор: [W1-08-F07](_WORK/W1_08_RESULT.md), строка75; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S002](SOURCES.md#s002), [S003](SOURCES.md#s003), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S044](SOURCES.md#s044), [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), [S049](SOURCES.md#s049), [S056](SOURCES.md#s056), [S053](SOURCES.md#s053), [S057](SOURCES.md#s057), [S058](SOURCES.md#s058), [S059](SOURCES.md#s059), [S060](SOURCES.md#s060), [S061](SOURCES.md#s061), [S062](SOURCES.md#s062)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F106](RAW_FACTS.md#f106). TinyYOLO3: три разных маршрута

Тип: source_code; проверка: прочитаны README/exporter/downloader/runner/ORT helpers.

1. **Vendor TPU**: внешний путь `linq_files/tpu_programs/tiny_yolo3_b8_o5_128x128_asic.tpu`, `input_1:0`, b8, NHWC416, float0..1. `run_tiny_yolo3_accuracy.py` выполняет letterbox и BGR→RGB. Runner декодирует raw-head выходы; generic формы поддерживают транспонирование/перестановки. Anchor defaults `10,14 23,27 37,58 81,82 135,169 344,319`, masks coarse→fine `3,4,5|0,1,2`, classes80. Декодирование использует sigmoid xy/objectness/classes, exp wh, anchors, grid/stride; внешний NMS. Это не встроенный NMS Model Zoo. Quality direct TPU + COCOeval; performance отдельно mlperf. README называет runtime contract подтверждённым, но бинарник/manifest/raw result недоступны в checkout.
2. **Strict ONNX**: cfg `https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg`, weights `https://data.pjreddie.com/files/yolov3-tiny.weights`; код сам строит Keras модель, читает Darknet header/BN/conv weights, сохраняет h5, экспортирует tf2onnx opset13; dynamic batch default0, NHWC416, `input_1`, raw heads. Имена enum/layers и anchors доступны, но URL cfg на master и weight URL без checksum — ещё не immutable provenance. Сравнение с vendor weights пока гипотеза: vendor source/hash не раскрыты.
3. **ONNX Model Zoo**: downloader использует `https://huggingface.co/onnxmodelzoo/tiny-yolov3-11/resolve/main/tiny-yolov3-11.onnx`; model card показывает ONNX1.6/opset11, ~34MB, image NCHW1x3x416x416 и второй input1x2 original image size, outputs boxes/scores/selected indices. Это другой graph boundary со встроенным selection/NMS, не raw-head vendor `.tpu`.

Важное расхождение: strict metadata задаёт BGR; ORT `preprocess_image` фактически оставляет OpenCV BGR и вообще не применяет поле image_color_order. Vendor runner делает RGB. Оба используют общий padding114/INTER_LINEAR. В primary Model Zoo card пример PIL RGB, padding128/BICUBIC. Поэтому «тот же TinyYOLO3» не означает честное сравнение качества или скорости. Сначала нужен byte-identical prepared tensor и проверка головы/весов. Это конкретный повод для sanity test цветного изображения до большого COCOeval.

Model Zoo card сообщает mAP0.331 как значение исходной TinyYOLOv3 на COCO, не LinQ INT8 measurement и не наш ORT test. Не переносить это качество на vendor compiled model.

<a id="f107"></a>

### F107 — FCN-ResNet50: точные веса известнее, но итогов исполнения нет

- Исходный локатор: [W1-08-F08](_WORK/W1_08_RESULT.md), строка87; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation + source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S002](SOURCES.md#s002), [S003](SOURCES.md#s003), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S044](SOURCES.md#s044), [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), [S049](SOURCES.md#s049), [S056](SOURCES.md#s056), [S053](SOURCES.md#s053), [S057](SOURCES.md#s057), [S058](SOURCES.md#s058), [S059](SOURCES.md#s059), [S060](SOURCES.md#s060), [S061](SOURCES.md#s061), [S062](SOURCES.md#s062)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F107](RAW_FACTS.md#f107). FCN-ResNet50: точные веса известнее, но итогов исполнения нет

Тип: source_code + primary_documentation; проверка: source files, RUN_SCENARIO и torchvision docs прочитаны. Export использует `FCN_ResNet50_Weights.COCO_WITH_VOC_LABELS_V1`, wrapper возвращает `model(x)['out']`; default tensor `[1,3,520,520]`, float normalized, input `input`, output `logits`, opset18, `dynamo=False`, constant folding, dynamic_axes batch/height/width. Quantizer позже статизирует input. Host preprocessing RGB PIL, принудительный square520 resize, /255 и ImageNet mean/std. Runtime делает argmax по class axis и resize mask nearest к исходному размеру. Это 21 labels (20 VOC + background), не произвольный промышленный segmentation head.

Torchvision primary docs объясняют, что enum обучен на COCO subset с VOC20; стандартный transform resize short side520 с aspect ratio и normalization. Репозиторный square resize — собственный контракт; его нельзя назвать byte-identical official transform. Публикуемое torchvision mIoU60.5 относится к COCO-val2017-VOC-labels, не к TPU INT8 и не прямо к репозиторному VOC2012 eval.

Standalone compile defaults O5/b8, но RUN_SCENARIO явно говорит, что segmentation O5 не дал final reproducible result и не должен входить в final result set. Это содержательная отрицательная зацепка; наличие defaultO5 не доказательство работоспособности. README называет TPU и ORT контуры рабочими, но численных summaries/logs в публичном checkout нет.

<a id="f108"></a>

### F108 — Разные контракты нельзя унифицировать по названию модели

- Исходный локатор: [W1-08-F09](_WORK/W1_08_RESULT.md), строка95; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033), [S059](SOURCES.md#s059), [S060](SOURCES.md#s060)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F108](RAW_FACTS.md#f108). Разные контракты нельзя унифицировать по названию модели

Тип: inference из [S033](SOURCES.md#s033)–[S059](SOURCES.md#s059), [S060](SOURCES.md#s060). В одном repo ResNet50 wrapper принимает NHWC0..255 с normalization внутри ONNX; YOLOv8 принимает NCHW0..1; TinyYOLO3 vendor NHWC0..1 RGB; TinyYOLO3 ORT остаётся BGR; FCN принимает уже нормализованный NCHW. Универсальный `frame/255` перед любым `.tpu` неверен. Первым артефактом интеграции должен быть machine-readable model manifest: source weights/hash; versions; graph/checksum; exact tensor names/shapes/layout/color/range; resize/pad/interpolation; class map; raw head/postprocessing; calibration provenance; compiler target/batch/preset; runtime version.


## W1-09 — W1-09 — LinQ: runtime API, артефакты и условные режимы online-доступа

<a id="f109"></a>

### F109 — официальный локальный Python runtime

- Исходный локатор: [W1-09-F01](_WORK/W1_09_RESULT.md), строка21; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F109](RAW_FACTS.md#f109) — официальный локальный Python runtime

- Тип: `primary_documentation`; выполненная проверка: прочитан сохранённый извлечённый текст guide; новый web open PDF вернул Internal Error.
- Источник: [S030](SOURCES.md#s030), §3.4, печатные pp.20–21; extracted lines 547–592.
- `Device.list_devices()` описан как поиск устройств **в локальном хосте**. Далее используются context managers `Device.open(...)`, `device.load(path)`, `program.inference()` и `inference.sync(input_dict_with_op_names)`.
- `sync` — блокирующий вызов. Вход — именованный словарь; выход читается по имени операции. В ResNet примере удаляют суффикс `:0` перед вызовом и восстанавливают tensor name после. Это пример преобразования имен, не универсальное правило для всех экспортов.
- Guide не даёт публичную полную спецификацию runtime/C ABI, ошибки всех методов, потокобезопасность, multiprocess semantics или сетевой API.

<a id="f110"></a>

### F110 — `.tpu`, веса и место компилятора

- Исходный локатор: [W1-09-F02](_WORK/W1_09_RESULT.md), строка29; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F110](RAW_FACTS.md#f110) — `.tpu`, веса и место компилятора

- Тип: `primary_documentation`; проверено чтением [S030](SOURCES.md#s030) §3.4 pp.19–20.
- Framework строит квантованную модель, затем `Network.from_quantized_model(...)`; компиляция выдаёт TLM программу с инструкциями TPU и константами/весами. `TpuProgram.from_executable(...)` и `.to_file(...)` сохраняют `.tpu`.
- Guide прямо обозначает `.tpu` разделительной линией Framework → SDK. Следствие (`inference`): на runtime-only машине может быть достаточно согласованной `.tpu`, без исходного training framework и компилятора. Но возможность компилировать на другой машине и переносимость `.tpu` нужно подтвердить для конкретных версий и target.
- Передача нового `.pt`/ONNX сама по себе не является загрузкой исполняемой программы в этот API. Для обновлённых весов нужен новый совместимый артефакт подготовки, если поставщик не выдаст иной явно поддержанный путь.

<a id="f111"></a>

### F111 — открытый исторический пакет получен и проверен без установки

- Исходный локатор: [W1-09-F03](_WORK/W1_09_RESULT.md), строка36; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S063](SOURCES.md#s063), [S064](SOURCES.md#s064), [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F111](RAW_FACTS.md#f111) — открытый исторический пакет получен и проверен без установки

- Тип: `local_observation` + `source_code`; выполнено: HTTPS PyPI JSON, скачивание sdist, сверка SHA256, безопасное чтение/извлечение отдельных файлов; пакет не импортировался и не устанавливался.
- Источники [S063](SOURCES.md#s063), [S064](SOURCES.md#s064)/[S065](SOURCES.md#s065); версия `15.0.24`, release/upload 2023-11-27.
- SHA256: `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`, совпал с PyPI.
- Локально: `W1_09/PYTPU_METADATA.json`, `W1_09/pytpu-15.0.24.tar.gz`, `W1_09/PYTPU_SOURCE/pytpu-15.0.24/`, `W1_09/LOCAL_CHECKS.json`.
- Доступность source distribution не означает наличие native `.so`, драйвера, compiler или права считать пакет актуальным SDK LinQ.

<a id="f112"></a>

### F112 — происхождение и предел атрибуции `pytpu`

- Исходный локатор: [W1-09-F04](_WORK/W1_09_RESULT.md), строка44; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F112](RAW_FACTS.md#f112) — происхождение и предел атрибуции `pytpu`

- Тип: `source_code`/metadata; проверено чтением PyPI, setup.py, archive manifest.
- PyPI maintainer: `IvaTechnologies`; author: `IVA-Tech`; `author_email='info@iva-tech.ru'`; homepage `http://git.mmp.iva-tech.ru/tpu_sw/iva_tpu_sdk`.
- В `_bindings.py` есть ссылка разработчиков на `https://jira.hi-tech.org/browse/TPU2-2010`. Это внутренний locator в исходнике, не открытый проверенный issue.
- Независимая связь с исследуемым стеком: текущий официальный `/sol` связывает ПО IVA H1 с OEM на LinQ H; официальный [S030](SOURCES.md#s030) импортирует `pytpu` и показывает то же семейство методов. Этого достаточно для исторической технической зацепки, но не для утверждения, что PyPI upload — официально рекомендованный дистрибутив LinQ 2026, или что нынешняя компания контролирует PyPI account.
- В JSON license — пустая строка; license_expression отсутствует; `LICENSE` в sdist не найден; явной лицензии в setup.py нет. Правовой режим повторного использования не установлен. Публичность исходника не равна open-source лицензии.

<a id="f113"></a>

### F113 — реальное API sdist расходится с README

- Исходный локатор: [W1-09-F05](_WORK/W1_09_RESULT.md), строка52; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065), [S049](SOURCES.md#s049)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F113](RAW_FACTS.md#f113) — реальное API sdist расходится с README

- Тип: `source_code`; проверено статическим чтением [S065](SOURCES.md#s065), `_bindings.py` lines 180–253, 270–425; `__init__.py`.
- Экспортируются `Device`, `Program`, `Inference`, `InferenceError`, `convert_to_raw`. README, напротив, описывает `from iva_tpu import TPUDevice, TPUProgram, TPUInference`; этих экспортов в `pytpu/__init__.py` нет. Исторические README snippets с queue stats нельзя переносить на реальный API пакета без проверки.
- Реальные сигнатуры: `Device.open(dev_name: str)`; `Device.list_devices() -> List[str]`; `Device.info() -> Dict`; `Device.load(program_path: str)`; `Program.info() -> Dict`; `Program.inference()`; `Inference.sync(inputs, mode=ProcessingMode.FULL) -> Dict[str,np.ndarray]`.
- Метода `Inference.run` в этом sdist нет. Его наличие в defensive `hasattr` стороннего кода [S049](SOURCES.md#s049) не доказывает новый API.
- `list_devices` лишь просматривает `/dev`, фильтруя regex `tpu.` и длину имени 4; не делает handshake с accelerator и не гарантирует usable device. Например, двухзначные имена этим историческим фильтром не обнаруживаются. `Device.open` вызывает native create/init/validation; именно это существенно сильнее простого списка файлов.

<a id="f114"></a>

### F114 — ctypes и native runtime

- Исходный локатор: [W1-09-F06](_WORK/W1_09_RESULT.md), строка60; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F114](RAW_FACTS.md#f114) — ctypes и native runtime

- Тип: `source_code`; проверено чтением [S065](SOURCES.md#s065) `_bindings.py` lines 28–159.
- Абсолютный путь native библиотеки: `/usr/lib/libtpu.2.so`; загрузчик `ctypes.CDLL` ленивый. Python dependency в setup.py — `numpy`; native driver/runtime в pip dependencies не поставляются.
- Поэтому успешный `import pytpu` по конструкции пакета **не доказывает** наличие libtpu, доступ к `/dev/tpuN` и исполнение модели. Аналогично framework import test из guide проверяет import Framework, а не аппаратный inference.
- Реальные native symbol names включают `tpu_create_device`, `tpu_init_device`, `tpu_load_program`, `tpu_create_program`, `tpu_create_inference`, `tpu_run_inference`, `tpu_get_inference_status`, `tpu_get_program_info`, `tpu_get_device_info`. Есть bindings `tpu_submit_inference` с callback, но это не доказательство поддержанного публичного Python async API.
- Для C/C++ это доказательство существования C boundary в исторической `.so`, а не достаточный header/ABI contract. Публичные headers, libtpu download, link flags и современный C++ example в этой ветке не найдены.

<a id="f115"></a>

### F115 — outputs и metadata: конкретный исторический контракт

- Исходный локатор: [W1-09-F07](_WORK/W1_09_RESULT.md), строка68; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F115](RAW_FACTS.md#f115) — outputs и metadata: конкретный исторический контракт

- Тип: `source_code`; проверено [S065](SOURCES.md#s065) `_bindings.py` lines 270–300, 332–499.
- `Program.info()` возвращает JSON native metadata. Внутри читаются `metadata['inputs']['1']`, `metadata['outputs']['2']`, `metadata['hardware_parameters']`. Входные имена и выходные имена берутся из metadata, а не угадываются по названию ONNX.
- `sync` принимает Mapping; создаёт input/output buffers, вызывает native inference, проверяет return/status codes. Native ошибки оборачиваются в `InferenceError` с `Invalid tpu_run_inference return code ...` либо `Invalid inference status code ...`.
- Для обычной программы результат — dictionary ndarray: dtype через `user_dtype`, shape через `user_shape`. Это реальные model outputs, ещё не events или boxes обязательного прикладного формата. Int8 арифметика ядра не означает, что Python API всегда отдаёт int8.
- Для raw programme output reshapes по `ddr_word_len`; `_is_raw_program` читает ZIP member `metadata.json`, raw heuristic — отсутствие `user_dtype`. Это формат **этого** пакета; не гарантированная спецификация всех `.tpu` 2026.
- Input data передаются через ndarray pointer. Сам код содержит TODO валидации dtype. Следствие: до вызова необходимо явно сверять имена, shape, dtype и C-contiguity; silent preprocessing/layout mismatch нельзя исключить одним успешным вызовом. Не установлен современный zero-copy/lifetime contract.

<a id="f116"></a>

### F116 — CLI и packaging inconsistency

- Исходный локатор: [W1-09-F08](_WORK/W1_09_RESULT.md), строка77; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030), [S063](SOURCES.md#s063), [S064](SOURCES.md#s064), [S065](SOURCES.md#s065), [S049](SOURCES.md#s049), [S060](SOURCES.md#s060), [S066](SOURCES.md#s066), [S053](SOURCES.md#s053), [S014](SOURCES.md#s014), [S026](SOURCES.md#s026), [S003](SOURCES.md#s003), [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F116](RAW_FACTS.md#f116) — CLI и packaging inconsistency

- Тип: `source_code` + `local_observation`; проверены setup.py и полный tar manifest.
- setup объявляет entrypoints `run_get_fps = pytpu.scripts.run_get_fps:main` и `pyrun_tpu = pytpu.scripts.pyrun_tpu_cli:main`. В опубликованном sdist директория `pytpu/scripts` отсутствует. Это статическое несоответствие упаковки: наличие entrypoint не доказывает runnable CLI; запуск не выполнен.
- `convert_to_raw` содержит условие internal dependency для debug conversion. Нельзя обещать пользователю полноценный RAW tooling из одного PyPI archive.

<a id="f117"></a>

### F117 — сторонний код 2026: что именно он добавляет

- Исходный локатор: [W1-09-F09](_WORK/W1_09_RESULT.md), строка83; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S049](SOURCES.md#s049)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F117](RAW_FACTS.md#f117) — сторонний код 2026: что именно он добавляет

- Тип: `source_code`; проверен pinned [S049](SOURCES.md#s049) commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`, локальный `git rev-parse HEAD` совпал.
- `run_yolov8_tpu.py`: тот же device/load/session; выбирает `run` при наличии, иначе `sync`, пробует несколько имён inputs. Это compatibility probing автора, не документация гарантированных SDK reflection методов.
- Inputs YOLO path: RGB, float32 /255, NCHW, letterbox. Outputs ожидаются rank3 с размерностью 84/85, далее host Ultralytics NMS. Последний batch дополняется повтором последнего изображения; лишние outputs отбрасываются. Эти контракты относятся к модели/runner, а не всем LinQ программам.
- Run-time timing обрамляет один runtime call; preprocessing/NMS за его пределами. Это не end-to-end latency сервиса. Готовых hardware logs этой веткой не получено.

<a id="f118"></a>

### F118 — Unicode defect независимо подтверждён AST

- Исходный локатор: [W1-09-F10](_WORK/W1_09_RESULT.md), строка90; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual AST/isolated helper check; no full runner/model/device execution.

- Sources: [S049](SOURCES.md#s049)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F118](RAW_FACTS.md#f118) — Unicode defect независимо подтверждён AST

- Тип: `local_observation`; выполнено: `ast.parse` без импорта runner и без TPU, `argparse.Namespace` проверка; результат сохранён LOCAL_CHECKS.json.
- [S049](SOURCES.md#s049) `scr/detection/run_yolov8_tpu.py` line206 обращается к `args.output_tens\u0e2d\u0e23\u0e4c_name` (Unicode escape точного identifier); parser создаёт `output_tensor_name`.
- В Namespace с объявленным parser именем `hasattr` первого атрибута False, правильного True. Если выполнение пройдёт предыдущие file/dependency/COCO checks, обращение вызывает AttributeError **до** `Device.list_devices/open`. Полный runner не запускался; это доказанный identifier mismatch, условный путь к исключению.
- Исправление стороннего примера не доказывает совместимость с установленным runtime и не превращает YOLOv8 path в подтверждённый аппаратный результат.

<a id="f119"></a>

### F119 — практический CLI benchmark и требования хоста в стороннем repo

- Исходный локатор: [W1-09-F11](_WORK/W1_09_RESULT.md), строка97; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S060](SOURCES.md#s060), [S066](SOURCES.md#s066), [S053](SOURCES.md#s053)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F119](RAW_FACTS.md#f119) — практический CLI benchmark и требования хоста в стороннем repo

- Тип: `source_code`/author scenario, не собственное измерение.
- [S060](SOURCES.md#s060) RUN_SCENARIO.txt (2026-03-25) требует отдельное TPU окружение `libtpu / tpu-dkms / pytpu / tpu_framework / mlperf`; `/dev/tpu0` отсутствует → пропустить TPU sections. Указанный автором binary path содержит `mlperf-16.16.12-Source/build/mlperf`; это не версия предоставленного нам SDK.
- [S066](SOURCES.md#s066) `run_fcn_resnet50_performance.py` фактически собирает `mlperf -s offline -m performance -p <program.tpu> -q <QPS>`. Binary — внешняя зависимость, в git не поставляется. Авторский wrapper сохраняет stdout/stderr, returncode, `mlperf_log_summary.txt`, проверяет `VALID` и Samples/sec. Такое имя не доказывает официальный MLCommons submission.
- [S053](SOURCES.md#s053) TinyYOLO runner имеет параметры layout/range и host postprocessing разных output layouts. Это показывает, почему вместе с чужим `.tpu` нужны metadata и эталонный postprocess; отсутствие единственного выхода `boxes` не означает неработающий TPU.

<a id="f120"></a>

### F120 — online/cloud: доказано заявление о направлении, не API доступа

- Исходный локатор: [W1-09-F12](_WORK/W1_09_RESULT.md), строка104; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S014](SOURCES.md#s014), [S026](SOURCES.md#s026)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F120](RAW_FACTS.md#f120) — online/cloud: доказано заявление о направлении, не API доступа

- Тип: `vendor_statement`; выполнено: самостоятельный web open текущего [S014](SOURCES.md#s014) `/hr`, [S026](SOURCES.md#s026) HPS datasheet.
- Официальная вакансия C++ говорит о Python prototype облачного inference и C++ пре-альфе. Требования/архитектуру сервиса ещё предлагают формализовать. Это свидетельство разработки cloud inference, но не public GA service и не режим хакатона.
- HPS datasheet p4 называет LinQ Cloud с контейнеризацией/виртуализацией ресурсов. Endpoint, schema, authentication, upload limits, quotas, scheduling и SDK версии там не установлены.
- Конкретные host/IP/token/SSH port, HTTP endpoint и container image для команды неизвестны. Отсутствие найденной публичной спецификации не доказывает, что закрытый сервис или документация не существуют.


## W1-10 — W1-10 — видео, tensor contracts и граница аппаратного inference

<a id="f121"></a>

### F121 — Официальный пример 2025 показывает границу до и после графа

- Исходный локатор: [W1-10-F01](_WORK/W1_10_RESULT.md), строка31; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F121](RAW_FACTS.md#f121). Официальный пример 2025 показывает границу до и после графа

Тип: primary_documentation. Проверка: прочитан локальный extracted guide, не аппаратный тест. Основание [S030](SOURCES.md#s030), стр.13,15–21.

В классификационном примере preprocessing предоставляет пользователь вместе с исходной моделью: PIL RGB; центральный квадрат со стороной `int(min(H,W)*0.85)`; resize224×224; float32; вычитание по RGB `[123.68,116.779,103.939]`; batch axis0. Формат `NHWC`, input shape `(1,224,224,3)`. Это **не** стандартный рецепт для всех LinQ/YOLO: здесь нет деления на255 и нет NCHW. Postprocess — индекс `argmax + 1` (классы примера нумеруются с1). Его применение к другому model zoo может дать систематическое смещение категории.

Тот же preprocess используется для калибровки и тестового изображения. Guide последовательно сравнивает исходный TensorFlow, квантованную модель, TLM и TPU через общую проверку ожидаемого класса; для quantized graph вход/выход проводят через `quantized_model.rescale`. При этом в примере `inference.sync` получает исходный словарь preprocess, без отдельного явного `rescale` в пользовательском hardware-call. **Вывод inference:** нельзя автоматически кормить int8 только потому, что вычислитель int8, и нельзя добавлять rescale поверх runtime без выяснения его контракта. Из одного walkthrough неизвестны все правила dtype/scales конкретного нового `.tpu`.

Guide явно называет `.tpu` границей Framework/SDK: Framework получает исходную модель, SDK загружает программу и исполняет заданные данные. Демонстрация использует `Device.list_devices → Device.open → device.load → program.inference → inference.sync`. Входы/выходы — словари. TensorFlow tensor name с `:0` преобразуется в operation name для TLM/runtime; это соглашение примера, не основание удалять произвольный суффикс во всех экспортерах. Извлечённый input literal выглядит как `' input:1'`, а helper удаляет лишь `:0`: из-за качества текста не фиксировать это как реальное обязательное input name.

Guide проверяет top1 на одном примере и печатает top16; этого недостаточно для доказательства численной эквивалентности, mAP или видеостабильности. TLM time является оценкой, не измерением end-to-end приложения.

<a id="f122"></a>

### F122 — Точный общий letterbox pinned repo

- Исходный локатор: [W1-10-F02](_WORK/W1_10_RESULT.md), строка43; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual isolated helper/formula/AST probe: _WORK/W1_10/CONTRACT_PROBES_RESULT.json; NumPy2.4.2; no OpenCV pixel resize, SDK or device execution.

- Sources: [S067](SOURCES.md#s067); [S173](SOURCES.md#s173)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F122](RAW_FACTS.md#f122). Точный общий letterbox pinned repo

Тип: source_code; проверка: чтение [S067](SOURCES.md#s067), формулы проверены локально. Для конкретных detection runners:

1. По изображению H×W вычисляется `r=min(S/H,S/W)`; resized size `(round(W*r), round(H*r))`, Python `round`.
2. `cv2.resize(...,INTER_LINEAR)`, полотно строго S×S. `dw=S-new_w`, `dh=S-new_h`; слева `dw//2`, справа остаток; сверху `dh//2`, снизу остаток. При нечётном padding дополнительный пиксель справа/снизу. Это не auto-stride letterbox и не растягивание изображения к квадрату.
3. Constant border `(114,114,114)`. Helper возвращает **номинальный** r и целочисленные left/top. Нет ограничителя scaleup: маленькие кадры могут увеличиваться.

Локальная проверка формул S=640: 1920×1080 →640×360, top/bottom140; 641×479 →640×478, top/bottom81. Во втором случае реальные масштабы x/y после округления немного отличаются, но код сохраняет единый r. Для воспроизведения именно этого примера inverse mapping должен повторять его r; для нового адаптера геометрическую конвенцию нужно зафиксировать и проверить. Это не установленная ошибка LinQ и не аппаратная численная проверка. OpenCV локально отсутствует, пиксельная интерполяция не выполнялась.

<a id="f123"></a>

### F123 — YOLOv8 boundary: RGB float NCHW и host NMS

- Исходный локатор: [W1-10-F03](_WORK/W1_10_RESULT.md), строка53; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S049](SOURCES.md#s049), [S055](SOURCES.md#s055), [S048](SOURCES.md#s048)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F123](RAW_FACTS.md#f123). YOLOv8 boundary: RGB float NCHW и host NMS

Тип: source_code. Проверка: чтение [S049](SOURCES.md#s049)–[S055](SOURCES.md#s055), [S048](SOURCES.md#s048), исполнение модели не выполнено.

При default640 оба TPU и ONNX runner используют `cv2.imread → letterbox → [:,:,::-1] → transpose(2,0,1) → float32/255 → expand_dims`. На runtime передаётся batch `[B,3,640,640]`, RGB unit float. Build calibration `preprocess_yolo` повторяет этот путь. Не нужно менять layout на NHWC по аналогии с guide2025: это разные модели и конверсия должна сохранять контракт конкретного экспорта.

Exporter задаёт `nms=False`. Runner ожидает rank3, ось каналов84 или85, при необходимости транспонирует в `[B,C,N]`. Это только эвристическая проверка формы; она не доказывает порядок координат, наличие objectness, степень декодирования, число классов, отсутствие sigmoid в графе или семантику85 каналов. Выход по умолчанию выбирается из build summary либо эвристикой «единственный / первый rank≥3 ndarray». В multi-output графе следует требовать точное имя и семантику каждого выхода.

Вызов runtime возвращает NumPy, далее `torch.from_numpy(pred)` и `ultralytics.utils.nms.non_max_suppression(conf=0.001,iou=0.65,max_det=300)` выполняются **после** таймера. Torch tensor создан на host, явного CUDA transfer нет. Указанные thresholds — evaluation defaults конкретного repo, не рекомендуемые product thresholds. Точная версия Ultralytics не закреплена и здесь не установлена: одних84/85 каналов недостаточно, чтобы безопасно смешивать разные YOLO heads.

После NMS код считает координаты xyxy в пикселях input canvas: x=(x-pad_x)/r, y=(y-pad_y)/r, clamp к `[0,W-1]`/`[0,H-1]`; затем переводит к COCO top-left xywh. Боксы шириной/высотой≤1 отбрасываются, class index0..79 переводится в COCO category id через COCO80_TO_91 (в id есть пропуски). Это важно для tracker/event слоя: нельзя передавать туда canvas coordinates или COCO id как непрерывный class index.

Batch helper добивает неполный batch повтором последнего изображения; декодируются лишь реальные строки metas. Файл `_b8.tpu` означает попытку исполнения fixed batch8, а не 8 независимых RTSP pipelines. Нужно сопоставить каждой строке реальные camera/frame/timestamp и исключить padded copies из результатов.

<a id="f124"></a>

### F124 — YOLOv8 пример в pinned состоянии нельзя объявлять runnable

- Исходный локатор: [W1-10-F04](_WORK/W1_10_RESULT.md), строка67; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual isolated helper/formula/AST probe: _WORK/W1_10/CONTRACT_PROBES_RESULT.json; NumPy2.4.2; no OpenCV pixel resize, SDK or device execution.

- Sources: [S049](SOURCES.md#s049); [S173](SOURCES.md#s173)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F124](RAW_FACTS.md#f124). YOLOv8 пример в pinned состоянии нельзя объявлять runnable

Тип: source_code + local_observation. [S049](SOURCES.md#s049) line206 обращается к `args.output_tens\u0e2d\u0e23\u0e4c_name`, parser определяет `output_tensor_name`. Изолированный AST probe проверил отсутствие первого атрибута у `argparse.Namespace(output_tensor_name=None)`. Если выполнение дошло до этой строки (есть program/dependencies/COCO), будет AttributeError; строка предшествует `Device.list_devices/open`. Полный скрипт не запускался и мог бы раньше упасть по отсутствующим файлам/зависимостям. Это дефект стороннего примера, не доказательство дефекта SDK.

<a id="f125"></a>

### F125 — TinyYOLO3: два принципиально разных output contracts

- Исходный локатор: [W1-10-F05](_WORK/W1_10_RESULT.md), строка71; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S053](SOURCES.md#s053), [S069](SOURCES.md#s069)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F125](RAW_FACTS.md#f125). TinyYOLO3: два принципиально разных output contracts

Тип: source_code; проверка: прочитан [S053](SOURCES.md#s053)–[S069](SOURCES.md#s069), не hardware run. Default runner: `S=416`, NHWC, RGB float32/255, batch8, input name `input_1:0`; возможны CLI `nchw`/`uint8`, но это переключатели приложения, а не доказанная поддержка любого layout/range бинарником. Название `.tpu` с `128x128` не равно размеру картинки416×416: без tensor metadata нельзя читать размеры входа из filename.

`decode_predictions` сначала пробует rank3 combined output с85 значениями/кандидат: boxes предполагаются уже decoded center-xywh, а objectness и classes — logits, к ним применяется sigmoid, score=obj×cls. Затем host class-aware `torchvision.ops.batched_nms`, inverse-letterbox и COCO mapping. Если binary уже выдаёт вероятности или нормализованные boxes, форма может пройти, но обработка будет семантически неправильной. Наличие sigmoid/диапазоны нужно сверять с graph/artifact, не угадывать по rank.

Альтернативный путь raw heads принимает rank4 NCHW/NHWC с каналами, кратными85; переводит в `[B,A,Hg,Wg,85]`, сортирует головы по grid height, использует anchors `10,14 23,27 37,58 81,82 135,169 344,319`, masks `3,4,5|0,1,2`. На host вычисляет `xy=(sigmoid(txy)+grid)*stride`, `wh=exp(twh)*anchor`, sigmoid(objectness/classes), scores, NMS, координаты. Здесь `stride=S/grid_height` используется по обеим осям: код рассчитан на квадратный вариант, не произвольную прямоугольную голову. Эти формулы доказывают реальный перенос **head decode** на host в данном пути, а не только NMS.

Выбор combined/head по размерности с перехватом исключений — адаптационная эвристика. Для результата хакатона нужен adapter с одним установленным вариантом и fail-fast при несовпадении; тихое переключение ветки может скрыть ошибку версии/выхода. Отсутствие ветки уже-NMS outputs `[B,N,6]` не означает отсутствие такой возможности у LinQ.

<a id="f126"></a>

### F126 — Auxiliary input нельзя подбирать только по имени и успешности вызова

- Исходный локатор: [W1-10-F06](_WORK/W1_10_RESULT.md), строка81; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual isolated helper/formula/AST probe: _WORK/W1_10/CONTRACT_PROBES_RESULT.json; NumPy2.4.2; no OpenCV pixel resize, SDK or device execution.

- Sources: [S053](SOURCES.md#s053); [S173](SOURCES.md#s173)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F126](RAW_FACTS.md#f126). Auxiliary input нельзя подбирать только по имени и успешности вызова

Тип: source_code + local_observation/inference; [S053](SOURCES.md#s053) funcs269,290,309,337.

Runner пробует input names с/без `:0`, introspection полей и стандартные guesses. При тексте ошибки `Missing required input tensor "..."` строит auxiliary inputs. Если имя содержит `shape`, использует H,W оригинальных изображений; размер2 → H,W **первой** картинки; размер2B → rows для каждой картинки; размер1 → S. Иные размеры дополняются нулями; non-shape inputs заполняются нулями. Не установлено, требуют ли конкретные binaries original-shape, resized-shape, canvas-shape, W,H или H,W. Успех runtime удостоверяет структурную приемлемость feed, но не правильность семантики.

В `infer_desc_dtype` substring `int8` проверяется раньше `uint8`. Локальный изолированный вызов с `{'dtype':'uint8'}` вернул `int8` (NumPy2.4.2). Это воспроизведённый helper defect, **только** для helper auto auxiliary dtype; основной explicit preprocessing uint8 использует `np.uint8` напрямую. Кроме того, значение поля `size` helper сначала интерпретирует как bytes, если кратно dtype.itemsize; без schema это неоднозначно — SDK может обозначать число элементов. Это риск адаптера, не установленный SDK bug.

<a id="f127"></a>

### F127 — Segmentation подтверждает, что «общего LinQ preprocess» нет

- Исходный локатор: [W1-10-F07](_WORK/W1_10_RESULT.md), строка89; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S070](SOURCES.md#s070)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F127](RAW_FACTS.md#f127). Segmentation подтверждает, что «общего LinQ preprocess» нет

Тип: source_code; [S070](SOURCES.md#s070). RGB PIL → bilinear **stretch** к width×height (defaults520×520), `/255`, channel normalization mean `[0.485,0.456,0.406]`, std `[0.229,0.224,0.225]`, NCHW float32. Нет letterbox. На host из logits выбирается class axis, argmax → uint8 mask, затем nearest resize до исходного H×W. Argmax-before-resize и resize-logits-before-argmax не обязаны давать один результат на границах: эталон должен повторять точный порядок. Fallback class axis=smallest dimension — эвристика, не безопасный контракт произвольного output tensor. Возвращаемая маска не содержит instance IDs или temporal identity.

<a id="f128"></a>

### F128 — Открытые показатели runner не означают RTSP throughput

- Исходный локатор: [W1-10-F08](_WORK/W1_10_RESULT.md), строка93; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S049](SOURCES.md#s049), [S053](SOURCES.md#s053), [S070](SOURCES.md#s070)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F128](RAW_FACTS.md#f128). Открытые показатели runner не означают RTSP throughput

Тип: source_code + inference. В [S049](SOURCES.md#s049) timer ограничен `run_once`; чтение файла, letterbox/batch assembly, NMS, координаты, JSON вне него. [S053](SOURCES.md#s053) и [S070](SOURCES.md#s070) устроены аналогично. Даже такое время нельзя без runtime trace назвать временем **только вычислителя**: синхронный вызов может включать driver/data transfer/host conversions. [S049](SOURCES.md#s049) принимает `.run` если существует, иначе `.sync`; семантика блокирования первого не документирована прочитанным guide, который использует sync. Следует отдельно подтвердить completion/fencing перед timing.

У warmup есть пограничный эффект: если warmup10 пересекается с batch8, второй batch целиком входит во время, но в числитель measured images идёт6. Последний padded batch может исполнять8 копий при меньшем числе реальных кадров. Это не чистый hardware throughput и не линейная оценка stream capacity. В repo `rg` по `VideoCapture|rtsp|track|avcodec|ffmpeg|gstreamer` совпадений не дал; анализировались image-dataset runners. Отрицательный результат ограничен этим checkout, не всей экосистемой.

<a id="f129"></a>

### F129 — Decode относится к конкретной конфигурации, tracking остаётся незакрытым

- Исходный локатор: [W1-10-F09](_WORK/W1_10_RESULT.md), строка99; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003), [S072](SOURCES.md#s072)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F129](RAW_FACTS.md#f129). Decode относится к конкретной конфигурации, tracking остаётся незакрытым

Тип: vendor_statement по [S003](SOURCES.md#s003); проверка: страница прочитана web. У HPS аппаратное **видеокодирование** перечислено как дополнительная ASIC-опция; это не обещание decode на LinQ H. У HX функции decoder перечислены в CPU-секции рядом с RK3588; TPU отделён. Отсюда inference: нельзя переносить эти функции на PCIe-модуль или обещанный cloud endpoint. Нужны точные product/BOM/API. В прочитанных guide/code не найден API track IDs, RTSP reconnect, ordering или rule engine.

OpenCV VideoCapture.read согласно [S072](SOURCES.md#s072) включает grab и decode. Поэтому добавление `cap.read()` в приложение добавит отдельную стоимость/буферизацию; измерение только inference не учитывает её. Это свойство API OpenCV, а не выбранный обязательный decoder. Для host MVP разумна явная цепочка `source → decode → frame metadata → preprocess → tensor inference → postprocess → per-camera tracker → rules → UI` (inference/recommendation, пока не реализация).


## W1-11 — W1-11. Производительность LinQ: что именно измерено

<a id="f130"></a>

### F130 — Актуальная vendor benchmark-таблица, а не собственный тест

- Исходный локатор: [W1-11-F01](_WORK/W1_11_RESULT.md), строка15; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement + reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F130](RAW_FACTS.md#f130). Актуальная vendor benchmark-таблица, а не собственный тест

Тип: `reported_measurement` + `vendor_statement`. Проверка: собственный сетевой TinyFish fetch прочитал PDF; web open, CLI TLS и попытка браузерного визуального просмотра не дали отрендеренную страницу. Следующая транскрипция — **извлечённый текст, визуальная верификация не выполнена**. Источник [S033](SOURCES.md#s033), p4, таблица «Производительность»; десятичные запятые сохранены.

| Сеть | Batch | HP FPS | HP latency, ms | HPQ FPS | HPQ latency, ms |
|---|---:|---:|---:|---:|---:|
| anti_spoof_mn3 | 1 | 1561,1 | 985,72 | 6244,4 | 985,72 |
| inception_v3 | 1 | 287,1 | 4,77 | 1148,4 | 4,77 |
| inception_v3 | 8 | 480,8 | - | 1923,2 | - |
| lenet5 | 1 | 12519,7 | 128,90 | 50078,8 | 128,90 |
| lenet5 | 8 | 84961,6 | - | 339846,4 | - |
| mobilenet_v2 | 1 | 1201,7 | 1,44 | 4806,8 | 1,44 |
| mobilenet_v2 | 8 | 2456,8 | - | 9827,2 | - |
| resnet152 | 1 | 228,4 | 5,34 | 913,6 | 5,34 |
| resnet50 | 1 | 432,9 | 2,99 | 1731,6 | 2,99 |
| resnet50 | 8 | 1112,8 | - | 4451,2 | - |
| ssd_mobilenet_v2 | 1 | 556,7 | 3,54 | 2226,8 | 3,54 |
| ssd_mobilenet_v2 | 8 | 428 | - | 1712 | - |
| yolo5s | 1 | 106,1 | 23,71 | 424,4 | 23,71 |
| yolov8n_pose | 1 | 104,8 | 21,51 | 419,2 | 21,51 |

Сноска связывает измерение с методикой MLCommons MLPerf и средой Intel Core i7-10700K @3.80GHz, Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43. Нет submission ID, LoadGen version/scenario, input sizes, weight hashes, calibration/quality, latency percentile, queue depth, числа активных чипов/процессов, clocks, границы I/O, decode/NMS. INT8 указан в линейке аппаратуры, но precision каждого эксперимента отдельно не раскрыт.

<a id="f131"></a>

### F131 — Внутренняя проверка чисел опровергает простые экстраполяции

- Исходный локатор: [W1-11-F02](_WORK/W1_11_RESULT.md), строка38; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F131](RAW_FACTS.md#f131). Внутренняя проверка чисел опровергает простые экстраполяции

Тип: `inference`; проверка: арифметика по [S033](SOURCES.md#s033), без железа.

- Во всех строках HPQ throughput ровно в четыре раза выше HP, а latency одинакова. Это совместимо с агрегированием независимых процессоров; не доказывает четырёхкратного ускорения одиночного запроса. Не установлено, действительно ли HPQ измерен независимо или таблица масштабирована арифметически.
- ResNet50 HP reciprocal throughput = 1000/432,9 ≈2,31ms, тогда как опубликованная latency2,99ms. HPQ reciprocal =0,578ms, опубликованная latency остаётся2,99ms. YOLO5s HP reciprocal ≈9,43ms против23,71ms. Значит, FPS и latency не описывают один последовательный цикл одинаковым способом. Возможны разные сценарии, overlap, очереди, percentile; конкретный механизм неизвестен.
- Пара значений anti_spoof/lenet выглядит необычно при заголовке ms. Нельзя молча делить эти latency на1000 или объявлять опечаткой: микросекунды/ошибка извлечения/исходная ошибка/другой знаменатель — только гипотезы. Браузерная попытка не смогла отрендерить PDF и повторила extract; это **не независимое визуальное подтверждение**.
- Batch8 для SSD MobileNetV2 даёт меньший FPS, чем batch1. Нельзя обещать рост от batching вообще. У batch8 не опубликована latency, поэтому выигрыш throughput ResNet не означает улучшения реакции камеры.
- p3 той же презентации имеет другие округлённые ResNet50 HP значения460/1046FPS при batch1/8, p4 —432,9/1112,8. У p3 нет сопоставимого полного протокола. Это разные показатели внутри документа, не доказательство регрессии SDK.

<a id="f132"></a>

### F132 — HPS, карта и чип — разные уровни

- Исходный локатор: [W1-11-F03](_WORK/W1_11_RESULT.md), строка48; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation + vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003), [S002](SOURCES.md#s002), [S026](SOURCES.md#s026), [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F132](RAW_FACTS.md#f132). HPS, карта и чип — разные уровни

Тип: `vendor_statement`/`primary_documentation`; проверка: web прочитал [S003](SOURCES.md#s003)/[S002](SOURCES.md#s002)/[S026](SOURCES.md#s026), собственный fetch [S033](SOURCES.md#s033).

На /tech LinQ H имеет24INT8 TOPS, SRAM16MB и двухканальный DDR4+ECC controller. /sol описывает HPQ на четырёх LinQ H,96TOPS. HPS datasheet задаёт3U node,960INT8 TOPS,640GB DDR4 ECC,2×PCIe×16 Gen4; ResNet50 batch1~2,3ms и потенциальные1,5ms. INT8 основной, FP16/BFloat16 названы перспективой. Дополнительное аппаратное video-codec оборудование опционально. В p3 презентации колонка HPS не содержит ResNet50 FPS; p8 объединяет40+ моделей; p9 HPC объединяет два HPS и server,1920TOPS,100+ моделей.

Инженерный вывод: суммарная память640GB не доказывает, что одна программа видит непрерывное640GB пространство или компилятор автоматически разбивает одну модель между всеми процессорами. Число одновременно размещаемых/исполняемых моделей не равно числу камер, частоте запросов или deadline. Опция codec не подтверждает, что штатная карта сама декодирует RTSP. Не присваивать облачному участнику весь HPS/HPC без идентификации выделенных устройств и contention.

<a id="f133"></a>

### F133 — Guide документирует влияние компиляции и TLM, не end-to-end benchmark

- Исходный локатор: [W1-11-F04](_WORK/W1_11_RESULT.md), строка56; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F133](RAW_FACTS.md#f133). Guide документирует влияние компиляции и TLM, не end-to-end benchmark

Тип: `primary_documentation`. Проверка: чтение сохранённого соседней веткой текста публичного guide [S030](SOURCES.md#s030); не выполнен локальный fetch оригинала и не запускался код.

Guide2025 RU.РМДВ.04.06.014-03 34 01, §3.2/p9–10: DEFAULT и STAGING, параллелизм pipeline, второй DDR, placement/cache и fusion. Для STAGING прямо оговорены возможная длительная компиляция и неверные программы, fallback DEFAULT. §3.3/p17 выводит `execution_time_us` как оценку TLM. §3.1 задаёт batch при построении графа; §3.3/p16 отмечает batch-sensitive quantized graph. Значит, время simulator/TLM нельзя представлять измерением runtime; preset и batch — обязательные параметры протокола. Версии хоста2025 (Ubuntu20.04/Python3.11/RAM≥32GB) не совпадают с benchmark environment2026; нет основания устанавливать одно окружение как универсальное.

<a id="f134"></a>

### F134 — Публичный авторский repo даёт три разных знаменателя скорости

- Исходный локатор: [W1-11-F05](_WORK/W1_11_RESULT.md), строка62; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S073](SOURCES.md#s073), [S049](SOURCES.md#s049)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F134](RAW_FACTS.md#f134). Публичный авторский repo даёт три разных знаменателя скорости

Тип: `source_code`. Проверка: прочитан pinned source [S073](SOURCES.md#s073)–[S049](SOURCES.md#s049) локального clone, [S073](SOURCES.md#s073) также открыт сетевым web; inference не запускался. Commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`.

1. `run_resnet50_performance.py:44–146`: wrapper вызывает `mlperf -s offline -m performance -p ... -q ...`, default QPS500 для batch1 и1000 дляbatch8,3runs. Берёт `Samples per second`, проверяет `Result is: VALID`. QPS — requested workload parameter, не измеренный FPS. Код не публикует сам результат; .tpu и vendor mlperf binary нужны отдельно. Наличие mlperf в названии файла не делает запуск официальной submission.
2. `run_resnet50_parallel_direct.py:201–314`: отдельный subprocess на explicit device/shard; `effective_fps = total / wall_sec`, таймер до Popen и до завершения всех процессов. Это включает startup/import/data/model-load/accuracy/output work. `shards[].throughput_img_per_sec` использует иной внутренний знаменатель, поэтому их сумму нельзя непосредственно сравнивать с aggregate effective_fps.
3. `run_yolov8_tpu.py:269–334`: таймер только вокруг `run_once`; imread/letterbox/BGR→RGB/float normalization/batching выполняются до, NMS/box mapping/predictions JSON после. FPS в summary =measured_images / infer_time, не скорость pipeline. warmup10images; частично пересекающая warmup batch учитывает полное batch-время при частичном числителе, последний batch может padding. Нет распределения individual latency. Вариант `inference.run`/`sync` выбирается по наличию атрибута; семантика полного завершения ветки run не доказана.

<a id="f135"></a>

### F135 — Подтверждённая локальная проверка ошибки примера

- Исходный локатор: [W1-11-F06](_WORK/W1_11_RESULT.md), строка70; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual AST/isolated helper check; no full runner/model/device execution.

- Sources: [S033](SOURCES.md#s033), [S003](SOURCES.md#s003), [S002](SOURCES.md#s002), [S026](SOURCES.md#s026), [S030](SOURCES.md#s030), [S073](SOURCES.md#s073), [S074](SOURCES.md#s074), [S049](SOURCES.md#s049), [S063](SOURCES.md#s063), [S075](SOURCES.md#s075), [S017](SOURCES.md#s017), [S076](SOURCES.md#s076), [S077](SOURCES.md#s077), [S078](SOURCES.md#s078), [S037](SOURCES.md#s037)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F135](RAW_FACTS.md#f135). Подтверждённая локальная проверка ошибки примера

Тип: `source_code` + `local_observation`. Проверка: AST нашёл `args.output_tensอร์_name`; parser объявляет `--output-tensor-name`. Минимальный `argparse.Namespace(output_tensor_name='out')` с getattr на фактическую Unicode-строку дал AttributeError. Артефакт `_WORK/W1_11/STATIC_CHECK.json`. В source обращение происходит до Device.list_devices/open. Полный скрипт не запускался: он может ранее остановиться на missing files/dependencies. Это дефект стороннего примера, не обнаруженная ошибка LinQ SDK. Не называть repo готовым воспроизводимым benchmark без исправления и реального TPU-run.

<a id="f136"></a>

### F136 — Историческая Python binding помогает определить границу API-time

- Исходный локатор: [W1-11-F07](_WORK/W1_11_RESULT.md), строка74; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S063](SOURCES.md#s063)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F136](RAW_FACTS.md#f136). Историческая Python binding помогает определить границу API-time

Тип: `source_code`. Проверка: прочитан [S063](SOURCES.md#s063) из сохранённого source pytpu15.0.24, runtime не загружался. `_bindings.py:387–416` sync резервирует I/O buffers, подготавливает pointers, вызывает native run, получает NumPy output и проверяет status. Следовательно даже sync wall-time этого кода шире device compute. README той поставки описывает старый iva_tpu interface и timings/stats; в фактическом `_bindings.py` соответствующих методов timings/stats нет. Не обещать доступность profiler/stat fields по README и не переносить ABI2023 на Runtime2026. Source предлагает повторно использовать inference session, поэтому создание model/session на каждый кадр исказит steady-state тест.

<a id="f137"></a>

### F137 — Настоящие исторические MLPerf logs и условия (существенная новая ветка)

- Исходный локатор: [W1-11-F08](_WORK/W1_11_RESULT.md), строка78; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation + reported_measurement + source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S075](SOURCES.md#s075)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F137](RAW_FACTS.md#f137). Настоящие исторические MLPerf logs и условия (существенная новая ветка)

Тип: `reported_measurement` + `source_code` + `primary_documentation`. Проверка: выполнены независимый web search, GitHub API tree и HTTP чтение оригинальных файлов [S075](SOURCES.md#s075); файлы сохранены в `_WORK/W1_11/MLPERF_2020`. Это **чужой состоявшийся тест**, не наш запуск.

Closed/IVATech, `iva-fpga-1`, statusRDI/edge; AlveoU200,250MHz,1accelerator, i7-7700K4.20GHz,16GBhostRAM,Ubuntu18.04,TF1.15.0. Measurements JSON: inputINT8,weightsINT8/FP16,quantization без retraining, исходные веса `https://zenodo.org/record/2535873/files/resnet50_v1.pb`. Code QSL готовит shape[1,224,224,3], preprocessing до query. SingleStream run1 VALID: p90=12,230138ms,mean12,081844ms,p99=12,345478ms,max14,198754ms,QPS incl overhead82,37; samples/query1,max_async1. Offline run1 VALID:88,8239samples/s, samples/query24576, aggregate query276,682437431s; один logging-allocation warning, ошибок нет. Accuracy75,756%,50000images.

Разницы файлов тоже существенны: system JSON называет libtpu7.1.15/compiler13.1.0; README перечисляет libtpu7.1.17/compiler14.0.0. QSL source возвращает PerformanceSampleCount10, log фиксирует1024. Это запрещает утверждать, что сегодняшняя копия всех source-файлов побайтно описывает использованный бинарник. Исторические условия всё равно намного прозрачнее современного слайда. Подробности и exact locators в реестре ниже.

Инженерный вывод: Offline aggregate latency276секунд означает длительность большого query, а не задержку одного кадра276секунд. Точно так же inverse88,8239FPS не заменяет p90 single-stream12,23ms. Это первичный конкретный контрпример смешению знаменателей. Подмена этой FPGA современным24TOPS ASIC или линейное умножение результата по частоте некорректны.

<a id="f138"></a>

### F138 — Авторские эксперименты2025 сообщают ограничения оптимизации

- Исходный локатор: [W1-11-F09](_WORK/W1_11_RESULT.md), строка88; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S017](SOURCES.md#s017), [S076](SOURCES.md#s076)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F138](RAW_FACTS.md#f138). Авторские эксперименты2025 сообщают ограничения оптимизации

Тип: `reported_measurement`. Проверка: сетевое чтение первичной статьи [S017](SOURCES.md#s017), [S076](SOURCES.md#s076) целиком; linked таблица cloud.mail.ru вернула404, поэтому её чисел не видел. Авторы Сергей Нефёдов, Руслан Качмазов, Лев Бабинцев, мастерская ВШЭ/VK. Статья30.03.2025 от аккаунта fivanov. Для IVA TPU описаны режим с предварительно загруженными данными и последовательный latency, batch1/2/4/8, проблемы compile/run некоторых STAGING-вариантов. Нет пригодной полной фиксации board/runtime/model hashes/input/quality для переноса на2026.

Авторы оценивают arithmetic throughput вручную через операции×FPS и называют floating-point производительностью; это не следует автоматически интерпретировать как физически выполненные FLOPS, INT8 TOPS или измеренные performance counters. Числа утилизации из статьи не дают коэффициент пересчёта для нашего решения. Их сообщение о remote GUI является историческим авторским опытом, не подтверждением доступа участников2026.

<a id="f139"></a>

### F139 — Университетская работа2026 — зацепка, но full protocol недоступен

- Исходный локатор: [W1-11-F10](_WORK/W1_11_RESULT.md), строка94; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S077](SOURCES.md#s077)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F139](RAW_FACTS.md#f139). Университетская работа2026 — зацепка, но full protocol недоступен

Тип: `reported_measurement` на уровне авторской аннотации. Проверка: web прочитал metadata [S077](SOURCES.md#s077); повторные web/TinyFish/CLI запросы нестабильны. Полный текст не прочитан. Магистерская ВКР Рудь Иван Васильевич, СПбПУ, 2026, визуальная локализация БПЛА/LinQ H. Аннотация перечисляет ResNet34 — 443 FPS; ResNet50 — 430 FPS; MobileNetV2 — 142 FPS; YOLO11l OBB — 20 FPS. Таблица прав: Internet full text — авторизованные пользователи СПбПУ, анонимные без действия чтения. Shape/batch/runtime/precision/denominator не установлены; возможна несопоставимость моделей и сценариев. Особенно MobileNetV2: 142 против 1201,7 FPS на vendor slide — повод выяснять условия, а не объявлять ошибочным один источник.


## W1-12 — W1-12 — диагностика, версии, совместимость и восстановление

<a id="f140"></a>

### F140 — Guide2025 §2 требует Ubuntu20.04, RAM≥32GB, Python3.11; локальный wheel `tpu_framework-py3-none-any.whl`; проверка установки через `import tpu_framework` и exit0. Это проверка Pyth

- Исходный локатор: [W1-12-F01](_WORK/W1_12_RESULT.md), строка19; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| [F140](RAW_FACTS.md#f140) | Guide2025 §2 требует Ubuntu20.04, RAM≥32GB, Python3.11; локальный wheel `tpu_framework-py3-none-any.whl`; проверка установки через `import tpu_framework` и exit0. Это проверка Python framework, не обнаружение устройства. | primary_documentation | Прочитан сохранённый полный extraction и заново получен официальный PDF через TinyFish; установка не выполнена | [S030](SOURCES.md#s030) |

<a id="f141"></a>

### F141 — Guide2025 §3.2 различает DEFAULT/STAGING. STAGING может давать недопустимые программы или чрезмерно долгую компиляцию; документ предлагает вернуться к DEFAULT и отправить bug repor

- Исходный локатор: [W1-12-F02](_WORK/W1_12_RESULT.md), строка20; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| [F141](RAW_FACTS.md#f141) | Guide2025 §3.2 различает DEFAULT/STAGING. STAGING может давать недопустимые программы или чрезмерно долгую компиляцию; документ предлагает вернуться к DEFAULT и отправить bug report. Упоминание DISABLED в следующем абзаце не задаёт здесь отдельную проверенную современную CLI-команду. | primary_documentation | Текст прочитан; compiler не запускался | [S030](SOURCES.md#s030), printed p10 |

<a id="f142"></a>

### F142 — Guide2025 §4 помещает TensorFlow deprecation warning в пример штатного logging; наличие/отсутствие отладочного вывода допускается. Warning касается `Zeros.__init__` и аргумента `dt

- Исходный локатор: [W1-12-F03](_WORK/W1_12_RESULT.md), строка21; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| [F142](RAW_FACTS.md#f142) | Guide2025 §4 помещает TensorFlow deprecation warning в пример штатного logging; наличие/отсутствие отладочного вывода допускается. Warning касается `Zeros.__init__` и аргумента `dtype`, не является сообщением о неподдерживаемой TPU operation. | primary_documentation | Прочитан полный контекст, включая продолжение p24 | [S030](SOURCES.md#s030), printed p23–24 |

<a id="f143"></a>

### F143 — Презентация2026 слайд4: Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43, i7-10700K в условиях заявленного измерения.

- Исходный локатор: [W1-12-F04](_WORK/W1_12_RESULT.md), строка22; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| [F143](RAW_FACTS.md#f143) | Презентация2026 слайд4: Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43, i7-10700K в условиях заявленного измерения. | reported_measurement (только среда) | Заново прочитано через TinyFish, собственного benchmark нет | [S033](SOURCES.md#s033) |

<a id="f144"></a>

### F144 — PyPI version15.0.24 опубликована 2023-11-27T09:41:37.939987Z, author IVA-Tech, Python≥3.6; sdist SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`. README п

- Исходный локатор: [W1-12-F05](_WORK/W1_12_RESULT.md), строка23; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation + source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S079](SOURCES.md#s079), [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| [F144](RAW_FACTS.md#f144) | PyPI version15.0.24 опубликована 2023-11-27T09:41:37.939987Z, author IVA-Tech, Python≥3.6; sdist SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`. README показывает `iva_tpu.TPUDevice`, фактический package экспортирует `Device`, `Program`, `Inference`, `InferenceError`. | primary_documentation / source_code | Открыт PyPI JSON, прочитаны локальные setup/init/bindings; sdist заново не устанавливался | [S079](SOURCES.md#s079)/[S065](SOURCES.md#s065) |

<a id="f145"></a>

### F145 — pytpu15.0.24 lazy-load `/usr/lib/libtpu.2.so` через ctypes.CDLL при первом обращении к binder; простой import не проверяет наличие .so, её symbols, driver или hardware. `Device.lis

- Исходный локатор: [W1-12-F06](_WORK/W1_12_RESULT.md), строка24; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| [F145](RAW_FACTS.md#f145) | pytpu15.0.24 lazy-load `/usr/lib/libtpu.2.so` через ctypes.CDLL при первом обращении к binder; простой import не проверяет наличие .so, её symbols, driver или hardware. `Device.list_devices()` только фильтрует имена файлов `/dev`, а не открывает/проверяет TPU. | source_code | Прочитан `_bindings.py:28–51,185–206`; hardware нет | [S065](SOURCES.md#s065) |

<a id="f146"></a>

### F146 — В старом binding есть отдельные init, valid-device, program, load, run-inference и inference-status error paths. Runtime message извлекается отдельными C API; таблицы значений stat

- Исходный локатор: [W1-12-F07](_WORK/W1_12_RESULT.md), строка25; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| [F146](RAW_FACTS.md#f146) | В старом binding есть отдельные init, valid-device, program, load, run-inference и inference-status error paths. Runtime message извлекается отдельными C API; таблицы значений status/init codes в sdist не найдено. | source_code / unknown | Прочитаны ветви, ни одна не вызвана на runtime | [S065](SOURCES.md#s065) |

<a id="f147"></a>

### F147 — `test_HW_params_mismatch` использует `device.info()['axi_word_len']` и намеренно другой DDR/cache target, ожидая ValueError. Это подтверждает, что авторы тестируют аппаратную совме

- Исходный локатор: [W1-12-F08](_WORK/W1_12_RESULT.md), строка26; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| [F147](RAW_FACTS.md#f147) | `test_HW_params_mismatch` использует `device.info()['axi_word_len']` и намеренно другой DDR/cache target, ожидая ValueError. Это подтверждает, что авторы тестируют аппаратную совместимость .tpu, но не задаёт совместимость compiler/runtime release. | source_code | Только inspection теста; test data/runtime нет | [S065](SOURCES.md#s065) |

<a id="f148"></a>

### F148 — Старые generator context managers open/load/inference/buffer освобождают handles после yield без try/finally. При exception в теле with код после yield не гарантирован. Есть TODO о

- Исходный локатор: [W1-12-F09](_WORK/W1_12_RESULT.md), строка27; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| [F148](RAW_FACTS.md#f148) | Старые generator context managers open/load/inference/buffer освобождают handles после yield без try/finally. При exception в теле with код после yield не гарантирован. Есть TODO о нестабильности destroy tensor buffer с ссылкой TPU2-2010. | source_code + inference о Python control flow | Source inspection; утечка на устройстве не измерялась | [S065](SOURCES.md#s065),185–253,306–322 |

<a id="f149"></a>

### F149 — `test_watchdog_error.py` помечен skip; причина говорит о mem collision и нарушении работы device/других tests. В тесте есть старые закомментированные API и TODO.

- Исходный локатор: [W1-12-F10](_WORK/W1_12_RESULT.md), строка28; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| [F149](RAW_FACTS.md#f149) | `test_watchdog_error.py` помечен skip; причина говорит о mem collision и нарушении работы device/других tests. В тесте есть старые закомментированные API и TODO. | source_code | Прочитан; опасный тест не запускался | [S065](SOURCES.md#s065) |

<a id="f150"></a>

### F150 — Pinned third-party YOLOv8 runner объявляет `--output-tensor-name`, затем обращается к `args.output_tensอร์_name` до list_devices/open. Это дефект примера.

- Исходный локатор: [W1-12-F11](_WORK/W1_12_RESULT.md), строка29; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual AST/argparse.Namespace identifier check; no full runner/SDK/device.

- Sources: [S049](SOURCES.md#s049)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| [F150](RAW_FACTS.md#f150) | Pinned third-party YOLOv8 runner объявляет `--output-tensor-name`, затем обращается к `args.output_tensอร์_name` до list_devices/open. Это дефект примера. | source_code + local_observation | AST и отдельный Namespace lookup воспроизвели AttributeError, полный runner не запускался | [S049](SOURCES.md#s049); auxiliary CHECK_EXAMPLE_ATTRIBUTE.py |

<a id="f151"></a>

### F151 — Страница issues стороннего repo при проверке показала Open0 и отсутствие результатов текущего фильтра. Releases — без релизов. Это не официальный SDK tracker и не доказательство от

- Исходный локатор: [W1-12-F12](_WORK/W1_12_RESULT.md), строка30; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S080](SOURCES.md#s080), [S081](SOURCES.md#s081)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| [F151](RAW_FACTS.md#f151) | Страница issues стороннего repo при проверке показала Open0 и отсутствие результатов текущего фильтра. Releases — без релизов. Это не официальный SDK tracker и не доказательство отсутствия closed issues/внутренних исправлений. | local_observation | Сетевые страницы открыты | [S080](SOURCES.md#s080)/[S081](SOURCES.md#s081) |

<a id="f152"></a>

### F152 — Точные диагностические сообщения и их владельцы

- Исходный локатор: [W1-12-MATRIX-6](_WORK/W1_12_RESULT.md), строка32; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065), [S049](SOURCES.md#s049)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Точные диагностические сообщения и их владельцы

Следующие шаблоны взяты из локально прочитанного sdist15.0.24 ([S065](SOURCES.md#s065)); переменные внутри фигурных скобок — фактические значения/сообщение C runtime, которого у нас нет. Не выдавать их за фактически полученный лог.

| Где | Python исключение / шаблон | Что действительно известно | Первое действие |
|---|---|---|---|
| Device.__init__, line218 | ValueError: `Invalid init code {init_code}: {message}` | C init вернул ненулевой код; расшифровка кода отсутствует | Сохранить полный message, версии .so/driver и node; vendor support |
| Device.__init__,221 | ValueError: `Invalid device: {message}` | После init проверка valid-device не прошла | Проверить node/access и штатный vendor sample; не считать автоматически PCIe failure |
| Program.__init__,285 | ValueError: `Invalid program: {message}` | C program validation не прошла | Проверить путь, hash, target/compiled metadata и версию toolchain |
| Device.load,250 | ValueError с device error message | Ошибка после load_program; Python не предоставляет отдельного классификатора | Сохранить точный C message, не заменять общим «нет TPU» |
| Inference._run,382 | InferenceError: `Invalid tpu_run_inference return code {status_code}: {message}` | Ненулевой результат C вызова запуска | Проверить штатную программу и input contract, прекратить resolver retries |
| Inference._check_status,422 | InferenceError: `Invalid inference status code {status_code}: {message}` | После sync status ненулевой | Отличать от ошибки initial run; собирать оба кода |
| Inference._load_inference,431 | ValueError: `Input data must be a mapping, got:{type}` | Host API получил не Mapping | Исправить input container до обращения за driver recovery |

Чистый Python layer также проверяет строковые типы dev/program path; lookup неизвестного tensor_name может дать KeyError, output reshape — обычную ошибку NumPy. Это не автоматически failure аппаратуры. В этом исходнике нет полноценной проверки shape/dtype входа перед передачей указателя: `_load_inference` берёт `tensor_data.ctypes.data_as(...)`; комментарий TODO прямо оставляет validation. Поэтому отсутствие раннего ValueError не доказывает правильность входа. Проверять shape, dtype, byte count и contiguous layout на стороне приложения необходимо до запуска; требования точного нового API получить у инженера.

Наличие `/dev/tpu0` и успешный `import pytpu` по отдельности не доказывают execution. В старом source list_devices фильтр `tpu.`/длина4 даже не является общим надёжным перечислением произвольного количества устройств.

### Сторонний runner: не путать с SDK

[S049](SOURCES.md#s049) имеет собственные ошибки для отсутствующего program file, dependencies, устройства, разрешения tensor names, формы prediction и чтения изображения. Они созданы Python-примером. Общий wrapper dependencies способен скрыть первопричину import error — нужен chained traceback. Resolver перебирает имена, ловит все Exception и оставляет лишь часть sample errors: ошибка устройства может выглядеть как неправильное имя тензора.

Локальная мини-проверка воспроизвела только lookup несуществующего Namespace attribute; она не доказывает runnable весь repo. Условия достижения дефекта: файл .tpu существует, imports и чтение COCO уже прошли. Если любое из них ломается раньше, пользователь увидит более раннюю ошибку. Рекомендуемый учебный patch — исправить имя на `output_tensor_name`, сохранить отдельный diff/commit; в этой research-ветке исходник repo не редактировался.

### TensorFlow warning и build warning

Guide2025 показывает deprecation `dtype` в TensorFlow initializer. Это warning host-компонента квантования, а не documented LinQ inference error. Проверять результат этапа и exit code; не скрывать все warnings глобально. Python3.8 в пути логов не доказывает, что требование Python3.11 ошибочно: возможен исторический пример. Точная dependency matrix остаётся вопросом.

В setup.py старого sdist условие VERSION==15.0.24 порождает предупреждение Invalid package version при сборке. Литерал совпадает с опубликованной версией: это артефакт build script/source, не признак повреждённого runtime или доказательство ложной версии PyPI. Ничего не переименовывать самостоятельно ради подавления warning.


## W1-13 — W1-13 — публичная экосистема, происхождение и поставка LinQ SDK

<a id="f153"></a>

### F153 — OEM и контролируемая загрузка.

- Исходный локатор: [W1-13-F01](_WORK/W1_13_RESULT.md), строка36; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F153](RAW_FACTS.md#f153) — OEM и контролируемая загрузка.** Тип `vendor_statement`; проверка: web прочитан `/sol`, строки273–293. Поставщик описывает преобразование графов в инструкции LinQ H, Python3.8 API/CLI и ПО под историческим названием «Фреймворк для работы тензорного процессора IVA H1…» как часть OEM на LinQ H. Раздел загрузки требует регистрации и верификации. Это подтверждает связь продуктов и модель получения, но не текущую версию wheel, конкретную лицензию SDK или API2026. [[S003](SOURCES.md#s003)]

<a id="f154"></a>

### F154 — подтверждённый maintainer graph.

- Исходный локатор: [W1-13-F02](_WORK/W1_13_RESULT.md), строка38; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S083](SOURCES.md#s083)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F154](RAW_FACTS.md#f154) — подтверждённый maintainer graph.** Тип `primary_documentation`; проверка: страница PyPI maintainer прочитана. `IvaTechnologies`, display name `IVA Technologies`, joined2020-04-15, имеет четыре публичных проекта, перечисленных в карте. Это атрибуция аккаунта/метаданных и исторического семейства, не доказательство юридической тождественности всех нынешних брендов и не поддержка текущего ABI. [[S083](SOURCES.md#s083)]

<a id="f155"></a>

### F155 — `pytpu15.0.24` доступен, но историчен.

- Исходный локатор: [W1-13-F03](_WORK/W1_13_RESULT.md), строка40; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S064](SOURCES.md#s064), [S084](SOURCES.md#s084), [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F155](RAW_FACTS.md#f155) — `pytpu15.0.24` доступен, но историчен.** Тип `primary_documentation`; проверка: JSON получен HTTP200, sdist независимо скачан и SHA256 проверен. Upload `2023-11-27T09:41:37.939987Z`, 19,201 bytes, SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`. Author `IVA-Tech`, email `info@iva-tech.ru`, Python `>=3.6`, homepage старого SDK. В JSON это latest `15.0.24`, а не Runtime16.18.6 из презентации2026. [[S064](SOURCES.md#s064), [S084](SOURCES.md#s084),[S065](SOURCES.md#s065)]

<a id="f156"></a>

### F156 — `pytpu` не поставляет runtime/compiler.

- Исходный локатор: [W1-13-F04](_WORK/W1_13_RESULT.md), строка42; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F156](RAW_FACTS.md#f156) — `pytpu` не поставляет runtime/compiler.** Тип `source_code`; проверка: sdist распакован/прочитан. `setup.py` install_requires только `numpy`; extras test содержит `tpu-tlm-is~=0.3.0.1`. `_bindings.py` lazy-load `/usr/lib/libtpu.2.so`. Отсутствие install dependency на native runtime не означает его ненужность: он ожидается на уровне Linux/system installation. Сам native binary в архиве отсутствует. [[S065](SOURCES.md#s065)]

<a id="f157"></a>

### F157 — публичный sdist не содержит объявленные CLI targets.

- Исходный локатор: [W1-13-F05](_WORK/W1_13_RESULT.md), строка44; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F157](RAW_FACTS.md#f157) — публичный sdist не содержит объявленные CLI targets.** Тип `source_code` + `local_observation`; проверка: полный список членов скачанного tar, без установки. `setup.py` объявляет `run_get_fps = pytpu.scripts.run_get_fps:main` и `pyrun_tpu = pytpu.scripts.pyrun_tpu_cli:main`, но ни одного `pytpu/scripts` в sdist нет. Ожидается, что такие entrypoints из этого артефакта не смогут загрузить target module без внешнего добавления; сам CLI не запускался. Это дефект/неполнота конкретного публичного архива, не доказанная ошибка vendor package2026. [[S065](SOURCES.md#s065)]

<a id="f158"></a>

### F158 — лицензию bindings нельзя восстановить по публичности.

- Исходный локатор: [W1-13-F06](_WORK/W1_13_RESULT.md), строка46; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065), [S087](SOURCES.md#s087)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F158](RAW_FACTS.md#f158) — лицензию bindings нельзя восстановить по публичности.** Тип `source_code`; проверка: manifest/metadata прочитаны. У `pytpu15.0.24` `License: UNKNOWN`, JSON license пуст, LICENSE-файла в sdist нет. То же неизвестное поле у `iva-tpu11.2.6`; лицензия всего SDK не установлена. Не присваивать им MIT по аналогии с соседним пакетом. [[S065](SOURCES.md#s065),[S087](SOURCES.md#s087)]

<a id="f159"></a>

### F159 — README и код `pytpu` отражают разные API-поколения.

- Исходный локатор: [W1-13-F07](_WORK/W1_13_RESULT.md), строка48; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F159](RAW_FACTS.md#f159) — README и код `pytpu` отражают разные API-поколения.** Тип `source_code`; проверка: README/setup/package прочитаны. README использует `from iva_tpu import TPUDevice, TPUProgram, TPUInference`, тогда как архив имеет пакет `pytpu` с новым `Device` API (подробности у W1-09). Это не безопасный copy-paste quickstart. Комментарий `_bindings.py:321` содержит `https://jira.hi-tech.org/browse/TPU2-2010`, добавляя след происхождения, но сам issue недоступен. [[S065](SOURCES.md#s065)]

<a id="f160"></a>

### F160 — `iva-tpu11.2.6` — loader, не binary distribution.

- Исходный локатор: [W1-13-F08](_WORK/W1_13_RESULT.md), строка50; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S085](SOURCES.md#s085), [S086](SOURCES.md#s086), [S087](SOURCES.md#s087)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F160](RAW_FACTS.md#f160) — `iva-tpu11.2.6` — loader, не binary distribution.** Тип `source_code`; проверка: sdist скачан, SHA256 проверен, `src/iva_tpu/__init__.py` прочитан. Код `importlib.util.spec_from_file_location("libtpu", "/usr/lib/libtpu.so")`, затем `module_from_spec` и `sys.modules["iva_tpu"] = libtpu`. Archive 2,238 bytes; SHA256 `885cb9ef75a87fb83dcf988d8e8664477a4bccca5f058feaede2130dc94a63ff`. Native extension не включён. Author `Maxim Moroz`, `m.moroz@iva-tech.ru`, тот же SDK homepage; numpy>=1.14/Python>=3.6. [[S085](SOURCES.md#s085), [S086](SOURCES.md#s086),[S087](SOURCES.md#s087)]

<a id="f161"></a>

### F161 — есть публичный helper model package с реальной лицензией.

- Исходный локатор: [W1-13-F09](_WORK/W1_13_RESULT.md), строка52; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S088](SOURCES.md#s088), [S089](SOURCES.md#s089), [S090](SOURCES.md#s090)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F161](RAW_FACTS.md#f161) — есть публичный helper model package с реальной лицензией.** Тип `source_code`; проверка: `iva_applications-11.0.1.tar.gz` скачан, SHA256 `f04be1de75b8a7b22bd835c424fb61cd27f3e179356b7b4edc13f03f470f6b68` проверен. Author `IVA Technologies`, `engineering@iva-tech.ru`; maintainers `a.zolotarev` и `IvaTechnologies`. В архиве LICENSE содержит стандартный MIT-текст, Copyright2020 IVA Technologies, хотя metadata license UNKNOWN. Лицензионный файл сильнее пустого/неполного классификатора; это относится к этому helper package, не автоматически к моделям, весам и всему SDK. [[S088](SOURCES.md#s088), [S089](SOURCES.md#s089),[S090](SOURCES.md#s090)]

<a id="f162"></a>

### F162 — helpers не равны Model Zoo/сертифицированной модели.

- Исходный локатор: [W1-13-F10](_WORK/W1_13_RESULT.md), строка54; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S090](SOURCES.md#s090)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F162](RAW_FACTS.md#f162) — helpers не равны Model Zoo/сертифицированной модели.** Тип `source_code`; проверка: tree/исходники просмотрены. В `iva-applications` есть `tiny_yolo2`, `tiny_yolo3`, `yolo2`, `yolo3`, `yolo4`, `ssd_mobilenet`, `rfdnet`, `resnet50`, `unet`, `bert_large`, `gpt2` и др.; распределение pre/post/calibration неодинаково. TinyYOLO3 package имеет host postprocess; нет supplied .tpu/.qm/weights, современного compiler или матрицы compatibility. Наличие имени GPT2/YOLO4 не доказывает, что текущий LinQ аппаратно поддерживает выбранную произвольную конфигурацию. Это полезный исторический первичный код для model_stack/данных. [[S090](SOURCES.md#s090)]

<a id="f163"></a>

### F163 — helpers жёстко привязаны к старому окружению.

- Исходный локатор: [W1-13-F11](_WORK/W1_13_RESULT.md), строка56; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S090](SOURCES.md#s090)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F163](RAW_FACTS.md#f163) — helpers жёстко привязаны к старому окружению.** Тип `source_code`; проверка: setup/metadata прочитаны. Base deps включают `scipy==1.4.1`, `keras==2.2.4`, matplotlib/Pillow/scikit-build/opencv-python/scikit-image/pydrive/pandas/transformers/sentencepiece. Extras: `tensorflow==2.4.1`, `transformers==4.5.1`, `pytpu==13.0.6`. `utils/tpu_runner.py` импортирует `TPUDevice, TPUProgram, TPUProgramInfo, TPUInference` из `pytpu`; поэтому «latest helpers + latest bindings» не является доказанно согласованным стеком. В современное Python3.11 environment механически устанавливать этот набор рискованно; реального resolver/install теста здесь нет. [[S090](SOURCES.md#s090)]

<a id="f164"></a>

### F164 — classifier demo представляет исторический UI и host/TPU развилку.

- Исходный локатор: [W1-13-F12](_WORK/W1_13_RESULT.md), строка58; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S091](SOURCES.md#s091), [S092](SOURCES.md#s092)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F164](RAW_FACTS.md#f164) — classifier demo представляет исторический UI и host/TPU развилку.** Тип `source_code`; проверка: PyPI JSON/sdist получены, SHA256 `aeaf3436a861da50af92cc1738a6356b7d533de0dbe99609655d9d6082c18c78` проверен. `iva-classification-demo1.1.0`, author `Alexeev Eugene`, `e.alekseev@iva-tech.ru`; depends TF1.15.0/Keras2.2.4/PyQt5/iva-applications/iva-tpu. `class_computer.py` выбирает TFRunnerDict при local flag и TPURunner иначе. Это исходный пример возможной границы UI/host execution, не текущий remote-access protocol LinQ и не пример контроля промышленной безопасности. [[S091](SOURCES.md#s091), [S092](SOURCES.md#s092)]

<a id="f165"></a>

### F165 — сторонний repo2026 не является SDK.

- Исходный локатор: [W1-13-F13](_WORK/W1_13_RESULT.md), строка60; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S093](SOURCES.md#s093), [S044](SOURCES.md#s044)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F165](RAW_FACTS.md#f165) — сторонний repo2026 не является SDK.** Тип `source_code`; проверка: текущая GitHub page/API прочитаны, локальный clone соседней ветки исследован на commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`, date `2026-04-03T12:44:54+07:00`, author `sherstpasha`. GitHub API license null, releases=[], tags=[]; в tracked tree LICENSE не найден. `requirements.txt`: numpy1.26.4, onnx~=1.16.0, onnxruntime~=1.18.0, tensorflow2.14.1, setuptools<81, torch/torchvision и др.; SDK/ultralytics не включены. `RUN_SCENARIO.txt` явно ожидает отдельное TPU-env с libtpu/tpu-dkms/pytpu/tpu_framework/mlperf. Внешний `mlperf-16.16.12-Source/build/mlperf` и vendor .tpu лежат в авторских `/home/smallpc_user/...`, не в repo. [[S093](SOURCES.md#s093),[S044](SOURCES.md#s044)]

<a id="f166"></a>

### F166 — воспроизводимость repo ограничена артефактами и дефектом.

- Исходный локатор: [W1-13-F14](_WORK/W1_13_RESULT.md), строка62; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S044](SOURCES.md#s044)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F166](RAW_FACTS.md#f166) — воспроизводимость repo ограничена артефактами и дефектом.** Тип `source_code`; проверка: tracked files/строки кода прочитаны; запуск не проводился. В `.gitignore` исключены experiments*, *.json, *.onnx, *.pt, *.weights, data/artifacts/third_party. Это объясняет, почему ссылки на results_summary.json из сценария не предоставляют сами результаты. В pinned `scr/detection/run_yolov8_tpu.py:206` аргумент `args.output_tensอร์_name` отличается от parser `output_tensor_name`; это ожидаемый AttributeError до device open при достижении строки. Нельзя объявлять repo runnable/измеренным по наличию сценария. Подробная ветка модели — W1-08. [[S044](SOURCES.md#s044)]

<a id="f167"></a>

### F167 — исторический GUI подтверждает SSH-сценарий, но не современную выдачу.

- Исходный локатор: [W1-13-F15](_WORK/W1_13_RESULT.md), строка64; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S046](SOURCES.md#s046), [S094](SOURCES.md#s094)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F167](RAW_FACTS.md#f167) — исторический GUI подтверждает SSH-сценарий, но не современную выдачу.** Тип `source_code`; проверка: найден через GitHub API `q=iva+tpu`, клонирован `sttell/IVA_compiler_runner`, commit `543ab4a0e53b4efb851af5c592f8089b5685ec70`, `2022-04-03T13:27:54+03:00`, author Илья Биро. README заявляет Ubuntu20.04, Boost>=1.71, Qt5/CMake/OpenSSL/OpenGL/LibSSH/Python3, version1.0; API releases/tags пусты, license null, LICENSE не найден. `lib/compiler_core/.../compiler_runner/runner.sh` требует внешний compiler directory, делает `make`, запускает `./hpm_scheduler -system=ivatpu ...`; `remote_runner/remoterunner.cpp:166` собирает команду `run_tpu -t -r -p ...` и передаёт файлы SSH/SFTP. Нет supplied hpm_scheduler source/native SDK. Это независимый исторический авторский слой автоматизации, связь автора с vendor не установлена. [[S046](SOURCES.md#s046),[S094](SOURCES.md#s094)]

<a id="f168"></a>

### F168 — официальный исторический manifest раскрывает закрытый участок supply.

- Исходный локатор: [W1-13-F16](_WORK/W1_13_RESULT.md), строка66; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S095](SOURCES.md#s095)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F168](RAW_FACTS.md#f168) — официальный исторический manifest раскрывает закрытый участок supply.** Тип `primary_documentation`; проверка: GitHub MLCommons API/RAW прочитаны, поддеревья/скрипты сохранены, измерения не анализировались (это W1-11). `closed/IVATech/README.md` v0.7 перечисляет In-house software: `AU200_freq250_axi512.bit`, `iva-tpu-dkms_4.1.4-1ubuntu1_all.deb`, `iva_tpu_4.1.4_amd64.deb`, `libtpu_7.1.17_amd64.deb`, `dnn_quant-3.3.3`, `protobuf_evert-3.3.1`, `tpu_quantize-3.2.1`, `tpu_commands/tpu_compiler/tpu_compiler_frontend/tpu_compiler_tools/tpu_datatypes/tpu_tlm-14.0.0`, `tpu_tlm_is-14.0.1`, `iva_applications-6.4.1`, с колонкой SHA HASH. Длины 40 hex; исходник не уточняет алгоритм, потому здесь не переименовываем их в SHA256. Все literal hashes сохранены в KEY_SOURCE_LOCATORS.TXT. Это manifest исторической FPGA submission, не версии нынешнего LinQ. [[S095](SOURCES.md#s095)]

<a id="f169"></a>

### F169 — старый воспроизводимый рецепт упирается в непоставленные пакеты.

- Исходный локатор: [W1-13-F17](_WORK/W1_13_RESULT.md), строка68; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S096](SOURCES.md#s096), [S097](SOURCES.md#s097)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F169](RAW_FACTS.md#f169) — старый воспроизводимый рецепт упирается в непоставленные пакеты.** Тип `source_code`; проверка: MLPerf v0.7 resnet/mobilenet README, requirements, quantize.sh, compile.sh прочитаны. Public refs: `mlperf/inference` checkout `r0.7`, clipp, spdlog, исходные models Zenodo. `quantize/requirements.txt` требует `tensorflow==1.15.0`, `tpu-quantize==3.2.1`, `tpu_compiler_frontend==14.0.0`, `iva-applications==6.4.1`, click7.1.2/Pillow7.2.0; `compile.sh` вызывает `.venv/bin/tcf compile --optimize quantized_data/to_compile resnet50.tpu`. Ссылки download для in-house wheels/debs в этих инструкциях нет. Явный private registry hostname/token не найден. Правильная формулировка — «требуются отдельно поставляемые исторические vendor packages», а не установленный URL приватного index. [[S096](SOURCES.md#s096),[S097](SOURCES.md#s097)]

<a id="f170"></a>

### F170 — отрицательные package lookup имеют узкий смысл.

- Исходный локатор: [W1-13-F18](_WORK/W1_13_RESULT.md), строка70; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S098](SOURCES.md#s098)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F170](RAW_FACTS.md#f170) — отрицательные package lookup имеют узкий смысл.** Тип `local_observation`; проверка: прямые HTTPS GET JSON2026-10-23 дали404 для normalised names `tpu-framework`, `dnn-quant`, `onnx-direct`, `tpu-tlm-is`, `tpu-compiler`, `tpu-compiler-frontend`, `tpu-compiler-tools`, `tpu-datatypes`, `tpu-commands`, `tpu-tlm`, `tpu-quantize`, `protobuf-evert`. Это опровергает простое предположение «названия из guide можно сейчас взять с PyPI», но не доказывает, что нет другой distribution name, bundles, private wheelhouse, mirror или выдачи через ЛК. [[S098](SOURCES.md#s098)]

<a id="f171"></a>

### F171 — `pip install mlperf` не восстанавливает vendor binary.

- Исходный локатор: [W1-13-F19](_WORK/W1_13_RESULT.md), строка72; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S099](SOURCES.md#s099)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F171](RAW_FACTS.md#f171) — `pip install mlperf` не восстанавливает vendor binary.** Тип `primary_documentation` + `inference`; проверка: PyPI JSON200. PyPI mlperf latest0.1.0 (2025), author_email `Arjun <arjun@gateoverflow.com>`, Repository `https://github.com/gateoverflow/mlc`, dependency requests. Нет атрибуции IVA/LinQ; название совпадает с индустриальным термином. Не подменять им C++ binary из стороннего repo. [[S099](SOURCES.md#s099)]

<a id="f172"></a>

### F172 — публичный current release channel не установлен.

- Исходный локатор: [W1-13-F20](_WORK/W1_13_RESULT.md), строка74; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003), [S098](SOURCES.md#s098), [S100](SOURCES.md#s100), [S101](SOURCES.md#s101)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F172](RAW_FACTS.md#f172) — публичный current release channel не установлен.** Тип `unknown` с подтверждённой границей поиска; проверка: поисковые запросы и GitHub/HF API выполнены. У lin-q.ru/sol нет открытой ссылки на GitHub/registry SDK в прочитанном содержимом; public software gate есть. GitHub exact-name searches и HF `search=iva_tpu` не дали актуального атрибутированного SDK/model repo; HF `search=linq` возвращает множество одноимённых embeddings/usernames. Ни один из них без связи с lin-q.ru/IVA не принят за LinQ Model Zoo. Контейнер registry/digest и release notes Framework2026.8.43 не установлены. [[S003](SOURCES.md#s003),[S098](SOURCES.md#s098),[S100](SOURCES.md#s100), [S101](SOURCES.md#s101)]

<a id="f173"></a>

### F173 — Карта доступности

- Исходный локатор: [W1-13-MATRIX-7](_WORK/W1_13_RESULT.md), строка17; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003), [S083](SOURCES.md#s083), [S064](SOURCES.md#s064), [S084](SOURCES.md#s084), [S065](SOURCES.md#s065), [S085](SOURCES.md#s085), [S086](SOURCES.md#s086), [S087](SOURCES.md#s087), [S088](SOURCES.md#s088), [S089](SOURCES.md#s089), [S090](SOURCES.md#s090), [S091](SOURCES.md#s091), [S092](SOURCES.md#s092), [S093](SOURCES.md#s093), [S044](SOURCES.md#s044), [S046](SOURCES.md#s046), [S094](SOURCES.md#s094), [S095](SOURCES.md#s095), [S096](SOURCES.md#s096), [S097](SOURCES.md#s097), [S098](SOURCES.md#s098), [S099](SOURCES.md#s099), [S100](SOURCES.md#s100), [S101](SOURCES.md#s101), [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Карта доступности

| Компонент | Что реально доступно | Версия/дата | Граница |
|---|---|---|---|
| `pytpu` | PyPI JSON, sdist | 15.0.24; 2023-11-27 | Python bindings; native `/usr/lib/libtpu.2.so` отдельно; совместимость с 2026 неизвестна |
| `iva-tpu` | PyPI JSON, sdist | 11.2.6; 2021-08-31 | Тонкий loader native `/usr/lib/libtpu.so`; библиотека не вложена |
| `iva-applications` | PyPI JSON, wheel и sdist | 11.0.1; 2021-10-13 | Host model utilities; нет weights/compiler/runtime |
| `iva-classification-demo` | PyPI JSON, sdist | 1.1.0; 2020-06-27 | Qt demo классификации, TF1.15; современная применимость не установлена |
| `tpu_framework` | Официальный guide описывает локальный wheel | Документ2025; wheel без номера версии в примере | На PyPI normalised name `tpu-framework` 404; актуальная поставка не получена |
| `dnn_quant`, `onnx_direct` | Официальный guide и сторонние imports | Версии текущей поставки неизвестны | По соответствующим PyPI JSON 404; это не доказывает отдельную private registry distribution: они могут входить в wheel |
| `tpu_compiler*`, `tpu_quantize`, `tpu_datatypes`, `tpu_tlm*`, `protobuf_evert` | Исторический официальный MLPerf manifest | 2020; точные версии ниже | Публичные JSON имена проверены, 404; исходные артефакты из manifest не получены |
| Native `libtpu`, `tpu-dkms` | Названия/старые manifest/сценарии | 2020 и сторонний2026 | Актуальный deb/firmware не получен |
| Vendor `mlperf` binary | Указан внешний путь в сценариях2026 | `mlperf-16.16.12-Source/build/mlperf` | В стороннем repo бинарника нет; PyPI `mlperf` чужой |
| Software download на `/sol` | Публично описаны условия | Текущая проверка | Регистрация и верификация учётной записи |
| GitLab-like SDK homepage | URL из PyPI | `http://git.mmp.iva-tech.ru/tpu_sw/iva_tpu_sdk` | HTTP/HTTPS не разрешились через DNS; login/содержимое не проверены |
| Контейнер/Model Zoo | Vendor упоминает портал/Model Zoo | Текущие маркетинговые материалы | Атрибутированного публичного image digest, repo или реестра не установлено |


## W1-14 — W1-14 — Реальные интеграции и сквозные демонстрации LinQ

<a id="f174"></a>

### F174 — Промышленный показ ПАК ОТПБ

- Исходный локатор: [W1-14-F01](_WORK/W1_14_RESULT.md), строка17; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S102](SOURCES.md#s102)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F174](RAW_FACTS.md#f174) — Промышленный показ ПАК ОТПБ

Основание: **vendor_statement** интегратора; статус: **прочитана первичная страница**, событие лично не наблюдалось. [[S102](SOURCES.md#s102)]

Сообщение от 19.06.2026 описывает показ комплекса в Томске 9–10 июня. Назван вычислитель с TPU LinQ; перечислены контроль СИЗ по виду работ, людей под техникой, посторонних в зоне работ, телефона, огня/дыма, опасных предметов, а также отчётность и уведомления. Отзывы представителей Газпром трансгаз Томск и Минтруда — свидетельство презентации, не акт внедрения. Не раскрыты модификация ускорителя, число плат/камер, модели и веса, runtime, FPS, качество или задержки. Категория доказательства: **выставочная демонстрация по сообщению участника**; исходное видео работы/телеметрия не найдены.

<a id="f175"></a>

### F175 — Технический путь IVA CV с TPU

- Исходный локатор: [W1-14-F02](_WORK/W1_14_RESULT.md), строка23; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S103](SOURCES.md#s103)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 disposition:** image0.1.310 superseded by page-separated0.1.3+p10; [F295](RAW_FACTS.md#f295). W1 literal below is search history, not an exact deploy tag.

### [F175](RAW_FACTS.md#f175) — Технический путь IVA CV с TPU

Основание: **primary_documentation**; статус: **прочитан PDF через web extraction**, CLI-скачивание не удалось; аппаратного исполнения нет. [[S103](SOURCES.md#s103)]

Печатные страницы 8–10 описывают поток: камеры/файлы → проектный компонент видеоаналитики → Edge-api → БД; передаются видеопотоки, события и изображения. Пайплайн и модели собирает вендор. На p9 дан TPU-пример контейнера с `--device /dev/tpu0:/dev/tpu0`, `ivacv.tech:15444/common/walkers-node:0.1.310`, переменными `IVA_EDGE_SERVER`, `IVA_EDGE_SERVER_WS`. Edge-api имеет REST/WebSockets/gRPC. На p18–19 прямо описано отсутствие общего типового инсталлятора: сборка и репозиторий выделяются под проект. На p5 указан Linux ≥6.0; конкретная версия TPU runtime/драйвера отсутствует.

Это **документированный пример развёртывания**. Наличие адреса registry не означает свободный pull. Запрос к registry, аутентификация, скачивание образа и backend-проверка не выполнялись. Пример tenant `cbr` не доказывает установленное использование TPU в Центральном банке. PDF-скриншот инструмент не вернул как пригодное изображение; визуальное соответствие расположения блоков не заявляется.

<a id="f176"></a>

### F176 — Пользовательская часть действительно включает события промышленной безопасности

- Исходный локатор: [W1-14-F03](_WORK/W1_14_RESULT.md), строка31; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S104](SOURCES.md#s104), [S103](SOURCES.md#s103)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F176](RAW_FACTS.md#f176) — Пользовательская часть действительно включает события промышленной безопасности

Основание: **primary_documentation**; статус: **прочитан PDF**, UI не запускался. [[S104](SOURCES.md#s104)]

В руководстве пользователя, PDF p6–7, список фильтруемых типов событий включает отсутствие каски/жилета, запретную зону, сигарету, дым, телефон. PDF p8–10 описывает просмотр нескольких камер, добавление URL/локации/сервера, рабочие зоны и режимы записи (постоянно, по движению, по событиям). Это конкретная продуктовая семантика вокруг inference, но не перечень моделей, не качество распознавания и не доказательство, что каждый этот тип события вычисляется TPU в примере [S103](SOURCES.md#s103).

<a id="f177"></a>

### F177 — Заявленная поддержка LinQ в IVA CV и несовпадение требований

- Исходный локатор: [W1-14-F04](_WORK/W1_14_RESULT.md), строка37; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S105](SOURCES.md#s105), [S103](SOURCES.md#s103)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F177](RAW_FACTS.md#f177) — Заявленная поддержка LinQ в IVA CV и несовпадение требований

Основание: **vendor_statement** и опубликованный стек; статус: **прочитана страница**. [[S105](SOURCES.md#s105)]

Страница платформы явно включает LinQ (TPU), C++-ядро, IP-камеры и интеграции. Опубликованы Linux kernel ≥6.1, MongoDB ≥7, Docker/containerd для устройств кроме Nvidia; runtime-list содержит TensorRT/OpenVINO/Libtorch/ONNX Runtime/RKNN/Core ML/OpenCL, отдельный TPU runtime не указан. Это неполный для LinQ контракт установки. Порог ядра ≥6.1 отличается от ≥6.0 в PDF [S103](SOURCES.md#s103); дата/редакция PDF не установлена, путь uploads/2026/05 не равен доказанной дате публикации. Требуется запрос согласованной матрицы версий.

<a id="f178"></a>

### F178 — «Лира»: публичная демонстрация нескольких сетей

- Исходный локатор: [W1-14-F05](_WORK/W1_14_RESULT.md), строка43; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S106](SOURCES.md#s106), [S110](SOURCES.md#s110)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F178](RAW_FACTS.md#f178) — «Лира»: публичная демонстрация нескольких сетей

Основание: **vendor_statement** в авторском интервью; статус: **прочитана страница записи**, аудиовидео интервью не прослушано, таймкоды не установлены. [[S106](SOURCES.md#s106)]

Интервью директора коммерческого блока ХайТэк Владислава Николаева датировано 09.07.2025. Описание указывает сервер AQserv + LinQ HPD и одновременную работу четырёх нейросетей на ЦИПР-2025. Модели, нагрузка, версии и измерения не даны. Поэтому четыре сети — не четыре камеры и не четыре потока с известной частотой. Категория: **сообщение о выставочном показе**, не runnable example.

Партнёрский первичный анонс Аквариуса от 04.06.2025 подтверждает состав AQserv/HPD, но использует будущее время о показе. Его нельзя цитировать как самостоятельное доказательство уже выполненного теста. [[S110](SOURCES.md#s110)]

<a id="f179"></a>

### F179 — Авторский код YOLOv8: изучаемый тензорный путь, не видеосервис

- Исходный локатор: [W1-14-F06](_WORK/W1_14_RESULT.md), строка51; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual AST/argparse.Namespace identifier check; no full runner/SDK/device.

- Sources: [S049](SOURCES.md#s049)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F179](RAW_FACTS.md#f179) — Авторский код YOLOv8: изучаемый тензорный путь, не видеосервис

Основание: **source_code**; статус: **повторно скачан pinned raw-файл и выполнена AST-инспекция**, без импорта зависимостей и исполнения на TPU. [[S049](SOURCES.md#s049)]

Commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140` (дату commit 03.04.2026 передала W1-06; собственно метаданные даты не перепроверялись). Сценарий читает изображения COCO, делает letterbox/BGR→RGB/NCHW/float32÷255, вызывает `Device.list_devices/open/load/inference`, затем host NMS через Ultralytics и `torch.from_numpy`. Таймер окружает вызов runtime, а не весь путь декодирования/событий. Скрипт не является RTSP/multi-camera приложением.

Локально подтверждён ошибочный аргумент на строке 206: атрибут `args.output_tensอร์_name` вместо parser destination `output_tensor_name`. Сохранён `STATIC_CHECK.json`; чужой код не изменялся. При прохождении предыдущих проверок такой доступ вызывает AttributeError до перечисления устройств. Это дефект конкретного стороннего примера, не установленная ошибка LinQ SDK.

<a id="f180"></a>

### F180 — Что автор называет завершённым TPU detection path

- Исходный локатор: [W1-14-F07](_WORK/W1_14_RESULT.md), строка59; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S107](SOURCES.md#s107)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F180](RAW_FACTS.md#f180) — Что автор называет завершённым TPU detection path

Основание: **source_code / авторское сообщение о результатах**; статус: **прочитан pinned RUN_SCENARIO.txt в web**, результаты не запускались и не измерялись нами. [[S107](SOURCES.md#s107)]

Документ от 25.03.2026 разделяет три окружения: TPU, CPU/CUDA baseline и экспорт tiny-YOLO3. При отсутствии `/dev/tpu0` предписан пропуск TPU. Финальный detection path использует vendor `.tpu` tiny_yolo3, а не собственный YOLOv8 export; отдельная строка сообщает о незавершённом FCN O5. Путь MLPerf содержит `mlperf-16.16.12-Source`. Слово done в сценарии — сообщение автора, не публичный аппаратный протокол. Переносимый урок: сохранять отдельно происхождение модели, компилированного артефакта и результаты; готовый vendor detector не подтверждает перенос собственного PPE detector.

<a id="f181"></a>

### F181 — Именованные промышленные внедрения IVA CV не доказывают LinQ

- Исходный локатор: [W1-14-F08](_WORK/W1_14_RESULT.md), строка65; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S108](SOURCES.md#s108), [S109](SOURCES.md#s109), [S111](SOURCES.md#s111)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F181](RAW_FACTS.md#f181) — Именованные промышленные внедрения IVA CV не доказывают LinQ

Основание: **vendor_statement** интегратора; статус: **прочитаны карточки проектов**. [[S108](SOURCES.md#s108), [S109](SOURCES.md#s109), [S111](SOURCES.md#s111)]

Северсталь: офисная биометрия + Болид СКУД; НПО Энергомаш: выдача ключей с IVA CV, KeyGuard/PERCo/Болид/AD; Мосводоканал: офисный биометрический СКУД и адаптивная подсветка для слабого освещения. В этих карточках аппаратный backend LinQ не установлен. Это **сообщения о deployment платформы IVA CV**, а не доказанные deployments TPU. Не следует переносить на наш кейс и заявленную для офисного турникета процедуру менее секунды.


## W1-15 — W1-15 — наблюдаемость и доказательство исполнения LinQ

<a id="f182"></a>

### F182 — официальные имена найдены.

- Исходный локатор: [W1-15-F01](_WORK/W1_15_RESULT.md), строка38; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_statement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S026](SOURCES.md#s026)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F182](RAW_FACTS.md#f182) — официальные имена найдены.** Тип `vendor_statement`, [S026](SOURCES.md#s026) p1/p3; статус: самостоятельно прочитан документ. HPS datasheet называет Performance Profiler, DNN Stat; profiler описан как мониторинг скорости и загрузки вычислительных блоков. Также заявлены Power Monitor, температурный контроль, watchdog и управление частотой. Руководства запуска, формат отчёта, доступные counters, единицы времени, kernel-level trace и привязка к request ID не опубликованы в этом документе. Нельзя из этой записи получить интерфейс SDK либо считать все эти функции выданными команде.

<a id="f183"></a>

### F183 — framework debug logs не тождественны runtime telemetry.

- Исходный локатор: [W1-15-F02](_WORK/W1_15_RESULT.md), строка40; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F183](RAW_FACTS.md#f183) — framework debug logs не тождественны runtime telemetry.** Тип `primary_documentation`, [S030](SOURCES.md#s030) §4 p23–24; статус: прочитан сохранённый текст, не запуск. Документ описывает служебный вывод конвертера, квантователя и компилятора; стандартный Python `logging` может полностью его убрать. Следовательно, отсутствие debug output не диагностирует отсутствие TPU, а наличие compiler logs не доказывает execution. В образце печатаются результаты original/quantized/TLM/TPU и оценка `TLM estimates execution time: 5627.364001024086 us`. Это оценка TLM, не измеренная аппаратная задержка. Число не использовать как benchmark нашего решения.

<a id="f184"></a>

### F184 — старый README содержит конкретные statistics, но расходится с implementation.

- Исходный локатор: [W1-15-F03](_WORK/W1_15_RESULT.md), строка42; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation + source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S079](SOURCES.md#s079), [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F184](RAW_FACTS.md#f184) — старый README содержит конкретные statistics, но расходится с implementation.** Тип `primary_documentation` для README, `source_code` для сравнения; [S079](SOURCES.md#s079)/[S065](SOURCES.md#s065); статус: самостоятельно прочитаны JSON и source. README описывает `TPUDevice`, `TPUInference`, `result.timings`, `queue_timings` для трёх очередей transfer-to/executor/transfer-from, `execution_timing` и `device.stats["mem"]`. В actual классе `Device` 15.0.24 нет метода/свойства `stats`, а `Inference.sync` возвращает словарь NumPy outputs, не описанный README status-result. Поэтому копирование этих snippets в API `Device.open()` необоснованно. Это историческая зацепка для запроса актуального API, не подтверждённая метрика 2026. Семантика и единицы timing надо запросить вместе с reference, не угадывать по имени.

### B. Что фактически делает pytpu15.0.24

<a id="f185"></a>

### F185 — импорт не handshake.

- Исходный локатор: [W1-15-F04](_WORK/W1_15_RESULT.md), строка46; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F185](RAW_FACTS.md#f185) — импорт не handshake.** Тип `source_code`, [S065](SOURCES.md#s065) `_bindings.py:28–51`; статус: код прочитан, native библиотека не загружалась нами. `_LIB_TPU_SO_PATH='/usr/lib/libtpu.2.so'`, `_LibTPUBinder` связывается лениво при доступе к property `libtpu`. Успешный `import pytpu` не проверяет наличие `.so`, драйвера, hardware и исправность устройства. `pip show` столь же слабое свидетельство.

<a id="f186"></a>

### F186 — `list_devices()` не device enumeration protocol.

- Исходный локатор: [W1-15-F05](_WORK/W1_15_RESULT.md), строка48; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual isolated listing-expression mock: _WORK/W1_15/STATIC_SOURCE_CHECK.json; no native load or hardware.

- Sources: [S065](SOURCES.md#s065); [S174](SOURCES.md#s174)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F186](RAW_FACTS.md#f186) — `list_devices()` не device enumeration protocol.** Тип `source_code`, [S065](SOURCES.md#s065) строки 201–204; статус: прочитан код и выполнена изолированная локальная проверка return expression с mock `/dev`. Реализация выбирает entries по `re.match(r'tpu.', f) and len(f)==4`, возвращая `/dev/...`. Не выполняет native вызов, `stat`, проверку char device, permissions, PCI identity или ioctl. Дополнительно она пропускает `tpux`/`tpu.` и исключает `tpu10`. Это поведение данной старой Python-функции, а не утверждение об именовании или числе устройств LinQ2026.

Изолированная проверка `STATIC_SOURCE_CHECK.py` / `.json`: для mock entries `tpu0,tpu9,tpu10,tpux,tpu.,tpu,nvidia0` возвращены `/dev/tpu0,/dev/tpu9,/dev/tpux,/dev/tpu.`. Тип `local_observation`, реальная локальная операция без импорта пакета и без аппаратного вызова. Первый запуск скрипта завершился FileNotFoundError из-за неверного собственного relative root; путь исправлен, повторный запуск успешен. Это не ошибка SDK.

<a id="f187"></a>

### F187 — native binding начинается при открытии и сильнее списка путей.

- Исходный локатор: [W1-15-F06](_WORK/W1_15_RESULT.md), строка52; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F187](RAW_FACTS.md#f187) — native binding начинается при открытии и сильнее списка путей.** Тип `source_code`, [S065](SOURCES.md#s065) строки 185–229; статус: прочитан код. `Device.open(dev_name)` передаёт строку в `tpu_create_device`, затем constructor вызывает `tpu_init_device` и `tpu_is_device_valid`. При неуспехе — `ValueError` с `Invalid init code ...` либо `Invalid device: ...` и native message. Это позволяет связать session с явно выбранным путем. Однако Python-код не раскрывает, как native библиотека проверяет реальное устройство.

<a id="f188"></a>

### F188 — информация устройства и программы доступна через native JSON.

- Исходный локатор: [W1-15-F07](_WORK/W1_15_RESULT.md), строка54; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F188](RAW_FACTS.md#f188) — информация устройства и программы доступна через native JSON.** Тип `source_code`, [S065](SOURCES.md#s065) строки 228–229, 273–295; статус: прочитан код. `Device.info()` вызывает `tpu_get_device_info` и JSON decode. `Program.info()` — `tpu_get_program_info`; constructor использует metadata keys `inputs['1']`, `outputs['2']`, `hardware_parameters`. Схема `Device.info()` здесь не задана; нет основания обещать serial, PCI address, firmware, driver version, execution counter, температурный датчик или даже их имена. Нужно сохранить фактически возвращённый JSON и разобрать его по актуальному reference.

<a id="f189"></a>

### F189 — загрузка и inference имеют явные проверки ошибок.

- Исходный локатор: [W1-15-F08](_WORK/W1_15_RESULT.md), строка56; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 clarification:** output is a view, not a numerical copy; Python-owned backing was retained in mock probe; [F267](RAW_FACTS.md#f267).

**[F189](RAW_FACTS.md#f189) — загрузка и inference имеют явные проверки ошибок.** Тип `source_code`, [S065](SOURCES.md#s065) строки 235–253, 373–425; статус: прочитан код, не вызвано. `load(path)` создаёт native program, проверяет valid program, вызывает `tpu_load_program`, проверяет device error string. `_run` передаёт указатели device/inference и mode в `tpu_run_inference`; ненулевой return code вызывает `InferenceError`. После копирования outputs `sync` вызывает `_check_status()` → `tpu_get_inference_status`; ненулевой status тоже ошибка. Наличие успешного sync в логе сильнее печати произвольной метки `TPU`, но закрытый native runtime остаётся доверенной частью цепочки.

<a id="f190"></a>

### F190 — внешний sync timer не чистый compute counter.

- Исходный локатор: [W1-15-F09](_WORK/W1_15_RESULT.md), строка58; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 clarification:** output is a view, not a numerical copy; Python-owned backing was retained in mock probe; [F267](RAW_FACTS.md#f267).

**[F190](RAW_FACTS.md#f190) — внешний sync timer не чистый compute counter.** Тип `source_code` + `inference`, [S065](SOURCES.md#s065) `Inference.sync`/`_load_inference`/`_get_inference`; статус: source analysis. Внутри sync резервируются buffers, загружаются данные, выполняется `_run`, формируются/копируются NumPy outputs и проверяется status. Стандартный mode `ProcessingMode.FULL=3`; определены также RAW=0, PRE_PROCESS=1, POST_PROCESS=2. Эти enum не доказывают перенос всех преобразований на CPU или TPU. Время вокруг sync включает Python/runtime и обработку buffers; нельзя подписывать его «время TPU ядра» без separate timing reference.

<a id="f191"></a>

### F191 — в просмотренном Python binding нет пути автоматического CPU-model fallback.

- Исходный локатор: [W1-15-F10](_WORK/W1_15_RESULT.md), строка60; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F191](RAW_FACTS.md#f191) — в просмотренном Python binding нет пути автоматического CPU-model fallback.** Тип `source_code`, [S065](SOURCES.md#s065); статус: просмотрен файл. Здесь нет вызова TensorFlow/ONNX Runtime/PyTorch для исполнения исходного neural graph в ветке ошибки устройства. Важное ограничение: это не доказывает отсутствие fallback в native `.so`, сервисной оболочке, обновлённом SDK или коде нашего приложения. Не найденный CPU-path не равен установленной невозможности mixed execution.

### C. Авторский CV пример и историческое измерение

<a id="f192"></a>

### F192 — сторонний YOLO runner не является готовым доказательством запуска.

- Исходный локатор: [W1-15-F11](_WORK/W1_15_RESULT.md), строка64; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S049](SOURCES.md#s049)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F192](RAW_FACTS.md#f192) — сторонний YOLO runner не является готовым доказательством запуска.** Тип `source_code`, [S049](SOURCES.md#s049) pinned строки 191–203; статус: самостоятельно прочитан remote source и AST локального клона. Parser создаёт `output_tensor_name`, а `main` до `list_devices()` обращается к `args.output_tensอร์_name`. При обычном argparse Namespace атрибута нет: ожидается AttributeError, если выполнение уже прошло предыдущие проверки файлов/импортов/COCO. Полный runner нами не запускался. AST нашёл именно не-ASCII attribute; дефект стороннего примера не переносится на SDK.

<a id="f193"></a>

### F193 — граница host/TPU в этом примере видима.

- Исходный локатор: [W1-15-F12](_WORK/W1_15_RESULT.md), строка66; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S049](SOURCES.md#s049)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F193](RAW_FACTS.md#f193) — граница host/TPU в этом примере видима.** Тип `source_code`, [S049](SOURCES.md#s049); статус: remote source прочитан. Device можно явно задать через `--device`, иначе берётся первый путь. Runner открывает device и `.tpu`, выполняет `run` при наличии, иначе `sync`. Замер perf_counter обрамляет runtime call; NMS вызывается после него через NumPy→torch и Ultralytics на host. Это отдельная постобработка, не установленный CPU fallback графа. Summary в JSON, созданный самим runner, остаётся application report, а не аппаратным attestation. Даже после исправления typo нужен реальный execution protocol.

<a id="f194"></a>

### F194 — исторический MLPerf связывает machine description, harness и logs, но относится к FPGA.

- Исходный локатор: [W1-15-F13](_WORK/W1_15_RESULT.md), строка68; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: reported_measurement + source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S075](SOURCES.md#s075), [S112](SOURCES.md#s112)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F194](RAW_FACTS.md#f194) — исторический MLPerf связывает machine description, harness и logs, но относится к FPGA.** Тип `reported_measurement` + `source_code`, [S075](SOURCES.md#s075)/[S112](SOURCES.md#s112); статус: самостоятельно скачаны и прочитаны raw files, benchmark не запускался нами. System JSON: `iva-fpga-1`, accelerator `IVA_FPGA_1`, 250MHz, Alveo U200, Ubuntu18.04, Tensorflow1.15.0; stack `iva_tpu4.1.4`, `libtpu7.1.15`, `tpu_quantize3.2.1`, `tpu-compiler13.1.0`. SingleStream summary сообщает VALID, p90 12,230,138ns, min duration60,000ms, query samples1. Это полезный образец воспроизводимого пакета доказательств, не производительность LinQ H2026.

<a id="f195"></a>

### F195 — submit/completion counts в historical harness не аппаратные utilization counters.

- Исходный локатор: [W1-15-F14](_WORK/W1_15_RESULT.md), строка70; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S112](SOURCES.md#s112)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F195](RAW_FACTS.md#f195) — submit/completion counts в historical harness не аппаратные utilization counters.** Тип `source_code`, [S112](SOURCES.md#s112); статус: скачан и прочитан source. `tpu_inference_submit`, `tpu_inference_wait`, получение output tensors и `QuerySamplesComplete` образуют проверяемую цепочку completion. `inferenceSubmitedCount_` и `inferenceCompletedCount_` — переменные harness, debug queue messages печатает spdlog. Они не доказывают наличие equivalent counters в современных firmware. MLPerf summary `VALID` сообщает о критериях данного benchmark; сам по себе не удостоверяет request/device identity нашего сервиса.

<a id="f196"></a>

### F196 — авторы VK/ВШЭ не имели встроенного счётчика операций/с в доступной им среде.

- Исходный локатор: [W1-15-F15](_WORK/W1_15_RESULT.md), строка72; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: reported_measurement.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S017](SOURCES.md#s017)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F196](RAW_FACTS.md#f196) — авторы VK/ВШЭ не имели встроенного счётчика операций/с в доступной им среде.** Тип `reported_measurement` для описанного опыта, [S017](SOURCES.md#s017); статус: самостоятельно прочитана статья, измерения не воспроизводились. Авторы считали операции модели и FPS вручную. Описаны remote GUI, preload performance, последовательная подача для latency, batch1/2/4/8 и STAGING. Версии и identity не даны. Это не опровержение profiler в HPS datasheet: отличаются время, окружение и смысл метрики. Derived ops/s не становятся аппаратным counter, а preload-результат — задержкой нашего видеосервиса.

<a id="f197"></a>

### F197 — контейнерный device mapping только предоставляет доступ.

- Исходный локатор: [W1-15-F16](_WORK/W1_15_RESULT.md), строка74; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S103](SOURCES.md#s103)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.

**W2 disposition:** image0.1.310 superseded by page-separated0.1.3+p10; [F295](RAW_FACTS.md#f295). W1 literal below is search history, not an exact deploy tag.

**[F197](RAW_FACTS.md#f197) — контейнерный device mapping только предоставляет доступ.** Тип `inference` из handoff [S103](SOURCES.md#s103), не самостоятельное чтение. Указанные родителем p9 литералы `--device /dev/tpu0:/dev/tpu0` и image `ivacv.tech:15444/common/walkers-node:0.1.310` объясняют binding контейнера к host device node. Даже подтверждённый docker inspect/compose с таким mapping доказывал бы возможность доступа, а не обращение inference к этому устройству. Full integration и независимая проверка документа у W1-14.


## W2-A — W2-A — поставка, окружение, доступ и права LinQ

<a id="f198"></a>

### F198 — Повторно получены `/docs`, `/sol`, `/tech`, `/press`, `/hr` через TinyFish. Списки ссылок `/docs` и `/sol` ведут к документации, gate и формам; прямого современного wheel/registry/

- Исходный локатор: [W2-A-F01](_WORK/W2_A_RESULT.md), строка17; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S019](SOURCES.md#s019), [S037](SOURCES.md#s037), [S014](SOURCES.md#s014), [S002](SOURCES.md#s002)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| [F198](RAW_FACTS.md#f198) | Повторно получены `/docs`, `/sol`, `/tech`, `/press`, `/hr` через TinyFish. Списки ссылок `/docs` и `/sol` ведут к документации, gate и формам; прямого современного wheel/registry/model-zoo URL в этих списках нет. | [S019](SOURCES.md#s019)–[S037](SOURCES.md#s037), [S014](SOURCES.md#s014), [S002](SOURCES.md#s002); live content/navigation inspection. Никакой authenticated области не читали. |

<a id="f199"></a>

### F199 — `/docs` продолжает ссылаться на `Framework_manual_H1.pdf`; актуальный public index не предоставляет отдельный installation guide или release notes compiler/runtime в извлечённом сп

- Исходный локатор: [W2-A-F02](_WORK/W2_A_RESULT.md), строка18; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S019](SOURCES.md#s019)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| [F199](RAW_FACTS.md#f199) | `/docs` продолжает ссылаться на `Framework_manual_H1.pdf`; актуальный public index не предоставляет отдельный installation guide или release notes compiler/runtime в извлечённом списке. | [S019](SOURCES.md#s019). Это наблюдение списка, не отрицание существования закрытых документов. |

<a id="f200"></a>

### F200 — Software route по-прежнему отделяет регистрацию от верификации. Выписанные права текущего пользователя не установлены; доступ к публичному guide не равен download/access к устройст

- Исходный локатор: [W2-A-F03](_WORK/W2_A_RESULT.md), строка19; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| [F200](RAW_FACTS.md#f200) | Software route по-прежнему отделяет регистрацию от верификации. Выписанные права текущего пользователя не установлены; доступ к публичному guide не равен download/access к устройству. | [S003](SOURCES.md#s003); live read. Форму повторно не исследовали и не отправляли. |

<a id="f201"></a>

### F201 — В списке `/press` открытый ZIP — `logo_linq.zip`, DOCX — `2025_about_linq.docx`, PDF — `2026_linq_presentation.pdf`. Это PR-материалы по явно данным названиям/подписям, а не подтве

- Исходный локатор: [W2-A-F04](_WORK/W2_A_RESULT.md), строка20; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S037](SOURCES.md#s037), [S014](SOURCES.md#s014), [S002](SOURCES.md#s002)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| [F201](RAW_FACTS.md#f201) | В списке `/press` открытый ZIP — `logo_linq.zip`, DOCX — `2025_about_linq.docx`, PDF — `2026_linq_presentation.pdf`. Это PR-материалы по явно данным названиям/подписям, а не подтверждённый SDK bundle. | [S037](SOURCES.md#s037), [S014](SOURCES.md#s014), [S002](SOURCES.md#s002); direct navigation links. ZIP/DOCX не загружали и их содержимое не заявляем. |

<a id="f202"></a>

### F202 — Реестровая индексированная страница показывает 32778, 31.03.2026, framework IVA H1 и ООО «ХАЙТЭК».

- Исходный локатор: [W2-A-F05](_WORK/W2_A_RESULT.md), строка21; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S113](SOURCES.md#s113)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| [F202](RAW_FACTS.md#f202) | Реестровая индексированная страница показывает 32778, 31.03.2026, framework IVA H1 и ООО «ХАЙТЭК». | [S113](SOURCES.md#s113); **indexed primary copy**, не live registry contents. web.open: TimeoutError; TinyFish: timeout. Технические вложения неизвестны. |

<a id="f203"></a>

### F203 — `pytpu-15.0.24.tar.gz` — открытый исторический Python-source artifact, SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`. Actual archive не содержит LICENSE

- Исходный локатор: [W2-A-F06](_WORK/W2_A_RESULT.md), строка22; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| [F203](RAW_FACTS.md#f203) | `pytpu-15.0.24.tar.gz` — открытый исторический Python-source artifact, SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`. Actual archive не содержит LICENSE/COPYING/EULA/NOTICE или native `.so/.dll/.deb/.rpm/.whl` членов. | [S065](SOURCES.md#s065); повторная read-only tar/member/metadata inspection, `INSPECT_SAVED.py`. Не package install/import. |

<a id="f204"></a>

### F204 — Для этого pytpu: `python_requires='>=3.6'`; основной `install_requires=['numpy']`; optional RAW test dependency `tpu-tlm-is~=0.3.0.1`. Native loader содержит `/usr/lib/libtpu.2.so`

- Исходный локатор: [W2-A-F07](_WORK/W2_A_RESULT.md), строка23; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| [F204](RAW_FACTS.md#f204) | Для этого pytpu: `python_requires='>=3.6'`; основной `install_requires=['numpy']`; optional RAW test dependency `tpu-tlm-is~=0.3.0.1`. Native loader содержит `/usr/lib/libtpu.2.so` и ленивую `_bind()`. | [S065](SOURCES.md#s065), `setup.py:25–47`, `_bindings.py:28–51`. Source inspection. Это не доказательство modern ABI или CPU-only compiler. |

<a id="f205"></a>

### F205 — `iva_applications-11.0.1.tar.gz` SHA256 `f04be1de75b8a7b22bd835c424fb61cd27f3e179356b7b4edc13f03f470f6b68` реально содержит LICENSE с copyright2020 IVA Technologies и MIT-условиями

- Исходный локатор: [W2-A-F08](_WORK/W2_A_RESULT.md), строка24; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S090](SOURCES.md#s090)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| [F205](RAW_FACTS.md#f205) | `iva_applications-11.0.1.tar.gz` SHA256 `f04be1de75b8a7b22bd835c424fb61cd27f3e179356b7b4edc13f03f470f6b68` реально содержит LICENSE с copyright2020 IVA Technologies и MIT-условиями, хотя PKG-INFO указывает UNKNOWN. | [S090](SOURCES.md#s090); actual archive LICENSE прочитан. Условия разрешают использование/изменение/распространение именно этого Software с сохранением copyright/permission notice. Не лицензируют compiler, веса или image. |

<a id="f206"></a>

### F206 — `iva-tpu-11.2.6.tar.gz` SHA256 `885cb9ef75a87fb83dcf988d8e8664477a4bccca5f058feaede2130dc94a63ff` также не содержит названных лицензионных/native файлов.

- Исходный локатор: [W2-A-F09](_WORK/W2_A_RESULT.md), строка25; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S087](SOURCES.md#s087)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| [F206](RAW_FACTS.md#f206) | `iva-tpu-11.2.6.tar.gz` SHA256 `885cb9ef75a87fb83dcf988d8e8664477a4bccca5f058feaede2130dc94a63ff` также не содержит названных лицензионных/native файлов. | [S087](SOURCES.md#s087); actual archive inspection. Отсутствие файла не устанавливает запрет; нужен grant поставщика/автора. |

<a id="f207"></a>

### F207 — Сторонний pinned repo указывает три отдельных Python environments; TPU env требует уже существующие `libtpu / tpu-dkms / pytpu / tpu_framework / mlperf`. Его requirements включает 

- Исходный локатор: [W2-A-F10](_WORK/W2_A_RESULT.md), строка26; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S044](SOURCES.md#s044)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| [F207](RAW_FACTS.md#f207) | Сторонний pinned repo указывает три отдельных Python environments; TPU env требует уже существующие `libtpu / tpu-dkms / pytpu / tpu_framework / mlperf`. Его requirements включает TF2.14.1 и NumPy1.26.4, но не восстанавливает названные vendor поставки. | [S044](SOURCES.md#s044), requirements.txt и RUN_SCENARIO.txt, раздел HOSTS AND ENVIRONMENTS. Static read, не validation. |

<a id="f208"></a>

### F208 — Public native-free import старых bindings не означает native-free metadata/runtime операции: `Device`/`Program` пути обращаются к `_LIB_TPU_BINDER.libtpu`. Ни это, ни архитектурное

- Исходный локатор: [W2-A-F11](_WORK/W2_A_RESULT.md), строка27; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065), [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| [F208](RAW_FACTS.md#f208) | Public native-free import старых bindings не означает native-free metadata/runtime операции: `Device`/`Program` пути обращаются к `_LIB_TPU_BINDER.libtpu`. Ни это, ни архитектурное разделение quantize/compile/run не решает зависимости импортов **неполученного** `tpu_framework`. | [S065](SOURCES.md#s065) `_bindings.py:195,244`; [S030](SOURCES.md#s030). Вывод ограничен source. CPU-only compile остаётся точным экспериментальным вопросом. |

<a id="f209"></a>

### F209 — Названия modern framework/runtime подтверждены условиями опубликованного benchmark2026, но exact METADATA, Requires-Dist, native ABI pairing и права поставки не появились в новом п

- Исходный локатор: [W2-A-F12](_WORK/W2_A_RESULT.md), строка28; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033), [S019](SOURCES.md#s019), [S113](SOURCES.md#s113)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| [F209](RAW_FACTS.md#f209) | Названия modern framework/runtime подтверждены условиями опубликованного benchmark2026, но exact METADATA, Requires-Dist, native ABI pairing и права поставки не появились в новом поиске. | [S033](SOURCES.md#s033) (reuse W1), [S019](SOURCES.md#s019)–[S113](SOURCES.md#s113) + negative searches. Не новые измерения и не установленная среда команды. |

<a id="f210"></a>

### F210 — Нормализованная component/version/access/license matrix

- Исходный локатор: [W2-A-MATRIX-8](_WORK/W2_A_RESULT.md), строка30; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S019](SOURCES.md#s019), [S003](SOURCES.md#s003), [S037](SOURCES.md#s037), [S014](SOURCES.md#s014), [S002](SOURCES.md#s002), [S113](SOURCES.md#s113), [S114](SOURCES.md#s114), [S065](SOURCES.md#s065), [S090](SOURCES.md#s090), [S087](SOURCES.md#s087), [S044](SOURCES.md#s044), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Нормализованная component/version/access/license matrix

`?` означает отсутствие именно нужного доказательства. Строки не являются совместимым installation set.

| Компонент / версия или контекст | Получение сейчас / формат | Python/OS/dependencies, установленные границы | Native/device requirement | Execute / modify / redistribute |
|---|---|---|---|---|
| Framework guide2025, программа `RU.РМДВ.04.06.014-03` | Public PDF via /docs; сохранённый текст W1 | Ubuntu20.04, Python3.11, RAM≥32GB; `tpu_framework-py3-none-any.whl` — документированный пример без exact release | Реальный wheel не получен; import/native dependency ?; compile без device ? | Документ можно читать; SDK grant ? |
| TPU Framework2026.8.43 | Только версия в vendor benchmark; bundle/channel ? | Ubuntu24.04 в benchmark; Python/Requires-Dist/ISA ? | Native compiler libs, target, license check ? | EULA/число рабочих мест/перенос ? |
| TPU Runtime16.18.6 | Только версия в benchmark; package filename ? | Companion driver/firmware/libtpu/pytpu versions ? | Inference требует выданный LinQ контур; local vs service ? | Execute grant/redistribution ? |
| Driver/firmware/current native runtime | Полная современная поставка не получена | Tested kernel/OS/ISA, `.so` SONAME, DKMS/firmware pairing ? | Отдельно от Python package; device permissions ? | ? |
| `pytpu15.0.24` (2023) | Public sdist, actual bytes в W1 | Requires-Python≥3.6, numpy; does not pin modern stack | Lazy import source; runtime `/usr/lib/libtpu.2.so`, binary не внутри | Metadata UNKNOWN; explicit license в archive не найден; modern grant ? |
| `iva-tpu11.2.6` (2021) | Public sdist, actual bytes | Старый package/import layer `iva_tpu`; не substitute pytpu | Старый native `libtpu.so`; pairing2026 ? | Explicit license в archive не найден; grant ? |
| `iva_applications11.0.1` (2021) | Public sdist, actual bytes | Исторические pins: scipy1.4.1, keras2.2.4; extras TF2.4.1, pytpu13.0.6 | Helpers не поставляют современные compiler/runtime binaries | MIT для actual code/docs этого пакета с сохранением notices |
| `dnn_quant`, `onnx_direct`, `tpu`/compiler/TLM modern | Имена в source/docs; соответствующий дистрибутив/bundling ? | Exact current versions/dependency closure ? | CPU-only eligibility ?; TLM optional availability ? | ? |
| Modern Model Zoo / готовые `.tpu` / checkpoints | Упомянут vendor; direct атрибутированный locator не найден | Per-model source/export/calibration/target manifest ? | Совместимость `.tpu` с выданным runtime ? | Code/weights/compiled artifact grants раздельно ? |
| `linq-cv-bench` commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140` | Public third-party source, saved clone | Авторский venv311, TF2.14.1; incomplete vendor deps | Автор требует TPU host для TPU sections; CPU-compile-only test им не установлен | Repo license null/явный grant в прочитанной поставке не установлен |
| Cloud/service/image хакатона | Online access обещан; endpoint/образ/выдача не получены | Contract, quotas, custom compile/model update ? | Кто физически имеет device/native runtime — зависит от выдачи | Multi-user access, uploads, retention, publication ? |

Матрица не обосновывает Windows/WSL/ARM совместимость. `py3-none-any` имени guide не раскрывает binary dependencies. Логотипы/перечень ОС не дают tested ABI release. Проверку слайда6 оставляем профильной W2-H; здесь новый PDF не читали/не выдаём текст за visual check.


## W2-B — W2-B — оригинальный guide, швы примера и граница source/version

<a id="f211"></a>

### F211 — CLI binary retrieval guide/presentation по HTTPS завершился TLS EOF; HTTP guide — remote disconnect; `curl.exe` с принудительным TLS1.2 — handshake failure. Оригинальных PDF bytes 

- Исходный локатор: [W2-B-F01](_WORK/W2_B_RESULT.md), строка17; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: network_observation / reported_remote_observation.

- actual_check: retrieval/tool outcomes only; no PDF image inspected.

- Sources: [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S118](SOURCES.md#s118)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт и решение | Тип основания / actual test |
|---|---|---|
| [F211](RAW_FACTS.md#f211) | CLI binary retrieval guide/presentation по HTTPS завершился TLS EOF; HTTP guide — remote disconnect; `curl.exe` с принудительным TLS1.2 — handshake failure. Оригинальных PDF bytes и их checksum нет. | actual network observations, [S030](SOURCES.md#s030)/[S033](SOURCES.md#s033)/[S118](SOURCES.md#s118); не отсутствие PDF |

<a id="f212"></a>

### F212 — web screenshot guide p11 отказал: content type не application/pdf; ссылку или вызов screenshot не считать просмотром.

- Исходный локатор: [W2-B-F02](_WORK/W2_B_RESULT.md), строка18; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: network_observation / reported_remote_observation.

- actual_check: retrieval/tool outcomes only; no PDF image inspected.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт и решение | Тип основания / actual test |
|---|---|---|
| [F212](RAW_FACTS.md#f212) | web screenshot guide p11 отказал: content type не application/pdf; ссылку или вызов screenshot не считать просмотром. | tool failure, [S030](SOURCES.md#s030); visual verification отсутствует |

<a id="f213"></a>

### F213 — TinyFish live browser run сообщил, что PDF виден и имеет28 страниц; повторил converter tuple p11 и single assignment p19. Ответ содержит только текст, ни image block, ни PNG, ни sc

- Исходный локатор: [W2-B-F03](_WORK/W2_B_RESULT.md), строка19; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: network_observation / reported_remote_observation.

- actual_check: retrieval/tool outcomes only; no PDF image inspected.

- Sources: [S117](SOURCES.md#s117)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт и решение | Тип основания / actual test |
|---|---|---|
| [F213](RAW_FACTS.md#f213) | TinyFish live browser run сообщил, что PDF виден и имеет28 страниц; повторил converter tuple p11 и single assignment p19. Ответ содержит только текст, ни image block, ни PNG, ни screenshot URL. Это новая удалённая заявка browser agent, но не просмотр страниц исследователем. Число28 не разрешает конфликт W1 `27` vs титул `Листов28`. | reported remote observation [S117](SOURCES.md#s117); no actual screenshot seen |

<a id="f214"></a>

### F214 — Старый URL `hi-tech.org/...rukovodstvo-polzovatelya.pdf` реально отвечает200, но `Content-Type: text/html`, 29101 bytes; web показывает главную ООО «Хайтэк-Интеграция», ИНН77223506

- Исходный локатор: [W2-B-F04](_WORK/W2_B_RESULT.md), строка20; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: network_observation / reported_remote_observation.

- actual_check: retrieval/tool outcomes only; no PDF image inspected.

- Sources: [S008](SOURCES.md#s008)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт и решение | Тип основания / actual test |
|---|---|---|
| [F214](RAW_FACTS.md#f214) | Старый URL `hi-tech.org/...rukovodstvo-polzovatelya.pdf` реально отвечает200, но `Content-Type: text/html`, 29101 bytes; web показывает главную ООО «Хайтэк-Интеграция», ИНН7722350688. Он не дал PDF и не является source guide для сверки. | downloaded HTTP headers + web HTML, [S008](SOURCES.md#s008); новый точный отрицательный результат |

<a id="f215"></a>

### F215 — TF v2.14.1 экспортирует `graph_util.import_graph_def` и `import_graph_def`; функция импортирует в текущий default Graph, по умолчанию добавляет scope import, а без return_elements 

- Исходный локатор: [W2-B-F05](_WORK/W2_B_RESULT.md), строка21; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S115](SOURCES.md#s115)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт и решение | Тип основания / actual test |
|---|---|---|
| [F215](RAW_FACTS.md#f215) | TF v2.14.1 экспортирует `graph_util.import_graph_def` и `import_graph_def`; функция импортирует в текущий default Graph, по умолчанию добавляет scope import, а без return_elements возвращает None. Она не является фабрикой нового tf.Graph. | official upstream source [S115](SOURCES.md#s115), importer.py354–411,485–493,549–552; static only |

<a id="f216"></a>

### F216 — TF v2.14.1 Session при graph=None использует ops.get_default_graph(); следовательно строка guide-text не доказывает TypeError от Session. Default import prefix может привести к нес

- Исходный локатор: [W2-B-F06](_WORK/W2_B_RESULT.md), строка22; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S116](SOURCES.md#s116), [S115](SOURCES.md#s115)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт и решение | Тип основания / actual test |
|---|---|---|
| [F216](RAW_FACTS.md#f216) | TF v2.14.1 Session при graph=None использует ops.get_default_graph(); следовательно строка guide-text не доказывает TypeError от Session. Default import prefix может привести к несоответствию имён; повторный импорт — к новому scope/старым nodes. Нужен минимальный прогон в matching среде, а не исправление от имени LinQ. | official upstream source [S116](SOURCES.md#s116) session.py662–668 + [S115](SOURCES.md#s115); conditional inference, не выполнено |

<a id="f217"></a>

### F217 — ONNX v1.15.0 экспортирует ModelProto; load_model возвращает этот тип, load является alias load_model. В этом source нет ModeProto. Это подтверждает подозрительность literal, но не 

- Исходный локатор: [W2-B-F07](_WORK/W2_B_RESULT.md), строка23; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S119](SOURCES.md#s119)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт и решение | Тип основания / actual test |
|---|---|---|
| [F217](RAW_FACTS.md#f217) | ONNX v1.15.0 экспортирует ModelProto; load_model возвращает этот тип, load является alias load_model. В этом source нет ModeProto. Это подтверждает подозрительность literal, но не доказывает наличие опечатки на исходной странице PDF. | official upstream source [S119](SOURCES.md#s119), __init__.py38,92,176–180, конец файла; static only |

<a id="f218"></a>

### F218 — Pinned third-party ResNet builder явно допускает tuple/single converter, преобразует tf.Graph через as_graph_def, затем использует RegularModel/calibrate/quantize и распаковывает N

- Исходный локатор: [W2-B-F08](_WORK/W2_B_RESULT.md), строка24; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S120](SOURCES.md#s120)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт и решение | Тип основания / actual test |
|---|---|---|
| [F218](RAW_FACTS.md#f218) | Pinned third-party ResNet builder явно допускает tuple/single converter, преобразует tf.Graph через as_graph_def, затем использует RegularModel/calibrate/quantize и распаковывает Network result. Эти защитные ветки не доказывают, что обе формы когда-либо были поддержаны одним SDK; sample не matching официальный end-to-end. | [S120](SOURCES.md#s120) source_code, actual network read + W1 saved source; не execution |

<a id="f219"></a>

### F219 — Целевые web поиски по end_to_end.py+tpu_framework/IVA/LinQ, onnx_to_tf+tpu_framework/128x128, точному designation и Framework_manual_H1 не дали релевантного официального source arc

- Исходный локатор: [W2-B-F09](_WORK/W2_B_RESULT.md), строка25; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S008](SOURCES.md#s008), [S115](SOURCES.md#s115), [S116](SOURCES.md#s116), [S117](SOURCES.md#s117), [S118](SOURCES.md#s118), [S119](SOURCES.md#s119), [S120](SOURCES.md#s120)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт и решение | Тип основания / actual test |
|---|---|---|
| [F219](RAW_FACTS.md#f219) | Целевые web поиски по end_to_end.py+tpu_framework/IVA/LinQ, onnx_to_tf+tpu_framework/128x128, точному designation и Framework_manual_H1 не дали релевантного официального source archive/errata. Broad onnx_direct выдаёт одноимённый LocalAI и исключён. | actual targeted search; не утверждение, что source не существует |


## W2-C — W2-C — ONNX frontend, versioned exporter и constraints кандидатов

<a id="f220"></a>

### F220 — W2-C-F01, S01, source intent.

- Исходный локатор: [W2-C-F01](_WORK/W2_C_RESULT.md), строка34; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S055](SOURCES.md#s055), [S048](SOURCES.md#s048)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- **[F220](RAW_FACTS.md#f220), [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), source intent.** Экспортёр автора выставляет по умолчанию `opset=13`, `batch_size=1`, `imgsz=640`, argparse-флаги `dynamic`/`simplify` по умолчанию false, а в `model.export` передаёт `nms=False`. Он сам допускает иной `--opset`, batch и dynamic. Это прямое опровержение прочтения «script доказывает только static13 разрешён LinQ»; успешный проход иных вариантов он тоже не доказывает.

<a id="f221"></a>

### F221 — W2-C-F02, S01, local source fact.

- Исходный локатор: [W2-C-F02](_WORK/W2_C_RESULT.md), строка35; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S055](SOURCES.md#s055), [S048](SOURCES.md#s048)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- **[F221](RAW_FACTS.md#f221), [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), local source fact.** `force_static_onnx_input_shape` меняет только четыре dim_value выбранного `graph.input`, жёстко `(1,3,img_size,img_size)`. Он не посещает nodes, initializers, Constant attrs, graph.output или value_info. Поэтому вызов не является полноценной shape specialization / пересборкой head. Даже если protobuf удалит взаимоисключающий dim_param, остаются неизменёнными внутренние constants. Из этого не следует, что конкретный неизвестный ONNX испорчен: его bytes отсутствуют.

<a id="f222"></a>

### F222 — W2-C-F03, S02, source intent.

- Исходный локатор: [W2-C-F03](_WORK/W2_C_RESULT.md), строка36; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S121](SOURCES.md#s121)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- **[F222](RAW_FACTS.md#f222), [S121](SOURCES.md#s121), source intent.** v8.3.0 создаёт dummy `(batch,3,H,W)`, задаёт Detect `dynamic/export/format`, делает два dry-run, затем `torch.onnx.export` с явным opset, constant folding, именами `images`/`output0` (для detection). При dynamic отмечены N,H,W и output anchor count. Это поддерживаемый путь экспортёра; не доказанная поддержка dynamic LinQ. Его `simplify=True` использует onnxslim0.1.34, исключение лишь логируется — флаг не гарантирует, что итог упрощён.

<a id="f223"></a>

### F223 — W2-C-F04, S03, source intent.

- Исходный локатор: [W2-C-F04](_WORK/W2_C_RESULT.md), строка37; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S122](SOURCES.md#s122)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- **[F223](RAW_FACTS.md#f223), [S122](SOURCES.md#s122), source intent.** Для обычного, не end2end Detect, `forward` строит feature heads, а при inference вызывает `_inference`; export возвращает `y`. `_inference` включает flatten по batch, concat, split box/classes, DFL, decode, умножение stride и class sigmoid. Поэтому noNMS output — decoded pre-NMS predictions; термин «raw» допустим только с явным определением этой границы.

<a id="f224"></a>

### F224 — W2-C-F05, S04, source intent.

- Исходный локатор: [W2-C-F05](_WORK/W2_C_RESULT.md), строка38; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S123](SOURCES.md#s123)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- **[F224](RAW_FACTS.md#f224), [S123](SOURCES.md#s123), source intent.** DFL v8.3.0 берёт `b,_,a`, reshape в `(b,4,c1,a)`, transpose(2,1), softmax(dim=1), фиксированную 1×1 convolution с индексными весами и reshape `(b,4,a)`. Это конкретная область для inventory и stagewise численного сравнения. Нет bytes → нет утверждения, что конкретный экспорт содержит именно ONNX Softmax/Conv с конкретными names/attrs: exporter и optimizers могут изменить представление.

<a id="f225"></a>

### F225 — W2-C-F06, S05, source intent + inference.

- Исходный локатор: [W2-C-F06](_WORK/W2_C_RESULT.md), строка39; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S124](SOURCES.md#s124)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- **[F225](RAW_FACTS.md#f225), [S124](SOURCES.md#s124), source intent + inference.** `make_anchors` зависит от feature h,w через arange/meshgrid, формирует coordinates и stride tensors; `dist2bbox` выполняет split/chunk и арифметику. Следовательно, смена только input dim у статического файла не доказывает обновления anchor/grid constants. Полноценный повторный экспорт на новом H/W с parity — различающий тест.

<a id="f226"></a>

### F226 — W2-C-F07, S06, source intent.

- Исходный локатор: [W2-C-F07](_WORK/W2_C_RESULT.md), строка40; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S125](SOURCES.md#s125)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- **[F226](RAW_FACTS.md#f226), [S125](SOURCES.md#s125), source intent.** v8.3.200 ONNX exporter выбирает `NMSModel(self.model,self.args)` при `args.nms`; при dynamic удаляет anchor axis из dynamic output mapping для NMS. Это versioned отличие от v8.3.0 ONNX path. Не выводить из этого поддержку ONNX NMS LinQ или произвольных dynamic H/W: даже здесь output и input annotations надо проверять в фактическом файле.

<a id="f227"></a>

### F227 — W2-C-F08, S07, source intent.

- Исходный локатор: [W2-C-F08](_WORK/W2_C_RESULT.md), строка41; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S126](SOURCES.md#s126), [S127](SOURCES.md#s127)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- **[F227](RAW_FACTS.md#f227), [S126](SOURCES.md#s126), [S127](SOURCES.md#s127), source intent.** YOLOv5 v7.0 detection экспорт имеет `(images,output0)`, dynamic input N/H/W, output dynamic N/anchors по axis1; Detect включает anchor/grid decode и conf/objectness channels. Конкретный v7.0 source не содержит DFL-путь v8 Detect. Это даёт иной кандидат для локализации head проблемы, но не доказывает, что vendor `yolo5s` benchmark использовал v7.0. v7.0 ONNX `simplify` использует onnx-simplifier≥0.4.1, а не onnxslim.

<a id="f228"></a>

### F228 — W2-C-F09, S08, standard semantics.

- Исходный локатор: [W2-C-F09](_WORK/W2_C_RESULT.md), строка42; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S128](SOURCES.md#s128), [S129](SOURCES.md#s129), [S130](SOURCES.md#s130)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- **[F228](RAW_FACTS.md#f228), [S128](SOURCES.md#s128), [S129](SOURCES.md#s129), [S130](SOURCES.md#s130), standard semantics.** Для Resize13 важны не только `op_type`, но mode, coordinate_transformation_mode, nearest_mode, scales vs sizes и их dtype; schema имеет defaults nearest/half_pixel/round_prefer_floor. Softmax13 имеет axis default -1. Reshape allowzero отличает трактовку 0. Поэтому inventory должен сохранять отсутствующие/присутствующие attrs и effective schema version. Не приписывать эти default values реальному YOLO файлу до чтения bytes.

<a id="f229"></a>

### F229 — W2-C-F10, S10, source configuration.

- Исходный локатор: [W2-C-F10](_WORK/W2_C_RESULT.md), строка43; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S131](SOURCES.md#s131), [S132](SOURCES.md#s132)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- **[F229](RAW_FACTS.md#f229), [S131](SOURCES.md#s131), [S132](SOURCES.md#s132), source configuration.** В проверенных yaml YOLOv8 и YOLO11 v8.3.0 есть `nn.Upsample` nearest×2 и Concat axis1, затем Detect. Это привязывает проверку Resize/Concat к конкретной архитектурной конфигурации вместо общего списка NPU-рисков. YAML не является ONNX inventory и не доказывает attributes, rank или lowering.

<a id="f230"></a>

### F230 — W2-C-F11, S01, source intent.

- Исходный локатор: [W2-C-F11](_WORK/W2_C_RESULT.md), строка44; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S055](SOURCES.md#s055), [S048](SOURCES.md#s048)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- **[F230](RAW_FACTS.md#f230), [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), source intent.** Build использует `tpu_framework.onnx_to_tf` или fallback import `onnx_direct.onnx_to_tf`, пробует try_simplify True/False/без аргумента, затем RegularModel с GraphDef; это два Python namespace одного предполагаемого TF seam, а не доказательство нового ONNX-native frontend. Broad exceptions скрывают исходную причинность; журнал надо сохранять отдельно по попыткам. По batch автор создаёт отдельные программы через `network.set_batch` для 1/8; это не dynamic batch одного executable.

<a id="f231"></a>

### F231 — W2-C-F12, K008 boundary.

- Исходный локатор: [W2-C-F12](_WORK/W2_C_RESULT.md), строка45; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), [S121](SOURCES.md#s121), [S122](SOURCES.md#s122), [S123](SOURCES.md#s123), [S124](SOURCES.md#s124), [S125](SOURCES.md#s125), [S126](SOURCES.md#s126), [S127](SOURCES.md#s127), [S128](SOURCES.md#s128), [S129](SOURCES.md#s129), [S130](SOURCES.md#s130), [S003](SOURCES.md#s003), [S002](SOURCES.md#s002), [S131](SOURCES.md#s131), [S132](SOURCES.md#s132)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


- **[F231](RAW_FACTS.md#f231), K008 boundary.** В этом build нет доказанного Q/DQ import path: исходный ONNX конвертируется в TF, затем собственный RegularModel calibrate/quantize. Ветвь `except TypeError: calibrate(...)` может изменить effective вызов; QDQ/готовый INT8 ONNX надо считать отдельным неустановленным frontend feature, не заменой calibration. Что именно означает percentile, W2-C не установил; это предмет W2-F. Нет оснований объявлять per-channel/asymmetric activation support.

<a id="f232"></a>

### F232 — Матрица кандидатов и минимальных различающих тестов

- Исходный локатор: [W2-C-MATRIX-9](_WORK/W2_C_RESULT.md), строка47; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), [S121](SOURCES.md#s121), [S131](SOURCES.md#s131), [S132](SOURCES.md#s132), [S128](SOURCES.md#s128), [S129](SOURCES.md#s129), [S130](SOURCES.md#s130), [S122](SOURCES.md#s122), [S126](SOURCES.md#s126), [S127](SOURCES.md#s127), [S125](SOURCES.md#s125)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Матрица кандидатов и минимальных различающих тестов

В графе столбца «узел» перечислены **области, выведенные из указанного source**, а не инвентарь отсутствующих ONNX files. Ни одна строка не имеет статуса actual LinQ import/compile. Риск означает неизвестное, способное изменить результат, а не установленный запрет.

| Кандидат/граница | Узел/атрибут, который проверять в bytes | Доказательство/версия | Риск | Минимальный различающий тест после доступа |
|---|---|---|---|---|
| Авторский YOLOv8s decoded/noNMS | Все domains/opsets/IR, первые реальные Resize attrs, DFL subgraph, Split/Concat axes, shape constants | [S055](SOURCES.md#s055), [S048](SOURCES.md#s048); upstream [S121](SOURCES.md#s121)–05 только пример v8.3.0 | У автора ultralytics не pinned, нет graph/log; статическое input patch не гарантирует shapes | Получить ровно авторский ONNX+версии; unchanged export → converter; сравнить все outputs с ORT до PTQ. При первом error извлечь реально падающий subgraph, сохранив константы |
| Тот же candidate, размер входа | reshape shape tensors, anchors/grids/strides, output dimensions | [F221](RAW_FACTS.md#f221)/[F225](RAW_FACTS.md#f225) | Противоречивые static constants при смене H/W | Повторно экспортировать на втором H/W; сравнить с тем же H/W в PyTorch. Отдельно проверить input-only patched файл как контроль; не отправлять его в final build без parity |
| Тот же candidate, batch | batch-dependent reshape и внутренние tensors | [S055](SOURCES.md#s055), [S048](SOURCES.md#s048)/[F230](RAW_FACTS.md#f230); [S121](SOURCES.md#s121)/[F222](RAW_FACTS.md#f222) | Compile batch8 и runtime dynamic N — разные возможности | Отдельные static1/static8 exports с одинаковым H/W; отдельно compile set_batch 1/8 из поддержанного baseline; сравнить порядок восьми разных inputs/outputs. Dynamic N тестировать отдельным файлом и отдельной программой |
| YOLOv8/YOLO11 v8.3.0 model configs | nearest upsample, concat axis1; фактические Resize scales/sizes и coordinate attrs | [S131](SOURCES.md#s131), [S132](SOURCES.md#s132) и [S128](SOURCES.md#s128), [S129](SOURCES.md#s129), [S130](SOURCES.md#s130) | Ошибка интерполяции/shape может пройти checker | Extract настоящий Resize subgraph; координатная ramp/checkerboard input, численное сравнение converter с ORT. Не перебирать все существующие ONNX Resize modes |
| YOLOv8 standard Detect decoded/noNMS | DFL: actual reshape/transpose/softmax axis/conv, dtype | [S122](SOURCES.md#s122)–04 | Точность/понижение DFL неизвестны, noNMS не устраняет их | Сохранить outputs до/после DFL из exact model; float converter parity; затем PTQ/TLM. Если падает этот участок — отдельный wrapper до DFL + host decode с проверкой полного эквивалентного результата |
| YOLO5s v7.0, если model_stack выберет именно его | grid/anchor decode, output axis, objectness; actual elementwise/reshape ops | [S126](SOURCES.md#s126), [S127](SOURCES.md#s127) | Иной контракт чем v8; vendor yolo5s version неизвестна | Exact weights/export manifest; ORT decoded output; попытка unchanged import. Не переносить parser/postprocess v8 на выход `(N,A,5+nc)` без чтения metadata |
| YOLO11 OBB | Angle path и box decode; реальные trig/reshape attrs только из OBB bytes | [S122](SOURCES.md#s122) OBB class; vendor family claim не bytes | Detection support не доказывает OBB или конкретный YOLO11l | Сперва запросить точный успешный OBB artifact/exporter/log у автора/поставщика; затем unchanged import/parity. До этого не объявлять actual Sin/Cos nodes по названию OBB |
| NMS-on-graph variant | Actual NMS/topk/slices/control-flow и output contract | [S125](SOURCES.md#s125) v8.3.200, явный wrapper | Версионное изменение export path; lowering неизвестен | После noNMS baseline экспорт той же модели той же версией с nms=True; diff inventories, isolated import, сверка NMS tie/class semantics и detections |
| External INT8/QDQ | QuantizeLinear/DequantizeLinear/QLinear* только если присутствуют в bytes; scale dtype/axis | [F231](RAW_FACTS.md#f231): текущих доказательств LinQ import нет | Неизвестно, распознаёт ли frontend quantized ONNX или требует float+vendor PTQ | Сначала получить ответ/schema реального SDK; потом один matched float/QDQ subgraph с одинаковой quantization. Не тратить full model training на непроверенный путь |


## W2-D — W2-D — modern detector route и custom-class adapter

<a id="f233"></a>

### F233 — S01/S02, source/history.

- Исходный локатор: [W2-D-F01](_WORK/W2_D_RESULT.md), строка26; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S133](SOURCES.md#s133), [S049](SOURCES.md#s049), [S060](SOURCES.md#s060)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F233](RAW_FACTS.md#f233) — [S133](SOURCES.md#s133)/[S049](SOURCES.md#s049), [S060](SOURCES.md#s060), source/history.** Новая полная история default branch не обнаружила опубликованных `.onnx/.qm/.tpu` либо results в `models/artifacts/experiments`: targeted `git log --all -- ...` пуст. В текущем tree этих закрывающих artifacts нет; [S133](SOURCES.md#s133) releases/tags/issues пусты. Это существенно сильнее проверки одного shallow checkout, но не исключает чужой private server, удалённые ветки либо неопубликованные logs. Полный history mirror и GIT_HISTORY_INSPECTION.json сохранены. V8 exporter/build появляются в history commit `f91c66b...`12.03.2026; дальнейшая история просмотренных файлов не добавляет success logs. Отсутствие лога не доказывает невозможность модели.

<a id="f234"></a>

### F234 — S02/S04, author-reported status.

- Исходный локатор: [W2-D-F02](_WORK/W2_D_RESULT.md), строка28; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S049](SOURCES.md#s049), [S060](SOURCES.md#s060), [S135](SOURCES.md#s135)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F234](RAW_FACTS.md#f234) — [S049](SOURCES.md#s049), [S060](SOURCES.md#s060)/[S135](SOURCES.md#s135), author-reported status.** Current RUN_SCENARIO завершает detection на vendor tiny_yolo3 и отмечает done для HP1M/HPD1M. Более ранний commit17.03 прямо разделял valid quality и INVALID MLPerfqps400. Поэтому current фраза, что VALID ожидается приqps2000, не заменяет raw loadgen summary. Для custom YOLOv8 author-reported done в найденных status notes не установлено. Нет причины объявлять весь репозиторий нерабочим из-за незавершённого modern route, равно как нет причины приписывать modern route успех Tiny.

<a id="f235"></a>

### F235 — S03/S09, новая контрпроверка альтернативы v8.

- Исходный локатор: [W2-D-F03](_WORK/W2_D_RESULT.md), строка30; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S134](SOURCES.md#s134), [S002](SOURCES.md#s002), [S140](SOURCES.md#s140)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F235](RAW_FACTS.md#f235) — [S134](SOURCES.md#s134)/[S002](SOURCES.md#s002), [S140](SOURCES.md#s140), новая контрпроверка альтернативы v8.** Исторический `export_yolov5su_to_onnx.py` действительно default `yolov5su.pt`, `from ultralytics import YOLO`, imgsz640/opset13/dynamic false; передаёт format/опсет/dynamic/imgsz, но не pin версии и не явный nms flag. Quantize ведёт ONNX→onnx_to_tf→RegularModel.calibrate/quantize→qm; compile→Network→compiler.compile_→TpuProgram; runner импортирует modern `ultralytics.utils.nms`, принимает84/85 и COCO80. Это ещё один source skeleton того же автора, не classic5+N success evidence. Upstream называет v5u objectness-free. Exact old ONNX bytes отсутствуют: из имени нельзя доказать nodes/output, но путать его с classic vendor yolo5s недопустимо.

<a id="f236"></a>

### F236 — S05, новое уточнение независимой линии.

- Исходный локатор: [W2-D-F04](_WORK/W2_D_RESULT.md), строка32; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S136](SOURCES.md#s136)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F236](RAW_FACTS.md#f236) — [S136](SOURCES.md#s136), новое уточнение независимой линии.** Университетская аннотация говорит о ранее записанных стендовых измерениях, повтор которых при подготовке работы ограничен недоступностью стенда. YOLO11l obb20FPS относится к этой линии; основная опубликованная quality evaluation — регрессия координат, не PPE detection. Точные weights/exporter/SKU/batch/input precision/runtime/timing boundary и raw protocol не доступны из metadata. Источник независим от repo по автору/публикации; независимость самого bench от vendor измерений неизвестна. Нельзя превращать его в custom YOLO11 horizontal-detection success или quality evidence. Это опровергает чрезмерный тезис «современный YOLO существует только в vendor family list», но не замыкает наш route.

<a id="f237"></a>

### F237 — S06/S07/S08, versioned source, K006.

- Исходный локатор: [W2-D-F05](_WORK/W2_D_RESULT.md), строка34; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S137](SOURCES.md#s137), [S138](SOURCES.md#s138), [S139](SOURCES.md#s139)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F237](RAW_FACTS.md#f237) — [S137](SOURCES.md#s137)/[S138](SOURCES.md#s138)/[S139](SOURCES.md#s139), versioned source, K006.** Modern NMS v8.3.0 и8.3.200 предполагает BCN: `nc = nc or (prediction.shape[1]-4)`; split `(4,nc,extra)`, class max; objectness multiply отсутствует. Classic v5v7.0 предполагает BNC, `nc=shape[2]-nm-5`, candidate objectness, затем `x[:,5:] *= x[:,4:5]`. Поэтому modern NMS не распознаёт old85 как 5+80. Если transpose old85 в BCN и оставить nc0 — будет81 класс, objectness станет class0. Если передать nc80 — objectness всё ещё class0, исходные class0..78 сдвинутся, последний class79 попадёт в extra. Простой `nc=80` проблему не решает. При v8 с81 настоящим классом85 каналов корректны, то есть число85 само по себе не ошибка.

<a id="f238"></a>

### F238 — S02/S06/S07/S10, contract.

- Исходный локатор: [W2-D-F06](_WORK/W2_D_RESULT.md), строка36; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S049](SOURCES.md#s049), [S060](SOURCES.md#s060), [S137](SOURCES.md#s137), [S138](SOURCES.md#s138), [S141](SOURCES.md#s141)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F238](RAW_FACTS.md#f238) — [S049](SOURCES.md#s049), [S060](SOURCES.md#s060)/[S137](SOURCES.md#s137)/[S138](SOURCES.md#s138)/[S141](SOURCES.md#s141), contract.** Для standard Detect v8.3.0 export/noNMS выход decoded `(B,4+nc,A)` с xywh в координатах padded input и class sigmoid, без отдельного objectness; DFL/decode/stride уже внутри. A зависит от фактических feature maps, не от nc, стандартный640 обычно8400. Не sigmoid повторно, не DFL/decode повторно. Противоположный raw-conv multihead export — другой manifest и отдельный decode. Pose/seg/OBB имеют extra и иной decoder; 4+nc правило только для plain detection.

<a id="f239"></a>

### F239 — S02, actual limited helper test.

- Исходный локатор: [W2-D-F07](_WORK/W2_D_RESULT.md), строка38; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual host helper/mock execution; no native SDK/device; limits in record.

- Sources: [S049](SOURCES.md#s049), [S060](SOURCES.md#s060); [S172](SOURCES.md#s172)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F239](RAW_FACTS.md#f239) — [S049](SOURCES.md#s049), [S060](SOURCES.md#s060), actual limited helper test.** SCHEMA_PROBE.py AST-извлекает именно normalizer из pinned source, подставляет shape-only object и выполняет стандартным Python. `(1,5/6/7,8400)` custom nc1/2/3 отвергнуты; `(1,85,8400)` принят; `(1,6,84)` ошибочно трансформирован в `(1,84,6)`, потому что84 распознано как channels. `(1,84,84)` неоднозначен и молча принят. Это выполненный probe Python helper без numpy, модели, NMS, SDK и устройства. Счётный counterexample old2: obj.1, cls[.9,.2] → корректный score.09/class0, modern interpretation → score.9/class1. При threshold.25 ошибка меняет и наличие detection. Числовая иллюстрация выведена из source, не исполнявшийся torch NMS test.

<a id="f240"></a>

### F240 — S06/S07, дополнительная граница.

- Исходный локатор: [W2-D-F08](_WORK/W2_D_RESULT.md), строка40; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S137](SOURCES.md#s137), [S138](SOURCES.md#s138)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F240](RAW_FACTS.md#f240) — [S137](SOURCES.md#s137)/[S138](SOURCES.md#s138), дополнительная граница.** Обе версии NMS имеют shortcut `prediction.shape[-1]==6` → готовые BNC detections. Для обычного full detector A велик, однако tiny synthetic probe сA6 попадёт в чужую ветку даже при правильном nc. Поэтому golden synthetic tensors для проверки этих функций должны иметь A≠6 или проверять этот shortcut отдельно. У v8.3.200 `end2end=False` не отключает shape[-1]==6 shortcut. Нельзя решить контракт только перестановкой осей. Результаты NMS могут изменяться на ties и max_nms/max_det/time limit; thresholds и package/backend нужно фиксировать.

<a id="f241"></a>

### F241 — S02/S06, adapter source.

- Исходный локатор: [W2-D-F09](_WORK/W2_D_RESULT.md), строка42; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S049](SOURCES.md#s049), [S060](SOURCES.md#s060), [S137](SOURCES.md#s137)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F241](RAW_FACTS.md#f241) — [S049](SOURCES.md#s049), [S060](SOURCES.md#s060)/[S137](SOURCES.md#s137), adapter source.** Runner imports `ultralytics.utils.nms`, а v8.3.0 NMS расположен в utils.ops. Поэтому просто pin8.3.0 без изменения import не даёт working runner. `load_io_names` при любом override сразу возвращает пару overrides и теряет второй name из summary; malformed/missing JSON молча переводит в heuristic mode. `pick_output` выбирает первый rank≥3. На multihead/pose может быть выбран неверный tensor. На custom evaluation COCO80_TO_91 и range guard дают неверный category_id или отбрасывают cls≥80. Такие ошибки не ловит successful runtime call.

<a id="f242"></a>

### F242 — Спецификация adapter и planned patch list

- Исходный локатор: [W2-D-MATRIX-10](_WORK/W2_D_RESULT.md), строка56; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S133](SOURCES.md#s133), [S049](SOURCES.md#s049), [S060](SOURCES.md#s060), [S134](SOURCES.md#s134), [S135](SOURCES.md#s135), [S136](SOURCES.md#s136), [S137](SOURCES.md#s137), [S138](SOURCES.md#s138), [S139](SOURCES.md#s139), [S002](SOURCES.md#s002), [S140](SOURCES.md#s140), [S141](SOURCES.md#s141)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Спецификация adapter и planned patch list

Один model manifest, владелец model_stack; host adapter обязан прочитать его до inference. Обязательные поля: task/variant, weights+ONNX+compiled hashes, exporter repo commit/package versions/export call, nc и упорядоченные names, train-id→evaluation-category-id, tensor names/dtypes/layout/shapes, output schema enum, bbox representation/units, decode/sigmoid/DFL/objectness/NMS boundary, quant output scale/zero point только по actual runtime contract, preprocess/color/range/resize/padding, compiled batch/target. Одних nc/name модели недостаточно.

1. Заменить84/85 heuristic на explicit `schema` и layout. Для `decoded_xywh_class_prob` принимать только channels4+nc, transpose только если manifest BNC. Для classic `decoded_xywh_obj_class_prob` принимать5+nc и использовать pinned v5 NMS либо явно проверенный conversion; не присваивать extra каналу смысл objectness автоматически. Post-NMS BNC6 — отдельный schema, не повторный NMS. Неоднозначная/неизвестная shape, неверный nc, лишние outputs — fail with descriptor dump.
2. Выбирать output по точному manifest name; summary имена проверять против actual tensor_descriptions, merge input/output overrides независимо. Не переходить молча к первому rank≥3 при отсутствии metadata. Для undecoded multiscale heads требовать все named tensors/anchors/strides и отдельный decoder.
3. Pin совместимый NMS source/package/import; передавать nc явно для modern plain detection, agnostic/multi_label/max_det/max_nms/conf/iou явно. Для v8.3.0 import изops; для v8.3.200 изnms. Это примеры проверенных вариантов, не требование именно этих пакетов. Проверить strict detection-only output `(k,6)` после NMS. Не добавлять sigmoid/objectness product в4+nc route; не терять objectness product в5+nc.
4. Убрать COCO80_TO_91 как default для custom; использовать manifest category map. Train class index0 может соответствовать category_id17 — mapping должен быть explicit. Метрики PPE определяются датасетом, не именами COCO. Хранить model_class_id, semantic label и evaluation_category_id отдельно.
5. Inverse letterbox использовать metadata именно каждого подготовленного frame; сначала xywh→xyxy в input pixels, затем remove pad/divide gain, agreed clipping, затем output format. Не умножать повторно stride. Не предполагать normalized coordinates по range values. Не менять текущий clipping/maximg-1 или small-box cutoff≤1 без согласования evaluator; эти параметры тоже могут влиять на AP.
6. Проверять batch count/order, finite values, dtype и actual output dequantization. Не угадывать масштабы uint8/int8. Пустой результат считать корректным только после этих checks; shape/API success не доказывают class correctness. Для parity clone output до NMS: проверенные NMS изменяют box coordinates in place.

Это спецификация изменений, не внесённый production patch. Unicode issue повторно не исследовалась; она не закрывает перечисленные contract defects.


## W2-E — W2-E — TinyYOLO3: provenance, three-path parity and exact I/O

<a id="f243"></a>

### F243 — What the vendor path actually proves

- Исходный локатор: [W2-E-F01](_WORK/W2_E_RESULT.md), строка32; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S142](SOURCES.md#s142)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F243](RAW_FACTS.md#f243) — What the vendor path actually proves

Type: source_code + unknown. Checked: pinned local source and new exact-name network searches, no vendor execution.

Repository commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140` (sherstpasha, 2026-04-03) provides `scr/detection/run_tiny_yolo3_vendor.py`, `run_tiny_yolo3_accuracy.py`, and `RUN_SCENARIO.txt` §§3.4/5. The code references an external `.tpu`, not a download endpoint or bundled artifact. The filename’s `128x128` must **not** be interpreted as image resolution: runner explicitly defaults416. Its compiler/hardware meaning is not established here. The filename `b8` is also weaker evidence than actual program metadata.

The runner’s discovery logic tries input aliases, missing-input exception text and auxiliary descriptors. For output decode it first tries rank3 tensors; if no candidate succeeds it takes the first two rank4 tensors and sorts their spatial height. These are heuristics, not a schema. Rank3 combined mode presumes pixel xywh and raw object/class logits, applying sigmoid to both; raw-head mode presumes actual raw logits and standard anchors. A supplied graph may already have sigmoid/decode/another coordinate convention. API success or plausible boxes do not validate those presumptions. It also always maps class indices through COCO80→91 even though `--num-classes` is configurable. This TinyYOLO seam reinforces K006; it does not resolve the separate Ultralytics runner investigation. [[S142](SOURCES.md#s142)]

<a id="f244"></a>

### F244 — Exact public artifacts now obtained

- Исходный локатор: [W2-E-F02](_WORK/W2_E_RESULT.md), строка40; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation + source_code.

- actual_check: binary/weights inspection; F05: actual ONNX Runtime 1.31.0 CPU b1/b2 + diagnostic raw-head derivative; no LinQ.

- Sources: [S143](SOURCES.md#s143), [S144](SOURCES.md#s144), [S145](SOURCES.md#s145), [S146](SOURCES.md#s146), [S147](SOURCES.md#s147), [S148](SOURCES.md#s148), [S149](SOURCES.md#s149), [S150](SOURCES.md#s150)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F244](RAW_FACTS.md#f244) — Exact public artifacts now obtained

Type: local_observation. Checked: actual HTTPS downloads, hash/size verification, protobuf inspection.

Downloaded `tiny-yolov3-11.onnx` from the exact HF endpoint used by the repo downloader; HF revision `80e90901d9fb3738092b3f09a0f457ed9e420d08` (lastModified2025-09-30). Its SHA256 and length equal the GitHub LFS pointer at onnx/models commit `c5cae0f1942c8d7727372c7b1f6b485aa39e4421`. This establishes that the mirror file inspected is the Model Zoo object, not merely another similarly named model. Pinned LFS URL and pointer saved. [[S143](SOURCES.md#s143), [S144](SOURCES.md#s144)/[S145](SOURCES.md#s145), [S146](SOURCES.md#s146), [S147](SOURCES.md#s147)]

Downloaded pjreddie `yolov3-tiny.weights`, 35,434,956 bytes, and cfg, 1,915 bytes. Weight header interpreted as int32 `[0,2,0,32013312,0]` (version0.2.0 + 64-bit seen field). `COMPARE.py` consumes exactly all35,434,956 bytes using the cfg convolution channel topology. The cfg live bytes were separately verified against Darknet commit `f6afaabcdf85f77e7aff2ec55c020c0e297c77f9`. [[S148](SOURCES.md#s148), [S149](SOURCES.md#s149), [S150](SOURCES.md#s150)]

No large datasets downloaded. Two model files total about71MB. Source/helper dependencies were used only for host inspection; no vendor SDK/native lib installed.

<a id="f245"></a>

### F245 — Checkpoint lineage established; not full numerical graph equivalence

- Исходный локатор: [W2-E-F03](_WORK/W2_E_RESULT.md), строка50; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation + source_code.

- actual_check: binary/weights inspection; F05: actual ONNX Runtime 1.31.0 CPU b1/b2 + diagnostic raw-head derivative; no LinQ.

- Sources: [S142](SOURCES.md#s142), [S143](SOURCES.md#s143), [S144](SOURCES.md#s144), [S145](SOURCES.md#s145), [S146](SOURCES.md#s146), [S147](SOURCES.md#s147), [S148](SOURCES.md#s148), [S149](SOURCES.md#s149), [S150](SOURCES.md#s150), [S151](SOURCES.md#s151), [S152](SOURCES.md#s152), [S153](SOURCES.md#s153), [S090](SOURCES.md#s090)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F245](RAW_FACTS.md#f245) — Checkpoint lineage established; not full numerical graph equivalence

Type: local_observation + inference. Checked: all13 conv kernel arrays and final biases compared directly, not model-name inference.

Model Zoo Conv initializers `conv2d_1/kernel:0` through `conv2d_13/kernel:0` are OIHW and exactly equal the corresponding contiguous kernel arrays read from the hashed pjreddie checkpoint. Both output biases `conv2d_10/bias:0`, `conv2d_13/bias:0` also exactly equal. Thus the alternative “these public branches use entirely unrelated learned conv checkpoints” is falsified for these downloaded bytes. This evidence does **not** extend to vendor `.tpu`.

The11 BN layers in binary have means0/variances1, transformed scales/offsets, epsilon≈1e−6. Strict exporter sets original gamma/beta/mean/variance on Keras BatchNormalization without explicit epsilon. A host algebra probe using source variance+`.001` gives maximum absolute effective-scale difference `9.5367431640625e-06`, offset difference≤`9.5367431640625e-07` across all layers. This supports transformed BN lineage, but `.001` was a tested hypothesis, not a pinned installed TensorFlow runtime contract. No claim of all-parameter byte equality or actual strict export numerical equality is made. BN epsilon/default version and exact execution still belong in the future parity test. Detailed per-layer measurements: `PARAMETER_COMPARISON.JSON`; code: `COMPARE.py`.

<a id="f246"></a>

### F246 — Fine anchors differ, with direct source provenance

- Исходный локатор: [W2-E-F04](_WORK/W2_E_RESULT.md), строка58; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation + source_code.

- actual_check: binary/weights inspection; F05: actual ONNX Runtime 1.31.0 CPU b1/b2 + diagnostic raw-head derivative; no LinQ.

- Sources: [S145](SOURCES.md#s145), [S146](SOURCES.md#s146), [S147](SOURCES.md#s147), [S148](SOURCES.md#s148), [S149](SOURCES.md#s149), [S150](SOURCES.md#s150), [S151](SOURCES.md#s151)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F246](RAW_FACTS.md#f246) — Fine anchors differ, with direct source provenance

Type: source_code + local_observation. Checked: real protobuf initializer values, graph connections, pinned upstream decoder.

Model Zoo initializer `TFNodes/yolo_evaluation_layer_1/Const:0` contains coarse anchors `[[81,82],[135,169],[344,319]]`. `.../Const_2:0` contains fine `[[23,27],[37,58],[81,82]]`, then Reshape_6 and Mul_7 multiply fine `Exp_1` outputs. This is not a documentation typo: it changes decoded sizes. For zero wh logits, e.g. first fine anchor width is23 instead of10 and height27 instead of14. The same raw predictions therefore yield different boxes before NMS.

`qqwweee/keras-yolo3` commit `e6598d13c703029b2686bc2eb8d5c09badf42992` (Phillip K.S. Chu,2018-07-30), `yolo3/model.py:196`, uses two-layer mask `[[3,4,5],[1,2,3]]`; cfg instead explicitly uses3,4,5 then0,1,2. Upstream source explains the binary’s decoder lineage. It is safer to call this **a proven recipe difference from the Darknet checkpoint cfg**, not claim an independently benchmarked accuracy defect. Model Zoo headline mAP0.331 is a card claim based on original Darknet model; it was not remeasured here and is not proof of this exact full-graph recipe’s AP. [[S145](SOURCES.md#s145), [S146](SOURCES.md#s146), [S147](SOURCES.md#s147)/[S148](SOURCES.md#s148), [S149](SOURCES.md#s149), [S150](SOURCES.md#s150)/[S151](SOURCES.md#s151)]

<a id="f247"></a>

### F247 — Actual binary I/O, embedded limits and batch failure

- Исходный локатор: [W2-E-F05](_WORK/W2_E_RESULT.md), строка66; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: local_observation + source_code.

- actual_check: binary/weights inspection; F05: actual ONNX Runtime 1.31.0 CPU b1/b2 + diagnostic raw-head derivative; no LinQ.
- Protocol clarification: latest saved HOST_PROBE_RESULT.JSON timestamp is2026-10-23T02:02:11.352325Z; HOST_PROCESS_RESULT returncode0. Earlier time in branch narrative may refer to an earlier run. b2 remains a recorded Squeeze failure; see [F333](RAW_FACTS.md#f333).

- Sources: [S143](SOURCES.md#s143), [S144](SOURCES.md#s144), [S152](SOURCES.md#s152)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F247](RAW_FACTS.md#f247) — Actual binary I/O, embedded limits and batch failure

Type: local_observation. Checked: protobuf plus CPUExecutionProvider ONNX Runtime1.31.0, tiny synthetic input, no timing benchmark.

The actual inputs use symbolic batch and unspecified H/W, despite card’s inference example `(1,3,416,416)`. Output annotations are `[1,?,4]`, `[1,80,?]`, `[1,?,3]`; third output is **int32**, after graph Cast of NMS indices. At416,b1 actual outputs are `yolonms_layer_1 (1,2535,4)`, `yolonms_layer_1:1 (1,80,2535)`, `yolonms_layer_1:2 (1,0,3)` on the chosen constant image.2535 =3×13²+3×26². No detections at embedded .6 on a synthetic image is not an accuracy result.

The original binary accepts b1 with float `image_shape=[[321,641]]`. b2 with `(2,3,416,416)` and `(2,2)` shape input fails at `TFNodes/yolo_evaluation_layer_1/Squeeze`: dimension0 must equal1 instead of2. Therefore **do not batch this full graph by trusting symbolic N**. Only the tested b2/geometry combination is an actual observed failure; it is not a general statement that every derivative/raw backbone is batch1-only.

Embedded NMS receives scalar initializers `max_output_size=20`, `iou_threshold=.5`, `layer.score_threshold=.6000000238418579`. The repo decoder can apply a second score threshold and global max300 afterward, but changing CLI `--iou-thres` never changes this node. Per-class cap20 also differs from global top300. Outputs boxes/scores remain dense candidates; NMS indices choose entries. Do not feed these output tensors to a raw-head decoder or apply sigmoid again. [[S143](SOURCES.md#s143), [S144](SOURCES.md#s144)/[S152](SOURCES.md#s152)]

`HOST_PROBE.py` writes `HOST_PROBE_RESULT.JSON` and `GOLDEN_SYNTHETIC_RAW.NPZ`. It also creates an **in-memory head-only derivative** by retaining ancestors of two raw conv outputs, dropping image_shape input and exposing coarse/fine outputs. That derivative succeeded with finite `(1,255,13,13)` and `(1,255,26,26)` outputs. It is a diagnostic reference, not the original full graph and not an exported strict model. Initial shell command reported exit1 because native stderr for the intentionally caught b2 failure was redirected by PowerShell; the script completed and recorded both cases. A repeat with Python subprocess capture established actual process returncode0 (`HOST_PROCESS_RESULT.JSON`), preserving native stderr separately (`HOST_PROBE_STDERR_NATIVE.TXT`). No success claim for b2; it remains a caught/recorded runtime failure.

<a id="f248"></a>

### F248 — Color and geometry need separate contracts

- Исходный локатор: [W2-E-F06](_WORK/W2_E_RESULT.md), строка78; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation + source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S148](SOURCES.md#s148), [S149](SOURCES.md#s149), [S150](SOURCES.md#s150), [S153](SOURCES.md#s153), [S090](SOURCES.md#s090)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F248](RAW_FACTS.md#f248) — Color and geometry need separate contracts

Type: source_code + primary_documentation + inference. Checked: official upstream sources and inspected helpers; no vendor color test.

Darknet’s `image.c`/`image_opencv.cpp` load RGB: OpenCV path calls `rgbgr_image` after cv2-style loading, and stb path deinterleaves native RGB; unit range. The strict exporter loads the same kernel channels and never implements a color permutation. Thus its BGR sidecar is not supported by the primary checkpoint recipe. Model Zoo’s PIL recipe creates RGB padding and OpenVINO’s own model description explicitly calls original ONNX input RGB, while its **converted OpenVINO** variant is BGR. This is concrete evidence that color order is artifact-specific; quoting the converted OpenVINO setting for the ONNX input would be wrong. [[S148](SOURCES.md#s148), [S149](SOURCES.md#s149), [S150](SOURCES.md#s150)/[S153](SOURCES.md#s153)]

Repo vendor runner reverses cv2 channels; repo ORT helper does not, and does not read/use its `image_color_order` field in preprocessing. Both strict and downloader sidecars say BGR. For original Model Zoo bytes the ORT recipe therefore conflicts with its primary RGB recipe. **For vendor binary we cannot choose RGB over BGR**: it could be separately transformed, exported from another source, or require different calibration/input handling. Need the vendor manifest/golden tensor or a known-good reference output; a photograph looking plausible under RGB is insufficient.

Geometry also differs independently. Repo: OpenCV linear, rounded new dimensions, fill114. Model Zoo card: PIL bicubic, truncated new dimensions, fill128. Original Darknet letterbox: its own resize and fill`.5` in float, not exactly128/255. Do not call all these the same “letterbox”. Model Zoo graph’s inverse correction uses rounded new shape and floating half-offset like its linked Keras source. For original H321,W641 at416, floor pre yields H208 while rounded inverse geometry yields H208 too; other noninteger cases can differ by a pixel, and odd padding can differ by a half pixel from integer paste. Tests must log actual new shape and pad, not just `scale`.

The old MIT `yolo_correct_boxes` is yet another geometry: builds **xyxy**, then scales directly by the supplied tuple twice; it has **no letterbox offset/scale inverse**. Caller must supply dimensions in the matching xy order for that formula; we did not find a TinyYOLO-specific preprocessor proving the vendor caller’s intended order. This helper is not interchangeable with Model Zoo yxyx/original-image boxes or the new runner’s letterbox inverse. [[S090](SOURCES.md#s090)]

<a id="f249"></a>

### F249 — Old MIT helper cannot be used unchanged as b8/custom-N decoder

- Исходный локатор: [W2-E-F07](_WORK/W2_E_RESULT.md), строка90; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S090](SOURCES.md#s090)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F249](RAW_FACTS.md#f249) — Old MIT helper cannot be used unchanged as b8/custom-N decoder

Type: source_code. Checked: actual archive source and LICENSE, not installed/executed with TensorFlow.

`iva_applications-11.0.1/src/iva_applications/tiny_yolo3/postprocess.py:55–56` asserts first dictionary value shape `(1,13,13,255)`, second `(1,26,26,255)`; it relies on dictionary insertion order instead of explicit known output names. The wrapper accepts `num_classes`, but255 forces80 classes with3 anchors if reshape is to be valid. Removing asserts alone is insufficient: shared `yolo_boxes_and_scores` flattens boxes to `[-1,4]` and scores to `[-1,num_classes]`, and NMS operates per class with no separate batch identity. b8 could merge detections from different images. Source uses coarse anchors3:6 and fine0:3, xy sigmoid, wh exp, sigmoid object/classes, product scores. Defaults score.5,IoU.5,max20 per class. This is a versioned host-code reference only. The archive has no TinyYOLO-specific preprocess module; generic yolo2 RGB resize is a different module, not evidence of this `.tpu` contract. [[S090](SOURCES.md#s090)]

<a id="f250"></a>

### F250 — Rights are layer-specific and conflicting model metadata needs preservation

- Исходный локатор: [W2-E-F08](_WORK/W2_E_RESULT.md), строка96; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S145](SOURCES.md#s145), [S146](SOURCES.md#s146), [S147](SOURCES.md#s147), [S148](SOURCES.md#s148), [S149](SOURCES.md#s149), [S150](SOURCES.md#s150), [S153](SOURCES.md#s153), [S090](SOURCES.md#s090)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F250](RAW_FACTS.md#f250) — Rights are layer-specific and conflicting model metadata needs preservation

Type: source_code / primary artifact license observation; not legal advice or current SDK permission grant.

Actual `iva_applications-11.0.1/LICENSE` has copyright2020 IVA Technologies and MIT terms including use/modify/distribute subject to retaining notice. This positively resolves permission for that helper source; no metadata UNKNOWN/null overrides the actual license file. It does not license vendor weights, `.tpu`, native runtime or SDK.

HF mirror card frontmatter says Apache-2.0, but its own License section says MIT; onnx/models TinyYOLO README has MIT SPDX and MIT section, while root LICENSE is Apache2. OpenVINO attribution points to root Apache2. Preserve this inconsistency instead of declaring one unqualified global license for every artifact. Darknet source root declares public domain; the direct checkpoint URL has no separately supplied weight license in the fetched response. None of these grants establishes a right to redistribute an unprovided proprietary vendor `.tpu` or shared SDK image. Before public submission include actual distribution terms/notices for each supplied layer; reading public code here does not require waiting for permission to inspect it. [[S145](SOURCES.md#s145), [S146](SOURCES.md#s146), [S147](SOURCES.md#s147)/[S148](SOURCES.md#s148), [S149](SOURCES.md#s149), [S150](SOURCES.md#s150)/[S153](SOURCES.md#s153)/[S090](SOURCES.md#s090)]

<a id="f251"></a>

### F251 — Three-path manifest

- Исходный локатор: [W2-E-MATRIX-11](_WORK/W2_E_RESULT.md), строка13; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_observation + unknown.

- actual_check: mixed per cell: actual public ONNX bytes,13conv comparison, ORT1.31.0 CPU b1 success/b2 failure; vendor.tpu/strict export/LinQ not run.

- Sources: [S142](SOURCES.md#s142), [S143](SOURCES.md#s143), [S144](SOURCES.md#s144), [S145](SOURCES.md#s145), [S146](SOURCES.md#s146), [S147](SOURCES.md#s147), [S148](SOURCES.md#s148), [S149](SOURCES.md#s149), [S150](SOURCES.md#s150), [S151](SOURCES.md#s151), [S152](SOURCES.md#s152), [S153](SOURCES.md#s153), [S090](SOURCES.md#s090)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Three-path manifest

“Runner” below means inspected source, not the unknown actual vendor binary interface. “Strict” means the pinned exporter source plus the fetched exact cfg/checkpoint, not an exported artifact created here.

| Seam | Vendor `.tpu` path | Strict Darknet export path | ONNX Model Zoo actual downloaded binary | Parity verdict |
|---|---|---|---|---|
| Artifact/provenance | `tiny_yolo3_b8_o5_128x128_asic.tpu`; external author path `/home/smallpc_user/linq_files/tpu_programs/...`; no supplied bytes/hash/original weights | pjreddie cfg SHA256 `84eb7a675ef87c906019ff5a6e0effe275d175adb75100dcb47f0727917dc2c7`; weights SHA256 `dccea06f59b781ec1234ddf8d1e94b9519a97f4245748a7d4db75d5b7080a42c` | SHA256 `f715cc2d99740d22d312777e20d9de2b2ecdc250155be8fd3752ce7e8b823521`; 35,511,756 bytes, identical to pinned GitHub LFS object | Vendor provenance unknown. Public conv checkpoint lineage established, full graph equality false |
| Input | Runner defaults `input_1:0`, float32 NHWC `(8,416,416,3)`, unit float | Export signature `input_1`, float32 NHWC `(None,416,416,3)` by default; optional static batch; opset13 | `input_1`: float32 `['N',3,'','']`; `image_shape`: float32 `['N',2]`; producer keras2onnx1.6.0, opset11, IR6 | Layout transpose can be made exact; second input/batch semantics differ |
| Color | Runner swaps cv2 BGR→RGB; no proof binary expects it | Sidecar literally says BGR; graph does not swap channels; raw pjreddie weights loaded unchanged | Card recipe creates RGB PIL image; kernel channel order exactly equals pjreddie weights; no first-channel reversal embedded | Strict BGR metadata is unsupported by upstream convention. Vendor RGB/BGR unresolved; RGB is not universal |
| Resize/pad | Runner shared helper: OpenCV INTER_LINEAR, round size, pad114, integer left/top | ORT helper uses same OpenCV recipe and leaves BGR; metadata color ignored | Card: PIL BICUBIC, floor `int` scaled dimensions, pad128, integer paste offset | Different input tensors even after color fix; card and graph themselves have floor/round geometry subtlety |
| Head outputs | Runner heuristically accepts combined rank3 or first two rank4 tensors, sorts by grid height; no actual output names/shapes available | Last conv tensors before `[yolo]`, inferred NHWC `(B,13,13,255)` and `(B,26,26,255)` at416; no decode/NMS | Internal raw conv names `convolution_output1` coarse, `convolution_output` fine, NCHW; public outputs are boxes/scores/NMS indices | Common raw boundary is constructible; public graph boundaries differ |
| Anchors | Runner assumes six standard anchors and masks `3,4,5|0,1,2` | Same cfg/masks | Coarse `(81,82),(135,169),(344,319)`; fine `(23,27),(37,58),(81,82)` | Fine-head decode non-parity proven in actual binary |
| Decode | Runner raw-head mode applies xy sigmoid+grid×stride, exp wh×anchors, sigmoid obj/classes, product score | Export stops at logits; external decoder required | Decode and inverse letterbox embedded; six Sigmoid, two Exp nodes and image_shape geometry | Same formula family but anchors and boundary differ; double decode/sigmoid prohibited |
| NMS | Runner multi-label class-aware torchvision `batched_nms`, CLI score `.001`, IoU `.45`, global max300 | External runner same assumptions | Embedded `NonMaxSuppression`: score `.6000000238418579`, IoU `.5`, max20 **per class**; public indices int32 | Host CLI `.001/.45` cannot recover candidates already discarded by graph NMS |
| Batch | Runner default8, last sample repeated to fill incomplete batch; no binary metadata proof | Default dynamic batch; actual export not run | CPU probe b1 succeeds, b2 fails at Squeeze of `image_shape` | Symbolic `N` not evidence of b8-capable full graph |
| Original-image boxes | Runner subtracts stored integer pad, divides scale, clips to width−1/height−1; rejects dimensions≤1 | Same external head decoder if chosen | Graph already corrects to original pixels, yxyx; host should select boxes by indices, without second inverse letterbox | Original boxes cannot be compared until one exact geometry/NMS policy is shared |


## W2-F — W2-F — quantizer semantics и калибровка с контролем качества

<a id="f252"></a>

### F252 — data-dependent quantization установлена документально, scope percentile нет.

- Исходный локатор: [W2-F-F01](_WORK/W2_F_RESULT.md), строка29; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F252](RAW_FACTS.md#f252) — data-dependent quantization установлена документально, scope percentile нет.** Тип primary_documentation, [S030](SOURCES.md#s030). Описание квантования отделяет чтение графа/весов от определения порога по calibration tensor; затем создаются SoftwareNetwork с quantization/rescale и квантованными весами, HardwareNetwork как TF-модель операций TPU. Одновременно описание аргумента percentile относится к весовым коэффициентам. Это не логическое доказательство ошибки текста: процедура в целом может быть data-dependent, а один параметр weights-only. Нельзя заменить это привычной интерпретацией percentile histogram activations. Точная формула, выбор абсолютных значений/знаков, denominator и смысл 100.0 неизвестны.

<a id="f253"></a>

### F253 — современный пример не сохраняет доказательство effective percentile.

- Исходный локатор: [W2-F-F02](_WORK/W2_F_RESULT.md), строка31; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S048](SOURCES.md#s048), [S154](SOURCES.md#s154), [S155](SOURCES.md#s155)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F253](RAW_FACTS.md#f253) — современный пример не сохраняет доказательство effective percentile.** Тип source_code + inference, [S048](SOURCES.md#s048)/[S154](SOURCES.md#s154), [S155](SOURCES.md#s155). В L275–278 любой TypeError от вызова с `percentile=args.percentile` приводит к повтору без параметра. Это ловит как unsupported keyword, так и TypeError внутри принятого вызова; первый проход мог уже менять состояние объекта. L304–326 summary сохраняет sample count, preprocess, shapes, `.qm` и compiled paths, но не requested/effective percentile, threshold dump, exception/retry flag или quantizer version. Наличие `.qm`/summary и успех всего builder не позволяют отличить применённый аргумент от default retry. Текущий HEAD не исправляет это. Нужны fail-closed вызов без blanket retry и запись фактического пути.

<a id="f254"></a>

### F254 — thresholds передаются отдельно, но публичной serialization schema нет.

- Исходный локатор: [W2-F-F03](_WORK/W2_F_RESULT.md), строка33; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S048](SOURCES.md#s048), [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F254](RAW_FACTS.md#f254) — thresholds передаются отдельно, но публичной serialization schema нет.** Тип source_code/unknown, [S048](SOURCES.md#s048). `thresholds = regular_model.calibrate(...)` → `regular_model.quantize(thresholds)` → `quantized_model.save(file_dir=..., file_name=...)`. Пример не показывает dtype, shape, naming, содержимое thresholds, собственный save/load thresholds или повторную quantization после перезапуска. `.qm` в [S030](SOURCES.md#s030) содержит топологию и числовые данные для compiler, но это не обещание экспорта исходных calibration statistics или portability thresholds между версиями/графами. Старый guide `save(file_path)` и новый sample `save(file_dir,file_name)` нельзя механически смешивать. Схема `.qm`, version policy и effective parameter dump текущего SDK unknown.

<a id="f255"></a>

### F255 — существует точная историческая формула выходного helper, её область узкая.

- Исходный локатор: [W2-F-F04](_WORK/W2_F_RESULT.md), строка35; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S089](SOURCES.md#s089)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F255](RAW_FACTS.md#f255) — существует точная историческая формула выходного helper, её область узкая.** Тип source_code, [S089](SOURCES.md#s089). `get_output_scale` читает `fpga_data.pickle`, фиксированный ключ `output_node_1`, берёт `pos_scale`, `pos_shift`, возвращает `scale * 2. ** shift`; `dequantize` возвращает `data * scale`. Docstrings называют int16 scale/int8 shift и float16 result, но код не проверяет фактический dtype, не округляет/клиппирует и не устанавливает granularity. У нас нет pickle, поэтому shape значений неизвестен. Это не общая формула нынешнего LinQ `.tpu`, не доказательство symmetric quantizer и не предписание добавить умножение к FULL output. Применение такого helper к уже user-format выходу способно повторить преобразование.

<a id="f256"></a>

### F256 — RAW file kind и ProcessingMode являются разными осями.

- Исходный локатор: [W2-F-F05](_WORK/W2_F_RESULT.md), строка37; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S063](SOURCES.md#s063)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F256](RAW_FACTS.md#f256) — RAW file kind и ProcessingMode являются разными осями.** Тип source_code, [S063](SOURCES.md#s063). `_is_raw_program` открывает ZIP `metadata.json`; `_is_raw_metadata` эвристически считает отсутствующий `user_dtype` признаком raw и комментирует address/size-only metadata. Независимо `ProcessingMode` задаёт RAW=0, PRE_PROCESS=1, POST_PROCESS=2, FULL=3, а `_run` передаёт число native `tpu_run_inference`. `_program._is_raw` управляет размерами и reshape возврата; mode не переписывает этот флаг. Поэтому одно `mode=RAW` само не доказывает, что Python output будет int8 тензором правильной формы или что текущий nonraw артефакт допускает безопасную такую подачу. Сначала нужен native contract конкретного release.

<a id="f257"></a>

### F257 — Python output conversion не является численным dequantization.

- Исходный локатор: [W2-F-F06](_WORK/W2_F_RESULT.md), строка39; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S063](SOURCES.md#s063)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F257](RAW_FACTS.md#f257) — Python output conversion не является численным dequantization.** Тип source_code/inference, [S063](SOURCES.md#s063). `_load_inference` передаёт адрес ndarray как `POINTER(c_uint8)`; это представление буфера, не `astype(uint8)` данных. Для nonraw `_get_inference` делает byte view в metadata `user_dtype` и reshape в `user_shape`; для raw — reshape по `ddr_word_len`. В Python-функции `view` нет scale multiplication, transpose или preprocessing. Где native/compiled artifact выполняет эти операции, этот слой не раскрывает. Из `POINTER(c_uint8)` нельзя выводить внешний uint8 contract. FULL — запрос режима к native API, не доказательство размещения всех операций на TPU.

<a id="f258"></a>

### F258 — float reference, quantized TF и runtime имеют разные документированные boundary adapters.

- Исходный локатор: [W2-F-F07](_WORK/W2_F_RESULT.md), строка41; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation + source_code + unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030), [S048](SOURCES.md#s048), [S063](SOURCES.md#s063)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F258](RAW_FACTS.md#f258) — float reference, quantized TF и runtime имеют разные документированные boundary adapters.** Тип primary_documentation/source_code, [S030](SOURCES.md#s030)/[S048](SOURCES.md#s048)/[S063](SOURCES.md#s063). Для TF quantized graph [S030](SOURCES.md#s030) использует `rescale` на входе и выходе; TLM получает исходные подготовленные данные с переименованием tensor→op, hardware example также использует исходную подготовку. Новый сторонний runner подаёт float32. Это согласуется с user/raw boundary processing, но не раскрывает современную численную формулу. Ошибку parity сначала локализовать на I/O: применять `rescale` к TF quantized graph там, где это требует конкретный API; не переносить его автоматически на FULL runtime. Формула native transform, host/device location и RAW↔FULL golden pairs unknown.

<a id="f259"></a>

### F259 — TLM полезен как отдельный численный checkpoint, не гарантированно доступен.

- Исходный локатор: [W2-F-F08](_WORK/W2_F_RESULT.md), строка43; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation + unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F259](RAW_FACTS.md#f259) — TLM полезен как отдельный численный checkpoint, не гарантированно доступен.** Тип primary_documentation/unknown, [S030](SOURCES.md#s030). Guide описывает HardwareNetwork и TLM execution, печатает estimated execution time, сравнивает вероятный класс. Это не текущая спецификация bit-exactness, не layerwise compare API и не валидация accuracy малых СИЗ. Актуальные export intermediate tensors, compare tool, численные допуски и TLM availability не найдены. Если текущего TLM нет, нельзя блокировать весь проект ожиданием этой стадии; пропуск фиксируется как невозможность разделить compiler/runtime error на два участка.

<a id="f260"></a>

### F260 — historical float16 flag не устанавливает QAT или mixed precision H1M.

- Исходный локатор: [W2-F-F09](_WORK/W2_F_RESULT.md), строка45; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S156](SOURCES.md#s156)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F260](RAW_FACTS.md#f260) — historical float16 flag не устанавливает QAT или mixed precision H1M.** Тип source_code/unknown, [S156](SOURCES.md#s156). MobileNet quantize script использует `quantize_graph ... --float16_capacity_control=true`. Это конкретная первичная зацепка об управляющем параметре старого FPGA toolchain; без help/source quantizer его функция не раскрыта. Он не является доказательством float16 arithmetic современного LinQ, current activation clipping или пути QAT/QDQ. Нового первичного QAT/QDQ примера/контракта не найдено, поэтому обширный поиск общих ONNX quantization tutorials не предпринимался.

| Вопрос | Установленный минимум | Что остаётся unknown / запрещённый перенос |
|---|---|---|
| Что калибруется | Порог по данным calibration tensor; модель имеет quantized weights | Как соотносятся weight/activation thresholds и percentile |
| percentile=100 | Такой default в guide/sample | Это не доказательство формулы `max(abs(x))`, percentile scope или допустимого диапазона |
| Granularity | Нет найденной спецификации | per-channel/per-tensor, axes, signedness, zero-point |
| Arithmetic | Guide в терминах связывает quantization с scaling/rounding | tie-breaking, saturation, accumulator/bias precision, residual rescale |
| Save/load | `.qm` сохранение показано; thresholds отдельный объект перед quantize | Threshold serialization, determinism, cross-version compatibility, current load API |
| Boundary | rescale для quantized TF; user metadata и native mode для historical runtime | Все scale/cast/layout/packing stages, host/device location |
| Comparison | Graph outputs и TLM demo описаны | Текущий layerwise compare tool, численная гарантия TLM↔device |
| QAT/QDQ | Первичного current path нет | Не говорить «не поддерживается»; не предлагать заранее INT8 ONNX как установленную замену |

<a id="f261"></a>

### F261 — Единый staged evaluation для малых СИЗ (K020)

- Исходный локатор: [W2-F-MATRIX-12](_WORK/W2_F_RESULT.md), строка94; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: engineering_recommendation grounded in primary documentation.

- actual_check: planned staged evaluation; no SDK calibration/compile/device run.

- Sources: [S019](SOURCES.md#s019), [S030](SOURCES.md#s030), [S048](SOURCES.md#s048), [S154](SOURCES.md#s154), [S155](SOURCES.md#s155), [S063](SOURCES.md#s063), [S089](SOURCES.md#s089), [S156](SOURCES.md#s156)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Единый staged evaluation для малых СИЗ (K020)

### Общая спецификация и разделение данных

Data/evaluation owner ведёт **один** manifest с image hash, camera ID, source clip, timestamp/time block, scene/light conditions, split, annotations и классами. Calibration, tuning validation и финальный holdout разделять по камерам и/или цельным непересекающимся time/clip blocks, исключая соседние кадры и повторные изображения между split. Для фиксированной камеры оценивать также отдельный поздний временной блок; для переноса между камерами — held-out камеры. Нельзя обещать одновременно camera-held-out при единственной камере: фактическую доступность фиксировать. Не отбирать только яркие кадры с крупными людьми. В calibration покрыть малые/дальние предметы, перекрытия, контраст, пустые сцены, наличие и отсутствие relevant СИЗ; эти страты должны реально присутствовать в данных, а не быть выдуманными классами кейса.

Числа100/500 — кандидаты budget experiments, не норма достаточности. Для сравнения размеров использовать вложенные subsets с сохранением покрытия и hash списков. Отдельный validation для выбора calibration/percentile/score threshold; final holdout после выбора. Если данных мало и есть только calibration+eval, любые итерации по eval считать tuning и получить новый независимый holdout перед заявлением качества. Достаточность оценивать по стабильности критических метрик/стратифицированному покрытию при добавлении данных и доступному budget, без обещания универсального sample count.

Один `MODEL_MANIFEST` у export/compile owner: weights/export graph hashes, exporter/options/opset, names/layout/static shape, preprocess, class mapping, output/decoder definition, quantizer settings+threshold artifact, compile target/preset, `.qm`/`.tpu` hashes. В роли quantization owner записывается только соответствующая часть; новые конкурирующие manifests не создавать.

### Последовательность и права вывода

| Stage / владелец | Что сравнивать и gate | Состояние сейчас; результат и ограничение |
|---|---|---|
| A. Float/export / model owner | Исходная float модель → exported ONNX → imported float graph, где доступен. Одни input tensors и raw heads, затем один decoder/NMS | Exported reference доступен без LinQ; importer может требовать SDK. Если raw/head semantics не совпадают, исправлять экспорт, не percentile. Успех не подтверждает PTQ. |
| B. PTQ/reference / quantization owner | Imported float → quantized reference с правильным boundary rescale; E-F1/F2 до sweep | Нужен SDK. Изолирует PTQ loss только при сравнимом imported float. Если imported float недоступен, разность ONNX→quant reference включает import+PTQ и так называется. |
| C. Compile / compile owner | Quant reference → optional TLM, exact compile output | Нужен SDK/TLM. Если TLM отсутствует, фиксировать skip, переходить к device с общей неопределённостью. Не делать обязательным недоступный инструмент. |
| D. Runtime / runtime owner | Reference/TLM → LinQ FULL с проверенным user I/O, E-F3 | Нужен LinQ. Расхождение только здесь требует boundary/compiler/runtime диагностики до смены calibration. Успех parity не доказывает full graph TPU coverage. |
| E. Quality / evaluation owner | Для принятых A–D те же labels, decoder/NMS, frozen thresholds и eval IDs | Можно подготовить сейчас, аппаратные outputs позже. Raw parity и итоговые accuracy — разные gates. |

Для каждого stage сохранять исходы PASS / FAIL / UNAVAILABLE / NOT_RUN, actual elapsed wall time, exit/error, stage artifacts и входную spec. Нет жёсткой выдуманной длительности компиляции. Изменение исходного float graph означает новый artifact lineage и повтор только зависимых gates. Known-good vendor sample полезен для isolating environment, но не обязательная единственная точка старта: выданный compiler+custom minimal example с reference/golden outputs способен дать проверяемый первый маршрут. Без reference успешная compilation — лишь syntax/support milestone.

### Метрики, memory/time и решение

Фиксировать AP50, AP50:95 и recall по классам; отдельно размерную страту мелких СИЗ с **явным определением размеров**. COCO AP_small и маленький объект после resize — не тождественные понятия: дополнительно указать bbox width/height в source и network pixels. Сохранить support counts и случаи miss по каждому классу/страте/камере; если наблюдений мало, вывод нестабилен, нулевые ошибки не доказывают достаточность. Для нарушения «отсутствие СИЗ» нужны person↔PPE association/правила и отдельная violation-level false negative/false positive оценка с владельцем rules; object recall не равен качеству определения нарушения.

Общие preprocessing, decoding, score/NMS и labels зафиксировать для оценки численной потери. Обязательно проверить NMS **внутри самого ONNX**, output stage и anchor mask/order: одинаковые CLI flags не обеспечивают одинаковый cutoff или decoder, когда один граф уже обрезал кандидаты. Если raw heads недоступны, фиксировать стадию after-NMS и сравнивать с тем же встроенным NMS на другом пути; потерю кандидатов от embedded score cutoff не называть PTQ loss. Это особенно важно для мелких СИЗ с низким confidence. Если позже меняются score thresholds, сообщать отдельно: это tuning меняет рабочую точку, а не восстанавливает прежние raw outputs. Допуски AP/recall/нарушений согласовать по полному заданию; сейчас численный «приемлемый loss» не установлен. Не выбирать победителя только по overall mAP, скрывающему респиратор/очки на дальнем человеке.

Связанный handoff от root/W2-E получен 01:59 UTC: сообщено об embedded NMS и anchor mask discrepancy в конкретном tiny-yolov3-11. Его численные literals в этой ветке самостоятельно не проверены; подробное primary evidence принадлежит W2-E. Здесь он учтён как требование проверки artifact-level NMS/decoder, а не как новый W2-F установленный факт.

Регистрировать calibration wall time, max RSS **включая subprocess tree** выбранным средством ОС, peak accelerator/GPU memory если действительно используется, memmap size/disk free, sample count, shape/dtype, preprocessing time и quantization time раздельно. При500×3×640×640×4 backing file =2,457,600,000 bytes≈2.29GiB, при100≈0.458GiB; это расчёт backing storage, не peak RAM. Memmap не гарантирует streaming calibrate: SDK может копировать целый tensor и хранить intermediate activations. Сохранять resource log с timestamps, OOM/error и частичным результатом; не приписывать quantizer wall time подготовке изображений.

Decision tree: A failed → исправить model mapping; A passed/B failed → подтверждённая PTQ loss, после E-F1 менять calibration composition/size или документированный parameter по одному; B passed/D failed → сначала user/raw/layout/compile/runtime; A–D passed/E bad → исходная модель/data/rules или недостаточная task quality. Если E-F1 не установил scope/effective percentile, остановить percentile sweep, сохранить baseline default и продолжить независимые стадии. QAT начинать только при фактическом SDK path и measured PTQ bottleneck; generic QDQ export не является подтверждённым обходом. Срок переключения пути задаёт общий 45-hour budget команды и фактические логи, не выдуманное vendor compile время.


## W2-G — W2-G — `.tpu`, Python/native boundary и tensor contract

<a id="f262"></a>

### F262 — современная версия не восстановлена

- Исходный локатор: [W2-G-F01](_WORK/W2_G_RESULT.md), строка29; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_metadata.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S064](SOURCES.md#s064), [S157](SOURCES.md#s157), [S082](SOURCES.md#s082), [S019](SOURCES.md#s019), [S159](SOURCES.md#s159)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F262](RAW_FACTS.md#f262) — современная версия не восстановлена

Тип `primary_metadata` + `network_observation`; [S064](SOURCES.md#s064), [S157](SOURCES.md#s157)/[S082](SOURCES.md#s082), [S019](SOURCES.md#s019)/[S159](SOURCES.md#s159). Current PyPI project release —15.0.24. Внешний runtime16.18.6 из benchmark2026 не обязан совпадать с version Python distribution, поэтому разницу чисел нельзя выдавать за incompatibility или устаревание API. Не получены current `METADATA`, binding source, C headers, SONAME, driver/firmware version matrix, serialized model format version или sample metadata. Это искомые missing fields, а не неизвестные названия методов, которые следует угадывать. [S064](SOURCES.md#s064), [S157](SOURCES.md#s157) public Python source не восстанавливает native ABI.

<a id="f263"></a>

### F263 — Python видит user/raw representation, но не реализует numerical codec

- Исходный локатор: [W2-G-F02](_WORK/W2_G_RESULT.md), строка33; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F263](RAW_FACTS.md#f263) — Python видит user/raw representation, но не реализует numerical codec

Тип `source_code`, [S065](SOURCES.md#s065), `Program.__init__`273–291, `_load_inference`427–457, `_get_inference`460–484. Native `tpu_get_program_info` возвращает JSON; Python читает `inputs['1']`, `outputs['2']`, `hardware_parameters`. Для ordinary program output interpreted as `user_dtype`, reshaped to `user_shape`; для raw program — uint8 array reshape `(-1,ddr_word_len)`. `_convert_from_uint8_to_user_dtype`487–495 — views, а не quantization/dequantization arithmetic. Он поддерживает dtype string containing `int`, float16 и float32; это не полная type capability matrix TPU. Pointer type `uint8*` — байтовый transport, не доказательство int8 semantic input.

Source size lookups: `tpu_get_input_size(program,index,is_raw)`, `tpu_get_output_size(...)`. Единицы в usage выглядят как bytes: выход выделен bytearray длиной tensor_size, затем dtype view. **Current native contract размера/выравнивания не документирован**; это вывод из исторического usage, а не универсальное соглашение. В Python input `tensor_size` вычислен, но не используется для проверки nbytes.

<a id="f264"></a>

### F264 — available historical schema шире W1 summary

- Исходный локатор: [W2-G-F03](_WORK/W2_G_RESULT.md), строка39; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S158](SOURCES.md#s158)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F264](RAW_FACTS.md#f264) — available historical schema шире W1 summary

Тип `source_code`, [S158](SOURCES.md#s158) `_get_tensor_description`76–104. Для user tensor reader требует именно:

| Поле | Реальное использование старым converter | Что остаётся неизвестным |
|---|---|---|
| `address`, `size` | `_to_raw_old` оставляет только эти два поля per tensor | Units/address space/alignment/limits/current schema version |
| `user_shape`, `padding` | Из padding pairs и user dimensions строится boolean shape mask | Validity отрицательных padding/current convention, dynamic dimension support |
| `user_order`, `tpu_order` | Передаются в TensorDescription | Значения/axis mapping для actual compiled model; layout нельзя вывести из имени модели |
| `user_dtype`, `tpu_dtype` | Lookup через отдельные STR_TO_* enums | Exact enum table и supported combinations отсутствующего tpu_tlm_is/current SDK |
| `tpu_shape` | Передаётся в TensorDescription | Packing/strides/block layout actual target |
| `scales` | Каждое значение преобразуется float, затем tuple | Direction multiplication/division, scalar/per-axis scope, rounding/saturation и relation к quantizer thresholds |
| `anchor` | Передаётся в TensorDescription | Значение и семантика именно tensor codec. Нельзя отождествлять с YOLO detection anchors |
| `hardware_parameters.cache_word_len`, `ddr_word_len` | Выбор historical target codec | Current accepted targets/format version |

Historical `_get_tpu_parameters` знает ровно пары cache/ddr:128/32→`128x128`,64/16→`64x64`,64/64→`64x64_fpga`; другие пары → NotImplementedError. Это ограничение debug converter15.0.24, не support matrix современных ускорителей.

`Codec.encode` вызывает `tpu_tlm_is.models.iotools.tpu_encode`, `decode` — `tpu_decode`. Actual numerical implementation отсутствует, поэтому перечисленных metadata fields недостаточно для самостоятельной правильной реализации packing/scales. Наличие Python-callable codec подтверждает отдельную host-side debug conversion в этой старой библиотеке; **оно не устанавливает размещение native FULL преобразований**.

<a id="f265"></a>

### F265 — FULL/RAW enum не определяет Python buffer schema

- Исходный локатор: [W2-G-F04](_WORK/W2_G_RESULT.md), строка58; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F265](RAW_FACTS.md#f265) — FULL/RAW enum не определяет Python buffer schema

Тип `source_code`, [S065](SOURCES.md#s065) enums165–169, `Inference.__init__`336–371, `_run`373–382, `sync`387–416, raw heuristic498–518. Enum values `RAW=0`, `PRE_PROCESS=1`, `POST_PROCESS=2`, `FULL=3`; `_run` передаёт `mode.value` в `tpu_run_inference`. Код не раскрывает реализацию этих стадий или location host/device. Названия и битовый вид значений не дают права самостоятельно описать stage semantics.

Размеры `_tensor_name_to_tensor_size` вычисляются в init по `_program._is_raw`, а output decoding также проверяет `_is_raw`, **не mode**. `_is_raw_program` открывает ZIP member `metadata.json`; `_is_raw_metadata` берёт первый output region/первый tensor и проверяет отсутствие `user_dtype`, предполагая отсутствие mixed tensors. Этот heuristic не versioned schema validator.

Конвертер создаёт новую ZIP-программу с сокращённой metadata, одновременно заранее сохраняя descriptions в Codec. Поэтому file RAW — отдельное преобразование artifact/metadata, mode RAW — runtime argument. Из source нельзя заключить, что ordinary `.tpu` + `mode=RAW` автоматически выдаст корректные raw tensors через этот Python wrapper. Не доказано и обратное: native может иметь дополнительные соглашения, которых здесь нет. Нужен current reference с supported combinations program format × mode × buffer representation.

<a id="f266"></a>

### F266 — validation concern сужен, не снят

- Исходный локатор: [W2-G-F05](_WORK/W2_G_RESULT.md), строка66; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual host helper/mock execution; no native SDK/device; limits in record.

- Sources: [S065](SOURCES.md#s065), [S160](SOURCES.md#s160)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F266](RAW_FACTS.md#f266) — validation concern сужен, не снят

Тип `source_code` + `local_helper_test`; [S065](SOURCES.md#s065) `_load_inference`427–457, [S160](SOURCES.md#s160). Реально отвергается non-Mapping (`ValueError`), неизвестное имя вызывает KeyError. `_run` проверяет native return, `_check_status` — status. Поэтому тезис «вообще нет validation» неверен.

Host fake probe: float64 вместо ожидаемого float32, C-noncontiguous slice и empty input Mapping приняты Python методом без exception до fake registration. Source не проверяет exact input name set, dtype, shape, C-contiguity или nbytes. Input index mapping объединяет inputs и outputs; совпадающие имена могут перезаписать index. Это статический возможный corner case данной реализации, **не утверждение, что compiler допускает такие имена**. Native может дополнительно проверять данные, но raw pointer не несёт numpy shape/strides/dtype; current safeguards и фактическое native failure behaviour не проверены. Не подавать malformed buffers на неизвестную native library ради этого исследования.

<a id="f267"></a>

### F267 — output view и ownership: copy claim опровергнут, dangling claim не подтверждён

- Исходный локатор: [W2-G-F06](_WORK/W2_G_RESULT.md), строка72; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual host helper/mock execution; no native SDK/device; limits in record.

- Sources: [S065](SOURCES.md#s065), [S160](SOURCES.md#s160)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F267](RAW_FACTS.md#f267) — output view и ownership: copy claim опровергнут, dangling claim не подтверждён

Тип `source_code` + `local_helper_test`, [S065](SOURCES.md#s065)/[S160](SOURCES.md#s160). Historical comment говорит о copy, но actual output path: `bytearray(np.empty(...uint8))` → ctypes `from_buffer` → cast pointer → `np.ctypeslib.as_array` → dtype `.view` → reshape. Это numpy view, `OWNDATA=False`; probe менял float через pointer, и изменение видно в возвращённом array. Комментарий нельзя цитировать как доказательство output copy.

При этом probe удалил local ctx/pointer, вызвал gc и получил сохранённые `[1.25,-2.5]`; weakref показывает original pointer still alive. Array base chain `ndarray→ndarray→memoryview` удерживает buffer ownership в проверенной среде. Отсутствие `.copy()` само по себе не доказывает use-after-free. Результат не гарантирует совместимость других Python/NumPy releases, поведение native destructor или lifetime современной версии. Выходного native buffer после destroy здесь не читали: вся память создана Python. Вопрос current API «сохраняется ли array после следующего inference/session close» остаётся к документации и actual SDK test.

<a id="f268"></a>

### F268 — cleanup concern исторически конкретен, modern repair неизвестен

- Исходный локатор: [W2-G-F07](_WORK/W2_G_RESULT.md), строка78; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code + local_helper_test.

- actual_check: actual host helper/mock execution; no native SDK/device; limits in record.

- Sources: [S065](SOURCES.md#s065), [S160](SOURCES.md#s160)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F268](RAW_FACTS.md#f268) — cleanup concern исторически конкретен, modern repair неизвестен

Тип `source_code` + `local_helper_test`; [S065](SOURCES.md#s065) `Device.open`185–199, `Device.load`235–253, `Program.inference`307–312, `buffer`315–322; [S160](SOURCES.md#s160). В generators explicit destroy стоит после yield без try/finally. В mock `Device.open` normal exit вызвал destroy, injected exception — не вызвал. ExitStack вокруг `sync` не исправляет отсутствие finally внутри entered context generators. Это реальное свойство control flow15.0.24, не аппаратное измерение leak и не current SDK diagnosis.

В `Program.buffer` TODO предупреждает о нестабильности тестов, **но actual `tpu_destroy_tensor_buffer_object` включён и вызывается на normal exit**. Нельзя писать «буфер никогда не уничтожается» или считать текст2023 доказательством нынешнего crash. В этой ветке не получены modern source/release notes, опровергающие или подтверждающие сохранение проблемы. Отсутствие исправления в публичном legacy архиве не значит отсутствия исправления в current release.

<a id="f269"></a>

### F269 — исторический C++ пример не задаёт современный ABI

- Исходный локатор: [W2-G-F08](_WORK/W2_G_RESULT.md), строка84; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S075](SOURCES.md#s075)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F269](RAW_FACTS.md#f269) — исторический C++ пример не задаёт современный ABI

Тип `source_code`, [S075](SOURCES.md#s075). `util.h` включает внешний `<tpu.h>` и использует shared_ptr для TPUDevice/TPUProgram; SUT вызывает старое семейство `tpu_program_get_input_buffer`, `tpu_inference_submit`, `tpu_inference_wait`. Это уже другое API family относительно ctypes `tpu_create_*`, `tpu_run_inference`. Source даёт пример lifetime/execution flow соответствующей версии2020, но не typedef definitions, ownership contract современного `<tpu.h>` или ABI stability promise. Совпадающий vendor lineage не разрешает смешивать старые declarations с новой `.so`.

<a id="f270"></a>

### F270 — Versioned API/schema comparison

- Исходный локатор: [W2-G-MATRIX-13](_WORK/W2_G_RESULT.md), строка88; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S064](SOURCES.md#s064), [S157](SOURCES.md#s157), [S065](SOURCES.md#s065), [S158](SOURCES.md#s158), [S075](SOURCES.md#s075), [S155](SOURCES.md#s155), [S030](SOURCES.md#s030), [S082](SOURCES.md#s082), [S019](SOURCES.md#s019), [S159](SOURCES.md#s159), [S160](SOURCES.md#s160)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Versioned API/schema comparison

| Область | Historical C++2020 | Actual pytpu15.0.24 source2023 | Official guide2025 | Current Runtime16.18.6 / выдача2026 |
|---|---|---|---|---|
| API family | `TPUDevice/TPUProgram`, external tpu.h, submit/wait | Device/Program/Inference; create/run/status ctypes | Device.open/load/inference/sync | Header/source not obtained; Python package version unknown |
| Model format | `.tpu` name, compile script | ZIP, metadata.json heuristic | Framework compiled `.tpu` boundary | Format version/compatibility not obtained |
| Schema | No schema specification in harness | inputs region1/outputs region2 + user/tpu fields, hardware params | Named input/output examples | Actual sample JSON absent |
| Processing | Old harness copies sample buffer and reads typed outputs | enum passed native; Python format handling separate | Float prepared input supplied | Numerical transformations/placement unknown |
| Lifecycle | shared_ptr usage; external ownership semantics | host allocations/views and generators above | with-style usage | Repair/exception guarantees not established |

Таблица — различие доказательств, **не compatibility matrix**. Guide2025 не объявлен obsolete. Закрыть diff можно только matching current source/reference, а не сопоставлением version numbers разных компонентов.


## W2-H — W2-H — аппаратные исполнения, память и multi-device mapping

<a id="f271"></a>

### F271 — (primary_documentation, text-only):

- Исходный локатор: [W2-H-F01](_WORK/W2_H_RESULT.md), строка17; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S019](SOURCES.md#s019)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F271](RAW_FACTS.md#f271) (primary_documentation, text-only):** публичный каталог группирует HP1M-01 и -02 под HP; HPD1M-00 Active / -01 Passive под HPD; HPD1M-10 Passive / -11 Active под HPQ. Это уже прямой пример, почему префикс HPD1M без суффикса не означает ровно двухчиповую карту. [S019](SOURCES.md#s019).

<a id="f272"></a>

### F272 — (primary_documentation, text-only):

- Исходный локатор: [W2-H-F02](_WORK/W2_H_RESULT.md), строка19; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S161](SOURCES.md#s161), [S021](SOURCES.md#s021)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F272](RAW_FACTS.md#f272) (primary_documentation, text-only):** HP1M-01 p5–6: ≤35Вт, ≥750МГц, одна H1M, DDR4ECC16ГБ, два канала по8ГБ/72bit, PCIe2.0x8 Endpoint; p12 ожидает одну строку2805:0006 rev08. HP1M-02 p5–6: тот же предел мощности/частоты, одна H1M, DDR4ECC32ГБ, два канала по16ГБ/72bit, PCIe2.0x8; p14 ожидает одну такую строку. [S161](SOURCES.md#s161)/[S021](SOURCES.md#s021). Это разные документированные комплектации, без доказанной хронологии перехода01→02. В HP02 p3/p7 повторено одно и то же обозначение в двух позициях; не трактовать шаблонное дублирование как два чипа или две разные ревизии.

<a id="f273"></a>

### F273 — (primary_documentation, text-only):

- Исходный локатор: [W2-H-F03](_WORK/W2_H_RESULT.md), строка21; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S162](SOURCES.md#s162), [S023](SOURCES.md#s023)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F273](RAW_FACTS.md#f273) (primary_documentation, text-only):** HPD1M-00 Active p5–6: ≤100Вт,32ГБ,2H1M, по16ГБ на чип, каждый2×8ГБ, PCIe3.0x16; p14 — два endpoint. HPD1M-01 Passive даёт ту же структуру/предел мощности. [S162](SOURCES.md#s162)/[S023](SOURCES.md#s023). HPD active datasheet p2 даёт60/70Вт, как W1 passive datasheet. Следовательно, простая гипотеза «100Вт из-за вентилятора активной версии» не объясняет расхождение:100Вт написано и для пассивной.

<a id="f274"></a>

### F274 — (primary_documentation, text-only):

- Исходный локатор: [W2-H-F04](_WORK/W2_H_RESULT.md), строка23; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S039](SOURCES.md#s039), [S025](SOURCES.md#s025)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F274](RAW_FACTS.md#f274) (primary_documentation, text-only):** HPQ/HPD1M-11 Active p5–6: ≤150Вт,64ГБ,4H1M,16ГБ на чип,2×8ГБ на чип, PCIe3.0x16; p8PEX8747, p14 четыре endpoint2805:0006 rev08. Passive -10 также имеет4чипа/64ГБ/≤150Вт. В -11 p6 составная плата названа HPD1M-10, а встроенное ПО -11: возможная общая плата или шаблонный перенос текста, ни одно объяснение не доказано. Имя платы не является firmware/SDK compatibility manifest. [S039](SOURCES.md#s039)/[S025](SOURCES.md#s025).

<a id="f275"></a>

### F275 — (primary_documentation + inference):

- Исходный локатор: [W2-H-F05](_WORK/W2_H_RESULT.md), строка25; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F275](RAW_FACTS.md#f275) (primary_documentation + inference):** H1M↔К1945ВМ3Я прямо задано presentation p2, как уже установлено W1; это не новый неизвестный. Там PCIe controller чипа Gen3x8. Presentation p3 при этом пишет HP2.0x8 и HPD/HPQ3.0x16. Возможность контроллера и спецификация реализации карты имеют разный scope; такое различие само по себе допустимо, но не доказывает Gen3 для фактической HP. Текст p3 даёт <30/<55/<105/<1150Вт для HP/HPD/HPQ/HPS, без условий режима. Новая сетeвая текстовая копия подтверждает W1 transcription, но визуальная проверка не выполнена. [S033](SOURCES.md#s033).

<a id="f276"></a>

### F276 — (primary_documentation, text-only):

- Исходный локатор: [W2-H-F06](_WORK/W2_H_RESULT.md), строка27; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: primary_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F276](RAW_FACTS.md#f276) (primary_documentation, text-only):** Framework guide p9 `compile_(hardware_parameters,network,parameters,slicing_scheme=None)` описывает slicing_scheme как распределение тензоров в памяти микропроцессора IVA H1. `get_hw_params(tpu_type)` и пример `128x128_asic` задают отдельное понятие target. p10 второйDDR, банки кеша, сроки жизни тензоров и слайсер слоёв описываются как оптимизации размещения/конвейеров. Это полезное прямое memory-planning свидетельство, но в этих разделах нет node/device ID, межчипового канала, remote allocation или правила суммы DDR. Нельзя переименовать этот механизм в multi-chip sharding. [S030](SOURCES.md#s030).

<a id="f277"></a>

### F277 — (source_code, static inspection; not execution):

- Исходный локатор: [W2-H-F07](_WORK/W2_H_RESULT.md), строка29; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S044](SOURCES.md#s044)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F277](RAW_FACTS.md#f277) (source_code, static inspection; not execution):** pinned benchmark commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`, RUN_SCENARIO дата2026-03-25, §8 сообщает о четырёх обнаруженных на сервере `/dev/tpu3…0` и использует labelHPD1M. `run_resnet50_parallel_direct.py` L202–325: для каждого `(device,shard_path)` запускает subprocess одного `run_resnet50_accuracy.py`, передавая одинаковый `--program-path` и отдельный `--device`; ожидает все процессы, суммирует число изображений и делит на полное wall time. `run_resnet50_accuracy.py` L296–315 выбирает device и делает `Device.open(device_id)`/`load(program_path)`. Это data parallel replication. Таймер direct пути захватывает запуск и завершение subprocess; его aggregate FPS нельзя называть чистым device compute. [S044](SOURCES.md#s044). Remote bytes именно parallel_direct независимо получены и совпали с W1 SHA256.

<a id="f278"></a>

### F278 — (source_code + inference):

- Исходный локатор: [W2-H-F08](_WORK/W2_H_RESULT.md), строка31; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S063](SOURCES.md#s063)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


**[F278](RAW_FACTS.md#f278) (source_code + inference):** build_resnet50_program.py L262/L364 использует `TPU_128x128_PARAMS`, а не SKU HPD1M; один и тот же target ещё не гарантирует совместимость со всеми ёмкостями памяти/поставками. Исторический pytpu15.0.24 `_bindings.py` L180–229 перечисляет имена файлов `/dev` по regex и длине и передаёт выбранный путь native `tpu_create_device`; Python-listing не возвращает физический SKU/BDF/серийный номер. Эта старая реализация не доказывает поведение Runtime16.18.6, но демонстрирует конкретную причину не считать `list_devices()` inventory физической карты. [S063](SOURCES.md#s063).

<a id="f279"></a>

### F279 — Таблица конфликтов и текущий статус

- Исходный локатор: [W2-H-MATRIX-14](_WORK/W2_H_RESULT.md), строка33; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S019](SOURCES.md#s019), [S161](SOURCES.md#s161), [S021](SOURCES.md#s021), [S162](SOURCES.md#s162), [S023](SOURCES.md#s023), [S039](SOURCES.md#s039), [S025](SOURCES.md#s025), [S033](SOURCES.md#s033), [S030](SOURCES.md#s030), [S044](SOURCES.md#s044), [S063](SOURCES.md#s063), [S163](SOURCES.md#s163), [S164](SOURCES.md#s164), [S020](SOURCES.md#s020)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Таблица конфликтов и текущий статус

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

<a id="f280"></a>

### F280 — Mapping: что документировано и какой переход ещё надо измерить

- Исходный локатор: [W2-H-MATRIX-15](_WORK/W2_H_RESULT.md), строка48; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S019](SOURCES.md#s019), [S161](SOURCES.md#s161), [S021](SOURCES.md#s021), [S162](SOURCES.md#s162), [S023](SOURCES.md#s023), [S039](SOURCES.md#s039), [S025](SOURCES.md#s025), [S033](SOURCES.md#s033), [S030](SOURCES.md#s030), [S044](SOURCES.md#s044), [S063](SOURCES.md#s063), [S163](SOURCES.md#s163), [S164](SOURCES.md#s164), [S020](SOURCES.md#s020)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Mapping: что документировано и какой переход ещё надо измерить

| Карта/исполнение | Чипы и локальная DDR | Host-side hardware discovery из РЭ | Runtime mapping |
|---|---|---|---|
| HP1M-01 |1H1M,16ГБ=2×8 |1×2805:0006 rev08; внешнийPCIe2.0x8 |BDF↔`/dev/tpuN` не опубликовано в изученном contract |
| HP1M-02 |1H1M,32ГБ=2×16 |1×тот же ID; внешний2.0x8 |то же; ёмкость32 не выводится из ID |
| HPD1M-00/01 |2H1M,каждый16ГБ;32всего |2×тот же ID заPEX8747; внешний3.0x16 |один runtime context на выбранный путь в примере; число разрешённых contexts/quota неизвестно |
| HPQ/HPD1M-10/11 |4H1M/К1945ВМ3Я,каждый16ГБ;64всего |4×тот же ID заPEX8747; внешний3.0x16 |нужна фактическая привязка всех четырёх путей к одной карте |

Цепочка доказательства: **этикетка/серийный номер карты → upstream switch и BDF-tree → BDF чипа → driver device node → runtime device info → loaded artifact/target → inference context/request**. Таблица не утверждает установленную биекцию BDF↔node для отсутствующего драйвера. Сам PCI ID одинаков у разных исполнений и недостаточен для установления объёма памяти. Число endpoint не включает мосты/switch functions; число строк всей `lspci` нельзя сравнивать напрямую с числом чипов.


## W2-I — W2-I — современные performance claims: единицы и протокол

<a id="f281"></a>

### F281 — Original presentation: честный отрицательный результат

- Исходный локатор: [W2-I-F01](_WORK/W2_I_RESULT.md), строка21; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F281](RAW_FACTS.md#f281). Original presentation: честный отрицательный результат

[S033](SOURCES.md#s033), ООО «ХайТэк», презентация 2026, автор extraction metadata Сергей Севрюков. W2 direct `curl.exe --max-time 20 --http1.1 -k` к canonical HTTPS завершился Schannel TLS handshake failure, exit35 (05:03:23 MSK); `DIRECT_HEADERS.txt` пуст. Web open дал unavailable; screenshot PDF index3 (p4) отказал: content type не application/pdf. **PDF bytes/hash/картинки страницы не получены, actual screenshot не просмотрен.** Не повторяли бесконечно одинаковый fetch и не выдавали ответ remote agent из W2-B за просмотр.

Числа и сноска сохранены без изменения из уже имеющегося `_WORK/W1_08/presentation2026_tinyfish.json`; этот snapshot — тот же upstream source, а не новое независимое доказательство. Сноска: Intel Core i7-10700K @3.80GHz, Ubuntu24.04, Runtime16.18.6, Framework2026.8.43; методика MLCommons MLPerf. Ни сноска, ни сеть с `mlperf` в имени не являются submission ID или LoadGen log. p3 ResNet50 HP460/1046 vs p4 432,9/1112,8 остаются разными опубликованными цифрами без сопоставимого протокола.

<a id="f282"></a>

### F282 — Записи измерений сохраняют неизвестный denominator

- Исходный локатор: [W2-I-F02](_WORK/W2_I_RESULT.md), строка27; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033), [S165](SOURCES.md#s165), [S044](SOURCES.md#s044), [S017](SOURCES.md#s017), [S076](SOURCES.md#s076), [S077](SOURCES.md#s077)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F282](RAW_FACTS.md#f282). Записи измерений сохраняют неизвестный denominator

`W2_I/MEASUREMENT_RECORDS.json` содержит все14 строк p4, original decimal literals и batch, устройства названы HP/HPQ, `tested_here=false`, `evidence_type=vendor_reported_table_text_only`. Input/weights/preset/precision per-model/quality/scenario/latency statistic/boundaries/actual devices — null. Throughput unit из заголовка FPS; не установлено, какой именно image/sample/batch counter делится на какой run interval. Число batch8 не надо дополнительно умножать на8: семантика samples/sec wrapper и слайда не связана.

Показательные записи (source p4; единицы только по extraction):

| model / batch | HP FPS | HP latency ms | HPQ FPS | HPQ latency ms | denominator / tested_here |
|---|---:|---:|---:|---:|---|
| anti_spoof_mn3 /1 |1561,1|985,72|6244,4|985,72|не раскрыт /false|
| lenet5 /1 |12519,7|128,90|50078,8|128,90|не раскрыт /false|
| resnet50 /1 |432,9|2,99|1731,6|2,99|не раскрыт /false|
| resnet50 /8 |1112,8|—|4451,2|—|не раскрыт /false|
| ssd_mobilenet_v2 /1 |556,7|3,54|2226,8|3,54|не раскрыт /false|
| ssd_mobilenet_v2 /8 |428|—|1712|—|не раскрыт /false|
| yolo5s /1 |106,1|23,71|424,4|23,71|не раскрыт /false|
| yolov8n_pose /1 |104,8|21,51|419,2|21,51|не раскрыт /false|

<a id="f283"></a>

### F283 — Попытка опровергнуть typo и арифметическое HPQ

- Исходный локатор: [W2-I-F03](_WORK/W2_I_RESULT.md), строка44; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S033](SOURCES.md#s033)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F283](RAW_FACTS.md#f283). Попытка опровергнуть typo и арифметическое HPQ

Тип: arithmetic inference по [S033](SOURCES.md#s033), без устройства. У всех14 строк отношение HPQ/HP throughput=4 и одинаковые latency literals. Это совместимо и с идеальным масштабированием независимых одинаковых engines, и с расчётной экстраполяцией. При отображённой точности измеренная сумма тоже может оказаться ровно4×. По таблице метод происхождения **неразличим**.

Для batch1 `1000/FPS` не равно опубликованной latency: у anti_spoof≈0,641ms, у lenet≈0,0799ms, ResNet50≈2,310ms, YOLO5s≈9,425ms. Это не даёт права заменить источник. Если throughput измерен Offline на preloaded данных, а latency отдельным последовательным режимом с другой границей, большой разрыв логически возможен. Percentile также не равен reciprocal средней скорости. Для одной и той же последовательной нагрузки с одним outstanding запросом невозможно объяснить столь большой разрыв одним лишь обычным p90: это было бы другое, гораздо более сильное допущение, которого источник не даёт.

Диагностический product `FPS × latency_seconds` у anti_spoof≈1538,8, lenet≈1613,8; подмена ms→us сделала бы его≈1,54/1,61, как порядок ряда других строк. Это **поддерживает подозрение** ошибки единиц, но не устанавливает её. Product нельзя называть measured concurrency: это потребовало бы средней latency и одного steady-state workload. При разных сценариях/percentile Little's-law интерпретация неприменима. Оставлены все исходные значения.

Снижение SSD batch8 throughput также не исправляем: batching не гарантирует рост, в частности может менять memory placement/pipeline/preset. Причину этого конкретного результата без logs не установили. Не выдаём эту правдоподобную причину за факт.

<a id="f284"></a>

### F284 — Новый современный primary protocol: только смысл методики

- Исходный локатор: [W2-I-F04](_WORK/W2_I_RESULT.md), строка54; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S165](SOURCES.md#s165)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F284](RAW_FACTS.md#f284). Новый современный primary protocol: только смысл методики

[S165](SOURCES.md#s165) — MLCommons policy commit `d3eba2f21026d868ad65cdcad2bb81e4a17ce3d3`, committer date2026-08-20. Скачаны original source bytes, SHA256 `94c69f01f1e0be24dc057180af6db878d1f5339fd31d54cbe5c386f8e198ce08`; actual HTTP200 02:04:29UTC. `MLCOMMONS_RULES.adoc:133–150,401–420,633–658`.

Policy различает последовательный Single Stream (следующий query после ответа; primary metric p90 early-stopping latency estimate), Server с Poisson requests и ограничением tail latency, Offline с передачей всех samples одним query и throughput. Latency определяется от scheduled pass query до reply. Разрешённая sample-independent resize/channel reorder/crop/normalization может быть untimed. Следовательно generic «MLPerf включает полную загрузку/предобработку/end-to-end камеры» неверно; детали SUT/LoadGen необходимы.

Это не утверждение, что vendor использовал именно этот commit, строго исполнил эти правила или подал официальную submission. Rules2026 не подставлены в logs2020, исторический FPGA повторно не исследовался. Нового primary locator современной LinQ MLCommons submission не найдено; не делаем вывод, что submission никогда не существовала.

<a id="f285"></a>

### F285 — Публичный repo содержит возможный протокол масштабирования, но не результаты

- Исходный локатор: [W2-I-F05](_WORK/W2_I_RESULT.md), строка62; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S044](SOURCES.md#s044)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F285](RAW_FACTS.md#f285). Публичный repo содержит возможный протокол масштабирования, но не результаты

[S044](SOURCES.md#s044), `sherstpasha/linq-cv-bench`, pinned commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`. GitHub API tree `truncated=false`,60 tracked tree entries, ни одного пути experiments/mlperf_log/results_summary/accuracy.txt; `REPO_RELEASES.json=[]`; единственная public branch main указывает тот же commit. Публичная HTML main также не содержит results attachment. Это scope данного tree/releases/branches, **не всех исторических commits, пользовательского диска или скрытых releases**. API bytes/hash/time сохранены.

`.gitignore:31–43` явно исключает JSON, ONNX/PT/weights/H5, artifacts/, experiments*/, explanatory-results Markdown. Это не доказательство, что они никогда не были tracked, но объясняет, почему инструкция «сохранить results_summary.json» не равна публикации результата. Для закрытия запроса нужны actual logs/build_summary/.tpu hash из разрешённой автором поставки, а не повторный запуск git search.

`scr/classification/run_resnet50_parallel_mlperf.py:105–131,138–192,235–268`:

- Запускает `mlperf -s offline -m performance -p <program> -q <effective_qps>` для каждого процесса. При переданных devices **реально добавляет `--dev <device>`**, хотя help:34 говорит «for reporting only». Actual support этого CLI binary не проверена: бинарник не получен.
- Пытается наблюдать `/proc/<pid>/fd`→`/dev/tpu*` каждые0,2s. Отсутствие наблюдения не доказывает отсутствие исполнения; открытый fd не доказывает полноту graph execution. Это схема source, не collected observation.
- При всех VALID суммирует `Samples per second` отдельных процессов, усредняет по valid repeats, speedup делит на measured baseline. **Не N×baseline.** `wall_sec` от запуска до завершения процессов сохранён отдельно и не является знаменателем этой суммы. Такая сумма rates отдельных интервалов ещё не синхронное `total_completed/common_window` измерение whole system.
- `RUN_SCENARIO.txt:392–491` сообщает четыре device paths и1/2/3/4-process runs с O5 и vendor `.tpu`. Это authored instructions/reported inventory, не published outcome и не mapping four devices↔oneHPQ. Значение `128x128_asic` в имени `.tpu` не объявлять image input128×128.

Repo custom ResNet50 имеет отдельный exact source contract: exporter `ResNet50_Weights.IMAGENET1K_V2`, shape `(batch,224,224,3)`, NHWC uint8 wrapper с internal normalization (`export_resnet50_to_onnx.py:11–29,57–81`). Это **не** установленный model/input/preset vendor slide: build/weights hashes и результат не опубликованы, vendor `resnet50_mlperf` — другой artifact path. Воспроизводимое имя модели не означает одинаковые веса или качество.

<a id="f286"></a>

### F286 — Независимые авторы: scope не расширился до comparable benchmark

- Исходный локатор: [W2-I-F06](_WORK/W2_I_RESULT.md), строка77; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S017](SOURCES.md#s017), [S076](SOURCES.md#s076), [S077](SOURCES.md#s077)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F286](RAW_FACTS.md#f286). Независимые авторы: scope не расширился до comparable benchmark

[S017](SOURCES.md#s017), [S076](SOURCES.md#s076) — Сергей Нефёдов, Руслан Качмазов, Лев Бабинцев, VK/ВШЭ, Habr30.03.2025. Повторный targeted fetch прочитал original article и outbound links; HTML extraction показывает inline figures до IVA section, а сами IVA results отправлены в cloud link. Direct linked visualization снова404. Даны авторские descriptions preloaded Performance и последовательного Latency, batches1/2/4/8, STAGING failures; нет downloadable matched scripts/logs/model+quality+version package. Это независимая авторская линия опыта, но не измерение текущих Runtime16.18.6/Framework2026.8.43/HPQ. Не приписывать ей современную precision/16TOPS physical measured arithmetic; авторы выводили operation throughput из модели×FPS.

[S077](SOURCES.md#s077) — Рудь Иван Васильевич, магистерская ВКР СПбПУ2026, «Исследование тензорных вычислителей компании „ХайТэк“ на задачах локализации БПЛА…», научный руководитель по indexed metadata Громов Виктор. Targeted search по полному автору/названию дал только library record, публичного доклада/appendix/repo не выявил. W2 web `/en/info` timeout, TinyFish `/en/info` и `/info` proxy_error, urllib `/en/info` TLS EOF; новое чтение metadata не состоялось. W1 открытый abstract с443/430/142/20FPS остаётся provenance этих чисел; W2 search snippet не повышает его до fulltext. Fulltext authorized-only не запрашивали обходом, credentials не использовали. Нет условия сопоставимости MobileNet142 vs vendor1201,7FPS; ни один источник не объявлен ошибочным.


## W2-J — W2-J — доказательство исполнения, profiler и граница полного графа

<a id="f287"></a>

### F287 — HPS profiler заявлен как мониторинг, а scope trace не описан

- Исходный локатор: [W2-J-F01](_WORK/W2_J_RESULT.md), строка32; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_claim.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S026](SOURCES.md#s026)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F287](RAW_FACTS.md#f287) — HPS profiler заявлен как мониторинг, а scope trace не описан

Тип `vendor_claim`, [S026](SOURCES.md#s026), page3. Performance Profiler описан как средство наблюдения скорости и загрузки вычислительных блоков. Power Monitor относится к мощности/тепловому режиму; DNN Stat назван на page1. Ни syntax запуска, ни пример export, ни единицы/источник измерения, ни request/model IDs в этих разделах не заданы. Поэтому **ни «только host estimates», ни «измеренные аппаратные per-request счётчики» из datasheet не следуют**. Наличие слова profiler не разрешает выбрать любую из этих интерпретаций. Page4 перечисляет User/Installation Guide, Developer SDK и Hardware Software Reference, но не предоставляет их содержимого. Вывод bounded до этого документа.

<a id="f288"></a>

### F288 — legacy timing shape имеет явно накопленные компоненты

- Исходный локатор: [W2-J-F02](_WORK/W2_J_RESULT.md), строка36; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: historical_documentation.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S166](SOURCES.md#s166), [S167](SOURCES.md#s167), [S168](SOURCES.md#s168), [S169](SOURCES.md#s169)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F288](RAW_FACTS.md#f288) — legacy timing shape имеет явно накопленные компоненты

Тип `historical_documentation`, [S166](SOURCES.md#s166), [S167](SOURCES.md#s167)/[S168](SOURCES.md#s168), [S169](SOURCES.md#s169) README86–100, source not executed. Три очереди именуются `QUEUE_TRANSFER_TO`, `QUEUE_EXECUTOR`, `QUEUE_TRANSFER_FROM`; далее idle/work и тройка last/average/maximum. Average/maximum описываются как значения по всем inferences объекта device. Отдельно показаны `execution_timing` и глобальное `device.stats["mem"]`. Не установлены units, wall/device clock, reset/rollover, thread safety, serialization order, global across all processes vs this object, mapping last к вызову в concurrency. Даже если modern API повторяет shape, среднее/maximum нельзя приложить к requestN как его персональную latency. Само поле last без correlation тоже двусмысленно при overlapping requests. Описание execution on TPU в README — историческое API claim, не увиденная register instrumentation.

<a id="f289"></a>

### F289 — actual archives не содержат реализации обещанных timings

- Исходный локатор: [W2-J-F03](_WORK/W2_J_RESULT.md), строка40; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S166](SOURCES.md#s166), [S167](SOURCES.md#s167), [S168](SOURCES.md#s168), [S169](SOURCES.md#s169)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F289](RAW_FACTS.md#f289) — actual archives не содержат реализации обещанных timings

Тип `source_code`, [S166](SOURCES.md#s166), [S167](SOURCES.md#s167)/[S168](SOURCES.md#s168), [S169](SOURCES.md#s169), actual downloaded files inspected. В13.0.13 `pytpu/pytpu/__init__.py` создаёт spec для `/usr/lib/pytpu.so` и экспортирует старые TPUDevice/TPUProgram/TPUProgramInfo. Полного native source/binary нет в tar member list. Поэтому numerical/timing implementation там восстановить нельзя.

В14.7.0 `pytpu/pytpu/__init__.py` импортирует `libtpu_bindings`, где CDLL target `/usr/lib/libtpu.2.so`, Device methods — create/init/info/load/run/submit; statuses получаются native. Static source не реализует README `load_inference_sync`/`result.timings`/`device.stats`; отдельные host helpers относятся уже к другому API. Это **более ранний конкретный пример README/source mismatch**, дополняющий W1 замечание о15.0.24. Он опровергает shortcut «возьмём любую из описанных статистик из public pip и получим current profiler». Не доказывает, что timings отсутствуют в отдельных иных native releases.

`disable_static_checker` присутствует только в старом README configuration example. Значение true отключает некий checker; ни semantic purpose, ни relation к fallback/partition coverage не описаны. Это **не strict/no-fallback flag**, и применять его ради доказательства исполнения нельзя.

<a id="f290"></a>

### F290 — `Estimated FPS` старого helper — host-derived throughput

- Исходный локатор: [W2-J-F04](_WORK/W2_J_RESULT.md), строка48; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S166](SOURCES.md#s166), [S167](SOURCES.md#s167), [S168](SOURCES.md#s168), [S169](SOURCES.md#s169)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F290](RAW_FACTS.md#f290) — `Estimated FPS` старого helper — host-derived throughput

Тип `source_code`, [S166](SOURCES.md#s166), [S167](SOURCES.md#s167)/[S168](SOURCES.md#s168), [S169](SOURCES.md#s169) `tools/get_fps.py`; не выполнялся. Оба helper формируют задания, запускают asyncio tasks, окружают их host `time()` и делят `n_queries * batch` на elapsed. В13.0.13 per-call path включает load, awaited status.is_success, get outputs. В14.7.0 get outputs закомментирован, и используются иные native binding calls. Это показанная формула пропускной способности выбранного harness; она не отдельный аппаратный operations counter, не реализация Performance Profiler и не измеренный tensor-core-only time. Не переносить результаты разных code paths в одну latency table. Корректность work count/генерации данных/мульти-input здесь не проверялась; running helper на чужом устройстве не выполнялся.

<a id="f291"></a>

### F291 — executable artifact — полезная lineage boundary, но не whole-graph proof

- Исходный локатор: [W2-J-F05](_WORK/W2_J_RESULT.md), строка52; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: vendor_claim.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S026](SOURCES.md#s026), [S063](SOURCES.md#s063)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F291](RAW_FACTS.md#f291) — executable artifact — полезная lineage boundary, но не whole-graph proof

Тип `vendor_claim` + `inference`, [S026](SOURCES.md#s026)/[S063](SOURCES.md#s063). Машинный код tensor cores заявлен официально; `.tpu` передаётся в native program load, Python reference не исполняет fallback TensorFlow/PyTorch neural graph. Это усиливает свидетельство по сравнению с произвольным backend label. Но ZIP с metadata и weights не предоставляет проверяемую ISA semantics; наличие машинного кода внутри не доказывает отсутствие других stages или полноту lowering source graph.

Для покрытия нужны: source graph/weights hashes → compile configuration/target/version → report о преобразованных/fused/eliminated операциях и местах выполнения → hash loaded program. Операция может исчезнуть при корректном constant folding/fusion, поэтому наивное равенство числа nodes числу TPU instructions не является coverage criterion. Если compiler по конструкции выдаёт только цельную TPU программу или error, matching release documentation этой гарантии может заменить подробный partition report; такой документ пока не получен. Если format допускает host program, его штатные стадии требуют описания. Отсутствие Python CPU-model path не доказывает native guarantee.

<a id="f292"></a>

### F292 — FULL/RAW и host processing не классифицируют fallback

- Исходный локатор: [W2-J-F06](_WORK/W2_J_RESULT.md), строка58; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S063](SOURCES.md#s063)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F292](RAW_FACTS.md#f292) — FULL/RAW и host processing не классифицируют fallback

Тип `source_code` + `inference`, [S063](SOURCES.md#s063)/[F264](RAW_FACTS.md#f264),[F290](RAW_FACTS.md#f290). Enum передаётся native; Python allocations/reshapes зависят от artifact RAW heuristic, а numerical converter вызывается через отдельный `tpu_tlm_is` codec. Не установлены actual FULL stage placement и units timing. Поэтому host scaling/transpose/packing нельзя автоматически назвать hidden model fallback, а FULL нельзя развернуть в обещание all stages TPU. До ответа поставщика модельный graph boundary, штатный runtime tensor codec и отдельно написанные decode/NMS должны записываться раздельно. Correct numerical output и FULL↔RAW parity проверяют correctness, но не physical execution.

<a id="f293"></a>

### F293 — per-request evidence возможно без profiler, но требует доверенной корреляции

- Исходный локатор: [W2-J-F07](_WORK/W2_J_RESULT.md), строка62; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: engineering_inference.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S063](SOURCES.md#s063), [S075](SOURCES.md#s075)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F293](RAW_FACTS.md#f293) — per-request evidence возможно без profiler, но требует доверенной корреляции

Тип `engineering_inference`, [S063](SOURCES.md#s063)/[S075](SOURCES.md#s075), не продуктовая capability claim. Matching runtime completion trace, связанный с exact loaded artifact и согласованным physical device mapping, может быть сильнее aggregate profiler chart. Если организатор принимает live witnessed run в выделенном слоте с device identity, model load hash и контролируемым входом, отдельная profiler утилита не логически обязательна. Ни такой критерий, ни server trace capability сейчас не подтверждены. Приложение, runtime и организатор — разные trust boundaries; свои JSON поля сами по себе не становятся аппаратным подтверждением.

<a id="f294"></a>

### F294 — Матрица силы свидетельств

- Исходный локатор: [W2-J-MATRIX-16](_WORK/W2_J_RESULT.md), строка107; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S026](SOURCES.md#s026), [S166](SOURCES.md#s166), [S167](SOURCES.md#s167), [S168](SOURCES.md#s168), [S169](SOURCES.md#s169), [S063](SOURCES.md#s063), [S019](SOURCES.md#s019), [S075](SOURCES.md#s075)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Матрица силы свидетельств

| Свидетельство | Что поддерживает | Что не закрывает |
|---|---|---|
| Successful versioned native open/load/status | Работа соответствующего runtime path | Реализацию native, whole graph, исходные weights |
| Artifact hash + compile coverage/guarantee | Lineage и выбранную границу graph lowering | Физическое выполнение конкретного request |
| Per-task completion с program/device mapping | Attribution выполнения в данной trust boundary | Верность compiler coverage и неподменённость source |
| Legacy last timing с подтверждённым scope | Один документированно сопоставленный timing | Attribution при concurrency без task ID |
| Average/max, FPS, aggregate utilisation | Нагрузку/throughput указанного scope | Per-request latency, our model identity, no fallback |
| Output parity/golden tensor | Numerical correctness данного input/path | Physical device identity |
| Invalid device/no mapping failure | Fail-closed данной точки/configuration | Частичный graph fallback и server model substitution |
| Unknown service revision rejection | Fail-closed model selection | Device execution или no-fallback native policy |
| Live engineer/jury witness в согласованном scope | Практическое принятие обязательного inference | Невыданные technical internals за пределами witness |


## W2-K — W2-K — IVA CV: промышленная интеграция и граница видео

<a id="f295"></a>

### F295 — Версия образа: исправление извлечения, а не найденный новый release

- Исходный локатор: [W2-K-F01](_WORK/W2_K_RESULT.md), строка13; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S103](SOURCES.md#s103)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F295](RAW_FACTS.md#f295) — Версия образа: исправление извлечения, а не найденный новый release

[S103](SOURCES.md#s103), админ-guide, печатные p9–10, раздел 6. Сохранённое HTML-извлечение содержит конец блока `ivacv.tech:15444/common/walkers-node:0.1.3</p>` и следующий блок `<p>10`. Повторное Markdown-извлечение независимо по вызову также даёт `0.1.3`. Web-text показывает `0.1.310` на переходе P8–P9. Аналогично:

| Компонент | Page-separated extraction | Слипшийся web-text | Следующая печатная страница |
|---|---|---|---|
| walkers-node | `0.1.3` | `0.1.310` | 10 |
| ivacv-service-node-cuda | `0.7.8` | `0.7.811` | 11 |
| edge-api | `0.3.10` | `0.3.1012` | 12 |
| vdms-api | `0.5.22` | `0.5.2214` | 14 |
| vdms-ui | `0.3.2` | `0.3.218` | 18 |

Не существует полученного image digest или registry-ответа, подтверждающего любой из этих тегов как доступный артефакт. Пока нет PDF bytes/render, для документационного примера использовать **`0.1.3 (по извлечению с границами страниц; визуальное подтверждение не получено)`**, а для настоящего запуска — выданный matching digest. Полные извлечения сохранены в ADMIN_GUIDE_EXTRACT.json и ADMIN_GUIDE_MARKDOWN_EXTRACT.json. SHA256 этих файлов фиксирует именно наши представления текста, не оригинальный PDF.

<a id="f296"></a>

### F296 — Generic TPU-гипотеза частично опровергнута; H1M/PPE-связь остаётся неизвестной

- Исходный локатор: [W2-K-F02](_WORK/W2_K_RESULT.md), строка27; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S103](SOURCES.md#s103), [S105](SOURCES.md#s105), [S102](SOURCES.md#s102)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F296](RAW_FACTS.md#f296) — Generic TPU-гипотеза частично опровергнута; H1M/PPE-связь остаётся неизвестной

[S103](SOURCES.md#s103), p9: непосредственно перед примером присутствует подпись «с использованием Linq TPU». Следовательно, весь смысл LinQ-примера не выведен только из имени `/dev/tpu0`. Одновременно p2 использует прежнее обозначение IVA (TPU), p5 — Linq; ни H1, ни H1M, ни HPD, ни версии TPU driver/runtime/compiler в извлечении не установлены. Документ не имеет найденной внутри даты/номера редакции. Дата каталога uploads/2026/05 не датирует содержащуюся в нём команду.

Проверено в текущей HTML-странице [S105](SOURCES.md#s105): она называет LinQ среди поддерживаемых чипов, но список NN runtimes отдельного TPU runtime не содержит. В ней Linux kernel >=6.1, тогда как PDF >=6.0. Это две несогласованные спецификации общего продукта, а не современная ABI-матрица. Нельзя ни объявить пример устаревшим только по слову IVA, ни объявить его совместимым с H1M только по слову LinQ.

[S102](SOURCES.md#s102) (новость интегратора 19.06.2026) явно связывает ПАК ОТПБ, LinQ и контроль СИЗ. Однако в тексте и извлечённых ссылках нет контейнерного тега/digest, перечня моделей, runtime, конфигурации или протокола измерения. Наличие LinQ в промышленной новости и LinQ в общем руководстве не устанавливает идентичность сборки. Tenant `cbr`, имя `walkers-node` и CUDA-пример другого project namespace не доказывают ни PPE-состав, ни deployment у названного заказчика.

Статус: primary documentation + vendor statement; исполнения не наблюдалось. Это уточнение W1, а не новое аппаратное подтверждение.

<a id="f297"></a>

### F297 — Переносимый состав поставки и конкретный порядок развёртывания

- Исходный локатор: [W2-K-F03](_WORK/W2_K_RESULT.md), строка37; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S103](SOURCES.md#s103)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F297](RAW_FACTS.md#f297) — Переносимый состав поставки и конкретный порядок развёртывания

[S103](SOURCES.md#s103) p6–20: общие каталоги, MongoDB replica-set, Edge-api, проектный videoanalytics node, VDMS-api, VDMS-ui. Документированный порядок старта: MongoDB → Edge-api → видеоаналитика → VDMS-api → VDMS-ui. Установка включает импорт дефолтной БД и настройку справочников, а не только `docker run` NN-контейнера.

Из LinQ-примера пригодны для сопоставления поставки следующие литералы: `IVA_CONFIG` из `config-patch.json`; `IVA_ENABLE_INSTALLER=0`; `IVA_TENANT="cbr"` (пример); `IVA_EDGE_SERVER="edge-api-1:16000"`; `IVA_EDGE_SERVER_WS="ws://edge-api-1:9001/datahub"`; mapping `/dev/tpu0:/dev/tpu0`; общий host-каталог `/msdata/shared` в `/app/msdata/shared` и `/app/msdata/data`; temp/logs mounts. Полная команда находится в сохранённом source extraction; мы не предлагаем запускать её на выданном сервисе без согласованной поставки.

**Неполученные обязательные части matching deploy:** actual images и digests; `config-patch.json`; project NN models/weights/compiled programs; внутренняя конфигурация `/app/msdata/config`; default DB dump и справочники; service scripts; драйвер/runtime для конкретного TPU и инструкция host/container ABI; ключи API и разрешённые методы; разрешение использовать поставку в требуемой среде. PDF говорит о проектной сборке vendor, следовательно, восстановить эти assets из общих названий невозможно.

Для воспроизведения после получения поставки: сначала зафиксировать manifest и права, подготовить matching host+driver+Docker/каталоги/пользователя, импортировать и настроить MongoDB, настроить Edge-api, затем videoanalytics с выданным конфигом, VDMS-api/UI. После старта документ требует отдельной функциональной проверки UI и тестовой видеоаналитики с камерами/файлами/API. Прохождение UI не доказывает TPU execution; нужно дополнительно связать NN-вызовы, устройство и результаты.

<a id="f298"></a>

### F298 — Где проходит граница video/event, и где она не раскрыта

- Исходный локатор: [W2-K-F04](_WORK/W2_K_RESULT.md), строка47; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S103](SOURCES.md#s103), [S104](SOURCES.md#s104)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F298](RAW_FACTS.md#f298) — Где проходит граница video/event, и где она не раскрыта

По [S103](SOURCES.md#s103) p8–16, без вывода скрытой реализации:

| Стадия | Что документировано | Чего документ не устанавливает |
|---|---|---|
| Вход | Videoanalytics component получает камеры/файлы/другие видеопотоки | Codec, decoder, транспорт/буферы, reconnect, частота анализа |
| Decode/preprocess | Общий перечень hardware video decode/encode support p5 | Нельзя распределить decode по каждому перечисленному чипу; нет конкретного LinQ decode API/BOM |
| Нейросети | Проектная сборка включает NN, code, config; LinQ device mapping p9 | Имена NN, opset/input/output, TPU coverage, fallback, batch/scheduler |
| Tracking/rules | Узел обрабатывает pipeline и отдаёт события/изображения/видео | Где выполняются NMS/tracker/PPE-association, temporal debounce/rules |
| Приём результатов | Edge-api принимает данные узлов и сохраняет в MongoDB; REST/WS/gRPC | Payload schema, acknowledgement, дедупликация и идемпотентность API |
| Обработка событий | VDMS-api содержит job очереди событий, её recovery-настройку | Полная queue semantics, delivery guarantee, end-to-end latency |
| Просмотр/архив | VDMS-api транслирует UI-видео, включает/выключает muxers, архивирует/удаляет данные; UI — static frontend через nginx | UI FPS не измеряет NN FPS; video retention не queue depth |

**Новый конкретный lesson:** VDMS `eventsProcessorJobIntervalMs` приведён с примером `500`, `eventsProcessorStuckRestartSec` — `10`. Это интервал job и срок перезапуска незавершённой обработки записи после аварийного остановa, не обещание event latency 500 ms и не device inference timeout 10 s. `streamMonitorJobIntervalMs` управляет мониторингом realtime muxers, а не обязательным NN sampling. `dataCleanupStreamsKeepHours` пример `0.5` относится к хранению видеоданных. См. source p14–15 и ключи в ADMIN_GUIDE_EXTRACT.json.

UI event filters из [S104](SOURCES.md#s104) (13-page guide, PDF p6–7) включают каску/жилет/опасную зону/сигарету/дым/телефон, однако список UI не раскрывает вычислитель каждой NN или правила формирования события. Параметр `defaultVisibleEventTypes` в серверном guide регулирует видимость типов для пользователей, а не набор запущенных моделей. API-control (`apps`, `appsAccess`, `apiMethods`, WS `topics/messages`) также является частью конфигурации и не даёт готового публичного inference endpoint.

Статус таблицы: documented process/service boundaries. Называть все эти стадии host CPU некорректно: сервисы находятся вне доказанного NN-вычисления, но внутреннее CPU/device распределение не опубликовано. Наличие RTSP и слова decode в общей документации **не доказывает LinQ silicon decode**. Ускоритель/remote SDK хакатона может принимать только тензоры, это вопрос отдельного access contract.

<a id="f299"></a>

### F299 — Multi-camera условия, которые реально можно перенести

- Исходный локатор: [W2-K-F05](_WORK/W2_K_RESULT.md), строка67; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S103](SOURCES.md#s103), [S104](SOURCES.md#s104)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F299](RAW_FACTS.md#f299) — Multi-camera условия, которые реально можно перенести

[S103](SOURCES.md#s103)/[S104](SOURCES.md#s104) поддерживают камеры/несколько окон, общие медиакаталоги, streams/frames/crops/chunks и проектные compute nodes. Из этого нельзя вывести допустимое N камер: нет codec, bitrate/resolution, analysis FPS, CPU/RAM/device quota, fairness, очереди кадров, timestamp policy или benchmark. Минимальные 8 GB RAM/256 GB disk в PDF — общие требования платформы, не sizing под N PPE-камер.

**Наш условный adapter/эксперимент**, а не функция IVA/LinQ SDK: bounded per-camera queue, явный drop policy, сохранение camera/frame/source timestamps, reconnect без накопления старого видео; замер age каждого кадра и event delay по каждой камере. Чтобы разделить decode и inference, прогнать один и тот же clip с реальным источником и заранее подготовленными входами при одинаковом NN sampling; добавить камеры до роста age или потерь и измерить host CPU/network отдельно. Записывать cold start, decode/preprocess, queue/batch wait, inference, NMS/tracker/rules, delivery/VDMS polling раздельно. Никаких численных performance ожиданий из материалов IVA CV не выводится.

<a id="f300"></a>

### F300 — Доступ/лицензия: конкретная коммерческая поставка, неизвестные права

- Исходный локатор: [W2-K-F06](_WORK/W2_K_RESULT.md), строка73; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S105](SOURCES.md#s105), [S103](SOURCES.md#s103)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F300](RAW_FACTS.md#f300) — Доступ/лицензия: конкретная коммерческая поставка, неизвестные права

[S105](SOURCES.md#s105) прямо выделяет стоимость лицензий платформы/модулей, внедрения и поддержки. [S103](SOURCES.md#s103) описывает отдельный project/customer repository и набор приложений/config/models. Публичное руководство доступно для чтения; open-source sample, license/EULA для `walkers-node`, условия anonymous pull, права на изменение/копирование weights или redistributing image в открытом submission не найдены в targeted поиске и прочитанных ссылках. Это **UNKNOWN**, не доказанный запрет исполнения.

URL `ivacv.tech:15444` и `pull.sh` не являются grant of access/license. Registry endpoint не проверялся: отсутствие полученной поставки/разрешения на конкретный image сделало probing образов бесполезным для нынешнего решения. Не предпринимались auth attempts, token guessing, обходы или обращения к людям.

Минимум, меняющий route: разрешение запуска командой в данном host/cloud; доступ пяти разработчиков; возможность изменять pipeline/config; условия использования/выгрузки weights/compiled artifacts; что разрешено публиковать в source/submission (свои adapters и ссылки на поставку либо также binaries). Эти права нужны отдельно для платформы, TPU runtime и моделей; privacy policy формы не заменяет их. До ответа architecture lessons переносимы, turnkey commercial product route остаётся условным.

<a id="f301"></a>

### F301 — Видео не просмотрено; четырёхсетевой показ не стал multi-stream test

- Исходный локатор: [W2-K-F07](_WORK/W2_K_RESULT.md), строка81; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S106](SOURCES.md#s106)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### [F301](RAW_FACTS.md#f301) — Видео не просмотрено; четырёхсетевой показ не стал multi-stream test

[S106](SOURCES.md#s106) открыта web и TinyFish: interview page 09.07.2025, Владислав Николаев, AQserv + LinQ HPD, описание four-network show. TinyFish HTML-output имеет `Video file`, но не возвращает playable source/iframe (iframe_links=[]); Python HTTPS fetch страницы завершился TLS EOF, HTTP — RemoteDisconnected. Targeted search Rutube/интервью не дал доступного проверенного media record с содержанием технического показа. **Аудиовидео не просмотрено/не прослушано, таймкодов нет.** Аннотация не повышена до наблюдения стенда. Партнёрский анонс Aquarius из W1 не повторно считается независимым post-event test.


## W2-L — W2-L — online control/data plane и граница видеосервиса

<a id="f302"></a>

### F302 — Организатор требует inference на LinQ и обещает online-доступ; public case не называет SSH, API, container, custom upload, compiler location, quota или camera transport. S01, загол

- Исходный локатор: [W2-L-F01](_WORK/W2_L_RESULT.md), строка17; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S035](SOURCES.md#s035)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт / локатор | Evidence type / actual test |
|---|---|---|
| [F302](RAW_FACTS.md#f302) | Организатор требует inference на LinQ и обещает online-доступ; public case не называет SSH, API, container, custom upload, compiler location, quota или camera transport. [S035](SOURCES.md#s035), заголовок LinQ и следующий абзац, web lines266–269. | `primary organizer statement`; live web.open/search; не доступ в кабинет/устройство. Отсутствие на public странице не доказывает отсутствия в полном закрытом ТЗ. |

<a id="f303"></a>

### F303 — Главная предлагает демонстрацию и тестовую среду; demo link6 ведёт к `https://lin-q.ru/footer` с popup anchor в W1 navigation. Web extraction footer содержит общие навигационные сс

- Исходный локатор: [W2-L-F02](_WORK/W2_L_RESULT.md), строка18; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S001](SOURCES.md#s001), [S034](SOURCES.md#s034)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт / локатор | Evidence type / actual test |
|---|---|---|
| [F303](RAW_FACTS.md#f303) | Главная предлагает демонстрацию и тестовую среду; demo link6 ведёт к `https://lin-q.ru/footer` с popup anchor в W1 navigation. Web extraction footer содержит общие навигационные ссылки, а не onboarding/API docs. [S001](SOURCES.md#s001)/[S034](SOURCES.md#s034). | `vendor statement + navigation observation`; web open/click. Форму/popup не отправляли, browser visual не смотрели; отсутствие текста в extractor не доказывает отсутствие JS popup. |

<a id="f304"></a>

### F304 — `/sol` software section описывает генерацию программы для LinQ H через quantization/compile, Python3.8 API и CLI. Download section требует регистрацию и верификацию. S04 lines273–2

- Исходный локатор: [W2-L-F03](_WORK/W2_L_RESULT.md), строка19; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S003](SOURCES.md#s003)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт / локатор | Evidence type / actual test |
|---|---|---|
| [F304](RAW_FACTS.md#f304) | `/sol` software section описывает генерацию программы для LinQ H через quantization/compile, Python3.8 API и CLI. Download section требует регистрацию и верификацию. [S003](SOURCES.md#s003) lines273–293. | `primary vendor documentation`; live web.open полного релевантного участка. Это локальное ПО/OEM описание, не право команды на remote compiler или executable SDK. |

<a id="f305"></a>

### F305 — В C++ вакансии производитель описывает cloud inference Python prototype и C++ pre-alpha, требования/архитектуру/обновления/monitoring как работу вакансии. S05 lines136–169.

- Исходный локатор: [W2-L-F04](_WORK/W2_L_RESULT.md), строка20; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S014](SOURCES.md#s014)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт / локатор | Evidence type / actual test |
|---|---|---|
| [F305](RAW_FACTS.md#f305) | В C++ вакансии производитель описывает cloud inference Python prototype и C++ pre-alpha, требования/архитектуру/обновления/monitoring как работу вакансии. [S014](SOURCES.md#s014) lines136–169. | `vendor statement`; live web.open. Дата публикации неизвестна: нельзя датировать зрелость сервиса сегодняшним днём или заключать, что конкурс использует этот prototype. REST/gRPC в требованиях вакансии не устанавливают transport сервиса. |

<a id="f306"></a>

### F306 — Официальный guide2025 документирует local host `Device.list_devices()`, `Device.open`, `device.load`, `program.inference`, blocking `sync` со словарём tensors; `.tpu` отделяет Fram

- Исходный локатор: [W2-L-F05](_WORK/W2_L_RESULT.md), строка21; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S030](SOURCES.md#s030)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт / локатор | Evidence type / actual test |
|---|---|---|
| [F306](RAW_FACTS.md#f306) | Официальный guide2025 документирует local host `Device.list_devices()`, `Device.open`, `device.load`, `program.inference`, blocking `sync` со словарём tensors; `.tpu` отделяет Framework от SDK. [S030](SOURCES.md#s030) §3.4 pp19–21, сохранённый extraction. | `primary documentation reused`, text inspection; не новый PDF fetch/visual и не SDK run. Следствие: local worker возможен в совместимой выданной среде, но API не сообщает remote access contract. |

<a id="f307"></a>

### F307 — LinQ Cloud/containerization и optional video hardware у HPS названы в datasheet, но это не спецификация предоставленного host/service. S07 p4 по сохранённым W1 фактам.

- Исходный локатор: [W2-L-F06](_WORK/W2_L_RESULT.md), строка22; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S026](SOURCES.md#s026)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт / локатор | Evidence type / actual test |
|---|---|---|
| [F307](RAW_FACTS.md#f307) | LinQ Cloud/containerization и optional video hardware у HPS названы в datasheet, но это не спецификация предоставленного host/service. [S026](SOURCES.md#s026) p4 по сохранённым W1 фактам. | `vendor marketing reused`; новый PDF в этой ветке не открывался. Нельзя выводить decoder availability, число streams, quota или device SKU команды. |

<a id="f308"></a>

### F308 — IVA CV admin text подтверждает отдельные компоненты videoanalytics/Edge-api/VDMS, модели проектной сборки и отдельную процедуру deploy. Сохранённый page-separated extraction исправ

- Исходный локатор: [W2-L-F07](_WORK/W2_L_RESULT.md), строка23; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S103](SOURCES.md#s103)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт / локатор | Evidence type / actual test |
|---|---|---|
| [F308](RAW_FACTS.md#f308) | IVA CV admin text подтверждает отдельные компоненты videoanalytics/Edge-api/VDMS, модели проектной сборки и отдельную процедуру deploy. Сохранённый page-separated extraction исправляет tags: `walkers-node:0.1.3` + следующая p10; `edge-api:0.3.10` + p12; `vdms-api:0.5.22` + p14; `vdms-ui:0.3.2` + p18. [S103](SOURCES.md#s103). | `primary documentation reused via W2-K text`; не PDF visual, registry pull или deployment. W1 `0.1.310` — concatenation artifact, не exact image. Literal Linq TPU не устанавливает SKU/runtime/PPE inventory. |

<a id="f309"></a>

### F309 — Новый targeted search не нашёл primary onboarding/API docs с model upload/compile/update, quotas/concurrency, payload limits, persistence/retention, auth или camera-network contrac

- Исходный локатор: [W2-L-F08](_WORK/W2_L_RESULT.md), строка24; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S035](SOURCES.md#s035), [S001](SOURCES.md#s001), [S034](SOURCES.md#s034), [S003](SOURCES.md#s003), [S014](SOURCES.md#s014), [S030](SOURCES.md#s030), [S026](SOURCES.md#s026), [S103](SOURCES.md#s103), [S063](SOURCES.md#s063), [S171](SOURCES.md#s171)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт / локатор | Evidence type / actual test |
|---|---|---|
| [F309](RAW_FACTS.md#f309) | Новый targeted search не нашёл primary onboarding/API docs с model upload/compile/update, quotas/concurrency, payload limits, persistence/retention, auth или camera-network contract именно обещанного доступа. | `bounded negative search`, не доказательство nonexistent service. Проверенные запросы/результаты ниже. Закрытые docs/личный кабинет не просматривались. |

<a id="f310"></a>

### F310 — Alternate direct HTTPS GET к HOME/SOL/HR/FOOTER/CASE через Python urllib все завершились TLS EOF 23.10.2026 02:08:36 UTC; web extraction тех же страниц доступен.

- Исходный локатор: [W2-L-F09](_WORK/W2_L_RESULT.md), строка25; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S035](SOURCES.md#s035), [S001](SOURCES.md#s001), [S034](SOURCES.md#s034), [S003](SOURCES.md#s003), [S014](SOURCES.md#s014), [S030](SOURCES.md#s030), [S026](SOURCES.md#s026), [S103](SOURCES.md#s103), [S063](SOURCES.md#s063), [S171](SOURCES.md#s171)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт / локатор | Evidence type / actual test |
|---|---|---|
| [F310](RAW_FACTS.md#f310) | Alternate direct HTTPS GET к HOME/SOL/HR/FOOTER/CASE через Python urllib все завершились TLS EOF 23.10.2026 02:08:36 UTC; web extraction тех же страниц доступен. | `local network observation`; `W2_L/FETCH.py`, `HTTP_LOG.json`. Это различие retrieval channels, не ограничение авторизации сайта и не outage сервиса. |

<a id="f311"></a>

### F311 — Исторический `pytpu15.0.24` test создаёт несколько inference descriptors на один opened device/program и распределяет их потокам; значение8 сопровождается TODO о неверных результат

- Исходный локатор: [W2-L-F10](_WORK/W2_L_RESULT.md), строка26; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S063](SOURCES.md#s063), [S171](SOURCES.md#s171)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Факт / локатор | Evidence type / actual test |
|---|---|---|
| [F311](RAW_FACTS.md#f311) | Исторический `pytpu15.0.24` test создаёт несколько inference descriptors на один opened device/program и распределяет их потокам; значение8 сопровождается TODO о неверных результатах. В14.7.0 get_fps несколько descriptors передаются asyncio tasks в одном процессе. [S063](SOURCES.md#s063)/[S171](SOURCES.md#s171). | `source_code reused`, локально прочитан после handoff W2-M; ни один test не запускался. Это опровергает превращение one-process-per-device в универсальное требование по этим примерам, но не устанавливает thread safety, shared-service concurrency или поддержку2026. |

<a id="f312"></a>

### F312 — Confirmed versus conditional control/data plane

- Исходный локатор: [W2-L-MATRIX-17](_WORK/W2_L_RESULT.md), строка28; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: engineering_recommendation grounded in primary documentation.

- actual_check: conditional routes/our queue contract; not an executed access route or a vendor capability claim.

- Sources: [S035](SOURCES.md#s035), [S030](SOURCES.md#s030), [S103](SOURCES.md#s103)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Confirmed versus conditional control/data plane

`Подтверждено` ниже означает документ/заявление; ни один remote route не исполнен. Артефакт команды, worker и backend не следует автоматически размещать на одном хосте.

| Route | Control plane: модель/compile/update | Data plane: кадры/результаты | Где worker и сервис команды | Status / решающее условие |
|---|---|---|---|---|
| R-L0: public promise | Не раскрыт | Не раскрыт | Не установлено | **Подтверждено только обещание** online LinQ inference, [S035](SOURCES.md#s035). До выдачи ничего не именовать endpoint/SSH. |
| R-L1: service custom model | Документированный upload исходного graph+weights и server compile **либо** upload matching `.tpu`; immutable model version, update readiness/rollback | Tensor/image calls с известными dtype/layout/limits и raw outputs; decode/pre/post согласно фактической схеме | Vendor runtime worker; наш backend/decoder/tracker/UI локально или на своей разрешённой машине | **Условно достаточно без shell.** Нужны Q1–Q4 и evidence Q5. Отсутствие compiler у клиента не blocker, если его функцию разрешённо выполняет vendor. |
| R-L2: service ready models only | Только catalog, custom update запрещён/не предоставлен | Готовые detections/events; tensor access может отсутствовать | Vendor model/video worker; наши правила/UI снаружи | **Условный ограниченный route.** Если нужные classes/outputs и правила конкурса допускают — интеграция возможна. Если нужен свой PPE graph и его нельзя загрузить, access формально есть, custom-model route блокирован; спросить альтернативную выдачу. Не объявлять generic detector эквивалентом PPE. |
| R-L3: shell/container + compiler/runtime | Graph/weights и compile на remote host при наличии поставки; либо перенос `.tpu` с другого совместимого compiler host; права записи/update отдельно | Local tensors через supplied runtime; video decode на host или доступном codec hardware | Worker remote; backend/UI remote только при подтверждённых lifecycle/ports; иначе backend локально | **Условно**, local API documented [S030](SOURCES.md#s030); факт shell/permissions конкурса неизвестен. Shell не гарантирует compiler, root, Docker, device permission или server lifecycle. |
| R-L4: job-only batch/file | Upload artifact/config и submit job по supplied documented procedure; persistence между jobs отдельно | Файл/набор tensor inputs → output artifact/log; deadline, queue и max payload определяют практичность | Worker lifecycle vendor job; local backend формирует/получает jobs | **Условно подходит для smoke/offline**, real-time только если bounded turnaround реально удовлетворяет задаче. Нельзя назвать upload whole video real-time автоматически. |
| R-L5: managed video service | Проектная model/config update, если разрешена | Camera/stream ingest и events; decode/tracking могут входить в service | Vendor video/runtime worker; наш UI/event adapter | **Условно**, нужен реальный supplied video contract. IVA CV [S103](SOURCES.md#s103) — пример отдельного продукта, не доказательство этой выдачи. Проверить camera reachability и timestamps, не дублировать decode без нужды. |

Все неподтверждённые limits: authentication scope/expiry; upload/file/model size и storage; per-team/device sessions; max in-flight, QPS и batch; queue timeout/cancel/retry/idempotency; compile queue и продолжительность; warm/cold lifetime, disconnect/restart; CPU/RAM/disk quota; persistent volumes/retention; inbound/outbound networking/proxy/VPN; codecs/camera count; logs/model-to-device correlation. **Ни одного численного лимита источники не дают.** Значения типа QPS/ports/session TTL не придумывать.

Service-only особенно рискует на передаче raw tensors, если API не принимает compressed frames/video. Пример исключительно нашей арифметики: один `1×3×640×640` float32 tensor = 4,915,200 bytes, восемь камер по10fps =393,216,000 bytes/s без protocol overhead. Для uint8 при том же shape:98,304,000 bytes/s. Это **не shape/model/fps требования и не измерение LinQ**; иллюстрирует необходимость Q2/Q3. JPEG/video уменьшают передачу, но только при поддержанном codec/decode, с отдельным влиянием на качество. Shell при decode на remote host не решает сетевую недостижимость камеры.

<a id="f313"></a>

### F313 — Наш queue/timestamp/frame identity contract — рекомендация, не функция LinQ SDK

- Исходный локатор: [W2-L-MATRIX-18](_WORK/W2_L_RESULT.md), строка57; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: engineering_recommendation grounded in primary documentation.

- actual_check: conditional routes/our queue contract; not an executed access route or a vendor capability claim.

- Sources: [S063](SOURCES.md#s063), [S171](SOURCES.md#s171)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Наш queue/timestamp/frame identity contract — рекомендация, не функция LinQ SDK

Назначить **одного владельца video/control adapter**. Он потребляет общий model manifest и golden input/output спецификацию от model/runtime владельцев, а не делает второй exporter/inventory. На границах сохранить:

- `camera_id`, уникальный `stream_epoch` после reconnect и монотонный внутри epoch `frame_seq`; tuple — frame identity. Отдельно `request_id/job_id`, `model_version/artifact_sha256`, preprocess/config hash. Это наша schema; vendor поля могут называться иначе и связываются adapter mapping.
- Source PTS + time base, если источник их даёт; local receive/decode-ready/enqueue/submit/result/event monotonic times; UTC wall time для журнала с отметкой clock source. Не вычитать часы разных host без known offset/synchronization. Capture-to-event нельзя заявлять, если capture timestamp неизвестен; тогда честно receive-to-event.
- Геометрия: original size, resize/letterbox scale/padding, crop/rotation; mapping outputs обратно к source frame. Tracking получает source timestamp и реальный gap после drop, а не считает каждый результат соседним кадром.
- Очередь finite по count/bytes и age budget; значения выбираются после Q3 и измерения. Для live alert при перегрузе предпочтителен свежий кадр: заменить устаревший unsent кадр той же камеры, записать reason/count. Для offline evaluation отдельный no-drop режим; не смешивать его FPS/quality с live sampling.
- Глобальный in-flight ≤ supplied quota; bounded per-camera pending и fair dispatch, чтобы активная камера не вытеснила остальные. Batch formation имеет deadline, padding/real-count по model manifest; не ждать медленную камеру бесконечно. Это policy команды, не характеристика vendor scheduler.
- Начать с одного владельца runtime session и serial submission допустимо как консервативную политику команды до ответа о concurrency. Это не аппаратное требование one-process-per-device: исторический код [S063](SOURCES.md#s063)/[S171](SOURCES.md#s171) содержит параллельные descriptors. Повышение concurrency проверять на actual release по correctness/isolation и разрешённой quota, не по старому TODO.
- При timeout результат может появиться позже: сопоставлять по identity, не добавлять старую detection к новому кадру; discard stale outputs с журналом. Retry только по documented semantics и лимиту, дедуплицировать event delivery локальным event key; не считать HTTP timeout доказательством отмены compute.
- Reconnect создаёт новый epoch; после model activation новый version boundary. Не смешивать old/new output в одном tracker state без явного перехода. При несовместимом class/geometry contract reset/перепривязка state — решение владельца модели/правил.

Метрики по каждой камере: ingress/source cadence, sampled/dropped/processed count, queue wait, network/serialization, vendor call (включает неизвестный internal queue если нет timestamps), inference только при отдельном trustworthy timer, postprocess, frame age и event delay; p50/p95/p99 и cold/warm отдельно. Суммарный accelerator throughput не подтверждает freshness/fairness видео.


## W2-M — W2-M — диагностика, session isolation и безопасное восстановление

<a id="f314"></a>

### F314 — Live `/docs` перечисляет hardware manuals и один framework operator guide. В полученном списке ссылок нет отдельной runtime error reference/release-notes страницы. `/sol` вновь пок

- Исходный локатор: [W2-M-F01](_WORK/W2_M_RESULT.md), строка17; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S019](SOURCES.md#s019), [S003](SOURCES.md#s003)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт и границы | Evidence / фактическая проверка | Источники |
|---|---|---|---|
| [F314](RAW_FACTS.md#f314) | Live `/docs` перечисляет hardware manuals и один framework operator guide. В полученном списке ссылок нет отдельной runtime error reference/release-notes страницы. `/sol` вновь показывает регистрацию+верификацию загрузки ПО. | Live extracted page+links; не читался закрытый кабинет. Отсутствие в этом списке не означает отсутствие документации у производителя. | [S019](SOURCES.md#s019), [S003](SOURCES.md#s003); `PRIMARY_NAVIGATION.json` |

<a id="f315"></a>

### F315 — Новый PyPI JSON отвечает200 и по `info.version` всё ещё указывает pytpu15.0.24; sdist upload2023-11-27. Это последний release **на этой карточке PyPI**, не последний LinQ Runtime/S

- Исходный локатор: [W2-M-F02](_WORK/W2_M_RESULT.md), строка18; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S064](SOURCES.md#s064), [S063](SOURCES.md#s063)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт и границы | Evidence / фактическая проверка | Источники |
|---|---|---|---|
| [F315](RAW_FACTS.md#f315) | Новый PyPI JSON отвечает200 и по `info.version` всё ещё указывает pytpu15.0.24; sdist upload2023-11-27. Это последний release **на этой карточке PyPI**, не последний LinQ Runtime/SDK вообще. Home URL остаётся старым Git-host. | Actual JSON bytes, SHA256 `10c33a7bcca80f7bdbad470e2ed52227e2514587c8d2ddb64ab572e5b3e46063`; не install. | [S064](SOURCES.md#s064), [S063](SOURCES.md#s063); `PYPI_CURRENT.json`, `HTTP_LOG.json` |

<a id="f316"></a>

### F316 — Source15.0.24 `test_parallel.py` открывает по device один Program, создаёт8 Inference descriptors и связывает каждый worker thread с собственным descriptor. `inference.sync` исполн

- Исходный локатор: [W2-M-F03](_WORK/W2_M_RESULT.md), строка19; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт и границы | Evidence / фактическая проверка | Источники |
|---|---|---|---|
| [F316](RAW_FACTS.md#f316) | Source15.0.24 `test_parallel.py` открывает по device один Program, создаёт8 Inference descriptors и связывает каждый worker thread с собственным descriptor. `inference.sync` исполняется в ThreadPoolExecutor. | Source inspection lines1–19,33–42,64–96,99–151; тест не запускался. | [S065](SOURCES.md#s065), `SOURCE_LOCATORS.json` |

<a id="f317"></a>

### F317 — Тот же тест при8threads содержит TODO о неправильных результатах; однопоточный вариант сопровождается комментарием об успехе. Корректность проверяется сравнением sum output, при не

- Исходный локатор: [W2-M-F04](_WORK/W2_M_RESULT.md), строка20; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт и границы | Evidence / фактическая проверка | Источники |
|---|---|---|---|
| [F317](RAW_FACTS.md#f317) | Тот же тест при8threads содержит TODO о неправильных результатах; однопоточный вариант сопровождается комментарием об успехе. Корректность проверяется сравнением sum output, при несовпадении печатается `X`; это **не assertion test**, гарантирующий падение при corrupt result. | Source lines17–19,87–94. TODO не подтверждает modern дефект и не устанавливает причину старого mismatch. | [S065](SOURCES.md#s065) |

<a id="f318"></a>

### F318 — В pytpu14.7.0 `get_fps.py` один TPUDevice получает список отдельных TPUInference длины `n_proc`; `asyncio.gather` запускает coroutine на этих descriptors. Несмотря на слово `proces

- Исходный локатор: [W2-M-F05](_WORK/W2_M_RESULT.md), строка21; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S169](SOURCES.md#s169)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт и границы | Evidence / фактическая проверка | Источники |
|---|---|---|---|
| [F318](RAW_FACTS.md#f318) | В pytpu14.7.0 `get_fps.py` один TPUDevice получает список отдельных TPUInference длины `n_proc`; `asyncio.gather` запускает coroutine на этих descriptors. Несмотря на слово `processes`, Python OS-process не создаётся в этом helper. | Actual sdist заново скачан200, SHA256 `54e63e4ecc787ab16e2ee3f32b3a4188928121b3954dfdf4334d9c7441b60f49`; source lines102–125, без запуска. | [S169](SOURCES.md#s169); `pytpu-14.7.0.tar.gz`, `SOURCE_14_7_0.json` |

<a id="f319"></a>

### F319 — 14.7.0 `submit_inference` действительно `async def`, вызывает native submit с callback и крутит `await asyncio.sleep(0)` до флага. Callback принимает `result`, но не проверяет его;

- Исходный локатор: [W2-M-F06](_WORK/W2_M_RESULT.md), строка22; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S169](SOURCES.md#s169)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт и границы | Evidence / фактическая проверка | Источники |
|---|---|---|---|
| [F319](RAW_FACTS.md#f319) |14.7.0 `submit_inference` действительно `async def`, вызывает native submit с callback и крутит `await asyncio.sleep(0)` до флага. Callback принимает `result`, но не проверяет его; assertion относится к submit return. В прочитанном helper нет cancel/timeout/finally для native request. | Source inspection libtpu_bindings.py179–212. Не исполнялся; факт объявления функции слабее supported modern API. Прерывание ожидания нельзя объявить native cancellation. | [S169](SOURCES.md#s169) |

<a id="f320"></a>

### F320 — В14.7.0 есть generic enum `TPUInferenceStatus`: `kOk=0`, `kError=1`, `kDevError=2`. Это конкретные historical source literals.

- Исходный локатор: [W2-M-F07](_WORK/W2_M_RESULT.md), строка23; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S169](SOURCES.md#s169)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт и границы | Evidence / фактическая проверка | Источники |
|---|---|---|---|
| [F320](RAW_FACTS.md#f320) | В14.7.0 есть generic enum `TPUInferenceStatus`: `kOk=0`, `kError=1`, `kDevError=2`. Это конкретные historical source literals. | Source236–239; нет version-matched C header, расшифровки причин, retry policy или current code map. Нельзя сопоставлять2 с «нужен reset». | [S169](SOURCES.md#s169) |

<a id="f321"></a>

### F321 — 15.0.24 docstring `Program.inference()` прямо предназначает Inference для **multiple sequential inferences/reuse**. Это опровергает гипотезу «каждый inference требует новый процесс

- Исходный локатор: [W2-M-F08](_WORK/W2_M_RESULT.md), строка24; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт и границы | Evidence / фактическая проверка | Источники |
|---|---|---|---|
| [F321](RAW_FACTS.md#f321) |15.0.24 docstring `Program.inference()` прямо предназначает Inference для **multiple sequential inferences/reuse**. Это опровергает гипотезу «каждый inference требует новый процесс/handle» на уровне намерения старого API. | Source307–312; не доказывает reuse после ошибки, simultaneous use одного descriptor или current lifecycle. | [S065](SOURCES.md#s065) |

<a id="f322"></a>

### F322 — Сторонний pinned2026 `run_resnet50_parallel_direct.py` создаёт subprocess на пару device/shard. Код реализует выбранное распределение; нет утверждения производителя о невозможности

- Исходный локатор: [W2-M-F09](_WORK/W2_M_RESULT.md), строка25; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S074](SOURCES.md#s074)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт и границы | Evidence / фактическая проверка | Источники |
|---|---|---|---|
| [F322](RAW_FACTS.md#f322) | Сторонний pinned2026 `run_resnet50_parallel_direct.py` создаёт subprocess на пару device/shard. Код реализует выбранное распределение; нет утверждения производителя о невозможности другой topology. | Source201–259; не hardware test. | [S074](SOURCES.md#s074) |

<a id="f323"></a>

### F323 — W2-G уже воспроизвёл отсутствие exception-path destroy с fake native15.0.24. Реальный normal-path buffer destroy включён. Array output является view с сохранённой Python buffer own

- Исходный локатор: [W2-M-F10](_WORK/W2_M_RESULT.md), строка26; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт и границы | Evidence / фактическая проверка | Источники |
|---|---|---|---|
| [F323](RAW_FACTS.md#f323) | W2-G уже воспроизвёл отсутствие exception-path destroy с fake native15.0.24. Реальный normal-path buffer destroy включён. Array output является view с сохранённой Python buffer ownership в проверенной среде; dangling не доказан. | Reused W2-G source/helper evidence, новый duplicate probe не выполнен. Current `.so`/source отсутствуют; modern fix или сохранение bug не установлены. | [S065](SOURCES.md#s065) + [F267](RAW_FACTS.md#f267)/[F320](RAW_FACTS.md#f320) |

<a id="f324"></a>

### F324 — `test_watchdog_error.py`15.0.24 skipped, основной body не исполняет inference (`...`), опасный сценарий остался комментариями. Это historical development note о программе, а не акт

- Исходный локатор: [W2-M-F11](_WORK/W2_M_RESULT.md), строка27; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S065](SOURCES.md#s065)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


| ID | Установленный факт и границы | Evidence / фактическая проверка | Источники |
|---|---|---|---|
| [F324](RAW_FACTS.md#f324) | `test_watchdog_error.py`15.0.24 skipped, основной body не исполняет inference (`...`), опасный сценарий остался комментариями. Это historical development note о программе, а не актуальный reproducer Runtime2026. | Source1–40; watchdog/invalid device buffers/fault programs не запускались. | [S065](SOURCES.md#s065) |

<a id="f325"></a>

### F325 — Version/evidence matrix

- Исходный локатор: [W2-M-MATRIX-19](_WORK/W2_M_RESULT.md), строка31; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: source_code / primary_documentation; see record.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S019](SOURCES.md#s019), [S003](SOURCES.md#s003), [S064](SOURCES.md#s064), [S063](SOURCES.md#s063), [S065](SOURCES.md#s065), [S169](SOURCES.md#s169), [S074](SOURCES.md#s074), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S082](SOURCES.md#s082)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Version/evidence matrix

Это matrix области доказательств, **не таблица совместимости**.

| Версия / источник | Lifecycle и concurrency, которые реально прочитаны | Что не переносить на2026 |
|---|---|---|
| pytpu14.7.0, upload2023-04-11 по actual PyPI JSON | Coroutine submit+callback, несколько Inference на device; generic status enum0/1/2 | Нельзя использовать старый polling helper как современный timeout/cancel; callback result ignored; нет current ABI pairing |
| pytpu15.0.24, upload2023-11-27 | Sequential reuse docstring; multithread test со своим Inference per thread; normal destroy; omission after exceptional yield; two native error boundaries | TODO mismatch не означает current broken concurrency; source omission не измеряет native leak; output view не доказывает dangling |
| Guide2025 `RU.РМДВ.04.06.014-03 34 01` | with-style runtime example, DEFAULT/STAGING compilation guidance | Не error table и не обещание thread safety/recovery; чтение existing extraction, без новой PDF/visual проверки |
|2026 vendor benchmark Runtime16.18.6 / Framework2026.8.43 | Версии среды заявленного измерения из W1/W2-I | Не номер полученного Python package, не release notes, не гарантия исправления старого cleanup |
| Third-party repo commit3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140,2026-04-03 | Process-per-device/shard orchestration автора | Не constraint runtime; только source выбранного sample |

<a id="f326"></a>

### F326 — Symptom → owner → evidence → differentiating check → safe action/version

- Исходный локатор: [W2-M-MATRIX-20](_WORK/W2_M_RESULT.md), строка43; контекст проверки23.10.2026; даты/версии первоисточников — в S.

- evidence_type: unknown.

- actual_check: read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run.

- Sources: [S019](SOURCES.md#s019), [S003](SOURCES.md#s003), [S064](SOURCES.md#s064), [S063](SOURCES.md#s063), [S065](SOURCES.md#s065), [S169](SOURCES.md#s169), [S074](SOURCES.md#s074), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S082](SOURCES.md#s082)

- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.


### Symptom → owner → evidence → differentiating check → safe action/version

Owner — владелец **границы**, не назначенный виновник. Матрица дополняет W1-12 exact exception templates, не переизобретает их как реальные логи. В2026 сначала читается matching bundle; literals2023 используются для распознавания только если installed source совпал.

| Symptom / версия | Owner(layer) | Evidence | Differentiating check | Safe action / stop condition |
|---|---|---|---|---|
| Import/dependency/native library load error; любая фактическая поставка | Инженер окружения, host package/loader | W2-A delivery; historical lazy loader15.0.24 | Executable/package path, full chained traceback, actual METADATA, `.so` dependencies; простое import отделить от первого native вызова | Исправить exact environment по manifest. Не повторять inference и не менять Python/runtime наугад. Driver reset не исправляет missing wheel/library. |
| Нет устройства в listing / endpoint недоступен | Runtime owner совместно environment/доступ | Historical listing слабее init; online mode W2-L не установлен | Direct Linux: отличить granted device node/passthrough/access от permission; remote API: только supplied health/version/error schema. Нет shell не означает нет LinQ | Сохранить topology и состояние доступа; запросить provision/permissions у владельца. Не менять общие права или driver. |
| `Invalid init code…` / `Invalid device…` в **matching15.0.24** | Native init / provisioning; runtime owner собирает | `_bindings.py`215–221; не расшифрованный код | Точное сообщение+код; до любой load; один granted device; сравнить штатный matching invocation с тем же manifest | Без таблицы не называть PCI fault/ресурс занят/необходим reset. Один диагностический clean-process open допустим после штатного закрытия своего предыдущего процесса; результат локализует state scope, не ремонтирует hardware по гарантии. Повторное init failure → vendor/admin. |
| `Invalid program…`, load error или target mismatch | Model/artifact owner + runtime ABI boundary |15.0.24 Program validation/load; historical hardware mismatch test W1 | Hash `.tpu`, compiler/target/release pairing, actual metadata; baseline и suspect artifact на той же validated среде | Исправить/rebuild согласованный artifact. Reload только документированным lifecycle после quiescence. Не перебирать I/O имена и не сбрасывать device ради malformed/несовместимой программы. |
| Mapping/key/shape/dtype/layout error, выявленный **до submit** | Model adapter/host | W2-G narrow validation; NumPy/app exceptions не hardware status | Запись фактического input spec против shared golden manifest; указатель не несёт numpy shape/strides | Отклонить запрос, исправить host tensor. Если доказано отсутствие native вызова и session lifetime не прерван, этот symptom сам по себе не требует process replacement. Unknown keys не подавлять общим native retry. |
|15.0.24 `Invalid tpu_run_inference return code…` либо `Invalid inference status code…` | Native submit/run vs completion, runtime owner | `_run`373–382 и `_check_status`418–425 — **две разные границы** | Сохранить оба доступных статуса, полный C message, artifact/input hashes, phase. Сравнить baseline valid request, а не blanket retries | Остановить admission на эту session; известность API определяет drain/close. Не выводить recovery из числа0/1/2 другого release. Reuse/reload только с matched recovery contract; при его отсутствии bounded new-worker diagnostic после завершения старого request, либо vendor. |
| Клиентский deadline истёк, native/server completion не подтверждён | Service/queue owner до выяснения native state | Current timeout/cancel contract не получен; old async polling не cancel | Был ли request submitted? Получен ли terminal status? Есть ли job/request ID, supported cancel acknowledgement и idempotency? Host timer и native timeout — разные события | Pending job считать in-flight/unknown, остановить admission, продолжить разрешённое наблюдение. Не отправлять duplicate автоматически и не освобождать buffers/handles до documented completion/cancel. Для persistent зависания → support; worker kill не объявлять safe cancellation. |
| Output mismatch при успешном status / только под threads | Model parity owner и runtime concurrency owner |15.0.24 test печатает mismatch без assertion; W2-G output ownership | Повторить serial golden A/B, сохранить отдельные I/O copies/hashes, ids и session generations; исключить shared mutable input/output и decoder mix-up | Вернуть наш service к проверенной serial конфигурации, сохранить first mismatch. Не считать status0 numerical proof, не «лечить» reset. Current parallel contract/bug report нужны отдельно. |
| Exception в приложении после завершённого inference; подозрение на resource growth | Runtime lifecycle owner | W2-G fake-native omission15.0.24; current fix unknown | Где exception относительно open/load/submit/completion/close? Реально вызван ли documented cleanup? Сравнить normal exit и ordinary host exception; RSS не равен native leak | Для15.0.24 избегать продолжения неопределённого ownership; одно штатное закрытие, без duplicate destroy. Для current использовать его contract. Отдельная own worker replacement после quiescence — mitigation приложения, не доказанная необходимость и не гарантия освобождения driver resources. |
| Clean own worker с baseline тоже не может init/load/run | Runtime owner → vendor/admin boundary | Сравнительный эксперимент, пока не выполнен | Manifest/permissions unchanged? baseline hash identical? Есть ли same release successful baseline до события? Ошибка до/после open? | Сохранить packet и прекратить повторяющиеся нагрузки. Администратор решает scope recovery: session/job/device/service. Никаких выдуманных unload/reset/reboot команд. Нельзя объявить hardware broken лишь по двум failures. |
| После reconnect поступил старый результат, frame/event продублирован | Service orchestration owner | Наше проектное правило, не LinQ feature | request_id + worker/session generation + frame timestamp + artifact version, outstanding ledger | Отбраковать stale generation, дедуплицировать события; transport retry только с documented idempotency. Worker replacement не разрешает автоматически replay неизвестного in-flight request. |

**Что сохранять до retry:** первый полный traceback/stderr и native message без обрезания; timestamp+monotonic duration; request/frame id и generation; фазу open/load/submit/complete/close; received code namespace+version; immutable artifact/input hashes и spec; среду/SDK/native/driver/firmware из общего manifest; device/job identity в разрешённом объёме; output arrays/shape/dtype/hash, если получены; outstanding/admission state; действия после сбоя с outcome. Credentials, tokens и кадры с ограниченным доступом не включать в публичный packet. Один packet/file на исходный инцидент, retries ссылаются на него и не заменяют исходную ошибку последней.

## Сводные карточки сборщика: актуальная область, матрицы и actual checks

<a id="f327"></a>
### F327 — IVA CV1.8: старое «СИЗ на лицах» означает COVID mask regime

- evidence_type: primary_documentation.
- actual_check: read_saved_text; no PDF image or runtime.
- Sources: [S170](SOURCES.md#s170).
- Context:23.10.2026; версии/даты документов и unknowns сохранены в тексте; это синтез сохранённых доказательств, не новая web-волна.

W2-K прочитал отдельный пользовательский guide IVA CV1.8,71pages; filename2021.07.22 (не доказанная дата публикации), uploads/2024/03 (не дата редакции). Раздел 6, PDFpage21/печатная p21 связывает «СИЗ на лицах» с медицинскими масками и COVID-19. Это не доказательство industrial helmet/respirator head и не LinQ execution. Новый W2 документ принадлежит той же IVA CV vendor lineage. Нельзя смешивать его с 13-page current UI guide или 20-page admin deploy guide. Exact source: W2_K_RESULT.md, раздел «Новая зацепка», S06; сохранённый source locator S170.

<a id="f328"></a>
### F328 — Реальный Model Zoo TinyYOLO3: operator inventory и граница diagnostic derivative

- evidence_type: local_observation.
- actual_check: actual saved binary protobuf inspection; CPU run separately F247.
- Sources: [S143](SOURCES.md#s143), [S152](SOURCES.md#s152).
- Context:23.10.2026; версии/даты документов и unknowns сохранены в тексте; это синтез сохранённых доказательств, не новая web-волна.

Сохранённый `_WORK/W2_E/GRAPH.JSON`: IR6, producerkeras2onnx1.6.0, domain""opset11. Exact original graph counts: `Conv`=13; `BatchNormalization`=11; `LeakyRelu`=11; `MaxPool`=6; `Resize`=1; `Concat`=15; `Transpose`=3; `Identity`=5; `Squeeze`=13; `Shape`=3; `Cast`=46; `Reshape`=12; `Unsqueeze`=29; `Slice`=39; `Mul`=13; `Div`=20; `ReduceMin`=2; `Round`=2; `Sub`=10; `Ceil`=4; `Loop`=4; `Tile`=4; `Exp`=2; `Sigmoid`=6; `Add`=4; `NonMaxSuppression`=1. Это inventory конкретного скачанного ONNX, не объявление LinQ support для этих operators/attrs. Input image_shape участвует во встроенной геометрии, b2 падает в Squeeze. Diagnostic in-memory derivative сохраняет ancestors двух conv outputs и удаляет image_shape/decode/NMS; его finite b1 outputs не доказывают full-graph b2 либо strict exporter parity. Source/protocol: GRAPH.JSON, HOST_PROBE.py/RESULT, F244–F247.

<a id="f329"></a>
### F329 — Текущая component/version/access matrix без смешения поколений

- evidence_type: normalized_documentation_matrix.
- actual_check: saved sources read; SDK install/compile not run.
- Sources: [S003](SOURCES.md#s003), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S063](SOURCES.md#s063), [S065](SOURCES.md#s065), [S090](SOURCES.md#s090), [S169](SOURCES.md#s169).
- Context:23.10.2026; версии/даты документов и unknowns сохранены в тексте; это синтез сохранённых доказательств, не новая web-волна.

| Слой | Что установлено | Версия/условия | Доступ/неизвестное |
|---|---|---|---|
| Framework guide | frozenGraphDef/ONNX → onnx_direct.onnx_to_tf → quantization → Network → compile → TpuProgram | guide2025 RU.РМДВ.04.06.014-03; Ubuntu20.04/Python3.11/RAM≥32GB | public text; wheel `tpu_framework-py3-none-any.whl` не получен; dependency lock unknown |
| Framework benchmark | обозначена TPU Framework2026.8.43 | Ubuntu24.04/i7-10700K; Python/TF unknown | vendor-reported environment; не предоставленная поставка |
| Runtime benchmark | TPU Runtime16.18.6 | exact Python package/native/driver pairing unknown | нет current bundle/reference; не выводить incompatibility из отличающихся version numbers |
| Website software | Python3.8 API+CLI; OEM; LinQCompiler/DNNQuant/Model Zoo | undated /sol | downloads после registration+verification; user outcome unreported |
| Third-party builder | RegularModel.calibrate → quantize(thresholds) → qm; Network tuple/set_batch; O1/O5 | pinned3ad1b7a; numpy1.26.4, ONNX~=1.16, ORT~=1.18, TF2.14.1; torch unpinned, ultralytics separate | source есть, matching wheels/weights/.tpu/logs нет; O1 ≠ доказанный DEFAULT |
| pytpu15.0.24 | Device/Program/Inference ctypes | upload2023-11-27; Python≥3.6, numpy; `/usr/lib/libtpu.2.so` | sdist/hash реально прочитаны; no native binary; no current ABI guarantee |
| pytpu14.7.0/13.0.13 | async/helper либо external native loader | uploads2023-04-11/2021-12-01 | actual sdists; README statistics не реализованы доступным source; не current profiler |
| iva-applications11.0.1 | host model utilities, Tiny postprocess | upload2021-10-13; actual MIT LICENSE2020 | source доступен; старые TF/Keras/pytpu deps; нет weights/.tpu/compiler |
| TLM | guide describes HardwareNetwork/model simulator | exact available current version unknown | optional supplied checkpoint; не обязательная предпосылка hardware smoke |
| Driver/firmware | отдельный LinQH1 driver в hardware guide; names libtpu/tpu-dkms в авторском scenario | current versions/kernel/glibc/ISA unknown | актуальные binaries/install/recovery docs не получены |
| Windows/WSL/ARM | HPS claims heterogeneous integration; workstation client feasible conditionally | no tested Windows framework/native package or WSL guarantee | `py3-none-any` не устанавливает поддержку всего стека |


<a id="f330"></a>
### F330 — Модели: точный уровень доказательства и первая незакрытая граница

- evidence_type: normalized_source_matrix.
- actual_check: no custom LinQ compile/run verified here; CPU Tiny test explicitly separated.
- Sources: [S002](SOURCES.md#s002), [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S044](SOURCES.md#s044), [S143](SOURCES.md#s143), [S075](SOURCES.md#s075), [S136](SOURCES.md#s136).
- Context:23.10.2026; версии/даты документов и unknowns сохранены в тексте; это синтез сохранённых доказательств, не новая web-волна.

| Кандидат | Конкретная конфигурация | Сильнейшее доказательство | Неизвестный gate |
|---|---|---|---|
| VendorTinyYOLO3 | внешний `tiny_yolo3_b8_o5_128x128_asic.tpu`; runner expects NHWC8×416×416×3 float0..1 | author RUN_SCENARIO says done HP/HPD; source recipe | binary/hash/original checkpoint/userI/O/pre/post/golden отсутствуют; no our LinQ run |
| Strict Tiny export | pinnedDarknetcfg+hashedweights; Keras/tf2onnx source, opset13, raw heads | actual conv checkpoint lineage with Model Zoo13kernels; exporter source | actual strict export/BN/runtime parity не выполнены; BGR sidecar конфликтует с RGB origin |
| Model ZooTiny original | actual35,511,756B ONNX, opset11/IR6; NCHW+image_shape; decoded+NMS outputs | actual ORT1.31CPU b1 success, b2Squeeze failure; anchors/NMS bytes | LinQ import/compile не проверены; full-graph parity со strict/vendor false/unknown respectively |
| YOLOv8n/s detection | source-detailed v8s default640/opset13/noNMS; upstreamv8.3.0 explanatory source | pinned exporter/build/runner; host helper defects established | author weights/ONNX/.qm/.tpu/logs absent; exact exporter package unknown; SDK float parity first |
| ClassicYOLO5s | vendor name yolo5s b1 benchmark106.1HP/424.4HPQFPS | reported slide; upstreamv5v7.0 supports explicit5+nc interpretation | vendor weights/exporter/input/task exact not supplied; no link to v7.0 proven |
| YOLOv5su | historical27.02.2026 author script defaultyolov5su.pt | source skeleton, objectness-free upstream terminology | не classic5s; no actual artifact/success evidence |
| YOLO11 detection | family claim; source-yaml/control head | vendor family list | нужно exact matched detection sample; OBB result не переносится |
| YOLO11lOBB | ВКР abstract20FPS, ранее записанные bench measurements | independent author metadata/abstract, not full protocol | shape/batch/SKU/runtime/weights/denominator unknown; стенд повторно недоступен; не PPE horizontal detector |
| yolov8n_pose | vendor2026 b1,104.8HP/419.2HPQFPS;21.51ms text | reported measurement table | pose ≠ detection; input/weights/quality/logs unknown |
| FCNResNet50 | torchvisionCOCO_WITH_VOC_LABELS_V1,21labels, NCHW520; dynamic export laterinput patch | source+author negative O5 final reproducibility note | не vendorFCN_8s; no finalO5 verified result/no published logs |
| CustomResNet50 | IMAGENET1K_V2,224, NHWCuint8 wrapper with normalization inside | source exporter and independent-device replication harness | not vendor resnet50_mlperf artifact; no actual author binaries/logs |
| IVATech2020ResNet50 | AlveoU200/250MHz, INT8 input, TF1.15; accuracy75.756% | actual published MLPerf logs+system+harness | historicalFPGA, not modern LinQH1M performance or ASIC compatibility |


<a id="f331"></a>
### F331 — Современные и исторические measurement records: условия и неизвестные

- evidence_type: reported_measurement + normalized_scope.
- actual_check: read_saved_tables/logs; none is our LinQ benchmark.
- Sources: [S033](SOURCES.md#s033), [S026](SOURCES.md#s026), [S075](SOURCES.md#s075), [S077](SOURCES.md#s077), [S165](SOURCES.md#s165).
- Context:23.10.2026; версии/даты документов и unknowns сохранены в тексте; это синтез сохранённых доказательств, не новая web-волна.

Современная полная 14-row таблица сохраняется в F130; W2 clarifications F281–F286. Общая сноска Runtime16.18.6/Framework2026.8.43/Ubuntu24.04/i7-10700K; per-model input/weights/calibration/precision/scenario/preset/quality/timer boundaries/latency statistic/device allocation неизвестны. HPQ=ровно 4×HP throughput во всех 14 строках; одинаковая latency. Это не доказывает arithmetic origin и не single-request speedup. `anti_spoof_mn3:985,72 ms`, `lenet5:128,90 ms` оставлены буквально; без original visual/correction нельзя менять на us. SSDMobileNetV2b8=428FPS против 556.7b1 также не исправляется. p3ResNet460/1046 отличается от p4 432.9/1112.8; reason unknown.

HPS datasheetResNet50b1≈2.3ms/optimizable1.5ms относится другому уровню/неполным условиям. University443/430/142/20FPS остаются abstract-level prior measurements, не comparable current protocol. Исторический AlveoU200Single Stream VALID: p9012.230138ms, mean12.081844ms, p9912.345478ms; OfflineVALID88.8239samples/s и query276.682437431s для 24576samples; accuracy75.756%/50000images. Это чужой FPGA run2020, не current ASIC и не наше измерение. MLCommons policy pinned2026 различает scenarios и разрешённый untimedpreprocess; он не устанавливает scenario/revision производителя. Число камер не выводится ни из одной строки; требуется quality-checked artifact и actual common-window workload, frameage/drop/fairness.

<a id="f332"></a>
### F332 — Видео: границы documented / conditional / unknown

- evidence_type: primary_documentation + engineering_recommendation.
- actual_check: source-only; no RTSP/service deployment benchmark.
- Sources: [S030](SOURCES.md#s030), [S026](SOURCES.md#s026), [S027](SOURCES.md#s027), [S103](SOURCES.md#s103).
- Context:23.10.2026; версии/даты документов и unknowns сохранены в тексте; это синтез сохранённых доказательств, не новая web-волна.

| Стадия | Установленное | Неизвестное / зависимость |
|---|---|---|
| Decode/ingest | image dataset runners не RTSP; IVA CV принимает камеры/файлы/потоки | actual online payload/codec/reachability/CPU budget; HPS optionalvideoencode недоказанный decode на LinQH; HXdecoder относится RK3588 |
| Preprocess | точные контракты отдельных ResNet/YOLO/Tiny/FCN | universalLinQpreprocess отсутствует; current native user↔raw transform unknown |
| NNgraph | guide `.tpu` → local runtime documented | actual custom model execution/wholegraph coverage/partialfallback not established |
| Decodehead/NMS | host явно показан в pinned runners; Tinyraw decode и NMS наружу | допустимость вконкурсе/ONNXNMS lowering/current service built-inNMS unknown |
| Tracking/PPEassociation/rules | слой будущего сервиса; IVA CV отдаёт события | accelerator API trackIDs/temporal semantics не установлены; absence violation ≠ singleobject metric |
| Event/storage/UI | IVA CVEdge-api → MongoDB → VDMS/UI documented | не API хакатона; UI event list не backendinventory/throughput;500msjobinterval/10sstuckrestart не SLAinference |
| Queues/timestamps | boundedper cameraqueue/fairdispatch/stream_epoch+frame_seq — наша recommendation | actual vendor quotas/cancel/order/persistence неизвестны; no invented defaultFPS/TTL/ports |


<a id="f333"></a>
### F333 — Actual checks: сохранённые протоколы и точный предел вывода

- evidence_type: local_observation.
- actual_check: read actual saved protocols during assembly; no re-execution/no new external evidence.
- Sources: [S152](SOURCES.md#s152), [S160](SOURCES.md#s160).; [S172](SOURCES.md#s172); [S173](SOURCES.md#s173)
- Context:23.10.2026; версии/даты документов и unknowns сохранены в тексте; это синтез сохранённых доказательств, не новая web-волна.

| Protocol | Фактически сохранённый исход | Предел |
|---|---|---|
| `_WORK/W2_E/HOST_PROBE_RESULT.JSON` | utc2026-10-23T02:02:11.352325Z, ORT1.31.0, CPUExecutionProvider; b1 outputs float32(1,2535,4), float32(1,80,2535), int32(1,0,3); b2errorSqueeze dimension0 must1instead2 shape{2,2} | actual CPU model inference; synthetic constant image; no accuracy/FPS/LinQ claim |
| `_WORK/W2_E/HOST_PROCESS_RESULT.JSON` | return code0, stdout2029bytes, stderr858bytes | caught b2 failure сохраняется; первая PowerShell exit1 неуспех b2 и некрах всего experiment |
| `_WORK/W2_E/PARAMETER_COMPARISON.JSON` | consumed35,434,956bytes==file_size;13kernel_exact,2finalbiasexact; BNaffine algebra epsilon.001hypothesis | no strict exporter execution; no vendor.tpu lineage |
| `_WORK/W2_D/SCHEMA_PROBE_RESULT.json` | nc1/2/3shape fail;85accepted;(1,6,84) → (1,84,6); oldobj.1×class.9=.09 vswrong.9/class1 | actual Python shape-only helper+source arithmetic, no torchNMS/model/TPU |
| `_WORK/W2_G/HOST_PROBE_RESULT.json` | CPython3.11.9/NumPy2.4.2, native_loadedfalse; normaldestroyyes, exceptiondestroyomitted; view mutation visible; afterctxgcvalues[1.25,-2.5], pointeralive | fake native/controlflow/ownedhostmemory; no currentnativeleak/dangling/deviceerror demonstrated |
| `_WORK/W1_10/CONTRACT_PROBES_RESULT.json` | uint8descriptor → int8; Unicodeattributeabsent; letterbox formulas1920×1080/641×479 | helper/formula-only; OpenCV pixels/model/runtime notrun |
| PDF guides/presentation/IVA CV | text extraction and alternative fetches; no originalPDFimage actually inspected | no visualverification; screenshotlink/plaintextremoteclaim ≠ viewedpage |


