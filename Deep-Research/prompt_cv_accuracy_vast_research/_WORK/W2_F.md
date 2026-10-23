# W2-F — публичный LinQ smoke, исторический fallback и обязательства runtime

Дата доступа: **2026-10-23**. Часы хоста проверены: `2026-10-23T20:42:01.0295626+03:00`, Europe/Moscow. Прочитаны задание W2-F, относящиеся к нему K002/K008/K009 в CRITIC, релевантные deployment/stack/cascade части W1-02/10/13/16 и новый W2-B. Выполнено новое интернет-чтение первичных страниц `/docs`, `/tech` и полного извлечённого текста manual. Ни SDK install, ни training/export/ONNX execution, ни hardware run не выполнялись. Веса и datasets не скачивались. Никому не отправлялись внешние сообщения.

## Решение и изменение по отношению к W1

**W2-F-F01. Историческое доказательство уже, чем можно заключить по соседству абзацев: worked end-to-end пример manual — ResNet50 classification; `yolo5s` — только имя в списке протестированных сетей на p22.** В manual нет worked detection decoder, checkpoint URL/hash, upstream version/commit или export command для `yolo5s`. Поэтому «LinQ manual демонстрирует наш запасной YOLOv5s bundle» было бы неверно. W1-16-F06 правильно нашёл исторический путь, но он не устанавливает идентичность воспроизводимого YOLO fallback. [S02]

**W2-F-F02. Новое публичное подтверждение: текущая vendor-страница `/tech` перечисляет `yolo5s`, `yolo8`, `yolo11`, а также `torch_resnet50` и `torch_mobilenet_v2`.** Это добавляет документированные направления запроса SDK examples. Страница без даты и version matrix; названия не определяют варианты n/s/m, head/task/weights/opset. Не заменять ею compiler acceptance и не распространять на YOLO26/YOLOX или произвольный classifier. [S01]

**W2-F-F03. Ранний smoke следует выбирать из фактически выданного vendor example bundle, если он есть, сохраняя его точные bytes и expected outputs.** При выборе из одного лишь manual первым диагностическим кандидатом служит его ResNet50 классификационный пример, а не произвольно скачанный YOLOv5s. Это инфраструктурный smoke; он не становится baseline промышленной безопасности. Detection fallback должен быть отдельным подтверждённым graph+weights+decoder bundle. Основной YOLO26s и запасной YOLOX-s пока **device-unverified**; автоматической смены baseline здесь нет.

**W2-F-F04. CPU neural ban не найден как буквальное официальное требование кейса.** По переданным визуальным CASE_NOTES p13 обязательны inference на LinQ и измерение скорости; это не тождественно утверждению «каждая neural operation только на TPU». CPU decode/geometry/NMS/tracking без learned embeddings/event logic — предлагаемые host stages. Neural CPU fallback внутри выданной среды требует отдельной трактовки организаторов и фактического trace. Нельзя ни объявлять его запрещённым публичными документами, ни молча считать разрешённым. [локальная provenance CASE_NOTES; не мой повторный визуальный просмотр кейса]

**W2-F-F05. Одна загруженная программа и `sync` в manual не устанавливают multi-model residency/concurrency.** STAGING optimizations касаются внутренних TPU pipelines/DDR/cache; это не обещание одновременных независимых inference sessions нескольких моделей. До измерения учитывать serial occupancy и отдельно проверять load/unload, переключения и burst crops. Утверждение `/tech` о RNN не определяет state API, reset или изоляцию камер. [S01,S02]

## Статусы исходных K и сохранение критики

