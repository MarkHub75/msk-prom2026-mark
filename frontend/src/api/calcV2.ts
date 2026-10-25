// Calculator v2 types, copied from the TypeScript blocks of docs/CALCULATOR_CONTRACT_V2.md 2.0.0 (К4 requests,
// К5 results, defaults and states). Local until OpenAPI 1.2.0 arrives with the backend; schema.d.ts is not touched.
// Keep in sync with the contract text: names and nullability are the contract, not a frontend choice.

export type Tier = "base" | "extended" | "max";
export type Mode = "rollout" | "scale";
export type TierShares = { base: number; extended: number; max: number };

export interface SiteInput {
  workshops: number;
  workers: number;
  shifts_per_day: number;
  working_days_year: number;
  operators: number;
}
// rollout: весь проект; scale: ДОБАВЛЯЕМАЯ область, не весь завод.

export interface ManualGroup {
  id: string;
  share: number;
  model_ids: string[];
}
export type CameraProfile =
  | { source: "manual"; cameras: number; groups: ManualGroup[] }
  | { source: "system"; camera_ids: number[] | null; include_seed: boolean };
// manual: сумма share=1 (допуск 1e-9); доли сервер переводит в целые количества.
// system: null выбирает все неудалённые камеры, по умолчанию include_seed=false.
// Нет enabled у Camera — не придумывать такой фильтр.

export interface LoadInput {
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

export interface ServerInput {
  slots: number;
  usable_cpu_cores: number;
  price_rub: number | null;
  power_w: number | null;
}
export interface HardwareInput {
  allowed_board_ids: string[];
  board_price_overrides: Record<string, number | null>;
  server: ServerInput;
}
// Отсутствующий key в price_overrides: каталог; явный null: цена неизвестна.

export interface InstalledInventory {
  boards: { board_id: string; count: number }[];
  servers: number;
}
// Одинаковый серверный профиль из hardware.server для существующих и новых серверов.
// Смешанные серверы разного типа в этой версии не моделируются.

export interface CostInput {
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
export interface InjuryBenefit {
  enabled: boolean;
  annual_injured_workers: number | null;
  rate_per_1000: number | null;
  cost_per_injured_worker_rub: number | null;
  cost_scope: "direct_only" | "all_in";
  reduction: TierShares;
}
export interface DowntimeBenefit {
  enabled: boolean;
  events_year: number | null;
  days_per_event: number | null;
  day_cost_rub: number | null;
  reduction: TierShares;
}
export interface FineItem {
  id: string;
  title: string;
  inspection_probability_year: number;
  amount_rub: number | null;
  reduction: TierShares;
}
export interface BenefitInput {
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

export interface CommonRequestV2 {
  contract_version: "2.0.0";
  preset_id: string | null;
  site: SiteInput;
  load: LoadInput;
  hardware: HardwareInput;
  costs: CostInput;
  benefits: BenefitInput;
}
export interface RolloutRequestV2 extends CommonRequestV2 {
  cameras: CameraProfile;
}
export interface ScaleRequestV2 extends CommonRequestV2 {
  current: CameraProfile;
  added: CameraProfile;
  installed: InstalledInventory | null;
}
export type ExportRequestV2 =
  | { mode: "rollout"; input: RolloutRequestV2 }
  | { mode: "scale"; input: ScaleRequestV2 };

export type NumberStatus = "known" | "assumed" | "derived" | "missing" | "not_applicable";
export type ResultStatus = "ready" | "estimated" | "partial" | "empty";
export type SourceKind = "argus_measurement" | "vendor_claim" | "official" | "team_assumption" | "user_input";
// user_input: введённые заводом цены/параметры, без выдачи за измерение Argus.
export type Verification = "verified_primary" | "cached_primary" | "pending_primary" | "not_applicable";

export interface SourceRecord {
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
export interface NumericEvidence {
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
export interface Notice {
  code: string;
  field: string | null;
  message: string;
}
export interface ResolvedGroup {
  id: string;
  cameras: number;
  camera_ids: number[];
  model_ids: string[];
}
export interface ResolvedProfile {
  cameras: number;
  groups: ResolvedGroup[];
}
export interface ModelLoad {
  id: string;
  title: string;
  kind: "detector" | "pose" | "extra";
  work_units: number | null;
  execution_status: "verified_linq" | "local_only" | "unverified" | "missing";
  source_ids: string[];
}
export interface BoardOffer {
  id: string;
  title: string;
  chips: number;
  slots: number;
  power_w: number | null;
  price_rub: number | null;
  source_ids: string[];
}
export interface TrackerFeature {
  available: boolean;
  max_stride: 1 | 2;
  report_ref: string | null;
}
export interface OfflineEconomy {
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
export interface FeaturesV2 {
  tracker: TrackerFeature;
  pdf_available: boolean;
  offline_economy: OfflineEconomy | null;
}
export interface Measurement {
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
export interface MarketReference {
  id: string;
  title: string;
  billing: "monthly_per_camera" | "one_off_per_camera" | "project";
  amount_rub: number | null;
  scope: string;
  source_ids: string[];
}
export interface PresetV2 {
  id: "workshop" | "shop" | "plant";
  title: string;
  area_m2: number | null;
  machines: number | null;
  note: string;
  rollout: RolloutRequestV2;
}
export interface FieldLimit {
  field: string;
  min: number | null;
  max: number | null;
  integer: boolean;
}
export interface DefaultsV2 {
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

export interface LoadResult {
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
export interface EquipmentState {
  boards: { board_id: string; count: number }[];
  chips: number;
  servers: number;
  used_slots: number;
  power_w: number | null;
}
export interface HardwareResult {
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
export interface MoneyLine {
  id: string;
  title: string;
  amount_rub: number | null;
  included: boolean;
  status: NumberStatus;
  evidence_keys: string[];
}
export interface PaybackResult {
  status: "within_horizon" | "after_horizon" | "no_positive_effect"
    | "no_initial_investment" | "insufficient_data" | "not_applicable";
  months: number | null;
  within_horizon: boolean | null;
  reason: string;
}
export interface SevereThreshold {
  status: "required" | "already_covered" | "needs_input" | "not_applicable";
  expected_prevented_cases: number | null;
  whole_prevented_cases: number | null;
  uncovered_cost_rub: number | null;
  reason: string;
}
export interface PriceThreshold {
  status: "at_or_below" | "already_within" | "free_still_insufficient"
    | "not_applicable" | "insufficient_data";
  board_id: string | null;
  boards_to_buy: number;
  max_unit_price_rub: number | null;
  current_unit_price_rub: number | null;
  reason: string;
}
export interface TierResultV2 {
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
export interface StepV2 {
  id: "naive" | "dedicated_capacity" | "scenario_models" | "activity_pool" | "tracker";
  title: string;
  available: boolean;
  chips: number | null;
  servers: number | null;
  equipment_capex_rub: number | null;
  reason: string;
}
export interface CurvePoint {
  cameras: number;
  chips: number | null;
  servers: number | null;
  tco_3_year_rub: number | null;
  rub_per_camera_month: number | null;
}
export interface ResultV2 {
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
export interface ApiErrorExisting {
  code: string;
  message: string;
  details: Record<string, string | number | null>;
}
