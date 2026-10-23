# W2-G — закреплённый Vast CLI, lifecycle и спорные начисления

Доступ и наблюдения: **2026-10-23, 17:44–17:47 UTC / 20:44–20:47 Europe/Moscow** по локальным UTC timestamps и HTTP Date в [manifest](W2_G_MATERIALS/manifest.json) и [additional manifest](W2_G_MATERIALS/additional_manifest.json). Автор первичных документов и кода — Vast.ai/vast-ai; автор решений и будущего протокола — исследователь W2-G. Публичные docs/API schema, release metadata, небольшой wheel и source прочитаны без credentials. CLI не установлен и не запущен; аккаунт, инвойсы, ресурсы не читались/не изменялись. Новых offers не запрашивал: timestamped public quotes остаются исключительно W1-12. Обучение, export, GPU и LinQ execution отсутствуют.

## Решение и статус критики

**W2-G-F01. Выбрать фактически опубликованный wheel `vastai-1.9.0-py3-none-any.whl`, а не произвольный `pip install vastai` и не legacy `vast.py`.** Его SHA256 **`dfa2349701a2302bdf2ea902bc0548609870da2888167883ab32eec954eed98b`**, 324493 bytes, совпал с digest официального release asset. Entry point: `vastai = vastai.cli.main:main`; Python `>=3.10,<4.0`. Wheel сохранён [здесь](W2_G_MATERIALS/vastai-1.9.0-py3-none-any.whl), metadata/entrypoint — рядом. Это pin CLI artifact, **не готовый dependency lock и не проверенная установка** [W2-G-S01/S02].

**W2-G-F02. Legacy вывод W1-13 о `shell=True` исправляется для выбранного wheel:** modular copy передаёт список аргументов `subprocess.run`, а не shell string. Но проверка exit code отсутствует и `StrictHostKeyChecking=no` сохраняется; внешний destination bytes/hash/load остаётся обязательным независимо от CLI success. Wheel destroy дополнительно имеет интерактивное подтверждение `y/N`, которого в исследованном legacy пути не было [W2-G-S03/S04].

**W2-G-F03. Billing неизвестность сузилась, но loading не закрыт:** новая найденная current FAQ явно включает loading в storage billing, одновременно current main Billing/Managing обещают отсутствие начисления при Loading. Уверенно объявлять loading полностью бесплатным нельзя. Две current страницы исключают compute/storage при offline, legacy FAQ включает offline storage. Для текущего документального default принимаем явную current offline-оговорку; фактический ledger ещё не наблюдался [W2-G-S07–S10].

Исходная критика **K010** сохранена в [CRITIC.md](../CRITIC.md), раздел «Lifecycle/стоимость…». Её ключевой тезис: «Даже valid copy command не отменяет destination hash/load». W2 не отрицает историческую правильность анализа legacy HEAD; он уточняет применимость к executable artifact. **Статус K010: закрыто документально по выбору artifact, командам и контролю integrity; уточнено по состояниям; остаётся открытым только фактический contract/Charges/payment и current loading contradiction.** Ни старый quote, ни этот runbook не авторизуют расходы/удаление.

**K011: уточнена применимость, интеграция остаётся у сборщика.** До аренды достаточно документальных/data/export gates и готового внешнего архива; VRAM qualification на конкретной 3090 — отдельная первая оплачиваемая стадия после разрешения. Не превращать full dependency engineering/strict recovery controller в обязательный новый проект. Вклад W2-G в minimal route: один CLI artifact, проверяемая внешняя копия, небольшой ledger; ни второй GPU, ни DDP для этого не требуются. Выбор сценария, людей, freeze и относительных reserves зависит от W2-A…F и сборки K011.

## Release против HEAD: реальный исполняемый путь

**W2-G-F04.** Release v1.9.0 опубликован `2026-10-20T21:31:52Z`, tag commit **`28bde4827374ef658694db5a1e1e61508b966e2f`**. Сравниваемый HEAD из W1 — **`42c3a47b44603775a5e31f54de0fce3994bd3f11`**, не плавающее имя master. GitHub compare содержит два промежуточных изменения: API-key/team notes и serverless disk metrics. Важнее этого перечня проверка bytes: извлечённые из wheel `cli/commands/{storage,instances,offers,billing}.py`, `api/client.py`, `cli/util.py` совпали с release source **и** этим HEAD; `api/{storage,instances,offers,billing}.py` совпали с HEAD. Результаты и hashes: [wheel_source_comparison.json](W2_G_MATERIALS/wheel_source_comparison.json), [additional_manifest.json](W2_G_MATERIALS/additional_manifest.json). Legacy целевые function bodies также совпадают между SHA, но это вспомогательное наблюдение, не доказательство wheel semantics [S01–S06].

