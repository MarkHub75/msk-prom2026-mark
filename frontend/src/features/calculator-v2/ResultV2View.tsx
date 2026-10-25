import type { EquipmentState, HardwareResult, MoneyLine, Notice, PaybackResult, PriceThreshold, ResultV2, SevereThreshold, TierResultV2 } from "../../api/calcV2";
import { Badge, Icon, Kpi, Panel } from "../../components/ui";
import { months, num, nullText, rub, STATUS } from "./format";

// К8: every sum, threshold and curve point is the server's; the screen only words statuses and null reasons.

export function StatusLine({ result, busy }: { result: ResultV2; busy: boolean }) {
  const s = STATUS[result.status];
  return <div className={`cv2-status is-${result.status}`} data-testid="result-status" data-status={result.status} role="status">
    <Badge tone={s.tone === "amber" ? "amber" : "grey"} icon={result.status === "partial" ? "alert" : result.status === "empty" ? "no-observation" : "info"}>{s.title}</Badge>
    <span>{s.text}</span>
    {busy && <Badge tone="accent" icon="spinner">пересчитываем — показан прошлый результат</Badge>}
  </div>;
}

/** К9: codes are for tests; the screen shows the server's Russian message, unknown codes included. */
export function Notices({ missing, warnings }: { missing: Notice[]; warnings: Notice[] }) {
  return <>
    {missing.length > 0 && <ul className="cv2-missing" data-testid="missing">{missing.map((n, i) => <li key={`${n.code}-${i}`} data-code={n.code}><Icon name="alert" size={14} /><span>{n.message}</span></li>)}</ul>}
    {warnings.length > 0 && <details className="cv2-warnings" data-testid="warnings"><summary>Оговорки расчёта · {warnings.length}</summary>
      <ul>{warnings.map((n, i) => <li key={`${n.code}-${i}`} data-code={n.code}>{n.message}</li>)}</ul>
    </details>}
  </>;
}

const SELECTION: Record<HardwareResult["selection"], string> = {
  priced_optimum: "дешёвая из допустимых комплектаций с известными ценами",
  technical_only: "техническая комплектация: цена части позиций неизвестна, это не «самая дешёвая»",
  unresolved: "не определена: нагрузка неизвестна",
};
const BASIS: Record<HardwareResult["inventory_basis"], string> = { none: "", provided: "установленное — как указано", estimated: "установленное — оценка по текущим камерам" };

function equipment(e: EquipmentState | null) {
  if (!e) return <span className="v5-muted">нет данных</span>;
  const list = e.boards.length ? e.boards.map(b => `${b.count} × ${b.board_id}`).join(" + ") : "плат нет";
  return <span className="mono">{list} · чипов {e.chips} · серверов {e.servers}{e.power_w === null ? "" : ` · до ${num(e.power_w)} Вт`}</span>;
}

export function HardwarePanel({ result }: { result: ResultV2 }) {
  const h = result.hardware, l = result.load;
  return <Panel title="Комплектация" data-testid="hardware">
    <p className="cv2-note">{SELECTION[h.selection]}{BASIS[h.inventory_basis] && ` · ${BASIS[h.inventory_basis]}`}</p>
    <dl className="v5-items cv2-equipment">
      {result.mode === "scale" && <div><dt>Было</dt><dd>{equipment(h.before)}</dd></div>}
      <div><dt>Купить</dt><dd>{equipment(h.purchase)}</dd></div>
      {result.mode === "scale" && <div><dt>Станет</dt><dd>{equipment(h.after)}</dd></div>}
      <div><dt>Платы</dt><dd className="mono">{rub(h.board_capex_rub, h.board_capex_rub === null ? "missing" : undefined)}</dd></div>
      <div><dt>Серверы</dt><dd className="mono">{rub(h.server_capex_rub, h.server_capex_rub === null ? "missing" : undefined)}</dd></div>
      <div><dt>Нужно чипов · запас</dt><dd className="mono">{num(h.required_after_chips)} · {num(h.spare_chips_after)}</dd></div>
      <div><dt>Ядер CPU</dt><dd className="mono">{num(l.required_cpu_cores)}</dd></div>
    </dl>
    {h.note && <p className="v5-hint">{h.note}</p>}
  </Panel>;
}

