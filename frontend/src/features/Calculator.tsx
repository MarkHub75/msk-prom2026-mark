import { useEffect, useMemo, useState } from "react";
import { api, apiError, type ApiFailure } from "../api/client";
import type { CalcAssumption, RolloutIn, RolloutResult, ScaleIn, ScaleResult, TierResult } from "../api/types";
import { useApi } from "../api/useApi";
import { Badge, Button, ErrorNotice, Field, Icon, isPending, Kpi, Loading, PageHeading, Panel, PendingNotice, Segmented, TextInput } from "../components/ui";
import { EXAMPLE_ASSUMPTIONS, EXAMPLE_ROLLOUT, EXAMPLE_SCALE, exampleRollout, exampleScale } from "./calculatorExample";
import { BreakEvenPanel, industryHint, MarketPanel } from "./calculatorEconomics";
import { useRole } from "../roles";
import "../styles/v5.css";

// tech.md 8.25: every figure is a signed assumption (CalcAssumption) or a measurement of the app;
// the screen only edits inputs and overrides, all arithmetic is the server's.
type Mode = "rollout" | "scale";
type RolloutField = Exclude<keyof RolloutIn, "overrides">;
type ScaleField = Exclude<keyof ScaleIn, "overrides">;

const PLANT: { key: RolloutField; label: string; min: number }[] = [
  { key: "workshops", label: "Цехов", min: 1 },
  { key: "cameras", label: "Камер", min: 1 },
  { key: "shifts_per_day", label: "Смен в сутки", min: 0 },
  { key: "workers", label: "Работников", min: 0 },
  { key: "operators", label: "Операторов в смену", min: 0 },
  { key: "incidents_per_year", label: "Инцидентов в год", min: 0 },
];
const COST: { key: RolloutField; label: string }[] = [
  { key: "downtime_cost_rub", label: "Простой" },
  { key: "fine_cost_rub", label: "Штраф" },
  { key: "treatment_cost_rub", label: "Лечение" },
  { key: "lawsuit_cost_rub", label: "Суды" },
];
const SCALE: { key: ScaleField; label: string; min: number }[] = [
  { key: "cameras_now", label: "Камер подключено сейчас", min: 1 },
  { key: "new_cameras", label: "Добавить камер", min: 0 },
];

const rubFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });
const numFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 2 });
const yearsFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 1 });
export const rub = (value: number) => `${rubFmt.format(value)} ₽`;
export function months(value: number | null) {
  if (value === null) return null;
  if (value < 1) return "меньше месяца";
  const text = `${numFmt.format(Math.round(value * 10) / 10)} мес.`;
  return value >= 24 ? `${text} · ${yearsFmt.format(value / 12)} г.` : text;
}

type Draft = Record<string, string>;
const toDraft = (input: object) => Object.fromEntries(Object.entries(input).filter(([k]) => k !== "overrides").map(([k, v]) => [k, String(v)]));
function parse(draft: Draft, fields: { key: string; min: number }[]) {
  const values: Record<string, number> = {}; const errors: Record<string, string> = {};
  for (const { key, min } of fields) {
    const raw = (draft[key] ?? "").replace(/\s/g, "").replace(",", ".");
    const n = Number(raw);
    if (raw === "" || !Number.isFinite(n)) errors[key] = "Нужно число";
    else if (n < min) errors[key] = min ? `Не меньше ${min}` : "Не меньше 0";
    else values[key] = n;
  }
  return { values, errors };
}

