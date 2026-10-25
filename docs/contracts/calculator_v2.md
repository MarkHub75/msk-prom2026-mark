# Контракт калькулятора Argus v2 для Егора и Astra

<!-- calculator-contract:begin version=2.0.0 -->

Версия договорённости: `2.0.0`. Дата: 25.10.2026. Целевая версия общего OpenAPI приложения: `1.2.0`. Этот документ — заранее согласованный контракт для параллельной разработки. Он не утверждает, что бэкенд уже реализован или проверен.

Одинаковый блок этого контракта включён в третий промпт Astra. Егор может начинать frontend по типам и JSON-примерам ниже. Astra реализует этот контракт, а не проектирует заново маршруты и названия полей. Несовместимое изменение требует новой согласованной версии обоих файлов; в рамках 2.0.0 допустимы только необязательные добавления, не требующие от Егора переделки.

## К1. Пользовательский результат и границы

Два режима: «Внедрение» и «Масштабирование». Три уровня оснащения: `base`, `extended`, `max`. Калькулятор отвечает: какое оборудование нужно; сколько вложить и содержать; когда окупится или что должно измениться для окупаемости.

Быстрый старт: «Мастерская», «Цех», «Завод», «По вашим камерам». Основные поля простые, расширенные допущения раскрываются отдельно. Все вычисления оборудования, экономики, порогов и графиков делает сервер. Frontend форматирует, редактирует форму и отображает результат. Собственные прежние формулы из `calculatorEconomics.tsx` и `calculatorExample.ts` не участвуют в живом v2-расчёте.

Запрос не сохраняет расчёт и не изменяет реальные правила камер, модели или конвейер. Экономия от политики будущего внедрения — расчётное предположение, а не реализованное ускорение текущего LinQ-показа. Авторизации не добавляем: действуют существующие роли.

## К2. Маршруты, форматы и совместимость

| Метод и URL | Формат тела/ответа | Роль |
| --- | --- | --- |
| `GET /api/calculator/defaults` | Существующий `CalculatorDefaults` плюс обязательное новое поле `v2: DefaultsV2` | Как сейчас, без обязательного X-Role |
| `POST /api/calculator/rollout` или `?format=legacy` | Существующий `RolloutIn → RolloutResult` | `X-Role: management` |
| `POST /api/calculator/scale` или `?format=legacy` | Существующий `ScaleIn → ScaleResult` | `management` или `admin` |
| `POST /api/calculator/rollout?format=v2` | `RolloutRequestV2 → ResultV2` | `management` |
| `POST /api/calculator/scale?format=v2` | `ScaleRequestV2 → ResultV2` | `management` или `admin` |
| `POST /api/calculator/export.pdf` | Заранее определённая дополнительная возможность, `ExportRequestV2 → application/pdf`; при выключенной функции 501 | По `mode` тела, как у соответствующего расчёта |

Для POST параметр `format` имеет enum `legacy | v2`, default `legacy`. Новый JSON выбирается **по query**, а не эвристикой по наличию полей. Неверная схема для выбранного формата — 422, без тихого отката к legacy. Параметр `format` не нужен у PDF.

У legacy сохраняются все поля, типы, значения enum, operation ID, назначение сумм и обязательность входов из 1.1.0. В частности:
- `TierResult`: `tier,title,accelerators,servers,capex_rub,opex_rub_year,savings_rub_year,payback_months,items`;
- `RolloutResult`: `incident_cost_rub,incidents_per_1000_workers,events_per_operator_shift,tiers,assumptions`;
- `ScaleResult`: `cameras_total,analysis_fps,capacity_fps,capacity_source,accelerators_now,accelerators_total,servers_total,capex_rub,items,assumptions`;
- `CalcAssumption.value` остаётся обязательным конечным float, не превращается в nullable;
- `scale.capex_rub` — только дополнительные вложения, `savings_rub_year` — валовая годовая выгода, `opex_rub_year` — годовые расходы.

Оборудование legacy рассчитывается новым общим движком; прежняя наивная оценка хранится в v2 `steps`. Legacy-входы преобразуются в документированный адаптер, см. К12. Это один движок и два формата, а не два несогласованных калькулятора.

Раздельный v2-формат нужен, потому что старые обязательные денежные float не позволяют честно передать неполную смету через null. Новый frontend использует `?format=v2` и nullable-поля со статусами; старый не получает несовместимые поля вместо сумм.

OpenAPI публикует обе схемы request/response как `oneOf/anyOf` с описанной здесь таблицей соответствия query. OpenAPI сам не выражает зависимость варианта тела от query: её проверяет runtime и адресные тесты. Сериализатор ответа не должен выбрасывать v2-поля через legacy-модель. У v2 есть discriminator `format:"v2"` и `contract_version:"2.0.0"`.

Базовый origin и REST-заголовок `X-Role` прежние. Калькулятор не создаёт новые WS-типы. При опциональном PDF frontend показывает действие только когда `defaults.v2.features.pdf_available=true`; основной v2 от PDF не зависит.

## К3. Общие правила чисел и схем

Ниже TypeScript — точное описание JSON, а не код обязательной реализации. Все поля обязательны, кроме явно помеченных `?`. `null` означает указанную недоступность/неприменимость; отсутствие поля не заменяет null. Новые request-объекты закрытые: неизвестное поле — 422. В ответах frontend игнорирует будущие неизвестные необязательные поля.

Числа конечные; NaN/Infinity запрещены. Количества целые, денежные входы неотрицательные, доли в [0,1], знаменатели положительны. Нулевой известный тариф/цена отличаются от неизвестных null. Отрицательными могут быть чистый эффект/баланс и расчётный порог цены платы до его классификации.

Ограничения: не более 10 000 камер суммарно, 128 групп в одном ручном профиле, 32 моделей в группе, 64 разрешённых позиций каталога плат. Превышение — 422. Слишком большая техническая задача с требуемыми чипами >100 000 — 409 `calculation_limit`, а не зависание. Денежные значения в ₽, частоты в кадрах/с либо явно обозначенных эквивалентных единицах/с; мощность в Вт, энергия в кВт·ч.

Для денег расчёт ведётся Decimal или эквивалентно устойчивой арифметикой. Возвращаем денежные суммы до копеек; промежуточные деньги до итогового округления не округляются. Нагрузка/ядра/месяцы/дробные пороги возвращаются с точностью до 6 знаков после запятой. `ceil` оборудования применяется к неокруглённым величинам с защитой только от численного шума, не к показанным 6 знакам. Фронт может выводить меньше знаков.

Невостребованная позиция не требует неизвестного значения: для доказанного нулевого количества/выключенного расхода 0×null=известный0. Ноль покупаемых серверов не требует цены сервера, ноль часов электричества даёт расход0 без тарифа/мощности, нулевое число предотвращаемых случаев даёт выгоду0 без стоимости случая. Это правило не разрешает заменить неизвестное количество нулём.

`H=3` года, `12H=36` месяцев. Срок >36 месяцев возвращается числом, а не «никогда не окупается». Цена за камеру делится на N всех камер при внедрении и N добавленных камер при расширении; знаменатель явно возвращается.

## К4. Типы запросов

```typescript
type Tier = "base" | "extended" | "max";
type Mode = "rollout" | "scale";
type TierShares = { base: number; extended: number; max: number };

interface SiteInput {
  workshops: number;
  workers: number;
  shifts_per_day: number;
  working_days_year: number;
  operators: number;
}
// rollout: весь проект; scale: ДОБАВЛЯЕМАЯ область, не весь завод.

interface ManualGroup {
  id: string;
  share: number;
  model_ids: string[];
}
type CameraProfile =
  | { source: "manual"; cameras: number; groups: ManualGroup[] }
  | { source: "system"; camera_ids: number[] | null; include_seed: boolean };
// manual: сумма share=1 (допуск 1e-9); доли сервер переводит в целые количества.
// system: null выбирает все неудалённые камеры, по умолчанию include_seed=false.
// Нет enabled у Camera — не придумывать такой фильтр.

interface LoadInput {
  activity_share: number;
  activity_measurement_id: string | null;
  target_fps: number;
  surge_fps: number;
  idle_check_s: number;
  peak_mode: "independent_p95" | "all_active";
  priority_cameras_reserve: number;
  detector_stride: 1 | 2;
  reference_chip_fps: number;
  capacity_derate: number;
  platform_capacity_override_fps: number | null;
  model_cost_overrides: Record<string, number>;
  cpu_basis: "inclusive" | "split";
  cpu_ms_per_unit: number;
  decode_cores_per_camera: number;
}

interface ServerInput {
  slots: number;
  usable_cpu_cores: number;
  price_rub: number | null;
  power_w: number | null;
}
interface HardwareInput {
  allowed_board_ids: string[];
  board_price_overrides: Record<string, number | null>;
  server: ServerInput;
}
// Отсутствующий key в price_overrides: каталог; явный null: цена неизвестна.

interface InstalledInventory {
  boards: { board_id: string; count: number }[];
  servers: number;
}
// Одинаковый серверный профиль из hardware.server для существующих и новых серверов.
// Смешанные серверы разного типа в этой версии не моделируются.

interface CostInput {
  integration_fixed_rub: number | null;
  integration_per_camera_rub: number | null;
  support_share_year: number;
  electricity_rub_kwh: number | null;
  operating_hours_year: number;
  signal_zones_per_camera: number;
  signal_unit_rub: number | null;
  speaker_per_workshop_rub: number | null;
  new_camera_unit_rub: number | null;
  new_camera_count: number;
  max_additional_camera_share: number;
}
interface InjuryBenefit {
  enabled: boolean;
  annual_injured_workers: number | null;
  rate_per_1000: number | null;
  cost_per_injured_worker_rub: number | null;
  cost_scope: "direct_only" | "all_in";
  reduction: TierShares;
}
interface DowntimeBenefit {
  enabled: boolean;
  events_year: number | null;
  days_per_event: number | null;
  day_cost_rub: number | null;
  reduction: TierShares;
}
interface FineItem {
  id: string;
  title: string;
  inspection_probability_year: number;
  amount_rub: number | null;
  reduction: TierShares;
}
interface BenefitInput {
  injuries: InjuryBenefit;
  downtime: DowntimeBenefit;
  fines: { enabled: boolean; items: FineItem[] };
  sfr_discount: {
    enabled: boolean;
    payroll_rub_year: number | null;
    tariff_share: number | null;
    additional_discount_share: number | null;
  };
  labor: {
    monetize: boolean;
    rows: {
      id: string;
      title: string;
      hours_saved_year: number;
      hour_cost_rub: number | null;
    }[];
  };
  severe_injury_cost_rub: number | null;
}

interface CommonRequestV2 {
  contract_version: "2.0.0";
  preset_id: string | null;
  site: SiteInput;
  load: LoadInput;
  hardware: HardwareInput;
  costs: CostInput;
  benefits: BenefitInput;
}
interface RolloutRequestV2 extends CommonRequestV2 {
  cameras: CameraProfile;
}
interface ScaleRequestV2 extends CommonRequestV2 {
  current: CameraProfile;
  added: CameraProfile;
  installed: InstalledInventory | null;
}
type ExportRequestV2 =
  | { mode: "rollout"; input: RolloutRequestV2 }
  | { mode: "scale"; input: ScaleRequestV2 };
```

### Семантика входов, которую нельзя угадывать

- `preset_id` — происхождение заполнения формы. Пресет возвращается полным запросом из defaults; после редактирования тело запроса авторитетно. По preset_id сервер **не переустанавливает** введённые числа и не загружает скрытые значения.
- `site.workshops`: rollout ≥1, scale ≥0; workers/operators ≥0; shifts 0…3; working_days 1…366.
- Для manual с N>0 группы непустые; share>0, уникальные id, сумма1. При N=0 groups=[]; нулевой rollout допустим как состояние «нет проекта». В масштабе current может быть0, added может быть0.
- Целые количества групп получают методом наибольших остатков: floor(N·share), остаток по убыванию дробной части, равенство — id по возрастанию. Нулевые группы в результате опускаются. В графике применяется тот же метод.
- В каждой непустой группе ровно одна модель `kind=detector`. Другие model_ids уникальны и известны каталогу. Нулевые/отрицательные модельные веса запрещены. Известная модель с неизвестной стоимостью допустима, но делает нагрузку неполной; неизвестный ID — 422.
- Для system модельные наборы берутся из эффективных включённых правил камер, требуемых классов и текущего реестра; detector всегда, pose только где нужна, extra — по необходимым классам. Нет модели — показывается missing, а не происходит тихое удаление сценария из нагрузки. Непроверенный класс не объявляется работающим.
- system с пустым/неподходящим набором возвращает 200 с N=0 и предупреждением; не подменяет данные пресетом. Указанный отсутствующий/deleted camera ID — 422. Если источники current/added используют один ID — 422; реальные добавляемые камеры обычно задаются manual.
- `activity_measurement_id=null`: доля задана в расчёте/конфиге; измерение не применяется само. Непустой ID разрешён только для существующего измерения из defaults с совпадающим числом (допуск1e-9), иначе422 `MEASUREMENT_MISMATCH`. После ручной правки доли frontend сбрасывает ID в null.
- 0<surge_fps≤target_fps≤120; idle_check_s>0 и 1/idle_check_s≤target_fps/detector_stride. Reference FPS>0, 0<derate≤1. CPU ms≥0; при cpu_basis=inclusive decode_cores_per_camera=0, split допускает отдельный неотрицательный decode.
- `priority_cameras_reserve` — неотрицательное целое до10 000; эффективный q=min(задано,N). Полная частота предусматривается лишь для q одновременных тревожных камер, а не для неограниченного их числа.
- `detector_stride=2` разрешён только если defaults.v2.features.tracker.available=true и есть подходящий отчёт проверки без потерянных событий. По умолчанию1. Не валидировано —422 `TRACKER_NOT_VALIDATED`; сервер не включает альтернативу молча.
- `costs.new_camera_count` — физические покупки для базового уровня, 0…Nscope. Nscope=N при rollout и Nadded при scale. На максимальном уровне дополнительно min(Nscope−new_camera_count,ceil(Nscope·max_additional_camera_share)). Это не повышает число анализируемых камер: речь о замене/оснащении уже посчитанных каналов.
- injuries: явное annual_injured_workers приоритетнее rate; если оно null, используется workers·rate/1000. Нельзя путать пострадавших с событиями Argus.
- enabled=false выгода даёт0, не требует заполнения её денежных null. enabled=true с недостающим входом — полезный 200/partial с missing, не 422. Значения0 действительны; отсутствие обозначается null.
- Только при `injuries.enabled=true` значение `cost_scope=all_in` несовместимо с enabled downtime или fines, а также с monetize=true и ненулевыми часами labor:422 `DOUBLE_COUNTING`. При выключенной injury-строке её сохранённый scope не блокирует другие выгоды. direct_only означает, что стоимость пострадавшего не включает отдельно считаемые простой, штрафы и время контроля.
- `sfr_discount.additional_discount_share` — дополнительная доля скидки к действующему тарифу, не уже полученная заводом; диапазон0…0.4. По умолчанию скидка выключена.
- Часы labor показываются всегда. В деньги включаются лишь при monetize=true, что означает изменение штата/оплачиваемых переработок. Незаполненная цена часа при monetize=true и ненулевых часах даёт missing.

## К5. Полные типы результатов, defaults и состояний

```typescript
type NumberStatus = "known" | "assumed" | "derived" | "missing" | "not_applicable";
type ResultStatus = "ready" | "estimated" | "partial" | "empty";
type SourceKind = "argus_measurement" | "vendor_claim" | "official" | "team_assumption" | "user_input";
// user_input: введённые заводом цены/параметры, без выдачи за измерение Argus.
type Verification = "verified_primary" | "cached_primary" | "pending_primary" | "not_applicable";

interface SourceRecord {
  id: string;
  title: string;
  kind: SourceKind;
  verification: Verification;
  url: string | null;
  data_year: number | null;
  published_at: string | null;
  checked_at: string | null;
  note: string;
}
interface NumericEvidence {
  key: string;
  title: string;
  value: number | null;
  unit: string;
  status: NumberStatus;
  source_ids: string[];
  formula: string | null;
  depends_on: string[];
  reason: string | null;
}
interface Notice {
  code: string;
  field: string | null;
  message: string;
}
interface ResolvedGroup {
  id: string;
  cameras: number;
  camera_ids: number[];
  model_ids: string[];
}
interface ResolvedProfile {
  cameras: number;
  groups: ResolvedGroup[];
}
interface ModelLoad {
  id: string;
  title: string;
  kind: "detector" | "pose" | "extra";
  work_units: number | null;
  execution_status: "verified_linq" | "local_only" | "unverified" | "missing";
  source_ids: string[];
}
interface BoardOffer {
  id: string;
  title: string;
  chips: number;
  slots: number;
  power_w: number | null;
  price_rub: number | null;
  source_ids: string[];
}
interface TrackerFeature {
  available: boolean;
  max_stride: 1 | 2;
  report_ref: string | null;
}
interface OfflineEconomy {
  report_ref: string;
  full_calls: number;
  policy_calls: number;
  reduction_share: number;
  matched_events: number;
  lost_events: number;
  new_events: number;
  confirm_shift_p90_ms: number | null;
  note: string;
}
interface FeaturesV2 {
  tracker: TrackerFeature;
  pdf_available: boolean;
  offline_economy: OfflineEconomy | null;
}
interface Measurement {
  id: string;
  key: "activity_share" | "platform_fps" | "rtt_p50_ms" | "inflight"
    | "inference_p50_ms" | "inference_p90_ms" | "events_per_camera_day";
  title: string;
  value: number | null;
  unit: string;
  status: "measured" | "not_measured";
  period_start: string | null;
  period_end: string | null;
  sample_count: number;
  source_ids: string[];
  note: string;
}
interface MarketReference {
  id: string;
  title: string;
  billing: "monthly_per_camera" | "one_off_per_camera" | "project";
  amount_rub: number | null;
  scope: string;
  source_ids: string[];
}
interface PresetV2 {
  id: "workshop" | "shop" | "plant";
  title: string;
  area_m2: number | null;
  machines: number | null;
  note: string;
  rollout: RolloutRequestV2;
}
interface FieldLimit {
  field: string;
  min: number | null;
  max: number | null;
  integer: boolean;
}
interface DefaultsV2 {
  format: "v2";
  contract_version: "2.0.0";
  formula_version: "argus-calc-2.0";
  rollout: RolloutRequestV2;
  scale: ScaleRequestV2;
  presets: PresetV2[];
  system_profile: ResolvedProfile;
  models: ModelLoad[];
  boards: BoardOffer[];
  assumptions: NumericEvidence[];
  measurements: Measurement[];
  market: MarketReference[];
  features: FeaturesV2;
  limits: FieldLimit[];
  sources: SourceRecord[];
  notices: Notice[];
}
// CalculatorDefaults 1.1.0 сохраняется и получает v2: DefaultsV2.

interface LoadResult {
  cameras: number;
  active_p95: number;
  priority_cameras_effective: number;
  peak_units_s: number | null;
  surge_units_s: number | null;
  required_units_s: number | null;
  effective_chip_units_s: number;
  required_chips: number | null;
  required_cpu_cores: number | null;
  naive_chips: number | null;
  basis: "independent_p95" | "all_active";
}
interface EquipmentState {
  boards: { board_id: string; count: number }[];
  chips: number;
  servers: number;
  used_slots: number;
  power_w: number | null;
}
interface HardwareResult {
  selection: "priced_optimum" | "technical_only" | "unresolved";
  inventory_basis: "none" | "provided" | "estimated";
  before: EquipmentState | null;
  purchase: EquipmentState | null;
  after: EquipmentState | null;
  required_before_chips: number | null;
  required_after_chips: number | null;
  spare_chips_after: number | null;
  board_capex_rub: number | null;
  server_capex_rub: number | null;
  note: string;
}
interface MoneyLine {
  id: string;
  title: string;
  amount_rub: number | null;
  included: boolean;
  status: NumberStatus;
  evidence_keys: string[];
}
interface PaybackResult {
  status: "within_horizon" | "after_horizon" | "no_positive_effect"
    | "no_initial_investment" | "insufficient_data" | "not_applicable";
  months: number | null;
  within_horizon: boolean | null;
  reason: string;
}
interface SevereThreshold {
  status: "required" | "already_covered" | "needs_input" | "not_applicable";
  expected_prevented_cases: number | null;
  whole_prevented_cases: number | null;
  uncovered_cost_rub: number | null;
  reason: string;
}
interface PriceThreshold {
  status: "at_or_below" | "already_within" | "free_still_insufficient"
    | "not_applicable" | "insufficient_data";
  board_id: string | null;
  boards_to_buy: number;
  max_unit_price_rub: number | null;
  current_unit_price_rub: number | null;
  reason: string;
}
interface TierResultV2 {
  tier: Tier;
  title: string;
  capex_rub: number | null;
  opex_rub_year: number | null;
  gross_benefit_rub_year: number | null;
  net_benefit_rub_year: number | null;
  tco_3_year_rub: number | null;
  net_balance_3_year_rub: number | null;
  rub_per_camera_month: number | null;
  camera_denominator: number;
  labor_hours_year: number;
  capex_lines: MoneyLine[];
  opex_lines: MoneyLine[];
  benefit_lines: MoneyLine[];
  payback: PaybackResult;
  severe_threshold: SevereThreshold;
  board_price_threshold: PriceThreshold;
}
interface StepV2 {
  id: "naive" | "dedicated_capacity" | "scenario_models" | "activity_pool" | "tracker";
  title: string;
  available: boolean;
  chips: number | null;
  servers: number | null;
  equipment_capex_rub: number | null;
  reason: string;
}
interface CurvePoint {
  cameras: number;
  chips: number | null;
  servers: number | null;
  tco_3_year_rub: number | null;
  rub_per_camera_month: number | null;
}
interface ResultV2 {
  format: "v2";
  contract_version: "2.0.0";
  formula_version: "argus-calc-2.0";
  mode: Mode;
  status: ResultStatus;
  cost_scope: "whole_project" | "incremental";
  horizon_years: 3;
  resolved: {
    current: ResolvedProfile;
    added: ResolvedProfile;
    total: ResolvedProfile;
    input: RolloutRequestV2 | ScaleRequestV2;
  };
  load: LoadResult;
  hardware: HardwareResult;
  tiers: TierResultV2[];
  steps: StepV2[];
  scale_curve: {
    scope: "greenfield_reference";
    tier: "base";
    points: CurvePoint[];
    note: string;
  };
  operator_events_per_shift: number | null;
  evidence: NumericEvidence[];
  sources: SourceRecord[];
  warnings: Notice[];
  missing: Notice[];
}
interface ApiErrorExisting {
  code: string;
  message: string;
  details: Record<string, string | number | null>;
}
```

Всегда три tier в порядке base/extended/max и пять step в указанном порядке. Недоступная tracker-ступень остаётся с available=false и null числами; её не изображают достигнутой. `scale_curve.points` всегда имеет 5,10,25,50,100,200,500 камер; при отсутствии расчётного профиля числа null и причина в missing.

