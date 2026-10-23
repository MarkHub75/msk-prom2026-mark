# W1-13 — публичная экосистема, происхождение и поставка LinQ SDK

Проверка: 2026-10-23; точные timestamps сетевых проверок сохранены в HTTP_CHECKS.JSON (01:33:29 UTC) и EXTRA_PYPI_CHECKS.JSON (01:35:53 UTC). Исследовательская ветка первой волны; сеть действительно проверена через web search/open, GitHub REST API, PyPI JSON и скачивание небольших исходных архивов. Доступа к LinQ, учётной записи производителя, приватному registry и актуальному полному SDK не было. Код источников не устанавливался и не исполнялся; inference/compile/benchmark не проводились.

## Главный вопрос и ответ

**Можно ли восстановить воспроизводимый старт только из общедоступных packages/repos?** Пока нет: публично можно получить исторические Python bindings и вспомогательную обработку моделей, сторонние сценарии 2026 и исторический benchmark harness. Полная цепочка LinQ 2026 требует поставки производителя: согласованных wheel/compiler/runtime/driver, подходящих .tpu и документации именно этой версии. Публичного контейнера или актуального публичного package index с этими компонентами не найдено. Это результат ограниченного поиска, не доказательство их отсутствия.

Новая важная находка — не только `pytpu`, но вся атрибутированная группа из **четырёх PyPI-проектов** пользователя `IvaTechnologies`: `pytpu`, `iva-applications`, `iva-tpu`, `iva-classification-demo`. Из них `iva-applications==11.0.1` содержит полноценные исходники host pre/postprocessing/calibration с MIT LICENSE, но не актуальный SDK. Другая полезная находка — исторический GUI `sttell/IVA_compiler_runner` (2022), который автоматизирует внешний compiler и SSH-выполнение `run_tpu`; встроенного компилятора там нет.

Практическое следствие: не строить окружение хакатона командой `pip install pytpu mlperf`. Первая команда выдаёт последний публичный bindings 2023 года; пакет с именем `mlperf` в PyPI относится к другому проекту. Нужен environment manifest от постановщика.

## Как читать факты

У каждого факта указаны **тип доказательства** и **статус фактически выполненной проверки** независимо. `source_code` — прочитан код; `primary_documentation` — опубликованная техническая документация/метаданные; `vendor_statement` — заявление поставщика; `local_observation` — собственный сетевой/файловый результат; `inference` — вывод из этих оснований; `unknown` — не установлено. «Прочитан» не означает «запущен» или «совместим с LinQ 2026».

## Карта доступности

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

## Подробные факты

**W1-13-F01 — OEM и контролируемая загрузка.** Тип `vendor_statement`; проверка: web прочитан `/sol`, строки273–293. Поставщик описывает преобразование графов в инструкции LinQ H, Python3.8 API/CLI и ПО под историческим названием «Фреймворк для работы тензорного процессора IVA H1…» как часть OEM на LinQ H. Раздел загрузки требует регистрации и верификации. Это подтверждает связь продуктов и модель получения, но не текущую версию wheel, конкретную лицензию SDK или API2026. [S01]

**W1-13-F02 — подтверждённый maintainer graph.** Тип `primary_documentation`; проверка: страница PyPI maintainer прочитана. `IvaTechnologies`, display name `IVA Technologies`, joined2020-04-15, имеет четыре публичных проекта, перечисленных в карте. Это атрибуция аккаунта/метаданных и исторического семейства, не доказательство юридической тождественности всех нынешних брендов и не поддержка текущего ABI. [S02]

