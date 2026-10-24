import { useMemo, useState, type ReactNode } from "react";
import { useLevelTitle } from "../components/ops/levels";
import { Link } from "react-router-dom";
import {
  AlertTriangle, ArrowDownToLine, Ban, CircleCheck, CircleDashed, CircleHelp, Construction, Fence, Flame, Footprints,
  HardHat, Anchor, Package, PersonStanding, RefreshCw, SlidersHorizontal, Smartphone, Square, Truck, Undo2, X,
  type LucideIcon,
} from "lucide-react";
import { api, apiError, type ApiFailure } from "../api/client";
import type { Schemas, Sector } from "../api/types";
import { useApi } from "../api/useApi";
import { useMeta } from "../components/AppShell";
import { Empty, ErrorNotice, Loading, PageHeading } from "../components/ui";

type CameraRule = Schemas["CameraRule"];
type ScenarioMeta = Schemas["ScenarioMeta"];
type Camera = Schemas["Camera"];
type Level = ScenarioMeta["default_level"];
type ScenarioStatus = ScenarioMeta["status"];

// /ohs/rules (tech.md 8.14): cameras grouped by sector × scenarios from the backend,
// a switch per cell, bulk on/off by row, sector and column, the scenario inspector.
const SW = 1.75;
export const SCENARIO_ICON: Record<string, LucideIcon> = {
  run: Footprints, truck: Truck, phone: Smartphone, fall: PersonStanding, fence: Fence,
  conveyor: ArrowDownToLine, fire: Flame, harness: HardHat, crane: Anchor, box: Package,
};
export const STATUS_LABEL: Record<ScenarioStatus, string> = {
  active: "Работает", model_missing: "Модель не подключена", skeleton: "Сценарий уточняется",
};
const STATUS_ICON: Record<ScenarioStatus, LucideIcon> = { active: CircleCheck, model_missing: Ban, skeleton: Construction };

export function ScenarioIcon({ icon, size = 16 }: { icon: string; size?: number }) {
  const I = SCENARIO_ICON[icon] ?? CircleHelp;
  return <I size={size} strokeWidth={SW} aria-hidden="true" className={icon === "fall" ? "ops-icon-fall" : undefined} />;
}
function LevelMark({ level }: { level: Level }) {
  const title = useLevelTitle();
  return <span className={`ops-level ops-level-${level}`}>{level === "red" ? <Square size={9} strokeWidth={0} fill="currentColor" aria-hidden="true" /> : <AlertTriangle size={10} strokeWidth={2.2} aria-hidden="true" />}{title(level)}</span>;
}
export function ScenarioState({ status, text }: { status: ScenarioStatus; text?: string }) {
  const I = STATUS_ICON[status];
  return <span className={`ops-sstate ops-sstate-${status}`} title={text}><I size={13} strokeWidth={SW} aria-hidden="true" />{STATUS_LABEL[status]}</span>;
}

type View = Schemas["RulesScreenView"] & { sectors: Sector[] };
interface Bulk { label: string; previous: CameraRule[] }
const key = (r: Pick<CameraRule, "camera_id" | "scenario">) => `${r.camera_id}:${r.scenario}`;
const paramList = (p: Record<string, number>) => Object.entries(p).map(([k, v]) => `${k} = ${String(v).replace(".", ",")}`).join(", ");