Статусы результата:
- `empty`: Ntotal=0; денежные итоги0, per-camera/payback null, нет покупки.
- `partial`: хотя бы один необходимый технический/включённый денежный вход неизвестен. Известные части сохранены, недоступные итогиnull.
- `estimated`: расчёт полный, но есть командные/вендорские допущения, непроверенные первичные данные либо оценённый инвентарь.
- `ready`: расчёт полный без таких допущений. Это не обещание фактического предотвращения травм.

Поле из missing обязательно объясняет конкретную причину. `null` в неприменимом пороге сам по себе не делает результат partial. Отключённая выгода имеет amount=0,included=false,status=not_applicable.

У каждого предметного численного входа есть запись evidence, у вычисленных основных итогов — formula и depends_on. Ключи стабильны: `load.required_units_s`, `load.required_chips`, `hardware.board_capex_rub`, `tier.base.capex_rub`, `tier.base.opex_rub_year`, `tier.base.tco_3_year_rub` и т.д. Массивы MoneyLine ссылаются на соответствующие evidence_keys. ID/номера версий/индексы списков не являются экономическими допущениями. Все source_ids должны разрешаться в sources ответа либо defaults той же версии; response содержит использованные источники для самостоятельной проверки.

## К6. Формулы нагрузки и смысл сравнений

### Единицы и модели

Опорная единица — стоимость одного запуска опорной модели на LinQ. `reference_chip_fps=104.8` — заявление вендора для yolov8n-pose/batch1, не замер Argus и не гарантия для всех моделей. Эффективная ёмкость `C=reference_chip_fps·capacity_derate`; default derate=.5, C=52.4 эквивалентных единиц/с.

Вес pose=1 по определению опоры. Вес detector=1 — явно подписанное допущение команды. Для extra-моделей без измерения/допущения вес null; их нельзя считать бесплатными или автоматически такими же. Пользователь может явно задать положительный model_cost_override, который отмечается как своё допущение.

Для группы g: n камер, d — вес detector, x — сумма остальных весов, f — target_fps, s — detector_stride, i=1/idle_check_s, b=min(f,surge_fps).

```text
active_g = f × (d/s + x)
idle_g   = i × d
surge_g  = b × (d/s + x)
```

Неподвижный отслеживаемый человек сохраняет камеру активной. Для пустой камеры контрольный кадр только detector; ожидание motion detector ~0.2с — проектное допущение, а не реализованная характеристика этой версии конвейера.

### Пик и всплеск

N=Σn. A95 — минимальное k с P(Bin(N,p)≤k)≥.95; для N=0 это0, p=0 даёт0, p=1 даётN. При peak_mode=all_active A95=N, подпись объясняет консервативный режим.

Для смешанных моделей сортируем группы по убыванию приращения active_g−idle_g, при равенстве id по возрастанию; берём A95 самых дорогих камер. Обозначим такую сумму Top(k,delta).

```text
peak  = Σ(n_g × idle_g) + Top(A95, active_g − idle_g)
q     = min(priority_cameras_reserve,N)
surge = Σ(n_g × surge_g) + Top(q, active_g − surge_g)
U     = max(peak,surge)
chips = ceil(U/C)
cpu   = U × cpu_ms_per_unit / 1000 + N × decode_cores_per_camera
```

Биномиальная независимость — допущение; синхронная пересменка покрывается surge и выбранным резервом, а полный одновременный максимум — all_active/q=N. Подпись не обещает полную частоту более чем q тревожным камерам. Default q=1 — допущение, не универсальный норматив.

77мс из брифа — консервативная оценка общего конвейера с хвостом и декодом. Default cpu_basis=inclusive, decode=0. Для отдельно учитываемого декода пользователь выбирает split и явно задаёт значения; это не два независимых подтверждённых измерения.

### Исправление примера трекера из брифа

Шаг detector=2 не уменьшает частоту pose/extra. Для восьми одинаковых камер detector+pose при p=.5:

```text
без трекера: A95=6, peak=144.5, chips=3
только detector через кадр: peak=108.5, chips=3
```

Брифовые2 получаются при сокращении всех моделей либо при другой смеси камер. Их нельзя зашивать в тест одинакового detector+pose. Для смеси4 detector+pose и4 detector-only получаются peak120.5/84.5 и chips3/2 при stride1/2. Трекер остаётся выключенным до проверки сохранности событий.

### Ступеньки

Все ступени используют одинаковые камеры, аппаратный каталог и CPU/слотовые ограничения:

1. `naive`: N·f·M_full / platform_capacity_fps, M_full — сумма весов всех разных моделей профиля; denominator — измеренная общая очередь либо подписанный default12.4. Это сравнение старого подхода, не паспорт чипа.
2. `dedicated_capacity`: та же нагрузка N·f·M_full, denominator C.
3. `scenario_models`: все камеры активны, только нужные им модели, stride1.
4. `activity_pool`: peak/surge по формулам выше, stride1.
5. `tracker`: те же peak/surge, detector_stride2, только если validated.

Каждая ступень возвращает потребность chips/servers и CAPEX только оборудования, без пусконаладки. Ступенька вправе не уменьшить число плат. Для неизвестных модельных весов соответствующая ступень неполная.

Наивная ёмкость площадки, RTT, inflight и измерения inference_time показываются справкой отдельно. Не выводить производительность чипа из 4/RTT как точный закон: это объяснение очереди, а не паспортный benchmark.

## К7. Подбор оборудования и масштабирование

Каталог по умолчанию: HP —1 чип, HPD —2, HPQ —4, сведения в К11. Slots задаются конфигом; default1 слот на плату — допущение, а не обещание совместимости любого сервера.

Ищем минимальный CAPEX плат+добавленных серверов среди допустимых комбинаций с известными ценами и характеристиками. Обе причины серверов учитываются вместе:

```text
servers_required_total = max(
  ceil((installed_slots + purchased_slots) / slots_per_server),
  ceil(required_cpu / usable_cpu_cores)
)
servers_to_buy = max(0, servers_required_total − installed_servers)
new_chips_needed = max(0, required_chips − installed_chips)
```

Новые платы должны покрывать new_chips_needed, итоговые слоты/CPU — размещаться в имеющихся+новых серверах. При равной цене: меньше новых серверов → меньше новых плат → меньше лишних чипов → лексикографический board_id. Используется ограниченный точный перебор/DP, не сложная внешняя система оптимизации.

Из перебора исключаются неизвестные цены, не заменяются нулём. Если нет ни одной оценённой допустимой комбинации, строится техническая комплектация по критерию минимум новых плат → минимум лишних чипов → ID; selection=technical_only, денежные итоги с неизвестной позициейnull. Она не называется самой дешёвой. При неизвестной нагрузке selection=unresolved, purchase/after null, сохранён before.

allowed_board_ids ограничивает только новые покупки. Реальный installed может содержать любой известный каталогу board_id. Повторяющиеся board_id в installed и повторы allowed_board_ids запрещены422. Неизвестный power не исключает пригодную по CAPEX/технике плату, но ограничивает энергетическую смету.

Для rollout before — нулевой инвентарь, inventory_basis=none. Для scale:
- installed задан — используются реальные количества, inventory_basis=provided;
- installed=null — инвентарь оценивается оптимальным greenfield-планом current, inventory_basis=estimated и предупреждение;
- если нагрузка current неизвестна и оценить инвентарь нельзя, before=null, selection=unresolved,purchase/after=null; это не нулевой инвентарь. Фактически переданный installed сохраняется даже при неизвестной нагрузке;
- имеющиеся платы не продаются и не создают отрицательную покупку;
- отсутствие цены существующей платы не мешает считать нулевую покупку, но её неизвестная мощность может ограничить итоговую энергетическую справку;
- installed servers должны вмещать указанные установленные платы по slots; противоречивый инвентарь —422 `INVENTORY_CAPACITY`;
- chips в old legacy accelerators_now остаются расчётной потребностью старых камер, а фактический инвентарь отображается только v2; их нельзя смешать.

Мощность after = Σboard_count·board_power + servers·server_power. В scale для расходов берётся мощность **добавленного** оборудования; неизменившиеся старые мощности не оплачиваются второй раз. Паспортные максимумы дают оценку сверху, не измеренное потребление.

Для added=0 при достаточном инвентаре нет покупки, пусконаладки и добавочных выгод. Если before объективно не покрывает existing workload, допускается техническая докупка с предупреждением `EXISTING_CAPACITY_SHORTFALL`: её стоимость не скрываем за «ничего не добавлено».

## К8. Стоимость, выгоды, окупаемость и пороги

Обозначим Nscope=N для rollout, Nadded для scale. Все три уровня используют одинаковую вычислительную комплектацию.

```text
equipment = board_purchase_cost + server_purchase_cost
integration = integration_fixed + Nscope × integration_per_camera
base = equipment + integration + new_camera_count × camera_price
extended = base + Nscope × signal_zones_per_camera × signal_price
max = extended + site.workshops × speaker_price
    + min(Nscope−new_camera_count,ceil(Nscope×max_additional_camera_share)) × camera_price
```

Когда Nscope=0, integration=0 и дополнительные камера/сигнал/громкоговоритель=0. Расходы реальной докупки недостающих старых мощностей всё же показываются. При Ntotal=0 весь проектempty.

Support_t=C_t·support_share_year. Electricity=(power_scope_w/1000)·operating_hours_year·electricity_rub_kwh. Значение8760 — год работы24/7, ватты обязательно делятся на1000.

Для каждой tier выгоды:

```text
injured_year = annual_injured_workers, если задано;
              иначе workers × rate_per_1000 / 1000
B_injury_t = injured_year × direct_cost_per_injured_worker × reduction_t
B_downtime_t = events_year × days_per_event × day_cost × reduction_t
B_fines_t = Σ(inspection_probability_year × fine_amount × reduction_t)
B_sfr = payroll_year × tariff_share × additional_discount_share
hours = Σ(hours_saved_year)
B_labor = Σ(hours_saved_year × hour_cost), только если monetize
B_t = сумма включённых строк
```

Штрафы — ожидаемая оценка риска, не гарантированная ежегодная экономия. Отключённая строка0; включённая неизвестная строкаnull, итог Bnull. Расходы относятся именно к предприятию, выплаты фонда не считаются экономией завода. Фактический простой задаётся отдельно: сроки расследования3/15 дней не означают остановку участка на3/15 дней.

```text
O_t = support_t + electricity
net_year_t = B_t − O_t
TCO3_t = C_t + 3 × O_t
net_balance3_t = 3 × B_t − TCO3_t
rub_camera_month_t = TCO3_t / (Nscope × 36), Nscope>0
payback_months_t = 12 × C_t / net_year_t, только net_year_t>0
```

Пограничные состояния:
- данных не хватает — payback.insufficient_data и monthsnull;
- net_year≤0 — no_positive_effect, monthsnull;
- C=0 и net_year>0 — no_initial_investment, months0;
- C>0 и0<months≤36 — within_horizon;
- months>36 — after_horizon, само число сохраняется;
- empty — not_applicable. Если C=0,net=0, расходов/выгод нет — not_applicable, а не «моментальная окупаемость».

### Порог предотвращённых тяжёлых случаев

Это **общее необходимое** предотвращённое число за3 года, не дополнительная выгода поверх уже включённой injury-строки.

```text
B_other = сумма включённых выгод, кроме injury-строки
gap = max(0, TCO3_t − 3 × B_other)
expected_prevented_cases = gap / severe_injury_cost
whole_prevented_cases = ceil(expected_prevented_cases)
```

Здесь severe_injury_cost заменяет прямую injury-выгоду и не включает простой/штрафы/труд, уже оставленные в B_other. Если затраты уже покрыты, expected/whole0,status=already_covered. Если gap>0,а цена тяжёлого случая0/null, needs_input и количестваnull. Для empty —not_applicable. Не вычитать исходную injury-выгоду из gap второй раз.

B_other суммируется независимо: неизвестная injury-выгода не мешает этому порогу, если остальные включённые строки и TCO известны. Неизвестный TCO или неизвестная прочая включённая выгода дают needs_input. При Nscope=0 добавочные выгоды0 независимо от заполненных site/benefits.

### Порог цены платы

Порог относится к фиксированной выбранной комплектации и изменению цены одного типа покупаемой платы. Если все цены плат известны, выбирается тип с максимальным текущим вкладом в стоимость новых плат, при равенстве board_id. Если цена ровно одного покупаемого типа неизвестна, именно она становится переменной P: это позволяет назвать приемлемую цену даже до получения предложения LinQ. Тип и количество q возвращаются явно. Это не повторный глобальный подбор всех комбинаций.

Для порога достаточно известных C_other, r, F и B: неизвестная текущая цена выбранной платы и вызванные ею null в полном CAPEX/TCO не блокируют формулу. current_unit_price_rub в таком случае null. Если неизвестны цены нескольких независимо покупаемых типов, прочие затраты либо включённые выгоды, возвращается insufficient_data. Не подставлять неизвестные прочие цены как0.

Пусть C(P)=C_other+qP, r=support_share_year, F=electricity, B=B_t.

```text
Pmax = [3 × (B − F) / (1 + 3r) − C_other] / q
```

q=0 —not_applicable. Pmax<0 —free_still_insufficient и max_unit_price_rub=null; нулевая цена не решает окупаемость. Pmax=0 —допустимая граница0. Если известная текущая цена≤Pmax —already_within; иначеat_or_below, в том числе при неизвестной текущей цене и вычисленном неотрицательном пороге. Учитывать зависимость поддержки от CAPEX, не вычитать цену платы только из первоначальной покупки.

Показанный max_unit_price_rub округляется вниз до копейки, чтобы не превысить допустимый порог. Статус определяется по неокруглённой величине; денежный вектор К13 до округления приведён отдельно.

### Кривая масштаба

Точки5/10/25/50/100/200/500, тот же p, модельная смесь total, нагрузочная политика и цены, заново рассчитанные аппаратные ступени. Состав групп масштабируется методом наибольших остатков от total. Это `greenfield_reference` базового уровня: стоимость эквивалентного **нового** внедрения без зачёта старых покупок. На экране масштабирования не выдавать эту кривую за добавочные расходы текущего расширения.

В каждой точке site.workshops масштабируется как max(1,ceil(original_workshops·Npoint/Ntotal)), physical new_camera_count — по прежней доле покупок; для base громкоговоритель не влияет. Пусконаладка fixed остаётся одной, per_camera масштабируется. Работники/выгоды для этого графика не нужны: он показывает TCO/камеру, не окупаемость условного завода. Цена камеры вправе вырасти на отдельной ступени покупки сервера.

Доля физических покупок для кривой = new_camera_count/Nscope при Nscope>0, иначе0; количество в точке=min(Npoint,ceil(Npoint×доля)). В scale ступеньки steps, как и кривая, показывают greenfield-сравнение для Ntotal, без зачёта установленного; основная hardware/tiers при этом остаётся incremental.

ID групп в resolved.current/added локальные. В resolved.total они получают префикс current: или added:; для rollout используются added:. Такой же порядок ID сохраняется при равенствах в Top/методе остатков. Это исключает коллизию двух групп all.

## К9. Defaults, измерения и источники

Default v2:
- rollout:8 камер,1 ручная группа detector+pose; site2 цеха,200 работников,2 смены,250 рабочих дней,2 оператора;
- load:p=.5,target12,surge5,idle4с,independent_p95,q1,stride1,reference104.8,derate.5,platform override null,cpu inclusive77мс,decode0;
- HP500000₽,HPD/HPQ null; сервер4 слота,16 полезных ядер,350000₽,250Вт — все параметры сервера являются командными допущениями;
- integration300000₽+0₽/камеру,support.15,electricity8₽/кВт·ч,hours8760,zones1,signal25000₽,speaker40000₽,camera30000₽,new_camera_count0,max_extra_share.2;
- injuries enabled,annualnull,rate1.17,cost1000000₽,direct_only,reduction .2/.3/.4; сумма прямых потерь — редактируемое допущение, не стоимость травмы по закону;
- downtime disabled,events/days/day_cost null,reduction .2/.3/.4;
- fines disabled; шаблоны general_ohs65000 и ppe140000, probability.1,reduction .2/.3/.4 — выбор внутри справочного диапазона и вероятность являются допущениями;
- sfr disabled,payroll/tariff/delta null;
- labor monetizefalse,две строки ohs/operator,часов0,ценачасаnull;
- severe_injury_cost=null: пользователь задаёт реальную прямую стоимость, порог показывает needs_input;
- scale по умолчанию current8+added8, те же модели,installednull; site описывает добавляемую область, а не вторично весь завод. new_camera_count8 — предположение о покупке физических камер, можно снизить до0.

GET defaults.v2.notices содержит информационные строки SFR_PREVENTION_INFO и SFR_DISCOUNT_CONDITIONS: возможное согласуемое возмещение не вычитается из CAPEX, скидка тарифа не возникает автоматически от покупки Argus. Соответствующие source_id включаются в defaults.v2.sources. Рыночные ориентиры должны различать подписку и разовую лицензию; неперепроверенные примеры помечаются pending_primary, не выдаются за новый действующий прайс.

site.working_days_year — справочное описание завода/пресета. При отдельно заданных годовых часах и годовых суммах оно не пересчитывает расходы/выгоды автоматически; не обещать обратного. Каждая цена/доля, отличающаяся от выбранного серверного defaults, получает источник user_input «задано в расчёте». Неизменённое значение сохраняет источник defaults; ссылка на замер допустима только через проверенный measurement_id.

Пресеты содержат полные v2-rollout тела:
- workshop «Мастерская»:5 камер,100м²,5 станков,1 цех,50 работников,1 смена,1 оператор;
- shop «Цех»:10000м²,20 камер по допущению2 камеры/1000м²,1 цех,200 работников,2 смены,2 оператора;
- plant «Завод»:200 камер,4 цеха,2000 работников,3 смены,4 оператора; площадьnull.
Работники/смены/дни/плотность/модельная смесь — изменяемые допущения. Все три стартуют с detector+pose на всех камерах; пользователь/системные правила могут дать другую смесь. Нельзя выдать ровно эту смесь за реальные требования любого завода.

По каждой доступной реальной камере активность — доля обработанных кадров с человеком score≥high_thresh из исходных LinQ-артефактов; одинаковые кадры detector/pose не считаются дважды, один набор видео/артефактов не множится циклами эфира. Сводка — медиана долей камер с валидными данными. Нет данных —not_measured, не0. Применение —явная кнопка. Подпись: демо-видео отобраны ради нарушений, на пилоте требуется новый замер.

Measurement.id неизменяем для одного содержимого: новое значение/период/выборка создаёт новый ID, например digest содержимого. Не переиспользовать старый ID с новой величиной; корректно заполненная форма не должна неожиданно менять источник.

Platform FPS — медиана валидных настоящих linq/fake=false throughput; при отсутствии сравнение naive использует командный12.4 с подписью. RTT/inflight отдельно. inference_time показывается только при наличии поля, p50/p90, с предупреждением о неподтверждённом смысле поля организаторами; если поля нет, соответствующие строки measurements опускаются.

Events_per_camera_day и operator_events_per_shift — информационные показатели, не прогноз травм и не денежная выгода. Учитывать события is_demo=0, не superseded, без повторного счёта одного event; источник указывает период и камеры. operator_events_per_shift=events_per_camera_day·Nscope/(operators·shifts), либоnull при отсутствии данных/нулевом знаменателе. Не называть это устойчивой оценкой после короткого демо.

Обязательные предупреждения, когда применимы:
`MODELED_POLICY_NOT_DEPLOYED`, `INDEPENDENT_ACTIVITY_ASSUMPTION`, `PRIORITY_RESERVE_LIMIT`, `MODEL_WEIGHT_ASSUMED`, `VENDOR_CAPACITY_NOT_APP_MEASUREMENT`, `PLATFORM_QUEUE_NOT_CHIP`, `DEMO_ACTIVITY_BIASED`, `SOURCE_PENDING_PRIMARY`, `INVENTORY_ESTIMATED`, `EXISTING_CAPACITY_SHORTFALL`.
Недостающие данные:
`MODEL_COST_UNKNOWN`, `SCENARIO_MODEL_MISSING`, `BOARD_PRICE_UNKNOWN`, `SERVER_PRICE_UNKNOWN`, `POWER_UNKNOWN`, `BENEFIT_INPUT_MISSING`.
Это коды для отображения/тестов, message приходит по-русски. Могут добавляться новые необязательные коды; неизвестный code frontend показывает по message.

## К10. Ошибки и поведение фронтенда

Сохраняется `ApiErrorExisting`, без массивов/объектов в details. Ключ `details.field` — точное поле, например `load.activity_share`, `hardware.board_price_overrides.HP`. Дополнительный `details.reason` — строка кода причины.

| HTTP | code | Причина |
| --- | --- | --- |
| 400 | role_required | Нет X-Role или роль нераспознана |
| 403 | forbidden_role | Роль известна, но не разрешена |
| 422 | validation | Неверное число/схема/query/поле; details.field и details.reason |
| 409 | calculation_limit | Ограничение вычислительного объёма |
| 501 | not_implemented | Только заранее описанная выключенная функция PDF |
| 500 | internal | Непредвиденная ошибка без секретов/traceback в UI |

200 partial не является HTTP-ошибкой. Недостающая цена/измерение не маскируется нулём и не уничтожает технический результат.

Для validation reason предусмотрены `SCHEMA_MISMATCH`, `UNSUPPORTED_VERSION`, `OUT_OF_RANGE`, `UNKNOWN_FIELD`, `UNKNOWN_MODEL`, `UNKNOWN_BOARD`, `GROUP_SHARES`, `DUPLICATE_CAMERA`, `MEASUREMENT_MISMATCH`, `TRACKER_NOT_VALIDATED`, `DOUBLE_COUNTING`, `INVENTORY_CAPACITY`, `LEGACY_REQUIRES_PRICING`. При нескольких ошибках указывается первая по стабильному порядку полей; не требуется новый формат multi-error.

В v2 details.field не имеет префикса body.: load.activity_share, а для query —format. Нормализация относится только к calculator-v2 и не меняет общую обработку ошибок остальных legacy-маршрутов.

Frontend:
1. Получает defaults, берёт полное `v2.rollout`/`v2.scale` или тело пресета, редактирует значения.
2. «По вашим камерам» переключает профиль на system; «Подставить активность» отдельно копирует измерение и ID.
3. Отправляет в соответствующий POST с format=v2, ролью и JSON.
4. Пока идёт пересчёт, сохраняет предыдущий результат с явной пометкой; поздний ответ старого запроса не заменяет новый. При422 подсвечивает field.
5. Отображает готовое/оценочное/частичное/пустое состояния; null — «нужно значение/нет данных/неприменимо» по reason, ноль — известный ноль.
6. Все суммы, графики, пороги и рыночные ориентиры берёт с сервера. Допустим только отдельно подписанный статический пример из этих же fixtures, без тихой подмены живого расчёта.
7. Не обещает доступный трекер/PDF/офлайн-проверку, если capability выключена.
8. Сохраняет стиль существующего экрана Егора: добавляет данные/секции, не устраивает редизайн.

## К11. Проверенная первичная база и явные поправки к UPGRADE

Источники нужно хранить в конфиге с датой/типом проверки, а не хардкодить в frontend. Ключи ниже стабильны; URL не подтверждает успешную новую загрузку документа.