| Интерфейс wheel | Реальный запрос / поведение | Locator выбранного source |
|---|---|---|
| `search offers` | По умолчанию POST `/api/v0/bundles/`; `--new` переключает PUT `/api/v0/search/asks/`. `--storage` задаёт `allocated_storage`; `--raw` возвращает offers list | `cli/commands/offers.py` L127–200; `api/client.py`, URL construction |
| `show instance ID` | GET `/api/v0/instances/ID/?owner=me`; возвращённая row преобразуется. Отсутствие в raw — объект `instances:null`, это не доказательство оплаты/уничтожения | `cli/commands/instances.py` L41–65; `api/instances.py` L83–91 |
| `show instances --raw` | Без explicit pagination собирает все v1 pages в flat list; `--limit`/`--next-token` меняют контракт на одну страницу | CLI instances L1054–1065; API instances L31–58 |
| `copy` | API PUT rsync при одном ID `None`, иначе copy_direct; local transfer запускает внешний rsync. Remote→remote ответ означает initiation | CLI storage L78–128; API storage L53–67 |
| `stop instance ID` / `start instance ID` | PUT `/api/v0/instances/ID/`, JSON state stopped/running. CLI печатает request result; polling состояния требуется отдельно | API instances L320–339; CLI instances L277–347 |
| `destroy instance ID` | Подтверждение по умолчанию; API DELETE `/api/v0/instances/ID/`, JSON `{}`. `-y` обходит prompt | CLI instances L212–248; API instances L309–317 |

**W2-G-F05. Два важных различия с legacy и документационными примерами.** CLI wheel default search включает verified/external/rentable, **не `rented=false`**; SDK helper/legacy включает rented. Наш точный query ниже явно задаёт все четыре фильтра. `local:path` поддерживается help/parser, но API dispatch проверяет только `None`, поэтому explicit `local` идёт через `copy_direct`, в отличие от unprefixed local Unix path через `rsync`. Это доказанное ветвление кода, **не наблюдённая ошибка сервера**: не утверждаем, что сервер обязан отказать. Для первого transfer выбираем legacy numeric remote + unprefixed local path, не нуждающийся в этом предположении [S03/S05/S06].

`subprocess.run(cmd)` в wheel copy не использует `check=True` и не исследует `returncode`. HTTP success может закончиться ошибкой rsync, тогда function возвращает `None`; main dispatcher завершает такой путь без доказательства копирования. `--raw` не превращает copy в integrity receipt. Аналогично wrappers start/stop/destroy не возвращают пользователю helper result как надёжный lifecycle status. Не строить контроллер на одном exit code [S03/S04/S02].

## Точные команды — только будущие, здесь не выполнялись

Среда выполнения примеров — **Linux/WSL control host**, POSIX paths; `.venv-vast190/bin/vastai` означает executable от выбранного wheel. Он должен быть отдельно установлен владельцем, затем его version и путь сопоставлены с manifest. GitHub asset уже скачан исследователем только как файл; его код не импортировался. Для установки будущий оператор может использовать:

```bash
python3 -m venv .venv-vast190
.venv-vast190/bin/python -m pip install ./vastai-1.9.0-py3-none-any.whl
.venv-vast190/bin/vastai --version
.venv-vast190/bin/python -m pip freeze --all > control-installed.txt
```

Перед install проверять SHA256 выше. Wheel METADATA закрепляет часть dependency versions, остальные — ranges; такая установка не воспроизводит транзитивные bytes во времени. Для повторного принятого control environment сохранить resolved lock/hashes/Python/OS и inventory. Это внешний runtime gate, не документальный пробел выбора CLI. Не использовать auto-update/installer с плавающим URL. API key настраивает владелец на control host; ключей в примерах и training image нет.

