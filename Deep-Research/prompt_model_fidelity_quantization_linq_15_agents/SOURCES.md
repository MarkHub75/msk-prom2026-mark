# Источники model_fidelity_quantization

Сборка сохранённых W1/W2: 2026-10-23, Europe/Moscow (начата 23:16 MSK). Нового получения источников сборщиком нет. Дата доступа в карточках — дата исследователя, не публикация и не установленный стек. Один URL/версия имеет один S-ID; разные локаторы и повторные чтения сохранены внутри карточки и не увеличивают независимость. Составные source cards сохраняют несколько связанных первичных файлов: их нельзя считать несколькими независимыми измерениями.

Типы: DOC/documentation; CODE/static source; VENDOR/author claim; PUB/published measurement; LOCAL/реальное локальное чтение; INFERENCE/наш вывод; UNKNOWN. У каждой F запись различает утверждение и actual checked scope. Отсутствующая дата publication/commit остаётся unknown, если она не указана в provenance ниже. Mutable docs/latest не pins среды.

<a id="S001"></a>
## S001 — Исходный полный кейс LinQ, ООО «ХайТэк»

[_WORK/INPUT/CASE_LINQ.pdf](_WORK/INPUT/CASE_LINQ.pdf). 20 страниц, 8 320 969 bytes; SHA256 `7dbece3cf414e2a09ff03c93e9e1ed87172d7724fb7edd5cd3a3ad565063689e`. Publication/public URL unknown. Доступ 2026-10-23. Локальный первичный растровый документ; hash проверен root. Locators с.4–5/7–9/12–13/19. Источник найден в соседнем исследовании и скопирован без изменения. Собственных новых рендеров сборщик не создавал. Поддерживает F001 и атрибутированные case факты.

<a id="S002"></a>
## S002 — Первичное визуальное чтение root всех 20 страниц кейса

[_WORK/CASE_NOTES.md](_WORK/CASE_NOTES.md), 2026-10-23. LOCAL observation текущего root: существующие соседние CASE_SHEET_1…5.png; с.5/7/13 прочитаны крупно. Это одна цепочка наблюдения; чтение заметок 15 исследователями не ещё 15 visual проверок. Provenance и оговорки полностью в заметках. Локаторы постраничного конспекта с.5/7/8/13/19; F001 и case-наблюдения веток.


