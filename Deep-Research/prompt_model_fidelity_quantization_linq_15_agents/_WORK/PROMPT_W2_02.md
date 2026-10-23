# Индивидуальное поручение W2-02 — вторая волна

Роль: самостоятельный сетевой исследователь gpt-6.1-sol, effort=medium, fork_turns=none. Ты получаешь новый контекст, не запускай субагентов. Рабочая папка текущая; topic model_fidelity_quantization. Это согласованная вторая волна после15 W1 (12general/3LinQ) и отдельного fresh critic high. Команда пяти участников строит industrial safety video service, final neural inference на LinQ обязателен. GPU не арендовали, модели/SDK/сервер не запускались. Кейс найден локально, root прочитал все20 страниц визуально по сохранённым рендерам: _WORK/CASE_NOTES.md; оригинал _WORK/INPUT/CASE_LINQ.pdf. VM/сервис обещаны, actual grant/SDK/device/model/GT отсутствуют. Заявление команды про1FPS и server-file mode — working assumptions, не контракт API/метрик.

Прочитай полностью оба входных договора, _WORK/CRITIC_HANDOFF.md, свой точный K текст ниже и указанные W1/source snapshots. Дальше получай новые первичные сетевые основания по узкому вопросу, а не повтор W1. Открывай фактический content и цепочки provenance, не пересказывай snippets. Даты/версии/commit/locators/author/access фиксируй; живые docs не lockfile. Если PDF bytes доступны, визуально проверь спорные tables/code/footnotes через PDF workflow; failed tool access vs actual closed file разделяй. При недоступном live source можно использовать сохранённый primary excerpt с атрибуцией, не выдавая его за свежий fetch. Copyright: пересказ+locators вместо длинных копий.

Собственный результат _WORK/W2_02.md; snapshots _WORK/MATERIALS_W2_02/. S/F префикс W2-02-. Каждый факт: source, locator, exact version/conditions, actual verification status, limitation, practical decision. Типы vendor claim/documentation/code/published measurement/local observation/inference/proposal/unknown; чтение кода не execution, чужой benchmark не наш. Общие ORT/Intel/NVIDIA возможности не доказывают LinQ. Неизвестность не доказательство отсутствия. Соседние отчёты secondary; их запуски не наши.

Никаких установок SDK, подключения сервера, аренды, training/model benchmarks, приложения, push/PR или сообщений людям. Допустимы маленькие read-only metadata/code inspection и явно аналитические расчёты там, где они нужны; не называй это модельным измерением. Команды/API только с фактической версией и основанием; pseudo-code явно. Опубликованные числа сохраняй вместе с setup, без переноса на LinQ/3090. Новые сильные зацепки можно развить, если меняют поставленный выбор, объяснив пользу.

В результате отдельный блок K dispositions: новый факт/source, что изменилось, closed/scope narrowed/contradiction/open/superseded, оставшийся риск и точный Q со способом закрытия. Не редактируй CRITIC или общие финальные файлы. Остановись при полезном новом основании/ограничивающем условии или содержательно локализованном unknown после адресного поиска; не искать закрытый SDK бесконечно. Короткая передача root:3 находки, блокер, следующий шаг, путь и K outcomes.

## Точный предмет и source targets критика

| W2_02.md | K002,K003 | Один цельный Ultralytics8.3.230 Detect/Pose безNMS contract с exact head/export/preprocess/NMS/inverse source; сравнить существенные helpers v8.3.0 из W1-05. Затем ONNX tensor+port+role→TF→QM/TPU mapping по реальному `onnx_to_tf`/`onnx_direct` поставщику, без подмены одноимённым converter. Target: pinned Ultralytics code, guide, pinned build_yolov8_program.py и доступный primary importer metadata/source. Stop: связанный контракт, G01–04 version delta, importer-specific UNKNOWN и минимальный probe. |

## Исходная критика (сохранять историю)

## K002 — Самый важный дополнительный importer-переход ещё не имеет семантического контракта

