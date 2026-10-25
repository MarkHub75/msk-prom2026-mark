import { useMemo, useState, type ReactNode } from "react";
import type { CameraProfile, DefaultsV2, Mode, RolloutRequestV2, ScaleRequestV2 } from "../../api/calcV2";
import { apiError, getActor, type ApiFailure } from "../../api/client";
import { Badge, Button, ErrorNotice, Icon, Loading, PageHeading, Panel, Segmented } from "../../components/ui";
import { useRole } from "../../roles";
import { num, rub } from "./format";
import { getAt, limitFor, NumField, parseNum, setAt, type NumOptions } from "./form";
import { CurvePanel, HardwarePanel, LoadKpis, Notices, StatusLine, ThresholdsPanel, TiersV2 } from "./ResultV2View";
import { StepsPanel } from "./StepsPanel";
import { useCalcV2, type RequestV2 } from "./useCalcV2";
import "../../styles/v5.css";
import "../../styles/calc-v2.css";

// Calculator v2 by docs/CALCULATOR_CONTRACT_V2.md 2.0.0 (К10): defaults give full request bodies, the form edits
// them, the server counts everything. Fixtures of К14 are used only in tests and screenshots, never here.
const clone = <T,>(v: T): T => JSON.parse(JSON.stringify(v)) as T;
const SYSTEM: CameraProfile = { source: "system", camera_ids: null, include_seed: false };
type Drafts = Record<string, { text: string; error?: string }>;

function Section({ title, children }: { title: string; children: ReactNode }) {
  return <fieldset className="cv2-section"><legend>{title}</legend><div className="v5-form-grid">{children}</div></fieldset>;
}