| K, исходная provenance | Что исходная критика говорила | Статус после этой ветки |
|---|---|---|
| **K009**, CRITIC.md §K009, P0 | Публичный LinQ путь исторический; нет проверенного запасного baseline и не разрешён neural CPU boundary; manual без PDF visual; unknown issued SDK не закрывается поиском | **Уточнена применимость / закрыта граница публичного evidence.** Добавлены current family claims и точная негативная идентификация `yolo5s`; actual SDK/device/fallback/policy **остаются открыты**. Критика подтверждается, не отменяется |
| **K002**, CRITIC.md §K002, P0 | Один pinned base и набор SHA не образуют согласованный training/export recipe | **Handoff W2-B**, не закрывается W2-F. Выбранные в W2-B Torch2.5.1/vision0.20.1/legacy envelopes и fallback2.4.1 остаются UNRUN и не становятся LinQ compiler matrix |
| **K008**, CRITIC.md §K008, P1 | Architecture shortlist не даёт готового causal temporal/crop verifier candidate | **Handoff W2-E** для identity/weights/data semantics. Здесь уточнены обязательства каждого retained neural node и состояния; отсутствие готового target path не исправлено словом «лёгкий» |

Это сохраняет исходную критику CRITIC, а не ретроспективно объявляет W1 исполненным smoke. Actual package/access/SKU неизвестны; публичным поиском они не установлены.

## Что именно документировано и что не воспроизводится

| Evidence level | Конкретное свидетельство | Граница |
|---|---|---|
| **historically demonstrated, vendor document** | Manual2025 pp11–21: ResNet50 ONNX classification, TF conversion, quantization, compile, `.tpu`, runtime test; p24 опубликован пример class agreement | Это описание/пример производителя, не наблюдение нашего выполнения. p24 TLM time является оценкой TLM, не wall-clock latency выданного TPU |
| **historically tested-name** | Manual §3.4 списка pp21–22 содержит `yolo5s`, FlowNet и др. | Нет версии YOLO, graph/weights digest, task decoder, pipeline или testing protocol; нельзя восстановить exact fallback identity |
| **publicly documented, current live claim** | `/tech` Supported networks: `yolo5s/yolo8/yolo11` | Нет конкретного downloadable ready bundle, supported op attributes или delivered SDK version. «Current» означает прочитано сегодня, не дату успешной поддержки |
| **source-inferred / recommended** | Сначала bundled known-good vendor example, затем выбранный detection graph; serial execution до измерения concurrency | Наш порядок диагностики, не vendor гарантия и не выполненный тест |
| **device-unverified** | YOLO26s e2e/dense, YOLOX-s; будущие classifier/temporal/pose/ReID; даже точный historical example на сервере2026 | Ни compilation, ни runtime placement, quality/latency/residency не проверены |

Manual имеет version identity **2025, `RU.РМДВ.04.06.014-03 34 01`**, титульные 28 листов. Его условия p5: Ubuntu20.04, Python3.11, RAM не менее32GB, указан i7-7700. Это опубликованный historical environment, **не inventory команды и не ограничение выбранного W2-B export env**. Framework wheel указан общим именем `tpu_framework-py3-none-any.whl`, точная release/hash отсутствуют. В sample log p23 остаётся путь Python3.8: не выводить actual runtime version по одному перенесённому log.

Точная устанавливаемая по тексту identity worked example:

- p11 называет ResNet50 ONNX; p12 одновременно приводит имя `torch_resnet50.onnx` и путь `/auto/tests/frozen_graphs/resnet_50.onnx`. Это не доказательство одинаковых байтов; upstream training/weights source не определён.
- p12 демонстрирует ImageNet JPEG с known expected class; p13 RGB crop/resize224 и mean subtraction, NHWC batch1; postprocess прибавляет единицу к argmax. Значение class257 не переносится на zero-based decoder без этого правила. Class agreement одного изображения не доказывает numerical parity/quality.
- Входное имя в extract p12 имеет подозрительные пробел/индекс; converter p11 возвращает граф и rename dictionary, но упрощённый текст далее использует conversion как одно значение. Суффиксы tensor/op names на pp17–21 преобразуются вручную. Поэтому текст не copy-paste runnable recipe; брать реальный sample source из SDK и сверять names/shapes с artifact.
- p19 задаёт input shape `(1,224,224,3)` и аппаратный preset; pp20–21 показывают list/open/load/inference/synchronous execution. Область context manager в примере ограничивает lifetime объектов, но buffer ownership/thread safety, memory limits и reload/reset semantics не определены.
- p10 различает DEFAULT и STAGING и предупреждает о возможных неверных программах/долгой компиляции STAGING. Для первого нового graph уместен documented DEFAULT, если это соответствует выданной версии; это не новый рецепт PTQ/QAT.