export function RulesPage() {
  const meta = useMeta();
  const view = useApi<View>(async () => {
    const [rules, sectors] = await Promise.all([api.GET("/api/ohs/rules"), api.GET("/api/sectors")]);
    if (rules.error || !rules.data) return { error: rules.error ?? { code: "network", message: "Сервер не отвечает" }, response: rules.response };
    return { data: { ...rules.data, sectors: sectors.data ?? [] } };
  }, []);
  const [local, setLocal] = useState<Record<string, CameraRule>>({});
  const [busy, setBusy] = useState<Set<string>>(new Set());
  const [error, setError] = useState<ApiFailure>();
  const [bulk, setBulk] = useState<Bulk>();
  const [picked, setPicked] = useState<string>();

  const data = view.data;
  const rows = useMemo(() => (data?.rows ?? []).map(row => ({ camera: row.camera, rules: new Map(row.rules.map(r => [r.scenario, local[key(r)] ?? r])) })), [data, local]);
  const groups = useMemo(() => {
    const sectors = data?.sectors ?? [];
    const order = new Map(sectors.map(s => [s.id, s]));
    const out = new Map<number, { id: number; name: string; sort: number; rows: typeof rows }>();
    for (const row of rows) {
      const s = order.get(row.camera.sector_id);
      const g = out.get(row.camera.sector_id) ?? { id: row.camera.sector_id, name: s?.name ?? `Сектор ${row.camera.sector_id}`, sort: s?.sort_order ?? 1e9, rows: [] };
      g.rows.push(row);
      out.set(g.id, g);
    }
    return [...out.values()].sort((a, b) => a.sort - b.sort || a.id - b.id);
  }, [rows, data]);

  async function apply(targets: CameraRule[], enabled: boolean, label?: string) {
    const todo = targets.filter(r => r.status === "active" && r.enabled !== enabled && !busy.has(key(r)));
    if (!todo.length) return;
    setError(undefined);
    setBusy(prev => new Set([...prev, ...todo.map(key)]));
    const done: CameraRule[] = [];
    for (const rule of todo) {
      const result = await api.PUT("/api/cameras/{camera_id}/rules/{scenario}", {
        params: { path: { camera_id: rule.camera_id, scenario: rule.scenario } },
        body: { enabled, params: rule.params },
      });
      setBusy(prev => { const next = new Set(prev); next.delete(key(rule)); return next; });
      if (result.error || !result.data) { setError(apiError(result.error)); break; }
      const saved = result.data;
      done.push(rule);
      setLocal(prev => ({ ...prev, [key(saved)]: saved }));
    }
    setBusy(prev => { const next = new Set(prev); todo.forEach(r => next.delete(key(r))); return next; });
    if (label && done.length) setBulk({ label: `${label}: ${done.length} ${plural(done.length)}`, previous: done });
  }
  async function undo() {
    if (!bulk) return;
    const prev = bulk.previous;
    setBulk(undefined);
    await apply(prev.filter(r => r.enabled).map(r => ({ ...current(r), enabled: false })), true);
    await apply(prev.filter(r => !r.enabled).map(r => ({ ...current(r), enabled: true })), false);
  }
  const current = (r: CameraRule) => local[key(r)] ?? r;
  function reload() { setLocal({}); setBulk(undefined); setError(undefined); view.reload(); }

  const heading = (meta?: ReactNode) => <PageHeading title="Правила наблюдения" meta={meta}>
    <button className="button button-small" onClick={reload} disabled={view.loading}><RefreshCw size={14} strokeWidth={SW} aria-hidden="true" /> Обновить</button>
  </PageHeading>;
  if (view.error) return <div className="ops-page">{heading()}<ErrorNotice error={view.error} retry={reload} /></div>;
  if (!data) return <div className="ops-page">{heading()}<Loading text="Загружаем правила камер" /></div>;

  const scenarios = data.scenarios;
  const selected = scenarios.find(s => s.id === picked) ?? scenarios[0];
  const all = rows.flatMap(r => [...r.rules.values()]);
  const enabledCount = all.filter(r => r.enabled && r.status === "active").length;
  const activeCount = scenarios.filter(s => s.status === "active").length;
  const column = (id: string) => rows.map(r => r.rules.get(id)).filter((r): r is CameraRule => !!r);
  const onCount = (list: CameraRule[]) => list.filter(r => r.enabled && r.status === "active").length;

  return <div className="ops-page" data-testid="rules-view">
    {heading(<>{rows.length} камер · {scenarios.length} сценариев, работают {activeCount} · включено правил <span className="mono">{enabledCount}</span></>)}
    <div className="ops-rules-bar" role="status">
      <span className="ops-rules-note">Изменения действуют на новые анализы видео. Уже обработанное видео — после «Пересчитать события» в параметрах камеры.</span>
      <span className="ops-rules-legend">
        {(["active", "model_missing", "skeleton"] as const).map(s => <span key={s}><ScenarioState status={s} /> <b className="mono">{scenarios.filter(x => x.status === s).length}</b></span>)}
      </span>
    </div>
    {error && <div className="ops-inline-error" role="alert"><AlertTriangle size={15} strokeWidth={SW} aria-hidden="true" /><span>{error.message}</span><button className="ops-icon-button" aria-label="Скрыть ошибку" onClick={() => setError(undefined)}><X size={14} strokeWidth={SW} /></button></div>}
    {bulk && <div className="ops-toast" role="status"><span>{bulk.label}</span><button className="button button-small" onClick={() => void undo()}><Undo2 size={14} strokeWidth={SW} aria-hidden="true" /> Отменить</button><button className="ops-icon-button" aria-label="Скрыть" onClick={() => setBulk(undefined)}><X size={14} strokeWidth={SW} /></button></div>}
    {!rows.length ? <Empty title="Камер нет" text="Правила задаются для камер. Добавьте камеры в разделе администратора — матрица появится здесь." /> : <div className="ops-rules-layout">
      <div className="ops-matrix-wrap" data-panel="Камеры × сценарии">
        <table className="ops-matrix" aria-label="Правила: камеры и сценарии">
          <thead>
            <tr>
              <th scope="col" className="ops-matrix-corner">Камера</th>
              {scenarios.map(s => <th key={s.id} scope="col" className={`ops-sc-head ${s.id === selected?.id ? "is-picked" : ""} ${s.status !== "active" ? "is-off" : ""}`}>
                <button className="ops-sc-pick" aria-pressed={s.id === selected?.id} onClick={() => setPicked(s.id)} title={s.description}>
                  <span className="ops-sc-top"><ScenarioIcon icon={s.icon} size={16} /><LevelMark level={s.default_level} /></span>
                  <span className="ops-sc-title">{s.title}</span>
                  {s.status === "active" ? <span className="ops-sc-count mono">{onCount(column(s.id))}/{rows.length}</span> : <ScenarioState status={s.status} text={s.status_text} />}
                </button>
              </th>)}
              <th scope="col" className="ops-matrix-tail">Вся строка</th>
            </tr>
            <tr className="ops-col-bulk">
              <th scope="row">Все камеры</th>
              {scenarios.map(s => <td key={s.id} className={s.id === selected?.id ? "is-picked" : ""}>
                {s.status === "active" ? <BulkPair what={`«${s.title}» на всех камерах`} on={() => void apply(column(s.id), true, `«${s.title}» включён`)} off={() => void apply(column(s.id), false, `«${s.title}» выключен`)} /> : <span className="ops-na-dash" aria-hidden="true">—</span>}
              </td>)}
              <td />
            </tr>
          </thead>
          {groups.map(g => {
            const sectorRules = g.rows.flatMap(r => [...r.rules.values()]);
            return <tbody key={g.id}>
              <tr className="ops-sector-row">
                <th scope="rowgroup" colSpan={scenarios.length + 1}><span>{g.name}</span><small>{g.rows.length} {g.rows.length === 1 ? "камера" : g.rows.length < 5 ? "камеры" : "камер"} · включено {onCount(sectorRules)}</small></th>
                <td><BulkPair what={`все сценарии в секторе «${g.name}»`} on={() => void apply(sectorRules, true, `${g.name}: включено`)} off={() => void apply(sectorRules, false, `${g.name}: выключено`)} /></td>
              </tr>
              {g.rows.map(({ camera, rules }) => <tr key={camera.id} className="ops-cam-row">
                <th scope="row" className="ops-cam-cell"><CameraLabel camera={camera} /></th>
                {scenarios.map(s => {
                  const rule = rules.get(s.id);
                  return <td key={s.id} className={`ops-cell ${s.id === selected?.id ? "is-picked" : ""}`}>
                    {!rule ? <span className="ops-na-dash">—</span> : <RuleSwitch rule={rule} scenario={s} camera={camera} busy={busy.has(key(rule))} toggle={() => void apply([rule], !rule.enabled)} />}
                  </td>;
                })}
                <td className="ops-row-bulk"><BulkPair what={`все сценарии на камере «${camera.name}»`} on={() => void apply([...rules.values()], true, `${camera.name}: включено`)} off={() => void apply([...rules.values()], false, `${camera.name}: выключено`)} /></td>
              </tr>)}
            </tbody>;
          })}
        </table>
      </div>
      {selected && <Inspector scenario={selected} rules={column(selected.id)} cameras={rows.map(r => r.camera)} zoneTitle={id => meta?.zone_kinds.find(z => z.id === id)?.title ?? id} />}
    </div>}
  </div>;
}

