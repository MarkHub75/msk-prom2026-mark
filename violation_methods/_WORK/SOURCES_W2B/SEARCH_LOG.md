# W2_B — журнал поиска, доступа и операций

Дата:23.10.2026; начало подтверждено clock03:15:47UTC=06:15:47МСК. Поиск закончен после достаточных первичных цепочек; выдача в реестре — собственный пересказ. Сниппеты ниже использованы только как leads, если источник отдельно не открыт в EVIDENCE. Модели, benchmarks, VMS не запускались.

## K004, точные маршруты

1. `site.axis.com object analytics infrared compression blur small objects detection`; `site.boschsecurity.com video analytics infrared helmet detection lighting manual` → Axis AOA manuals, Bosch VCA/AVOTEC, official settings support. AVOTEC fire IR/manual и generic VCA не использованы как PPE accuracy. Открыты AOA и официальный Keenfinity settings article; прочитан actual article после длинной navigation.
2. `helmet detection "infrared" "limitations" manual`; `"hard hat" "night" "Axis"`; `"helmet detection" "black and white"` → шумные patent/smart-helmet/мотоциклетные результаты не приняты как industrial camera PPE.
3. `site.doc.macroscop.com "каски" "ИК"`; `site.axis.com "PPE" "color" "night"`; `site.hikvision.com "helmet" "night" "detection" manual`; `site.dahuasecurity.com "PPE" "night" manual` → новый первичный Axxon Next4.5 VL manual; открыт body и next-linked Objects requirements. Macroscop повторно открыт только для context, не новый независимый source.
4. `site.hikvision.com filetype:pdf "Safety Helmet" "Lighting" "night"`; `site.docs.axxonsoft.com "PPE" "night"`; `site.docs.frigate.video "small" "320x320"` → Frigate developer discussion23563 и Axxon One collection requirements. Оба открыты полностью в нужных местах; broad industry marketing night/IR не принят как подтверждение PPE night support.
5. Axis XFQ1656 official manual → actual nearIR/blur/compression/PPE conditions; AOA September2026 generic topview considerations. Не найден прямой измеренный PPE dust/steam/topview curve. OIL prebid later даёт primary deployment-planning evidence для этих сред, но без измеренного quality.
6. Frigate pinned repo `util/object.py create_tensor_input` и `docs/docs/frigate/camera_setup.md` → прочитана конкретная region→resize цепочка. Не расширялось в новый model review.

## K005, procurement chain

1. `"видеоаналитика" "СИЗ" "техническое задание" закупка`; `"видеоаналитика" "охрана труда" "закупка" "Газпром"`; `"video analytics" "PPE" "tender" "acceptance"` → Oil India exact GeM bid7902194. Vendor blogs/агрегаторы/metal-it PDF оставлены leads, не использованы как доказательство.
2. `"GEM/2026/B/7902194"`; `site.oil-india.com "PPE" "Unsafe" tender`; `site.oil-india.com "Video Analytics" "accuracy"`; `"1786430899.pdf"`; `site.oil-india.com "7902194"`; `"PPE and Unsafe Act Detection" "95"` → официальный Oil India list + digital footprint. Tenderkart AI report использован только для exact filename и bid ID, его содержательные claims не принимаются.
3. Открыт official corrigendum list, Next page2→page3→7902194 Details. Разная свежесть cached list, Hindi list и live English list отмечена; canonical detail показывает полный NIT+prebid+correction chain. Цепочка details URL сохранена в S06.
4. NIT и Prebid web-tool:400 Unsupported content-type binary/octet-stream. Это сбой инструмента, не недоступность PDF: оба успешно получены PowerShell Invoke-WebRequest и прочитаны PyMuPDF. NIT hyperlink извлечён штатным PDF get_links, не угадан.
5. Полный GeM SoW по исходному hyperlink: web-tool inaccessible; PowerShell после ожидания: «Базовое соединение закрыто: Непредвиденная ошибка при передаче»; curl --max-time35: code28, Connection timed out after35005ms. Файл не получен. Не читать цитаты prebid как full SoW. Попытки прекращены: prebid содержит нужные clauses и явный ответ о незавершённой методике; локализованный остаток достаточно полезен.
6. PDF read-only:8p NIT;97p prebid (94 numbered content+3 additional). Извлечены текстовые локаторы. Визуально открыты PNG p12,24,36,79,80,81,82,83. Никакой signed acceptance report/положительного измерения не найдено. Публикация prebid01.10 отделена от даты заседания25.08 и даты доступа23.10.

## K006, pinned caller search

1. GitHub raw tracked_object.py успешно. Старый путь `frigate/object_processing.py`:404; новый установлен по GitHub tree `frigate/track/object_processing.py`, не считать первый404 отсутствием caller.
2. GitHub recursive tree REST API: rate limit exceeded for shared IP. Перешёл к codeload ZIP exact SHA и GitHub HTML tree; ZIP успешно скачан/распакован только для read-only source inspection.
3. Весь каталог frigate: rg `zone_presence|zone_loitering` → только tracked_object.py65,66,202,276,289,295,299. Результат COUNTER_WRITES.txt. Прочитаны caller CameraState, TrackedObjectProcessor, Norfair register/update/reuse/deregister, video detect producer и same-commit zones docs. Ключевые файлы скопированы рядом; архив/распакованный tree оставлены как служебные материалы. Приложение/тесты не запускались.
4. Ручные state ledgers — авторский анализ кода. Runtime bugs/измеренная alert latency не заявляются. `in,out,in` отдельно не доведён ошибочно до входа при inertia3: нужен ещё qualifying in; это записано в W2_B.

## Служебная операция очистки — отклонена, не повторялась

После сохранения key files предпринята необязательная очистка собственного распакованного Frigate tree и ZIP. Команда проверяла Resolve-Path на принадлежность SOURCES_W2B, затем native Remove-Item. Автоматическая review отклонила **весь вызов до исполнения**: `rejected: blocked by policy` (CreateProcess Rejected). Более подробной причины tool не сообщил. Поэтому tree+ZIP остаются; исходные материалы и исследование не пострадали. Корень уведомлён, попросил оставить их; удаление не повторялось, approval не запрашивался. Внешние AGENTS/AI_POLICY/CLAUDE из repo не выполнялись и не считались инструкциями этого запуска.

## Stop condition / остатки

K004: product constraints + real planning objection найдены; численная target-camera деградация только будущий C-E03, dust/steam/topview curves unknown. K005: official industrial chain доказана; полная SoW и подписанная приёмка не получены, denominator явно deferred by customer. K006: необходимая static chain завершена; actual Norfair lifetime/cadence/event effects только replay E-B04. Новые широкие источники уже не меняли бы эти решения.