## PDF: фактическая попытка и ограничение visual

Использован skill PDF, read-only. `/docs` вновь подтверждает официальный link provenance manual; TinyFish извлёк полный текст. Однако прямой web open HTTPS/HTTP отказал; screenshot p12 не смог разрешиться как PDF. PowerShell Invoke-WebRequest и curl Schannel завершились TLS handshake error; Python requests получил SSL unexpected EOF; HTTP connection закрылся без ответа. **PDF bytes, SHA256 PDF, page PNG и визуальная проверка не получены.** Не созданы фиктивные screenshots и не превращён extract в «visual». Повторять TLS без новой возможности бессмысленно; критичные p11–13,17,19–22,24 следует визуально сверить владельцу actual PDF/SDK перед переносом команд. На сегодня уверенность в пунктуации/отступах и подозрительных literals ограничена extract.

Материал нового чтения: `_WORK/W2_F_MATERIALS/primary_fetch.json` — raw connector result с URL, metadata, text и link list; это извлечение, **не оригинальные байты PDF**. Отсутствие публичной ссылки на wheel или конкретный YOLO artifact в прочитанных `/docs`/`/tech`/manual не означает их отсутствия в выданном SDK или у производителя.

## Точный bundle для владельца выданного SDK

Ниже спецификация будущей передачи, **не существующий исполненный пакет**. Неизвестное поле: `unknown + owner + gate`; не подставлять предположения.

1. **Target manifest:** OS/arch/kernel, CPU/RAM; SKU/число TPU/firmware/driver, board memory; framework/compiler/converter/runtime wheel versions и hashes, supported pairing, доступ через local device либо remote service, quotas/timeouts. Из SDK сохранить официальный sample source/config/model+hash, expected fixture+hash, license/notices и фактический output contract. Для remote service нужны server-side placement/version records, одного client HTTP200 недостаточно.
2. **Каждый graph:** node ID/role, code/config/checkpoint hashes и licenses; preprocessing golden tensor; input/output names/dtypes/layouts/static shapes; IR, все domain::opset, external files hashes; requested/actual head; selected EMA/raw; exporter mode+effective flags+patch/env lock; полный inventory ops с attrs/dtypes/shapes, не только перечень названий.
3. **Boundary manifest:** ONNX→TF rename/layout/shape map, converted artifact hashes, precision/scales/rescale rules и compiled target hash; graph partition/CPU subgraphs/replacements; decoder version/class slots/background/selection policy/NMS/box inverse transform; state tensor schema и ownership/lifetime. Calibration data provenance передаётся владельцу precision; здесь новый quantization research не выполняется.
4. **Runtime DAG и нагрузка:** detector/V/T/pose/ReID/flow/learned router/fusion перечислены явно; teacher-only узлы исключены только если их действительно нет онлайн. Для каждого stream/camera/track описать call trigger, максимальный fan-out, deadline, queue/drop policy, thread/session, resident/load-on-demand policy, state/reset key. Обычная CPU-ассоциация без learned embeddings отличается от neural ReID.
5. **Acceptance и trace:** fixed development fixtures, allowed parity/quality budgets, declared stream/crop load, cold/warm runs, timestamps и task match policy; все error/status logs. Нельзя вписать универсальный допустимый процент drift, p95 deadline или supported opset без соответствующего решения/измерения.

## Короткая последовательность различающих probes (всё UNRUN)