Поддержанные нормализованные F (case chain, не independent repeats): [F012](RAW_FACTS.md#F012), [F078](RAW_FACTS.md#F078), [F142](RAW_FACTS.md#F142), [F152](RAW_FACTS.md#F152), [F196](RAW_FACTS.md#F196).

<a id="S003"></a>
## S003 — Дополнительное локальное визуальное чтение W2-07 четырёх страниц

[_WORK/W2_07.md](_WORK/W2_07.md), S06/F04; existing large PNG с.5/7/13/19 соседнего исследования, 2026-10-23. LOCAL observation, не новый PDF fetch/рендер и не device test. Та же первичная цепочка кейса S001; самостоятельное чтение этих страниц отличается от пересказа root.


Поддержанные нормализованные F (case chain, не independent repeats): [F249](RAW_FACTS.md#F249).

<a id="S004"></a>
## S004 — Состояние текущего исследовательского запуска

[_WORK/RUN_STATE.md](_WORK/RUN_STATE.md), [_WORK/W1_MANIFEST.json](_WORK/W1_MANIFEST.json), [_WORK/W2_MANIFEST.json](_WORK/W2_MANIFEST.json), весь журнал и completed wave manifests; 2026-10-23. LOCAL process evidence, publication N/A. Поддерживает F002/F003; не SDK/device evidence.

<a id="S005"></a>
## S005

Primary identity: https://github.com/pytorch/pytorch/blob/0fabc3ba44823f257e70ce397d989c8de5e362c1/docs/source/notes/randomness.rst

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F004](RAW_FACTS.md#F004)

Происхождение: `W1-01-S01`, [W1-01](_WORK/W1_01.md), строка 21.

PyTorch Contributors, Reproducibility, tag v2.9.0; release 2025-10-15 17:12:27Z; commit `0fabc3ba44823f257e70ce397d989c8de5e362c1`

[randomness.rst](https://github.com/pytorch/pytorch/blob/0fabc3ba44823f257e70ce397d989c8de5e362c1/docs/source/notes/randomness.rst), строки 6–20, разделы Controlling sources of randomness, CUDA convolution benchmarking, Avoiding nondeterministic algorithms, DataLoader (163+)

Первичная документация в исходном репозитории; raw прочитан. [Release](https://github.com/pytorch/pytorch/releases/tag/v2.9.0), tag SHA и время release проверены GitHub API

<a id="S006"></a>
## S006

Primary identity: https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F005](RAW_FACTS.md#F005)

Происхождение: `W1-01-S02`, [W1-01](_WORK/W1_01.md), строка 22.

PyTorch Tutorials, Saving and Loading Models; наблюдаемая шапка 2.14.0+cu130; дата публикации не установлена

[Документ](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html), Saving & Loading Model for Inference, строки веб-представления 331–375; General Checkpoint 394–423; Warmstarting 458–470

Первичная документация; открыта. Подвижная ссылка, версия здесь фиксирует прочитанный контекст

<a id="S007"></a>
## S007

Primary identity: https://github.com/onnx/onnx/blob/57b9c6a4f6eebb09ae1b34cfb632078518f72832/docs/OnnxBackendTest.md

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F006](RAW_FACTS.md#F006)

Происхождение: `W1-01-S03`, [W1-01](_WORK/W1_01.md), строка 23.

ONNX Contributors, ONNX Backend Test, v1.19.0; release 2025-08-26 21:48:02Z; commit `57b9c6a4f6eebb09ae1b34cfb632078518f72832`

[Документ](https://github.com/onnx/onnx/blob/57b9c6a4f6eebb09ae1b34cfb632078518f72832/docs/OnnxBackendTest.md), строки 9–24

Первичная документация, raw прочитан; [release](https://github.com/onnx/onnx/releases/tag/v1.19.0) и SHA проверены API

<a id="S008"></a>
## S008

Primary identity: https://github.com/onnx/onnx/blob/57b9c6a4f6eebb09ae1b34cfb632078518f72832/onnx/backend/test/runner/__init__.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F007](RAW_FACTS.md#F007), [F008](RAW_FACTS.md#F008)

Происхождение: `W1-01-S04`, [W1-01](_WORK/W1_01.md), строка 24.

ONNX Contributors, тот же commit/v1.19.0, backend runner

[runner/__init__.py](https://github.com/onnx/onnx/blob/57b9c6a4f6eebb09ae1b34cfb632078518f72832/onnx/backend/test/runner/__init__.py), `Runner.assert_similar_outputs`, строки 185–229; ветка получения expected outputs 427–447; чтение fixtures 468–489

Наблюдение по исходному коду, raw прочитан; код не исполнялся

<a id="S009"></a>
## S009

Primary identity: https://scikit-learn.org/stable/common_pitfalls.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F009](RAW_FACTS.md#F009)

Происхождение: `W1-01-S05`, [W1-01](_WORK/W1_01.md), строка 25.

scikit-learn developers, Common pitfalls; наблюдаемая версия документации 1.9.1; дата публикации не установлена

[Документ](https://scikit-learn.org/stable/common_pitfalls.html), §12.2 Data leakage, строки 120–141; §12.3.1 randomness, 219–224

Первичная документация; открыта

<a id="S010"></a>
## S010

Primary identity: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F010](RAW_FACTS.md#F010)

Происхождение: `W1-01-S06`, [W1-01](_WORK/W1_01.md), строка 26.

scikit-learn developers, GroupShuffleSplit; наблюдаемая версия 1.9.1; дата публикации не установлена

[Документ](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html), строки 638–670, Notes 816–817

Первичная документация; открыта

<a id="S011"></a>
## S011

Primary identity: https://onnx.ai/onnx/intro/concepts.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F011](RAW_FACTS.md#F011)

Происхождение: `W1-01-S07`, [W1-01](_WORK/W1_01.md), строка 27.

ONNX Contributors, ONNX Concepts; наблюдаемая версия 1.24.0; дата публикации не установлена

[Документ](https://onnx.ai/onnx/intro/concepts.html), Metadata, строки 1447–1483; Supported Types 1491–1498

Первичная документация; открыта

<a id="S012"></a>
## S012

Primary identity: https://docs.pytorch.org/docs/2.9/onnx.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F013](RAW_FACTS.md#F013), [F014](RAW_FACTS.md#F014)

Происхождение: `W1-02-S01`, [W1-02](_WORK/W1_02.md), строка 93.

- **[S012](SOURCES.md#S012)** PyTorch Foundation, [torch.onnx, documentation 2.9](https://docs.pytorch.org/docs/2.9/onnx.html). Страница Created 2025-06-10, Updated 2025-08-29; API torch.onnx.export, parameters и versionchanged. [F013](RAW_FACTS.md#F013)/F02. Контроль текущей страницы: [stable redirect](https://docs.pytorch.org/docs/stable/onnx.html) → 2.14, release date 2.14 не установлена.

<a id="S013"></a>
## S013

Primary identity: https://docs.pytorch.org/docs/2.9/generated/torch.jit.trace.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F015](RAW_FACTS.md#F015)

Происхождение: `W1-02-S02`, [W1-02](_WORK/W1_02.md), строка 94.

- **[S013](SOURCES.md#S013)** PyTorch Foundation, [torch.jit.trace, documentation 2.9](https://docs.pytorch.org/docs/2.9/generated/torch.jit.trace.html), Warning и check_inputs; дата публикации страницы не указана. [F015](RAW_FACTS.md#F015).

<a id="S014"></a>
## S014

Primary identity: https://docs.pytorch.org/tutorials/beginner/onnx/export_control_flow_model_to_onnx_tutorial.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F023](RAW_FACTS.md#F023)

Происхождение: `W1-02-S03`, [W1-02](_WORK/W1_02.md), строка 95.

- **[S014](SOURCES.md#S014)** PyTorch Tutorials, [Export a model with control flow to ONNX](https://docs.pytorch.org/tutorials/beginner/onnx/export_control_flow_model_to_onnx_tutorial.html), разделы Prerequisites, First Attempt, Suggested Patch; отображается tutorials 2.14.0+cu130, prerequisite torch>=2.8; дата публикации не установлена. [F023](RAW_FACTS.md#F023). Это авторский исполняемый tutorial, но нами не исполнен.

<a id="S015"></a>
## S015

Primary identity: https://github.com/pytorch/pytorch/blob/0fabc3ba44823f257e70ce397d989c8de5e362c1/torch/onnx/_internal/exporter/_verification.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F017](RAW_FACTS.md#F017)

Происхождение: `W1-02-S04`, [W1-02](_WORK/W1_02.md), строка 96.

- **[S015](SOURCES.md#S015)** PyTorch, [v2.9.0 _verification.py](https://github.com/pytorch/pytorch/blob/0fabc3ba44823f257e70ce397d989c8de5e362c1/torch/onnx/_internal/exporter/_verification.py#L149), функция verify_onnx_program, строки 149–185; _compare_tensors 137–145. [F017](RAW_FACTS.md#F017).

<a id="S016"></a>
## S016

Primary identity: https://github.com/pytorch/pytorch/blob/0fabc3ba44823f257e70ce397d989c8de5e362c1/torch/onnx/_internal/exporter/_core.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F017](RAW_FACTS.md#F017)

Происхождение: `W1-02-S05`, [W1-02](_WORK/W1_02.md), строка 97.

- **[S016](SOURCES.md#S016)** PyTorch, [v2.9.0 _core.py](https://github.com/pytorch/pytorch/blob/0fabc3ba44823f257e70ce397d989c8de5e362c1/torch/onnx/_internal/exporter/_core.py#L1592), export verification 1592–1659. [F017](RAW_FACTS.md#F017). Commit date 2025-10-09; [release v2.9.0](https://github.com/pytorch/pytorch/releases/tag/v2.9.0) published 2025-10-15T17:12:27Z, подтверждено API.

<a id="S017"></a>
## S017

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/utils/export/engine.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F016](RAW_FACTS.md#F016), [F206](RAW_FACTS.md#F206)

Происхождение: `W1-02-S06`, [W1-02](_WORK/W1_02.md), строка 98.

- **[S017](SOURCES.md#S017)** Ultralytics, [v8.3.230 utils/export/engine.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/utils/export/engine.py#L14), torch2onnx:14–49, особенно 37–48. [F016](RAW_FACTS.md#F016).

Происхождение: `W2-02-S03`, [W2-02](_WORK/W2_02.md), строка 19. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [utils/export/engine.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/utils/export/engine.py#L14)

`torch2onnx`14–49; reexport `utils/export/__init__.py`3–5

Raw200. Это helper ONNX, а не соседний Ultralytics TF export через `onnx2tf`.

<a id="S018"></a>
## S018

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/engine/exporter.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F016](RAW_FACTS.md#F016), [F018](RAW_FACTS.md#F018), [F021](RAW_FACTS.md#F021), [F022](RAW_FACTS.md#F022), [F050](RAW_FACTS.md#F050), [F206](RAW_FACTS.md#F206), [F241](RAW_FACTS.md#F241), [F242](RAW_FACTS.md#F242), [F245](RAW_FACTS.md#F245)

Происхождение: `W1-02-S07`, [W1-02](_WORK/W1_02.md), строка 99.

- **[S018](SOURCES.md#S018)** Ultralytics, [v8.3.230 engine/exporter.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/engine/exporter.py#L629), __call__:438–452, export_onnx:629–693, NMSModel.forward:1372–1448. [F018](RAW_FACTS.md#F018)/F09/F10. Requirements 631–633: onnx>=1.12.0,<=1.19.1, при simplify onnxslim>=0.1.71 и onnxruntime[-gpu]; это ограничения прочитанной версии, не предложенный полный lockfile.

Происхождение: `W1-04-S07`, [W1-04](_WORK/W1_04.md), строка 138. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S018](SOURCES.md#S018).** Ultralytics [engine/exporter.py NMSModel](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/engine/exporter.py#L1372), v8.3.230, preparation 465–470, NMSModel.forward 1372–1448; [F050](RAW_FACTS.md#F050). Общие exporter сведения — W1_02.md.

Происхождение: `W2-02-S02`, [W2-02](_WORK/W2_02.md), строка 18. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [exporter.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/engine/exporter.py)

438–481;629–691

Raw200. Подготовка и ONNX path, включая optional simplification/IR header cap.

Происхождение: `W2-06-S02`, [W2-06](_WORK/W2_06.md), строка 14. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [exporter.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/engine/exporter.py), [export/engine.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/utils/export/engine.py)

U; exporter131 accepted ONNX flags,398–400 RTDETR nms coercion,465–479 preparation,629–693 ONNX; engine14–48 torch2onnx. raw200, `u_exporter.py/u_exportengine.py`.

<a id="S019"></a>
## S019

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/modules/head.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F019](RAW_FACTS.md#F019), [F020](RAW_FACTS.md#F020), [F044](RAW_FACTS.md#F044), [F045](RAW_FACTS.md#F045), [F046](RAW_FACTS.md#F046), [F048](RAW_FACTS.md#F048), [F054](RAW_FACTS.md#F054), [F208](RAW_FACTS.md#F208)

Происхождение: `W1-02-S08`, [W1-02](_WORK/W1_02.md), строка 100.

- **[S019](SOURCES.md#S019)** Ultralytics, [v8.3.230 nn/modules/head.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/modules/head.py#L114), Detect.forward/_inference и Pose.forward/kpts_decode. [F019](RAW_FACTS.md#F019)/F08. [S017](SOURCES.md#S017), [S018](SOURCES.md#S018), [S019](SOURCES.md#S019) commit 389b87f8cb9dbf2f31be8b70a94a3e47e11693db, commit date 2025-11-21T19:17:12Z; [release v8.3.230](https://github.com/ultralytics/ultralytics/releases/tag/v8.3.230) published 2025-11-21T19:18:06Z, подтверждено API.

Происхождение: `W1-04-S02`, [W1-04](_WORK/W1_04.md), строка 133. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S019](SOURCES.md#S019).** Ultralytics [head.py v8.3.230](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/modules/head.py#L79), hash 389b87f8cb9dbf2f31be8b70a94a3e47e11693db. W1-02 API уже установил commit 2025-11-21 и release v8.3.230 2025-11-21; здесь заново прочитан raw. Detect/Pose/Segment/end2end/RTDETRDecoder; [F044](RAW_FACTS.md#F044), [F045](RAW_FACTS.md#F045), [F046](RAW_FACTS.md#F046), [F047](RAW_FACTS.md#F047), [F048](RAW_FACTS.md#F048),[F054](RAW_FACTS.md#F054).

Происхождение: `W2-02-S01`, [W2-02](_WORK/W2_02.md), строка 17. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [head.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/modules/head.py)

Detect 68–124,149–189; Pose319–384

Raw HTTP200, source reading. Не execution и не наличие этих head в ещё не выданных weights.

<a id="S020"></a>
## S020

Primary identity: https://onnx.ai/onnx/api/checker.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F024](RAW_FACTS.md#F024)

Происхождение: `W1-02-S09`, [W1-02](_WORK/W1_02.md), строка 101.

- **[S020](SOURCES.md#S020)** ONNX, [onnx.checker](https://onnx.ai/onnx/api/checker.html), API check_model, full_check/check_custom_domain. Веб-документация 1.24.0, дата публикации неизвестна. [F024](RAW_FACTS.md#F024).

<a id="S021"></a>
## S021

Primary identity: https://onnx.ai/onnx/operators/onnx__Resize.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F024](RAW_FACTS.md#F024), [F030](RAW_FACTS.md#F030), [F031](RAW_FACTS.md#F031)

Происхождение: `W1-02-S10`, [W1-02](_WORK/W1_02.md), строка 102.

- **[S021](SOURCES.md#S021)** ONNX, [Resize operator](https://onnx.ai/onnx/operators/onnx__Resize.html), версии Resize и attributes coordinate_transformation_mode/nearest_mode, пример _resize_downsample_sizes_linear_pytorch_half_pixel. Веб-документация 1.24.0; дата публикации неизвестна. [F024](RAW_FACTS.md#F024). Семантика выбранного opset требует отдельного чтения соответствующей секции, а не переноса самого нового schema в старый граф.

Происхождение: `W1-03-S06`, [W1-03](_WORK/W1_03.md), строка 28.

[Resize](https://onnx.ai/onnx/operators/onnx__Resize.html)

D. Схема13 §Attributes/Inputs, web3410–3490; схема10 для сравнения; у новых схем дополнительно появляются параметры, поэтому читать именно effective schema.

<a id="S022"></a>
## S022

Primary identity: https://github.com/onnx/onnx/blob/v1.19.1/onnx/checker.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F025](RAW_FACTS.md#F025)

Происхождение: `W1-03-S01`, [W1-03](_WORK/W1_03.md), строка 23.

[ONNX checker](https://github.com/onnx/onnx/blob/v1.19.1/onnx/checker.py#L121), [versioning](https://github.com/onnx/onnx/blob/v1.19.1/docs/Versioning.md#operator-versioning)

C/D. v1.19.1, commit `b751946c3d59a3c8358abcc0569b59e6ddb08cdd`; release опубликован 2025-10-10 02:06:42 UTC по [release API](https://api.github.com/repos/onnx/onnx/releases/tags/v1.19.1). `check_model` строки121–144; versioning §Operator versioning. Получен raw-код.

<a id="S023"></a>
## S023

Primary identity: https://onnx.ai/onnx/repo-docs/ShapeInference.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F026](RAW_FACTS.md#F026)

Происхождение: `W1-03-S02`, [W1-03](_WORK/W1_03.md), строка 24.

[Shape inference](https://onnx.ai/onnx/repo-docs/ShapeInference.html#limitations), [Python API](https://github.com/onnx/onnx/blob/v1.19.1/onnx/shape_inference.py#L26)

D/C. Живая документация §Limitations, строки1433–1438 веб-страницы; pinned код v1.19.1 `infer_shapes`, строки26–54.

<a id="S024"></a>
## S024

Primary identity: https://github.com/daquexian/onnx-simplifier/blob/v0.4.36/onnxsim/onnx_simplifier.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F027](RAW_FACTS.md#F027)

Происхождение: `W1-03-S03`, [W1-03](_WORK/W1_03.md), строка 25.

[onnx-simplifier API и CLI](https://github.com/daquexian/onnx-simplifier/blob/v0.4.36/onnxsim/onnx_simplifier.py#L100)

C. v0.4.36, tag commit `fbf1ca8e26ba29200f6572194391b148c0695254`, commit date 2024-03-04 06:54:35 UTC по [API](https://api.github.com/repos/daquexian/onnx-simplifier/commits/v0.4.36). Release endpoint вернул404: дата релиза не установлена. `simplify` строки100–136, вызов compare210–212, CLI274–280; raw открыт. Репозиторий API редиректит на onnxsim/onnxsim.

<a id="S025"></a>
## S025

Primary identity: https://github.com/daquexian/onnx-simplifier/blob/v0.4.36/onnxsim/model_checking.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F027](RAW_FACTS.md#F027), [F028](RAW_FACTS.md#F028)

Происхождение: `W1-03-S04`, [W1-03](_WORK/W1_03.md), строка 26.

[onnxsim model_checking.py](https://github.com/daquexian/onnx-simplifier/blob/v0.4.36/onnxsim/model_checking.py#L131)

C. Тот же tag/commit. Генерация `np.random.rand`124–129; CPU EP и отключение ORT optimizations142–150; `range(n_times)`, allclose, return True161–185.

<a id="S026"></a>
## S026

Primary identity: https://onnx.ai/onnx/operators/onnx__Softmax.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F029](RAW_FACTS.md#F029)

Происхождение: `W1-03-S05`, [W1-03](_WORK/W1_03.md), строка 27.

[Softmax](https://onnx.ai/onnx/operators/onnx__Softmax.html)

D. Схемы11 и13; §Summary/Attributes; web строки1428–1439 и1549–1566.

<a id="S027"></a>
## S027

Primary identity: https://onnx.ai/onnx/operators/onnx__Transpose.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F032](RAW_FACTS.md#F032)

Происхождение: `W1-03-S07`, [W1-03](_WORK/W1_03.md), строка 29.

[Transpose](https://onnx.ai/onnx/operators/onnx__Transpose.html)

D. Схема13, Summary/perm, web1646–1675.

<a id="S028"></a>
## S028

Primary identity: https://onnx.ai/onnx/operators/onnx__Reshape.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F032](RAW_FACTS.md#F032)

Происхождение: `W1-03-S08`, [W1-03](_WORK/W1_03.md), строка 30.

[Reshape](https://onnx.ai/onnx/operators/onnx__Reshape.html#reshape-14)

D. Схема14, Summary/allowzero; раздел отдельно прочитан из HTML по заголовку Reshape-14; отличать от схемы13 без allowzero.

<a id="S029"></a>
## S029

Primary identity: https://onnx.ai/onnx/operators/onnx__Gather.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F033](RAW_FACTS.md#F033)

Происхождение: `W1-03-S09`, [W1-03](_WORK/W1_03.md), строка 31.

[Gather](https://onnx.ai/onnx/operators/onnx__Gather.html)

D. Схема13, Summary/axis/indices, web1428–1438 и раздел Inputs.

<a id="S030"></a>
## S030

Primary identity: https://onnx.ai/onnx/operators/onnx__Slice.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F033](RAW_FACTS.md#F033)

Происхождение: `W1-03-S10`, [W1-03](_WORK/W1_03.md), строка 32.

[Slice](https://onnx.ai/onnx/operators/onnx__Slice.html)

D. Схема13, Summary/Inputs; web1428–1445, обработка отрицательных индексов/шага.

<a id="S031"></a>
## S031

Primary identity: https://onnx.ai/onnx/operators/onnx__Concat.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F033](RAW_FACTS.md#F033)

Происхождение: `W1-03-S11`, [W1-03](_WORK/W1_03.md), строка 33.

[Concat](https://onnx.ai/onnx/operators/onnx__Concat.html)

D. Схема13, Summary/axis, web1429–1436.

<a id="S032"></a>
## S032

Primary identity: https://onnx.ai/onnx/operators/onnx__Conv.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F034](RAW_FACTS.md#F034)

Происхождение: `W1-03-S12`, [W1-03](_WORK/W1_03.md), строка 34.

[Conv](https://onnx.ai/onnx/operators/onnx__Conv.html)

D. Схема11, Inputs/Attributes; N,C,spatial; weight M,C/group,spatial; SAME_UPPER/LOWER, group/dilations/pads.

<a id="S033"></a>
## S033

Primary identity: https://onnx.ai/onnx/operators/onnx__Sigmoid.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F035](RAW_FACTS.md#F035)

Происхождение: `W1-03-S13`, [W1-03](_WORK/W1_03.md), строка 35.

[Sigmoid](https://onnx.ai/onnx/operators/onnx__Sigmoid.html)

D. Схема13 Summary, web1429–1446.

<a id="S034"></a>
## S034

Primary identity: https://onnx.ai/onnx/operators/onnx__NonMaxSuppression.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F035](RAW_FACTS.md#F035)

Происхождение: `W1-03-S14`, [W1-03](_WORK/W1_03.md), строка 36.

[NonMaxSuppression](https://onnx.ai/onnx/operators/onnx__NonMaxSuppression.html)

D. Схема11 Summary/Inputs/Outputs, web1428–1478.

<a id="S035"></a>
## S035

Primary identity: https://onnxruntime.ai/docs/performance/model-optimizations/graph-optimizations.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F036](RAW_FACTS.md#F036)

Происхождение: `W1-03-S15`, [W1-03](_WORK/W1_03.md), строка 37.

[ORT graph optimizations](https://onnxruntime.ai/docs/performance/model-optimizations/graph-optimizations.html)

D. Живая документация, Basic/Extended/Layout, Online/Offline, Usage; web199–266. Дата/релиз страницы не указан.

<a id="S036"></a>
## S036

Primary identity: https://github.com/microsoft/onnxruntime/blob/v1.23.2/onnxruntime/core/optimizer/constant_folding.cc

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F036](RAW_FACTS.md#F036)

Происхождение: `W1-03-S16`, [W1-03](_WORK/W1_03.md), строка 38.

[ORT constant folding](https://github.com/microsoft/onnxruntime/blob/v1.23.2/onnxruntime/core/optimizer/constant_folding.cc#L40)

C. v1.23.2, commit `a83fc4d58cb48eb68890dd689f94f28288cf2278`; [release API](https://api.github.com/repos/microsoft/onnxruntime/releases/tags/v1.23.2): 2025-10-25 04:15:21 UTC. `ConstantFoldShapeNode`40–98 и CPU folding252–279. Raw открыт.

<a id="S037"></a>
## S037

Primary identity: https://github.com/microsoft/onnxruntime/issues/33345

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F037](RAW_FACTS.md#F037)

Происхождение: `W1-03-S17`, [W1-03](_WORK/W1_03.md), строка 39.

[ConvAddFusion issue33345](https://github.com/microsoft/onnxruntime/issues/33345)

R. Открыт2026-10-13 09:44:45 UTC, на момент чтения open. Body/Reproduction/Expected and actual/Environment получены также через GitHub API. ORT1.31.0, ONNX1.23.1, NumPy2.5.3, Python3.12.6, Windows11 x64, CPU EP, opset18, IR10.

<a id="S038"></a>
## S038

Primary identity: https://github.com/microsoft/onnxruntime/issues/33358

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F038](RAW_FACTS.md#F038)

Происхождение: `W1-03-S18`, [W1-03](_WORK/W1_03.md), строка 40.

[GatherToSliceFusion issue33358](https://github.com/microsoft/onnxruntime/issues/33358)

R. Открыт2026-10-14 03:13:17 UTC, open. Body/Reproduction/Environment получены через API. ORT1.31.0, ONNX1.23.1, NumPy2.5.3, Python3.12.6, Windows11 x64 CPU EP; opset21 IR10.

<a id="S039"></a>
## S039

Primary identity: https://github.com/onnx/onnx/blob/v1.19.1/onnx/utils.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F039](RAW_FACTS.md#F039)

Происхождение: `W1-03-S19`, [W1-03](_WORK/W1_03.md), строка 41.

[extract_model](https://github.com/onnx/onnx/blob/v1.19.1/onnx/utils.py#L195), [convert_version](https://github.com/onnx/onnx/blob/v1.19.1/onnx/version_converter.py#L17)

C. v1.19.1. utils195–259: tensor-name boundaries и ограничение If/Loop; version_converter17–40: raises RuntimeError при отсутствии необходимого преобразования. Raw открыт.

<a id="S040"></a>
## S040

Primary identity: https://onnxruntime.ai/docs/execution-providers/

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F040](RAW_FACTS.md#F040)

Происхождение: `W1-03-S20`, [W1-03](_WORK/W1_03.md), строка 42.

[ORT execution providers](https://onnxruntime.ai/docs/execution-providers/), [troubleshooting](https://onnxruntime.ai/docs/performance/tune-performance/troubleshooting.html)

D. §Use Execution Providers/GetCapability; §Why is my model running slower on GPU than on CPU: placement и verbose logging.

<a id="S041"></a>
## S041

Primary identity: https://onnxruntime.ai/docs/tutorials/mobile/helpers/make-dynamic-shape-fixed.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: контекст/ограничение в инженерных приложениях

Происхождение: `W1-03-S21`, [W1-03](_WORK/W1_03.md), строка 43.

[Fix dynamic shape helper](https://onnxruntime.ai/docs/tutorials/mobile/helpers/make-dynamic-shape-fixed.html)

D. §Usage, Making a symbolic dimension fixed, Making an input shape fixed. NNAPI/CoreML примеры не свидетельствуют о LinQ.

<a id="S042"></a>
## S042

Primary identity: https://github.com/microsoft/onnxruntime/blob/v1.23.2/onnxruntime/python/onnxruntime_inference_collection.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F040](RAW_FACTS.md#F040)

Происхождение: `W1-03-S22`, [W1-03](_WORK/W1_03.md), строка 44.

[ORT Python session implementation](https://github.com/microsoft/onnxruntime/blob/v1.23.2/onnxruntime/python/onnxruntime_inference_collection.py#L481)

C. v1.23.2: `disabled_optimizers`481–485, `_create_inference_session`502, преобразование в set577–584. Код прямо называет параметр внутренним и обычно недокументированным.

<a id="S043"></a>
## S043

Primary identity: https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F041](RAW_FACTS.md#F041), [F042](RAW_FACTS.md#F042), [F043](RAW_FACTS.md#F043), [F165](RAW_FACTS.md#F165), [F166](RAW_FACTS.md#F166), [F172](RAW_FACTS.md#F172), [F174](RAW_FACTS.md#F174), [F181](RAW_FACTS.md#F181), [F182](RAW_FACTS.md#F182), [F184](RAW_FACTS.md#F184), [F188](RAW_FACTS.md#F188), [F189](RAW_FACTS.md#F189), [F190](RAW_FACTS.md#F190), [F191](RAW_FACTS.md#F191), [F192](RAW_FACTS.md#F192), [F193](RAW_FACTS.md#F193), [F235](RAW_FACTS.md#F235), [F238](RAW_FACTS.md#F238)

Происхождение: `W1-04-S01`, [W1-04](_WORK/W1_04.md), строка 132. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S043](SOURCES.md#S043).** Павел Шерстнев / sherstpasha, сторонний [linq-cv-bench run_yolov8_tpu.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py#L164). Pinned hash 3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140; raw повторно получен. Дата commit независимо здесь не подтверждена (API 403); сосед указывает 2026-04-03. Локаторы 164–183,206,272–305; [F041](RAW_FACTS.md#F041), [F042](RAW_FACTS.md#F042), [F043](RAW_FACTS.md#F043). Code observation, не vendor documentation.

Происхождение: `W1-13-S08`, [W1-13](_WORK/W1_13.md), строка 30. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Тот же commit, runtime. https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py

Raw HTTP200; run_once L109–112; main imports L191–196; malformed arg L206; Device/load L209–220; host NMS L273–282. Прочитан код, не выполнен.

Происхождение: `W1-14-S03`, [W1-14](_WORK/W1_14.md), строка 21. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_14](_WORK/MATERIALS_W1_14/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Тот же commit, [run_yolov8_tpu.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py); L69–78,109–112,164–183,206,272–305

Raw заново скачан и прочитан; SHA256 `06aee82f9dc970627820ea4e2adfaac890b8a6843ac6856d9556c7ff9ebf38c5`. Код не исполнен.

Происхождение: `W1-15-S02`, [W1-15](_WORK/W1_15.md), строка 24. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_15](_WORK/MATERIALS_W1_15/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[run_yolov8_tpu.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py), commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`

Свежий raw HTTP успешно получен и прочитан целиком; локально [MATERIALS_W1_15/run_yolov8_tpu.py](_WORK/MATERIALS_W1_15/run_yolov8_tpu.py). Дата commit 2026-04-03 по сохранённым metadata W1-04, здесь заново не запрашивалась. Статический аудит стороннего кода, не vendor guarantee и не выполненный тест

Происхождение: `W2-05-S07`, [W2-05](_WORK/W2_05.md), строка 19. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_05](_WORK/MATERIALS_W2_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[self-build YOLOv8 runner PIN](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py), L109–112,206,269–280,311–333; соседние build/export того же PIN

Свежие raw200, статическое чтение; результаты self-build не обнаружены в [S169](SOURCES.md#S169).

<a id="S044"></a>
## S044

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/modules/block.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F044](RAW_FACTS.md#F044)

Происхождение: `W1-04-S03`, [W1-04](_WORK/W1_04.md), строка 134. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S044](SOURCES.md#S044).** Ultralytics [block.py, DFL](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/modules/block.py#L58), та же версия, 58–80; [F044](RAW_FACTS.md#F044).

<a id="S045"></a>
## S045

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/utils/nms.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F043](RAW_FACTS.md#F043), [F045](RAW_FACTS.md#F045), [F048](RAW_FACTS.md#F048), [F049](RAW_FACTS.md#F049), [F052](RAW_FACTS.md#F052), [F053](RAW_FACTS.md#F053), [F209](RAW_FACTS.md#F209)

Происхождение: `W1-04-S04`, [W1-04](_WORK/W1_04.md), строка 135. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S045](SOURCES.md#S045).** Ultralytics [utils/nms.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/utils/nms.py#L13), та же версия. non_max_suppression 13–166; [F043](RAW_FACTS.md#F043),[F045](RAW_FACTS.md#F045),[F048](RAW_FACTS.md#F048),[F049](RAW_FACTS.md#F049),[F052](RAW_FACTS.md#F052),[F053](RAW_FACTS.md#F053).

Происхождение: `W2-02-S06`, [W2-02](_WORK/W2_02.md), строка 22. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [nms.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/utils/nms.py#L13)

13–166; TorchNMS.nms255–296

Raw200. Runtime branch зависит от наличия `torchvision` в `sys.modules`.

<a id="S046"></a>
## S046

Primary identity: https://github.com/ultralytics/yolov5/blob/915bbf294bb74c859f0b41f1c23bc395014ea679/models/yolo.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F047](RAW_FACTS.md#F047)

Происхождение: `W1-04-S05`, [W1-04](_WORK/W1_04.md), строка 136. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S046](SOURCES.md#S046).** Ultralytics [YOLOv5 models/yolo.py v7.0](https://github.com/ultralytics/yolov5/blob/915bbf294bb74c859f0b41f1c23bc395014ea679/models/yolo.py#L38). API ref v7.0→915bbf294bb74c859f0b41f1c23bc395014ea679, commit 2022-11-22T15:23:47Z; release date отдельно не проверена. Detect 38–89; [F047](RAW_FACTS.md#F047).

<a id="S047"></a>
## S047

Primary identity: https://github.com/ultralytics/yolov5/blob/915bbf294bb74c859f0b41f1c23bc395014ea679/utils/general.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F047](RAW_FACTS.md#F047)

Происхождение: `W1-04-S06`, [W1-04](_WORK/W1_04.md), строка 137. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S047](SOURCES.md#S047).** Ultralytics [YOLOv5 utils/general.py v7.0](https://github.com/ultralytics/yolov5/blob/915bbf294bb74c859f0b41f1c23bc395014ea679/utils/general.py#L884), та же версия, NMS 884–999; [F047](RAW_FACTS.md#F047).

<a id="S048"></a>
## S048

Primary identity: https://github.com/onnx/onnx/blob/57b9c6a4f6eebb09ae1b34cfb632078518f72832/docs/Operators.md

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F051](RAW_FACTS.md#F051), [F052](RAW_FACTS.md#F052)

Происхождение: `W1-04-S08`, [W1-04](_WORK/W1_04.md), строка 139. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S048](SOURCES.md#S048).** ONNX maintainers [Operators.md NonMaxSuppression](https://github.com/onnx/onnx/blob/57b9c6a4f6eebb09ae1b34cfb632078518f72832/docs/Operators.md#NonMaxSuppression), tag v1.19.0→57b9c6a4f6eebb09ae1b34cfb632078518f72832, commit 2025-08-26T21:37:09Z, release date отдельно не проверена. Operator since opset11, lines 21322–21364; [F051](RAW_FACTS.md#F051)/F12. Дополнительно открыта [официальная страница](https://onnx.ai/onnx/operators/onnx__NonMaxSuppression.html), отображает docs 1.24.0; технические выводы привязаны к pinned spec, не к дате текущего сайта.

<a id="S049"></a>
## S049

Primary identity: https://docs.pytorch.org/vision/0.24/generated/torchvision.ops.nms.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F052](RAW_FACTS.md#F052), [F053](RAW_FACTS.md#F053), [F076](RAW_FACTS.md#F076), [F147](RAW_FACTS.md#F147)

Происхождение: `W1-04-S09`, [W1-04](_WORK/W1_04.md), строка 140. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S049](SOURCES.md#S049).** PyTorch/Torchvision [nms documentation 0.24](https://docs.pytorch.org/vision/0.24/generated/torchvision.ops.nms.html), Warning и Parameters/Returns. Дата публикации страницы не указана. [F052](RAW_FACTS.md#F052)/F13. Содержит первичную оговорку CPU/GPU ties; количественного измерения не публикует.

Происхождение: `W1-06-S08`, [W1-06](_WORK/W1_06.md), строка 32. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_06](_WORK/MATERIALS_W1_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[torchvision.ops.nms, torchvision 0.24](https://docs.pytorch.org/vision/0.24/generated/torchvision.ops.nms.html), дата страницы не указана

Documentation; описание строки 29–43, особенно equal-score CPU/GPU tie

Происхождение: `W1-12-S04`, [W1-12](_WORK/W1_12.md), строка 22. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_12](_WORK/MATERIALS_W1_12/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

PyTorch, [torchvision.ops.nms, docs 0.24](https://docs.pytorch.org/vision/0.24/generated/torchvision.ops.nms.html), дата публикации/релиза здесь не установлена; description и Parameters

DOC. CPU/GPU ties; не спецификация всех NMS.

<a id="S050"></a>
## S050

Primary identity: https://github.com/facebookresearch/detr/blob/29901c51d7fe8712168b8d0d64351170bc0f83e0/models/detr.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F054](RAW_FACTS.md#F054)

Происхождение: `W1-04-S10`, [W1-04](_WORK/W1_04.md), строка 141. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S050](SOURCES.md#S050).** Meta/Facebook Research [DETR models/detr.py](https://github.com/facebookresearch/detr/blob/29901c51d7fe8712168b8d0d64351170bc0f83e0/models/detr.py#L258), commit 29901c51d7fe8712168b8d0d64351170bc0f83e0, API date 2024-03-12T15:58:25Z; PostProcess 258–286. [F054](RAW_FACTS.md#F054). Не утверждается, что это дата оригинальной публикации DETR.

<a id="S051"></a>
## S051

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/models/rtdetr/predict.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F054](RAW_FACTS.md#F054), [F241](RAW_FACTS.md#F241), [F242](RAW_FACTS.md#F242), [F245](RAW_FACTS.md#F245)

Происхождение: `W1-04-S11`, [W1-04](_WORK/W1_04.md), строка 142. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S051](SOURCES.md#S051).** Ultralytics [RT-DETR predictor](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/models/rtdetr/predict.py#L54), v8.3.230; postprocess 54–72, pre_transform 75–89; [F054](RAW_FACTS.md#F054).

Происхождение: `W2-06-S03`, [W2-06](_WORK/W2_06.md), строка 15. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [RTDETRPredictor](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/models/rtdetr/predict.py), [BasePredictor](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/engine/predictor.py), [downloads.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/utils/downloads.py)

U; postprocess/pre_transform, BasePredictor151–173, attempt_download_asset425+; raw200.

<a id="S052"></a>
## S052

Primary identity: https://github.com/pytorch/vision/blob/7a9db90e9aadea3e3e1fec35969601167e9efd4f/torchvision/models/detection/faster_rcnn.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F055](RAW_FACTS.md#F055)

Происхождение: `W1-04-S12`, [W1-04](_WORK/W1_04.md), строка 143. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S052](SOURCES.md#S052).** PyTorch [torchvision FasterRCNN](https://github.com/pytorch/vision/blob/7a9db90e9aadea3e3e1fec35969601167e9efd4f/torchvision/models/detection/faster_rcnn.py#L43), v0.24.0→7a9db90e9aadea3e3e1fec35969601167e9efd4f, API commit 2025-10-10T04:10:42Z; release date отдельно не проверена. Class docstring; [F055](RAW_FACTS.md#F055).

<a id="S053"></a>
## S053

Primary identity: https://github.com/pytorch/vision/blob/7a9db90e9aadea3e3e1fec35969601167e9efd4f/torchvision/models/detection/roi_heads.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F055](RAW_FACTS.md#F055)

Происхождение: `W1-04-S13`, [W1-04](_WORK/W1_04.md), строка 144. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S053](SOURCES.md#S053).** PyTorch [RoIHeads.postprocess_detections](https://github.com/pytorch/vision/blob/7a9db90e9aadea3e3e1fec35969601167e9efd4f/torchvision/models/detection/roi_heads.py#L671), та же версия, 671–726; [F055](RAW_FACTS.md#F055).

<a id="S054"></a>
## S054

Primary identity: https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/codecs/simcc_label.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F056](RAW_FACTS.md#F056), [F243](RAW_FACTS.md#F243), [F244](RAW_FACTS.md#F244), [F245](RAW_FACTS.md#F245)

Происхождение: `W1-04-S14`, [W1-04](_WORK/W1_04.md), строка 145. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S054](SOURCES.md#S054).** OpenMMLab [MMPose SimCCLabel](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/codecs/simcc_label.py#L156), v1.3.2→5408bc76f5b848cf925a0d1857899011d8c5b497, API commit 2024-07-12T11:27:25Z; release date отдельно не проверена. decode 156–200; [F056](RAW_FACTS.md#F056).

Происхождение: `W2-06-S08`, [W2-06](_WORK/W2_06.md), строка 20. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

OpenMMLab [SimCCLabel](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/codecs/simcc_label.py), [TopdownAffine](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/datasets/transforms/topdown_transforms.py), [TopdownPoseEstimator](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/models/pose_estimators/topdown.py)

M; decode156–200, affine transform85–135, add_pred_to_datasample150–171. get_simcc_maximum primary helper свежо прочитан в v1.0.0 и сохранён W1-04 для M; v1.3.2 имеет дополнительный apply_softmax flag, defaultFalse.

<a id="S055"></a>
## S055

Primary identity: https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/codecs/utils/post_processing.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F056](RAW_FACTS.md#F056)

Происхождение: `W1-04-S15`, [W1-04](_WORK/W1_04.md), строка 146. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_04](_WORK/MATERIALS_W1_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

- **[S055](SOURCES.md#S055).** OpenMMLab [get_simcc_maximum](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/codecs/utils/post_processing.py#L41), та же версия, 41–105; [F056](RAW_FACTS.md#F056).

Проверенные числа в этом отчёте — размерности/параметры исходного кода и явно заданные арифметические fixtures. Опубликованных benchmark measurements и собственного измерения точности/скорости в этой ветке нет.

<a id="S056"></a>
## S056

Primary identity: https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/data/augment.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F058](RAW_FACTS.md#F058)

Происхождение: `W1-05-S01`, [W1-05](_WORK/W1_05.md), строка 23. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_05](_WORK/MATERIALS_W1_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[Ultralytics augment.py](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/data/augment.py#L1563), `LetterBox.__call__`, локальные строки 1563–1598

v8.3.0; release 2024-09-30 01:00:15Z; commit `6e43d1e1e5db72afbf686dee6745669bcb124b0a`

code observation

<a id="S057"></a>
## S057

Primary identity: https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/engine/predictor.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F057](RAW_FACTS.md#F057), [F058](RAW_FACTS.md#F058)

Происхождение: `W1-05-S02`, [W1-05](_WORK/W1_05.md), строка 24. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_05](_WORK/MATERIALS_W1_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[predictor.py](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/engine/predictor.py#L115), `BasePredictor.preprocess/pre_transform`, 115–156

тот же tag/commit

code observation

<a id="S058"></a>
## S058

Primary identity: https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/utils/ops.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F059](RAW_FACTS.md#F059), [F060](RAW_FACTS.md#F060)

Происхождение: `W1-05-S03`, [W1-05](_WORK/W1_05.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_05](_WORK/MATERIALS_W1_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[ops.py](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/utils/ops.py#L88), `scale_boxes` 88–123; `clip_boxes` 315–334; `xywh2xyxy` 412+; `scale_coords` 733–конец

тот же tag/commit

code observation

<a id="S059"></a>
## S059

Primary identity: https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/models/yolo/pose/predict.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F059](RAW_FACTS.md#F059)

Происхождение: `W1-05-S04`, [W1-05](_WORK/W1_05.md), строка 26. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_05](_WORK/MATERIALS_W1_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[pose/predict.py](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/models/yolo/pose/predict.py), `PosePredictor.postprocess`, локальные строки 50–52

тот же tag/commit

code observation

<a id="S060"></a>
## S060

Primary identity: https://github.com/pytorch/vision/blob/afc54f754c734d903a06194e416495e20d920ff6/torchvision/models/detection/transform.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F061](RAW_FACTS.md#F061)

Происхождение: `W1-05-S05`, [W1-05](_WORK/W1_05.md), строка 27. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_05](_WORK/MATERIALS_W1_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[torchvision detection/transform.py](https://github.com/pytorch/vision/blob/afc54f754c734d903a06194e416495e20d920ff6/torchvision/models/detection/transform.py), `_resize_image_and_masks` 25–83; `GeneralizedRCNNTransform` 119–169, 237–277; `resize_keypoints/boxes` 288–319

v0.20.0; release 2024-10-17 16:22:28Z; commit `afc54f754c734d903a06194e416495e20d920ff6`, 2024-10-04

code observation

<a id="S061"></a>
## S061

Primary identity: https://github.com/onnx/onnx/blob/3bf92c03a9f27eba3bda1e5b9e63ea20ec213557/onnx/defs/tensor/defs.cc

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F062](RAW_FACTS.md#F062)

Происхождение: `W1-05-S06`, [W1-05](_WORK/W1_05.md), строка 28. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_05](_WORK/MATERIALS_W1_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[ONNX defs/tensor/defs.cc](https://github.com/onnx/onnx/blob/3bf92c03a9f27eba3bda1e5b9e63ea20ec213557/onnx/defs/tensor/defs.cc#L2150), `Resize_ver19_attr_coordinate_transformation_mode_doc`, 2150–2190, schema 2246+

ONNX v1.16.2; release 2024-08-01 13:15:32Z; commit `3bf92c03a9f27eba3bda1e5b9e63ea20ec213557`

schema documentation in code; привязка к Resize schema, не ко всем opset

<a id="S062"></a>
## S062

Primary identity: https://github.com/opencv/opencv/blob/71d3237a093b60a27601c20e9ee6c3e52154e8b1/modules/videoio/src/cap_ffmpeg_impl.hpp

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F063](RAW_FACTS.md#F063)

Происхождение: `W1-05-S07`, [W1-05](_WORK/W1_05.md), строка 29. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_05](_WORK/MATERIALS_W1_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[OpenCV cap_ffmpeg_impl.hpp](https://github.com/opencv/opencv/blob/71d3237a093b60a27601c20e9ee6c3e52154e8b1/modules/videoio/src/cap_ffmpeg_impl.hpp), result_format 1653–1656; POS_MSEC 1786–1790; ORIENTATION 1840–1847, 2062+

4.10.0; release 2024-06-03 08:08:09Z; commit `71d3237a093b60a27601c20e9ee6c3e52154e8b1`

code observation именно FFmpeg backend

<a id="S063"></a>
## S063

Primary identity: https://github.com/FFmpeg/FFmpeg/blob/b08d7969c550a804a59511c7b83f2dd8cc0499b8/libavutil/frame.h

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F064](RAW_FACTS.md#F064)

Происхождение: `W1-05-S08`, [W1-05](_WORK/W1_05.md), строка 30. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_05](_WORK/MATERIALS_W1_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[FFmpeg frame.h](https://github.com/FFmpeg/FFmpeg/blob/b08d7969c550a804a59511c7b83f2dd8cc0499b8/libavutil/frame.h), DISPLAYMATRIX 74–80; SAR/pts/time_base 493–516; best_effort_timestamp 688

n7.1; commit `b08d7969c550a804a59511c7b83f2dd8cc0499b8`, 2024-09-29 16:47:04Z; отдельная release date не установлена

API documentation

<a id="S064"></a>
## S064

Primary identity: https://github.com/FFmpeg/FFmpeg/blob/b08d7969c550a804a59511c7b83f2dd8cc0499b8/doc/ffmpeg.texi

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F065](RAW_FACTS.md#F065)

Происхождение: `W1-05-S09`, [W1-05](_WORK/W1_05.md), строка 31. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_05](_WORK/MATERIALS_W1_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[FFmpeg ffmpeg.texi](https://github.com/FFmpeg/FFmpeg/blob/b08d7969c550a804a59511c7b83f2dd8cc0499b8/doc/ffmpeg.texi), display_rotation 1191+; autorotate 1254+; fps_mode 1998–2023

n7.1, тот же commit

CLI documentation

<a id="S065"></a>
## S065

Primary identity: https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/datasets/transforms/topdown_transforms.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F066](RAW_FACTS.md#F066)

Происхождение: `W1-05-S10`, [W1-05](_WORK/W1_05.md), строка 32. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_05](_WORK/MATERIALS_W1_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[MMPose topdown_transforms.py](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/datasets/transforms/topdown_transforms.py), `TopdownAffine.transform`, локальные 85–135

v1.3.2; release 2024-07-12 12:18:03Z; tag SHA `5408bc76f5b848cf925a0d1857899011d8c5b497` проверен git ls-remote

code observation; release API получен, commit API rate limited

<a id="S066"></a>
## S066

Primary identity: https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/models/pose_estimators/topdown.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F066](RAW_FACTS.md#F066)

Происхождение: `W1-05-S11`, [W1-05](_WORK/W1_05.md), строка 33. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_05](_WORK/MATERIALS_W1_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[MMPose topdown.py](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/models/pose_estimators/topdown.py), `add_pred_to_datasample`, локальные 150–156

тот же tag

code observation

<a id="S067"></a>
## S067

Primary identity: https://docs.pytorch.org/docs/2.9/notes/numerical_accuracy.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F067](RAW_FACTS.md#F067), [F068](RAW_FACTS.md#F068)

Происхождение: `W1-06-S01`, [W1-06](_WORK/W1_06.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_06](_WORK/MATERIALS_W1_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[PyTorch Numerical accuracy, 2.9](https://docs.pytorch.org/docs/2.9/notes/numerical_accuracy.html). Страница updated 2025-07-16. [Релиз v2.9.0](https://github.com/pytorch/pytorch/releases/tag/v2.9.0) опубликован 2025-10-15T17:12:27Z по GitHub API, полученному в этой сессии

Documentation; §§Batched computations, Extremal values, TF32, Reduced Precision Reduction for FP16 and BF16 GEMMs, SDPA. В web-представлении строки 68–117

<a id="S068"></a>
## S068

Primary identity: https://docs.pytorch.org/docs/2.9/amp.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F069](RAW_FACTS.md#F069)

Происхождение: `W1-06-S02`, [W1-06](_WORK/W1_06.md), строка 26. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_06](_WORK/MATERIALS_W1_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[torch.amp, PyTorch 2.9](https://docs.pytorch.org/docs/2.9/amp.html), updated 2025-06-12

Documentation; Autocasting, Op Eligibility, CUDA Ops that can autocast to float32; строки 124–159, 317–338

<a id="S069"></a>
## S069

Primary identity: https://docs.pytorch.org/docs/2.9/notes/randomness.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F070](RAW_FACTS.md#F070)

Происхождение: `W1-06-S03`, [W1-06](_WORK/W1_06.md), строка 27. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_06](_WORK/MATERIALS_W1_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[Reproducibility, PyTorch 2.9](https://docs.pytorch.org/docs/2.9/notes/randomness.html), updated 2024-11-26

Documentation; Controlling sources of randomness; CUDA convolution benchmarking; Avoiding nondeterministic algorithms, строки 68–115

<a id="S070"></a>
## S070

Primary identity: https://github.com/microsoft/onnxconverter-common/blob/a84c006a53a373207ee6206c52df682ae1f7e509/onnxconverter_common/float16.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F071](RAW_FACTS.md#F071), [F072](RAW_FACTS.md#F072)

Происхождение: `W1-06-S04`, [W1-06](_WORK/W1_06.md), строка 28. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_06](_WORK/MATERIALS_W1_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[onnxconverter-common float16.py, commit a84c006a53a373207ee6206c52df682ae1f7e509](https://github.com/microsoft/onnxconverter-common/blob/a84c006a53a373207ee6206c52df682ae1f7e509/onnxconverter_common/float16.py), tag v1.16.0

Code observation; `convert_np_to_float16` строки 26–81; `convert_tensor_float_to_float16` 83–122; `DEFAULT_OP_BLOCK_LIST` 128–157; `convert_float_to_float16` 180–246. Tag→commit проверен GitHub API и сохранён MATERIALS_W1_06/CONVERTER_TAG.json; raw файл сохранён FLOAT16_V1_16_0.py. Дата commit/release не установлена: следующий API-запрос получил rate limit; tag/commit закреплены

<a id="S071"></a>
## S071

Primary identity: https://onnxruntime.ai/docs/performance/model-optimizations/float16.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F073](RAW_FACTS.md#F073), [F115](RAW_FACTS.md#F115), [F229](RAW_FACTS.md#F229)

Происхождение: `W1-06-S05`, [W1-06](_WORK/W1_06.md), строка 29. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_06](_WORK/MATERIALS_W1_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[ORT Float16 and mixed precision models](https://onnxruntime.ai/docs/performance/model-optimizations/float16.html)

Documentation, страница без закреплённой версии/даты публикации; §§Float16 Tool Arguments и Mixed Precision Tool Arguments, строки 196–233. Не объявляется контрактом всех будущих ORT/CPU EP

Происхождение: `W1-09-S04`, [W1-09](_WORK/W1_09.md), строка 22. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_09](_WORK/MATERIALS_W1_09/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [ORT Float16 and mixed precision](https://onnxruntime.ai/docs/performance/model-optimizations/float16.html), live без pinned release/date, §§Mixed Precision, Tool Arguments, L200–233

Documentation; указанный GPU requirement требует сверки с [S101](SOURCES.md#S101)

Происхождение: `W2-03-S09`, [W2-03](_WORK/W2_03.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_03](_WORK/MATERIALS_W2_03/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [Float16 and mixed precision](https://onnxruntime.ai/docs/performance/model-optimizations/float16.html), §Mixed Precision; [gh-pages raw](https://github.com/microsoft/onnxruntime/blob/gh-pages/docs/performance/model-optimizations/float16.md#L45), L45–62

**Fresh live documentation**, raw SHA `049e63…9b299`; GPU requirement и ModelProto example. Версия/дата документа не объявлены. Путь docs на tag v1.23.2 и rel-1.23.2 дал 404; нельзя назвать live текст документацией релиза v1.23.2.

<a id="S072"></a>
## S072

Primary identity: https://arxiv.org/abs/1909.03469v1

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F074](RAW_FACTS.md#F074)

Происхождение: `W1-06-S06`, [W1-06](_WORK/W1_06.md), строка 30. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_06](_WORK/MATERIALS_W1_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Blanchard, D. Higham, N. Higham, [Accurate Computation of the Log-Sum-Exp and Softmax Functions, arXiv v1](https://arxiv.org/html/1909.03469v1), 2019-09-08

Авторская статья, прочитано HTML full text; §1, Table 1; §4 Algorithms with shifting; §6 Conclusions. Теоретический анализ, не benchmark нашей CV-модели

<a id="S073"></a>
## S073

Primary identity: https://numpy.org/doc/2.2/reference/generated/numpy.isclose.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F075](RAW_FACTS.md#F075)

Происхождение: `W1-06-S07`, [W1-06](_WORK/W1_06.md), строка 31. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_06](_WORK/MATERIALS_W1_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[NumPy isclose, 2.2](https://numpy.org/doc/2.2/reference/generated/numpy.isclose.html), дата страницы не указана

Documentation; Warning и Notes, строки 81–89, 127–134

<a id="S074"></a>
## S074

Primary identity: https://developers.google.com/edge/litert/conversion/tensorflow/quantization/post_training_float16_quant

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F077](RAW_FACTS.md#F077)

Происхождение: `W1-06-S09`, [W1-06](_WORK/W1_06.md), строка 33. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_06](_WORK/MATERIALS_W1_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[Google LiteRT post-training float16 quantization](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/post_training_float16_quant), страница updated 2026-05-28 UTC

Documentation/tutorial; Overview строки 42–45 и Convert строки 108–115. Tutorial измерения MNIST не используются как evidence качества нашего переноса

<a id="S075"></a>
## S075

Primary identity: https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F079](RAW_FACTS.md#F079), [F089](RAW_FACTS.md#F089), [F090](RAW_FACTS.md#F090), [F101](RAW_FACTS.md#F101), [F105](RAW_FACTS.md#F105), [F110](RAW_FACTS.md#F110), [F144](RAW_FACTS.md#F144)

Происхождение: `W1-07-S01`, [W1-07](_WORK/W1_07.md), строка 32. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, ORT documentation; изменяемая страница, точная публикация не указана

https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html — Static/Dynamic Quantization, Debugging, Int4/UInt4, FAQ

Происхождение: `W1-08-S10`, [W1-08](_WORK/W1_08.md), строка 28. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_08](_WORK/MATERIALS_W1_08/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[ONNX Runtime quantization](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html), текущая невёрсионированная документация; дата публикации не указана

Открыты representations QDQ/QOperator, method selection, accuracy debugging. Не использовать как lock-файл ORT.

Происхождение: `W1-09-S01`, [W1-09](_WORK/W1_09.md), строка 19. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_09](_WORK/MATERIALS_W1_09/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [ORT Quantize ONNX models](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html), live без pinned release/date; §§Quantization Debugging, ONNX representation, строки страницы 198–208, 244–253

Documentation; прочитана страница, а не snippets

Происхождение: `W1-12-S01`, [W1-12](_WORK/W1_12.md), строка 19. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_12](_WORK/MATERIALS_W1_12/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [Quantize ONNX Models](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html), mutable docs, дата публикации/редакции не указана; Quantization Debugging

DOC. Сопоставление весов/активаций, затруднения при перестройке graph. Возможности ORT, не LinQ.

<a id="S076"></a>
## S076

Primary identity: https://github.com/microsoft/onnxruntime/blob/v1.22.0/onnxruntime/python/tools/quantization/calibrate.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F080](RAW_FACTS.md#F080), [F090](RAW_FACTS.md#F090), [F216](RAW_FACTS.md#F216)

Происхождение: `W1-07-S02`, [W1-07](_WORK/W1_07.md), строка 33. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, ORT v1.22.0; release 2025-05-10T01:14:00Z, short commit f217402

https://github.com/microsoft/onnxruntime/blob/v1.22.0/onnxruntime/python/tools/quantization/calibrate.py — CalibrationMethod, MinMaxCalibrater, PercentileCalibrater, DistributionCalibrater, HistogramCollector.get_entropy_threshold, create_calibrator. Release: https://github.com/microsoft/onnxruntime/releases/tag/v1.22.0

<a id="S077"></a>
## S077

Primary identity: https://github.com/microsoft/onnxruntime/blob/v1.22.0/onnxruntime/python/tools/quantization/quantize.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F080](RAW_FACTS.md#F080), [F081](RAW_FACTS.md#F081), [F090](RAW_FACTS.md#F090)

Происхождение: `W1-07-S03`, [W1-07](_WORK/W1_07.md), строка 34. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, ORT v1.22.0

https://github.com/microsoft/onnxruntime/blob/v1.22.0/onnxruntime/python/tools/quantization/quantize.py — quantize_static, get_qdq_config; local lines 478–505, 635–636, 660–670

<a id="S078"></a>
## S078

Primary identity: https://docs.openvino.ai/2025/openvino-workflow/model-optimization-guide/quantizing-models-post-training/basic-quantization-flow.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F082](RAW_FACTS.md#F082), [F090](RAW_FACTS.md#F090)

Происхождение: `W1-07-S04`, [W1-07](_WORK/W1_07.md), строка 35. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Intel/OpenVINO docs 2025, Basic Quantization Flow; дата страницы не установлена

https://docs.openvino.ai/2025/openvino-workflow/model-optimization-guide/quantizing-models-post-training/basic-quantization-flow.html — Tune quantization parameters: preset, subset_size, fast_bias_correction, ignored_scope, target_device

<a id="S079"></a>
## S079

Primary identity: https://github.com/openvinotoolkit/nncf/blob/v2.17.0/nncf/quantization/range_estimator.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F083](RAW_FACTS.md#F083), [F090](RAW_FACTS.md#F090)

Происхождение: `W1-07-S05`, [W1-07](_WORK/W1_07.md), строка 36. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Intel, NNCF v2.17.0; release 2025-06-18T14:59:06Z, short commit b34d24e

https://github.com/openvinotoolkit/nncf/blob/v2.17.0/nncf/quantization/range_estimator.py — StatisticsType, AggregatorType, StatisticsCollectorParameters, RangeEstimatorParametersSet. Release: https://github.com/openvinotoolkit/nncf/releases/tag/v2.17.0

<a id="S080"></a>
## S080

Primary identity: https://github.com/openvinotoolkit/nncf/blob/v2.17.0/nncf/quantization/advanced_parameters.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F083](RAW_FACTS.md#F083), [F090](RAW_FACTS.md#F090)

Происхождение: `W1-07-S06`, [W1-07](_WORK/W1_07.md), строка 37. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Intel, NNCF v2.17.0

https://github.com/openvinotoolkit/nncf/blob/v2.17.0/nncf/quantization/advanced_parameters.py — QuantizationParameters, AdvancedQuantizationParameters, convert_range_estimator_parameters_to_dict

<a id="S081"></a>
## S081

Primary identity: https://docs.openvino.ai/2025/openvino-workflow/model-optimization-guide/quantizing-models-post-training/quantizing-with-accuracy-control.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F084](RAW_FACTS.md#F084), [F090](RAW_FACTS.md#F090), [F114](RAW_FACTS.md#F114)

Происхождение: `W1-07-S07`, [W1-07](_WORK/W1_07.md), строка 38. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Intel/OpenVINO docs 2025, Accuracy Control; дата страницы не установлена

https://docs.openvino.ai/2025/openvino-workflow/model-optimization-guide/quantizing-models-post-training/quantizing-with-accuracy-control.html — validation callback, quantize_with_accuracy_control, max_drop/drop_type, saving reverted operations

Происхождение: `W1-09-S08`, [W1-09](_WORK/W1_09.md), строка 26. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_09](_WORK/MATERIALS_W1_09/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Intel, [OpenVINO 2025 Quantizing with Accuracy Control](https://docs.openvino.ai/2025/openvino-workflow/model-optimization-guide/quantizing-models-post-training/quantizing-with-accuracy-control.html), §§Prepare datasets, Run quantization, L4056–4207

Documentation; ветка 2025, дата обновления не установлена

<a id="S082"></a>
## S082

Primary identity: https://developers.google.com/edge/litert/conversion/tensorflow/quantization/post_training_integer_quant

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F085](RAW_FACTS.md#F085), [F090](RAW_FACTS.md#F090)

Происхождение: `W1-07-S08`, [W1-07](_WORK/W1_07.md), строка 39. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Google AI Edge, Post-training integer quantization; last updated 2026-05-28 UTC

https://developers.google.com/edge/litert/conversion/tensorflow/quantization/post_training_integer_quant — dynamic range, float fallback, integer-only quantization

<a id="S083"></a>
## S083

Primary identity: https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F087](RAW_FACTS.md#F087), [F090](RAW_FACTS.md#F090)

Происхождение: `W1-07-S09`, [W1-07](_WORK/W1_07.md), строка 40. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Google AI Edge, LiteRT 8-bit quantization specification; версия страницы не зафиксирована

https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec — Specification summary, Per-axis, CONV_2D, DEPTHWISE_CONV_2D

<a id="S084"></a>
## S084

Primary identity: https://github.com/tensorflow/tensorflow/blob/v2.20.0/tensorflow/lite/python/optimize/calibrator.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F086](RAW_FACTS.md#F086), [F090](RAW_FACTS.md#F090)

Происхождение: `W1-07-S10`, [W1-07](_WORK/W1_07.md), строка 41. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

TensorFlow authors, TensorFlow v2.20.0; release API published_at 2025-08-13T17:45:14Z

https://github.com/tensorflow/tensorflow/blob/v2.20.0/tensorflow/lite/python/optimize/calibrator.py — Calibrator._feed_tensors, calibrate_and_quantize. Release: https://github.com/tensorflow/tensorflow/releases/tag/v2.20.0

<a id="S085"></a>
## S085

Primary identity: https://github.com/tensorflow/tensorflow/blob/v2.20.0/tensorflow/lite/tools/optimize/calibration/calibration_logger.cc

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F086](RAW_FACTS.md#F086), [F090](RAW_FACTS.md#F090)

Происхождение: `W1-07-S11`, [W1-07](_WORK/W1_07.md), строка 42. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

TensorFlow authors, TensorFlow v2.20.0

https://github.com/tensorflow/tensorflow/blob/v2.20.0/tensorflow/lite/tools/optimize/calibration/calibration_logger.cc — MinMax::Update, lines 27–47

<a id="S086"></a>
## S086

Primary identity: https://arxiv.org/abs/2004.09602v1

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F088](RAW_FACTS.md#F088), [F090](RAW_FACTS.md#F090), [F230](RAW_FACTS.md#F230)

Происхождение: `W1-07-S12`, [W1-07](_WORK/W1_07.md), строка 43. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Wu, Judd, Zhang, Isaev, Micikevicius; paper arXiv v1, 2020-04-20

https://arxiv.org/html/2004.09602v1 — §§3.4,4.1–4.2, Table 5, Appendix A.1/Table 9

Происхождение: `W2-04-S01`, [W2-04](_WORK/W2_04.md), строка 11. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_04](_WORK/MATERIALS_W2_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Wu, Judd, Zhang, Isaev, Micikevicius, [Integer Quantization](https://arxiv.org/pdf/2004.09602v1), arXiv v1, 20 Apr 2020

PDF получен; §4, Tables 2/6/7/9/10, Appendix A; визуально сверены с.9,11,17. [PDF](_WORK/MATERIALS_W2_04/wu_2004.09602v1.pdf), [text](_WORK/MATERIALS_W2_04/wu_2004.09602v1.txt)

Published measurement в PyTorch/custom quantization; не доказательство integer deployment на конкретном ускорителе

<a id="S087"></a>
## S087

Primary identity: https://docs.openvino.ai/2025/openvino-workflow/model-optimization-guide/weight-compression.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F089](RAW_FACTS.md#F089), [F090](RAW_FACTS.md#F090)

Происхождение: `W1-07-S13`, [W1-07](_WORK/W1_07.md), строка 44. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_07](_WORK/MATERIALS_W1_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Intel/OpenVINO docs 2025, LLM Weight Compression

https://docs.openvino.ai/2025/openvino-workflow/model-optimization-guide/weight-compression.html — introduction, INT8/INT4 weight compression

<a id="S088"></a>
## S088

Primary identity: https://docs.pytorch.org/ao/stable/pt2e_quantization/pt2e_quant_qat.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F091](RAW_FACTS.md#F091), [F092](RAW_FACTS.md#F092), [F105](RAW_FACTS.md#F105)

Происхождение: `W1-08-S01`, [W1-08](_WORK/W1_08.md), строка 19. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_08](_WORK/MATERIALS_W1_08/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[PyTorch 2 Export QAT](https://docs.pytorch.org/ao/stable/pt2e_quantization/pt2e_quant_qat.html), torchao 0.17, Created/Updated 2026-03-25

Открыта документация: Import the Backend Specific Quantizer; Prepare; Training Loop; Conclusion. Пример использует XNNPACK, PyTorch 2.6+ capture.

<a id="S089"></a>
## S089

Primary identity: https://qualcomm.github.io/aimet-pages/releases/2.20.0/techniques/qat.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F093](RAW_FACTS.md#F093), [F105](RAW_FACTS.md#F105)

Происхождение: `W1-08-S02`, [W1-08](_WORK/W1_08.md), строка 20. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_08](_WORK/MATERIALS_W1_08/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[AIMET QAT](https://qualcomm.github.io/aimet-pages/releases/2.20.0/techniques/qat.html), 2.20.0; календарная дата релиза отдельно не установлена

Открыты Variants, Typical recommendations, Workflow, API/export; ONNX training tab — Not supported.

<a id="S090"></a>
## S090

Primary identity: https://qualcomm.github.io/aimet-pages/releases/2.20.0/tutorials/on_target_inference.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F094](RAW_FACTS.md#F094), [F105](RAW_FACTS.md#F105)

Происхождение: `W1-08-S03`, [W1-08](_WORK/W1_08.md), строка 21. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_08](_WORK/MATERIALS_W1_08/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[AIMET on-target inference](https://qualcomm.github.io/aimet-pages/releases/2.20.0/tutorials/on_target_inference.html), 2.20.0

Открыты экспорт model + encodings, Qualcomm conversion/quantization/compilation. Это документация Qualcomm, не LinQ.

<a id="S091"></a>
## S091

Primary identity: https://arxiv.org/abs/2004.10568v2

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F095](RAW_FACTS.md#F095), [F105](RAW_FACTS.md#F105)

Происхождение: `W1-08-S04`, [W1-08](_WORK/W1_08.md), строка 22. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_08](_WORK/MATERIALS_W1_08/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Nagel et al., [AdaRound](https://arxiv.org/html/2004.10568v2), arXiv v2 2020-06-30, ICML 2020; [metadata](https://arxiv.org/abs/2004.10568)

Полный HTML, §3.3, §5 experimental setup и robustness.

<a id="S092"></a>
## S092

Primary identity: https://qualcomm.github.io/aimet-pages/releases/2.20.0/tutorials/notebooks/onnx/quantization/adaround.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F096](RAW_FACTS.md#F096), [F105](RAW_FACTS.md#F105)

Происхождение: `W1-08-S05`, [W1-08](_WORK/W1_08.md), строка 23. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_08](_WORK/MATERIALS_W1_08/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[AIMET AdaRound ONNX notebook](https://qualcomm.github.io/aimet-pages/releases/2.20.0/tutorials/notebooks/onnx/quantization/adaround.html), 2.20.0; [feature/API guide](https://qualcomm.github.io/aimet-pages/releases/2.20.0/ptq_techniques/adaround.html)

Открыты реальный notebook и guide; пример ResNet18/ImageNet, авторская оговорка об упрощённом, не SOTA опыте.

<a id="S093"></a>
## S093

Primary identity: https://arxiv.org/abs/2102.05426v2

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F097](RAW_FACTS.md#F097), [F104](RAW_FACTS.md#F104), [F105](RAW_FACTS.md#F105), [F231](RAW_FACTS.md#F231)

Происхождение: `W1-08-S06`, [W1-08](_WORK/W1_08.md), строка 24. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_08](_WORK/MATERIALS_W1_08/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Li et al., [BRECQ](https://arxiv.org/html/2102.05426v2), arXiv v2 2021-07-25, ICLR 2021; [metadata](https://arxiv.org/abs/2102.05426)

Полный HTML: §3, §4.4, Appendix B.4.3/B.4.4.

Происхождение: `W2-04-S02`, [W2-04](_WORK/W2_04.md), строка 12. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_04](_WORK/MATERIALS_W2_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Li, Gong et al., [BRECQ](https://arxiv.org/pdf/2102.05426v2), arXiv v2, 25 Jul 2021 / ICLR2021

PDF получен; Tables 2–5, Appendix B.4.4; визуально сверены с.7,8,15. [PDF](_WORK/MATERIALS_W2_04/brecq_2102.05426v2.pdf), [text](_WORK/MATERIALS_W2_04/brecq_2102.05426v2.txt)

Published measurement; при сравнении методов таблица включает авторские reimplementations, помеченные *

<a id="S094"></a>
## S094

Primary identity: https://github.com/yhhhli/BRECQ/tree/e455d62e93c70351961f8991c913b59435bd165f

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F098](RAW_FACTS.md#F098), [F104](RAW_FACTS.md#F104), [F105](RAW_FACTS.md#F105)

Происхождение: `W1-08-S07`, [W1-08](_WORK/W1_08.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_08](_WORK/MATERIALS_W1_08/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[BRECQ source](https://github.com/yhhhli/BRECQ/tree/e455d62e93c70351961f8991c913b59435bd165f), HEAD SHA получен `git ls-remote`; дата commit отдельно не установлена

Raw содержимое README.md, main_imagenet.py, quant/quant_model.py, quant/block_recon.py, quant/quant_block.py прочитано и сохранено.

<a id="S095"></a>
## S095

Primary identity: https://arxiv.org/abs/1906.04721v2

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F099](RAW_FACTS.md#F099), [F105](RAW_FACTS.md#F105)

Происхождение: `W1-08-S08`, [W1-08](_WORK/W1_08.md), строка 26. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_08](_WORK/MATERIALS_W1_08/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Nagel et al., [Data-Free Quantization](https://arxiv.org/html/1906.04721v2), v2 2019-09-09, ICCV 2019

Полный HTML: §4.1 scaling equivariance, §4.2 bias correction, Appendix D empirical correction. CVF PDF дал HTTP 403; основание — открытый arXiv HTML.

<a id="S096"></a>
## S096

Primary identity: https://github.com/qualcomm/aimet/blob/492f54a7bb2ca60045ac56df4b782151ff605627/TrainingExtensions/torch/src/python/aimet_torch/bias_correction.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F100](RAW_FACTS.md#F100), [F105](RAW_FACTS.md#F105)

Происхождение: `W1-08-S09`, [W1-08](_WORK/W1_08.md), строка 27. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_08](_WORK/MATERIALS_W1_08/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

AIMET [bias_correction.py](https://github.com/qualcomm/aimet/blob/492f54a7bb2ca60045ac56df4b782151ff605627/TrainingExtensions/torch/src/python/aimet_torch/bias_correction.py), tag 2.20.0 → SHA `492f54a7bb2ca60045ac56df4b782151ff605627`

Raw прочитан, локальная копия `aimet_2_20_bias_correction.py`; функции `correct_bias`, `call_empirical_correct_bias`, `disable_output_quantizers`.

<a id="S097"></a>
## S097

Primary identity: https://www.tensorflow.org/model_optimization/guide/quantization/training

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F102](RAW_FACTS.md#F102), [F105](RAW_FACTS.md#F105)

Происхождение: `W1-08-S11`, [W1-08](_WORK/W1_08.md), строка 29. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_08](_WORK/MATERIALS_W1_08/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[TensorFlow Model Optimization QAT overview](https://www.tensorflow.org/model_optimization/guide/quantization/training), Last updated 2024-02-03 UTC

Открыты API compatibility, General support matrix, backend caveat. Документ старый; актуальную комбинацию TF/Keras/TFMOT следует проверить до установки.

<a id="S098"></a>
## S098

Primary identity: https://nvidia.github.io/Model-Optimizer/guides/quantization_aware_training_and_distillation.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F103](RAW_FACTS.md#F103), [F105](RAW_FACTS.md#F105)

Происхождение: `W1-08-S12`, [W1-08](_WORK/W1_08.md), строка 30. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_08](_WORK/MATERIALS_W1_08/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[NVIDIA ModelOpt QAT and Distillation](https://nvidia.github.io/Model-Optimizer/guides/quantization_aware_training_and_distillation.html), страница показала dev-version `0.0.1.dev1+g55003cc81`; дата публикации не установлена

Открыт текст QAT/QAD и Choose a framework. Не фиксировать по этой странице выпущенную версию пакета и не переносить LLM-рецепты на CV.

<a id="S099"></a>
## S099

Primary identity: https://github.com/microsoft/onnxruntime/blob/v1.23.2/onnxruntime/python/tools/quantization/quantize.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F106](RAW_FACTS.md#F106), [F107](RAW_FACTS.md#F107)

Происхождение: `W1-09-S02`, [W1-09](_WORK/W1_09.md), строка 20. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_09](_WORK/MATERIALS_W1_09/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [quantize.py v1.23.2](https://github.com/microsoft/onnxruntime/blob/v1.23.2/onnxruntime/python/tools/quantization/quantize.py#L479), `quantize_static`, L479–577, L755–779; [base_quantizer.py](https://github.com/microsoft/onnxruntime/blob/v1.23.2/onnxruntime/python/tools/quantization/base_quantizer.py#L172), `should_quantize_node`, L172–189

Code observation; raw загружен и прочитан; не исполнен

<a id="S100"></a>
## S100

Primary identity: https://github.com/microsoft/onnxruntime/blob/v1.23.2/onnxruntime/python/tools/quantization/qdq_loss_debug.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F108](RAW_FACTS.md#F108), [F109](RAW_FACTS.md#F109)

Происхождение: `W1-09-S03`, [W1-09](_WORK/W1_09.md), строка 21. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_09](_WORK/MATERIALS_W1_09/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [qdq_loss_debug.py v1.23.2](https://github.com/microsoft/onnxruntime/blob/v1.23.2/onnxruntime/python/tools/quantization/qdq_loss_debug.py), функции L64/115/180/270/341/375

Code observation; оригинальное имя функции содержит `noice`, не исправлять его в вызове

<a id="S101"></a>
## S101

Primary identity: https://github.com/microsoft/onnxconverter-common/blob/v1.16.0/onnxconverter_common/auto_mixed_precision.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F115](RAW_FACTS.md#F115), [F116](RAW_FACTS.md#F116), [F225](RAW_FACTS.md#F225), [F228](RAW_FACTS.md#F228)

Происхождение: `W1-09-S05`, [W1-09](_WORK/W1_09.md), строка 23. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_09](_WORK/MATERIALS_W1_09/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [auto_mixed_precision.py v1.16.0](https://github.com/microsoft/onnxconverter-common/blob/v1.16.0/onnxconverter_common/auto_mixed_precision.py), `auto_convert_mixed_precision` L36–116, `get_tensor_values_using_ort` L141–174, SegmentList/NodeSegment L177–242

Code observation; raw прочитан, SHA сохранён ниже; CPU provider явный

Происхождение: `W2-03-S04`, [W2-03](_WORK/W2_03.md), строка 20. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_03](_WORK/MATERIALS_W2_03/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [auto_mixed_precision.py](https://github.com/microsoft/onnxconverter-common/blob/v1.16.0/onnxconverter_common/auto_mixed_precision.py#L141), **v1.16.0**, `auto_convert_mixed_precision`, `get_tensor_values_using_ort`, L141–174

**Fresh static code**, SHA `69a04b…020d1`; оба InferenceSession жёстко задают CPUExecutionProvider. Комментарий CUDA касается extraction intermediate outputs. Не запускалось.

<a id="S102"></a>
## S102

Primary identity: https://github.com/openvinotoolkit/nncf/blob/v2.18.0/src/nncf/quantization/quantize_model.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F111](RAW_FACTS.md#F111)

Происхождение: `W1-09-S06`, [W1-09](_WORK/W1_09.md), строка 24. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_09](_WORK/MATERIALS_W1_09/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Intel/OpenVINO, [NNCF quantize_model.py v2.18.0](https://github.com/openvinotoolkit/nncf/blob/v2.18.0/src/nncf/quantization/quantize_model.py#L297), L297–409

Code observation; `quantize_with_accuracy_control` dispatch только OpenVINO/ONNX

<a id="S103"></a>
## S103

Primary identity: https://github.com/openvinotoolkit/nncf/blob/v2.18.0/src/nncf/quantization/algorithms/accuracy_control/algorithm.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F112](RAW_FACTS.md#F112), [F113](RAW_FACTS.md#F113)

Происхождение: `W1-09-S07`, [W1-09](_WORK/W1_09.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_09](_WORK/MATERIALS_W1_09/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Intel/OpenVINO, [NNCF accuracy_control/algorithm.py v2.18.0](https://github.com/openvinotoolkit/nncf/blob/v2.18.0/src/nncf/quantization/algorithms/accuracy_control/algorithm.py), L149–169, L286–393; [advanced_parameters.py](https://github.com/openvinotoolkit/nncf/blob/v2.18.0/src/nncf/quantization/advanced_parameters.py), RestoreMode L191–202, AdvancedAccuracyRestorerParameters L435–467

Code observation; greedy restoration, reranking и конечный бюджет

<a id="S104"></a>
## S104

Primary identity: https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-explicit-quantization.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F117](RAW_FACTS.md#F117)

Происхождение: `W1-09-S09`, [W1-09](_WORK/W1_09.md), строка 27. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_09](_WORK/MATERIALS_W1_09/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

NVIDIA, [TensorRT Explicit Quantization](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-explicit-quantization.html), live latest с navigation 11.4.0, §§Processing of Q/DQ, Placement, ONNX support, L154–175/177–178/206–234

Documentation; live 2026, не контракт 8.x/10.x. Родительская Working with Quantized Types обновлена Oct 05, 2026. В самой странице остался исторический текст «latest PyTorch 2.0»; поэтому он не используется как актуальное ограничение PyTorch

<a id="S105"></a>
## S105

Primary identity: https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/engine-tools.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F118](RAW_FACTS.md#F118)

Происхождение: `W1-09-S10`, [W1-09](_WORK/W1_09.md), строка 28. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_09](_WORK/MATERIALS_W1_09/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

NVIDIA, [TensorRT Engine Tools and Debugging](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/engine-tools.html), live latest, §Engine Inspector, L142–231

Documentation; подробность зависит от ProfilingVerbosity

<a id="S106"></a>
## S106

Primary identity: https://docs.openvino.ai/2025/api/ie_python_api/_autosummary/openvino.CompiledModel.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F118](RAW_FACTS.md#F118)

Происхождение: `W1-09-S11`, [W1-09](_WORK/W1_09.md), строка 29. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_09](_WORK/MATERIALS_W1_09/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Intel, [OpenVINO 2025 CompiledModel.get_runtime_model](https://docs.openvino.ai/2025/api/ie_python_api/_autosummary/openvino.CompiledModel.html), L4374–4383

Documentation; device-specific execution graph

<a id="S107"></a>
## S107

Primary identity: https://arxiv.org/abs/1911.03852v1

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F119](RAW_FACTS.md#F119)

Происхождение: `W1-09-S12`, [W1-09](_WORK/W1_09.md), строка 30. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_09](_WORK/MATERIALS_W1_09/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Dong et al., [HAWQ-V2 arXiv:1911.03852v1](https://arxiv.org/html/1911.03852v1), опубликован 2019-11-10, §§2.1–2.3, Assumption 1; quantitative benchmarks не используются

Авторская статья; метод Hessian trace и Pareto выбора. Численные benchmark gains не переносим: версия arXiv v1 отличается от NeurIPS 2020, наш стек не измерен

<a id="S108"></a>
## S108

Primary identity: https://arxiv.org/abs/2202.06934v3

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F120](RAW_FACTS.md#F120), [F121](RAW_FACTS.md#F121)

Происхождение: `W1-10-S01`, [W1-10](_WORK/W1_10.md), строка 15. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_10](_WORK/MATERIALS_W1_10/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

**[S108](SOURCES.md#S108) — SAHI, авторская статья.** Akyon, Altinuc, Temizel, arXiv:2202.06934v3, 07.04.2022; ICIP 2022. Открыт полный [HTML v3](https://arxiv.org/html/2202.06934v3), локальная копия `MATERIALS_W1_10/SAHI.html`. Локаторы: §3, §4, таблицы 1–2, абзацы перед заключением. Метод увеличивает относительный размер объектов через нарезку. Есть измерения на VisDrone/xView, а не фабрике; обсуждаются потери на крупных объектах. Важная деталь: таблицы используют AP50, не усреднённый COCO AP50:95. Числа из abstract без этой оговорки не переносить в отчёт.

<a id="S109"></a>
## S109

Primary identity: https://github.com/obss/sahi/blob/0.11.18/sahi/predict.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F122](RAW_FACTS.md#F122)

Происхождение: `W1-10-S02`, [W1-10](_WORK/W1_10.md), строка 17. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_10](_WORK/MATERIALS_W1_10/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

**[S109](SOURCES.md#S109) — SAHI, исходный код.** Проверен tag `0.11.18`, [sahi/predict.py](https://github.com/obss/sahi/blob/0.11.18/sahi/predict.py), [raw](https://raw.githubusercontent.com/obss/sahi/0.11.18/sahi/predict.py); сохранён `sahi_predict.py`. Локаторы по сохранённому raw: `get_sliced_prediction`, строки 125–285; defaults 130–138; `num_batch = 1`, строка 202; дополнительный полный проход 268+; верхнеуровневое переключение postprocess при низком confidence 472–476. Дата релиза и полный commit не установлены: GitHub API ответил rate-limit 403; tag и фактическое содержимое проверены. Не выдаётся за текущую последнюю версию. Первая попытка имени `v0.11.18` дала 404; верный tag без `v`.

<a id="S110"></a>
## S110

Primary identity: https://arxiv.org/abs/1910.06278v1

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F123](RAW_FACTS.md#F123)

Происхождение: `W1-10-S03`, [W1-10](_WORK/W1_10.md), строка 19. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_10](_WORK/MATERIALS_W1_10/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

**[S110](SOURCES.md#S110) — DARK, авторская статья.** Zhang et al., [полный arXiv HTML 1910.06278v1](https://arxiv.org/html/1910.06278v1), 14.10.2019; [CVPR 2020 proceedings](https://openaccess.thecvf.com/content_CVPR_2020/html/Zhang_Distribution-Aware_Coordinate_Representation_for_Human_Pose_Estimation_CVPR_2020_paper.html). Локальная копия `DARK.html`. Локаторы: Coordinate Decoding, уравнения 1–2 и 9–11; Coordinate Encoding, уравнения 12–13. CVF PDF при открытии вернул 403, вместо него прочитан полный авторский HTML. **Слово quantisation здесь означает округление пространственных координат при downsampling; это не эксперимент с INT8 весами/активациями.**

<a id="S111"></a>
## S111

Primary identity: https://arxiv.org/abs/1812.00324v2

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F124](RAW_FACTS.md#F124)

Происхождение: `W1-10-S04`, [W1-10](_WORK/W1_10.md), строка 21. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_10](_WORK/MATERIALS_W1_10/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

**[S111](SOURCES.md#S111) — CrowdPose, авторская статья.** Li et al., [полный HTML arXiv:1812.00324v2](https://arxiv.org/html/1812.00324v2), 23.01.2019; CVPR 2019, pp.10863–10872. Локально `CrowdPose.html`. Локаторы: Introduction/Fig.1, §4.1 Crowd Index, §4.3–4.4, §5.2–5.3. Окклюзии создают ошибки сборки точек разных людей и дубли скелетов; плотность людей не заменяет степень перекрытия. Это benchmark повседневных сцен с 14 точками; нет фабричной оценки и нет INT8 сравнения.

<a id="S112"></a>
## S112

Primary identity: https://arxiv.org/abs/1907.07484v2

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F125](RAW_FACTS.md#F125)

Происхождение: `W1-10-S05`, [W1-10](_WORK/W1_10.md), строка 23. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_10](_WORK/MATERIALS_W1_10/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

**[S112](SOURCES.md#S112) — Robust Detection Benchmark, авторская статья.** Michaelis et al., [полный arXiv:1907.07484v2](https://arxiv.org/html/1907.07484v2), 31.03.2020; первая версия 17.07.2019. Локально `RobustDetection.html`. Локаторы §2.1 Corruption types/Benchmark datasets/Metrics, §3.1, §3.6, Appendix A. Наборы PASCAL-C, COCO-C, Cityscapes-C, 15 типов искажений × 5 уровней; также отдельные driving данные. Здесь используем принцип раздельных видов/сил искажений, а не численные результаты как прогноз для завода.

<a id="S113"></a>
## S113

Primary identity: https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F126](RAW_FACTS.md#F126), [F127](RAW_FACTS.md#F127)

Происхождение: `W1-10-S06`, [W1-10](_WORK/W1_10.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_10](_WORK/MATERIALS_W1_10/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

**[S113](SOURCES.md#S113) — официальный cocoapi, исходный код evaluator.** [cocoeval.py, commit 8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py). Commit API получен; committer date 20.02.2020 17:25:28 UTC, не дата текущего доступа. Raw сохранён как `cocoapi_PythonAPI_pycocotools_cocoeval.py`, метаданные — `cocoapi_commit.json`. Локаторы: `computeOks` 192–233; `evaluateImg` 235+, `summarize` 473–485; `setDetParams` 502–511; `setKpParams` 513–523.

<a id="S114"></a>
## S114

Primary identity: https://github.com/open-mmlab/mmpose/releases/tag/v1.3.2

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F128](RAW_FACTS.md#F128), [F129](RAW_FACTS.md#F129)

Происхождение: `W1-10-S07`, [W1-10](_WORK/W1_10.md), строка 27. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_10](_WORK/MATERIALS_W1_10/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

**[S114](SOURCES.md#S114) — MMPose, исходный код.** Tag `v1.3.2`, [release note](https://github.com/open-mmlab/mmpose/releases/tag/v1.3.2), 12.07.2024, отображаемый short commit `5408bc7`. Проверены и сохранены [post_processing.py](https://github.com/open-mmlab/mmpose/blob/v1.3.2/mmpose/codecs/utils/post_processing.py), [refinement.py](https://github.com/open-mmlab/mmpose/blob/v1.3.2/mmpose/codecs/utils/refinement.py), [simcc_label.py](https://github.com/open-mmlab/mmpose/blob/v1.3.2/mmpose/codecs/simcc_label.py). Локаторы: `get_simcc_maximum` 41–105; `get_heatmap_maximum` 156–198; `refine_keypoints` 9–46; `refine_keypoints_dark` 49–102; `SimCCLabel.decode` 156–200. Полный commit API недоступен из-за rate limit; версия фиксирована tag, дата подтверждена release note. Эти codec-функции не означают, что любой RTMPose checkpoint использует одинаковые параметры.

<a id="S115"></a>
## S115

Primary identity: https://github.com/pytorch/vision/blob/v0.20.1/torchvision/models/_meta.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F130](RAW_FACTS.md#F130)

Происхождение: `W1-10-S08`, [W1-10](_WORK/W1_10.md), строка 29. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_10](_WORK/MATERIALS_W1_10/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

**[S115](SOURCES.md#S115) — torchvision, словарь классов.** Tag `v0.20.1`, [torchvision/models/_meta.py](https://github.com/pytorch/vision/blob/v0.20.1/torchvision/models/_meta.py), [raw](https://raw.githubusercontent.com/pytorch/vision/v0.20.1/torchvision/models/_meta.py), сохранён `torchvision_meta.py`. Локатор `_COCO_CATEGORIES`, строки 1011–1103, `cell phone` 1089. Дата релиза отдельно не проверена, не используется как аргумент новизны. Сам файл помечен private API: здесь читаем метаданные, не предлагаем импорт private переменной в продукт.

HTML и raw-код сохранены только для воспроизводимости чтения; список файлов и SHA256 — `MATERIALS_W1_10/SHA256.json`. Конец проверки по clock — 19:35:52 UTC (22:35:52 MSK). Источник реализации и соответствующая статья не являются независимыми подтверждениями одного эффекта.

<a id="S116"></a>
## S116

Primary identity: https://arxiv.org/abs/2110.06864v3

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F131](RAW_FACTS.md#F131), [F134](RAW_FACTS.md#F134)

Происхождение: `W1-11-S01`, [W1-11](_WORK/W1_11.md), строка 23. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_11](_WORK/MATERIALS_W1_11/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Zhang et al., [ByteTrack v3](https://arxiv.org/html/2110.06864v3), 2022-04-07; первая подача 2021-10-13

§3 BYTE; Appendix D, формула (1). [F131](RAW_FACTS.md#F131), [F134](RAW_FACTS.md#F134)

<a id="S117"></a>
## S117

Primary identity: https://github.com/FoundationVision/ByteTrack/blob/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/byte_tracker.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F132](RAW_FACTS.md#F132), [F133](RAW_FACTS.md#F133)

Происхождение: `W1-11-S02`, [W1-11](_WORK/W1_11.md), строка 24. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_11](_WORK/MATERIALS_W1_11/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

FoundationVision/ByteTrack, commit `d1bf0191adff59bc8fcfeaa0b33d3d1642552a99`; дата merge не установлена

[byte_tracker.py](https://github.com/FoundationVision/ByteTrack/blob/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/byte_tracker.py), `BYTETracker.__init__/update`, L146–181, L193–273; [kalman_filter.py](https://github.com/FoundationVision/ByteTrack/blob/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/kalman_filter.py), `KalmanFilter.__init__`, L40–48. [F132](RAW_FACTS.md#F132), [F133](RAW_FACTS.md#F133)

<a id="S118"></a>
## S118

Primary identity: https://arxiv.org/abs/2206.14651v2

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F135](RAW_FACTS.md#F135)

Происхождение: `W1-11-S03`, [W1-11](_WORK/W1_11.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_11](_WORK/MATERIALS_W1_11/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Aharon et al., [BoT-SORT v2](https://arxiv.org/html/2206.14651v2), 2022-07-07; первая подача 2022-06-29

§3.1–3.3, §4.4 Limitations. [F135](RAW_FACTS.md#F135)

<a id="S119"></a>
## S119

Primary identity: https://github.com/NirAharon/BoT-SORT/blob/251985436d6712aaf682aaaf5f71edb4987224bd/tracker/bot_sort.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F136](RAW_FACTS.md#F136)

Происхождение: `W1-11-S04`, [W1-11](_WORK/W1_11.md), строка 26. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_11](_WORK/MATERIALS_W1_11/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

NirAharon/BoT-SORT, commit `251985436d6712aaf682aaaf5f71edb4987224bd`, commit patch Date 2022-10-30

[bot_sort.py](https://github.com/NirAharon/BoT-SORT/blob/251985436d6712aaf682aaaf5f71edb4987224bd/tracker/bot_sort.py), `BoTSORT.__init__/update`, L203–231, L269–323, L414–418; [kalman_filter.py](https://github.com/NirAharon/BoT-SORT/blob/251985436d6712aaf682aaaf5f71edb4987224bd/tracker/kalman_filter.py), L41. [F136](RAW_FACTS.md#F136)

<a id="S120"></a>
## S120

Primary identity: https://github.com/FFmpeg/FFmpeg/blob/n8.0/libavutil/frame.h

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F137](RAW_FACTS.md#F137)

Происхождение: `W1-11-S05`, [W1-11](_WORK/W1_11.md), строка 27. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_11](_WORK/MATERIALS_W1_11/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

FFmpeg tag `n8.0`, tag ref `a4044e04486d1136022498891088a90baf5b2775`; точная дата тега не извлекалась

[libavutil/frame.h](https://github.com/FFmpeg/FFmpeg/blob/n8.0/libavutil/frame.h), L520–538, L687–692, поля `pts`, `pkt_dts`, `time_base`, `best_effort_timestamp`; [документация AVFrame 8.0](https://ffmpeg.org/doxygen/8.0/structAVFrame.html). [F137](RAW_FACTS.md#F137)

<a id="S121"></a>
## S121

Primary identity: https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/apis/inference_tracking.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F138](RAW_FACTS.md#F138)

Происхождение: `W1-11-S06`, [W1-11](_WORK/W1_11.md), строка 28. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_11](_WORK/MATERIALS_W1_11/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

OpenMMLab MMPose tag `v1.3.2`, ref `5408bc76f5b848cf925a0d1857899011d8c5b497`; дата релиза здесь не установлена

[inference_tracking.py](https://github.com/open-mmlab/mmpose/blob/v1.3.2/mmpose/apis/inference_tracking.py), `_track_by_iou`, L36–58; `_track_by_oks`, L60–97. [F138](RAW_FACTS.md#F138)

<a id="S122"></a>
## S122

Primary identity: https://github.com/activitynet/ActivityNet/blob/82304fa9f4a7219421df13dae6347a445c4cf5bc/Evaluation/eval_detection.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F139](RAW_FACTS.md#F139)

Происхождение: `W1-11-S07`, [W1-11](_WORK/W1_11.md), строка 29. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_11](_WORK/MATERIALS_W1_11/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ActivityNet, commit `82304fa9f4a7219421df13dae6347a445c4cf5bc`, commit patch Date 2021-01-06

[Evaluation/eval_detection.py](https://github.com/activitynet/ActivityNet/blob/82304fa9f4a7219421df13dae6347a445c4cf5bc/Evaluation/eval_detection.py), `compute_average_precision_detection`, L182–260; [utils.py](https://github.com/activitynet/ActivityNet/blob/82304fa9f4a7219421df13dae6347a445c4cf5bc/Evaluation/utils.py), `segment_iou`, L25–50. [F139](RAW_FACTS.md#F139)

<a id="S123"></a>
## S123

Primary identity: https://arxiv.org/abs/2009.07736v2

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F140](RAW_FACTS.md#F140)

Происхождение: `W1-11-S08`, [W1-11](_WORK/W1_11.md), строка 30. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_11](_WORK/MATERIALS_W1_11/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Luiten et al., [HOTA v2](https://arxiv.org/abs/2009.07736v2), 2020-09-29

Abstract: разделение detection, association, localization. [F140](RAW_FACTS.md#F140)

<a id="S124"></a>
## S124

Primary identity: https://docs.nvidia.com/deepstream/text/DS_plugin_gst-nvdsanalytics

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F141](RAW_FACTS.md#F141)

Происхождение: `W1-11-S09`, [W1-11](_WORK/W1_11.md), строка 31. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_11](_WORK/MATERIALS_W1_11/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

NVIDIA, [Gst-nvdsanalytics](https://docs.nvidia.com/deepstream/text/DS_plugin_gst-nvdsanalytics), страница объявляет версию **9.2**, дата публикации не указана

Вступление, Features, L27–30 и L55–58 текущего HTML. [F141](RAW_FACTS.md#F141). Это пример контракта event engine, не зависимость или возможность LinQ. URL архива 8.0 не получен браузерным инструментом; сведения 8.0 ему не приписываем

<a id="S125"></a>
## S125

Primary identity: https://github.com/microsoft/onnxruntime/blob/5c1b7ccbff7e5141c1da7a9d963d660e5741c319/onnxruntime/python/tools/quantization/qdq_loss_debug.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F143](RAW_FACTS.md#F143)

Происхождение: `W1-12-S02`, [W1-12](_WORK/W1_12.md), строка 20. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_12](_WORK/MATERIALS_W1_12/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [qdq_loss_debug.py v1.20.1, commit 5c1b7ccbff7e5141c1da7a9d963d660e5741c319](https://github.com/microsoft/onnxruntime/blob/5c1b7ccbff7e5141c1da7a9d963d660e5741c319/onnxruntime/python/tools/quantization/qdq_loss_debug.py). Дата commit не установлена: GitHub API 403 rate limit. `modify_model_output_intermediate_tensors` L64, `collect_activations` L115–165, `create_activation_matching` L180. [Копия](_WORK/MATERIALS_W1_12/qdq_loss_debug.py)

CODE. Augmentation меняет graph; API привязан к версии.

<a id="S126"></a>
## S126

Primary identity: https://github.com/cocodataset/cocoapi/blob/6c3b394c07aed33fd83784a8bf8798059a1e9ae4/PythonAPI/pycocotools/cocoeval.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F145](RAW_FACTS.md#F145), [F146](RAW_FACTS.md#F146)

Происхождение: `W1-12-S03`, [W1-12](_WORK/W1_12.md), строка 21. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_12](_WORK/MATERIALS_W1_12/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

COCO authors, [cocoeval.py commit 6c3b394c07aed33fd83784a8bf8798059a1e9ae4](https://github.com/cocodataset/cocoapi/blob/6c3b394c07aed33fd83784a8bf8798059a1e9ae4/PythonAPI/pycocotools/cocoeval.py), Toolbox 2.0; шапка 2015, дата commit не установлена (API 403). `evaluateImg` L235, `accumulate` L315, `computeOks` L192–233, `Params` L498–545. [Копия](_WORK/MATERIALS_W1_12/cocoeval.py)

CODE. Reference conventions, не установленный пакет; содержит `np.float`, нельзя обещать запуск с текущим NumPy.

<a id="S127"></a>
## S127

Primary identity: https://github.com/JonathonLuiten/TrackEval/blob/12c8791b303e0a0b50f753af204249e622d0281a/trackeval/metrics/hota.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F148](RAW_FACTS.md#F148)

Происхождение: `W1-12-S05`, [W1-12](_WORK/W1_12.md), строка 23. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_12](_WORK/MATERIALS_W1_12/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

TrackEval authors, [hota.py commit 12c8791b303e0a0b50f753af204249e622d0281a](https://github.com/JonathonLuiten/TrackEval/blob/12c8791b303e0a0b50f753af204249e622d0281a/trackeval/metrics/hota.py), дата commit не установлена (API 403); `eval_sequence`, `combine_sequences`, `_compute_final_fields`. [Копия](_WORK/MATERIALS_W1_12/hota.py)

CODE. Detection/association, не notification utility. Тоже содержит `np.float`.

<a id="S128"></a>
## S128

Primary identity: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F149](RAW_FACTS.md#F149)

Происхождение: `W1-12-S06`, [W1-12](_WORK/W1_12.md), строка 24. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_12](_WORK/MATERIALS_W1_12/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

SciPy, [bootstrap API](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html), открытая страница отображает **v1.18.0**, дата публикации неизвестна; `paired`, `method`, `rng`, Warns/Notes

DOC. Парность индексов, BCa degeneracy; не автоматическая поправка на видеокорреляцию.

<a id="S129"></a>
## S129

Primary identity: https://github.com/scipy/scipy/blob/527eb7fd7953a1de068f94bf8b322f249b9405ae/scipy/stats/_resampling.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F149](RAW_FACTS.md#F149)

Происхождение: `W1-12-S07`, [W1-12](_WORK/W1_12.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_12](_WORK/MATERIALS_W1_12/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

SciPy, [_resampling.py v1.17.1, commit 527eb7fd7953a1de068f94bf8b322f249b9405ae](https://github.com/scipy/scipy/blob/527eb7fd7953a1de068f94bf8b322f249b9405ae/scipy/stats/_resampling.py), API подтвердил committer date **2026-02-22T19:06:42Z**, release commit. `_bootstrap_resample` L74, `if paired` L214, warning L669. [Копия](_WORK/MATERIALS_W1_12/scipy_resampling.py)

CODE. Код и live docs разных версий; здесь не запускались.

<a id="S130"></a>
## S130

Primary identity: https://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015.pdf

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F150](RAW_FACTS.md#F150), [F250](RAW_FACTS.md#F250)

Происхождение: `W1-12-S08`, [W1-12](_WORK/W1_12.md), строка 26. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_12](_WORK/MATERIALS_W1_12/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

A. Colin Cameron, Douglas L. Miller, [A Practitioner's Guide to Cluster-Robust Inference](https://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015.pdf), JHR 50(2), 317–372, **2015**, author PDF; Introduction, VI.A, VI.C.3 (PDF с.25,29)

PUB. Регрессия; основание осторожности при few clusters, не гарантия CI для AP.

Происхождение: `W2-07-S05`, [W2-07](_WORK/W2_07.md), строка 17. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_07](_WORK/MATERIALS_W2_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Cameron & Miller, [A Practitioner's Guide to Cluster-Robust Inference](https://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015.pdf), JHR 50(2):317–372, **2015**; §VI.A PDF с.25–26, §VI.C.3 с.29

Published methodology; web PDF text получен заново; byte fetch failed WinError 10054. Screenshot вызван, usable image не получено: визуальная проверка этой статьи не заявляется. Не используем спорные таблицы/числа. Это regression theory, не готовый CI для AP/event matching.

<a id="S131"></a>
## S131

Primary identity: https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_debugger

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F151](RAW_FACTS.md#F151)

Происхождение: `W1-12-S09`, [W1-12](_WORK/W1_12.md), строка 27. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_12](_WORK/MATERIALS_W1_12/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Google AI Edge Authors, [Inspecting Quantization Errors with Quantization Debugger](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_debugger), Copyright 2024, **Last updated 2026-05-28 UTC**; Advanced usages → Custom metrics, Whole model verify mode; selective quantization limits

DOC. LiteRT/TFLite; переносится идея границ сравнения, не API/поддержка LinQ.

<a id="S132"></a>
## S132

Primary identity: LOCAL:W1-12-S11

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: контекст/ограничение в инженерных приложениях

Происхождение: `W1-12-S11`, [W1-12](_WORK/W1_12.md), строка 29. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_12](_WORK/MATERIALS_W1_12/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[Соседний evaluation report](../evaluation/report_machine_evaluation.md), checked_at выше; paired comparison, native/export/compiled parity, finite close

Вторичная навигация, не независимое первичное подтверждение.

<a id="S133"></a>
## S133

Primary identity: https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F153](RAW_FACTS.md#F153), [F154](RAW_FACTS.md#F154), [F155](RAW_FACTS.md#F155), [F156](RAW_FACTS.md#F156), [F157](RAW_FACTS.md#F157), [F158](RAW_FACTS.md#F158), [F159](RAW_FACTS.md#F159), [F172](RAW_FACTS.md#F172), [F173](RAW_FACTS.md#F173), [F174](RAW_FACTS.md#F174), [F177](RAW_FACTS.md#F177), [F178](RAW_FACTS.md#F178), [F183](RAW_FACTS.md#F183), [F184](RAW_FACTS.md#F184), [F185](RAW_FACTS.md#F185), [F186](RAW_FACTS.md#F186), [F187](RAW_FACTS.md#F187), [F197](RAW_FACTS.md#F197), [F198](RAW_FACTS.md#F198), [F199](RAW_FACTS.md#F199), [F200](RAW_FACTS.md#F200), [F201](RAW_FACTS.md#F201), [F202](RAW_FACTS.md#F202), [F205](RAW_FACTS.md#F205), [F212](RAW_FACTS.md#F212), [F213](RAW_FACTS.md#F213), [F214](RAW_FACTS.md#F214), [F217](RAW_FACTS.md#F217), [F219](RAW_FACTS.md#F219), [F220](RAW_FACTS.md#F220), [F221](RAW_FACTS.md#F221), [F222](RAW_FACTS.md#F222), [F223](RAW_FACTS.md#F223), [F224](RAW_FACTS.md#F224), [F238](RAW_FACTS.md#F238)

Происхождение: `W1-13-S01`, [W1-13](_WORK/W1_13.md), строка 23. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ООО «ХайТэк», guide 2025, RU.РМДВ.04.06.014-03 34 01. https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf

Свежий TinyFish fetch полного текстового извлечения; титул, §2 с.5–6; §3.1 с.7–9; §3.2 с.9–10; §3.3 с.11; пример с.11–21; термины с.25. PDF bytes web/urllib не получил: inaccessible / SSL EOF. **Визуального чтения PDF не было.** Соседний saved extraction проверен как дополнительный канал того же документа, не независимый источник. Титул пишет «Листов 28», extracted text заканчивается печатной с.27; точное число PDF-страниц здесь не утверждаем.

Происхождение: `W1-14-S01`, [W1-14](_WORK/W1_14.md), строка 19. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_14](_WORK/MATERIALS_W1_14/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ООО «ХайТэк», [Framework_manual_H1.pdf](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf), **2025, RU.РМДВ.04.06.014-03 34 01**; §3.1 с.7–8; §3.2 с.9–10; пример с.14–21

Сохранённый первичный текст `../research_link_platform/_WORK/W1_03/Framework_manual_H1_extracted.txt`, provenance: TinyFish extraction 2026-10-23. Копия в MATERIALS_W1_14. Новый web.open inaccessible, прямой HTTP TLS/connection failure; PDF bytes/скриншоты не получены. Это чтение извлечённого текста, не визуальный просмотр.

Происхождение: `W1-15-S01`, [W1-15](_WORK/W1_15.md), строка 23. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_15](_WORK/MATERIALS_W1_15/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[Framework manual H1](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf), 2025, RU.РМДВ.04.06.014-03 34 01, 28 листов

Web URL сейчас inaccessible. Прочитан сохранённый **первичный extracted text**, полученный соседней веткой через TinyFish: `../research_link_platform/_WORK/W1_03/Framework_manual_H1_extracted.txt`, provenance в первых двух строках. Не оригинальные PDF bytes и не визуальное чтение. С.17–21, текстовые строки 451–592, особенно 550–592. Это версия документа, не версия выданного SDK

Происхождение: `W2-01-S01`, [W2-01](_WORK/W2_01.md), строка 13. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_01](_WORK/MATERIALS_W2_01/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ООО «ХайТэк», [Framework_manual_H1.pdf](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf), титул2025, RU.РМДВ.04.06.014-03 34 01; exact wheel release отсутствует

Fresh TinyFish text, титул/§1.2.1 с.4/§2.1 с.5/§3.1 с.7–9/§3.2 с.9–10/§3.3 с.11/пример с.19–21. `MATERIALS_W2_01/Framework_manual_H1_fresh_extracted.txt`. Text extraction, не visual. Дата публикации неизвестна.

Происхождение: `W2-02-S12`, [W2-02](_WORK/W2_02.md), строка 28. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ООО «ХайТэк», [Framework_manual_H1.pdf](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf)

2025, RU.РМДВ.04.06.014-03 34 01; §3.3–3.4, печатные с.11,19–20; W1-14 extraction259–282,517–549

**Сохранённый первичный excerpt**, полученный W1 через TinyFish, не новый PDF fetch. Наш urllib SSL EOF; web inaccessible. PDF bytes нет, визуально таблицы/код не проверены. W2-01 сообщил свежий текст того же doc и те же signature/example seams; это не наша независимая visual verification.

Происхождение: `W2-03-S01`, [W2-03](_WORK/W2_03.md), строка 17. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_03](_WORK/MATERIALS_W2_03/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ООО «ХайТэк», [Framework_manual_H1.pdf](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf), 2025, RU.РМДВ.04.06.014-03 34 01, §3.1 с.7–8; локальный excerpt L129–180

**Saved primary text** из W1-14 `MATERIALS_W1_14/Framework_manual_H1_extracted.txt`; provenance W1: TinyFish extraction из соседнего linq_platform. Это не свежий fetch PDF. Свежий web.open inaccessible; прямой HTTPS завершился SSL UNEXPECTED_EOF. PDF bytes не получены, визуальной проверки спорной строки не было. Это access failure, не доказательство закрытости самого PDF.

Происхождение: `W2-05-S10`, [W2-05](_WORK/W2_05.md), строка 22. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_05](_WORK/MATERIALS_W2_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ООО «ХайТэк», [Framework manual2025](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf), RU.РМДВ.04.06.014-03 34 01, с.20–21; [docs index](https://lin-q.ru/docs) live

Guide — сохранённый primary extraction [W1 snapshot](_WORK/MATERIALS_W1_14/Framework_manual_H1_extracted.txt), не новый fetch guide. Docs index заново TinyFish: framework guide есть, отдельный version-matched runtime contract в прочитанных links не найден. Не доказательство отсутствия документа у поставщика.

<a id="S134"></a>
## S134

Primary identity: https://lin-q.ru/sol

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F170](RAW_FACTS.md#F170), [F172](RAW_FACTS.md#F172), [F174](RAW_FACTS.md#F174), [F184](RAW_FACTS.md#F184), [F197](RAW_FACTS.md#F197), [F205](RAW_FACTS.md#F205), [F218](RAW_FACTS.md#F218), [F219](RAW_FACTS.md#F219), [F220](RAW_FACTS.md#F220), [F221](RAW_FACTS.md#F221), [F222](RAW_FACTS.md#F222), [F223](RAW_FACTS.md#F223), [F224](RAW_FACTS.md#F224)

Происхождение: `W1-13-S02`, [W1-13](_WORK/W1_13.md), строка 24. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Официальная страница ПО и модулей, дата публикации неизвестна. https://lin-q.ru/sol

Web open/click: раздел ПО; отдельно раздел HX. Доступ к ПО после регистрации/верификации; Python3.8 API/CLI; связь имени IVA H1 с OEM LinQ H.

Происхождение: `W1-14-S05`, [W1-14](_WORK/W1_14.md), строка 23. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_14](_WORK/MATERIALS_W1_14/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ООО «ХайТэк», [LinQ software/products](https://lin-q.ru/sol), §§Программное обеспечение, LinQ HPS; live, дата обновления не объявлена

Страница заново открыта: DNN Quant/Graph Optimizer, последовательность quantization→compilation, Python3.8/CLI, доступ ПО после верификации. Vendor description, без version-specific quantizer spec.

Происхождение: `W2-01-S03`, [W2-01](_WORK/W2_01.md), строка 15. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_01](_WORK/MATERIALS_W2_01/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

LinQ, [ПО](https://lin-q.ru/sol#linq_soft), live без версии/даты

Fresh TinyFish section «Программное обеспечение»: Python3.8, доступ после регистрации и верификации. Не устанавливает release/runtime ABI. Metadata: `fresh_source_metadata.json`.

Происхождение: `W2-03-S03`, [W2-03](_WORK/W2_03.md), строка 19. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_03](_WORK/MATERIALS_W2_03/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ООО «ХайТэк», [ПО LinQ](https://lin-q.ru/sol), §Программное обеспечение, web L273–289; [LinQ technology](https://lin-q.ru/tech), IP-ядро L45–53

**Fresh vendor pages** открыты web; дата публикации/редакция не объявлены. Quantization→compile, Python API/CLI и int8 claim; страница ПО сообщает верификацию аккаунта для скачивания. Не numerical/compiler contract. Прямой urllib HTTPS этих страниц дал SSL error, хотя web чтение удалось.

<a id="S135"></a>
## S135

Primary identity: https://lin-q.ru/tech

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F172](RAW_FACTS.md#F172), [F174](RAW_FACTS.md#F174), [F184](RAW_FACTS.md#F184), [F212](RAW_FACTS.md#F212)

Происхождение: `W1-13-S03`, [W1-13](_WORK/W1_13.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Официальный технологический стек, дата неизвестна. https://lin-q.ru/tech

Web: «Поддерживаемые сети», «Оригинальный framework». Список семейств и общая схема, без версионной матрицы операторов.

Происхождение: `W1-14-S06`, [W1-14](_WORK/W1_14.md), строка 24. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_14](_WORK/MATERIALS_W1_14/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ООО «ХайТэк», [технологии LinQ H](https://lin-q.ru/tech), §§IP-ядро, Поддерживаемые сети; live, дата не объявлена

Страница заново открыта: int8, семейства yolo8/yolo11. Это уровень семейства/рекламируемой возможности, не operator matrix и не подтверждение конкретного head/custom nc.

Происхождение: `W2-02-S16`, [W2-02](_WORK/W2_02.md), строка 32. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ООО «ХайТэк», [технологии](https://lin-q.ru/tech)

live страница, web lines58–107, дата публикации неизвестна

Web content открыт 2026-10-23; family list yolo8/yolo11 не содержит importer build/opset/mapping definition. Shell TLS failure этой страницы — ограничение транспорта, не закрытость страницы.

<a id="S136"></a>
## S136

Primary identity: https://lin-q.ru/docs

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F172](RAW_FACTS.md#F172), [F205](RAW_FACTS.md#F205)

Происхождение: `W1-13-S04`, [W1-13](_WORK/W1_13.md), строка 26. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Официальный каталог docs, дата неизвестна. https://lin-q.ru/docs

Свежий TinyFish text + links: hardware manuals, framework guide [S133](SOURCES.md#S133). Прямой web open недоступен. Из просмотренных ссылок release notes/operator matrix не установлены; полноту всех ресурсов компании не утверждаем.

Происхождение: `W2-01-S02`, [W2-01](_WORK/W2_01.md), строка 14. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_01](_WORK/MATERIALS_W2_01/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

LinQ, [каталог документации](https://lin-q.ru/docs), live без версии/даты публикации

Fresh TinyFish text+links: единственная найденная ссылка на Framework guide ведёт к [S133](SOURCES.md#S133). В полученном списке нет release notes/таблицы миграции. Это граница данного каталога, не утверждение об отсутствии закрытых документов. Metadata/links: `fresh_source_metadata.json`.

<a id="S137"></a>
## S137

Primary identity: https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F169](RAW_FACTS.md#F169), [F172](RAW_FACTS.md#F172), [F174](RAW_FACTS.md#F174), [F184](RAW_FACTS.md#F184), [F185](RAW_FACTS.md#F185), [F237](RAW_FACTS.md#F237)

Происхождение: `W1-13-S05`, [W1-13](_WORK/W1_13.md), строка 27. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Официальная презентация 2026, author metadata Сергей Севрюков; точная дата публикации неизвестна. https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf

Свежий TinyFish text; блок «Производительность» (соседний источник локализует как с.4), подпись Runtime16.18.6 / Framework2026.8.43; список сетей; PyTorch через ONNX. Официальный https://lin-q.ru/press содержит ссылку. PDF bytes не получены, таблица визуально здесь не читалась.

Происхождение: `W1-14-S09`, [W1-14](_WORK/W1_14.md), строка 27. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_14](_WORK/MATERIALS_W1_14/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ООО «ХайТэк», [презентация 2026](https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf), с.4, примечание benchmark; **2026**, точная дата публикации не установлена

Прочитано сохранённое первичное TinyFish text extraction `../research_link_platform/_WORK/W1_08/presentation2026_tinyfish.json`. В нём Runtime16.18.6 / Framework2026.8.43 / Ubuntu24.04. Наш web.open inaccessible. Числа качества/скорости из неё здесь не используются.

Происхождение: `W1-15-S06`, [W1-15](_WORK/W1_15.md), строка 28. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_15](_WORK/MATERIALS_W1_15/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[Официальная презентация LinQ 2026](https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf)

Попытка web доступа inaccessible; собственной свежей проверки содержимого нет. Версии benchmark из соседних выписок не принимаются за версии сервера; не используются как доказательство выданной среды

Происхождение: `W2-05-S08`, [W2-05](_WORK/W2_05.md), строка 20. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_05](_WORK/MATERIALS_W2_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ООО «ХайТэк», [presentation2026](https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf), блок «Производительность», строка сети и сноска (W1 локализует как с.4)

Свежий TinyFish extracted text, [snapshot](_WORK/MATERIALS_W2_05/tinyfish_presentation_docs.json); author metadata Сергей Севрюков, published_date=null. Web inaccessible и прямой bytes TLS EOF. **PDF bytes не получены; визуальная проверка таблицы/сноски не выполнена.** Это extraction primary source, не собственный rerun.

<a id="S138"></a>
## S138

Primary identity: https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/export_yolov8s_to_onnx.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F160](RAW_FACTS.md#F160), [F172](RAW_FACTS.md#F172), [F174](RAW_FACTS.md#F174), [F182](RAW_FACTS.md#F182), [F184](RAW_FACTS.md#F184)

Происхождение: `W1-13-S06`, [W1-13](_WORK/W1_13.md), строка 28. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Павел Шерстнев / sherstpasha, linq-cv-bench, commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`, 2026-04-03 12:44:54 +0700. https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/export_yolov8s_to_onnx.py

Повторно получен raw HTTP200; parse_args L13–23; model.export L62–72; metadata L78–89. Commit/date проверены локальным git show pinned соседнего checkout; GitHub API попытка дала rate-limit403.

Происхождение: `W1-14-S04`, [W1-14](_WORK/W1_14.md), строка 22. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_14](_WORK/MATERIALS_W1_14/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Тот же commit, [export_yolov8s_to_onnx.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/export_yolov8s_to_onnx.py); `main`, `model.export(...nms=False)`

Raw заново получен, прочитан; SHA256 `a3decdc38ecf864c725cbf52b101102ac2f7e71c0ec62a84f675425dfd736b22`. Дата commit 2026-04-03T05:44:54Z прочитана в сохранённом первичном GitHub API `../research_link_platform/_WORK/W2_F/COMMITS.TXT`. Наша свежая API попытка 403; это не независимая сетевая проверка даты.

<a id="S139"></a>
## S139

Primary identity: https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/build_yolov8_program.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F158](RAW_FACTS.md#F158), [F161](RAW_FACTS.md#F161), [F162](RAW_FACTS.md#F162), [F163](RAW_FACTS.md#F163), [F164](RAW_FACTS.md#F164), [F172](RAW_FACTS.md#F172), [F174](RAW_FACTS.md#F174), [F175](RAW_FACTS.md#F175), [F176](RAW_FACTS.md#F176), [F177](RAW_FACTS.md#F177), [F183](RAW_FACTS.md#F183), [F184](RAW_FACTS.md#F184), [F199](RAW_FACTS.md#F199), [F200](RAW_FACTS.md#F200), [F201](RAW_FACTS.md#F201), [F202](RAW_FACTS.md#F202), [F205](RAW_FACTS.md#F205), [F212](RAW_FACTS.md#F212), [F213](RAW_FACTS.md#F213), [F215](RAW_FACTS.md#F215), [F217](RAW_FACTS.md#F217), [F219](RAW_FACTS.md#F219), [F220](RAW_FACTS.md#F220), [F221](RAW_FACTS.md#F221), [F222](RAW_FACTS.md#F222), [F223](RAW_FACTS.md#F223), [F224](RAW_FACTS.md#F224)

Происхождение: `W1-13-S07`, [W1-13](_WORK/W1_13.md), строка 29. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Тот же commit, build YOLOv8s. https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/build_yolov8_program.py

Raw HTTP200; static shape L98–111; converter retries L114–139; preset L170–181; main L191–339; calibration L275–281; compile L288–301; summary L304–325.

Происхождение: `W1-14-S02`, [W1-14](_WORK/W1_14.md), строка 20. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_14](_WORK/MATERIALS_W1_14/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

sherstpasha, [build_yolov8_program.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/build_yolov8_program.py), commit **3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140**; L18–31,38–108,113–138,169–181,214–325

Raw заново скачан HTTP, прочитан, SHA256 `db6aea75d43827b7f21a87585c2d2b86e88fadbaf5179da778d8fad4cd48d0bf`. Сторонний код, не официальный quantizer implementation.

Происхождение: `W2-01-S07`, [W2-01](_WORK/W2_01.md), строка 19. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_01](_WORK/MATERIALS_W2_01/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Павел Шерстнев, [build_yolov8_program.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/build_yolov8_program.py), commit3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140, 2026-04-03 по W1 git metadata

Сохранённый pinned primary source из `../MATERIALS_W1_13/build_yolov8_program.py`, повторно прочитан; в W2 заново по сети не получался. L169–181 presets; L274–292 calibration/save/network; L294–299 target. Сторонний код без exact Framework pin, не vendor migration note и не наш запуск.

Происхождение: `W2-02-S13`, [W2-02](_WORK/W2_02.md), строка 29. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Павел Шерстнев / sherstpasha, [build_yolov8_program.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/build_yolov8_program.py)

commit3ad1b7…a140; 98–139,151–156,216–272,285–297

Новый raw200; SHA256 `db6aea75d43827b7f21a87585c2d2b86e88fadbaf5179da778d8fad4cd48d0bf`, совпадает W1. **Сторонний** example, не source самого converter.

Происхождение: `W2-03-S02`, [W2-03](_WORK/W2_03.md), строка 18. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_03](_WORK/MATERIALS_W2_03/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

sherstpasha, [build_yolov8_program.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/build_yolov8_program.py#L275), commit **3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140**, L275–281,304–325

**Fresh static code**; SHA совпадает W1-14. Сторонний клиент SDK, не quantizer implementation производителя. Не содержит wheel/native version lock достаточный для связи с guide.

<a id="S140"></a>
## S140

Primary identity: https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/RUN_SCENARIO.txt

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F167](RAW_FACTS.md#F167), [F172](RAW_FACTS.md#F172), [F234](RAW_FACTS.md#F234), [F235](RAW_FACTS.md#F235), [F236](RAW_FACTS.md#F236)

Происхождение: `W1-13-S09`, [W1-13](_WORK/W1_13.md), строка 31. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Тот же commit, RUN_SCENARIO, внутренняя дата текста 2026-03-25. https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/RUN_SCENARIO.txt

Raw HTTP200; §§1–3, «Final TPU plan», «Current completion status»: сам автор финальным TPU detection называет vendor TinyYOLO3, не self-build YOLOv8.

Происхождение: `W2-05-S01`, [W2-05](_WORK/W2_05.md), строка 13. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_05](_WORK/MATERIALS_W2_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[RUN_SCENARIO](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/RUN_SCENARIO.txt), автор sherstpasha; внутренняя дата 2026-03-25; §§3.1–3.5,5,8

Свежий HTTP200 raw, [scenario.txt](_WORK/MATERIALS_W2_05/scenario.txt), SHA256 `39eac9f06cfed3592ad5e077b865d812ffffa195d9428c8854dbc27d926f4446`. История commit заново получена GitHub connector: author/committer date 2026-04-03T05:44:54Z; §8 добавлен этим commit. Внутренняя дата текста не дата всех добавлений.

<a id="S141"></a>
## S141

Primary identity: https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/README.md

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F168](RAW_FACTS.md#F168), [F172](RAW_FACTS.md#F172)

Происхождение: `W1-13-S10`, [W1-13](_WORK/W1_13.md), строка 32. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Тот же commit, detection README. https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/README.md

Raw HTTP200; vendor path и указанный автором контракт `.tpu`, отдельные зависимости TPU/strict export/CPU-CUDA.

<a id="S142"></a>
## S142

Primary identity: https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/requirements.txt

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F172](RAW_FACTS.md#F172)

Происхождение: `W1-13-S11`, [W1-13](_WORK/W1_13.md), строка 33. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Тот же commit, requirements. https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/requirements.txt

Raw HTTP200, L1–11: numpy1.26.4, onnx~=1.16.0, onnxruntime~=1.18.0, TensorFlow2.14.1; torch/torchvision unpinned. Ultralytics и exact TPU packages не закреплены.

<a id="S143"></a>
## S143

Primary identity: https://pypi.org/project/pytpu/15.0.21/

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F171](RAW_FACTS.md#F171), [F172](RAW_FACTS.md#F172)

Происхождение: `W1-13-S12`, [W1-13](_WORK/W1_13.md), строка 34. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

IVA-Tech PyPI pytpu15.0.21; релиз 2023-10-30. https://pypi.org/project/pytpu/15.0.21/

Открыты metadata и Example; текст всё ещё показывает `iva_tpu`, TPUDevice/TPUProgram/TPUInference. Это историческая документация пакета, не API Runtime16.

<a id="S144"></a>
## S144

Primary identity: https://pypi.org/project/iva-tpu/11.2.6/

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F171](RAW_FACTS.md#F171), [F172](RAW_FACTS.md#F172)

Происхождение: `W1-13-S13`, [W1-13](_WORK/W1_13.md), строка 35. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_13](_WORK/MATERIALS_W1_13/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

IVA-Tech PyPI iva-tpu11.2.6; релиз 2021-08-31. https://pypi.org/project/iva-tpu/11.2.6/

Открыты metadata и Example; load_tensors/get_tensors, старый объектный интерфейс.

<a id="S145"></a>
## S145

Primary identity: https://pypi.org/project/pytpu/15.0.24/

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F174](RAW_FACTS.md#F174), [F179](RAW_FACTS.md#F179), [F184](RAW_FACTS.md#F184), [F238](RAW_FACTS.md#F238), [F239](RAW_FACTS.md#F239)

Происхождение: `W1-14-S07`, [W1-14](_WORK/W1_14.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_14](_WORK/MATERIALS_W1_14/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

IvaTechnologies, [pytpu 15.0.24](https://pypi.org/project/pytpu/15.0.24/), релиз **2023-11-27**; `_bindings.py` L165–169,373–408,427–518

PyPI заново открыт; исходник прочитан из сохранённого sdist `../research_link_platform/_WORK/W1_13/SOURCE/pytpu-15.0.24/pytpu/_bindings.py`, копия в своих MATERIALS. Не устанавливался/не импортировался. Исторический Python binding, native implementation и совместимость с 2026 неизвестны.

Происхождение: `W2-05-S09`, [W2-05](_WORK/W2_05.md), строка 21. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_05](_WORK/MATERIALS_W2_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

IVA-Tech, [PyPI pytpu15.0.24](https://pypi.org/project/pytpu/15.0.24/), 2023-11-27; [JSON metadata](https://pypi.org/pypi/pytpu/15.0.24/json), sdist `pytpu-15.0.24.tar.gz`

Свежий sdist200; SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f` совпал с PyPI. Без установки/импорта; извлечены только `.py`/README. `_bindings.py` L165–169,373–425,427–518; `_converter_to_raw.py` L29–40,63–140.

<a id="S146"></a>
## S146

Primary identity: https://pypi.org/project/iva-applications/11.0.1/

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F174](RAW_FACTS.md#F174), [F180](RAW_FACTS.md#F180), [F184](RAW_FACTS.md#F184)

Происхождение: `W1-14-S08`, [W1-14](_WORK/W1_14.md), строка 26. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_14](_WORK/MATERIALS_W1_14/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

IVA Technologies, [iva-applications 11.0.1](https://pypi.org/project/iva-applications/11.0.1/), релиз **2021-10-13**; `src/iva_applications/dequantization.py` L6–39

PyPI заново открыт; полный helper прочитан из соседнего сохранённого sdist, копия в своих MATERIALS. Старый FPGA scale/shift helper; не текущий `.tpu` contract.

<a id="S147"></a>
## S147

Primary identity: https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/coco_utils.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F192](RAW_FACTS.md#F192)

Происхождение: `W1-15-S03`, [W1-15](_WORK/W1_15.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_15](_WORK/MATERIALS_W1_15/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[coco_utils.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/coco_utils.py), тот же SHA

Свежий raw HTTP, [локальная копия](_WORK/MATERIALS_W1_15/coco_utils.py); `letterbox`, строки 19–38

<a id="S148"></a>
## S148

Primary identity: https://github.com/FFmpeg/FFmpeg/blob/n8.0/doc/ffprobe.texi

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F194](RAW_FACTS.md#F194)

Происхождение: `W1-15-S04`, [W1-15](_WORK/W1_15.md), строка 26. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_15](_WORK/MATERIALS_W1_15/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[FFmpeg ffprobe n8.0 source documentation](https://github.com/FFmpeg/FFmpeg/blob/n8.0/doc/ffprobe.texi), tag n8.0

Свежий raw HTTP, [локальная копия](_WORK/MATERIALS_W1_15/ffprobe_n8.0.texi). Строки 104–116, 130–149, 193–219, 240–283. Дата release отдельно не проверена; это документ tag, не установленная версия FFmpeg. ffmpeg.org page дважды timeout

<a id="S149"></a>
## S149

Primary identity: https://onnxruntime.ai/docs/api/python/api_summary.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F195](RAW_FACTS.md#F195)

Происхождение: `W1-15-S05`, [W1-15](_WORK/W1_15.md), строка 27. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W1_15](_WORK/MATERIALS_W1_15/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[ONNX Runtime Python API](https://onnxruntime.ai/docs/api/python/api_summary.html), текущая web documentation, точный release страницы не указан

Прочитаны Load and run a model / Data inputs and outputs / InferenceSession, включая provider precedence, default CPU I/O, profiling. Это пример для **ORT baseline/сервиса, только если он действительно ORT**, не API LinQ

<a id="S150"></a>
## S150

Primary identity: https://pypi.org/pypi/pytpu/json

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F197](RAW_FACTS.md#F197), [F203](RAW_FACTS.md#F203), [F205](RAW_FACTS.md#F205)

Происхождение: `W2-01-S04`, [W2-01](_WORK/W2_01.md), строка 16. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_01](_WORK/MATERIALS_W2_01/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

IVA-Tech, [PyPI pytpu JSON](https://pypi.org/pypi/pytpu/json); latest field15.0.24, release upload2023-11-27T09:41:37.939987Z

HTTP200 JSON, поля info.version/requires_python/home_page и releases15.0.24. Сохранён `pytpu.json`; URL/hash исходного архива — `sdist_provenance.json`. `requires_python=>=3.6`, не Python3.8 pin.

<a id="S151"></a>
## S151

Direct archived distribution: [pytpu-15.0.24.tar.gz](https://files.pythonhosted.org/packages/bd/9a/ee7cc0a40291dcb7ef399d30b80892909c3add5e3a0ebf1bc04a8c97f0ba/pytpu-15.0.24.tar.gz); upload 2023-11-27T09:41:37.939987Z, SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`. Provenance: [_WORK/MATERIALS_W2_01/sdist_provenance.json](_WORK/MATERIALS_W2_01/sdist_provenance.json).

Primary identity: LOCAL:W2-01-S05

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F197](RAW_FACTS.md#F197), [F203](RAW_FACTS.md#F203), [F204](RAW_FACTS.md#F204), [F205](RAW_FACTS.md#F205)

Происхождение: `W2-01-S05`, [W2-01](_WORK/W2_01.md), строка 17. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_01](_WORK/MATERIALS_W2_01/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

IVA-Tech, sdist `pytpu-15.0.24.tar.gz`, URL и SHA256 из [S150](SOURCES.md#S150); исторический publisher source

Архив прочитан в памяти, без установки/исполнения setup.py. SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f` совпал с PyPI digest. Сохранены `pytpu_15_0_24_setup.py`, `pytpu_15_0_24_PKG-INFO`, `pytpu_15_0_24__bindings.py`. Локаторы ниже — номера строк сохранённого исходника.

<a id="S152"></a>
## S152

Primary identity: https://pypi.org/pypi/iva-tpu/json

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F205](RAW_FACTS.md#F205)

Происхождение: `W2-01-S06`, [W2-01](_WORK/W2_01.md), строка 18. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_01](_WORK/MATERIALS_W2_01/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

PyPI [iva-tpu JSON](https://pypi.org/pypi/iva-tpu/json); author metadata Maxim Moroz; latest11.2.6

Fresh HTTP200, `iva-tpu.json`: Python>=3.6, homepage того же IVA SDK проекта. Исторический runtime package, не Framework2026 manifest.

<a id="S153"></a>
## S153

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/engine/predictor.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F207](RAW_FACTS.md#F207), [F211](RAW_FACTS.md#F211)

Происхождение: `W2-02-S04`, [W2-02](_WORK/W2_02.md), строка 20. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [predictor.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/engine/predictor.py#L151), [model.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/engine/model.py#L527)

preprocess151–173, pre_transform193–201; model.predict defaults527

Raw200. Wrapper arguments могут изменять поведение; здесь они задаются явно.

<a id="S154"></a>
## S154

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/data/augment.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F207](RAW_FACTS.md#F207), [F211](RAW_FACTS.md#F211)

Происхождение: `W2-02-S05`, [W2-02](_WORK/W2_02.md), строка 21. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [augment.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/data/augment.py#L1568)

LetterBox1568–1608,1638–1692

Raw200. Defaults и image path, не bit-exact обещание любой OpenCV версии.

<a id="S155"></a>
## S155

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/utils/ops.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F210](RAW_FACTS.md#F210), [F211](RAW_FACTS.md#F211)

Происхождение: `W2-02-S07`, [W2-02](_WORK/W2_02.md), строка 23. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [ops.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/utils/ops.py)

scale_boxes102–134; clip_boxes152–177,clip_coords180–205; scale_coords554–586

Raw200. Default inverse для centered letterbox; не общий inverse crop/stretch.

<a id="S156"></a>
## S156

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/models/yolo/detect/predict.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F209](RAW_FACTS.md#F209), [F210](RAW_FACTS.md#F210), [F211](RAW_FACTS.md#F211)

Происхождение: `W2-02-S08`, [W2-02](_WORK/W2_02.md), строка 24. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [detect/predict.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/models/yolo/detect/predict.py), [pose/predict.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/models/yolo/pose/predict.py)

Detect54–65,108–121; Pose54–77

Raw200. Post-NMS construction/inverse, без tracker.

<a id="S157"></a>
## S157

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/tasks.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F206](RAW_FACTS.md#F206), [F208](RAW_FACTS.md#F208)

Происхождение: `W2-02-S09`, [W2-02](_WORK/W2_02.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [tasks.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/tasks.py#L219), [torch_utils.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/utils/torch_utils.py#L236), [block.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/modules/block.py), [tal.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/utils/tal.py#L352)

fuse219–260; ConvBN236–268; DFL58–79, C2f303–314; anchors352–364, dist2bbox367–376

Raw200. Все внутренние helpers той же версии.

<a id="S158"></a>
## S158

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/cfg/models/v8/yolov8.yaml

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F208](RAW_FACTS.md#F208)

Происхождение: `W2-02-S10`, [W2-02](_WORK/W2_02.md), строка 26. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [YOLOv8 config](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/cfg/models/v8/yolov8.yaml), [Pose config](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/cfg/models/v8/yolov8-pose.yaml)

P3/8,P4/16,P5/32, конечные Detect/Pose

Raw200. Дефолтные nc80/1 и K17×3 — свойства configs, не custom manifest.

<a id="S159"></a>
## S159

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/engine/results.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F210](RAW_FACTS.md#F210), [F211](RAW_FACTS.md#F211)

Происхождение: `W2-02-S11`, [W2-02](_WORK/W2_02.md), строка 27. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [results.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/engine/results.py#L1161), [v8.3.0 results.py](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/engine/results.py#L1306)

New Keypoints1177–1180,xy1203; old1306–1312

Обе raw200. Наблюдается расхождение docstring/code в новой версии; не исполнено.

<a id="S160"></a>
## S160

Primary identity: https://github.com/onnx/onnx/blob/3bf92c03a9f27eba3bda1e5b9e63ea20ec213557/onnx/onnx.proto

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F213](RAW_FACTS.md#F213)

Происхождение: `W2-02-S14`, [W2-02](_WORK/W2_02.md), строка 30. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ONNX maintainers [onnx.proto](https://github.com/onnx/onnx/blob/3bf92c03a9f27eba3bda1e5b9e63ea20ec213557/onnx/onnx.proto#L189), [IR.md](https://github.com/onnx/onnx/blob/3bf92c03a9f27eba3bda1e5b9e63ea20ec213557/docs/IR.md#L264)

ONNX1.16.2 commit3bf92c…3557, ValueInfo189–191, Node208–214; IR namespaces264–285

Raw200; поясняет name/port contract. Не устанавливает accepted ONNX version LinQ.

<a id="S161"></a>
## S161

Primary identity: https://github.com/tensorflow/tensorflow/blob/v2.15.1/tensorflow/python/framework/ops.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F213](RAW_FACTS.md#F213)

Происхождение: `W2-02-S15`, [W2-02](_WORK/W2_02.md), строка 31. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_02](_WORK/MATERIALS_W2_02/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

TensorFlow authors [ops.py v2.15.1](https://github.com/tensorflow/tensorflow/blob/v2.15.1/tensorflow/python/framework/ops.py#L2949)

Graph.get_operation_by_name/get_tensor_by_name2949–2994, as_graph_element2860+

Raw200, tag-specific API example, **не версия выданного LinQ TensorFlow**. Разные APIs для operation и tensor.

<a id="S162"></a>
## S162

Primary identity: https://github.com/microsoft/onnxconverter-common/blob/v1.16.0/onnxconverter_common/auto_mixed_precision_model_path.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F216](RAW_FACTS.md#F216), [F226](RAW_FACTS.md#F226)

Происхождение: `W2-03-S05`, [W2-03](_WORK/W2_03.md), строка 21. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_03](_WORK/MATERIALS_W2_03/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [auto_mixed_precision_model_path.py](https://github.com/microsoft/onnxconverter-common/blob/v1.16.0/onnxconverter_common/auto_mixed_precision_model_path.py#L22), **v1.16.0**, L22–32,60–62,105–117,183–203,240–282

**Fresh static code**, SHA `425277…830c3`; отдельный API с required `provider`; он передаётся FP32 baseline и FP16 trial sessions. Не доказательство работоспособности любой модели/платформы.

<a id="S163"></a>
## S163

Primary identity: https://github.com/microsoft/onnxconverter-common/blob/v1.16.0/requirements.txt

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F229](RAW_FACTS.md#F229)

Происхождение: `W2-03-S06`, [W2-03](_WORK/W2_03.md), строка 22. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_03](_WORK/MATERIALS_W2_03/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [requirements.txt](https://github.com/microsoft/onnxconverter-common/blob/v1.16.0/requirements.txt), **v1.16.0**, обе строки; [setup.py](https://github.com/microsoft/onnxconverter-common/blob/v1.16.0/setup.py), requirements/install_requires

**Fresh static metadata**: `onnx>=1.18.0`, packaging; ORT не pinned runtime dependency. Delayed import ORT в [S101](SOURCES.md#S101)/S05. По версии converter нельзя восстановить версию ORT.

<a id="S164"></a>
## S164

Primary identity: https://github.com/microsoft/onnxruntime/blob/v1.23.2/docs/OperatorKernels.md

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F227](RAW_FACTS.md#F227)

Происхождение: `W2-03-S07`, [W2-03](_WORK/W2_03.md), строка 23. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_03](_WORK/MATERIALS_W2_03/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [OperatorKernels.md](https://github.com/microsoft/onnxruntime/blob/v1.23.2/docs/OperatorKernels.md), **ORT v1.23.2**, CPU Cast L62+, Conv L85–87, MatMul L233+; CUDA Conv L645+, MatMul L747+

**Fresh generated kernel documentation**. Таблица описывает registered kernels, не итоговый execution graph. Статически прочитана, конкретный wheel/build/hardware не проверен.

<a id="S165"></a>
## S165

Primary identity: https://github.com/microsoft/onnxruntime/blob/v1.23.2/onnxruntime/core/optimizer/insert_cast_transformer.cc

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F227](RAW_FACTS.md#F227), [F228](RAW_FACTS.md#F228)

Происхождение: `W2-03-S08`, [W2-03](_WORK/W2_03.md), строка 24. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_03](_WORK/MATERIALS_W2_03/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Microsoft, [insert_cast_transformer.cc](https://github.com/microsoft/onnxruntime/blob/v1.23.2/onnxruntime/core/optimizer/insert_cast_transformer.cc), **ORT v1.23.2**, `NeedInsertCast` L17–26, `IsIsolatedFp16NodeOnCpu`, `ApplyImpl` L457+

**Fresh static runtime code**: предусмотрена вставка casts для не назначенного EP узла с FP16 input без subgraph, перенос вычисления к FP32 CPU; есть оптимизация casts. Это механизм, а не наш выполненный результат.

<a id="S166"></a>
## S166

Primary identity: https://github.com/yhhhli/BRECQ/blob/e455d62e93c70351961f8991c913b59435bd165f/README.md

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F231](RAW_FACTS.md#F231)

Происхождение: `W2-04-S03`, [W2-04](_WORK/W2_04.md), строка 13. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_04](_WORK/MATERIALS_W2_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Авторы BRECQ, [README at e455d62](https://github.com/yhhhli/BRECQ/blob/e455d62e93c70351961f8991c913b59435bd165f/README.md)

Секция Usage, фактически прочитан [immutable snapshot](_WORK/MATERIALS_W2_04/brecq_e455d62_README.md); HEAD независимо получен git ls-remote

Reported example output, не наш запуск; дата commit не установлена

<a id="S167"></a>
## S167

Primary identity: https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/docs/en/03-benchmark/benchmark.md

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F232](RAW_FACTS.md#F232)

Происхождение: `W2-04-S04`, [W2-04](_WORK/W2_04.md), строка 14. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_04](_WORK/MATERIALS_W2_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

OpenMMLab, [MMDeploy v1.3.1 benchmark source](https://github.com/open-mmlab/mmdeploy/blob/v1.3.1/docs/en/03-benchmark/benchmark.md)

Accuracy benchmark / mmdet / YOLOX, Notes; HTML headers разобраны вместе со строкой, [snapshot](_WORK/MATERIALS_W2_04/mmdeploy_v1.3.1_benchmark.md)

Не переносить latency platform на accuracy run; config links внутри документа mutable

<a id="S168"></a>
## S168

Primary identity: https://github.com/open-mmlab/mmdeploy/blob/c73756366e374507b5d619cfe06deea72d2ad61d/docs/en/03-benchmark/quantization.md

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F233](RAW_FACTS.md#F233)

Происхождение: `W2-04-S05`, [W2-04](_WORK/W2_04.md), строка 15. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_04](_WORK/MATERIALS_W2_04/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

OpenMMLab, [MMDeploy v0.14.0 quantization source](https://github.com/open-mmlab/mmdeploy/blob/v0.14.0/docs/en/03-benchmark/quantization.md), также [rendered docs](https://mmdeploy.readthedocs.io/en/0.x/03-benchmark/quantization.html)

Quantize with ncnn / Pose detection / note flip_test; raw tag и HTML прочитаны, [snapshot](_WORK/MATERIALS_W2_04/mmdeploy_v0.14.0_quantization.md)

Старый стек 0.x; не современный MMPose1.x/LinQ recipe

<a id="S169"></a>
## S169

Primary identity: https://api.github.com/repos/sherstpasha/linq-cv-bench/git/trees/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140?recursive=1

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F234](RAW_FACTS.md#F234), [F235](RAW_FACTS.md#F235), [F236](RAW_FACTS.md#F236)

Происхождение: `W2-05-S02`, [W2-05](_WORK/W2_05.md), строка 14. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_05](_WORK/MATERIALS_W2_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[recursive tree PIN](https://api.github.com/repos/sherstpasha/linq-cv-bench/git/trees/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140?recursive=1), [main tree](https://api.github.com/repos/sherstpasha/linq-cv-bench/git/trees/main?recursive=1), [releases](https://api.github.com/repos/sherstpasha/linq-cv-bench/releases), [Actions](https://api.github.com/repos/sherstpasha/linq-cv-bench/actions/runs?per_page=10)

Свежий API200: оба tree совпадают побайтово, `truncated=false`; releases=[]; Actions `total_count=0`. [GitHub connector checks](_WORK/MATERIALS_W2_05/github_connector_checks.json). Tags connector отказал по allowlist: это tool limitation, не доказательство отсутствия tags. Не просмотрены все исторические деревья, внешние диски/закрытые приложения автора.

<a id="S170"></a>
## S170

Primary identity: https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/.gitignore

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: контекст/ограничение в инженерных приложениях

Происхождение: `W2-05-S03`, [W2-05](_WORK/W2_05.md), строка 15. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_05](_WORK/MATERIALS_W2_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[.gitignore PIN](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/.gitignore), раздел Project artifacts/Data

Свежий raw200; исключены `*.json`, `*.onnx`, `*.pt`, `*.weights`, `artifacts/`, `experiments*/`, `POYASNITELNAYA_ZAPISKA_LinQ_RESULTS.md`. Правила ignore объясняют возможное отсутствие в git, но не доказывают ни существование, ни отсутствие локальных авторских результатов.

<a id="S171"></a>
## S171

Primary identity: https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_tiny_yolo3_vendor.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F234](RAW_FACTS.md#F234)

Происхождение: `W2-05-S04`, [W2-05](_WORK/W2_05.md), строка 16. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_05](_WORK/MATERIALS_W2_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[vendor orchestrator PIN](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_tiny_yolo3_vendor.py), constants, main; [detection README PIN](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/README.md), Vendor section

Свежие raw200; статическое чтение автора, не vendor API specification.

<a id="S172"></a>
## S172

Primary identity: https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_tiny_yolo3_accuracy.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F238](RAW_FACTS.md#F238), [F240](RAW_FACTS.md#F240)

Происхождение: `W2-05-S05`, [W2-05](_WORK/W2_05.md), строка 17. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_05](_WORK/MATERIALS_W2_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[vendor accuracy adapter PIN](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_tiny_yolo3_accuracy.py), `run_once` L176–179, `compute_coco_metrics` L618–676, main L679–830

Свежий raw200, прочитан. Реальные metrics/predictions не получены.

<a id="S173"></a>
## S173

Primary identity: https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_tiny_yolo3_performance.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F240](RAW_FACTS.md#F240)

Происхождение: `W2-05-S06`, [W2-05](_WORK/W2_05.md), строка 18. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_05](_WORK/MATERIALS_W2_05/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[vendor performance adapter PIN](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_tiny_yolo3_performance.py), L29–110

Свежий raw200. Нативный executable MLPerf не получен/не выполнен.

<a id="S174"></a>
## S174

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/cfg/models/rt-detr/rtdetr-l.yaml

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F241](RAW_FACTS.md#F241), [F242](RAW_FACTS.md#F242), [F245](RAW_FACTS.md#F245)

Происхождение: `W2-06-S01`, [W2-06](_WORK/W2_06.md), строка 13. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [rtdetr-l.yaml](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/cfg/models/rt-detr/rtdetr-l.yaml), [head.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/modules/head.py)

U; config nc/backbone/last head; RTDETRDecoder `__init__`, `forward`, `_get_decoder_input`; свежий raw200, `u_model.yaml/u_head.py`.

<a id="S175"></a>
## S175

Primary identity: https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/modules/transformer.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F241](RAW_FACTS.md#F241), [F242](RAW_FACTS.md#F242), [F245](RAW_FACTS.md#F245)

Происхождение: `W2-06-S04`, [W2-06](_WORK/W2_06.md), строка 16. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

Ultralytics [transformer.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/modules/transformer.py), [modules/utils.py](https://github.com/ultralytics/ultralytics/blob/389b87f8cb9dbf2f31be8b70a94a3e47e11693db/ultralytics/nn/modules/utils.py)

U; MSDeformAttn.forward, DeformableTransformerDecoderLayer/Decoder, multi_scale_deformable_attn_pytorch103–161; raw200, code read only.

<a id="S176"></a>
## S176

Primary identity: https://onnx.ai/onnx/operators/onnx__GridSample.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F242](RAW_FACTS.md#F242), [F245](RAW_FACTS.md#F245)

Происхождение: `W2-06-S05`, [W2-06](_WORK/W2_06.md), строка 17. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

ONNX maintainers [GridSample specification](https://onnx.ai/onnx/operators/onnx__GridSample.html)

Открыты schema sections16/20/22; вывод привязан к **GridSample-16**, не текущему default22; HTML сохранён `onnx_gridsample.html`. Это schema, не LinQ support.

<a id="S177"></a>
## S177

Primary identity: https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/configs/body_2d_keypoint/rtmpose/coco/rtmpose-m_8xb256-420e_coco-256x192.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F243](RAW_FACTS.md#F243), [F244](RAW_FACTS.md#F244), [F245](RAW_FACTS.md#F245)

Происхождение: `W2-06-S06`, [W2-06](_WORK/W2_06.md), строка 18. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

OpenMMLab [RTMPose-m config](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/configs/body_2d_keypoint/rtmpose/coco/rtmpose-m_8xb256-420e_coco-256x192.py), [metafile](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/configs/body_2d_keypoint/rtmpose/coco/rtmpose_coco.yml)

M; codec/model/val_pipeline/test_cfg; exact Name/Weights record; raw200 `m_model.py/m_metafile.yml`. Weights bytes не получены.

<a id="S178"></a>
## S178

Primary identity: https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/models/heads/coord_cls_heads/rtmcc_head.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F243](RAW_FACTS.md#F243), [F244](RAW_FACTS.md#F244), [F245](RAW_FACTS.md#F245)

Происхождение: `W2-06-S07`, [W2-06](_WORK/W2_06.md), строка 19. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

OpenMMLab [RTMCCHead](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/models/heads/coord_cls_heads/rtmcc_head.py), [GAU](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/models/utils/rtmcc_block.py), [ScaleNorm](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/mmpose/models/utils/transformer.py)

M; head forward134–161/predict193–210, GAU `_forward`, transformer ScaleNorm.forward; raw200 `m_head.py/m_gau.py/m_transformer.py`.

<a id="S179"></a>
## S179

Primary identity: https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/configs/mmpose/pose-detection_simcc_onnxruntime_dynamic.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F243](RAW_FACTS.md#F243), [F244](RAW_FACTS.md#F244), [F245](RAW_FACTS.md#F245)

Происхождение: `W2-06-S09`, [W2-06](_WORK/W2_06.md), строка 21. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

MMDeploy [SimCC ORT config](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/configs/mmpose/pose-detection_simcc_onnxruntime_dynamic.py), [base ONNX](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/configs/_base_/onnx_config.py), [config utils](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/mmdeploy/utils/config_utils.py), [ONNX export](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/mmdeploy/apis/onnx/export.py)

D; complete config, opset11, get_dynamic_axes388–423, export138–148; raw200.

<a id="S180"></a>
## S180

Primary identity: https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/mmdeploy/codebase/mmpose/models/heads/simcc_head.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F243](RAW_FACTS.md#F243), [F244](RAW_FACTS.md#F244), [F245](RAW_FACTS.md#F245)

Происхождение: `W2-06-S10`, [W2-06](_WORK/W2_06.md), строка 22. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

MMDeploy [simcc_head rewrite](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/mmdeploy/codebase/mmpose/models/heads/simcc_head.py), [pose forward rewrite](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/mmdeploy/codebase/mmpose/models/pose_estimators/base.py), [backend](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/mmdeploy/codebase/mmpose/deploy/pose_detection_model.py), [task](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/mmdeploy/codebase/mmpose/deploy/pose_detection.py)

D; rewrite7–29; forward→_forward; backend103–166; task182–274 creates dummy full-image bbox. raw200; stock demo is not detector+pose video pipeline.

<a id="S181"></a>
## S181

Primary identity: https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/requirements/codebases.txt

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F244](RAW_FACTS.md#F244), [F245](RAW_FACTS.md#F245)

Происхождение: `W2-06-S11`, [W2-06](_WORK/W2_06.md), строка 23. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

MMDeploy [requirements/codebases.txt](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/requirements/codebases.txt), [regression/mmpose.yml](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/tests/regression/mmpose.yml), [support docs](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/docs/en/04-supported-codebases/mmpose.md)

D; requirements mmpose1.0.0/mmdet3.0.0; regression SimCC model is MobileNetV2, not selected RTMPose-m; support table RTMPose row ORT/TRT/ncnn/OpenVINO Y. Static code/docs, not read test log.

<a id="S182"></a>
## S182

Primary identity: https://github.com/open-mmlab/mmpose/blob/c7bfc9e461a4f084b9d1de059410c012307782ca/mmpose/datasets/transforms/topdown_transforms.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F244](RAW_FACTS.md#F244), [F245](RAW_FACTS.md#F245)

Происхождение: `W2-06-S12`, [W2-06](_WORK/W2_06.md), строка 24. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

MMPose [v1.0.0 TopdownAffine](https://github.com/open-mmlab/mmpose/blob/c7bfc9e461a4f084b9d1de059410c012307782ca/mmpose/datasets/transforms/topdown_transforms.py), [TopdownPoseEstimator](https://github.com/open-mmlab/mmpose/blob/c7bfc9e461a4f084b9d1de059410c012307782ca/mmpose/models/pose_estimators/topdown.py)

v1.0.0; transform stores input_size only vs newer input_center/scale; estimator150–155 uses gt_instances bbox_centers/scales. raw200 `m100_*`; version seam, no executed failure.

<a id="S183"></a>
## S183

Primary identity: https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/configs/mmpose/pose-detection_simcc_tensorrt_dynamic-256x192.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F244](RAW_FACTS.md#F244), [F245](RAW_FACTS.md#F245)

Происхождение: `W2-06-S13`, [W2-06](_WORK/W2_06.md), строка 25. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_06](_WORK/MATERIALS_W2_06/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

MMDeploy [SimCC TRT config](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/configs/mmpose/pose-detection_simcc_tensorrt_dynamic-256x192.py), [generic pose TRT INT8](https://github.com/open-mmlab/mmdeploy/blob/bc75c9d6c8940aa03d0e1e5b5962bd930478ba77/configs/mmpose/pose-detection_tensorrt-int8_static-256x192.py)

D; former two SimCC outputs, batch min1/opt2/max4; latter generic single-output inherited schema. Neither is LinQ quantization recipe.

<a id="S184"></a>
## S184

Primary identity: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F246](RAW_FACTS.md#F246)

Происхождение: `W2-07-S01`, [W2-07](_WORK/W2_07.md), строка 13. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_07](_WORK/MATERIALS_W2_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

SciPy community, [proportion_ci docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html), отображается **v1.18.0**, Parameters/method exact; publication date unknown

Documentation, actual HTML открыт web и сохранён bytes. Mutable docs не lockfile. Запросы versioned 1.17.1 docs через web дали tool Internal Error, а не доказательство отсутствия документации.

<a id="S185"></a>
## S185

Primary identity: https://github.com/scipy/scipy/blob/527eb7fd7953a1de068f94bf8b322f249b9405ae/scipy/stats/_binomtest.py

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F246](RAW_FACTS.md#F246), [F247](RAW_FACTS.md#F247)

Происхождение: `W2-07-S02`, [W2-07](_WORK/W2_07.md), строка 14. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_07](_WORK/MATERIALS_W2_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

SciPy community, [_binomtest.py](https://github.com/scipy/scipy/blob/527eb7fd7953a1de068f94bf8b322f249b9405ae/scipy/stats/_binomtest.py), **v1.17.1**, commit `527eb7fd7953a1de068f94bf8b322f249b9405ae`; локальный `proportion_ci` L50, `_binom_exact_conf_int` L130–160, `binomtest` L204

Code прочитан и [сохранён](_WORK/MATERIALS_W2_07/scipy_binomtest.py), не исполнен. Commit date 2026-02-22T19:06:42Z взята из W1-12 API observation, здесь повторно не проверена. Live docs и code разных версий, их не выдаём за один release.

<a id="S186"></a>
## S186

Primary identity: https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F248](RAW_FACTS.md#F248)

Происхождение: `W2-07-S03`, [W2-07](_WORK/W2_07.md), строка 15. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_07](_WORK/MATERIALS_W2_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

NIST/SEMATECH, [e-Handbook §8.4.5.1](https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm), “Confidence Interval Equation and Zero Fails Case” / table interpretation

Documentation, actual content открыт web. Fixed-time HPP/exponential conditions; не исследование CV false alerts. Дата редакции неизвестна. Python HTTP 403; web content доступен.

<a id="S187"></a>
## S187

Primary identity: https://www.itl.nist.gov/div898/handbook/eda/section3/eda366j.htm

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F248](RAW_FACTS.md#F248)

Происхождение: `W2-07-S04`, [W2-07](_WORK/W2_07.md), строка 16. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_07](_WORK/MATERIALS_W2_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

NIST/SEMATECH, [e-Handbook §1.3.6.6.19](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366j.htm), Probability Mass Function

Documentation, actual web content прочитан; дата неизвестна. Poisson parameter на странице — mean count per interval, не автоматически rate/hour.

<a id="S188"></a>
## S188

Primary identity: LOCAL:W2-07-S07

Access: **2026-10-23**. Publication/version/commit и точный locator — в атрибутированных записях ниже; если поле не названо, оно **UNKNOWN**, а не дата доступа. Actual checked scope и evidence type не расширяются за исходную запись.

Поддержанные F: [F250](RAW_FACTS.md#F250)

Происхождение: `W2-07-S07`, [W2-07](_WORK/W2_07.md), строка 19. Сохранённые материалы этой проверки: [_WORK/MATERIALS_W2_07](_WORK/MATERIALS_W2_07/); exact filename/hash/source URL и действительный scope — в manifest/provenance и исходной записи, не новый fetch сборщика.

[W1-12](_WORK/W1_12.md), разделы «Парная uncertainty», «Входы», E03–E06; [сохранённый SciPy bootstrap source](_WORK/MATERIALS_W1_12/scipy_resampling.py), pin/sha в W1 retrieval

Secondary protocol + сохранённый primary code; neighbour runs не присвоены. Bootstrap остаётся design-specific.
