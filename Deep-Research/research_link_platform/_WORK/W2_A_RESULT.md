# W2-A — поставка, окружение, доступ и права LinQ

Назначение: K001, K002, K019, K020. Контекст — подготовка пяти инженеров к 45-часовому хакатону, ночь 23.10.2026 MSK. Новые сетевые проверки выполнены 23.10.2026 примерно 04:47–04:54 MSK; локальная отметка во время проверки: `2026-10-23T04:51:48.9130065+03:00`, отметка завершения записи: `2026-10-23T04:54:38.1522680+03:00`. Точное UTC-время архивной инспекции сохранено в `W2_A/SAVED_ARCHIVE_INSPECTION.JSON`. Прочитаны исходная задача, релевантные K критика, W1-03/04/13, ACCESS_HELP_RESULT, RUN_STATE и назначенные артефакты. Пользователь не подтвердил регистрацию/SDK; SDK/device access не получен. Регистрация, сообщения, установка, компиляция и inference не выполнялись.

## Решение и изменение относительно W1

**Одну полную современную воспроизводимую поставку восстановить не удалось.** Из реальной публичной навигации получены документы, но не executable bundle, современный wheelhouse или container digest. Это узкая граница наблюдения, а не утверждение, что таких поставок нет. Публичные Python bindings/helpers существуют, поэтому формулировка «всё исполняемое ПО закрыто» чрезмерна; они не составляют современный compiler/runtime комплект.

Новый первичный след — **индексированная копия реестра Минцифры с записью 32778 от 31.03.2026** и полным названием framework IVA H1, правообладатель ООО «ХАЙТЭК». Live-страницу получить не удалось двумя каналами, а карточка с release/install/license сведениями не прочитана. Запись нельзя считать manifest версии 2026.8.43 или разрешением распространения.

W1 не опровергнут в главном: Python3.8 на сайте, Python3.11/Ubuntu20.04 в guide2025 и Ubuntu24.04/Framework2026.8.43/Runtime16.18.6 в benchmark остаются разными контекстами. Нет основания ни объявлять guide отменённым, ни утверждать его точное соответствие нынешнему wheel. Новая архивная инспекция закрепляет лицензионную границу actual файлами и hash, а не значением `License: UNKNOWN`.

## Факты и статус проверки