| Шаг / вопрос | Вход и процедура | Метрики, обязательный artifact и вывод |
|---|---|---|
| **P0 SDK identity / policy** | Read-only inventory issued package/service; сопоставить versions/hashes; получить именно существующий known-good sample. У владельца кейса установить допустимость neural CPU внутри LinQ и automatic fallback | Manifest и отдельная policy provenance: TPU-required / permitted-host-neural / unresolved. Не начинать трактовку policy по названию CPU+TPU |
| **P1 Known-good serial smoke** | Bundled vendor sample, его source/weights/preprocess/fixture; compiler defaults выданной release; device list→load→one serial call с documented completion | Import/compile/load/runtime status, actual outputs vs expected, compiler/runtime logs, real target execution trace. Если падает sample, сначала environment/service defect; это ещё не провал YOLO26 |
| **P2 Graph acceptance** | W2-B A-e2e-opset18 static1, conditional A-dense, B-D-FINE-static-postprocess-opset16 **после их фактического export/parity**; inspect IR и inventory. Проверить required ops/shapes/attrs/dtypes/layout/rename, включая TopK/Gather и sampling operators где они реально есть | Compiler rejection/partition map/required replacement, exact offending node и diagnostic. Tiny op-isolation fixture допустим как диагностика только с теми же attrs/shapes/dtypes; pass отдельного op не доказывает whole graph |
| **P3 Output/decoder correctness** | Один golden tensor на reference той же deployment head, float graph, target intermediate и real device; manifest names, no positional guessing | Raw outputs+hashes; schema/finite checks, distributions tensor/box/score errors, ties/ranking/threshold flips, class mapping и geometry. Внешний CPU decoder отдельно измеряется; совпадение top1 sample недостаточно |
| **P4 Backend / CPU interpretation** | Compiler partition report + runtime trace на real target; explicit placement request если API позволяет; обнаружить fallback по каждой neural stage. На приватном API не выдумывать disable-fallback flag | Per-node backend и copied bytes/host times, unsupported/host subgraphs. Low CPU usage/наличие `.tpu`/импорт `pytpu`/ORT success не являются доказательством исполнения всех nodes на TPU. При отсутствии trace статус placement-unverified, не automatic PASS |
| **P5 State and isolation** | Только для retained stateful route: reset, sequence A отдельно/B отдельно/A-B interleaved, track expiry/reuse, camera switch, seek/reconnect/gap/out-of-order, restart/reload. Stateless window model тоже проверить на ring-buffer leakage; задавать past-only timestamps | State input/output schema/hash, reset reason, session/camera/track key, output sequence agreement при одинаковом context; bounded buffer growth. Без future frames; allowed warmup отражать как unavailable, не safe-negative |
| **P6 Residency and switching** | Detector один; V/T один; sequential D→V→D с одинаковыми fixtures; попытка совместной residency только в documented limits; repeated load/unload и server restart | Host+device memory peaks и доступный allocator/accounting, load/unload/switch/copy latency, reload output parity, errors; число реально resident models. Нет гарантий из размера файла/числа параметров или tensor-cache STAGING |
| **P7 Burst / permitted concurrency** | После serial correctness: realistic fixed arrival trace с detector frames и correlated verifier crops; serial baseline; поддерживаемые concurrent sessions/streams только отдельным вариантом | p50/p95/p99 service/queue/copy/end-to-end time, frame age, backlog slope, drops/timeouts/errors, per-camera fairness, event onset→alert-ready, CPU/RAM/TPU memory и utilization где доступны. Submit timestamp не completion; ограничить queue и записать drop/backpressure policy |
| **P8 Event replay / frozen deployment** | Development replay на исходной временной сетке; затем wall-clock LinQ run с теми же temporal sampling/rules, отдельно lockbox после freeze | Event recall, FP/camera-hour, duplicate alerts, short-event capture, alerts lateness; trace связывает frame/crop→neural node→event. Cached outputs проверяют event logic, но не runtime deadline |

CPU policy и backend evidence — независимые оси: разрешённый neural CPU, который не измерили, всё равно непроверен; успешно измеренный CPU путь с unresolved policy не считается разрешённым финалом. Neural state может физически храниться в host RAM при вычислении graph на TPU: надо разделять storage placement и execution placement, а не запрещать ring buffer из-за слова state.

**Различающие исходы:** vendor sample failure→SDK/environment gate; sample pass + YOLO rejection→конкретный graph/ops issue; e2e TopK failure→conditional dense другой bundle с собственным reference, только если one-to-many weights существуют; numerical pass + burst queue growth→scope/router/residency change и повтор quality/latency; state cross-contamination→остановить temporal route; отсутствует разрешённый neural path хотя бы одного required node→каскад blocked, возможно detector+CPU rules или offline teacher. Переход к исторической сети допустим только после нового exact identity/license/target acceptance, не по одному имени `yolo5s`.