| source_id | Содержание и правильная квалификация |
| --- | --- |
| `vendor_modules` | [Производитель](https://lin-q.ru/sol): HP1,HPD2,HPQ4 чипа. Проверено25.10.2026. |
| `vendor_pose_benchmark` | [Презентация2026](https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf):104.8FPS yolov8n-pose,batch1. Сохранённая первичная выписка `Deep-Research/research_link_platform/_WORK/W2_H/PRIMARY_FETCH.json`; прямая повторная загрузка недоступна. verification=cached_primary. |
| `vendor_board_power` | [HP](https://files.lin-q.ru/tpu/docs/_HPact_manual_LINQ_HP1M_02.pdf), [HPD](https://files.lin-q.ru/tpu/docs/_HPDpass_manual_LINQ_HPD1M_01.pdf), [HPQ](https://files.lin-q.ru/tpu/docs/_HPQpass_manual_LINQ_HPD1M_10.pdf): верхние границы35/100/150Вт конкретных исполнений. cached_primary, не измерение потребления. При выдаче разбить на отдельные source_id с суффиксами _hp/_hpd/_hpq. |
| `team_defaults` | Цена HP500000,server350000/16cores/4slots/250W,derate.5,detectorweight1,CPU77 и экономические цены/эффекты — допущения. |
| `rosstat_injury_rate` | [Росстат](https://rosstat.gov.ru/working_conditions): локальный `docs/ECONOMICS_SOURCES.md` указывает1.17 пострадавших/1000,2025,публикация2026; первичный массив при подготовке недоступен. verification=pending_primary, не объявлять заново проверенным фактом. |
| `labor_investigation` | [СФР: расследование](https://sfr.gov.ru/employers/lk_insurer/baza_znanij/nesch_sluchai_na_proizvod/rassledovanie/):3/15дней — сроки расследования, не длительность остановки цеха. |
| `sfr_discount` | [СФР21.10.2026](https://sfr.gov.ru/branches/novgorod/news~2026/10/21/285762): скидка тарифа до40% при условиях/заявлении, не автоматически от покупки Argus. |
| `sfr_prevention` | [Текущие правила СФР](https://sfr.gov.ru/employers/lk_insurer/baza_znanij/finansovoe_obespechenie_predupreditelnih_mer): приказ347н11.07.2024, согласуемое возмещение, до20%/условное увеличение до30%. Ссылка467н из брифа не закрепляется как актуальная. Пригодность покупки Argus не доказана. |
| `fines_reference` | КоАП5.27.1ч1/ч4: справочные диапазоны50–80/130–150тыс для юрлиц. [Официальное разъяснение](https://epp.genproc.gov.ru/ru/proc_11/activity/legal-education/explain/e149481/); старое разъяснение не заменяет сверку актуальной редакции. Выбранные65/140тыс — допущение в диапазоне, verification=pending_primary до новой сверки. |

HPD/HPQ ценыnull и потому не становятся «дешевле бесплатной HP». Их power/slots/совместимость конкретного исполнения уточняются конфигом; default slots1 помечен как допущение.

Информация о финансировании СФР — справочная, **не вычитается из CAPEX/TCO**. Конкурентные ориентиры берутся из `docs/ECONOMICS_SOURCES.md`/первичных прайсов, включают источник/дату/объём услуги; неизвестная или непроверенная цена может быть null. Подписка и разовая лицензия не выдаются за равнозначные услуги и не становятся самостоятельной «выгодой» в окупаемости.

Явные содержательные уточнения по сравнению с брифом: detector-only stride вместо деления всех моделей; резерв тревожных камер в surge; CPU77 как допущение inclusive; пострадавшие вместо событий; отдельный реальный простой; современная ссылка СФР; неизвестные цены не0; актуальный инвентарь для расширения. Исходный бриф сохраняется в промпте целиком, но эти правила устраняют его неоднозначности.

## К12. Legacy-адаптер и тестовая совместимость

Legacy-тело без format=v2 продолжает приниматься. Модельный профиль по legacy `models_per_frame=M` интерпретируется как единое эквивалентное количество моделей на каждой камере; может быть дробным и равным0 как раньше, новая v2-группа этого поля не имеет. Внутренние эквивалентные веса для адаптера: d=min(1,M), x=max(0,M−1); при M=0 нагрузка0. Строгий положительный вес реальной v2-модели не превращается в новый запрет ранее допустимого legacy-запроса.

Load использует новый default p/.95/surge/q и C, target FPS из pipeline; старый `accelerator.capacity_fps` — reference для naive-сравнения, не навязывается как физическая ёмкость чипа. Переопределение legacy `accelerator.capacity_fps` в запросе трактуется как явный override эффективной ёмкости для этого legacy-расчёта и отмечается в assumptions; отсутствие override выбирает C новой модели. Остальные legacy override keys сохраняют существующий смысл.

Legacy `accelerator.price_rub` отображается в цену HP, `accelerators_per_server` — в эквивалентную вместимость сервера по HP. Старый float-override >0, включая дробный, продолжает приниматься: нижняя граница серверов по нему ceil(HP_chips/accelerators_per_server), затем берётся максимум с CPU-требованием. Это совместимость абстрактного legacy-параметра, а не разрешение дробных физических слотов в v2 ServerInput. Остальные цены/доли — прежние ключи. В legacy rollout физические новые камеры учитываются только max как раньше; incident_cost=downtime+fine+treatment+lawsuit, savings=incidents_per_year·incident_cost·reduction_t. Учитываются новые расходы electricity; прежний источник/тип каждого поля сохраняется.

Legacy scale: current inventory оценивается по нынешней потребности, purchase cameras=addedN как раньше; прочие расходы интеграции в legacy scale0, новые board/server и камеры оплачиваются один раз. V2 рекомендует фактический installed и явные затраты, legacy не получает новые обязательные входы.

Старые поля non-null: для legacy отсутствующие новые каталожные альтернативы не выбираются, действует известная HP-цена из старого численного конфига. Если конфиг настолько неполон, что никакой честный денежный результат legacy невозможен, вернуть422 validation с field и reason `LEGACY_REQUIRES_PRICING`. Не отправлять null/0 вместо неизвестного и не приписывать legacy-клиенту поддержку v2 partial.

Снимок OpenAPI1.1.0 защищается отдельно: существующий test_openapi_only_grows от1.0.0 недостаточен. Проверки: старые request fixtures проходят; поля/required/enums/типы не исчезли; `create_app().openapi()` совпадает с сохранённым контрактом; v2 DTO сохраняются сериализатором и имеют discriminator.

## К13. Контрольные значения и проверка формул

Нагрузочные векторы ниже используют target12,surge5,idle.25,detector=pose=1,C52.4,stride1. CPU-колонки используют **split**:77мс/единицу + .1ядра/камеру; это отдельная тестовая конфигурация, не default inclusive.

| N | A95 | q | peak | surge | chips | CPU cores | servers16cores/4slots,HP |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 8 | 6 | 1 | 144.5 | 94 | 3 | 11.9265 | 1 |
| 8 | 6 | 6 | 144.5 | 164 | 4 | 13.428 | 1 |
| 16 | 11 | 1 | 265.25 | 174 | 6 | 22.02425 | 2 |
| 200 | 112 | 0 | 2710 | 2000 | 52 | 228.67 | 15 |
| 200 | 112 | 200 | 2710 | 4800 | 92 | 389.6 | 25 |

Восемь одинаковых камер: naive16,dedicated4,scenario_models4,activity_pool3; tracker3 при доказанном detector stride2. CPU может требовать больше серверов, чем слоты; нельзя считать servers только как ceil(chips/4).

Инвентарь8→16камер при той же split-нагрузке и ценах HP500000/server350000,прочие затраты0:
- 3HP+1server → купить3HP+1server:1850000₽;
- 4HP+1server → купить2HP+1server:1350000₽;
- 6HP+2server → купить0:0₽.
Эти суммы не включают камеры/пусконаладку: это контролируемый equipment-only вектор.

Финансовый независимый вектор: C1000000,r.1,F40000,B500000,N8:
```text
OPEX140000; net360000; payback33.333333мес
TCO3=1420000; net_balance3=80000; rub_camera_month=4930.555556
C_other500000,q1 → Pmax561538.461538
B_other200000,severe_cost400000 → gap820000, expected2.05, whole3
```

В этом независимом векторе дробные денежные значения показаны до денежного округления; JSON возвращает rub_camera_month4930.56 и Pmax561538.46.

Обязательные границы: N0/1; p0/1; точный quantileCDF; точная вместимость и чуть выше; q0/N/большеN; неизвестная extra-weight; stride1/2 и unavailable; price0/null; нет серверной цены; существующий запас; added0; поддержка0; net0; C0; payback36; zero/unknown severe cost; q_purchase0; отрицательный Pmax; NaN/Infinity; неизвестные поля/IDs/формат; несовпадающее измерение; partial и empty.

Суммы строк должны сходиться с итогами, обе реализации копий контракта иметь одинаковые examples, legacy и v2 — пользоваться одним ядром. Табличные golden vectors являются независимыми ожидаемыми числами; нельзя переписать их под ошибку реализации.

## К14. Примеры запросов, ответов и состояний

Это согласованные данные для разработки и проверки, а не ответы уже реализованного backend. Полные примеры и явно обозначенные проекции разделены; нормативная полная схема находится в К4–К5. Примеры можно сохранить как локальные fixtures для frontend, затем заменить вызовами реального API без изменения публичных полей.

## К14.1. Полный новый блок GET /api/calculator/defaults — поле v2

Ниже именно полный DefaultsV2, значение поля v2 существующего GET. Legacy-поля верхнего объекта сохраняются, но здесь не дублируются. Изолированный пример не выдаётся за фактические камеры/метрики стенда.

```json
{
  "format": "v2",
  "contract_version": "2.0.0",
  "formula_version": "argus-calc-2.0",
  "rollout": {
    "contract_version": "2.0.0",
    "preset_id": null,
    "site": {
      "workshops": 2,
      "workers": 200,
      "shifts_per_day": 2,
      "working_days_year": 250,
      "operators": 2
    },
    "load": {
      "activity_share": 0.5,
      "activity_measurement_id": null,
      "target_fps": 12,
      "surge_fps": 5,
      "idle_check_s": 4,
      "peak_mode": "independent_p95",
      "priority_cameras_reserve": 1,
      "detector_stride": 1,
      "reference_chip_fps": 104.8,
      "capacity_derate": 0.5,
      "platform_capacity_override_fps": null,
      "model_cost_overrides": {},
      "cpu_basis": "inclusive",
      "cpu_ms_per_unit": 77,
      "decode_cores_per_camera": 0
    },
    "hardware": {
      "allowed_board_ids": [
        "HP",
        "HPD",
        "HPQ"
      ],
      "board_price_overrides": {},
      "server": {
        "slots": 4,
        "usable_cpu_cores": 16,
        "price_rub": 350000,
        "power_w": 250
      }
    },
    "costs": {
      "integration_fixed_rub": 300000,
      "integration_per_camera_rub": 0,
      "support_share_year": 0.15,
      "electricity_rub_kwh": 8,
      "operating_hours_year": 8760,
      "signal_zones_per_camera": 1,
      "signal_unit_rub": 25000,
      "speaker_per_workshop_rub": 40000,
      "new_camera_unit_rub": 30000,
      "new_camera_count": 0,
      "max_additional_camera_share": 0.2
    },
    "benefits": {
      "injuries": {
        "enabled": true,
        "annual_injured_workers": null,
        "rate_per_1000": 1.17,
        "cost_per_injured_worker_rub": 1000000,
        "cost_scope": "direct_only",
        "reduction": {
          "base": 0.2,
          "extended": 0.3,
          "max": 0.4
        }
      },
      "downtime": {
        "enabled": false,
        "events_year": null,
        "days_per_event": null,
        "day_cost_rub": null,
        "reduction": {
          "base": 0.2,
          "extended": 0.3,
          "max": 0.4
        }
      },
      "fines": {
        "enabled": false,
        "items": [
          {
            "id": "general_ohs",
            "title": "Общие требования охраны труда",
            "inspection_probability_year": 0.1,
            "amount_rub": 65000,
            "reduction": {
              "base": 0.2,
              "extended": 0.3,
              "max": 0.4
            }
          },
          {
            "id": "ppe",
            "title": "Обеспечение СИЗ",
            "inspection_probability_year": 0.1,
            "amount_rub": 140000,
            "reduction": {
              "base": 0.2,
              "extended": 0.3,
              "max": 0.4
            }
          }
        ]
      },
      "sfr_discount": {
        "enabled": false,
        "payroll_rub_year": null,
        "tariff_share": null,
        "additional_discount_share": null
      },
      "labor": {
        "monetize": false,
        "rows": [
          {
            "id": "ohs",
            "title": "Инженер охраны труда",
            "hours_saved_year": 0,
            "hour_cost_rub": null
          },
          {
            "id": "operator",
            "title": "Оператор",
            "hours_saved_year": 0,
            "hour_cost_rub": null
          }
        ]
      },
      "severe_injury_cost_rub": null
    },
    "cameras": {
      "source": "manual",
      "cameras": 8,
      "groups": [
        {
          "id": "standard",
          "share": 1,
          "model_ids": [
            "det-yolov8n@640-ap9999",
            "pose-yolov8n@640-ap9999"
          ]
        }
      ]
    }
  },
  "scale": {
    "contract_version": "2.0.0",
    "preset_id": null,
    "site": {
      "workshops": 2,
      "workers": 200,
      "shifts_per_day": 2,
      "working_days_year": 250,
      "operators": 2
    },
    "load": {
      "activity_share": 0.5,
      "activity_measurement_id": null,
      "target_fps": 12,
      "surge_fps": 5,
      "idle_check_s": 4,
      "peak_mode": "independent_p95",
      "priority_cameras_reserve": 1,
      "detector_stride": 1,
      "reference_chip_fps": 104.8,
      "capacity_derate": 0.5,
      "platform_capacity_override_fps": null,
      "model_cost_overrides": {},
      "cpu_basis": "inclusive",
      "cpu_ms_per_unit": 77,
      "decode_cores_per_camera": 0
    },
    "hardware": {
      "allowed_board_ids": [
        "HP",
        "HPD",
        "HPQ"
      ],
      "board_price_overrides": {},
      "server": {
        "slots": 4,
        "usable_cpu_cores": 16,
        "price_rub": 350000,
        "power_w": 250
      }
    },
    "costs": {
      "integration_fixed_rub": 300000,
      "integration_per_camera_rub": 0,
      "support_share_year": 0.15,
      "electricity_rub_kwh": 8,
      "operating_hours_year": 8760,
      "signal_zones_per_camera": 1,
      "signal_unit_rub": 25000,
      "speaker_per_workshop_rub": 40000,
      "new_camera_unit_rub": 30000,
      "new_camera_count": 8,
      "max_additional_camera_share": 0.2
    },
    "benefits": {
      "injuries": {
        "enabled": true,
        "annual_injured_workers": null,
        "rate_per_1000": 1.17,
        "cost_per_injured_worker_rub": 1000000,
        "cost_scope": "direct_only",
        "reduction": {
          "base": 0.2,
          "extended": 0.3,
          "max": 0.4
        }
      },
      "downtime": {
        "enabled": false,
        "events_year": null,
        "days_per_event": null,
        "day_cost_rub": null,
        "reduction": {
          "base": 0.2,
          "extended": 0.3,
          "max": 0.4
        }
      },
      "fines": {
        "enabled": false,
        "items": [
          {
            "id": "general_ohs",
            "title": "Общие требования охраны труда",
            "inspection_probability_year": 0.1,
            "amount_rub": 65000,
            "reduction": {
              "base": 0.2,
              "extended": 0.3,
              "max": 0.4
            }
          },
          {
            "id": "ppe",
            "title": "Обеспечение СИЗ",
            "inspection_probability_year": 0.1,
            "amount_rub": 140000,
            "reduction": {
              "base": 0.2,
              "extended": 0.3,
              "max": 0.4
            }
          }
        ]
      },
      "sfr_discount": {
        "enabled": false,
        "payroll_rub_year": null,
        "tariff_share": null,
        "additional_discount_share": null
      },
      "labor": {
        "monetize": false,
        "rows": [
          {
            "id": "ohs",
            "title": "Инженер охраны труда",
            "hours_saved_year": 0,
            "hour_cost_rub": null
          },
          {
            "id": "operator",
            "title": "Оператор",
            "hours_saved_year": 0,
            "hour_cost_rub": null
          }
        ]
      },
      "severe_injury_cost_rub": null
    },
    "current": {
      "source": "manual",
      "cameras": 8,
      "groups": [
        {
          "id": "standard",
          "share": 1,
          "model_ids": [
            "det-yolov8n@640-ap9999",
            "pose-yolov8n@640-ap9999"
          ]
        }
      ]
    },
    "added": {
      "source": "manual",
      "cameras": 8,
      "groups": [
        {
          "id": "standard",
          "share": 1,
          "model_ids": [
            "det-yolov8n@640-ap9999",
            "pose-yolov8n@640-ap9999"
          ]
        }
      ]
    },
    "installed": null
  },
  "presets": [
    {
      "id": "workshop",
      "title": "Мастерская",
      "area_m2": 100,
      "machines": 5,
      "note": "Работники, смены, плотность и смесь моделей — редактируемые допущения.",
      "rollout": {
        "contract_version": "2.0.0",
        "preset_id": "workshop",
        "site": {
          "workshops": 1,
          "workers": 50,
          "shifts_per_day": 1,
          "working_days_year": 250,
          "operators": 1
        },
        "load": {
          "activity_share": 0.5,
          "activity_measurement_id": null,
          "target_fps": 12,
          "surge_fps": 5,
          "idle_check_s": 4,
          "peak_mode": "independent_p95",
          "priority_cameras_reserve": 1,
          "detector_stride": 1,
          "reference_chip_fps": 104.8,
          "capacity_derate": 0.5,
          "platform_capacity_override_fps": null,
          "model_cost_overrides": {},
          "cpu_basis": "inclusive",
          "cpu_ms_per_unit": 77,
          "decode_cores_per_camera": 0
        },
        "hardware": {
          "allowed_board_ids": [
            "HP",
            "HPD",
            "HPQ"
          ],
          "board_price_overrides": {},
          "server": {
            "slots": 4,
            "usable_cpu_cores": 16,
            "price_rub": 350000,
            "power_w": 250
          }
        },
        "costs": {
          "integration_fixed_rub": 300000,
          "integration_per_camera_rub": 0,
          "support_share_year": 0.15,
          "electricity_rub_kwh": 8,
          "operating_hours_year": 8760,
          "signal_zones_per_camera": 1,
          "signal_unit_rub": 25000,
          "speaker_per_workshop_rub": 40000,
          "new_camera_unit_rub": 30000,
          "new_camera_count": 0,
          "max_additional_camera_share": 0.2
        },
        "benefits": {
          "injuries": {
            "enabled": true,
            "annual_injured_workers": null,
            "rate_per_1000": 1.17,
            "cost_per_injured_worker_rub": 1000000,
            "cost_scope": "direct_only",
            "reduction": {
              "base": 0.2,
              "extended": 0.3,
              "max": 0.4
            }
          },
          "downtime": {
            "enabled": false,
            "events_year": null,
            "days_per_event": null,
            "day_cost_rub": null,
            "reduction": {
              "base": 0.2,
              "extended": 0.3,
              "max": 0.4
            }
          },
          "fines": {
            "enabled": false,
            "items": [
              {
                "id": "general_ohs",
                "title": "Общие требования охраны труда",
                "inspection_probability_year": 0.1,
                "amount_rub": 65000,
                "reduction": {
                  "base": 0.2,
                  "extended": 0.3,
                  "max": 0.4
                }
              },
              {
                "id": "ppe",
                "title": "Обеспечение СИЗ",
                "inspection_probability_year": 0.1,
                "amount_rub": 140000,
                "reduction": {
                  "base": 0.2,
                  "extended": 0.3,
                  "max": 0.4
                }
              }
            ]
          },
          "sfr_discount": {
            "enabled": false,
            "payroll_rub_year": null,
            "tariff_share": null,
            "additional_discount_share": null
          },
          "labor": {
            "monetize": false,
            "rows": [
              {
                "id": "ohs",
                "title": "Инженер охраны труда",
                "hours_saved_year": 0,
                "hour_cost_rub": null
              },
              {
                "id": "operator",
                "title": "Оператор",
                "hours_saved_year": 0,
                "hour_cost_rub": null
              }
            ]
          },
          "severe_injury_cost_rub": null
        },
        "cameras": {
          "source": "manual",
          "cameras": 5,
          "groups": [
            {
              "id": "standard",
              "share": 1,
              "model_ids": [
                "det-yolov8n@640-ap9999",
                "pose-yolov8n@640-ap9999"
              ]
            }
          ]
        }
      }
    },
    {
      "id": "shop",
      "title": "Цех",
      "area_m2": 10000,
      "machines": null,
      "note": "Работники, смены, плотность и смесь моделей — редактируемые допущения.",
      "rollout": {
        "contract_version": "2.0.0",
        "preset_id": "shop",
        "site": {
          "workshops": 1,
          "workers": 200,
          "shifts_per_day": 2,
          "working_days_year": 250,
          "operators": 2
        },
        "load": {
          "activity_share": 0.5,
          "activity_measurement_id": null,
          "target_fps": 12,
          "surge_fps": 5,
          "idle_check_s": 4,
          "peak_mode": "independent_p95",
          "priority_cameras_reserve": 1,
          "detector_stride": 1,
          "reference_chip_fps": 104.8,
          "capacity_derate": 0.5,
          "platform_capacity_override_fps": null,
          "model_cost_overrides": {},
          "cpu_basis": "inclusive",
          "cpu_ms_per_unit": 77,
          "decode_cores_per_camera": 0
        },
        "hardware": {
          "allowed_board_ids": [
            "HP",
            "HPD",
            "HPQ"
          ],
          "board_price_overrides": {},
          "server": {
            "slots": 4,
            "usable_cpu_cores": 16,
            "price_rub": 350000,
            "power_w": 250
          }
        },
        "costs": {
          "integration_fixed_rub": 300000,
          "integration_per_camera_rub": 0,
          "support_share_year": 0.15,
          "electricity_rub_kwh": 8,
          "operating_hours_year": 8760,
          "signal_zones_per_camera": 1,
          "signal_unit_rub": 25000,
          "speaker_per_workshop_rub": 40000,
          "new_camera_unit_rub": 30000,
          "new_camera_count": 0,
          "max_additional_camera_share": 0.2
        },
        "benefits": {
          "injuries": {
            "enabled": true,
            "annual_injured_workers": null,
            "rate_per_1000": 1.17,
            "cost_per_injured_worker_rub": 1000000,
            "cost_scope": "direct_only",
            "reduction": {
              "base": 0.2,
              "extended": 0.3,
              "max": 0.4
            }
          },
          "downtime": {
            "enabled": false,
            "events_year": null,
            "days_per_event": null,
            "day_cost_rub": null,
            "reduction": {
              "base": 0.2,
              "extended": 0.3,
              "max": 0.4
            }
          },
          "fines": {
            "enabled": false,
            "items": [
              {
                "id": "general_ohs",
                "title": "Общие требования охраны труда",
                "inspection_probability_year": 0.1,
                "amount_rub": 65000,
                "reduction": {
                  "base": 0.2,
                  "extended": 0.3,
                  "max": 0.4
                }
              },
              {
                "id": "ppe",
                "title": "Обеспечение СИЗ",
                "inspection_probability_year": 0.1,
                "amount_rub": 140000,
                "reduction": {
                  "base": 0.2,
                  "extended": 0.3,
                  "max": 0.4
                }
              }
            ]
          },
          "sfr_discount": {
            "enabled": false,
            "payroll_rub_year": null,
            "tariff_share": null,
            "additional_discount_share": null
          },
          "labor": {
            "monetize": false,
            "rows": [
              {
                "id": "ohs",
                "title": "Инженер охраны труда",
                "hours_saved_year": 0,
                "hour_cost_rub": null
              },
              {
                "id": "operator",
                "title": "Оператор",
                "hours_saved_year": 0,
                "hour_cost_rub": null
              }
            ]
          },
          "severe_injury_cost_rub": null
        },
        "cameras": {
          "source": "manual",
          "cameras": 20,
          "groups": [
            {
              "id": "standard",
              "share": 1,
              "model_ids": [
                "det-yolov8n@640-ap9999",
                "pose-yolov8n@640-ap9999"
              ]
            }
          ]
        }
      }
    },
    {
      "id": "plant",
      "title": "Завод",
      "area_m2": null,
      "machines": null,
      "note": "Работники, смены, плотность и смесь моделей — редактируемые допущения.",
      "rollout": {
        "contract_version": "2.0.0",
        "preset_id": "plant",
        "site": {
          "workshops": 4,
          "workers": 2000,
          "shifts_per_day": 3,
          "working_days_year": 250,
          "operators": 4
        },
        "load": {
          "activity_share": 0.5,
          "activity_measurement_id": null,
          "target_fps": 12,
          "surge_fps": 5,
          "idle_check_s": 4,
          "peak_mode": "independent_p95",
          "priority_cameras_reserve": 1,
          "detector_stride": 1,
          "reference_chip_fps": 104.8,
          "capacity_derate": 0.5,
          "platform_capacity_override_fps": null,
          "model_cost_overrides": {},
          "cpu_basis": "inclusive",
          "cpu_ms_per_unit": 77,
          "decode_cores_per_camera": 0
        },
        "hardware": {
          "allowed_board_ids": [
            "HP",
            "HPD",
            "HPQ"
          ],
          "board_price_overrides": {},
          "server": {
            "slots": 4,
            "usable_cpu_cores": 16,
            "price_rub": 350000,
            "power_w": 250
          }
        },
        "costs": {
          "integration_fixed_rub": 300000,
          "integration_per_camera_rub": 0,
          "support_share_year": 0.15,
          "electricity_rub_kwh": 8,
          "operating_hours_year": 8760,
          "signal_zones_per_camera": 1,
          "signal_unit_rub": 25000,
          "speaker_per_workshop_rub": 40000,
          "new_camera_unit_rub": 30000,
          "new_camera_count": 0,
          "max_additional_camera_share": 0.2
        },
        "benefits": {
          "injuries": {
            "enabled": true,
            "annual_injured_workers": null,
            "rate_per_1000": 1.17,
            "cost_per_injured_worker_rub": 1000000,
            "cost_scope": "direct_only",
            "reduction": {
              "base": 0.2,
              "extended": 0.3,
              "max": 0.4
            }
          },
          "downtime": {
            "enabled": false,
            "events_year": null,
            "days_per_event": null,
            "day_cost_rub": null,
            "reduction": {
              "base": 0.2,
              "extended": 0.3,
              "max": 0.4
            }
          },
          "fines": {
            "enabled": false,
            "items": [
              {
                "id": "general_ohs",
                "title": "Общие требования охраны труда",
                "inspection_probability_year": 0.1,
                "amount_rub": 65000,
                "reduction": {
                  "base": 0.2,
                  "extended": 0.3,
                  "max": 0.4
                }
              },
              {
                "id": "ppe",
                "title": "Обеспечение СИЗ",
                "inspection_probability_year": 0.1,
                "amount_rub": 140000,
                "reduction": {
                  "base": 0.2,
                  "extended": 0.3,
                  "max": 0.4
                }
              }
            ]
          },
          "sfr_discount": {
            "enabled": false,
            "payroll_rub_year": null,
            "tariff_share": null,
            "additional_discount_share": null
          },
          "labor": {
            "monetize": false,
            "rows": [
              {
                "id": "ohs",
                "title": "Инженер охраны труда",
                "hours_saved_year": 0,
                "hour_cost_rub": null
              },
              {
                "id": "operator",
                "title": "Оператор",
                "hours_saved_year": 0,
                "hour_cost_rub": null
              }
            ]
          },
          "severe_injury_cost_rub": null
        },
        "cameras": {
          "source": "manual",
          "cameras": 200,
          "groups": [
            {
              "id": "standard",
              "share": 1,
              "model_ids": [
                "det-yolov8n@640-ap9999",
                "pose-yolov8n@640-ap9999"
              ]
            }
          ]
        }
      }
    }
  ],
  "system_profile": {
    "cameras": 0,
    "groups": []
  },
  "models": [
    {
      "id": "det-yolov8n@640-ap9999",
      "title": "Детектор YOLOv8n",
      "kind": "detector",
      "work_units": 1,
      "execution_status": "verified_linq",
      "source_ids": [
        "team_defaults",
        "linq_historical_report"
      ]
    },
    {
      "id": "pose-yolov8n@640-ap9999",
      "title": "Поза YOLOv8n-pose",
      "kind": "pose",
      "work_units": 1,
      "execution_status": "verified_linq",
      "source_ids": [
        "vendor_pose_benchmark",
        "linq_historical_report"
      ]
    }
  ],
  "boards": [
    {
      "id": "HP",
      "title": "LinQ HP",
      "chips": 1,
      "slots": 1,
      "power_w": 35,
      "price_rub": 500000,
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hp",
        "team_defaults"
      ]
    },
    {
      "id": "HPD",
      "title": "LinQ HPD",
      "chips": 2,
      "slots": 1,
      "power_w": 100,
      "price_rub": null,
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpd",
        "team_defaults"
      ]
    },
    {
      "id": "HPQ",
      "title": "LinQ HPQ",
      "chips": 4,
      "slots": 1,
      "power_w": 150,
      "price_rub": null,
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpq",
        "team_defaults"
      ]
    }
  ],
  "assumptions": [
    {
      "key": "request.site.workshops",
      "title": "request.site.workshops",
      "value": 2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.site.workers",
      "title": "request.site.workers",
      "value": 200,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.site.shifts_per_day",
      "title": "request.site.shifts_per_day",
      "value": 2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.site.working_days_year",
      "title": "request.site.working_days_year",
      "value": 250,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.site.operators",
      "title": "request.site.operators",
      "value": 2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.activity_share",
      "title": "request.load.activity_share",
      "value": 0.5,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.target_fps",
      "title": "request.load.target_fps",
      "value": 12,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.surge_fps",
      "title": "request.load.surge_fps",
      "value": 5,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.idle_check_s",
      "title": "request.load.idle_check_s",
      "value": 4,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.priority_cameras_reserve",
      "title": "request.load.priority_cameras_reserve",
      "value": 1,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.detector_stride",
      "title": "request.load.detector_stride",
      "value": 1,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.reference_chip_fps",
      "title": "request.load.reference_chip_fps",
      "value": 104.8,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "vendor_pose_benchmark"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.capacity_derate",
      "title": "request.load.capacity_derate",
      "value": 0.5,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.platform_capacity_override_fps",
      "title": "request.load.platform_capacity_override_fps",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.load.cpu_ms_per_unit",
      "title": "request.load.cpu_ms_per_unit",
      "value": 77,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.decode_cores_per_camera",
      "title": "request.load.decode_cores_per_camera",
      "value": 0,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.hardware.server.slots",
      "title": "request.hardware.server.slots",
      "value": 4,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.hardware.server.usable_cpu_cores",
      "title": "request.hardware.server.usable_cpu_cores",
      "value": 16,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.hardware.server.price_rub",
      "title": "request.hardware.server.price_rub",
      "value": 350000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.hardware.server.power_w",
      "title": "request.hardware.server.power_w",
      "value": 250,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.integration_fixed_rub",
      "title": "request.costs.integration_fixed_rub",
      "value": 300000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.integration_per_camera_rub",
      "title": "request.costs.integration_per_camera_rub",
      "value": 0,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.support_share_year",
      "title": "request.costs.support_share_year",
      "value": 0.15,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.electricity_rub_kwh",
      "title": "request.costs.electricity_rub_kwh",
      "value": 8,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.operating_hours_year",
      "title": "request.costs.operating_hours_year",
      "value": 8760,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.signal_zones_per_camera",
      "title": "request.costs.signal_zones_per_camera",
      "value": 1,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.signal_unit_rub",
      "title": "request.costs.signal_unit_rub",
      "value": 25000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.speaker_per_workshop_rub",
      "title": "request.costs.speaker_per_workshop_rub",
      "value": 40000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.new_camera_unit_rub",
      "title": "request.costs.new_camera_unit_rub",
      "value": 30000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.new_camera_count",
      "title": "request.costs.new_camera_count",
      "value": 0,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.max_additional_camera_share",
      "title": "request.costs.max_additional_camera_share",
      "value": 0.2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.injuries.annual_injured_workers",
      "title": "request.benefits.injuries.annual_injured_workers",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.injuries.rate_per_1000",
      "title": "request.benefits.injuries.rate_per_1000",
      "value": 1.17,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "rosstat_injury_rate"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.injuries.cost_per_injured_worker_rub",
      "title": "request.benefits.injuries.cost_per_injured_worker_rub",
      "value": 1000000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.injuries.reduction.base",
      "title": "request.benefits.injuries.reduction.base",
      "value": 0.2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.injuries.reduction.extended",
      "title": "request.benefits.injuries.reduction.extended",
      "value": 0.3,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.injuries.reduction.max",
      "title": "request.benefits.injuries.reduction.max",
      "value": 0.4,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.downtime.events_year",
      "title": "request.benefits.downtime.events_year",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.downtime.days_per_event",
      "title": "request.benefits.downtime.days_per_event",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.downtime.day_cost_rub",
      "title": "request.benefits.downtime.day_cost_rub",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.downtime.reduction.base",
      "title": "request.benefits.downtime.reduction.base",
      "value": 0.2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.downtime.reduction.extended",
      "title": "request.benefits.downtime.reduction.extended",
      "value": 0.3,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.downtime.reduction.max",
      "title": "request.benefits.downtime.reduction.max",
      "value": 0.4,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.0.inspection_probability_year",
      "title": "request.benefits.fines.items.0.inspection_probability_year",
      "value": 0.1,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.0.amount_rub",
      "title": "request.benefits.fines.items.0.amount_rub",
      "value": 65000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.0.reduction.base",
      "title": "request.benefits.fines.items.0.reduction.base",
      "value": 0.2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.0.reduction.extended",
      "title": "request.benefits.fines.items.0.reduction.extended",
      "value": 0.3,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.0.reduction.max",
      "title": "request.benefits.fines.items.0.reduction.max",
      "value": 0.4,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.1.inspection_probability_year",
      "title": "request.benefits.fines.items.1.inspection_probability_year",
      "value": 0.1,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.1.amount_rub",
      "title": "request.benefits.fines.items.1.amount_rub",
      "value": 140000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.1.reduction.base",
      "title": "request.benefits.fines.items.1.reduction.base",
      "value": 0.2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.1.reduction.extended",
      "title": "request.benefits.fines.items.1.reduction.extended",
      "value": 0.3,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.1.reduction.max",
      "title": "request.benefits.fines.items.1.reduction.max",
      "value": 0.4,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.sfr_discount.payroll_rub_year",
      "title": "request.benefits.sfr_discount.payroll_rub_year",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.sfr_discount.tariff_share",
      "title": "request.benefits.sfr_discount.tariff_share",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.sfr_discount.additional_discount_share",
      "title": "request.benefits.sfr_discount.additional_discount_share",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.labor.rows.0.hours_saved_year",
      "title": "request.benefits.labor.rows.0.hours_saved_year",
      "value": 0,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.labor.rows.0.hour_cost_rub",
      "title": "request.benefits.labor.rows.0.hour_cost_rub",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.labor.rows.1.hours_saved_year",
      "title": "request.benefits.labor.rows.1.hours_saved_year",
      "value": 0,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.labor.rows.1.hour_cost_rub",
      "title": "request.benefits.labor.rows.1.hour_cost_rub",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.severe_injury_cost_rub",
      "title": "request.benefits.severe_injury_cost_rub",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.cameras.cameras",
      "title": "request.cameras.cameras",
      "value": 8,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.cameras.groups.0.share",
      "title": "request.cameras.groups.0.share",
      "value": 1,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HP.chips",
      "title": "catalog.boards.HP.chips",
      "value": 1,
      "unit": "шт.",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hp",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HP.slots",
      "title": "catalog.boards.HP.slots",
      "value": 1,
      "unit": "шт.",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hp",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HP.power_w",
      "title": "catalog.boards.HP.power_w",
      "value": 35,
      "unit": "Вт",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hp",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HP.price_rub",
      "title": "catalog.boards.HP.price_rub",
      "value": 500000,
      "unit": "₽",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hp",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPD.chips",
      "title": "catalog.boards.HPD.chips",
      "value": 2,
      "unit": "шт.",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpd",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPD.slots",
      "title": "catalog.boards.HPD.slots",
      "value": 1,
      "unit": "шт.",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpd",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPD.power_w",
      "title": "catalog.boards.HPD.power_w",
      "value": 100,
      "unit": "Вт",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpd",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPD.price_rub",
      "title": "catalog.boards.HPD.price_rub",
      "value": null,
      "unit": "₽",
      "status": "missing",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpd",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "catalog.boards.HPQ.chips",
      "title": "catalog.boards.HPQ.chips",
      "value": 4,
      "unit": "шт.",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpq",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPQ.slots",
      "title": "catalog.boards.HPQ.slots",
      "value": 1,
      "unit": "шт.",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpq",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPQ.power_w",
      "title": "catalog.boards.HPQ.power_w",
      "value": 150,
      "unit": "Вт",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpq",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPQ.price_rub",
      "title": "catalog.boards.HPQ.price_rub",
      "value": null,
      "unit": "₽",
      "status": "missing",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpq",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "catalog.models.detector.work_units",
      "title": "catalog.models.detector.work_units",
      "value": 1,
      "unit": "экв.ед.",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.models.pose.work_units",
      "title": "catalog.models.pose.work_units",
      "value": 1,
      "unit": "экв.ед.",
      "status": "assumed",
      "source_ids": [
        "vendor_pose_benchmark"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "market.normacheck_cloud.amount_rub",
      "title": "NormaCheck: непроверенный месячный ориентир",
      "value": 3900,
      "unit": "₽/камера/месяц",
      "status": "assumed",
      "source_ids": [
        "market_normacheck_unverified"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "market.trassir_ppe.amount_rub",
      "title": "TRASSIR: условная точка диапазона",
      "value": 6500,
      "unit": "₽/канал, разово",
      "status": "assumed",
      "source_ids": [
        "market_trassir_unverified",
        "team_defaults"
      ],
      "formula": "(6000+7000)/2 — условная точка локальной выписки",
      "depends_on": [],
      "reason": null
    }
  ],
  "measurements": [
    {
      "id": "fixture_not_measured_activity",
      "key": "activity_share",
      "title": "Измеренная активность камер",
      "value": null,
      "unit": "доля",
      "status": "not_measured",
      "period_start": null,
      "period_end": null,
      "sample_count": 0,
      "source_ids": [],
      "note": "Изолированный пример не содержит измерений; рабочий ответ возвращает доступные факты."
    },
    {
      "id": "fixture_not_measured_platform",
      "key": "platform_fps",
      "title": "Измеренная пропускная способность площадки",
      "value": null,
      "unit": "кадр/с",
      "status": "not_measured",
      "period_start": null,
      "period_end": null,
      "sample_count": 0,
      "source_ids": [],
      "note": "Новых замеров нет; для сравнения явно используется командное допущение 12,4."
    }
  ],
  "market": [
    {
      "id": "normacheck_cloud",
      "title": "NormaCheck: облачная видеоаналитика",
      "billing": "monthly_per_camera",
      "amount_rub": 3900,
      "scope": "Непроверенный ориентир по локальной выписке: цена за камеру в месяц. Состав облачной услуги и сопоставимость с Argus уточняются; в выгоды B не входит.",
      "source_ids": [
        "market_normacheck_unverified"
      ]
    },
    {
      "id": "trassir_ppe",
      "title": "TRASSIR: модуль контроля спецодежды",
      "billing": "one_off_per_camera",
      "amount_rub": 6500,
      "scope": "Условная точка диапазона 6000–7000 ₽ за модуль на канал; не подтверждённый сегодня прайс. Разовая лицензия не равна полной стоимости внедрения; в выгоды B не входит.",
      "source_ids": [
        "market_trassir_unverified",
        "team_defaults"
      ]
    }
  ],
  "features": {
    "tracker": {
      "available": false,
      "max_stride": 1,
      "report_ref": null
    },
    "pdf_available": false,
    "offline_economy": null
  },
  "limits": [
    {
      "field": "cameras.cameras",
      "min": 0,
      "max": 10000,
      "integer": true
    },
    {
      "field": "load.activity_share",
      "min": 0,
      "max": 1,
      "integer": false
    },
    {
      "field": "load.target_fps",
      "min": 0,
      "max": 120,
      "integer": false
    },
    {
      "field": "load.priority_cameras_reserve",
      "min": 0,
      "max": 10000,
      "integer": true
    },
    {
      "field": "costs.support_share_year",
      "min": 0,
      "max": 1,
      "integer": false
    }
  ],
  "sources": [
    {
      "id": "team_defaults",
      "title": "Расчётные допущения команды Argus",
      "kind": "team_assumption",
      "verification": "not_applicable",
      "url": null,
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "Цены, CPU, запас, сервер и эффект — редактируемые допущения, не замеры."
    },
    {
      "id": "user_input",
      "title": "Данные, введённые в этот расчётный пример",
      "kind": "user_input",
      "verification": "not_applicable",
      "url": null,
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "Эталонный пользовательский ввод; не данные реально обследованного завода."
    },
    {
      "id": "vendor_pose_benchmark",
      "title": "Бенчмарк LinQ: yolov8n-pose, batch 1",
      "kind": "vendor_claim",
      "verification": "cached_primary",
      "url": "https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf",
      "data_year": 2026,
      "published_at": null,
      "checked_at": null,
      "note": "104,8 FPS: заявление вендора; сохранённая первичная выписка, не замер Argus."
    },
    {
      "id": "vendor_modules",
      "title": "Модули LinQ HP, HPD, HPQ",
      "kind": "vendor_claim",
      "verification": "verified_primary",
      "url": "https://lin-q.ru/sol",
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "HP=1, HPD=2, HPQ=4 чипа."
    },
    {
      "id": "vendor_board_power_hp",
      "title": "Паспортная мощность конкретного исполнения HP",
      "kind": "vendor_claim",
      "verification": "cached_primary",
      "url": "https://files.lin-q.ru/tpu/docs/_HPact_manual_LINQ_HP1M_02.pdf",
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "35 Вт — верхняя паспортная граница, не измеренное потребление."
    },
    {
      "id": "vendor_board_power_hpd",
      "title": "Паспортная мощность конкретного исполнения HPD",
      "kind": "vendor_claim",
      "verification": "cached_primary",
      "url": "https://files.lin-q.ru/tpu/docs/_HPDpass_manual_LINQ_HPD1M_01.pdf",
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "100 Вт — верхняя паспортная граница."
    },
    {
      "id": "vendor_board_power_hpq",
      "title": "Паспортная мощность конкретного исполнения HPQ",
      "kind": "vendor_claim",
      "verification": "cached_primary",
      "url": "https://files.lin-q.ru/tpu/docs/_HPQpass_manual_LINQ_HPD1M_10.pdf",
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "150 Вт — верхняя паспортная граница."
    },
    {
      "id": "rosstat_injury_rate",
      "title": "Отраслевая подсказка частоты пострадавших",
      "kind": "official",
      "verification": "pending_primary",
      "url": "https://rosstat.gov.ru/working_conditions",
      "data_year": 2025,
      "published_at": null,
      "checked_at": null,
      "note": "1,17 на 1000 за 2025 из локальной выписки; первичный массив требует проверки."
    },
    {
      "id": "linq_historical_report",
      "title": "Историческое подтверждение исполнения detector и pose на LinQ",
      "kind": "argus_measurement",
      "verification": "cached_primary",
      "url": null,
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "Существовавший до этого контракта отчёт; новых замеров эти JSON не изображают."
    },
    {
      "id": "market_normacheck_unverified",
      "title": "NormaCheck: облачная видеоаналитика, непроверенный ориентир",
      "kind": "vendor_claim",
      "verification": "pending_primary",
      "url": null,
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "docs/ECONOMICS_SOURCES.md: 3900 ₽/камера/месяц. Это локальная выписка, не подтверждённый сегодня прайс; дата публикации неизвестна."
    },
    {
      "id": "market_trassir_unverified",
      "title": "TRASSIR: модуль СИЗ на канал, непроверенный ориентир",
      "kind": "vendor_claim",
      "verification": "pending_primary",
      "url": null,
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "docs/ECONOMICS_SOURCES.md: диапазон 6000–7000 ₽/канал. 6500 ₽ — условная точка внутри диапазона, не подтверждённая цена предложения; дата публикации неизвестна."
    },
    {
      "id": "sfr_prevention",
      "title": "СФР: финансовое обеспечение предупредительных мер",
      "kind": "official",
      "verification": "verified_primary",
      "url": "https://sfr.gov.ru/employers/lk_insurer/baza_znanij/finansovoe_obespechenie_predupreditelnih_mer",
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "Первичная база К11: согласуемое возмещение по действующим правилам. Допустимость покупки Argus не установлена; из CAPEX/TCO ничего автоматически не вычитается."
    },
    {
      "id": "sfr_discount",
      "title": "СФР: условия скидки к страховому тарифу",
      "kind": "official",
      "verification": "verified_primary",
      "url": "https://sfr.gov.ru/branches/novgorod/news~2026/10/21/285762",
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "Первичная база К11: до 40% при соблюдении условий и подаче заявления; приобретение Argus само по себе скидку не даёт."
    }
  ],
  "notices": [
    {
      "code": "EXAMPLE_CONTEXT",
      "field": null,
      "message": "Полный пример блока GET.v2 для изолированного контекста без камер и новых измерений; не снимок действующего завода."
    },
    {
      "code": "SFR_PREVENTION_INFO",
      "field": null,
      "message": "Часть затрат потенциально согласуется с СФР как предупредительные меры; это возмещение при выполнении условий, не автоматическое финансирование Argus и не вычет из CAPEX/TCO."
    },
    {
      "code": "SFR_DISCOUNT_CONDITIONS",
      "field": "benefits.sfr_discount",
      "message": "Скидка к тарифу может составлять до 40% при выполнении условий; покупка Argus её автоматически не даёт. В расчёт она включается отдельно и по умолчанию выключена."
    }
  ]
}
```

## К14.2. Полный запрос внедрения

POST /api/calculator/rollout?format=v2, X-Role: management.

```json
{
  "contract_version": "2.0.0",
  "preset_id": null,
  "site": {
    "workshops": 2,
    "workers": 200,
    "shifts_per_day": 2,
    "working_days_year": 250,
    "operators": 2
  },
  "load": {
    "activity_share": 0.5,
    "activity_measurement_id": null,
    "target_fps": 12,
    "surge_fps": 5,
    "idle_check_s": 4,
    "peak_mode": "independent_p95",
    "priority_cameras_reserve": 1,
    "detector_stride": 1,
    "reference_chip_fps": 104.8,
    "capacity_derate": 0.5,
    "platform_capacity_override_fps": null,
    "model_cost_overrides": {},
    "cpu_basis": "inclusive",
    "cpu_ms_per_unit": 77,
    "decode_cores_per_camera": 0
  },
  "hardware": {
    "allowed_board_ids": [
      "HP",
      "HPD",
      "HPQ"
    ],
    "board_price_overrides": {},
    "server": {
      "slots": 4,
      "usable_cpu_cores": 16,
      "price_rub": 350000,
      "power_w": 250
    }
  },
  "costs": {
    "integration_fixed_rub": 300000,
    "integration_per_camera_rub": 0,
    "support_share_year": 0.15,
    "electricity_rub_kwh": 8,
    "operating_hours_year": 8760,
    "signal_zones_per_camera": 1,
    "signal_unit_rub": 25000,
    "speaker_per_workshop_rub": 40000,
    "new_camera_unit_rub": 30000,
    "new_camera_count": 0,
    "max_additional_camera_share": 0.2
  },
  "benefits": {
    "injuries": {
      "enabled": true,
      "annual_injured_workers": null,
      "rate_per_1000": 1.17,
      "cost_per_injured_worker_rub": 1000000,
      "cost_scope": "direct_only",
      "reduction": {
        "base": 0.2,
        "extended": 0.3,
        "max": 0.4
      }
    },
    "downtime": {
      "enabled": false,
      "events_year": null,
      "days_per_event": null,
      "day_cost_rub": null,
      "reduction": {
        "base": 0.2,
        "extended": 0.3,
        "max": 0.4
      }
    },
    "fines": {
      "enabled": false,
      "items": [
        {
          "id": "general_ohs",
          "title": "Общие требования охраны труда",
          "inspection_probability_year": 0.1,
          "amount_rub": 65000,
          "reduction": {
            "base": 0.2,
            "extended": 0.3,
            "max": 0.4
          }
        },
        {
          "id": "ppe",
          "title": "Обеспечение СИЗ",
          "inspection_probability_year": 0.1,
          "amount_rub": 140000,
          "reduction": {
            "base": 0.2,
            "extended": 0.3,
            "max": 0.4
          }
        }
      ]
    },
    "sfr_discount": {
      "enabled": false,
      "payroll_rub_year": null,
      "tariff_share": null,
      "additional_discount_share": null
    },
    "labor": {
      "monetize": false,
      "rows": [
        {
          "id": "ohs",
          "title": "Инженер охраны труда",
          "hours_saved_year": 0,
          "hour_cost_rub": null
        },
        {
          "id": "operator",
          "title": "Оператор",
          "hours_saved_year": 0,
          "hour_cost_rub": null
        }
      ]
    },
    "severe_injury_cost_rub": null
  },
  "cameras": {
    "source": "manual",
    "cameras": 8,
    "groups": [
      {
        "id": "standard",
        "share": 1,
        "model_ids": [
          "det-yolov8n@640-ap9999",
          "pose-yolov8n@640-ap9999"
        ]
      }
    ]
  }
}
```

## К14.3. Полный ответ внедрения

Полный ResultV2 для предыдущего запроса: estimated, три HP и один сервер; неподтверждённые данные явно подписаны.

```json
{
  "format": "v2",
  "contract_version": "2.0.0",
  "formula_version": "argus-calc-2.0",
  "mode": "rollout",
  "status": "estimated",
  "cost_scope": "whole_project",
  "horizon_years": 3,
  "resolved": {
    "current": {
      "cameras": 0,
      "groups": []
    },
    "added": {
      "cameras": 8,
      "groups": [
        {
          "id": "added:standard",
          "cameras": 8,
          "camera_ids": [],
          "model_ids": [
            "det-yolov8n@640-ap9999",
            "pose-yolov8n@640-ap9999"
          ]
        }
      ]
    },
    "total": {
      "cameras": 8,
      "groups": [
        {
          "id": "added:standard",
          "cameras": 8,
          "camera_ids": [],
          "model_ids": [
            "det-yolov8n@640-ap9999",
            "pose-yolov8n@640-ap9999"
          ]
        }
      ]
    },
    "input": {
      "contract_version": "2.0.0",
      "preset_id": null,
      "site": {
        "workshops": 2,
        "workers": 200,
        "shifts_per_day": 2,
        "working_days_year": 250,
        "operators": 2
      },
      "load": {
        "activity_share": 0.5,
        "activity_measurement_id": null,
        "target_fps": 12,
        "surge_fps": 5,
        "idle_check_s": 4,
        "peak_mode": "independent_p95",
        "priority_cameras_reserve": 1,
        "detector_stride": 1,
        "reference_chip_fps": 104.8,
        "capacity_derate": 0.5,
        "platform_capacity_override_fps": null,
        "model_cost_overrides": {},
        "cpu_basis": "inclusive",
        "cpu_ms_per_unit": 77,
        "decode_cores_per_camera": 0
      },
      "hardware": {
        "allowed_board_ids": [
          "HP",
          "HPD",
          "HPQ"
        ],
        "board_price_overrides": {},
        "server": {
          "slots": 4,
          "usable_cpu_cores": 16,
          "price_rub": 350000,
          "power_w": 250
        }
      },
      "costs": {
        "integration_fixed_rub": 300000,
        "integration_per_camera_rub": 0,
        "support_share_year": 0.15,
        "electricity_rub_kwh": 8,
        "operating_hours_year": 8760,
        "signal_zones_per_camera": 1,
        "signal_unit_rub": 25000,
        "speaker_per_workshop_rub": 40000,
        "new_camera_unit_rub": 30000,
        "new_camera_count": 0,
        "max_additional_camera_share": 0.2
      },
      "benefits": {
        "injuries": {
          "enabled": true,
          "annual_injured_workers": null,
          "rate_per_1000": 1.17,
          "cost_per_injured_worker_rub": 1000000,
          "cost_scope": "direct_only",
          "reduction": {
            "base": 0.2,
            "extended": 0.3,
            "max": 0.4
          }
        },
        "downtime": {
          "enabled": false,
          "events_year": null,
          "days_per_event": null,
          "day_cost_rub": null,
          "reduction": {
            "base": 0.2,
            "extended": 0.3,
            "max": 0.4
          }
        },
        "fines": {
          "enabled": false,
          "items": [
            {
              "id": "general_ohs",
              "title": "Общие требования охраны труда",
              "inspection_probability_year": 0.1,
              "amount_rub": 65000,
              "reduction": {
                "base": 0.2,
                "extended": 0.3,
                "max": 0.4
              }
            },
            {
              "id": "ppe",
              "title": "Обеспечение СИЗ",
              "inspection_probability_year": 0.1,
              "amount_rub": 140000,
              "reduction": {
                "base": 0.2,
                "extended": 0.3,
                "max": 0.4
              }
            }
          ]
        },
        "sfr_discount": {
          "enabled": false,
          "payroll_rub_year": null,
          "tariff_share": null,
          "additional_discount_share": null
        },
        "labor": {
          "monetize": false,
          "rows": [
            {
              "id": "ohs",
              "title": "Инженер охраны труда",
              "hours_saved_year": 0,
              "hour_cost_rub": null
            },
            {
              "id": "operator",
              "title": "Оператор",
              "hours_saved_year": 0,
              "hour_cost_rub": null
            }
          ]
        },
        "severe_injury_cost_rub": null
      },
      "cameras": {
        "source": "manual",
        "cameras": 8,
        "groups": [
          {
            "id": "standard",
            "share": 1,
            "model_ids": [
              "det-yolov8n@640-ap9999",
              "pose-yolov8n@640-ap9999"
            ]
          }
        ]
      }
    }
  },
  "load": {
    "cameras": 8,
    "active_p95": 6,
    "priority_cameras_effective": 1,
    "peak_units_s": 144.5,
    "surge_units_s": 94.0,
    "required_units_s": 144.5,
    "effective_chip_units_s": 52.4,
    "required_chips": 3,
    "required_cpu_cores": 11.1265,
    "naive_chips": 16,
    "basis": "independent_p95"
  },
  "hardware": {
    "selection": "priced_optimum",
    "before": {
      "boards": [],
      "chips": 0,
      "servers": 0,
      "used_slots": 0,
      "power_w": 0.0
    },
    "purchase": {
      "boards": [
        {
          "board_id": "HP",
          "count": 3
        }
      ],
      "chips": 3,
      "servers": 1,
      "used_slots": 3,
      "power_w": 355.0
    },
    "after": {
      "boards": [
        {
          "board_id": "HP",
          "count": 3
        }
      ],
      "chips": 3,
      "servers": 1,
      "used_slots": 3,
      "power_w": 355.0
    },
    "board_capex_rub": 1500000.0,
    "server_capex_rub": 350000.0,
    "required_after_chips": 3,
    "spare_chips_after": 0,
    "note": "Эталонный пример использует HP: остальные цены неизвестны; новый глобальный solver здесь не имитируется.",
    "inventory_basis": "none",
    "required_before_chips": 0
  },
  "tiers": [
    {
      "tier": "base",
      "title": "Базовый",
      "capex_rub": 2150000.0,
      "opex_rub_year": 347378.4,
      "gross_benefit_rub_year": 46800.0,
      "net_benefit_rub_year": -300578.4,
      "tco_3_year_rub": 3192135.2,
      "net_balance_3_year_rub": -3051735.2,
      "rub_per_camera_month": 11083.8,
      "camera_denominator": 8,
      "labor_hours_year": 0,
      "capex_lines": [
        {
          "id": "boards",
          "title": "Новые платы LinQ",
          "amount_rub": 1500000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.boards"
          ]
        },
        {
          "id": "servers",
          "title": "Новые серверы",
          "amount_rub": 350000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.servers"
          ]
        },
        {
          "id": "integration_fixed",
          "title": "Пусконаладка: фиксированная часть",
          "amount_rub": 300000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.integration_fixed"
          ]
        },
        {
          "id": "integration_cameras",
          "title": "Пусконаладка камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.integration_cameras"
          ]
        },
        {
          "id": "physical_cameras",
          "title": "Покупка физических камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.physical_cameras"
          ]
        }
      ],
      "opex_lines": [
        {
          "id": "support",
          "title": "Поддержка",
          "amount_rub": 322500.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.opex.support"
          ]
        },
        {
          "id": "electricity",
          "title": "Электроэнергия вычислительного оборудования",
          "amount_rub": 24878.4,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "cost.electricity_rub_year"
          ]
        }
      ],
      "benefit_lines": [
        {
          "id": "injuries",
          "title": "Предотвращённые прямые потери предприятия от травм",
          "amount_rub": 46800.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.benefit.injuries"
          ]
        },
        {
          "id": "downtime",
          "title": "Простой",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.base.benefit.downtime"
          ]
        },
        {
          "id": "fines",
          "title": "Штрафы",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.base.benefit.fines"
          ]
        },
        {
          "id": "sfr_discount",
          "title": "Дополнительная скидка СФР",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.base.benefit.sfr_discount"
          ]
        },
        {
          "id": "labor",
          "title": "Время работников в деньгах",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.base.benefit.labor"
          ]
        }
      ],
      "payback": {
        "status": "no_positive_effect",
        "months": null,
        "within_horizon": false,
        "reason": "Расчётная годовая выгода не превышает годовые расходы; измените фактические входы."
      },
      "severe_threshold": {
        "status": "needs_input",
        "expected_prevented_cases": null,
        "whole_prevented_cases": null,
        "uncovered_cost_rub": 3192135.2,
        "reason": "Задайте прямую стоимость тяжёлого случая для предприятия."
      },
      "board_price_threshold": {
        "status": "free_still_insufficient",
        "board_id": "HP",
        "boards_to_buy": 3,
        "max_unit_price_rub": null,
        "current_unit_price_rub": 500000.0,
        "reason": "Даже бесплатная плата не покрывает остальные расходы при этих входах; знание текущей цены платы для этого вывода не требуется."
      }
    },
    {
      "tier": "extended",
      "title": "Расширенный",
      "capex_rub": 2350000.0,
      "opex_rub_year": 377378.4,
      "gross_benefit_rub_year": 70200.0,
      "net_benefit_rub_year": -307178.4,
      "tco_3_year_rub": 3482135.2,
      "net_balance_3_year_rub": -3271535.2,
      "rub_per_camera_month": 12090.75,
      "camera_denominator": 8,
      "labor_hours_year": 0,
      "capex_lines": [
        {
          "id": "boards",
          "title": "Новые платы LinQ",
          "amount_rub": 1500000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.boards"
          ]
        },
        {
          "id": "servers",
          "title": "Новые серверы",
          "amount_rub": 350000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.servers"
          ]
        },
        {
          "id": "integration_fixed",
          "title": "Пусконаладка: фиксированная часть",
          "amount_rub": 300000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.integration_fixed"
          ]
        },
        {
          "id": "integration_cameras",
          "title": "Пусконаладка камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.integration_cameras"
          ]
        },
        {
          "id": "physical_cameras",
          "title": "Покупка физических камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.physical_cameras"
          ]
        },
        {
          "id": "signals",
          "title": "Световые и звуковые сигналы зон",
          "amount_rub": 200000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.signals"
          ]
        }
      ],
      "opex_lines": [
        {
          "id": "support",
          "title": "Поддержка",
          "amount_rub": 352500.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.opex.support"
          ]
        },
        {
          "id": "electricity",
          "title": "Электроэнергия вычислительного оборудования",
          "amount_rub": 24878.4,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "cost.electricity_rub_year"
          ]
        }
      ],
      "benefit_lines": [
        {
          "id": "injuries",
          "title": "Предотвращённые прямые потери предприятия от травм",
          "amount_rub": 70200.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.benefit.injuries"
          ]
        },
        {
          "id": "downtime",
          "title": "Простой",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.extended.benefit.downtime"
          ]
        },
        {
          "id": "fines",
          "title": "Штрафы",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.extended.benefit.fines"
          ]
        },
        {
          "id": "sfr_discount",
          "title": "Дополнительная скидка СФР",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.extended.benefit.sfr_discount"
          ]
        },
        {
          "id": "labor",
          "title": "Время работников в деньгах",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.extended.benefit.labor"
          ]
        }
      ],
      "payback": {
        "status": "no_positive_effect",
        "months": null,
        "within_horizon": false,
        "reason": "Расчётная годовая выгода не превышает годовые расходы; измените фактические входы."
      },
      "severe_threshold": {
        "status": "needs_input",
        "expected_prevented_cases": null,
        "whole_prevented_cases": null,
        "uncovered_cost_rub": 3482135.2,
        "reason": "Задайте прямую стоимость тяжёлого случая для предприятия."
      },
      "board_price_threshold": {
        "status": "free_still_insufficient",
        "board_id": "HP",
        "boards_to_buy": 3,
        "max_unit_price_rub": null,
        "current_unit_price_rub": 500000.0,
        "reason": "Даже бесплатная плата не покрывает остальные расходы при этих входах; знание текущей цены платы для этого вывода не требуется."
      }
    },
    {
      "tier": "max",
      "title": "Максимальный",
      "capex_rub": 2490000.0,
      "opex_rub_year": 398378.4,
      "gross_benefit_rub_year": 93600.0,
      "net_benefit_rub_year": -304778.4,
      "tco_3_year_rub": 3685135.2,
      "net_balance_3_year_rub": -3404335.2,
      "rub_per_camera_month": 12795.61,
      "camera_denominator": 8,
      "labor_hours_year": 0,
      "capex_lines": [
        {
          "id": "boards",
          "title": "Новые платы LinQ",
          "amount_rub": 1500000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.boards"
          ]
        },
        {
          "id": "servers",
          "title": "Новые серверы",
          "amount_rub": 350000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.servers"
          ]
        },
        {
          "id": "integration_fixed",
          "title": "Пусконаладка: фиксированная часть",
          "amount_rub": 300000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.integration_fixed"
          ]
        },
        {
          "id": "integration_cameras",
          "title": "Пусконаладка камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.integration_cameras"
          ]
        },
        {
          "id": "physical_cameras",
          "title": "Покупка физических камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.physical_cameras"
          ]
        },
        {
          "id": "signals",
          "title": "Световые и звуковые сигналы зон",
          "amount_rub": 200000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.signals"
          ]
        },
        {
          "id": "speakers",
          "title": "Громкоговорители в цехах",
          "amount_rub": 80000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.speakers"
          ]
        },
        {
          "id": "max_cameras",
          "title": "Дополнительное оснащение каналов камерами",
          "amount_rub": 60000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.max_cameras"
          ]
        }
      ],
      "opex_lines": [
        {
          "id": "support",
          "title": "Поддержка",
          "amount_rub": 373500.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.opex.support"
          ]
        },
        {
          "id": "electricity",
          "title": "Электроэнергия вычислительного оборудования",
          "amount_rub": 24878.4,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "cost.electricity_rub_year"
          ]
        }
      ],
      "benefit_lines": [
        {
          "id": "injuries",
          "title": "Предотвращённые прямые потери предприятия от травм",
          "amount_rub": 93600.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.benefit.injuries"
          ]
        },
        {
          "id": "downtime",
          "title": "Простой",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.max.benefit.downtime"
          ]
        },
        {
          "id": "fines",
          "title": "Штрафы",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.max.benefit.fines"
          ]
        },
        {
          "id": "sfr_discount",
          "title": "Дополнительная скидка СФР",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.max.benefit.sfr_discount"
          ]
        },
        {
          "id": "labor",
          "title": "Время работников в деньгах",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.max.benefit.labor"
          ]
        }
      ],
      "payback": {
        "status": "no_positive_effect",
        "months": null,
        "within_horizon": false,
        "reason": "Расчётная годовая выгода не превышает годовые расходы; измените фактические входы."
      },
      "severe_threshold": {
        "status": "needs_input",
        "expected_prevented_cases": null,
        "whole_prevented_cases": null,
        "uncovered_cost_rub": 3685135.2,
        "reason": "Задайте прямую стоимость тяжёлого случая для предприятия."
      },
      "board_price_threshold": {
        "status": "free_still_insufficient",
        "board_id": "HP",
        "boards_to_buy": 3,
        "max_unit_price_rub": null,
        "current_unit_price_rub": 500000.0,
        "reason": "Даже бесплатная плата не покрывает остальные расходы при этих входах; знание текущей цены платы для этого вывода не требуется."
      }
    }
  ],
  "steps": [
    {
      "id": "naive",
      "title": "Как считалось раньше",
      "available": true,
      "chips": 16,
      "servers": 4,
      "equipment_capex_rub": 9400000.0,
      "reason": "Общая greenfield-потребность; старый инвентарь не зачтён."
    },
    {
      "id": "dedicated_capacity",
      "title": "Ёмкость выделенной платы",
      "available": true,
      "chips": 4,
      "servers": 1,
      "equipment_capex_rub": 2350000.0,
      "reason": "Общая greenfield-потребность; старый инвентарь не зачтён."
    },
    {
      "id": "scenario_models",
      "title": "Модели только где нужны",
      "available": true,
      "chips": 4,
      "servers": 1,
      "equipment_capex_rub": 2350000.0,
      "reason": "Общая greenfield-потребность; старый инвентарь не зачтён."
    },
    {
      "id": "activity_pool",
      "title": "Активность и резерв тревог",
      "available": true,
      "chips": 3,
      "servers": 1,
      "equipment_capex_rub": 1850000.0,
      "reason": "Общая greenfield-потребность; старый инвентарь не зачтён."
    },
    {
      "id": "tracker",
      "title": "Трекер между кадрами детектора",
      "available": false,
      "chips": null,
      "servers": null,
      "equipment_capex_rub": null,
      "reason": "Нет отчёта, подтверждающего сохранность событий; трекер выключен."
    }
  ],
  "scale_curve": {
    "scope": "greenfield_reference",
    "tier": "base",
    "points": [
      {
        "cameras": 5,
        "chips": 2,
        "servers": 1,
        "tco_3_year_rub": 2459776.8,
        "rub_per_camera_month": 13665.43
      },
      {
        "cameras": 10,
        "chips": 4,
        "servers": 1,
        "tco_3_year_rub": 3924493.6,
        "rub_per_camera_month": 10901.37
      },
      {
        "cameras": 25,
        "chips": 8,
        "servers": 2,
        "tco_3_year_rub": 7413987.2,
        "rub_per_camera_month": 8237.76
      },
      {
        "cameras": 50,
        "chips": 15,
        "servers": 4,
        "tco_3_year_rub": 13660616.0,
        "rub_per_camera_month": 7589.23
      },
      {
        "cameras": 100,
        "chips": 27,
        "servers": 7,
        "tco_3_year_rub": 24129096.8,
        "rub_per_camera_month": 6702.53
      },
      {
        "cameras": 200,
        "chips": 52,
        "servers": 14,
        "tco_3_year_rub": 46358476.8,
        "rub_per_camera_month": 6438.68
      },
      {
        "cameras": 500,
        "chips": 124,
        "servers": 32,
        "tco_3_year_rub": 109169361.6,
        "rub_per_camera_month": 6064.96
      }
    ],
    "note": "Стоимость базового нового внедрения, без зачёта старого инвентаря; доля физических покупок взята из расчётной области."
  },
  "operator_events_per_shift": null,
  "evidence": [
    {
      "key": "request.site.workshops",
      "title": "request.site.workshops",
      "value": 2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.site.workers",
      "title": "request.site.workers",
      "value": 200,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.site.shifts_per_day",
      "title": "request.site.shifts_per_day",
      "value": 2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.site.working_days_year",
      "title": "request.site.working_days_year",
      "value": 250,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.site.operators",
      "title": "request.site.operators",
      "value": 2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.activity_share",
      "title": "request.load.activity_share",
      "value": 0.5,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.target_fps",
      "title": "request.load.target_fps",
      "value": 12,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.surge_fps",
      "title": "request.load.surge_fps",
      "value": 5,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.idle_check_s",
      "title": "request.load.idle_check_s",
      "value": 4,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.priority_cameras_reserve",
      "title": "request.load.priority_cameras_reserve",
      "value": 1,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.detector_stride",
      "title": "request.load.detector_stride",
      "value": 1,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.reference_chip_fps",
      "title": "request.load.reference_chip_fps",
      "value": 104.8,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "vendor_pose_benchmark"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.capacity_derate",
      "title": "request.load.capacity_derate",
      "value": 0.5,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.platform_capacity_override_fps",
      "title": "request.load.platform_capacity_override_fps",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.load.cpu_ms_per_unit",
      "title": "request.load.cpu_ms_per_unit",
      "value": 77,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.load.decode_cores_per_camera",
      "title": "request.load.decode_cores_per_camera",
      "value": 0,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.hardware.server.slots",
      "title": "request.hardware.server.slots",
      "value": 4,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.hardware.server.usable_cpu_cores",
      "title": "request.hardware.server.usable_cpu_cores",
      "value": 16,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.hardware.server.price_rub",
      "title": "request.hardware.server.price_rub",
      "value": 350000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.hardware.server.power_w",
      "title": "request.hardware.server.power_w",
      "value": 250,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.integration_fixed_rub",
      "title": "request.costs.integration_fixed_rub",
      "value": 300000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.integration_per_camera_rub",
      "title": "request.costs.integration_per_camera_rub",
      "value": 0,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.support_share_year",
      "title": "request.costs.support_share_year",
      "value": 0.15,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.electricity_rub_kwh",
      "title": "request.costs.electricity_rub_kwh",
      "value": 8,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.operating_hours_year",
      "title": "request.costs.operating_hours_year",
      "value": 8760,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.signal_zones_per_camera",
      "title": "request.costs.signal_zones_per_camera",
      "value": 1,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.signal_unit_rub",
      "title": "request.costs.signal_unit_rub",
      "value": 25000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.speaker_per_workshop_rub",
      "title": "request.costs.speaker_per_workshop_rub",
      "value": 40000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.new_camera_unit_rub",
      "title": "request.costs.new_camera_unit_rub",
      "value": 30000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.new_camera_count",
      "title": "request.costs.new_camera_count",
      "value": 0,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.costs.max_additional_camera_share",
      "title": "request.costs.max_additional_camera_share",
      "value": 0.2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.injuries.annual_injured_workers",
      "title": "request.benefits.injuries.annual_injured_workers",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.injuries.rate_per_1000",
      "title": "request.benefits.injuries.rate_per_1000",
      "value": 1.17,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "rosstat_injury_rate"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.injuries.cost_per_injured_worker_rub",
      "title": "request.benefits.injuries.cost_per_injured_worker_rub",
      "value": 1000000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.injuries.reduction.base",
      "title": "request.benefits.injuries.reduction.base",
      "value": 0.2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.injuries.reduction.extended",
      "title": "request.benefits.injuries.reduction.extended",
      "value": 0.3,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.injuries.reduction.max",
      "title": "request.benefits.injuries.reduction.max",
      "value": 0.4,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.downtime.events_year",
      "title": "request.benefits.downtime.events_year",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.downtime.days_per_event",
      "title": "request.benefits.downtime.days_per_event",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.downtime.day_cost_rub",
      "title": "request.benefits.downtime.day_cost_rub",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.downtime.reduction.base",
      "title": "request.benefits.downtime.reduction.base",
      "value": 0.2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.downtime.reduction.extended",
      "title": "request.benefits.downtime.reduction.extended",
      "value": 0.3,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.downtime.reduction.max",
      "title": "request.benefits.downtime.reduction.max",
      "value": 0.4,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.0.inspection_probability_year",
      "title": "request.benefits.fines.items.0.inspection_probability_year",
      "value": 0.1,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.0.amount_rub",
      "title": "request.benefits.fines.items.0.amount_rub",
      "value": 65000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.0.reduction.base",
      "title": "request.benefits.fines.items.0.reduction.base",
      "value": 0.2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.0.reduction.extended",
      "title": "request.benefits.fines.items.0.reduction.extended",
      "value": 0.3,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.0.reduction.max",
      "title": "request.benefits.fines.items.0.reduction.max",
      "value": 0.4,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.1.inspection_probability_year",
      "title": "request.benefits.fines.items.1.inspection_probability_year",
      "value": 0.1,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.1.amount_rub",
      "title": "request.benefits.fines.items.1.amount_rub",
      "value": 140000,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.1.reduction.base",
      "title": "request.benefits.fines.items.1.reduction.base",
      "value": 0.2,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.1.reduction.extended",
      "title": "request.benefits.fines.items.1.reduction.extended",
      "value": 0.3,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.fines.items.1.reduction.max",
      "title": "request.benefits.fines.items.1.reduction.max",
      "value": 0.4,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.sfr_discount.payroll_rub_year",
      "title": "request.benefits.sfr_discount.payroll_rub_year",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.sfr_discount.tariff_share",
      "title": "request.benefits.sfr_discount.tariff_share",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.sfr_discount.additional_discount_share",
      "title": "request.benefits.sfr_discount.additional_discount_share",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.labor.rows.0.hours_saved_year",
      "title": "request.benefits.labor.rows.0.hours_saved_year",
      "value": 0,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.labor.rows.0.hour_cost_rub",
      "title": "request.benefits.labor.rows.0.hour_cost_rub",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.labor.rows.1.hours_saved_year",
      "title": "request.benefits.labor.rows.1.hours_saved_year",
      "value": 0,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.benefits.labor.rows.1.hour_cost_rub",
      "title": "request.benefits.labor.rows.1.hour_cost_rub",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.benefits.severe_injury_cost_rub",
      "title": "request.benefits.severe_injury_cost_rub",
      "value": null,
      "unit": "значение",
      "status": "missing",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "request.cameras.cameras",
      "title": "request.cameras.cameras",
      "value": 8,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "request.cameras.groups.0.share",
      "title": "request.cameras.groups.0.share",
      "value": 1,
      "unit": "значение",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HP.chips",
      "title": "catalog.boards.HP.chips",
      "value": 1,
      "unit": "шт.",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hp",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HP.slots",
      "title": "catalog.boards.HP.slots",
      "value": 1,
      "unit": "шт.",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hp",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HP.power_w",
      "title": "catalog.boards.HP.power_w",
      "value": 35,
      "unit": "Вт",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hp",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HP.price_rub",
      "title": "catalog.boards.HP.price_rub",
      "value": 500000,
      "unit": "₽",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hp",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPD.chips",
      "title": "catalog.boards.HPD.chips",
      "value": 2,
      "unit": "шт.",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpd",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPD.slots",
      "title": "catalog.boards.HPD.slots",
      "value": 1,
      "unit": "шт.",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpd",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPD.power_w",
      "title": "catalog.boards.HPD.power_w",
      "value": 100,
      "unit": "Вт",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpd",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPD.price_rub",
      "title": "catalog.boards.HPD.price_rub",
      "value": null,
      "unit": "₽",
      "status": "missing",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpd",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "catalog.boards.HPQ.chips",
      "title": "catalog.boards.HPQ.chips",
      "value": 4,
      "unit": "шт.",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpq",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPQ.slots",
      "title": "catalog.boards.HPQ.slots",
      "value": 1,
      "unit": "шт.",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpq",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPQ.power_w",
      "title": "catalog.boards.HPQ.power_w",
      "value": 150,
      "unit": "Вт",
      "status": "assumed",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpq",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.boards.HPQ.price_rub",
      "title": "catalog.boards.HPQ.price_rub",
      "value": null,
      "unit": "₽",
      "status": "missing",
      "source_ids": [
        "vendor_modules",
        "vendor_board_power_hpq",
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": "Значение не задано; включение зависит от выбранной строки расчёта."
    },
    {
      "key": "catalog.models.detector.work_units",
      "title": "catalog.models.detector.work_units",
      "value": 1,
      "unit": "экв.ед.",
      "status": "assumed",
      "source_ids": [
        "team_defaults"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "catalog.models.pose.work_units",
      "title": "catalog.models.pose.work_units",
      "value": 1,
      "unit": "экв.ед.",
      "status": "assumed",
      "source_ids": [
        "vendor_pose_benchmark"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "load.cameras",
      "title": "load.cameras",
      "value": 8,
      "unit": "значение",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Формулы К6",
      "depends_on": [
        "request.load.target_fps",
        "request.load.activity_share"
      ],
      "reason": null
    },
    {
      "key": "load.active_p95",
      "title": "load.active_p95",
      "value": 6,
      "unit": "значение",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Формулы К6",
      "depends_on": [
        "request.load.target_fps",
        "request.load.activity_share"
      ],
      "reason": null
    },
    {
      "key": "load.priority_cameras_effective",
      "title": "load.priority_cameras_effective",
      "value": 1,
      "unit": "значение",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Формулы К6",
      "depends_on": [
        "request.load.target_fps",
        "request.load.activity_share"
      ],
      "reason": null
    },
    {
      "key": "load.peak_units_s",
      "title": "load.peak_units_s",
      "value": 144.5,
      "unit": "значение",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Формулы К6",
      "depends_on": [
        "request.load.target_fps",
        "request.load.activity_share"
      ],
      "reason": null
    },
    {
      "key": "load.surge_units_s",
      "title": "load.surge_units_s",
      "value": 94.0,
      "unit": "значение",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Формулы К6",
      "depends_on": [
        "request.load.target_fps",
        "request.load.activity_share"
      ],
      "reason": null
    },
    {
      "key": "load.required_units_s",
      "title": "load.required_units_s",
      "value": 144.5,
      "unit": "значение",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Формулы К6",
      "depends_on": [
        "request.load.target_fps",
        "request.load.activity_share"
      ],
      "reason": null
    },
    {
      "key": "load.effective_chip_units_s",
      "title": "load.effective_chip_units_s",
      "value": 52.4,
      "unit": "значение",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Формулы К6",
      "depends_on": [
        "request.load.target_fps",
        "request.load.activity_share"
      ],
      "reason": null
    },
    {
      "key": "load.required_chips",
      "title": "load.required_chips",
      "value": 3,
      "unit": "значение",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Формулы К6",
      "depends_on": [
        "request.load.target_fps",
        "request.load.activity_share"
      ],
      "reason": null
    },
    {
      "key": "load.required_cpu_cores",
      "title": "load.required_cpu_cores",
      "value": 11.1265,
      "unit": "значение",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Формулы К6",
      "depends_on": [
        "request.load.target_fps",
        "request.load.activity_share"
      ],
      "reason": null
    },
    {
      "key": "load.naive_chips",
      "title": "load.naive_chips",
      "value": 16,
      "unit": "значение",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Формулы К6",
      "depends_on": [
        "request.load.target_fps",
        "request.load.activity_share"
      ],
      "reason": null
    },
    {
      "key": "hardware.purchase.HP.count",
      "title": "hardware.purchase.HP.count",
      "value": 3,
      "unit": "шт.",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "max(0, required_chips-installed_chips)",
      "depends_on": [
        "load.required_chips"
      ],
      "reason": null
    },
    {
      "key": "hardware.purchase.servers",
      "title": "hardware.purchase.servers",
      "value": 1,
      "unit": "шт.",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "max(0, required_servers-installed_servers)",
      "depends_on": [
        "load.required_cpu_cores"
      ],
      "reason": null
    },
    {
      "key": "hardware.board_capex_rub",
      "title": "hardware.board_capex_rub",
      "value": 1500000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "purchase.HP.count * HP.price",
      "depends_on": [
        "hardware.purchase.HP.count",
        "catalog.boards.HP.price_rub"
      ],
      "reason": null
    },
    {
      "key": "hardware.server_capex_rub",
      "title": "hardware.server_capex_rub",
      "value": 350000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "purchase.servers * server.price",
      "depends_on": [
        "hardware.purchase.servers",
        "request.hardware.server.price_rub"
      ],
      "reason": null
    },
    {
      "key": "cost.electricity_rub_year",
      "title": "cost.electricity_rub_year",
      "value": 24878.4,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "power_scope_w/1000 * hours * tariff",
      "depends_on": [
        "request.costs.operating_hours_year",
        "request.costs.electricity_rub_kwh"
      ],
      "reason": null
    },
    {
      "key": "benefits.injured_workers_year",
      "title": "benefits.injured_workers_year",
      "value": 0.234,
      "unit": "чел./год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "workers * rate_per_1000 / 1000",
      "depends_on": [
        "request.site.workers",
        "request.benefits.injuries.rate_per_1000"
      ],
      "reason": null
    },
    {
      "key": "tier.base.capex.boards",
      "title": "tier.base.capex.boards",
      "value": 1500000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Новые платы LinQ",
      "depends_on": [
        "hardware.board_capex_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.base.capex.servers",
      "title": "tier.base.capex.servers",
      "value": 350000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Новые серверы",
      "depends_on": [
        "hardware.server_capex_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.base.capex.integration_fixed",
      "title": "tier.base.capex.integration_fixed",
      "value": 300000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Пусконаладка: фиксированная часть",
      "depends_on": [
        "request.costs.integration_fixed_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.base.capex.integration_cameras",
      "title": "tier.base.capex.integration_cameras",
      "value": 0.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Пусконаладка камер",
      "depends_on": [
        "request.costs.integration_per_camera_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.base.capex.physical_cameras",
      "title": "tier.base.capex.physical_cameras",
      "value": 0.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Покупка физических камер",
      "depends_on": [
        "request.costs.new_camera_count",
        "request.costs.new_camera_unit_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.base.capex_rub",
      "title": "tier.base.capex_rub",
      "value": 2150000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "sum(capex_lines)",
      "depends_on": [
        "tier.base.capex.boards",
        "tier.base.capex.servers",
        "tier.base.capex.integration_fixed",
        "tier.base.capex.integration_cameras",
        "tier.base.capex.physical_cameras"
      ],
      "reason": null
    },
    {
      "key": "tier.base.opex.support",
      "title": "tier.base.opex.support",
      "value": 322500.0,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "capex * support_share_year",
      "depends_on": [
        "tier.base.capex_rub",
        "request.costs.support_share_year"
      ],
      "reason": null
    },
    {
      "key": "tier.base.opex_rub_year",
      "title": "tier.base.opex_rub_year",
      "value": 347378.4,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "support + electricity",
      "depends_on": [
        "tier.base.opex.support",
        "cost.electricity_rub_year"
      ],
      "reason": null
    },
    {
      "key": "tier.base.benefit.injuries",
      "title": "tier.base.benefit.injuries",
      "value": 46800.0,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "injured_year * direct_cost * reduction",
      "depends_on": [
        "benefits.injured_workers_year",
        "request.benefits.injuries.cost_per_injured_worker_rub",
        "request.benefits.injuries.reduction.base"
      ],
      "reason": null
    },
    {
      "key": "tier.base.benefit.downtime",
      "title": "tier.base.benefit.downtime",
      "value": 0,
      "unit": "₽/год",
      "status": "not_applicable",
      "source_ids": [
        "user_input"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "tier.base.benefit.fines",
      "title": "tier.base.benefit.fines",
      "value": 0,
      "unit": "₽/год",
      "status": "not_applicable",
      "source_ids": [
        "user_input"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "tier.base.benefit.sfr_discount",
      "title": "tier.base.benefit.sfr_discount",
      "value": 0,
      "unit": "₽/год",
      "status": "not_applicable",
      "source_ids": [
        "user_input"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "tier.base.benefit.labor",
      "title": "tier.base.benefit.labor",
      "value": 0,
      "unit": "₽/год",
      "status": "not_applicable",
      "source_ids": [
        "user_input"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "tier.base.gross_benefit_rub_year",
      "title": "tier.base.gross_benefit_rub_year",
      "value": 46800.0,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "sum(included benefits)",
      "depends_on": [
        "tier.base.benefit.injuries",
        "tier.base.benefit.downtime",
        "tier.base.benefit.fines",
        "tier.base.benefit.sfr_discount",
        "tier.base.benefit.labor"
      ],
      "reason": null
    },
    {
      "key": "tier.base.net_benefit_rub_year",
      "title": "tier.base.net_benefit_rub_year",
      "value": -300578.4,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "gross - opex",
      "depends_on": [
        "tier.base.gross_benefit_rub_year",
        "tier.base.opex_rub_year"
      ],
      "reason": null
    },
    {
      "key": "tier.base.tco_3_year_rub",
      "title": "tier.base.tco_3_year_rub",
      "value": 3192135.2,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "capex + 3*opex",
      "depends_on": [
        "tier.base.capex_rub",
        "tier.base.opex_rub_year"
      ],
      "reason": null
    },
    {
      "key": "tier.base.net_balance_3_year_rub",
      "title": "tier.base.net_balance_3_year_rub",
      "value": -3051735.2,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "3*gross - TCO3",
      "depends_on": [
        "tier.base.gross_benefit_rub_year",
        "tier.base.tco_3_year_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.base.rub_per_camera_month",
      "title": "tier.base.rub_per_camera_month",
      "value": 11083.8,
      "unit": "₽/камера/мес",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "TCO3 / (Nscope*36)",
      "depends_on": [
        "tier.base.tco_3_year_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.base.board_price_threshold.c_other_rub",
      "title": "tier.base.board_price_threshold.c_other_rub",
      "value": 650000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "sum(capex_lines except variable HP purchase)",
      "depends_on": [
        "tier.base.capex.servers",
        "tier.base.capex.integration_fixed",
        "tier.base.capex.integration_cameras",
        "tier.base.capex.physical_cameras"
      ],
      "reason": null
    },
    {
      "key": "tier.base.board_price_threshold.raw_unit_price_rub",
      "title": "tier.base.board_price_threshold.raw_unit_price_rub",
      "value": -201548.32,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "(3*(B-electricity)/(1+3*r)-C_other)/q",
      "depends_on": [
        "tier.base.board_price_threshold.c_other_rub",
        "tier.base.gross_benefit_rub_year",
        "cost.electricity_rub_year",
        "request.costs.support_share_year"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.capex.boards",
      "title": "tier.extended.capex.boards",
      "value": 1500000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Новые платы LinQ",
      "depends_on": [
        "hardware.board_capex_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.capex.servers",
      "title": "tier.extended.capex.servers",
      "value": 350000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Новые серверы",
      "depends_on": [
        "hardware.server_capex_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.capex.integration_fixed",
      "title": "tier.extended.capex.integration_fixed",
      "value": 300000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Пусконаладка: фиксированная часть",
      "depends_on": [
        "request.costs.integration_fixed_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.capex.integration_cameras",
      "title": "tier.extended.capex.integration_cameras",
      "value": 0.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Пусконаладка камер",
      "depends_on": [
        "request.costs.integration_per_camera_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.capex.physical_cameras",
      "title": "tier.extended.capex.physical_cameras",
      "value": 0.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Покупка физических камер",
      "depends_on": [
        "request.costs.new_camera_count",
        "request.costs.new_camera_unit_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.capex.signals",
      "title": "tier.extended.capex.signals",
      "value": 200000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Световые и звуковые сигналы зон",
      "depends_on": [
        "request.costs.signal_zones_per_camera",
        "request.costs.signal_unit_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.capex_rub",
      "title": "tier.extended.capex_rub",
      "value": 2350000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "sum(capex_lines)",
      "depends_on": [
        "tier.extended.capex.boards",
        "tier.extended.capex.servers",
        "tier.extended.capex.integration_fixed",
        "tier.extended.capex.integration_cameras",
        "tier.extended.capex.physical_cameras",
        "tier.extended.capex.signals"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.opex.support",
      "title": "tier.extended.opex.support",
      "value": 352500.0,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "capex * support_share_year",
      "depends_on": [
        "tier.extended.capex_rub",
        "request.costs.support_share_year"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.opex_rub_year",
      "title": "tier.extended.opex_rub_year",
      "value": 377378.4,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "support + electricity",
      "depends_on": [
        "tier.extended.opex.support",
        "cost.electricity_rub_year"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.benefit.injuries",
      "title": "tier.extended.benefit.injuries",
      "value": 70200.0,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "injured_year * direct_cost * reduction",
      "depends_on": [
        "benefits.injured_workers_year",
        "request.benefits.injuries.cost_per_injured_worker_rub",
        "request.benefits.injuries.reduction.extended"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.benefit.downtime",
      "title": "tier.extended.benefit.downtime",
      "value": 0,
      "unit": "₽/год",
      "status": "not_applicable",
      "source_ids": [
        "user_input"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "tier.extended.benefit.fines",
      "title": "tier.extended.benefit.fines",
      "value": 0,
      "unit": "₽/год",
      "status": "not_applicable",
      "source_ids": [
        "user_input"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "tier.extended.benefit.sfr_discount",
      "title": "tier.extended.benefit.sfr_discount",
      "value": 0,
      "unit": "₽/год",
      "status": "not_applicable",
      "source_ids": [
        "user_input"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "tier.extended.benefit.labor",
      "title": "tier.extended.benefit.labor",
      "value": 0,
      "unit": "₽/год",
      "status": "not_applicable",
      "source_ids": [
        "user_input"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "tier.extended.gross_benefit_rub_year",
      "title": "tier.extended.gross_benefit_rub_year",
      "value": 70200.0,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "sum(included benefits)",
      "depends_on": [
        "tier.extended.benefit.injuries",
        "tier.extended.benefit.downtime",
        "tier.extended.benefit.fines",
        "tier.extended.benefit.sfr_discount",
        "tier.extended.benefit.labor"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.net_benefit_rub_year",
      "title": "tier.extended.net_benefit_rub_year",
      "value": -307178.4,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "gross - opex",
      "depends_on": [
        "tier.extended.gross_benefit_rub_year",
        "tier.extended.opex_rub_year"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.tco_3_year_rub",
      "title": "tier.extended.tco_3_year_rub",
      "value": 3482135.2,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "capex + 3*opex",
      "depends_on": [
        "tier.extended.capex_rub",
        "tier.extended.opex_rub_year"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.net_balance_3_year_rub",
      "title": "tier.extended.net_balance_3_year_rub",
      "value": -3271535.2,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "3*gross - TCO3",
      "depends_on": [
        "tier.extended.gross_benefit_rub_year",
        "tier.extended.tco_3_year_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.rub_per_camera_month",
      "title": "tier.extended.rub_per_camera_month",
      "value": 12090.75,
      "unit": "₽/камера/мес",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "TCO3 / (Nscope*36)",
      "depends_on": [
        "tier.extended.tco_3_year_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.board_price_threshold.c_other_rub",
      "title": "tier.extended.board_price_threshold.c_other_rub",
      "value": 850000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "sum(capex_lines except variable HP purchase)",
      "depends_on": [
        "tier.extended.capex.servers",
        "tier.extended.capex.integration_fixed",
        "tier.extended.capex.integration_cameras",
        "tier.extended.capex.physical_cameras",
        "tier.extended.capex.signals"
      ],
      "reason": null
    },
    {
      "key": "tier.extended.board_price_threshold.raw_unit_price_rub",
      "title": "tier.extended.board_price_threshold.raw_unit_price_rub",
      "value": -252077.06,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "(3*(B-electricity)/(1+3*r)-C_other)/q",
      "depends_on": [
        "tier.extended.board_price_threshold.c_other_rub",
        "tier.extended.gross_benefit_rub_year",
        "cost.electricity_rub_year",
        "request.costs.support_share_year"
      ],
      "reason": null
    },
    {
      "key": "tier.max.capex.boards",
      "title": "tier.max.capex.boards",
      "value": 1500000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Новые платы LinQ",
      "depends_on": [
        "hardware.board_capex_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.max.capex.servers",
      "title": "tier.max.capex.servers",
      "value": 350000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Новые серверы",
      "depends_on": [
        "hardware.server_capex_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.max.capex.integration_fixed",
      "title": "tier.max.capex.integration_fixed",
      "value": 300000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Пусконаладка: фиксированная часть",
      "depends_on": [
        "request.costs.integration_fixed_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.max.capex.integration_cameras",
      "title": "tier.max.capex.integration_cameras",
      "value": 0.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Пусконаладка камер",
      "depends_on": [
        "request.costs.integration_per_camera_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.max.capex.physical_cameras",
      "title": "tier.max.capex.physical_cameras",
      "value": 0.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Покупка физических камер",
      "depends_on": [
        "request.costs.new_camera_count",
        "request.costs.new_camera_unit_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.max.capex.signals",
      "title": "tier.max.capex.signals",
      "value": 200000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Световые и звуковые сигналы зон",
      "depends_on": [
        "request.costs.signal_zones_per_camera",
        "request.costs.signal_unit_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.max.capex.speakers",
      "title": "tier.max.capex.speakers",
      "value": 80000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Громкоговорители в цехах",
      "depends_on": [
        "request.site.workshops",
        "request.costs.speaker_per_workshop_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.max.capex.max_cameras",
      "title": "tier.max.capex.max_cameras",
      "value": 60000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К8: Дополнительное оснащение каналов камерами",
      "depends_on": [
        "request.costs.max_additional_camera_share",
        "request.costs.new_camera_unit_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.max.capex_rub",
      "title": "tier.max.capex_rub",
      "value": 2490000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "sum(capex_lines)",
      "depends_on": [
        "tier.max.capex.boards",
        "tier.max.capex.servers",
        "tier.max.capex.integration_fixed",
        "tier.max.capex.integration_cameras",
        "tier.max.capex.physical_cameras",
        "tier.max.capex.signals",
        "tier.max.capex.speakers",
        "tier.max.capex.max_cameras"
      ],
      "reason": null
    },
    {
      "key": "tier.max.opex.support",
      "title": "tier.max.opex.support",
      "value": 373500.0,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "capex * support_share_year",
      "depends_on": [
        "tier.max.capex_rub",
        "request.costs.support_share_year"
      ],
      "reason": null
    },
    {
      "key": "tier.max.opex_rub_year",
      "title": "tier.max.opex_rub_year",
      "value": 398378.4,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "support + electricity",
      "depends_on": [
        "tier.max.opex.support",
        "cost.electricity_rub_year"
      ],
      "reason": null
    },
    {
      "key": "tier.max.benefit.injuries",
      "title": "tier.max.benefit.injuries",
      "value": 93600.0,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "injured_year * direct_cost * reduction",
      "depends_on": [
        "benefits.injured_workers_year",
        "request.benefits.injuries.cost_per_injured_worker_rub",
        "request.benefits.injuries.reduction.max"
      ],
      "reason": null
    },
    {
      "key": "tier.max.benefit.downtime",
      "title": "tier.max.benefit.downtime",
      "value": 0,
      "unit": "₽/год",
      "status": "not_applicable",
      "source_ids": [
        "user_input"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "tier.max.benefit.fines",
      "title": "tier.max.benefit.fines",
      "value": 0,
      "unit": "₽/год",
      "status": "not_applicable",
      "source_ids": [
        "user_input"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "tier.max.benefit.sfr_discount",
      "title": "tier.max.benefit.sfr_discount",
      "value": 0,
      "unit": "₽/год",
      "status": "not_applicable",
      "source_ids": [
        "user_input"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "tier.max.benefit.labor",
      "title": "tier.max.benefit.labor",
      "value": 0,
      "unit": "₽/год",
      "status": "not_applicable",
      "source_ids": [
        "user_input"
      ],
      "formula": null,
      "depends_on": [],
      "reason": null
    },
    {
      "key": "tier.max.gross_benefit_rub_year",
      "title": "tier.max.gross_benefit_rub_year",
      "value": 93600.0,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "sum(included benefits)",
      "depends_on": [
        "tier.max.benefit.injuries",
        "tier.max.benefit.downtime",
        "tier.max.benefit.fines",
        "tier.max.benefit.sfr_discount",
        "tier.max.benefit.labor"
      ],
      "reason": null
    },
    {
      "key": "tier.max.net_benefit_rub_year",
      "title": "tier.max.net_benefit_rub_year",
      "value": -304778.4,
      "unit": "₽/год",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "gross - opex",
      "depends_on": [
        "tier.max.gross_benefit_rub_year",
        "tier.max.opex_rub_year"
      ],
      "reason": null
    },
    {
      "key": "tier.max.tco_3_year_rub",
      "title": "tier.max.tco_3_year_rub",
      "value": 3685135.2,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "capex + 3*opex",
      "depends_on": [
        "tier.max.capex_rub",
        "tier.max.opex_rub_year"
      ],
      "reason": null
    },
    {
      "key": "tier.max.net_balance_3_year_rub",
      "title": "tier.max.net_balance_3_year_rub",
      "value": -3404335.2,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "3*gross - TCO3",
      "depends_on": [
        "tier.max.gross_benefit_rub_year",
        "tier.max.tco_3_year_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.max.rub_per_camera_month",
      "title": "tier.max.rub_per_camera_month",
      "value": 12795.61,
      "unit": "₽/камера/мес",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "TCO3 / (Nscope*36)",
      "depends_on": [
        "tier.max.tco_3_year_rub"
      ],
      "reason": null
    },
    {
      "key": "tier.max.board_price_threshold.c_other_rub",
      "title": "tier.max.board_price_threshold.c_other_rub",
      "value": 990000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "sum(capex_lines except variable HP purchase)",
      "depends_on": [
        "tier.max.capex.servers",
        "tier.max.capex.integration_fixed",
        "tier.max.capex.integration_cameras",
        "tier.max.capex.physical_cameras",
        "tier.max.capex.signals",
        "tier.max.capex.speakers",
        "tier.max.capex.max_cameras"
      ],
      "reason": null
    },
    {
      "key": "tier.max.board_price_threshold.raw_unit_price_rub",
      "title": "tier.max.board_price_threshold.raw_unit_price_rub",
      "value": -282605.79,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "(3*(B-electricity)/(1+3*r)-C_other)/q",
      "depends_on": [
        "tier.max.board_price_threshold.c_other_rub",
        "tier.max.gross_benefit_rub_year",
        "cost.electricity_rub_year",
        "request.costs.support_share_year"
      ],
      "reason": null
    },
    {
      "key": "steps.naive.chips",
      "title": "steps.naive.chips",
      "value": 16,
      "unit": "шт.",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К6: ступень naive",
      "depends_on": [
        "load.required_chips"
      ],
      "reason": null
    },
    {
      "key": "steps.naive.equipment_capex_rub",
      "title": "steps.naive.equipment_capex_rub",
      "value": 9400000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "boards+servers, greenfield",
      "depends_on": [
        "catalog.boards.HP.price_rub"
      ],
      "reason": null
    },
    {
      "key": "steps.dedicated_capacity.chips",
      "title": "steps.dedicated_capacity.chips",
      "value": 4,
      "unit": "шт.",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К6: ступень dedicated_capacity",
      "depends_on": [
        "load.required_chips"
      ],
      "reason": null
    },
    {
      "key": "steps.dedicated_capacity.equipment_capex_rub",
      "title": "steps.dedicated_capacity.equipment_capex_rub",
      "value": 2350000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "boards+servers, greenfield",
      "depends_on": [
        "catalog.boards.HP.price_rub"
      ],
      "reason": null
    },
    {
      "key": "steps.scenario_models.chips",
      "title": "steps.scenario_models.chips",
      "value": 4,
      "unit": "шт.",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К6: ступень scenario_models",
      "depends_on": [
        "load.required_chips"
      ],
      "reason": null
    },
    {
      "key": "steps.scenario_models.equipment_capex_rub",
      "title": "steps.scenario_models.equipment_capex_rub",
      "value": 2350000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "boards+servers, greenfield",
      "depends_on": [
        "catalog.boards.HP.price_rub"
      ],
      "reason": null
    },
    {
      "key": "steps.activity_pool.chips",
      "title": "steps.activity_pool.chips",
      "value": 3,
      "unit": "шт.",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "К6: ступень activity_pool",
      "depends_on": [
        "load.required_chips"
      ],
      "reason": null
    },
    {
      "key": "steps.activity_pool.equipment_capex_rub",
      "title": "steps.activity_pool.equipment_capex_rub",
      "value": 1850000.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "boards+servers, greenfield",
      "depends_on": [
        "catalog.boards.HP.price_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.5.tco_3_year_rub",
      "title": "curve.5.tco_3_year_rub",
      "value": 2459776.8,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Greenfield base: C+3O",
      "depends_on": [
        "catalog.boards.HP.price_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.5.rub_per_camera_month",
      "title": "curve.5.rub_per_camera_month",
      "value": 13665.43,
      "unit": "₽/камера/мес",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "curve TCO3/(N*36)",
      "depends_on": [
        "curve.5.tco_3_year_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.10.tco_3_year_rub",
      "title": "curve.10.tco_3_year_rub",
      "value": 3924493.6,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Greenfield base: C+3O",
      "depends_on": [
        "catalog.boards.HP.price_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.10.rub_per_camera_month",
      "title": "curve.10.rub_per_camera_month",
      "value": 10901.37,
      "unit": "₽/камера/мес",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "curve TCO3/(N*36)",
      "depends_on": [
        "curve.10.tco_3_year_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.25.tco_3_year_rub",
      "title": "curve.25.tco_3_year_rub",
      "value": 7413987.2,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Greenfield base: C+3O",
      "depends_on": [
        "catalog.boards.HP.price_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.25.rub_per_camera_month",
      "title": "curve.25.rub_per_camera_month",
      "value": 8237.76,
      "unit": "₽/камера/мес",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "curve TCO3/(N*36)",
      "depends_on": [
        "curve.25.tco_3_year_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.50.tco_3_year_rub",
      "title": "curve.50.tco_3_year_rub",
      "value": 13660616.0,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Greenfield base: C+3O",
      "depends_on": [
        "catalog.boards.HP.price_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.50.rub_per_camera_month",
      "title": "curve.50.rub_per_camera_month",
      "value": 7589.23,
      "unit": "₽/камера/мес",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "curve TCO3/(N*36)",
      "depends_on": [
        "curve.50.tco_3_year_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.100.tco_3_year_rub",
      "title": "curve.100.tco_3_year_rub",
      "value": 24129096.8,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Greenfield base: C+3O",
      "depends_on": [
        "catalog.boards.HP.price_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.100.rub_per_camera_month",
      "title": "curve.100.rub_per_camera_month",
      "value": 6702.53,
      "unit": "₽/камера/мес",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "curve TCO3/(N*36)",
      "depends_on": [
        "curve.100.tco_3_year_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.200.tco_3_year_rub",
      "title": "curve.200.tco_3_year_rub",
      "value": 46358476.8,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Greenfield base: C+3O",
      "depends_on": [
        "catalog.boards.HP.price_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.200.rub_per_camera_month",
      "title": "curve.200.rub_per_camera_month",
      "value": 6438.68,
      "unit": "₽/камера/мес",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "curve TCO3/(N*36)",
      "depends_on": [
        "curve.200.tco_3_year_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.500.tco_3_year_rub",
      "title": "curve.500.tco_3_year_rub",
      "value": 109169361.6,
      "unit": "₽",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "Greenfield base: C+3O",
      "depends_on": [
        "catalog.boards.HP.price_rub"
      ],
      "reason": null
    },
    {
      "key": "curve.500.rub_per_camera_month",
      "title": "curve.500.rub_per_camera_month",
      "value": 6064.96,
      "unit": "₽/камера/мес",
      "status": "derived",
      "source_ids": [
        "team_defaults"
      ],
      "formula": "curve TCO3/(N*36)",
      "depends_on": [
        "curve.500.tco_3_year_rub"
      ],
      "reason": null
    }
  ],
  "sources": [
    {
      "id": "team_defaults",
      "title": "Расчётные допущения команды Argus",
      "kind": "team_assumption",
      "verification": "not_applicable",
      "url": null,
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "Цены, CPU, запас, сервер и эффект — редактируемые допущения, не замеры."
    },
    {
      "id": "user_input",
      "title": "Данные, введённые в этот расчётный пример",
      "kind": "user_input",
      "verification": "not_applicable",
      "url": null,
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "Эталонный пользовательский ввод; не данные реально обследованного завода."
    },
    {
      "id": "vendor_pose_benchmark",
      "title": "Бенчмарк LinQ: yolov8n-pose, batch 1",
      "kind": "vendor_claim",
      "verification": "cached_primary",
      "url": "https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf",
      "data_year": 2026,
      "published_at": null,
      "checked_at": null,
      "note": "104,8 FPS: заявление вендора; сохранённая первичная выписка, не замер Argus."
    },
    {
      "id": "vendor_modules",
      "title": "Модули LinQ HP, HPD, HPQ",
      "kind": "vendor_claim",
      "verification": "verified_primary",
      "url": "https://lin-q.ru/sol",
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "HP=1, HPD=2, HPQ=4 чипа."
    },
    {
      "id": "vendor_board_power_hp",
      "title": "Паспортная мощность конкретного исполнения HP",
      "kind": "vendor_claim",
      "verification": "cached_primary",
      "url": "https://files.lin-q.ru/tpu/docs/_HPact_manual_LINQ_HP1M_02.pdf",
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "35 Вт — верхняя паспортная граница, не измеренное потребление."
    },
    {
      "id": "vendor_board_power_hpd",
      "title": "Паспортная мощность конкретного исполнения HPD",
      "kind": "vendor_claim",
      "verification": "cached_primary",
      "url": "https://files.lin-q.ru/tpu/docs/_HPDpass_manual_LINQ_HPD1M_01.pdf",
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "100 Вт — верхняя паспортная граница."
    },
    {
      "id": "vendor_board_power_hpq",
      "title": "Паспортная мощность конкретного исполнения HPQ",
      "kind": "vendor_claim",
      "verification": "cached_primary",
      "url": "https://files.lin-q.ru/tpu/docs/_HPQpass_manual_LINQ_HPD1M_10.pdf",
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "150 Вт — верхняя паспортная граница."
    },
    {
      "id": "rosstat_injury_rate",
      "title": "Отраслевая подсказка частоты пострадавших",
      "kind": "official",
      "verification": "pending_primary",
      "url": "https://rosstat.gov.ru/working_conditions",
      "data_year": 2025,
      "published_at": null,
      "checked_at": null,
      "note": "1,17 на 1000 за 2025 из локальной выписки; первичный массив требует проверки."
    },
    {
      "id": "linq_historical_report",
      "title": "Историческое подтверждение исполнения detector и pose на LinQ",
      "kind": "argus_measurement",
      "verification": "cached_primary",
      "url": null,
      "data_year": null,
      "published_at": null,
      "checked_at": null,
      "note": "Существовавший до этого контракта отчёт; новых замеров эти JSON не изображают."
    }
  ],
  "warnings": [
    {
      "code": "MODELED_POLICY_NOT_DEPLOYED",
      "field": "load",
      "message": "Экономия — модель будущего внедрения; текущий конвейер не изменяется."
    },
    {
      "code": "INDEPENDENT_ACTIVITY_ASSUMPTION",
      "field": "load.activity_share",
      "message": "Независимая активность камер является допущением."
    },
    {
      "code": "PRIORITY_RESERVE_LIMIT",
      "field": "load.priority_cameras_reserve",
      "message": "Полная частота предусмотрена только для заданного резерва тревожных камер."
    },
    {
      "code": "MODEL_WEIGHT_ASSUMED",
      "field": "load.model_cost_overrides",
      "message": "Вес detector=1 — допущение команды."
    },
    {
      "code": "VENDOR_CAPACITY_NOT_APP_MEASUREMENT",
      "field": "load.reference_chip_fps",
      "message": "104,8 FPS — заявление вендора для опорной модели."
    },
    {
      "code": "PLATFORM_QUEUE_NOT_CHIP",
      "field": "load.platform_capacity_override_fps",
      "message": "12,4 FPS в сравнении — исторический общий лимит площадки, не паспорт чипа."
    },
    {
      "code": "SOURCE_PENDING_PRIMARY",
      "field": "benefits.injuries.rate_per_1000",
      "message": "Отраслевая подсказка 1,17 требует проверки первичного массива."
    },
    {
      "code": "SEVERE_COST_REQUIRED",
      "field": "benefits.severe_injury_cost_rub",
      "message": "Порог по тяжёлым случаям требует стоимости случая; основная смета от этого не становится неполной."
    }
  ],
  "missing": []
}
```

## К14.4. Полный запрос расширения

POST /api/calculator/scale?format=v2. Фактически установлены 4HP+1сервер; current8+added8, покупаются 8 физических камер. site описывает добавляемую область.

```json
{
  "contract_version": "2.0.0",
  "preset_id": null,
  "site": {
    "workshops": 2,
    "workers": 200,
    "shifts_per_day": 2,
    "working_days_year": 250,
    "operators": 2
  },
  "load": {
    "activity_share": 0.5,
    "activity_measurement_id": null,
    "target_fps": 12,
    "surge_fps": 5,
    "idle_check_s": 4,
    "peak_mode": "independent_p95",
    "priority_cameras_reserve": 1,
    "detector_stride": 1,
    "reference_chip_fps": 104.8,
    "capacity_derate": 0.5,
    "platform_capacity_override_fps": null,
    "model_cost_overrides": {},
    "cpu_basis": "inclusive",
    "cpu_ms_per_unit": 77,
    "decode_cores_per_camera": 0
  },
  "hardware": {
    "allowed_board_ids": [
      "HP",
      "HPD",
      "HPQ"
    ],
    "board_price_overrides": {},
    "server": {
      "slots": 4,
      "usable_cpu_cores": 16,
      "price_rub": 350000,
      "power_w": 250
    }
  },
  "costs": {
    "integration_fixed_rub": 300000,
    "integration_per_camera_rub": 0,
    "support_share_year": 0.15,
    "electricity_rub_kwh": 8,
    "operating_hours_year": 8760,
    "signal_zones_per_camera": 1,
    "signal_unit_rub": 25000,
    "speaker_per_workshop_rub": 40000,
    "new_camera_unit_rub": 30000,
    "new_camera_count": 8,
    "max_additional_camera_share": 0.2
  },
  "benefits": {
    "injuries": {
      "enabled": true,
      "annual_injured_workers": null,
      "rate_per_1000": 1.17,
      "cost_per_injured_worker_rub": 1000000,
      "cost_scope": "direct_only",
      "reduction": {
        "base": 0.2,
        "extended": 0.3,
        "max": 0.4
      }
    },
    "downtime": {
      "enabled": false,
      "events_year": null,
      "days_per_event": null,
      "day_cost_rub": null,
      "reduction": {
        "base": 0.2,
        "extended": 0.3,
        "max": 0.4
      }
    },
    "fines": {
      "enabled": false,
      "items": [
        {
          "id": "general_ohs",
          "title": "Общие требования охраны труда",
          "inspection_probability_year": 0.1,
          "amount_rub": 65000,
          "reduction": {
            "base": 0.2,
            "extended": 0.3,
            "max": 0.4
          }
        },
        {
          "id": "ppe",
          "title": "Обеспечение СИЗ",
          "inspection_probability_year": 0.1,
          "amount_rub": 140000,
          "reduction": {
            "base": 0.2,
            "extended": 0.3,
            "max": 0.4
          }
        }
      ]
    },
    "sfr_discount": {
      "enabled": false,
      "payroll_rub_year": null,
      "tariff_share": null,
      "additional_discount_share": null
    },
    "labor": {
      "monetize": false,
      "rows": [
        {
          "id": "ohs",
          "title": "Инженер охраны труда",
          "hours_saved_year": 0,
          "hour_cost_rub": null
        },
        {
          "id": "operator",
          "title": "Оператор",
          "hours_saved_year": 0,
          "hour_cost_rub": null
        }
      ]
    },
    "severe_injury_cost_rub": null
  },
  "current": {
    "source": "manual",
    "cameras": 8,
    "groups": [
      {
        "id": "standard",
        "share": 1,
        "model_ids": [
          "det-yolov8n@640-ap9999",
          "pose-yolov8n@640-ap9999"
        ]
      }
    ]
  },
  "added": {
    "source": "manual",
    "cameras": 8,
    "groups": [
      {
        "id": "standard",
        "share": 1,
        "model_ids": [
          "det-yolov8n@640-ap9999",
          "pose-yolov8n@640-ap9999"
        ]
      }
    ]
  },
  "installed": {
    "boards": [
      {
        "board_id": "HP",
        "count": 4
      }
    ],
    "servers": 1
  }
}
```

## К14.5. Расширение: проекция результата

Это проекция результата расширения: не полный HTTP-ответ и не сокращённая схема ResultV2. В живом ответе обязательны все поля К5, как в полном примере К14.3.

```json
{
  "mode": "scale",
  "status": "estimated",
  "cost_scope": "incremental",
  "load": {
    "cameras": 16,
    "active_p95": 11,
    "priority_cameras_effective": 1,
    "peak_units_s": 265.25,
    "surge_units_s": 174.0,
    "required_units_s": 265.25,
    "effective_chip_units_s": 52.4,
    "required_chips": 6,
    "required_cpu_cores": 20.42425,
    "naive_chips": 31,
    "basis": "independent_p95"
  },
  "hardware": {
    "selection": "priced_optimum",
    "before": {
      "boards": [
        {
          "board_id": "HP",
          "count": 4
        }
      ],
      "chips": 4,
      "servers": 1,
      "used_slots": 4,
      "power_w": 390.0
    },
    "purchase": {
      "boards": [
        {
          "board_id": "HP",
          "count": 2
        }
      ],
      "chips": 2,
      "servers": 1,
      "used_slots": 2,
      "power_w": 320.0
    },
    "after": {
      "boards": [
        {
          "board_id": "HP",
          "count": 6
        }
      ],
      "chips": 6,
      "servers": 2,
      "used_slots": 6,
      "power_w": 710.0
    },
    "board_capex_rub": 1000000.0,
    "server_capex_rub": 350000.0,
    "required_after_chips": 6,
    "spare_chips_after": 0,
    "note": "Эталонный пример использует HP: остальные цены неизвестны; новый глобальный solver здесь не имитируется.",
    "inventory_basis": "provided",
    "required_before_chips": 3
  },
  "tiers": [
    {
      "tier": "base",
      "title": "Базовый",
      "capex_rub": 1890000.0,
      "opex_rub_year": 305925.6,
      "gross_benefit_rub_year": 46800.0,
      "net_benefit_rub_year": -259125.6,
      "tco_3_year_rub": 2807776.8,
      "net_balance_3_year_rub": -2667376.8,
      "rub_per_camera_month": 9749.23,
      "camera_denominator": 8,
      "labor_hours_year": 0,
      "capex_lines": [
        {
          "id": "boards",
          "title": "Новые платы LinQ",
          "amount_rub": 1000000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.boards"
          ]
        },
        {
          "id": "servers",
          "title": "Новые серверы",
          "amount_rub": 350000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.servers"
          ]
        },
        {
          "id": "integration_fixed",
          "title": "Пусконаладка: фиксированная часть",
          "amount_rub": 300000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.integration_fixed"
          ]
        },
        {
          "id": "integration_cameras",
          "title": "Пусконаладка камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.integration_cameras"
          ]
        },
        {
          "id": "physical_cameras",
          "title": "Покупка физических камер",
          "amount_rub": 240000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.physical_cameras"
          ]
        }
      ],
      "opex_lines": [
        {
          "id": "support",
          "title": "Поддержка",
          "amount_rub": 283500.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.opex.support"
          ]
        },
        {
          "id": "electricity",
          "title": "Электроэнергия вычислительного оборудования",
          "amount_rub": 22425.6,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "cost.electricity_rub_year"
          ]
        }
      ],
      "benefit_lines": [
        {
          "id": "injuries",
          "title": "Предотвращённые прямые потери предприятия от травм",
          "amount_rub": 46800.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.benefit.injuries"
          ]
        },
        {
          "id": "downtime",
          "title": "Простой",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.base.benefit.downtime"
          ]
        },
        {
          "id": "fines",
          "title": "Штрафы",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.base.benefit.fines"
          ]
        },
        {
          "id": "sfr_discount",
          "title": "Дополнительная скидка СФР",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.base.benefit.sfr_discount"
          ]
        },
        {
          "id": "labor",
          "title": "Время работников в деньгах",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.base.benefit.labor"
          ]
        }
      ],
      "payback": {
        "status": "no_positive_effect",
        "months": null,
        "within_horizon": false,
        "reason": "Расчётная годовая выгода не превышает годовые расходы; измените фактические входы."
      },
      "severe_threshold": {
        "status": "needs_input",
        "expected_prevented_cases": null,
        "whole_prevented_cases": null,
        "uncovered_cost_rub": 2807776.8,
        "reason": "Задайте прямую стоимость тяжёлого случая для предприятия."
      },
      "board_price_threshold": {
        "status": "free_still_insufficient",
        "board_id": "HP",
        "boards_to_buy": 2,
        "max_unit_price_rub": null,
        "current_unit_price_rub": 500000.0,
        "reason": "Даже бесплатная плата не покрывает остальные расходы при этих входах; знание текущей цены платы для этого вывода не требуется."
      }
    },
    {
      "tier": "extended",
      "title": "Расширенный",
      "capex_rub": 2090000.0,
      "opex_rub_year": 335925.6,
      "gross_benefit_rub_year": 70200.0,
      "net_benefit_rub_year": -265725.6,
      "tco_3_year_rub": 3097776.8,
      "net_balance_3_year_rub": -2887176.8,
      "rub_per_camera_month": 10756.17,
      "camera_denominator": 8,
      "labor_hours_year": 0,
      "capex_lines": [
        {
          "id": "boards",
          "title": "Новые платы LinQ",
          "amount_rub": 1000000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.boards"
          ]
        },
        {
          "id": "servers",
          "title": "Новые серверы",
          "amount_rub": 350000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.servers"
          ]
        },
        {
          "id": "integration_fixed",
          "title": "Пусконаладка: фиксированная часть",
          "amount_rub": 300000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.integration_fixed"
          ]
        },
        {
          "id": "integration_cameras",
          "title": "Пусконаладка камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.integration_cameras"
          ]
        },
        {
          "id": "physical_cameras",
          "title": "Покупка физических камер",
          "amount_rub": 240000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.physical_cameras"
          ]
        },
        {
          "id": "signals",
          "title": "Световые и звуковые сигналы зон",
          "amount_rub": 200000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.signals"
          ]
        }
      ],
      "opex_lines": [
        {
          "id": "support",
          "title": "Поддержка",
          "amount_rub": 313500.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.opex.support"
          ]
        },
        {
          "id": "electricity",
          "title": "Электроэнергия вычислительного оборудования",
          "amount_rub": 22425.6,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "cost.electricity_rub_year"
          ]
        }
      ],
      "benefit_lines": [
        {
          "id": "injuries",
          "title": "Предотвращённые прямые потери предприятия от травм",
          "amount_rub": 70200.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.benefit.injuries"
          ]
        },
        {
          "id": "downtime",
          "title": "Простой",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.extended.benefit.downtime"
          ]
        },
        {
          "id": "fines",
          "title": "Штрафы",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.extended.benefit.fines"
          ]
        },
        {
          "id": "sfr_discount",
          "title": "Дополнительная скидка СФР",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.extended.benefit.sfr_discount"
          ]
        },
        {
          "id": "labor",
          "title": "Время работников в деньгах",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.extended.benefit.labor"
          ]
        }
      ],
      "payback": {
        "status": "no_positive_effect",
        "months": null,
        "within_horizon": false,
        "reason": "Расчётная годовая выгода не превышает годовые расходы; измените фактические входы."
      },
      "severe_threshold": {
        "status": "needs_input",
        "expected_prevented_cases": null,
        "whole_prevented_cases": null,
        "uncovered_cost_rub": 3097776.8,
        "reason": "Задайте прямую стоимость тяжёлого случая для предприятия."
      },
      "board_price_threshold": {
        "status": "free_still_insufficient",
        "board_id": "HP",
        "boards_to_buy": 2,
        "max_unit_price_rub": null,
        "current_unit_price_rub": 500000.0,
        "reason": "Даже бесплатная плата не покрывает остальные расходы при этих входах; знание текущей цены платы для этого вывода не требуется."
      }
    },
    {
      "tier": "max",
      "title": "Максимальный",
      "capex_rub": 2170000.0,
      "opex_rub_year": 347925.6,
      "gross_benefit_rub_year": 93600.0,
      "net_benefit_rub_year": -254325.6,
      "tco_3_year_rub": 3213776.8,
      "net_balance_3_year_rub": -2932976.8,
      "rub_per_camera_month": 11158.95,
      "camera_denominator": 8,
      "labor_hours_year": 0,
      "capex_lines": [
        {
          "id": "boards",
          "title": "Новые платы LinQ",
          "amount_rub": 1000000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.boards"
          ]
        },
        {
          "id": "servers",
          "title": "Новые серверы",
          "amount_rub": 350000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.servers"
          ]
        },
        {
          "id": "integration_fixed",
          "title": "Пусконаладка: фиксированная часть",
          "amount_rub": 300000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.integration_fixed"
          ]
        },
        {
          "id": "integration_cameras",
          "title": "Пусконаладка камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.integration_cameras"
          ]
        },
        {
          "id": "physical_cameras",
          "title": "Покупка физических камер",
          "amount_rub": 240000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.physical_cameras"
          ]
        },
        {
          "id": "signals",
          "title": "Световые и звуковые сигналы зон",
          "amount_rub": 200000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.signals"
          ]
        },
        {
          "id": "speakers",
          "title": "Громкоговорители в цехах",
          "amount_rub": 80000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.speakers"
          ]
        },
        {
          "id": "max_cameras",
          "title": "Дополнительное оснащение каналов камерами",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.max_cameras"
          ]
        }
      ],
      "opex_lines": [
        {
          "id": "support",
          "title": "Поддержка",
          "amount_rub": 325500.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.opex.support"
          ]
        },
        {
          "id": "electricity",
          "title": "Электроэнергия вычислительного оборудования",
          "amount_rub": 22425.6,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "cost.electricity_rub_year"
          ]
        }
      ],
      "benefit_lines": [
        {
          "id": "injuries",
          "title": "Предотвращённые прямые потери предприятия от травм",
          "amount_rub": 93600.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.benefit.injuries"
          ]
        },
        {
          "id": "downtime",
          "title": "Простой",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.max.benefit.downtime"
          ]
        },
        {
          "id": "fines",
          "title": "Штрафы",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.max.benefit.fines"
          ]
        },
        {
          "id": "sfr_discount",
          "title": "Дополнительная скидка СФР",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.max.benefit.sfr_discount"
          ]
        },
        {
          "id": "labor",
          "title": "Время работников в деньгах",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.max.benefit.labor"
          ]
        }
      ],
      "payback": {
        "status": "no_positive_effect",
        "months": null,
        "within_horizon": false,
        "reason": "Расчётная годовая выгода не превышает годовые расходы; измените фактические входы."
      },
      "severe_threshold": {
        "status": "needs_input",
        "expected_prevented_cases": null,
        "whole_prevented_cases": null,
        "uncovered_cost_rub": 3213776.8,
        "reason": "Задайте прямую стоимость тяжёлого случая для предприятия."
      },
      "board_price_threshold": {
        "status": "free_still_insufficient",
        "board_id": "HP",
        "boards_to_buy": 2,
        "max_unit_price_rub": null,
        "current_unit_price_rub": 500000.0,
        "reason": "Даже бесплатная плата не покрывает остальные расходы при этих входах; знание текущей цены платы для этого вывода не требуется."
      }
    }
  ]
}
```

## К14.6. Неполная смета при неизвестной цене HP

Возьмите полное тело К14.2, замените только hardware.allowed_board_ids на ["HP"] и hardware.board_price_overrides на {"HP":null}. Полный ответ имеет ту же схему К5 и обязательные поля, что полный ответ К14.3. Ниже проекция, не полный HTTP-ответ: технический результат и известные части сохранены, неизвестные деньги не превращены в ноль. CAPEX/TCO остаются неизвестны, но порог цены одной HP вычисляется независимо: остальные расходы и выгоды известны, поэтому для всех трёх уровней подтверждено free_still_insufficient.

```json
{
  "mode": "rollout",
  "status": "partial",
  "load": {
    "cameras": 8,
    "active_p95": 6,
    "priority_cameras_effective": 1,
    "peak_units_s": 144.5,
    "surge_units_s": 94.0,
    "required_units_s": 144.5,
    "effective_chip_units_s": 52.4,
    "required_chips": 3,
    "required_cpu_cores": 11.1265,
    "naive_chips": 16,
    "basis": "independent_p95"
  },
  "hardware": {
    "selection": "technical_only",
    "before": {
      "boards": [],
      "chips": 0,
      "servers": 0,
      "used_slots": 0,
      "power_w": 0.0
    },
    "purchase": {
      "boards": [
        {
          "board_id": "HP",
          "count": 3
        }
      ],
      "chips": 3,
      "servers": 1,
      "used_slots": 3,
      "power_w": 355.0
    },
    "after": {
      "boards": [
        {
          "board_id": "HP",
          "count": 3
        }
      ],
      "chips": 3,
      "servers": 1,
      "used_slots": 3,
      "power_w": 355.0
    },
    "board_capex_rub": null,
    "server_capex_rub": 350000.0,
    "required_after_chips": 3,
    "spare_chips_after": 0,
    "note": "Эталонный пример использует HP: остальные цены неизвестны; новый глобальный solver здесь не имитируется.",
    "inventory_basis": "none",
    "required_before_chips": 0
  },
  "tiers": [
    {
      "tier": "base",
      "title": "Базовый",
      "capex_rub": null,
      "opex_rub_year": null,
      "gross_benefit_rub_year": 46800.0,
      "net_benefit_rub_year": null,
      "tco_3_year_rub": null,
      "net_balance_3_year_rub": null,
      "rub_per_camera_month": null,
      "camera_denominator": 8,
      "labor_hours_year": 0,
      "capex_lines": [
        {
          "id": "boards",
          "title": "Новые платы LinQ",
          "amount_rub": null,
          "included": true,
          "status": "missing",
          "evidence_keys": [
            "tier.base.capex.boards"
          ]
        },
        {
          "id": "servers",
          "title": "Новые серверы",
          "amount_rub": 350000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.servers"
          ]
        },
        {
          "id": "integration_fixed",
          "title": "Пусконаладка: фиксированная часть",
          "amount_rub": 300000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.integration_fixed"
          ]
        },
        {
          "id": "integration_cameras",
          "title": "Пусконаладка камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.integration_cameras"
          ]
        },
        {
          "id": "physical_cameras",
          "title": "Покупка физических камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.capex.physical_cameras"
          ]
        }
      ],
      "opex_lines": [
        {
          "id": "support",
          "title": "Поддержка",
          "amount_rub": null,
          "included": true,
          "status": "missing",
          "evidence_keys": [
            "tier.base.opex.support"
          ]
        },
        {
          "id": "electricity",
          "title": "Электроэнергия вычислительного оборудования",
          "amount_rub": 24878.4,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "cost.electricity_rub_year"
          ]
        }
      ],
      "benefit_lines": [
        {
          "id": "injuries",
          "title": "Предотвращённые прямые потери предприятия от травм",
          "amount_rub": 46800.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.base.benefit.injuries"
          ]
        },
        {
          "id": "downtime",
          "title": "Простой",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.base.benefit.downtime"
          ]
        },
        {
          "id": "fines",
          "title": "Штрафы",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.base.benefit.fines"
          ]
        },
        {
          "id": "sfr_discount",
          "title": "Дополнительная скидка СФР",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.base.benefit.sfr_discount"
          ]
        },
        {
          "id": "labor",
          "title": "Время работников в деньгах",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.base.benefit.labor"
          ]
        }
      ],
      "payback": {
        "status": "insufficient_data",
        "months": null,
        "within_horizon": null,
        "reason": "Неизвестна цена покупаемой HP и зависящие от CAPEX расходы."
      },
      "severe_threshold": {
        "status": "needs_input",
        "expected_prevented_cases": null,
        "whole_prevented_cases": null,
        "uncovered_cost_rub": null,
        "reason": "Неизвестна полная стоимость проекта."
      },
      "board_price_threshold": {
        "status": "free_still_insufficient",
        "board_id": "HP",
        "boards_to_buy": 3,
        "max_unit_price_rub": null,
        "current_unit_price_rub": null,
        "reason": "Даже бесплатная плата не покрывает остальные расходы при этих входах; знание текущей цены платы для этого вывода не требуется."
      }
    },
    {
      "tier": "extended",
      "title": "Расширенный",
      "capex_rub": null,
      "opex_rub_year": null,
      "gross_benefit_rub_year": 70200.0,
      "net_benefit_rub_year": null,
      "tco_3_year_rub": null,
      "net_balance_3_year_rub": null,
      "rub_per_camera_month": null,
      "camera_denominator": 8,
      "labor_hours_year": 0,
      "capex_lines": [
        {
          "id": "boards",
          "title": "Новые платы LinQ",
          "amount_rub": null,
          "included": true,
          "status": "missing",
          "evidence_keys": [
            "tier.extended.capex.boards"
          ]
        },
        {
          "id": "servers",
          "title": "Новые серверы",
          "amount_rub": 350000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.servers"
          ]
        },
        {
          "id": "integration_fixed",
          "title": "Пусконаладка: фиксированная часть",
          "amount_rub": 300000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.integration_fixed"
          ]
        },
        {
          "id": "integration_cameras",
          "title": "Пусконаладка камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.integration_cameras"
          ]
        },
        {
          "id": "physical_cameras",
          "title": "Покупка физических камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.physical_cameras"
          ]
        },
        {
          "id": "signals",
          "title": "Световые и звуковые сигналы зон",
          "amount_rub": 200000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.capex.signals"
          ]
        }
      ],
      "opex_lines": [
        {
          "id": "support",
          "title": "Поддержка",
          "amount_rub": null,
          "included": true,
          "status": "missing",
          "evidence_keys": [
            "tier.extended.opex.support"
          ]
        },
        {
          "id": "electricity",
          "title": "Электроэнергия вычислительного оборудования",
          "amount_rub": 24878.4,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "cost.electricity_rub_year"
          ]
        }
      ],
      "benefit_lines": [
        {
          "id": "injuries",
          "title": "Предотвращённые прямые потери предприятия от травм",
          "amount_rub": 70200.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.extended.benefit.injuries"
          ]
        },
        {
          "id": "downtime",
          "title": "Простой",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.extended.benefit.downtime"
          ]
        },
        {
          "id": "fines",
          "title": "Штрафы",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.extended.benefit.fines"
          ]
        },
        {
          "id": "sfr_discount",
          "title": "Дополнительная скидка СФР",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.extended.benefit.sfr_discount"
          ]
        },
        {
          "id": "labor",
          "title": "Время работников в деньгах",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.extended.benefit.labor"
          ]
        }
      ],
      "payback": {
        "status": "insufficient_data",
        "months": null,
        "within_horizon": null,
        "reason": "Неизвестна цена покупаемой HP и зависящие от CAPEX расходы."
      },
      "severe_threshold": {
        "status": "needs_input",
        "expected_prevented_cases": null,
        "whole_prevented_cases": null,
        "uncovered_cost_rub": null,
        "reason": "Неизвестна полная стоимость проекта."
      },
      "board_price_threshold": {
        "status": "free_still_insufficient",
        "board_id": "HP",
        "boards_to_buy": 3,
        "max_unit_price_rub": null,
        "current_unit_price_rub": null,
        "reason": "Даже бесплатная плата не покрывает остальные расходы при этих входах; знание текущей цены платы для этого вывода не требуется."
      }
    },
    {
      "tier": "max",
      "title": "Максимальный",
      "capex_rub": null,
      "opex_rub_year": null,
      "gross_benefit_rub_year": 93600.0,
      "net_benefit_rub_year": null,
      "tco_3_year_rub": null,
      "net_balance_3_year_rub": null,
      "rub_per_camera_month": null,
      "camera_denominator": 8,
      "labor_hours_year": 0,
      "capex_lines": [
        {
          "id": "boards",
          "title": "Новые платы LinQ",
          "amount_rub": null,
          "included": true,
          "status": "missing",
          "evidence_keys": [
            "tier.max.capex.boards"
          ]
        },
        {
          "id": "servers",
          "title": "Новые серверы",
          "amount_rub": 350000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.servers"
          ]
        },
        {
          "id": "integration_fixed",
          "title": "Пусконаладка: фиксированная часть",
          "amount_rub": 300000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.integration_fixed"
          ]
        },
        {
          "id": "integration_cameras",
          "title": "Пусконаладка камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.integration_cameras"
          ]
        },
        {
          "id": "physical_cameras",
          "title": "Покупка физических камер",
          "amount_rub": 0.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.physical_cameras"
          ]
        },
        {
          "id": "signals",
          "title": "Световые и звуковые сигналы зон",
          "amount_rub": 200000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.signals"
          ]
        },
        {
          "id": "speakers",
          "title": "Громкоговорители в цехах",
          "amount_rub": 80000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.speakers"
          ]
        },
        {
          "id": "max_cameras",
          "title": "Дополнительное оснащение каналов камерами",
          "amount_rub": 60000.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.capex.max_cameras"
          ]
        }
      ],
      "opex_lines": [
        {
          "id": "support",
          "title": "Поддержка",
          "amount_rub": null,
          "included": true,
          "status": "missing",
          "evidence_keys": [
            "tier.max.opex.support"
          ]
        },
        {
          "id": "electricity",
          "title": "Электроэнергия вычислительного оборудования",
          "amount_rub": 24878.4,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "cost.electricity_rub_year"
          ]
        }
      ],
      "benefit_lines": [
        {
          "id": "injuries",
          "title": "Предотвращённые прямые потери предприятия от травм",
          "amount_rub": 93600.0,
          "included": true,
          "status": "derived",
          "evidence_keys": [
            "tier.max.benefit.injuries"
          ]
        },
        {
          "id": "downtime",
          "title": "Простой",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.max.benefit.downtime"
          ]
        },
        {
          "id": "fines",
          "title": "Штрафы",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.max.benefit.fines"
          ]
        },
        {
          "id": "sfr_discount",
          "title": "Дополнительная скидка СФР",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.max.benefit.sfr_discount"
          ]
        },
        {
          "id": "labor",
          "title": "Время работников в деньгах",
          "amount_rub": 0,
          "included": false,
          "status": "not_applicable",
          "evidence_keys": [
            "tier.max.benefit.labor"
          ]
        }
      ],
      "payback": {
        "status": "insufficient_data",
        "months": null,
        "within_horizon": null,
        "reason": "Неизвестна цена покупаемой HP и зависящие от CAPEX расходы."
      },
      "severe_threshold": {
        "status": "needs_input",
        "expected_prevented_cases": null,
        "whole_prevented_cases": null,
        "uncovered_cost_rub": null,
        "reason": "Неизвестна полная стоимость проекта."
      },
      "board_price_threshold": {
        "status": "free_still_insufficient",
        "board_id": "HP",
        "boards_to_buy": 3,
        "max_unit_price_rub": null,
        "current_unit_price_rub": null,
        "reason": "Даже бесплатная плата не покрывает остальные расходы при этих входах; знание текущей цены платы для этого вывода не требуется."
      }
    }
  ],
  "missing": [
    {
      "code": "BOARD_PRICE_UNKNOWN",
      "field": "hardware.board_price_overrides.HP",
      "message": "Цена покупаемой HP неизвестна; техническая комплектация рассчитана, CAPEX/TCO недоступны."
    }
  ]
}
```

## К14.7. Ошибки

422: если в полном запросе заменить load.activity_share на 1.2. Неизвестная цена из К14.6 вместо этого даёт успешный 200 partial.

```json
{
  "code": "validation",
  "message": "Неверное значение: load.activity_share",
  "details": {
    "field": "load.activity_share",
    "reason": "OUT_OF_RANGE"
  }
}
```

### Ошибка выбора формата

422: неверный format или несовместимая с выбранным форматом схема. Это обычный существующий ApiError.

```json
{
  "code": "validation",
  "message": "Неверный формат запроса",
  "details": {
    "field": "format",
    "reason": "SCHEMA_MISMATCH"
  }
}
```

### Выключенный PDF

501 при features.pdf_available=false; дополнительные маршруты не изобретаются.

```json
{
  "code": "not_implemented",
  "message": "Экспорт PDF отключён",
  "details": {
    "field": "features.pdf_available",
    "reason": "PDF_DISABLED"
  }
}
```

### Галерея состояний окупаемости

Это самостоятельные фрагменты PaybackResult и PriceThreshold, не полные HTTP-ответы. Контрольный C=1000000, поддержка r=.1 и прочие расходы F=40000 в год: при B=500000 срок 33,333333 месяца; при B=240000 срок 120 месяцев. Для отдельного ценового порога C_other=500000,q=1,B=500000,r=.1,F=40000: текущая цена HP неизвестна, допустимый максимум 561538,46 ₽. Полный ResultV2 во всех случаях соответствует К5.

```json
{
  "within_horizon": {
    "status": "within_horizon",
    "months": 33.333333,
    "within_horizon": true,
    "reason": "Математический пример: C=1000000, r=.1, F=40000, B=500000; net=360000 в год."
  },
  "after_horizon": {
    "status": "after_horizon",
    "months": 120,
    "within_horizon": false,
    "reason": "Тот же C/r/F, B=240000: net=100000 в год, срок 120 месяцев."
  },
  "unknown_current_price": {
    "status": "at_or_below",
    "board_id": "HP",
    "boards_to_buy": 1,
    "max_unit_price_rub": 561538.46,
    "current_unit_price_rub": null,
    "reason": "Независимый вектор: C_other=500000, q=1, B=500000, r=.1, F=40000. Текущая цена HP неизвестна, но цена для окупаемости за 3 года не должна превышать 561538,46 ₽."
  }
}
```

<!-- calculator-contract:end -->