**W1-13-F03 — `pytpu15.0.24` доступен, но историчен.** Тип `primary_documentation`; проверка: JSON получен HTTP200, sdist независимо скачан и SHA256 проверен. Upload `2023-11-27T09:41:37.939987Z`, 19,201 bytes, SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`. Author `IVA-Tech`, email `info@iva-tech.ru`, Python `>=3.6`, homepage старого SDK. В JSON это latest `15.0.24`, а не Runtime16.18.6 из презентации2026. [S03,S04]

**W1-13-F04 — `pytpu` не поставляет runtime/compiler.** Тип `source_code`; проверка: sdist распакован/прочитан. `setup.py` install_requires только `numpy`; extras test содержит `tpu-tlm-is~=0.3.0.1`. `_bindings.py` lazy-load `/usr/lib/libtpu.2.so`. Отсутствие install dependency на native runtime не означает его ненужность: он ожидается на уровне Linux/system installation. Сам native binary в архиве отсутствует. [S04]

**W1-13-F05 — публичный sdist не содержит объявленные CLI targets.** Тип `source_code` + `local_observation`; проверка: полный список членов скачанного tar, без установки. `setup.py` объявляет `run_get_fps = pytpu.scripts.run_get_fps:main` и `pyrun_tpu = pytpu.scripts.pyrun_tpu_cli:main`, но ни одного `pytpu/scripts` в sdist нет. Ожидается, что такие entrypoints из этого артефакта не смогут загрузить target module без внешнего добавления; сам CLI не запускался. Это дефект/неполнота конкретного публичного архива, не доказанная ошибка vendor package2026. [S04]

**W1-13-F06 — лицензию bindings нельзя восстановить по публичности.** Тип `source_code`; проверка: manifest/metadata прочитаны. У `pytpu15.0.24` `License: UNKNOWN`, JSON license пуст, LICENSE-файла в sdist нет. То же неизвестное поле у `iva-tpu11.2.6`; лицензия всего SDK не установлена. Не присваивать им MIT по аналогии с соседним пакетом. [S04,S06]

**W1-13-F07 — README и код `pytpu` отражают разные API-поколения.** Тип `source_code`; проверка: README/setup/package прочитаны. README использует `from iva_tpu import TPUDevice, TPUProgram, TPUInference`, тогда как архив имеет пакет `pytpu` с новым `Device` API (подробности у W1-09). Это не безопасный copy-paste quickstart. Комментарий `_bindings.py:321` содержит `https://jira.hi-tech.org/browse/TPU2-2010`, добавляя след происхождения, но сам issue недоступен. [S04]

**W1-13-F08 — `iva-tpu11.2.6` — loader, не binary distribution.** Тип `source_code`; проверка: sdist скачан, SHA256 проверен, `src/iva_tpu/__init__.py` прочитан. Код `importlib.util.spec_from_file_location("libtpu", "/usr/lib/libtpu.so")`, затем `module_from_spec` и `sys.modules["iva_tpu"] = libtpu`. Archive 2,238 bytes; SHA256 `885cb9ef75a87fb83dcf988d8e8664477a4bccca5f058feaede2130dc94a63ff`. Native extension не включён. Author `Maxim Moroz`, `m.moroz@iva-tech.ru`, тот же SDK homepage; numpy>=1.14/Python>=3.6. [S05,S06]

**W1-13-F09 — есть публичный helper model package с реальной лицензией.** Тип `source_code`; проверка: `iva_applications-11.0.1.tar.gz` скачан, SHA256 `f04be1de75b8a7b22bd835c424fb61cd27f3e179356b7b4edc13f03f470f6b68` проверен. Author `IVA Technologies`, `engineering@iva-tech.ru`; maintainers `a.zolotarev` и `IvaTechnologies`. В архиве LICENSE содержит стандартный MIT-текст, Copyright2020 IVA Technologies, хотя metadata license UNKNOWN. Лицензионный файл сильнее пустого/неполного классификатора; это относится к этому helper package, не автоматически к моделям, весам и всему SDK. [S07,S08]

**W1-13-F10 — helpers не равны Model Zoo/сертифицированной модели.** Тип `source_code`; проверка: tree/исходники просмотрены. В `iva-applications` есть `tiny_yolo2`, `tiny_yolo3`, `yolo2`, `yolo3`, `yolo4`, `ssd_mobilenet`, `rfdnet`, `resnet50`, `unet`, `bert_large`, `gpt2` и др.; распределение pre/post/calibration неодинаково. TinyYOLO3 package имеет host postprocess; нет supplied .tpu/.qm/weights, современного compiler или матрицы compatibility. Наличие имени GPT2/YOLO4 не доказывает, что текущий LinQ аппаратно поддерживает выбранную произвольную конфигурацию. Это полезный исторический первичный код для model_stack/данных. [S08]