function plural(n: number) { const d = n % 10, h = n % 100; return d === 1 && h !== 11 ? "правило" : d >= 2 && d <= 4 && (h < 12 || h > 14) ? "правила" : "правил"; }

function CameraLabel({ camera }: { camera: Camera }) {
  return <div className="ops-cam">
    <div className="ops-cam-name"><span title={camera.description || camera.name}>{camera.name}</span>{camera.is_demo && <em>Демо</em>}</div>
    <div className="ops-cam-meta">
      <span>{camera.has_calibration ? "калибровка есть" : "без калибровки"}</span>
      <span>зон: <b className="mono">{camera.zones_count}</b></span>
      <Link to={`/admin/cameras/${camera.id}?tab=rules`} className="ops-cam-link" aria-label={`Параметры камеры «${camera.name}»`}><SlidersHorizontal size={13} strokeWidth={SW} aria-hidden="true" />Параметры</Link>
    </div>
  </div>;
}

function BulkPair({ what, on, off }: { what: string; on: () => void; off: () => void }) {
  return <span className="ops-bulk"><button onClick={on} aria-label={`Включить ${what}`} title={`Включить ${what}`}>Вкл</button><button onClick={off} aria-label={`Выключить ${what}`} title={`Выключить ${what}`}>Выкл</button></span>;
}