/** Debounced POST of the current inputs; the last answer stays on screen (dimmed) while the next one runs. */
function useCalc<T>(post: () => Promise<{ data?: T; error?: unknown; response: Response }>, key: string, ready: boolean) {
  const [state, setState] = useState<{ data?: T; error?: ApiFailure; busy: boolean }>({ busy: false });
  useEffect(() => {
    if (!ready) return;
    let alive = true;
    setState(s => ({ ...s, busy: true }));
    const timer = setTimeout(() => {
      post().then(r => {
        if (!alive) return;
        if (r.error !== undefined || !r.data) setState(s => ({ data: s.data, error: { ...apiError(r.error), status: r.response.status }, busy: false }));
        else setState({ data: r.data, busy: false });
      }).catch((e: unknown) => { if (alive) setState(s => ({ data: s.data, error: apiError(e), busy: false })); });
    }, 300);
    return () => { alive = false; clearTimeout(timer); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, ready]);
  return state;
}

function NumberField({ label, unit, value, error, hint, onChange }: { label: string; unit?: string; value: string; error?: string; hint?: string; onChange: (v: string) => void }) {
  return <Field label={label} error={error} hint={hint}>
    <span className="v5-num-input"><TextInput inputMode="decimal" value={value} onChange={e => onChange(e.target.value)} aria-invalid={Boolean(error)} aria-label={label} />{unit && <small>{unit}</small>}</span>
  </Field>;
}

function Items({ items }: { items: { label: string; value: string }[] }) {
  if (!items.length) return null;
  return <dl className="v5-items">{items.map((item, i) => <div key={`${item.label}-${i}`}><dt>{item.label}</dt><dd>{item.value}</dd></div>)}</dl>;
}

const TIER_NOTE: Record<TierResult["tier"], string> = {
  base: "существующие камеры, ускорители и сервер",
  extended: "плюс свет и звук у опасных зон",
  max: "плюс громкоговорители в цехах и новые камеры",
};

function Tier({ tier, best }: { tier: TierResult; best: boolean }) {
  const payback = months(tier.payback_months);
  const net = tier.savings_rub_year - tier.opex_rub_year;
  return <article className={`v5-tier${best ? " is-best" : ""}`} data-testid={`tier-${tier.tier}`}>
    <header><h3>{tier.title}</h3><small>{TIER_NOTE[tier.tier]}</small>{best && <Badge tone="accent">быстрее окупается</Badge>}</header>
    <div className="v5-tier-capex"><span>Вложения</span><b className="mono">{rub(tier.capex_rub)}</b></div>
    <div className={`v5-tier-payback${payback ? "" : " is-none"}`}>
      <span>Окупаемость</span>
      {payback ? <b>{payback}</b> : <b>Не окупается при этих допущениях</b>}
    </div>
    <dl className="v5-tier-facts">
      <div><dt>Экономия в год</dt><dd className="mono">{rub(tier.savings_rub_year)}</dd></div>
      <div><dt>Поддержка в год</dt><dd className="mono">{rub(tier.opex_rub_year)}</dd></div>
      <div><dt>Чистый эффект в год</dt><dd className={`mono${net < 0 ? " is-neg" : ""}`}>{net < 0 ? "−" : ""}{rub(Math.abs(net))}</dd></div>
      <div><dt>Ускорители · серверы</dt><dd className="mono">{tier.accelerators} · {tier.servers}</dd></div>
    </dl>
    <details className="v5-tier-items"><summary>Из чего сложилась сумма</summary><Items items={tier.items} /></details>
  </article>;
}

interface Plant { incidents?: number; workers?: number }

function RolloutView({ result, plant }: { result: RolloutResult; plant: Plant }) {
  const paying = result.tiers.filter(t => t.payback_months !== null);
  const best = paying.length ? paying.reduce((a, b) => (b.payback_months! < a.payback_months! ? b : a)).tier : undefined;
  return <>
    <div className="v5-kpis">
      <Kpi label="Цена одного инцидента" value={rubFmt.format(result.incident_cost_rub)} unit="₽" hint="простой + штраф + лечение + суды" />
      <Kpi label="Инцидентов на 1000 работников" value={result.incidents_per_1000_workers === null ? "—" : numFmt.format(result.incidents_per_1000_workers)} hint={result.incidents_per_1000_workers === null ? "работников 0" : "в год"} />
      <Kpi label="Событий на оператора за смену" value={result.events_per_operator_shift === null ? "—" : numFmt.format(result.events_per_operator_shift)} hint={result.events_per_operator_shift === null ? "нужны события эфира сервера и хотя бы один оператор" : "по событиям эфира за период статистики"} />
    </div>
    <div className="v5-tiers">{result.tiers.map(t => <Tier key={t.tier} tier={t} best={t.tier === best && paying.length > 1} />)}</div>
    <BreakEvenPanel tiers={result.tiers} assumptions={result.assumptions} incidents={plant.incidents} workers={plant.workers} cost={result.incident_cost_rub} />
  </>;
}

function ScaleView({ result }: { result: ScaleResult }) {
  const added = result.accelerators_total - result.accelerators_now;
  return <>
    <div className="v5-kpis">
      <Kpi label="Камер после расширения" value={result.cameras_total} />
      <Kpi label="Ускорителей LinQ" value={<>{result.accelerators_now}<span className="v5-arrow">→</span>{result.accelerators_total}</>} hint={added > 0 ? `докупить ${added}` : "хватает текущих"} />
      <Kpi label="Серверов всего" value={result.servers_total} />
      <Kpi label="Вложения в расширение" value={rubFmt.format(result.capex_rub)} unit="₽" />
    </div>
    <div className="v5-scale-basis">
      <div><span>Пропускная способность ускорителя</span><b className="mono">{numFmt.format(result.capacity_fps)} кадр/с</b><small>{result.capacity_source}</small></div>
      <div><span>Частота анализа на камеру</span><b className="mono">{numFmt.format(result.analysis_fps)} кадр/с</b><small>pipeline.target_analysis_fps</small></div>
    </div>
    {result.items.length > 0 && <Panel title="Из чего сложилась сумма"><Items items={result.items} /></Panel>}
  </>;
}

function Assumptions({ list, overrides, onChange }: { list: CalcAssumption[]; overrides: Record<string, string>; onChange: (key: string, value: string | null) => void }) {
  return <table className="ds-table v5-assume" data-testid="assumptions">
    <thead><tr><th>Допущение</th><th className="num">Значение</th><th>Источник</th></tr></thead>
    <tbody>{list.map(a => {
      const draft = overrides[a.key];
      const changed = draft !== undefined;
      return <tr key={a.key} className={changed ? "is-changed" : undefined}>
        <td><b>{a.title}</b><small className="mono">{a.key}</small><small className="v5-source-inline">{changed ? "своё значение" : a.source}</small></td>
        <td className="num">{a.editable
          ? <span className="v5-num-input v5-assume-input"><TextInput inputMode="decimal" aria-label={a.title} value={draft ?? String(a.value)} onChange={e => onChange(a.key, e.target.value)} /><small>{a.unit}</small>{changed && <button type="button" className="v5-reset" onClick={() => onChange(a.key, null)} aria-label={`Вернуть «${a.title}»`} title="Вернуть исходное"><Icon name="refresh" size={13} /></button>}</span>
          : <span className="mono">{numFmt.format(a.value)} <small>{a.unit}</small></span>}</td>
        <td className="v5-source">{changed ? <Badge tone="accent">своё значение</Badge> : a.source}</td>
      </tr>;
    })}</tbody>
  </table>;
}

const PENDING_CALC = "Посчитает окупаемость внедрения и цену расширения на ваших цифрах; у каждого допущения — подписанный источник.";

/** 501: what the calculator will answer, counted here on the same assumptions and the demo plant, clearly marked as an example. */
function Example({ mode }: { mode: Mode }) {
  const inputs = mode === "rollout"
    ? [...PLANT, ...COST].map(f => ({ label: f.label, value: COST.some(c => c.key === f.key) ? rub(EXAMPLE_ROLLOUT[f.key]) : String(EXAMPLE_ROLLOUT[f.key]) }))
    : SCALE.map(f => ({ label: f.label, value: String(EXAMPLE_SCALE[f.key]) }));
  return <>
    <PendingNotice text={PENDING_CALC} />
    <div className="v5-calc-grid" data-testid="calc-example">
      <Panel title={mode === "rollout" ? "Пример завода" : "Пример расширения"}>
        <Items items={inputs} />
        {mode === "rollout" && <p className="v5-hint">{industryHint(EXAMPLE_ROLLOUT.workers)}. В примере 4 инцидента в год: это выше среднего, замените своими.</p>}
        <p className="v5-hint"><Icon name="info" size={14} />Когда сервер подключится, здесь будут поля для ваших цифр.</p>
      </Panel>
      <section className="v5-calc-result" aria-label="Пример расчёта">
        <div className="v5-example-tag"><Badge tone="grey" icon="info">пример, сервер ещё не подключён</Badge><small>те же формулы и допущения, что у сервера; {mode === "rollout" ? "события на оператора считаются только по живым данным" : "пропускная способность — из допущения, а не из замеров приложения"}</small></div>
        <div>{mode === "rollout" ? <RolloutView result={exampleRollout()} plant={{ incidents: EXAMPLE_ROLLOUT.incidents_per_year, workers: EXAMPLE_ROLLOUT.workers }} /> : <ScaleView result={exampleScale()} />}</div>
      </section>
    </div>
    <Panel title="Допущения примера" flush><Assumptions list={EXAMPLE_ASSUMPTIONS} overrides={{}} onChange={() => undefined} /></Panel>
    <MarketPanel cameras={mode === "rollout" ? EXAMPLE_ROLLOUT.cameras : EXAMPLE_SCALE.cameras_now + EXAMPLE_SCALE.new_cameras} />
  </>;
}

export function CalculatorPage() {
  const [role] = useRole();
  const canRollout = role === "management";
  const [mode, setMode] = useState<Mode>(canRollout ? "rollout" : "scale");
  const shown: Mode = canRollout ? mode : "scale";
  const defaults = useApi(() => api.GET("/api/calculator/defaults"), []);
  const [rollout, setRollout] = useState<Draft>();
  const [scale, setScale] = useState<Draft>();
  const [overrides, setOverrides] = useState<Record<string, string>>({});
  const base = defaults.data;
  useEffect(() => { if (base) { setRollout(r => r ?? toDraft(base.rollout)); setScale(s => s ?? toDraft(base.scale)); } }, [base]);

  const r = useMemo(() => parse(rollout ?? {}, [...PLANT, ...COST.map(c => ({ key: c.key, min: 0 }))]), [rollout]);
  const s = useMemo(() => parse(scale ?? {}, SCALE), [scale]);
  const o = useMemo(() => {
    const values: Record<string, number> = {}; const errors: Record<string, string> = {};
    for (const [k, v] of Object.entries(overrides)) { const n = Number(v.replace(/\s/g, "").replace(",", ".")); if (v.trim() === "" || !Number.isFinite(n) || n < 0) errors[k] = "Нужно число не меньше 0"; else values[k] = n; }
    return { values, errors };
  }, [overrides]);
  const okR = Boolean(rollout) && !Object.keys(r.errors).length && !Object.keys(o.errors).length;
  const okS = Boolean(scale) && !Object.keys(s.errors).length && !Object.keys(o.errors).length;
  const rolloutBody = { ...(r.values as Omit<RolloutIn, "overrides">), overrides: o.values };
  const scaleBody = { ...(s.values as Omit<ScaleIn, "overrides">), overrides: o.values };
  const rolloutCalc = useCalc(() => api.POST("/api/calculator/rollout", { body: rolloutBody }), JSON.stringify(rolloutBody), okR && shown === "rollout");
  const scaleCalc = useCalc(() => api.POST("/api/calculator/scale", { body: scaleBody }), JSON.stringify(scaleBody), okS && shown === "scale");
  const calc = shown === "rollout" ? rolloutCalc : scaleCalc;

  const heading = <PageHeading title="Калькулятор окупаемости" meta={<span>Все цены и доли — подписанные допущения команды: замените своими. Расчёт не сохраняется.</span>}>
    {canRollout && <Segmented label="Режим" value={shown} onChange={setMode} options={[{ id: "rollout", label: "Внедрение" }, { id: "scale", label: "Масштабирование" }]} />}
  </PageHeading>;
  if (isPending(defaults.error) || isPending(calc.error)) return <div className="v5-page v5-calc" data-testid="calculator">{heading}<Example mode={shown} /></div>;
  if (defaults.error) return <div className="v5-page">{heading}<ErrorNotice error={defaults.error} retry={defaults.reload} /></div>;
  if (!base || !rollout || !scale) return <div className="v5-page">{heading}<Loading text="Получаем допущения калькулятора" /></div>;

  const changed = Object.keys(overrides).length;
  const setR = (key: string) => (v: string) => setRollout(d => ({ ...d, [key]: v }));
  const setS = (key: string) => (v: string) => setScale(d => ({ ...d, [key]: v }));
  const setOverride = (key: string, value: string | null) => setOverrides(all => { const next = { ...all }; if (value === null) delete next[key]; else next[key] = value; return next; });
  const reset = () => { setRollout(toDraft(base.rollout)); setScale(toDraft(base.scale)); setOverrides({}); };
  const result = calc.data;

  return <div className="v5-page v5-calc" data-testid="calculator">
    {heading}
    <div className="v5-calc-grid">
      <Panel title={shown === "rollout" ? "Ваш завод" : "Камеры"} tools={<Button size="sm" variant="ghost" icon="refresh" onClick={reset}>Пример для демо</Button>}>
        <form className="v5-form" onSubmit={e => e.preventDefault()}>
          {shown === "rollout" ? <>
            <div className="v5-form-grid">{PLANT.map(f => <NumberField key={f.key} label={f.label} value={rollout[f.key] ?? ""} error={r.errors[f.key]} hint={f.key === "incidents_per_year" ? industryHint(r.values.workers) : undefined} onChange={setR(f.key)} />)}</div>
            <h3 className="v5-form-h">Цена одного инцидента</h3>
            <div className="v5-form-grid">{COST.map(f => <NumberField key={f.key} label={f.label} unit="₽" value={rollout[f.key] ?? ""} error={r.errors[f.key]} onChange={setR(f.key)} />)}</div>
          </> : <div className="v5-form-grid">{SCALE.map(f => <NumberField key={f.key} label={f.label} value={scale[f.key] ?? ""} error={s.errors[f.key]} onChange={setS(f.key)} />)}</div>}
          <p className="v5-hint"><Icon name="info" size={14} />Пример завода: «пример для демо, замените своими». Пересчёт идёт сразу при вводе.</p>
        </form>
      </Panel>
      <section className="v5-calc-result" aria-label="Результат расчёта" aria-busy={calc.busy}>
        {calc.error && <ErrorNotice error={calc.error} compact />}
        {result ? <div className={calc.busy ? "is-stale" : undefined}>{shown === "rollout" ? <RolloutView result={result as RolloutResult} plant={{ incidents: r.values.incidents_per_year, workers: r.values.workers }} /> : <ScaleView result={result as ScaleResult} />}</div>
          : (shown === "rollout" ? okR : okS) ? !calc.error && <Loading text="Считаем" /> : <p className="v5-hint is-error" role="alert">Исправьте отмеченные поля: расчёт ждёт чисел.</p>}
      </section>
    </div>
    <div className="v5-calc-grid v5-calc-grid-even">
      <Panel title="Допущения" tools={changed ? <Badge tone="accent">изменено {changed}</Badge> : undefined} flush>
        <Assumptions list={base.assumptions} overrides={overrides} onChange={setOverride} />
        {Object.keys(o.errors).length > 0 && <p className="v5-hint is-error" role="alert">В допущениях есть не число или отрицательное значение: расчёт ждёт исправления.</p>}
      </Panel>
      <div className="v5-stack">
      <Panel title="Замеры приложения" flush>
        {base.measured.length ? <table className="ds-table v5-assume" data-testid="measured">
          <thead><tr><th>Замер</th><th className="num">Значение</th><th>Источник</th></tr></thead>
          <tbody>{base.measured.map(m => <tr key={m.key}><td><b>{m.title}</b><small className="v5-source-inline">{m.source}</small></td><td className="num"><span className="mono">{numFmt.format(m.value)} <small>{m.unit}</small></span></td><td className="v5-source">{m.source}</td></tr>)}</tbody>
        </table> : <p className="v5-hint">Замеров пока нет: обработайте видео на LinQ, и здесь появится пропускная способность и RTT.</p>}
      </Panel>
      <MarketPanel cameras={shown === "rollout" ? r.values.cameras : (s.values.cameras_now ?? 0) + (s.values.new_cameras ?? 0)} />
      </div>
    </div>
  </div>;
}