**W1-13-F11 — helpers жёстко привязаны к старому окружению.** Тип `source_code`; проверка: setup/metadata прочитаны. Base deps включают `scipy==1.4.1`, `keras==2.2.4`, matplotlib/Pillow/scikit-build/opencv-python/scikit-image/pydrive/pandas/transformers/sentencepiece. Extras: `tensorflow==2.4.1`, `transformers==4.5.1`, `pytpu==13.0.6`. `utils/tpu_runner.py` импортирует `TPUDevice, TPUProgram, TPUProgramInfo, TPUInference` из `pytpu`; поэтому «latest helpers + latest bindings» не является доказанно согласованным стеком. В современное Python3.11 environment механически устанавливать этот набор рискованно; реального resolver/install теста здесь нет. [S08]

**W1-13-F12 — classifier demo представляет исторический UI и host/TPU развилку.** Тип `source_code`; проверка: PyPI JSON/sdist получены, SHA256 `aeaf3436a861da50af92cc1738a6356b7d533de0dbe99609655d9d6082c18c78` проверен. `iva-classification-demo1.1.0`, author `Alexeev Eugene`, `e.alekseev@iva-tech.ru`; depends TF1.15.0/Keras2.2.4/PyQt5/iva-applications/iva-tpu. `class_computer.py` выбирает TFRunnerDict при local flag и TPURunner иначе. Это исходный пример возможной границы UI/host execution, не текущий remote-access protocol LinQ и не пример контроля промышленной безопасности. [S09]

**W1-13-F13 — сторонний repo2026 не является SDK.** Тип `source_code`; проверка: текущая GitHub page/API прочитаны, локальный clone соседней ветки исследован на commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`, date `2026-04-03T12:44:54+07:00`, author `sherstpasha`. GitHub API license null, releases=[], tags=[]; в tracked tree LICENSE не найден. `requirements.txt`: numpy1.26.4, onnx~=1.16.0, onnxruntime~=1.18.0, tensorflow2.14.1, setuptools<81, torch/torchvision и др.; SDK/ultralytics не включены. `RUN_SCENARIO.txt` явно ожидает отдельное TPU-env с libtpu/tpu-dkms/pytpu/tpu_framework/mlperf. Внешний `mlperf-16.16.12-Source/build/mlperf` и vendor .tpu лежат в авторских `/home/smallpc_user/...`, не в repo. [S10,S11]

**W1-13-F14 — воспроизводимость repo ограничена артефактами и дефектом.** Тип `source_code`; проверка: tracked files/строки кода прочитаны; запуск не проводился. В `.gitignore` исключены experiments*, *.json, *.onnx, *.pt, *.weights, data/artifacts/third_party. Это объясняет, почему ссылки на results_summary.json из сценария не предоставляют сами результаты. В pinned `scr/detection/run_yolov8_tpu.py:206` аргумент `args.output_tensอร์_name` отличается от parser `output_tensor_name`; это ожидаемый AttributeError до device open при достижении строки. Нельзя объявлять repo runnable/измеренным по наличию сценария. Подробная ветка модели — W1-08. [S11]

**W1-13-F15 — исторический GUI подтверждает SSH-сценарий, но не современную выдачу.** Тип `source_code`; проверка: найден через GitHub API `q=iva+tpu`, клонирован `sttell/IVA_compiler_runner`, commit `543ab4a0e53b4efb851af5c592f8089b5685ec70`, `2022-04-03T13:27:54+03:00`, author Илья Биро. README заявляет Ubuntu20.04, Boost>=1.71, Qt5/CMake/OpenSSL/OpenGL/LibSSH/Python3, version1.0; API releases/tags пусты, license null, LICENSE не найден. `lib/compiler_core/.../compiler_runner/runner.sh` требует внешний compiler directory, делает `make`, запускает `./hpm_scheduler -system=ivatpu ...`; `remote_runner/remoterunner.cpp:166` собирает команду `run_tpu -t -r -p ...` и передаёт файлы SSH/SFTP. Нет supplied hpm_scheduler source/native SDK. Это независимый исторический авторский слой автоматизации, связь автора с vendor не установлена. [S12,S13]

**W1-13-F16 — официальный исторический manifest раскрывает закрытый участок supply.** Тип `primary_documentation`; проверка: GitHub MLCommons API/RAW прочитаны, поддеревья/скрипты сохранены, измерения не анализировались (это W1-11). `closed/IVATech/README.md` v0.7 перечисляет In-house software: `AU200_freq250_axi512.bit`, `iva-tpu-dkms_4.1.4-1ubuntu1_all.deb`, `iva_tpu_4.1.4_amd64.deb`, `libtpu_7.1.17_amd64.deb`, `dnn_quant-3.3.3`, `protobuf_evert-3.3.1`, `tpu_quantize-3.2.1`, `tpu_commands/tpu_compiler/tpu_compiler_frontend/tpu_compiler_tools/tpu_datatypes/tpu_tlm-14.0.0`, `tpu_tlm_is-14.0.1`, `iva_applications-6.4.1`, с колонкой SHA HASH. Длины 40 hex; исходник не уточняет алгоритм, потому здесь не переименовываем их в SHA256. Все literal hashes сохранены в KEY_SOURCE_LOCATORS.TXT. Это manifest исторической FPGA submission, не версии нынешнего LinQ. [S14]

**W1-13-F17 — старый воспроизводимый рецепт упирается в непоставленные пакеты.** Тип `source_code`; проверка: MLPerf v0.7 resnet/mobilenet README, requirements, quantize.sh, compile.sh прочитаны. Public refs: `mlperf/inference` checkout `r0.7`, clipp, spdlog, исходные models Zenodo. `quantize/requirements.txt` требует `tensorflow==1.15.0`, `tpu-quantize==3.2.1`, `tpu_compiler_frontend==14.0.0`, `iva-applications==6.4.1`, click7.1.2/Pillow7.2.0; `compile.sh` вызывает `.venv/bin/tcf compile --optimize quantized_data/to_compile resnet50.tpu`. Ссылки download для in-house wheels/debs в этих инструкциях нет. Явный private registry hostname/token не найден. Правильная формулировка — «требуются отдельно поставляемые исторические vendor packages», а не установленный URL приватного index. [S15,S16]

**W1-13-F18 — отрицательные package lookup имеют узкий смысл.** Тип `local_observation`; проверка: прямые HTTPS GET JSON2026-10-23 дали404 для normalised names `tpu-framework`, `dnn-quant`, `onnx-direct`, `tpu-tlm-is`, `tpu-compiler`, `tpu-compiler-frontend`, `tpu-compiler-tools`, `tpu-datatypes`, `tpu-commands`, `tpu-tlm`, `tpu-quantize`, `protobuf-evert`. Это опровергает простое предположение «названия из guide можно сейчас взять с PyPI», но не доказывает, что нет другой distribution name, bundles, private wheelhouse, mirror или выдачи через ЛК. [S17]

**W1-13-F19 — `pip install mlperf` не восстанавливает vendor binary.** Тип `primary_documentation` + `inference`; проверка: PyPI JSON200. PyPI mlperf latest0.1.0 (2025), author_email `Arjun <arjun@gateoverflow.com>`, Repository `https://github.com/gateoverflow/mlc`, dependency requests. Нет атрибуции IVA/LinQ; название совпадает с индустриальным термином. Не подменять им C++ binary из стороннего repo. [S18]