export function CalculatorV2({ defaults }: { defaults: DefaultsV2 }) {
  const [role] = useRole();
  const canRollout = role === "management";
  const [mode, setMode] = useState<Mode>(canRollout ? "rollout" : "scale");
  const shown: Mode = canRollout ? mode : "scale";
  const [rollout, setRollout] = useState<RolloutRequestV2>(() => clone(defaults.rollout));
  const [scale, setScale] = useState<ScaleRequestV2>(() => clone(defaults.scale));
  const [drafts, setDrafts] = useState<Drafts>({});
  const body: RequestV2 = shown === "rollout" ? rollout : scale;
  const setBody = (next: RequestV2) => (shown === "rollout" ? setRollout(next as RolloutRequestV2) : setScale(next as ScaleRequestV2));
  const draftKey = (path: string) => `${shown}:${path}`;
  const invalid = (m: Mode) => Object.entries(drafts).some(([k, d]) => k.startsWith(`${m}:`) && d.error);

  const rolloutCalc = useCalcV2("rollout", rollout, canRollout && shown === "rollout" && !invalid("rollout"));
  const scaleCalc = useCalcV2("scale", scale, shown === "scale" && !invalid("scale"));
  const calc = shown === "rollout" ? rolloutCalc : scaleCalc;
  const result = calc.result?.mode === shown ? calc.result : undefined;
  const serverField = calc.error?.code === "validation" ? calc.field : undefined;

  const field = (path: string, label: string, o: NumOptions = {}) => {
    const lim = limitFor(defaults.limits, path);
    const opts: NumOptions = { ...o, integer: o.integer ?? lim?.integer, min: o.min ?? lim?.min ?? undefined, max: o.max ?? lim?.max ?? undefined };
    const d = drafts[draftKey(path)];
    const onDraft = (text: string) => {
      const parsed = parseNum(text, opts);
      setDrafts(all => ({ ...all, [draftKey(path)]: { text, error: parsed.error } }));
      if (parsed.error === undefined) {
        let next = setAt(body, path, opts.emptyDeletes && parsed.value === null ? undefined : parsed.value);
        // К4: a hand-edited activity share is no longer the measurement.
        if (path === "load.activity_share") next = setAt(next, "load.activity_measurement_id", null);
        setBody(next);
      }
    };
    const error = d?.error ?? (serverField === path ? calc.error?.message : undefined);
    return <NumField key={path} id={`cv2-${shown}-${path}`} label={label} value={getAt(body, path)} draft={d?.text} error={error} options={opts} onDraft={onDraft} />;
  };
  const toggle = (path: string, label: string) => <label key={path} className="cv2-check"><input type="checkbox" checked={Boolean(getAt(body, path))} onChange={e => setBody(setAt(body, path, e.target.checked))} />{label}</label>;

  const resetDrafts = (m: Mode) => setDrafts(all => Object.fromEntries(Object.entries(all).filter(([k]) => !k.startsWith(`${m}:`))));
  const pickPreset = (id: string) => { const p = defaults.presets.find(x => x.id === id); if (!p) return; setRollout(clone(p.rollout)); resetDrafts("rollout"); setMode("rollout"); };
  const pickSystem = () => {
    if (shown === "rollout") setRollout(r => ({ ...r, preset_id: null, cameras: clone(SYSTEM) }));
    else setScale(s => ({ ...s, current: clone(SYSTEM) }));
    resetDrafts(shown);
  };
  const profile = shown === "rollout" ? rollout.cameras : scale.current;
  const activity = defaults.measurements.find(m => m.key === "activity_share" && m.status === "measured" && m.value !== null);

  const presets = <div className="cv2-presets" role="group" aria-label="Быстрый старт">
    {defaults.presets.map(p => <button key={p.id} type="button" className={shown === "rollout" && rollout.preset_id === p.id && rollout.cameras.source === "manual" ? "is-on" : undefined} aria-pressed={shown === "rollout" && rollout.preset_id === p.id} onClick={() => pickPreset(p.id)} disabled={!canRollout} title={p.note}>
      <b>{p.title}</b><small>{p.rollout.cameras.source === "manual" ? `${p.rollout.cameras.cameras} камер` : "камеры системы"}{p.area_m2 ? ` · ${num(p.area_m2)} м²` : ""}</small>
    </button>)}
    <button type="button" className={profile.source === "system" ? "is-on" : undefined} aria-pressed={profile.source === "system"} onClick={pickSystem}>
      <b>По вашим камерам</b><small>{defaults.system_profile.cameras ? `${defaults.system_profile.cameras} камер в системе` : "камер в системе пока нет"}</small>
    </button>
  </div>;

  const cameraFields = shown === "rollout"
    ? (rollout.cameras.source === "manual" ? [field("cameras.cameras", "Камер")] : [])
    : [scale.current.source === "manual" ? field("current.cameras", "Камер сейчас") : null, scale.added.source === "manual" ? field("added.cameras", "Добавить камер") : null];

  const boardsSection = defaults.boards.map(b => {
    const allowed = body.hardware.allowed_board_ids.includes(b.id);
    const overrides = body.hardware.board_price_overrides;
    const unknown = b.id in overrides && overrides[b.id] === null;
    const setAllowed = (on: boolean) => setBody(setAt(body, "hardware.allowed_board_ids", on ? [...body.hardware.allowed_board_ids, b.id] : body.hardware.allowed_board_ids.filter(x => x !== b.id)));
    const setUnknown = (on: boolean) => setBody(setAt(body, `hardware.board_price_overrides.${b.id}`, on ? null : undefined));
    return <div key={b.id} className="cv2-board">
      <label className="cv2-check"><input type="checkbox" checked={allowed} onChange={e => setAllowed(e.target.checked)} />{b.title} · {b.chips} чип.</label>
      {!unknown && field(`hardware.board_price_overrides.${b.id}`, `Цена ${b.id}`, { unit: "₽", min: 0, nullable: true, emptyDeletes: true, hint: b.price_rub === null ? "в каталоге цены нет — пусто значит неизвестна" : `пусто — каталог: ${rub(b.price_rub)}` })}
      <label className="cv2-check"><input type="checkbox" checked={unknown} onChange={e => setUnknown(e.target.checked)} />цена неизвестна</label>
    </div>;
  });

  const [pdf, setPdf] = useState<{ busy: boolean; error?: ApiFailure }>({ busy: false });
  const exportPdf = async () => {
    setPdf({ busy: true });
    try {
      const headers: Record<string, string> = { "Content-Type": "application/json", "X-Role": role };
      const actor = getActor(); if (actor) headers["X-Actor"] = encodeURIComponent(actor);
      const r = await globalThis.fetch(new Request(new URL("/api/calculator/export.pdf", import.meta.env.VITE_API_BASE || location.origin), { method: "POST", headers, body: JSON.stringify({ mode: shown, input: body }) }));
      if (!r.ok) { setPdf({ busy: false, error: { ...apiError(await r.json().catch(() => undefined)), status: r.status } }); return; }
      const url = URL.createObjectURL(await r.blob());
      const a = document.createElement("a"); a.href = url; a.download = `argus-calculator-${shown}.pdf`; document.body.append(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 2000);
      setPdf({ busy: false });
    } catch (e) { setPdf({ busy: false, error: apiError(e) }); }
  };

  const market = useMemo(() => defaults.market.map(m => ({ ...m, sources: m.source_ids.map(id => defaults.sources.find(s => s.id === id)).filter(Boolean) })), [defaults]);

  return <div className="v5-page v5-calc cv2" data-testid="calculator-v2">
    <PageHeading title="Калькулятор окупаемости" meta={<span>Сервер считает оборудование, затраты и пороги; цены и доли — подписанные допущения, замените своими.</span>}>
      {defaults.features.pdf_available && <Button size="sm" icon="download" busy={pdf.busy} onClick={() => void exportPdf()} data-testid="calc-pdf">PDF</Button>}
      {canRollout && <Segmented label="Режим" value={shown} onChange={setMode} options={[{ id: "rollout", label: "Внедрение" }, { id: "scale", label: "Масштабирование" }]} />}
    </PageHeading>
    {pdf.error && <ErrorNotice error={pdf.error} compact />}
    {presets}
    <div className="v5-calc-grid">
      <Panel title={shown === "rollout" ? "Ваш проект" : "Расширение"} tools={<Button size="sm" variant="ghost" icon="refresh" onClick={() => { if (shown === "rollout") setRollout(clone(defaults.rollout)); else setScale(clone(defaults.scale)); resetDrafts(shown); }}>Сбросить</Button>}>
        <form className="v5-form cv2-form" onSubmit={e => e.preventDefault()}>
          {profile.source === "system" && <p className="v5-hint"><Icon name="camera" size={14} />Камеры и модели берутся из правил камер системы{defaults.system_profile.cameras ? `: ${defaults.system_profile.cameras} камер` : "; сейчас подходящих камер нет — расчёт будет пустым"}.</p>}
          <div className="v5-form-grid">
            {cameraFields}
            {field("site.workshops", shown === "rollout" ? "Цехов" : "Цехов в добавляемой области")}
            {field("site.workers", "Работников")}
            {field("site.shifts_per_day", "Смен в сутки")}
            {field("site.operators", "Операторов в смену")}
            {field("load.activity_share", "Доля времени с людьми в кадре", { hint: "0…1; модель нагрузки, не замер" })}
            {field("benefits.severe_injury_cost_rub", "Прямая стоимость тяжёлого случая", { unit: "₽", nullable: true, min: 0 })}
          </div>
          {activity && <Button size="sm" variant="ghost" icon="activity" onClick={() => setBody(setAt(setAt(body, "load.activity_share", activity.value), "load.activity_measurement_id", activity.id))}>Подставить активность: {num(activity.value)} ({activity.title})</Button>}
          {shown === "scale" && <label className="cv2-check"><input type="checkbox" checked={scale.installed !== null} onChange={e => setScale(s => ({ ...s, installed: e.target.checked ? { boards: [{ board_id: "HP", count: 0 }], servers: 0 } : null }))} />Указать установленное оборудование (иначе сервер оценит его по текущим камерам)</label>}
          {shown === "scale" && scale.installed && <div className="v5-form-grid">{field("installed.boards.0.count", `Установлено плат ${scale.installed.boards[0]?.board_id ?? "HP"}`, { integer: true, min: 0 })}{field("installed.servers", "Установлено серверов", { integer: true, min: 0 })}</div>}
          <details className="cv2-advanced">
            <summary>Расширенные допущения</summary>
            <Section title="Нагрузка">
              {field("load.target_fps", "Частота анализа", { unit: "кадр/с" })}
              {field("load.surge_fps", "Частота при всплеске", { unit: "кадр/с" })}
              {field("load.idle_check_s", "Проверка пустой камеры раз в", { unit: "с" })}
              {field("load.priority_cameras_reserve", "Резерв тревожных камер", { integer: true, min: 0 })}
              {field("load.reference_chip_fps", "Ёмкость чипа по заявлению производителя", { unit: "кадр/с" })}
              {field("load.capacity_derate", "Запас ёмкости", { hint: "доля, 0…1" })}
              {field("load.cpu_ms_per_unit", "CPU на единицу нагрузки", { unit: "мс", min: 0 })}
              <label className="cv2-check"><input type="checkbox" checked={body.load.peak_mode === "all_active"} onChange={e => setBody(setAt(body, "load.peak_mode", e.target.checked ? "all_active" : "independent_p95"))} />Все камеры активны одновременно (консервативно)</label>
            </Section>
            <fieldset className="cv2-section"><legend>Платы LinQ</legend><div className="cv2-boards">{boardsSection}</div></fieldset>
            <Section title="Сервер">
              {field("hardware.server.price_rub", "Цена сервера", { unit: "₽", nullable: true, min: 0 })}
              {field("hardware.server.slots", "Слотов под платы", { integer: true, min: 1 })}
              {field("hardware.server.usable_cpu_cores", "Полезных ядер CPU", { min: 0 })}
              {field("hardware.server.power_w", "Мощность сервера", { unit: "Вт", nullable: true, min: 0 })}
            </Section>
            <Section title="Затраты">
              {field("costs.integration_fixed_rub", "Пусконаладка, фиксированно", { unit: "₽", nullable: true, min: 0 })}
              {field("costs.integration_per_camera_rub", "Пусконаладка на камеру", { unit: "₽", nullable: true, min: 0 })}
              {field("costs.support_share_year", "Поддержка в год, доля вложений", { min: 0, max: 1 })}
              {field("costs.electricity_rub_kwh", "Электроэнергия", { unit: "₽/кВт·ч", nullable: true, min: 0 })}
              {field("costs.operating_hours_year", "Часов работы в год", { min: 0, max: 8784 })}
              {field("costs.signal_zones_per_camera", "Сигнальных зон на камеру", { min: 0 })}
              {field("costs.signal_unit_rub", "Свет и звук у зоны", { unit: "₽", nullable: true, min: 0 })}
              {field("costs.speaker_per_workshop_rub", "Громкоговоритель в цех", { unit: "₽", nullable: true, min: 0 })}
              {field("costs.new_camera_unit_rub", "Новая камера с монтажом", { unit: "₽", nullable: true, min: 0 })}
              {field("costs.new_camera_count", "Покупаем физических камер", { integer: true, min: 0 })}
              {field("costs.max_additional_camera_share", "Доля новых камер на максимальном уровне", { min: 0, max: 1 })}
            </Section>
            <Section title="Выгоды: травмы">
              {toggle("benefits.injuries.enabled", "Учитывать")}
              {field("benefits.injuries.annual_injured_workers", "Пострадавших в год", { nullable: true, min: 0, hint: "пусто — по частоте на 1000" })}
              {field("benefits.injuries.rate_per_1000", "Пострадавших на 1000 работников", { nullable: true, min: 0 })}
              {field("benefits.injuries.cost_per_injured_worker_rub", "Прямые потери на пострадавшего", { unit: "₽", nullable: true, min: 0 })}
              {field("benefits.injuries.reduction.base", "Снижение: базовый", { min: 0, max: 1 })}
              {field("benefits.injuries.reduction.extended", "Снижение: расширенный", { min: 0, max: 1 })}
              {field("benefits.injuries.reduction.max", "Снижение: максимальный", { min: 0, max: 1 })}
            </Section>
            <Section title="Выгоды: простой, штрафы, СФР, время">
              {toggle("benefits.downtime.enabled", "Простой")}
              {field("benefits.downtime.events_year", "Остановок в год", { nullable: true, min: 0 })}
              {field("benefits.downtime.days_per_event", "Дней на остановку", { nullable: true, min: 0 })}
              {field("benefits.downtime.day_cost_rub", "Стоимость дня простоя", { unit: "₽", nullable: true, min: 0 })}
              {toggle("benefits.fines.enabled", "Штрафы (ожидаемый риск)")}
              {body.benefits.fines.items.map((f, i) => field(`benefits.fines.items.${i}.amount_rub`, f.title, { unit: "₽", nullable: true, min: 0 }))}
              {toggle("benefits.sfr_discount.enabled", "Скидка СФР")}
              {field("benefits.sfr_discount.payroll_rub_year", "Фонд оплаты труда в год", { unit: "₽", nullable: true, min: 0 })}
              {field("benefits.sfr_discount.additional_discount_share", "Дополнительная скидка", { nullable: true, min: 0, max: 0.4 })}
              {toggle("benefits.labor.monetize", "Время контроля в деньгах")}
              {body.benefits.labor.rows.map((row, i) => field(`benefits.labor.rows.${i}.hours_saved_year`, `${row.title}: часов в год`, { min: 0 }))}
            </Section>
          </details>
        </form>
      </Panel>
      <section className="v5-calc-result cv2-result" aria-label="Результат расчёта" aria-busy={calc.busy}>
        {calc.error && !serverField && <ErrorNotice error={calc.error} compact />}
        {serverField && <p className="v5-hint is-error" role="alert" data-testid="field-error">Сервер не принял поле: {calc.error?.message}{result ? ". Показан последний расчёт." : ""}</p>}
        {result ? <div className={`cv2-result-body${calc.busy ? " is-stale" : ""}`}>
          <StatusLine result={result} busy={calc.busy} />
          <Notices missing={result.missing} warnings={result.warnings} />
          <StepsPanel result={result} trackerAvailable={defaults.features.tracker.available} />
          <LoadKpis result={result} />
          <HardwarePanel result={result} />
        </div> : !calc.error && <Loading text="Считаем на сервере" />}
      </section>
    </div>
    {result && <div className={`cv2-below${calc.busy ? " is-stale" : ""}`}>
      <TiersV2 result={result} />
      <ThresholdsPanel result={result} />
      <CurvePanel result={result} />
    </div>}
    <Panel title="Рыночные ориентиры" tools={<Badge tone="grey">чужие цены, не цена Argus</Badge>} flush data-testid="market-v2">
      <table className="ds-table v5-market">
        <thead><tr><th>Что</th><th>Цена</th><th>Источник</th></tr></thead>
        <tbody>{market.map(m => <tr key={m.id}><td><b>{m.title}</b><small>{m.scope}</small></td>
          <td className="v5-market-value">{m.amount_rub === null ? "нет данных" : `${rub(m.amount_rub)} ${m.billing === "monthly_per_camera" ? "за камеру в месяц" : m.billing === "one_off_per_camera" ? "за камеру разово" : "за проект"}`}</td>
          <td className="v5-source">{m.sources.map(s => `${s!.title}${s!.checked_at ? `, ${s!.checked_at.slice(0, 10)}` : ""}${s!.verification === "pending_primary" ? " (не перепроверено)" : ""}`).join("; ")}</td></tr>)}</tbody>
      </table>
    </Panel>
    {defaults.notices.length > 0 && <ul className="cv2-notices">{defaults.notices.map(n => <li key={n.code} data-code={n.code}><Icon name="info" size={14} />{n.message}</li>)}</ul>}
  </div>;
}