Read-only примеры после account setup владельцем; `INSTANCE_ID` и даты — placeholders, не существующие ресурсы этого исследования:

```bash
.venv-vast190/bin/vastai search offers 'gpu_name=RTX_3090 num_gpus=1 verified=true external=false rentable=true rented=false reliability>=0.99 disk_space>=100' --type on-demand --storage 100 --order dph_total --limit 3 --raw
.venv-vast190/bin/vastai show instance INSTANCE_ID --raw
.venv-vast190/bin/vastai show instances --raw
.venv-vast190/bin/vastai show volumes --raw
.venv-vast190/bin/vastai show invoices-v1 --charges --start-date START_UTC_UNIX --end-date END_UTC_UNIX --limit 100 --raw
.venv-vast190/bin/vastai show invoices-v1 --invoices --start-date START_UTC_UNIX --end-date END_UTC_UNIX --limit 100 --raw
```

Это рецепт обновления **той же** quote specification W1, не новый market survey. Перед будущей арендой сохранить полный ответ с UTC/query/D/offer/machine/host/type/end_date и отдельными rate fields. Для 2 GPU меняется `num_gpus=2`, но в minimal route вторая GPU не обязательна. Полный raw show может содержать `extra_env`, connection tokens/onstart: evidence storage должен быть приватным, а review copy редактируется без потери resource/state/rate полей. Установка и эти запросы здесь отсутствуют.

На каждом billing raw ответе следовать `next_token` до null, повторяя **тот же** date/filter запрос с `--next-token NEXT_TOKEN`; это одна страница в raw, а не гарантированно вся история. UNIX bounds — UTC, оба inclusive в выбранном helper. При агрегации соседних окон избегать двойного включения границы. История invoices — платежи/пополнения, **не** замена per-resource charges [S11/S12/S13].

Отдельный lifecycle после самостоятельного разрешения, не выполнять как один script:

```bash
.venv-vast190/bin/vastai copy INSTANCE_ID:/workspace/archive/run_id/ /srv/team_archive/run_id/
.venv-vast190/bin/vastai stop instance INSTANCE_ID
.venv-vast190/bin/vastai show instance INSTANCE_ID --raw
.venv-vast190/bin/vastai start instance INSTANCE_ID
```

Первая команда выбирает содержимое immutable source directory, согласно trailing slash semantics Data Movement. Transfer возможен при ограничениях доступности ports/host; обычный SSH/SCP требует работающего sshd и не является универсальной заменой stopped-instance transfer. На native Windows установка Python package сама по себе не предоставляет rsync; `D:\...` также нельзя переносить в этот Unix-path протокол. В WSL использовать проверенные Linux paths и доступные `rsync`/`ssh`. Wheel улучшил shell handling, но `-e` по-прежнему содержит SSH command string и отключённую проверку host key: для доверенного backup предпочесть отдельно проверенный SSH/SFTP route с verified host key либо явно принять ограничения CLI; тождество hash при ошибочно доверенном источнике не удостоверяет происхождение [S03/S06/S14].

**Предлагаемый TEAM gate, отдельный от CLI:** до transfer trainer делает native recovery snapshot **до stripping**, закрывает его запись, фиксирует run/attempt/parent, список filenames, byte sizes и SHA256; manifest становится immutable. На внешнем destination независимый reader сверяет полный список/bytes/hash и загружает trusted checkpoint выбранным trainer для проверки expected state/epoch/optimizer и идентичности. Partial output, missing file, mismatch или load failure => `TRAINED_UNARCHIVED`, сохраняется прошлый verified snapshot. Никаких lockbox данных в smoke/архивном тестовом payload.

Receipt содержит source instance/run/attempt/checkpoint hash, destination identity/path/object-version при наличии, verified file list/bytes/hash, load-check environment/result, UTC и verifier identity. Только после receipt всех уникальных outputs и отдельного lifecycle поручения допустима будущая команда:

```bash
.venv-vast190/bin/vastai destroy instance INSTANCE_ID
```

Prompt не проверяет receipt автоматически. `--yes` не входит в минимальный ручной runbook. Перед запросом сохранить state/rates/receipt и точный ID; после — отдельно reconcile instance absence и полный список оставшихся volumes/charges. Destroy instance не является delete volume. Copy success, state request acceptance и archive acceptance — три разных факта.