**W1-13-F20 — публичный current release channel не установлен.** Тип `unknown` с подтверждённой границей поиска; проверка: поисковые запросы и GitHub/HF API выполнены. У lin-q.ru/sol нет открытой ссылки на GitHub/registry SDK в прочитанном содержимом; public software gate есть. GitHub exact-name searches и HF `search=iva_tpu` не дали актуального атрибутированного SDK/model repo; HF `search=linq` возвращает множество одноимённых embeddings/usernames. Ни один из них без связи с lin-q.ru/IVA не принят за LinQ Model Zoo. Контейнер registry/digest и release notes Framework2026.8.43 не установлены. [S01,S17,S19]

## Противоречия и важные несовпадения версий

1. `/sol`: API Python3.8; официальный guide2025: Python3.11 и пример `pip install tpu_framework-py3-none-any.whl`; PyPI binding: >=3.6; сторонний repo: venv311/TF2.14.1. Это разные документы/артефакты, а не единая совместимая матрица. Ни версия wheel guide, ни его полный dependency manifest публичным именем не заданы. Не исправлять документированный filename на угаданный номер версии. [S01,S20,S03,S11]
2. Публичный PyPI latest bindings2023 не равен runtime/framework из vendor slides2026 (16.18.6 / 2026.8.43, данные W1-03). Между числами нельзя арифметически вывести ABI support. [S03; handoff W1-03]
3. README `iva_tpu/TPUDevice` и действительный package `pytpu/Device` расходятся; `iva-applications11.0.1` ожидает `pytpu13.0.6`. Нельзя чинить импорт простым переименованием пакета без проверки API/native runtime. [S04,S08]
4. LICENSE UNKNOWN в metadata не всегда означает отсутствие лицензии: у iva-applications есть MIT LICENSE. Обратное тоже верно — MIT helpers не выдаёт MIT-лицензию proprietary compiler. [S04,S08]
5. Repo2026 полезен для изучения пайплайна, но не содержит все binary/model assets и имеет независимый source defect. Наличие build/run сценариев не является свидетельством выполненного TPU-run. [S11]