| ID | Установленный факт / решение | Основание и фактический тест |
|---|---|---|
| W2-A-F01 | Повторно получены `/docs`, `/sol`, `/tech`, `/press`, `/hr` через TinyFish. Списки ссылок `/docs` и `/sol` ведут к документации, gate и формам; прямого современного wheel/registry/model-zoo URL в этих списках нет. | S01–S03; live content/navigation inspection. Никакой authenticated области не читали. |
| W2-A-F02 | `/docs` продолжает ссылаться на `Framework_manual_H1.pdf`; актуальный public index не предоставляет отдельный installation guide или release notes compiler/runtime в извлечённом списке. | S01. Это наблюдение списка, не отрицание существования закрытых документов. |
| W2-A-F03 | Software route по-прежнему отделяет регистрацию от верификации. Выписанные права текущего пользователя не установлены; доступ к публичному guide не равен download/access к устройству. | S02; live read. Форму повторно не исследовали и не отправляли. |
| W2-A-F04 | В списке `/press` открытый ZIP — `logo_linq.zip`, DOCX — `2025_about_linq.docx`, PDF — `2026_linq_presentation.pdf`. Это PR-материалы по явно данным названиям/подписям, а не подтверждённый SDK bundle. | S03; direct navigation links. ZIP/DOCX не загружали и их содержимое не заявляем. |
| W2-A-F05 | Реестровая индексированная страница показывает 32778, 31.03.2026, framework IVA H1 и ООО «ХАЙТЭК». | S04; **indexed primary copy**, не live registry contents. web.open: TimeoutError; TinyFish: timeout. Технические вложения неизвестны. |
| W2-A-F06 | `pytpu-15.0.24.tar.gz` — открытый исторический Python-source artifact, SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`. Actual archive не содержит LICENSE/COPYING/EULA/NOTICE или native `.so/.dll/.deb/.rpm/.whl` членов. | S06; повторная read-only tar/member/metadata inspection, `INSPECT_SAVED.py`. Не package install/import. |
| W2-A-F07 | Для этого pytpu: `python_requires='>=3.6'`; основной `install_requires=['numpy']`; optional RAW test dependency `tpu-tlm-is~=0.3.0.1`. Native loader содержит `/usr/lib/libtpu.2.so` и ленивую `_bind()`. | S06, `setup.py:25–47`, `_bindings.py:28–51`. Source inspection. Это не доказательство modern ABI или CPU-only compiler. |
| W2-A-F08 | `iva_applications-11.0.1.tar.gz` SHA256 `f04be1de75b8a7b22bd835c424fb61cd27f3e179356b7b4edc13f03f470f6b68` реально содержит LICENSE с copyright2020 IVA Technologies и MIT-условиями, хотя PKG-INFO указывает UNKNOWN. | S07; actual archive LICENSE прочитан. Условия разрешают использование/изменение/распространение именно этого Software с сохранением copyright/permission notice. Не лицензируют compiler, веса или image. |
| W2-A-F09 | `iva-tpu-11.2.6.tar.gz` SHA256 `885cb9ef75a87fb83dcf988d8e8664477a4bccca5f058feaede2130dc94a63ff` также не содержит названных лицензионных/native файлов. | S08; actual archive inspection. Отсутствие файла не устанавливает запрет; нужен grant поставщика/автора. |
| W2-A-F10 | Сторонний pinned repo указывает три отдельных Python environments; TPU env требует уже существующие `libtpu / tpu-dkms / pytpu / tpu_framework / mlperf`. Его requirements включает TF2.14.1 и NumPy1.26.4, но не восстанавливает названные vendor поставки. | S09, requirements.txt и RUN_SCENARIO.txt, раздел HOSTS AND ENVIRONMENTS. Static read, не validation. |
| W2-A-F11 | Public native-free import старых bindings не означает native-free metadata/runtime операции: `Device`/`Program` пути обращаются к `_LIB_TPU_BINDER.libtpu`. Ни это, ни архитектурное разделение quantize/compile/run не решает зависимости импортов **неполученного** `tpu_framework`. | S06 `_bindings.py:195,244`; S10. Вывод ограничен source. CPU-only compile остаётся точным экспериментальным вопросом. |
| W2-A-F12 | Названия modern framework/runtime подтверждены условиями опубликованного benchmark2026, но exact METADATA, Requires-Dist, native ABI pairing и права поставки не появились в новом поиске. | S11 (reuse W1), S01–S04 + negative searches. Не новые измерения и не установленная среда команды. |

## Нормализованная component/version/access/license matrix

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

## Попытка опровержения и отрицательные результаты

1. **Гипотеза: существует не замеченный public executable bundle.** Новый live `/docs`/`sol`/`tech`/`press` navigation audit и HTML-format `/sol` не дали SDK URL; обнаруженные explicit download URLs перечислены в F04. Поиск exact modern versions, exact framework filename/name, release/install/license дал преимущественно одноимённые .NET/linqapp/Google TPU продукты. Их не принимали за LinQ. Не угадывали имена закрытых wheel/архивов и не пытались обходить gate.
2. **Гипотеза: registry раскрывает свежую установочную документацию/лицензию.** Нашли индексированную primary table, но live fetch обоими каналами timeout. Ни registry details, ни attachments, ни license не получены. Не называем их отсутствующими. S04 — отдельный точный путь продолжения.
3. **Гипотеза: guide2025 точно задаёт current dependency set.** Нет wheel METADATA ни release note mapping; сторонний repo требует внешние vendor компоненты. Совместимость не доказана, но и несовместимость не доказана. Число `-03` в документе не wheel semver.
4. **Гипотеза: import без native library доказывает CPU-only compile.** Source pytpu специально ленивый; это делает import слабым свидетельством. Неполученный compiler может иметь иные native/license dependencies. Отрицательный вывод о CPU compile также не сделан.
5. **Гипотеза: UNKNOWN означает нет разрешающей лицензии.** Опровергнута для actual `iva_applications11.0.1` по вложенному MIT LICENSE. Для bindings такой файл не найден; нельзя переносить MIT от соседнего проекта.

Не повторяли W1 package-name404 и maintainer graph: они уже сохранены. Новый поиск нацелен на текущий release и реальные links. Единственная исполненная программа W2-A — наш archive reader над сохранёнными tar.gz. Это не SDK/import/compile/device test.

## Минимальное дерево экспериментов и уникальный владелец

Владелец этой границы для команды: **один инженер окружения/поставки**. Он выдаёт общий паспорт окружения/manifest остальным четырём, а не просит каждого повторять inventory. Model golden specification и numerical parity принадлежат модельной ветке; device execution proof — runtime/observability ветке.

| Эксперимент | Доступ/точные prerequisites | Минимальный success и развилка | Чего success не доказывает |
|---|---|---|---|
| W2-A-E01: delivery closure | Сейчас доступна только inspection открытых artifacts. Для полной проверки нужен actual wheelhouse/image + vendor install instructions и совместимые runtime-target сведения. | SHA256 каждого файла или image digest; wheel METADATA/WHEEL/entry_points/licenses; `Requires-Python/Requires-Dist`; версии `.so`/driver/firmware; все зависимости доступны в разрешённом контуре. Если выдача API-only, локальную установку не считать основным путём. | Что license позволяет передать весь image пяти людям; что ABI работает; что устройство исполняет граф. |
| W2-A-E02: install + import в одном release | Нужен SDK и подтверждённая vendor-supported host OS/ISA/Python; LinQ для этой проверки не предполагается. | Clean venv/container, установка из exact поставки, `pip check`, `import tpu_framework` exit0. Missing native `.so`/license/dependency локализовать до файла/операции, не менять случайно TF/Python. | CPU-only compile; supported ops; device availability. |
| W2-A-E03: decisive CPU-only compile | Нужны E01/E02 и один **matching-release** compiler example с исходной моделью, compile config, calibration inputs при необходимости. Устройство на compiler host отсутствует/не предоставлено; topology фиксируется. | Exact documented call завершился0, создан непустой `.tpu`, hash/target/log записаны. Это опровергает требование локальной платы именно для данной версии/target. При ошибке native runtime различить library dependency и необходимость physical device: установка `.so` без устройства может быть отдельным разрешённым повтором. При license server error — отдельная зависимость. | Runtime compatibility, корректность tensors, performance, inference на LinQ. Успех на одном target не универсальный cross-compile grant. |
| W2-A-E04: handoff `.tpu` runtime-владельцу | Нужен LinQ и совпадающий runtime/target либо документированная compatibility; общий model manifest/golden inputs. | Runtime-владелец принимает hash/config и выполняет load/inference/parity с evidence устройства. Результат возвращается в общий manifest. | Quality full dataset/production video budget. Этот тест здесь не дублируется. |

**Known-good vendor binary полезен, но не логически обязателен.** Если поставщик даёт только compiler+custom example, E03 может начинаться с этого matching example, а E04 — с его результата. Нужны воспроизводимый CPU reference/golden tensors и target/device evidence. Если выдаётся только remote compiler job, можно проверить compilation без локального устройства, но нельзя назвать это CPU-only vendor compilation: удалённый job может использовать недоступные нам native services/device. TLM — дополнительный checkpoint при фактической поставке, не gate всего маршрута.

### Командный каркас будущей установки — только план

После E01 переменные должны содержать **реально выданные** пути; этот блок не исполнялся. `VENDOR_LOCKFILE` и `VENDOR_CPU_COMPILE_EXAMPLE` — placeholders для supplied artifacts, не придуманные имена LinQ файлов. Если поставщик выдаёт image/service, следовать его контракту вместо этого venv route.

```sh
python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --no-index --find-links "$WHEELHOUSE" -r "$VENDOR_LOCKFILE"
"$VENV/bin/python" -m pip check
"$VENV/bin/python" -c 'import tpu_framework'
# Только после проверки matching example/аргументов по полученной документации:
"$VENV/bin/python" "$VENDOR_CPU_COMPILE_EXAMPLE"
```

Compile example должен уже содержать vendor-approved inputs/config либо получить exact аргументы из поставки. Каркас не заявляет наличие такого скрипта сегодня и не заменяет отсутствующий API call. До запуска сохранить host manifest, отсутствие/невыдачу device, env и dependency lock; после — exit codes, полный stderr/stdout, wall time, peak RAM, `.tpu` SHA256/target. Длительность не известна; таймбокс выбирает команда, не выдаём плановые минуты за измерение.

## Точные оставшиеся unknown и путь разрешения

- **Access:** фактический результат регистрации/верификации отдельно от доступного download list; online mode, device SKU, compiler location и право custom-model update — ответ постановщика/actual account observation.
- **Delivery:** matching framework wheel/image/lockfile; native `.so`, driver, firmware, Python and target pairing — прочитать выданную поставку. Если карточка registry доступна пользователю, проверить её документационные ссылки, не пересылать credentials.
- **Rights:** EULA/grant конкретной поставки: запуск пяти участников; clone/share image; изменение examples; публикация собственных `.tpu`; права checkpoint/data upload и retention — текст download conditions/организатор. Неизвестность не равна установленному запрету на запуск.
- **CPU compile:** E03 отдельно отвечает «нужна ли плата» и «нужны ли native библиотеки/лицензионный сервис». Нельзя сливать эти вопросы.

## Источники и локаторы

Все новые access — 23.10.2026, интервал указан в начале; полные tool-return snapshots — `W2_A/`. У сайтов без published_date дата не выведена из crawl time.

| ID | Прямая ссылка / автор / дата | Прочитанный локатор / файл / тип |
|---|---|---|
| W2-A-S01 | https://lin-q.ru/docs — LinQ/ООО «ХайТэк», дата не указана | TinyFish text+all links+metadata; `NAVIGATION_SNAPSHOT.JSON`, первый result; live. web.open отдельно недоступен. |
| W2-A-S02 | https://lin-q.ru/sol — LinQ/ООО «ХайТэк», дата не указана | Software/download links; `NAVIGATION_SNAPSHOT.JSON` второй result; `SOL_HTML_SNAPSHOT.JSON`; live. |
| W2-A-S03 | https://lin-q.ru/press ; https://lin-q.ru/hr ; https://lin-q.ru/tech — тот же автор, дата не указана | `PRESS_HR_SNAPSHOT.JSON`, `NAVIGATION_SNAPSHOT.JSON`; links/extracted content. Не cloud API specification. |
| W2-A-S04 | https://reestr.digital.gov.ru/reestr/?EX_PAGE_N=35&EX_PAGE_S=100&PAGE_N=47&PAGE_S=40 — Минцифры, строка регистрации31.03.2026 | Search exact title/32778: индексированная таблица; `REGISTRY_SEARCH.TXT`; failed live methods `REGISTRY_FETCH.JSON`. Полная карточка не получена. |
| W2-A-S05 | https://www.cnews.ru/news/line/2026-05-06_frejmvork_dlya_tenzornogo — сообщение представителей «ХайТэк», 06.05.2026 | Только discovery registry lead, не самостоятельное техническое подтверждение. `LICENSE_SEARCH.TXT`/`REGISTRY_SEARCH.TXT`. |
| W2-A-S06 | https://files.pythonhosted.org/packages/bd/9a/ee7cc0a40291dcb7ef399d30b80892909c3add5e3a0ebf1bc04a8c97f0ba/pytpu-15.0.24.tar.gz — IVA-Tech, upload2023-11-27 по W1 PyPI | Actual saved archive `_WORK/W1_13/PYTPU-15.0.24.TAR.GZ`; setup/PKG-INFO and `_bindings.py` locators F06/F07/F11. W2 read-only evidence `SAVED_ARCHIVE_INSPECTION.JSON`. |
| W2-A-S07 | https://files.pythonhosted.org/packages/93/ad/cd5000f6b458ef22fce4d58e0214ba3ebf8d49f6c6890c8c6d892adf0884/iva_applications-11.0.1.tar.gz — IVA Technologies, upload2021-10-13; LICENSE copyright2020 | Actual saved archive `_WORK/W1_13/IVA_APPLICATIONS-11.0.1.TAR.GZ`; LICENSE, setup, PKG-INFO. |
| W2-A-S08 | https://files.pythonhosted.org/packages/64/ee/0c5f2b71f8fc94771a638dc1300dd9a9c6e530701734ff405249111a3a26/iva-tpu-11.2.6.tar.gz — Maxim Moroz/IVA,2021 | Actual saved archive `_WORK/W1_13/IVA-TPU-11.2.6.TAR.GZ`; member/metadata inspection. |
| W2-A-S09 | https://github.com/sherstpasha/linq-cv-bench/tree/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140 — sherstpasha, commit2026-04-03; RUN_SCENARIO dated2026-03-25 | Saved `_WORK/W1_06/linq-cv-bench/requirements.txt`, RUN_SCENARIO.txt HOSTS AND ENVIRONMENTS, .gitignore; static read. Vendor relationship not established. |
| W2-A-S10 | https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf — ООО «ХайТэк»,2025 | Reused `_WORK/W1_03/Framework_manual_H1_extracted.txt`, §2 and import/compile/runtime separation; text only, no new PDF/visual QA. Detailed errata owned W2-B. |
| W2-A-S11 | https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf — LinQ,2026 | Reused W1-03/04 benchmark environment p4; current source link reconfirmed by /press. New PDF contents not fetched here. |

## Компактный handoff root

K001 остаётся открытым до actual download/access grant; public navigation boundary уточнена новым live evidence. K002 остаётся открытым до одного современного bundle/manifest; ни obsolete guide, ни CPU-only compile не заявляем. K019 частично закрыт для historical MIT helper по actual archive, а compiler/runtime/weights/image rights открыты. K020 — E01–E03 принадлежат одному environment владельцу, E04 передаётся runtime владельцу с единым model manifest; vendor binary smoke и TLM полезны при наличии, но не mandatory для любого возможного старта.

Новая полезная primary зацепка: registry32778/31.03.2026, но пока indexed-copy-only; продолжение — live details/doc links при доступности. Дочерних агентов не создавал, общие файлы не менял.