## State-by-state: политика, конфликт, проверка

**W2-G-F06.** Таблица — документальная интерпретация, не наблюдение списаний. `G` — compute **всего offer**, `Srun/Sstop` — storage allocation, `Bin/Bout` — usage network. Current main Billing задаёт секундный учёт active compute и online storage; bandwidth отдельно. Внутренний расчётный engine публично не проверен [S07].

| Состояние | Документальное начисление | Конфликт/граница | Точная будущая проверка |
|---|---|---|---|
| running/active connected | G + allocation storage + metered network | Idle/0% utilization не скидка | `gpu`, `disk`, `bwd`, `bwu`; rate×duration/volume против полного contract |
| loading | Compute явно не active; FAQ включает online storage; main Billing/Manage обещают «не charged» | **Current-current конфликт storage/transfer scope** | Синхронный state timeline и items `disk/bwd/bwu` за image pull interval; попросить exact metering exclusion |
| stopped/inactive online | Compute не active; storage продолжается; transfers отдельно | Sstop может быть выше Srun | Hover actual stopped price + `disk`; не подставлять Srun по умолчанию |
| offline | Current main+FAQ исключают active и storage | Legacy FAQ включает storage offline/broken; reserve консервативный | State interval, `gpu/disk` entries и corrections, не имитировать outage |
| expired | Contract останавливается; restart запрещён; возможное удаление через 48h | Отдельный expired storage тариф не найден; online/stopped трактовка условна | end_date/expiry→deletion timeline; `disk` и contract closure. 48h не backup SLA |
| destroyed | Container data удалены; прежний allocation больше не существует | Независимые volumes и delayed ledger ещё возможны | Deletion acknowledgement/absence, затем latest disk accrual end и все volume IDs |
| volume attached/detached | Отдельно тарифицируется, переживает instance destroy | Instance offline exemption не доказан для separate volume | `type=volume`, соответствующий `source`, `disk` до own removal; отдельный contract/rate |

Источники таблицы: current main Billing Pricing L191–196 и Loading L339–341 [S07]; current FAQ Pricing L123–128, **explicit loading** [S08]; legacy FAQ Billing L255–257 [S09]; Managing Instances L217–238, L338–347 [S10]; Storage Types Costs L191–197 [S15]. Offline documentation precedence — наше решение по актуальным страницам, не официальное разрешение противоречия. Для loading такого разрешения нет; бюджетировать storage/transfer консервативно до Charges/официального уточнения.

**W2-G-F07. Новая schema позволяет проверять узко.** Public Show Charges OpenAPI `info.version:1.0.0` описывает GET `/api/v0/charges/`, required `select_filters.day` UTC Unix seconds; resource `type`, `source`, start/end, amount и nested items с enum **`gpu,disk,bwd,bwu`**. Contract amount округлён до 3 decimals. Полей guaranteed raw byte counter/rate/unit-divisor/schema currency declaration в просмотренном charge-item блоке нет; description — строка, не типизированная metering formula. Поэтому дробные totals и округление не восстанавливают SI/TiB divisor. Сервер допускает max500/page, выбранный CLI cap100/page — ограничения разных уровней, не конфликт [S11/S13].

## Units и точные оставшиеся вопросы

W1-12 quote остаётся наблюдением **17:04:35–17:04:37 UTC 2026-10-23**, не будущим договором. Его `dph_total = dph_base + storage_total_cost` и `storage_cost × D /720` — наблюдённые равенства тех JSON. Не умножать multi-GPU `dph_base` на GPU count повторно, не добавлять storage к dph_total ещё раз. CLI `--storage` подписан **GiB**, field help `storage_cost` — $/GB/month, main billing — $/GB/hour, bandwidth — $/TB. Отсюда **не следует** общий byte divisor для allocation/transfer. 720 — арифметика снимков, не календарный месяц. Эти W1 факты не переизмерялись [W1-12-F02/F04; S05/S07].

Будущий владелец аккаунта проверяет, не меняя settings ради исследования:

1. **Q-G01 Loading:** какая точная строка `disk` покрывает loading timestamps; входит ли image pull в `bwd`, с какого network interface и учитывается ли повторное скачивание cached layers? Противоречащие current sections приложить. Отсутствие крупной charge при маленьком test не доказывает exemption из-за округления/задержки.
2. **Q-G02 Rates/units:** contract running/stopped `diskHour`, allocation quantity и единица GiB/GB; `$ /GB/month` denominator; `bwd/bwu` quantity, bytes divisor TB/TiB, per-direction rates. Включены ли pip/apt/weights ingress и request/storage backend charges? Для package transfers общий network policy есть; исключения/точное metering image pull не доказаны.
3. **Q-G03 State:** коррелировать actual/intended/cur/next state, UTC transitions и charge interval; какое состояние реально использует billing? `intended_status=stopped` после PUT ещё не подтверждает stopped compute. Для offline/expired не устраивать платные/failure эксперименты без нужды: проверить лишь естественно возникшие интервалы либо официальный ответ.
4. **Q-G04 Payments:** Charges всех pages объясняет resource usage; `/api/v1/invoices/` — top-ups/transfers/payment records. Проверить saved-card/autobilling/negative balance policy, tax/FX/payment terms и предел порученных расходов. Zero balance не считать cap; current FAQ также описывает возможное погашение отрицательного баланса картой [S08/S12].
5. **Q-G05 Closure:** конец начисления source container после destroy, существование volumes, corrections и последующие charges сверять по resource ID и interval, не только по времени появления записи. Уничтожение не обещает немедленный нулевой total balance.

## Минимальный будущий различающий эксперимент

**Вопрос:** позволяет ли выбранный wheel безопасно получить independently verified archive и reconciled lifecycle/cost evidence? Предпосылки: отдельное разрешение расходов/stop/start, pinned control runtime с rsync/ssh, разрешённый archive destination, owner-controlled contract, небольшой несекретный test directory, native snapshot schema владельца trainer. Destroy не нужен для первого integrity drill; его stage возможен позднее только после receipt и отдельного lifecycle scope.

1. До аренды read-only source/artifact checks уже выполнены. Будущий оператор локально проверяет version/path/deps и transport, пишет immutable small fixture+manifest. Это без-GPU preparation; fit здесь не заявляется.
2. На отдельно разрешённом instance копирует fixture, получает destination bytes/hash; проверяет заведомо повреждённую **вторую тестовую копию**, которая обязана быть отвергнута. Transfer лог и CLI exit сохраняются раздельно с verifier result.
3. Для реального native checkpoint выполняет destination trusted load и фиксирует его state/parent. На short qualification отдельно измеряет worst-case train+val memory: успешный transfer этого не заменяет.
4. Если разрешены stop/start, сохраняет state/rate snapshots до/после, ждёт actual status и доступность, не считает request ответ финалом. Billing сохраняет с полной pagination и последующим refresh после учётной задержки; расход сопоставляет с timeline/bytes/rates и округлением.

Метрики/артефакты: bytes/hash agreement, verifier false accepts (нужен ноль в planned negative fixture), load outcome, source/destination identity, transfer duration/retries, actual transition lag, archive receipt, rate+quantity units, `gpu/disk/bwd/bwu` amount и unresolved residual. **Успех** — целая загружаемая внешняя копия и объяснимый ledger; **failure** — любой missing/hash/load mismatch, непринятый state или необъяснённые units/charges => не запускать длинную серию/не удалять единственную копию. CLI exit0 при rejected destination — подтверждение необходимости независимого gate, а не успешный backup.

Этот опыт не доказывает future host reliability, exact numerical resume, целевой accuracy, 24GB fit полной задачи, выигрыш второй GPU или LinQ compatibility/latency. Lockbox не используется ни для fixture, ни для qualification/train selection. Training owner получает native pre-strip snapshot/lineage requirement (W2-A), stack owner — отсутствие runtime lock (W2-B), LinQ owner — hash проверенного inference artifact (W2-F), сборщик K011 — minimal one-GPU qualification без нового controller проекта. Оставшиеся actual rates/invoice/owner permissions не закрываются публичным поиском.

## Реестр первичных источников

Все прочитаны 2026-10-23; live docs не имеют подтверждённой publication revision. Локальные MD/YAML snapshots с access+SHA фиксируют **прочитанное содержимое**, не равенство docs repository commit или серверной реализации. Номера строк GitHub относятся к указанному SHA; web locators относятся к этому доступу.