## Источники и ограничения

Все online access — 2026-10-23; точные timestamps batch-проверок даны в HTTP_CHECKS.JSON и EXTRA_PYPI_CHECKS.JSON. Сетевые snapshots/архивы сохраняются в `_WORK/W1_13`; исходные upstream имена внутри архивов/clone сохранены, собственные auxiliary названы uppercase.

| ID | URL / title | Автор, document date | Locator / что прочитано | Ограничения |
|---|---|---|---|---|
| W1-13-S01 | https://lin-q.ru/sol — «Модули ускорения LinQ» | ООО «ХайТэк», дата страницы не указана | Web text273–293, software/OEM/download | Vendor statement; CLI TLS EOF, web прочитал |
| W1-13-S02 | https://pypi.org/user/IvaTechnologies/ — Profile | PyPI/IvaTechnologies, dynamic | строки33–40, 4 projects | Не подтверждает current support/legal entity |
| W1-13-S03 | https://pypi.org/pypi/pytpu/json ; https://pypi.org/project/pytpu/ | PyPI metadata/IVA-Tech, last upload2023-11-27 | version/releases/URLs/hashes/maintainer | JSON author fields self-declared; native SDK нет |
| W1-13-S04 | https://files.pythonhosted.org/packages/bd/9a/ee7cc0a40291dcb7ef399d30b80892909c3add5e3a0ebf1bc04a8c97f0ba/pytpu-15.0.24.tar.gz | IVA-Tech2023 | setup.py, PKG-INFO, README, _bindings.py, archive tree | Чтение, не execution |
| W1-13-S05 | https://pypi.org/pypi/iva-tpu/json ; https://pypi.org/project/iva-tpu/11.2.6/ | Maxim Moroz/IVA,2021-08-31 | version/author/release files | Старое семейство |
| W1-13-S06 | https://files.pythonhosted.org/packages/64/ee/0c5f2b71f8fc94771a638dc1300dd9a9c6e530701734ff405249111a3a26/iva-tpu-11.2.6.tar.gz | Maxim Moroz,2021 | setup.py, src/iva_tpu/__init__.py | Native libtpu не вложен |
| W1-13-S07 | https://pypi.org/pypi/iva-applications/json ; https://pypi.org/project/iva-applications/11.0.1/ | IVA Technologies,2021-10-13 | metadata/maintainers/dependencies | Package metadata incomplete license |
| W1-13-S08 | https://files.pythonhosted.org/packages/93/ad/cd5000f6b458ef22fce4d58e0214ba3ebf8d49f6c6890c8c6d892adf0884/iva_applications-11.0.1.tar.gz | IVA Technologies,2021; LICENSE2020 | setup.py, LICENSE, src tree, utils/tpu_runner.py | Helpers only; contemporary compiler capability не следует |
| W1-13-S09 | https://pypi.org/pypi/iva-classification-demo/json ; https://pypi.org/project/iva-classification-demo/1.1.0/ | Alexeev Eugene,2020-06-27 | metadata + sdist class_computer.py | Legacy UI, не актуальный quickstart |
| W1-13-S10 | https://api.github.com/repos/sherstpasha/linq-cv-bench ; /releases ; /tags | sherstpasha, repo created2026-02-25 | metadata/license/releases/tags | License null, атрибуция vendor не установлена |
| W1-13-S11 | https://github.com/sherstpasha/linq-cv-bench/tree/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140 | sherstpasha,2026-04-03 | requirements.txt, RUN_SCENARIO.txt, .gitignore, scr build/run files | Только static inspection, чужой author environment |
| W1-13-S12 | https://github.com/sttell/IVA_compiler_runner/tree/543ab4a0e53b4efb851af5c592f8089b5685ec70 | sttell/Илья Биро,2022-04-03 | README, runner.sh, remote_runner code | Исторический GUI; vendor relationship unknown |
| W1-13-S13 | https://api.github.com/repos/sttell/IVA_compiler_runner ; /releases ; /tags | GitHub metadata | license null, empty release/tag lists | README version1.0 не GitHub release |
| W1-13-S14 | https://raw.githubusercontent.com/mlcommons/inference_results_v0.7/master/closed/IVATech/README.md | IVATech submission / MLCommons, v0.7 2020 | In-house software table | Проверен current raw master; tree SHA сохранён в MLPERF tree JSON, не whole-repo pin |
| W1-13-S15 | https://github.com/mlcommons/inference_results_v0.7/tree/master/closed/IVATech/code/resnet/v1 | IVATech,2020 | README + quantize requirements/sh | Supply path only; benchmarks → W1-11 |
| W1-13-S16 | https://github.com/mlcommons/inference_results_v0.7/tree/master/open/IVATech/code/mobilenet/v1 | IVATech,2020 | README + quantize requirements/sh | Аналогичная supply gap |
| W1-13-S17 | https://pypi.org/pypi/tpu-framework/json и 11 иных lookup | PyPI dynamic, проверка2026-10-23 | HTTP_CHECKS.JSON; EXTRA_PYPI_CHECKS.JSON |404 только для проверенных normalised names |
| W1-13-S18 | https://pypi.org/pypi/mlperf/json | gateoverflow/mlc,2025 | info/project_urls/deps | Чужой пакет; исходники проекта не исследовались |
| W1-13-S19 | https://huggingface.co/api/models?search=iva_tpu ; https://huggingface.co/api/models?search=linq | Hugging Face dynamic | [] для iva_tpu; список для linq | Поиск по именам, не exhaustive content search |
| W1-13-S20 | https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf | ООО «ХайТэк»,2025, RU.РМДВ.04.06.014-03 34 01 | Уже сохранённый W1-03/Framework_manual_H1_extracted.txt: §2, imports281–282 | В этой ветке прочитан сохранённый текст, не повторный PDF download |