export function paybackText(p: PaybackResult): string {
  switch (p.status) {
    case "within_horizon": return p.months === null ? "в пределах 3 лет" : months(p.months);
    case "after_horizon": return p.months === null ? "дольше 3 лет" : `${months(p.months)} — дольше 3 лет`;
    case "no_positive_effect": return "Выгода не покрывает расходы";
    case "no_initial_investment": return "Вложений нет";
    case "insufficient_data": return "Нужно значение";
    case "not_applicable": return "Неприменимо";
  }
}

function lineAmount(l: MoneyLine) {
  if (!l.included) return <span className="v5-muted">не включено</span>;
  return <span className="mono">{rub(l.amount_rub, l.status)}</span>;
}

function Lines({ title, lines }: { title: string; lines: MoneyLine[] }) {
  return <div className="cv2-lines"><b>{title}</b><dl className="v5-items">{lines.map(l => <div key={l.id} className={l.included ? undefined : "is-off"}><dt>{l.title}</dt><dd>{lineAmount(l)}</dd></div>)}</dl></div>;
}

/** Null totals: «нужно значение» when the result is partial, «неприменимо» when empty. */
const totalStatus = (r: ResultV2) => (r.status === "partial" ? "missing" : r.status === "empty" ? "not_applicable" : undefined);

function TierCard({ tier, result }: { tier: TierResultV2; result: ResultV2 }) {
  const st = totalStatus(result);
  const pb = tier.payback;
  const net = tier.net_benefit_rub_year;
  return <article className="v5-tier" data-testid={`tier-${tier.tier}`}>
    <header><h3>{tier.title}</h3></header>
    <div className="v5-tier-capex"><span>Вложения</span><b className="mono">{rub(tier.capex_rub, st)}</b></div>
    <div className={`v5-tier-payback${pb.status === "within_horizon" || pb.status === "after_horizon" || pb.status === "no_initial_investment" ? "" : " is-none"}`} data-payback={pb.status}>
      <span>Окупаемость</span><b>{paybackText(pb)}</b><small className="cv2-reason">{pb.reason}</small>
    </div>
    <dl className="v5-tier-facts">
      <div><dt>Расходы в год</dt><dd className="mono">{rub(tier.opex_rub_year, st)}</dd></div>
      <div><dt>Выгода в год</dt><dd className="mono">{rub(tier.gross_benefit_rub_year, st)}</dd></div>
      <div><dt>Чистый эффект в год</dt><dd className={`mono${net !== null && net < 0 ? " is-neg" : ""}`}>{rub(net, st)}</dd></div>
      <div><dt>Владение за 3 года</dt><dd className="mono">{rub(tier.tco_3_year_rub, st)}</dd></div>
      <div><dt>Баланс за 3 года</dt><dd className={`mono${(tier.net_balance_3_year_rub ?? 0) < 0 ? " is-neg" : ""}`}>{rub(tier.net_balance_3_year_rub, st)}</dd></div>
      <div><dt>На камеру в месяц</dt><dd className="mono">{rub(tier.rub_per_camera_month, tier.camera_denominator ? st : "not_applicable")}<small> / {tier.camera_denominator} кам.</small></dd></div>
      <div><dt>Часы контроля в год</dt><dd className="mono">{num(tier.labor_hours_year)}</dd></div>
    </dl>
    <details className="v5-tier-items"><summary>Из чего сложилась сумма</summary>
      <Lines title="Вложения" lines={tier.capex_lines} />
      <Lines title="Расходы в год" lines={tier.opex_lines} />
      <Lines title="Выгоды в год" lines={tier.benefit_lines} />
    </details>
  </article>;
}

export function TiersV2({ result }: { result: ResultV2 }) {
  return <div className="v5-tiers" data-testid="tiers">{result.tiers.map(t => <TierCard key={t.tier} tier={t} result={result} />)}</div>;
}