| ID | Автор, URL / version / locator | Evidence и предел |
|---|---|---|
| W2-G-S01 | Vast.ai, [release v1.9.0](https://github.com/vast-ai/vast-cli/releases/tag/v1.9.0), [API metadata](https://api.github.com/repos/vast-ai/vast-cli/releases/tags/v1.9.0); published 2026-10-20, tag 28bde482… | release.json, wheel asset digest/size, tag identity; не запуск |
| W2-G-S02 | Vast.ai, [official wheel asset](https://github.com/vast-ai/vast-cli/releases/download/v1.9.0/vastai-1.9.0-py3-none-any.whl), wheel METADATA/entry_points, [main.py](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/main.py), `main/run_command` | Реально скачанные bytes; статическое извлечение, не установка |
| W2-G-S03 | [CLI storage.py](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/storage.py#L78), L78–128 | subprocess argv/no checked result, host-key option; wheel совпал с source |
| W2-G-S04 | [CLI instances.py](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/instances.py), L41–65,212–347,1054–1065; [API instances](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/api/instances.py), L31–91,309–339 | source control flow, не измерение transitions |
| W2-G-S05 | [CLI offers.py](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/offers.py#L127), L22–33,127–200; [API offers](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/api/offers.py), L12–56 | CLI vs SDK default filters, storage units/endpoint |
| W2-G-S06 | [API storage.py](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/api/storage.py#L53), L53–67; [utils](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/utils.py#L87), L87–119; [compare](https://api.github.com/repos/vast-ai/vast-cli/compare/28bde4827374ef658694db5a1e1e61508b966e2f...42c3a47b44603775a5e31f54de0fce3994bd3f11) | URI parsing/dispatch and release vs HEAD; no server copy test |
| W2-G-S07 | [Current Billing](https://docs.vast.ai/guides/reference/billing), Pricing L191–196, Transactions L266–278, Loading L339–341 | current policy/units; actual invoice unknown |
| W2-G-S08 | [Current FAQ Billing](https://docs.vast.ai/guides/reference/faq/billing), Pricing L123–128, Billing L107–116 | Новое explicit loading storage + offline exclusion; contradiction сохранён |
| W2-G-S09 | [Legacy FAQ](https://console.vast.ai/faq/), Billing→Pricing L255–257 | competing offline policy, дата публикации не установлена |
| W2-G-S10 | [Managing Instances](https://docs.vast.ai/guides/instances/manage-instances), Operations/Restart/Loading/Expiration L217–238,287–303,338–347 | lifecycle policy, отсутствие гарантии рестарта/48h preservation |
| W2-G-S11 | [Show Charges](https://docs.vast.ai/api-reference/billing/show-charges), [OpenAPI YAML](https://docs.vast.ai/api-reference/openapi/yaml/show_charges.yaml), info.version1.0.0; YAML L108–179 | typed items enum/source/rounded amount; не actual account charges |
| W2-G-S12 | [Show Invoices](https://docs.vast.ai/api-reference/billing/show-invoices), [YAML](https://docs.vast.ai/api-reference/openapi/yaml/show_invoices.yaml), route/query/schema | Payments vs usage, UTC filter/pagination; no account access |
| W2-G-S13 | [CLI billing.py](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/billing.py), L346–438; [API billing](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/api/billing.py#L66), L66–167 | Exact date flags/raw pagination/endpoint/cap; не выполнен |
| W2-G-S14 | [Data Movement](https://docs.vast.ai/guides/instances/storage/data-movement), CLI Copy, trailing slash paragraph, SCP, VM Constraints | Transports и ограничения; отдельный VM-only constraints не переносится на Docker |
| W2-G-S15 | [Storage Types](https://docs.vast.ai/guides/instances/storage/types), Characteristics/Limitations/Costs L129–197 | charged allocation, separate local volumes, possible higher stopped rate |

Негативные находки: guessed `setup.py` URL вернул404 — не использован; guessed list-instances page не открылась, правильный `show-instances` открыт; несуществующий `vastai/cli/query.py` в wheel заменён реальным import `vastai.api.query` при чтении handlers. Наличие CLI network-volume commands не доказывает доступный cross-host backup contract; minimal route от него не зависит. Все архивные материалы — только этой ветки, предыдущие W1/CRITIC не изменены.