## Где искали, ошибки и воспроизводимость поиска

- Web exact queries: `"LinQ" "tpu_framework" github`, `"pytpu" IVA`, `"dnn_quant" "iva"`, `"onnx_direct" TPU`, `"git.mmp.iva-tech.ru"`, `"tpu_framework"`, `"dnn_quant"`, `"IVA" "TPU" github SDK`, `"lin-q.ru" "github"`, `"LinQ" "registry"`, `"tpu_sw" github`, `"IVA" "inference_results" github`. Много .NET/Linq messaging/Coral/Intelligent Video Analytics совпадений отброшено.
- PyPI: сначала source-identified names, затем maintainer profile (нашёл ещё три проекта), затем все имена vendor manifest. JSON и небольшие sdists реально получены; никакие weights не клонировались.
- GitHub REST repository search `iva+tpu` дал `sttell/IVA_compiler_runner` (а также нерелевантный профиль); repo клонирован. Search `dnn_quant`, `tpu_framework` в описаниях возвращает посторонние проекты. Это repository search, не authenticated code search. Дополнительные поиски `IVA+MLPerf`, `linq+TPU`, `iva_tpu_sdk` API вернули403 rate limit exceeded; fallback web не принёс нового актуального SDK.
- Старые `git.mmp.iva-tech.ru` HTTP/HTTPS и `jira.hi-tech.org/browse/TPU2-2010` CLI: `getaddrinfo failed`. Web SDK URL: not accessible. Нельзя трактовать это как увиденный login gate или доказательство, что private GitLab существует сейчас.
- `lin-q.ru/sol`, /tech, /docs CLI: `SSL: UNEXPECTED_EOF_WHILE_READING`; web /sol читается, /docs в одной попытке недоступен. Это ограничение fetch transport; guide и доступность docs уже установлены W1-03.
- GitHub web paths MLCommons closed/open дали restricted URL; REST contents и raw endpoints успешно прочитаны. Не нужно считать закрытым сам публичный repository.
- Явных credentials, registry URLs или гарантированной открытой Docker image для LinQ в прочитанном коде/источниках не найдено; данные пользователей/аккаунты не создавались, сообщения vendor не отправлялись.

## Что запросить и проверить в первые часы