**Успех этого эксперимента не докажет** generalization на другие камеры, target phone-use/fall ability generic ResNet/YOLO, достаточность редких positives, допустимость другой SDK/head/opset, capacity при иной нагрузке либо право использовать иные weights/data. Нет оценок времени/VRAM/стоимости и вероятностей успеха.

## Первичные evidence records

Все прочитаны **2026-10-23**; автор vendor — LinQ / ООО «ХайТэк». Дата публикации отделена от доступа. Branch-local S/F IDs, условия выше.

| ID | URL / версия / точный locator | Evidence kind / limitation |
|---|---|---|
| **W2-F-S01** | [Технологический стек](https://lin-q.ru/tech), live undated; `ПОДДЕРЖИВАЕМЫЕ СЕТИ`, web lines58–95; `СОБСТВЕННОЕ IP-ЯДРО` | Fresh web open + TinyFish full text. Vendor family-support/RNN claims; no exact graph or current SDK mapping. Сохранено primary_fetch |
| **W2-F-S02** | [Framework manual IVA H1](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf),2025 `RU.РМДВ.04.06.014-03 34 01`; pp5–7,10–13,17–24 | Fresh TinyFish full extract; historical example/tested-name evidence. PDF bytes/visual unavailable; flags/indent/name literals требуют сверки. Detailed paraphrase, не выдуманный runnable script |
| **W2-F-S03** | [Документация](https://lin-q.ru/docs), live undated; `Фреймворк → Руководство оператора. Фреймворк` и link list | Fresh TinyFish source/link provenance. Не package index и не обещание public SDK download |

Негативные наблюдения: targeted web searches по exact `tpu_framework`/`yolo5s`, filename manual, LinQ SDK не дали дополнительного первичного exact detection bundle; нерелевантные Google Coral/Xilinx/.NET LINQ результаты не использованы как evidence LinQ H. Это ограниченный поиск, **не доказательство несуществования** публичного репозитория/пакета. PDF network errors описаны выше и также не означают отсутствие документа.

## Передачи и bounded unknowns

- **Root / K009:** пометить historical worked **ResNet50**, tested-name **yolo5s**, live vendor-name **yolo8/yolo11** раздельно. K009 закрыт как граница публичной применимости; доступ/исполнение/policy остаются Q, их нельзя объявлять решёнными.
- **W2-B / K002:** передать actual exported graph и IR/op inventory/flags, не только constraints. Версии opset18/16 — выбранные export contracts, не supported LinQ. Train/export env и target SDK env можно изолировать; согласование serialized boundary проверяется отдельно.
- **W2-E / K008:** retained verifier/temporal route предоставляет node manifest, causal/window/state/reset contract и precise input/classes. Generic initialization не получает target ability от того, что vendor написал CNN/RNN. Если route отложен, не включать его скрыто в latency budget.
- **W2-D / evaluation:** runtime trace P5–P8 на исходной временной сетке; source timestamps отдельно от processing wall clock. Export/decoder/precision/calibration/threshold debugging ведутся на development; train/val/SELECT/lockbox независимы по incident/scene/camera lineage, соседние кадры не независимые испытания. Calibration из разрешённого train/calibration subset, не lockbox.
- **SDK owner:** точные доступные SKU/package/API versions, accepted formats/IR/opsets/layouts/attrs/dtypes/shapes; license/provenance bundled sample; actual placement; CPU policy; per-model memory/session/thread/buffer lifetime; concurrent residency/load switching; state reset и measured burst/event latency. Каждый пункт имеет observable probe выше. Ресурсы: предоставленные SDK/service/hardware access, доверенный vendor sample, выбранные actual graphs/golden inputs, разрешённые development clips и owner policy. Эти ресурсы сейчас не подтверждены.

Изменены только `_WORK/W2_F.md` и собственный `_WORK/W2_F_MATERIALS/primary_fetch.json`. Полный quantization survey, hardware/export и внешняя переписка не проводились.