**Приоритет / закрытие:** P0; WEB частично, ARTIFACT+TEST обязательно.

**Проблема и локатор.** W1-13, F02/F09/F10/F12, карта ONNX→TF; W1-14 E04; W1-02/03 описывают PyTorch↔ONNX существенно подробнее, чем **ONNX↔TF через конкретный `onnx_to_tf`**. Сохранённый `build_yolov8_program.py` сначала переписывает input metadata, затем перебирает converter/simplification, отображает имена и пробует несколько output names. Успешный RegularModel constructor не подтверждает ни тождество выбранного тензора, ни сохранение layout и graph cut. Имя `onnx_to_tf` нельзя автоматически отождествить с любым популярным проектом onnx-tf/onnx2tf.

**Что меняет для команды.** PyTorch↔ORT PASS и плохой LinQ output могут разделяться ошибкой import ещё до quantizer. Если выбрать другой одноимённый tensor/порт либо потерять второй output, сравнение «PTQ ухудшил» причинно неверно. Сравнение только конечных боксов не восстановит это различие.

**Недостающее доказательство.** Идентичность поставщика и версии importer; точная семантика mapping, входов/выходов и возможных transpose; список преобразованных operators/attributes; float TF outputs на том же canonical input. Понадобится либо mapping семантических выходов, либо честная отметка о необозримой границе.

**Узкое W2 / source targets / завершение.** **W2-02**: проследить этот importer по официальному guide, фактическим import lines и доступным metadata/source `onnx_direct`/`tpu_framework`, не устанавливая SDK и не подменяя его сторонним converter. Составить admission contract: ONNX tensor name+port+shape+role→TF tensor name+port+shape+role→QM/TPU descriptor; вынести принудительную static-shape правку отдельным parent artifact. Привязать к обычному Detect и Pose выбранной закреплённой реализации, включая все outputs. Завершение: найден первичный контракт и минимальные probes либо указано, какие поля можно получить только из выданного SDK; неподтверждённые операции остаются UNKNOWN, а не UNSUPPORTED.

**Disposition W2:** PENDING.



## K003 — Полезные YOLO факты взяты из разных версий; целостный worked example ещё не собран

**Приоритет / закрытие:** P1; WEB, затем ARTIFACT+TEST.

**Проблема и локатор.** W1-02/04 закрепляют Ultralytics8.3.230; W1-05 — preprocess/inverse v8.3.0; W1-11 — оригинальные ByteTrack/BoT-SORT. Сторонний LinQ repo не pin Ultralytics/torch. Каждый локальный вывод ограничен версией корректно, но будущий читатель может склеить «стандартный YOLO pipeline» из этих фрагментов. Особо опасны `.pt`-dependent rectangle, расположение NMS между файлами, nc inference, `shape[-1]==6`, inverse geometry и используемая tracker integration.

**Что меняет для команды.** Это может создать новый decoder/preprocess mismatch уже при следовании отчёту. Нужен один полностью прослеживаемый иллюстративный маршрут; он не должен становиться без основания рекомендацией поставить эту версию на сервер.

**Недостающее доказательство.** Совпадающие tag/commit для head, export helper, preparation/fusion, predictor, LetterBox, inverse helpers, NMS и конфигурации выходов. Изменения между v8.3.0 и8.3.230, влияющие на конкретные W1 fixtures, пока не сведены.

**Узкое W2 / source targets / завершение.** **W2-02**: по закреплённому Ultralytics8.3.230 проследить один обычный non-end2end Detect и один Pose без NMS: вход→подготовка→export→decoded pre-NMS output→общий NMS→inverse. Проверить, какие из G01–G04 W1-05 сохраняются, а какие требуют новой версии expected result. Custom nc=1/2/3 и kpt_shape задаются manifest, не эвристикой. Выход — один version-coherent contract и короткий diff, не повтор W1-04. Завершение: каждый используемый helper имеет тот же immutable commit либо явно обозначенную внешнюю зависимость; установленная версия LinQ adapter всё ещё требует environment manifest.

**Disposition W2:** PENDING.