1. **Получить ровно тот environment, на котором должен идти inference:** ОС/архитектура/kernel/Python; versions `libtpu`, firmware/driver, `pytpu`, `tpu_framework`, compiler, quantizer и vendor `mlperf`. Запросить lockfile/constraints и checksum артефактов; проверить право пользователя видеть /dev/tpu*. Решение: воспроизвести готовый image или ставить packages самостоятельно.
2. **Уточнить механизм поставки:** URL ЛК/wheelhouse/private index/container registry, необходимые credentials/network/VPN, image digest и право на скачивание/перенос. В источниках эти адреса не установлены, не подставлять старый DNS SDK homepage как рабочий endpoint.
3. **Проверить состав wheel без запуска:** unzip/list METADATA/Requires-Dist/top-level modules/entrypoints/licenses; установить, входят ли dnn_quant и onnx_direct внутрь tpu_framework, и что требует отдельно native ABI. Сопоставить с pip freeze/dpkg -l от vendor. Public package name и import name могут различаться.
4. **Запросить совместимый минимальный пример:** исходная ONNX, input/preprocess, calibration subset/recipe, exact compiler flags, готовый .qm/.tpu, expected output и known-good run log. Без этого даже корректный импорт не проверяет hardware path.
5. **Проверить native integration до своей модели:** перечисление устройств, open, загрузка поставленного .tpu, inference одной известной картинки, tensors сравнить с expected output. Сохранить версии, hash .tpu, logs и evidence устройства. Запуск произвести отдельным экспериментом после доступа; здесь он не выполнен.
6. **После known-good примера переносить сторонний code:** зафиксировать commit, исправить unicode argument defect в собственной копии, установить согласованные зависимости, явно разделить source pipeline и внешние vendor programs. Не считать `requirements.txt` полным lockfile SDK.
7. **Право использования/публикации уточнить для каждого слоя:** licenses SDK/compiler/runtime отдельно, примеры отдельно, model code/weights/datasets отдельно. Из публичной MIT лицензии helpers не выводится право публиковать весь поставленный Docker image.

## Handoff

- **W1-03 / environment:** четыре публичных package traces не заменяют доступ2026; запросить полный delivery manifest и container digest. tpu_framework/dnn_quant/onnx_direct по проверенным PyPI именам404; distribution bundling неизвестен.
- **W1-06 compiler:** новый исторический GUI2022 требует внешний hpm_scheduler; не текущий compiler. Сильнее для provenance — MLPerf v0.7 manifest с dnn_quant3.3.3 и compiler14.0.0, но современных исходников compiler не найдено.
- **W1-07 calibration и W1-08 model_stack:** сохранён `SOURCE/iva_applications-11.0.1` с MIT LICENSE, host YOLO/SSD/pre/post/calibration. Можно читать как исторический код и источник правил, не как доказательство поддерживаемых моделей2026. Веса/готовые программы не входят.
- **W1-09 runtime:** подтверждены source provenance, старый iva_tpu loader libtpu.so, pytpu15.0.24 libtpu.2.so и отсутствующие CLI modules. Полный API здесь намеренно не дублирован.
- **W1-11 benchmark:** открыты historical closed/open IVATech trees; измерения и system records не разбирались, чтобы не дублировать вашу ветку.
- **Будущая W2:** установить происхождение современного tpu_framework wheel и native runtime по полученному artifact METADATA; найти actual vendor release channel вместо дополнительных общих поисков LinQ.

## Сохранённые материалы

`HTTP_CHECKS.JSON`, `EXTRA_PYPI_CHECKS.JSON`, snapshots `PYPI...TXT`, `IVA-APPLICATIONS_JSON.TXT`, `IVA-TPU_JSON.TXT`, `IVA-CLASSIFICATION-DEMO_JSON.TXT`, tar.gz с проверенными hashes; `SOURCE/` с распакованными upstream sdists; `PYTPU_15_0_24_ARCHIVE_MEMBERS.TXT`; `KEY_SOURCE_LOCATORS.TXT`; `IVA_COMPILER_RUNNER/` pinned clone; `MLPERF_V07/` supply README/scripts и `MLPERF_IVAT_CLOSED_TREE.JSON`, `MLPERF_IVAT_OPEN_TREE.JSON` с Git tree SHA. Общие итоговые файлы не менялись.