function severeText(s: SevereThreshold): string {
  switch (s.status) {
    case "required": return `предотвратить ${num(s.whole_prevented_cases)} тяж. случ. за 3 года (ожидаемо ${num(s.expected_prevented_cases)})`;
    case "already_covered": return "затраты уже покрыты другими выгодами";
    case "needs_input": return `нужна стоимость тяжёлого случая; не покрыто ${rub(s.uncovered_cost_rub)}`;
    case "not_applicable": return "неприменимо";
  }
}
function priceText(p: PriceThreshold): string {
  const what = p.board_id ? `${p.board_id} × ${p.boards_to_buy}` : "плата";
  switch (p.status) {
    case "at_or_below": return `${what}: окупается за 3 года при цене до ${rub(p.max_unit_price_rub)}; сейчас ${rub(p.current_unit_price_rub, p.current_unit_price_rub === null ? "missing" : undefined)}`;
    case "already_within": return `${what}: текущая цена ${rub(p.current_unit_price_rub)} уже не выше ${rub(p.max_unit_price_rub)}`;
    case "free_still_insufficient": return `${what}: даже бесплатная плата не окупает проект за 3 года`;
    case "not_applicable": return "неприменимо: плат не покупаем";
    case "insufficient_data": return nullText("missing");
  }
}

export function ThresholdsPanel({ result }: { result: ResultV2 }) {
  return <Panel title="Что должно измениться для окупаемости за 3 года" flush data-testid="thresholds">
    <table className="ds-table cv2-thresholds">
      <thead><tr><th>Уровень</th><th>Предотвращённые тяжёлые случаи</th><th>Цена платы</th></tr></thead>
      <tbody>{result.tiers.map(t => <tr key={t.tier} data-tier={t.tier}>
        <td><b>{t.title}</b></td>
        <td data-status={t.severe_threshold.status}>{severeText(t.severe_threshold)}<small>{t.severe_threshold.reason}</small></td>
        <td data-status={t.board_price_threshold.status}>{priceText(t.board_price_threshold)}<small>{t.board_price_threshold.reason}</small></td>
      </tr>)}</tbody>
    </table>
    <p className="v5-hint">Порог случаев — общее необходимое число за 3 года вместо прямой выгоды от травм, а не добавка к ней. Порог цены — для выбранной комплектации, без нового подбора.</p>
  </Panel>;
}

export function CurvePanel({ result }: { result: ResultV2 }) {
  const pts = result.scale_curve.points;
  const max = Math.max(1, ...pts.map(p => p.rub_per_camera_month ?? 0));
  return <Panel title="Кривая масштаба: базовый уровень" data-testid="curve" tools={<Badge tone="grey">как новое внедрение</Badge>}>
    <ol className="cv2-curve">{pts.map(p => <li key={p.cameras} style={{ ["--share" as string]: (p.rub_per_camera_month ?? 0) / max }}>
      <span className="cv2-curve-n mono">{p.cameras}</span>
      <span className="cv2-curve-bar" aria-hidden><i /></span>
      <span className="mono">{rub(p.rub_per_camera_month)}<small> /кам./мес</small></span>
      <span className="mono cv2-curve-hw">{p.chips === null ? "нет данных" : `${p.chips} чип. · ${p.servers} серв.`}</span>
    </li>)}</ol>
    <p className="v5-hint">{result.scale_curve.note}{result.mode === "scale" ? " На экране расширения это стоимость эквивалентного нового внедрения, не добавочные расходы." : ""}</p>
  </Panel>;
}

export function LoadKpis({ result }: { result: ResultV2 }) {
  const l = result.load;
  return <div className="v5-kpis">
    <Kpi label="Камер в расчёте" value={l.cameras} hint={result.cost_scope === "incremental" ? "добавляемая область и итог" : "весь проект"} />
    <Kpi label="Активны в пике (p95)" value={l.active_p95} hint={l.basis === "all_active" ? "консервативно: все активны" : `резерв тревог ${l.priority_cameras_effective}`} />
    <Kpi label="Нагрузка, ед./с" value={num(l.required_units_s)} hint={`пик ${num(l.peak_units_s)} · всплеск ${num(l.surge_units_s)}`} />
    <Kpi label="Нужно чипов" value={num(l.required_chips)} hint={`наивно ${num(l.naive_chips)}`} />
    {result.operator_events_per_shift !== null && <Kpi label="Событий на оператора за смену" value={num(result.operator_events_per_shift)} hint="справочно, не прогноз травм" />}
  </div>;
}