function RuleSwitch({ rule, scenario, camera, busy, toggle }: { rule: CameraRule; scenario: ScenarioMeta; camera: Camera; busy: boolean; toggle: () => void }) {
  const custom = Object.keys(rule.params).length > 0;
  if (rule.status !== "active") return <span className="ops-na" title={`${STATUS_LABEL[rule.status]}: ${scenario.status_text}`}><CircleDashed size={14} strokeWidth={SW} aria-hidden="true" /><span className="sr-only">{scenario.title} на камере {camera.name}: {STATUS_LABEL[rule.status]}</span></span>;
  return <span className="ops-cell-in">
    <button role="switch" aria-checked={rule.enabled} aria-busy={busy} disabled={busy} onClick={toggle} className={`ops-switch ${rule.enabled ? "is-on" : ""} ${busy ? "is-busy" : ""}`} aria-label={`${scenario.title} на камере ${camera.name}`} title={rule.enabled ? "Включено" : "Выключено"}>
      <i aria-hidden="true" /><span aria-hidden="true">{rule.enabled ? "Вкл" : "Выкл"}</span>
    </button>
    {custom && <span className="ops-custom" title={`Свои параметры: ${paramList(rule.params)}`}><SlidersHorizontal size={11} strokeWidth={2} aria-hidden="true" /><span className="sr-only">Свои параметры: {paramList(rule.params)}</span></span>}
  </span>;
}

function Inspector({ scenario, rules, cameras, zoneTitle }: { scenario: ScenarioMeta; rules: CameraRule[]; cameras: Camera[]; zoneTitle: (id: string) => string }) {
  const name = (id: number) => cameras.find(c => c.id === id)?.name ?? `Камера ${id}`;
  const custom = rules.filter(r => Object.keys(r.params).length);
  const on = rules.filter(r => r.enabled && r.status === "active").length;
  return <aside className="ops-inspector" data-panel="Сценарий" aria-label={`Сценарий «${scenario.title}»`}>
    <div className="ops-insp-col">
    <header className="ops-insp-head">
      <span className="ops-insp-icon"><ScenarioIcon icon={scenario.icon} size={20} /></span>
      <div><h2>{scenario.title}</h2><div className="ops-insp-tags"><LevelMark level={scenario.default_level} /><ScenarioState status={scenario.status} /></div></div>
    </header>
    <p className="ops-insp-desc">{scenario.description}</p>
    {scenario.status !== "active" && <p className={`ops-insp-status ops-sstate-${scenario.status}`}>{scenario.status_text}</p>}
    <dl className="ops-insp-dl">
      <div><dt>Включено</dt><dd><b className="mono">{on}</b> из <span className="mono">{rules.length}</span> камер</dd></div>
      <div><dt>Классы модели</dt><dd className="ops-chips">{scenario.required_classes.length ? scenario.required_classes.map(c => <code key={c}>{c}</code>) : "—"}</dd></div>
      <div><dt>Зоны</dt><dd className="ops-chips">{scenario.zone_kinds.length ? scenario.zone_kinds.map(z => <span key={z}>{zoneTitle(z)}</span>) : "не нужны"}</dd></div>
    </dl>
    </div>
    <div className="ops-insp-col">
    <h3>Параметры по умолчанию</h3>
    {scenario.params.length ? <table className="ops-params">
      <tbody>{scenario.params.map(p => <tr key={p.key}><th scope="row">{p.title}</th><td className="mono">{fmt(p.default)}{p.unit && <small> {p.unit}</small>}</td><td className="mono ops-range">{fmt(p.min)}…{fmt(p.max)}</td></tr>)}</tbody>
    </table> : <p className="ops-muted">Параметров нет.</p>}
    </div>
    <div className="ops-insp-col">
    <h3>Свои параметры камер</h3>
    {custom.length ? <ul className="ops-custom-list">{custom.map(r => <li key={r.camera_id}><Link to={`/admin/cameras/${r.camera_id}?tab=rules`}>{name(r.camera_id)}</Link><span className="mono">{paramList(r.params)}</span></li>)}</ul> : <p className="ops-muted">Все камеры на значениях по умолчанию. Менять — в параметрах камеры, вкладка «Правила».</p>}
    </div>
  </aside>;
}
const fmt = (v: number) => String(v).replace(".", ",");
