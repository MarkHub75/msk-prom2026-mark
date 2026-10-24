import { Link } from "react-router-dom";
import { api } from "../../api/client";
import type { PassportScenario } from "../../api/types";
import { useApi } from "../../api/useApi";
import { Badge, buttonClass, Empty, ErrorNotice, Icon, IconButton, Loading, Panel, type IconName, type Tone } from "../../components/ui";
import { pct } from "../../components/charts/scale";
import "../../styles/v5.css";

// tech.md 8.28: the passport is computed on request from the HUD of the camera's last ready video;
// the verdict per scenario and its reason come from the server as they are.
type Verdict = PassportScenario["verdict"];
const VERDICT: Record<Verdict, { title: string; tone: Tone; icon: IconName }> = {
  suitable: { title: "Годна", tone: "green", icon: "ok" },
  partial: { title: "Частично", tone: "amber", icon: "alert" },
  unsuitable: { title: "Непригодна", tone: "red", icon: "critical" },
  unknown: { title: "Нет оценки", tone: "grey", icon: "no-observation" },
};
const ORDER: Verdict[] = ["unsuitable", "partial", "unknown", "suitable"];
const px = (v: number | null) => v === null ? "—" : `${Math.round(v)} px`;
// Server text texts.PASSPORT_NO_ZONES = "Нет зон: {kinds}" (tech.md 8.28 step 6): the fix is on the Zones tab.
const NO_ZONES = "Нет зон";

export function PassportTab({ cameraId }: { cameraId: number }) {
  const passport = useApi(() => api.GET("/api/cameras/{camera_id}/passport", { params: { path: { camera_id: cameraId } } }), [cameraId]);
  if (passport.error) return <ErrorNotice error={passport.error} retry={passport.reload} pending="Оценит по последней записи, какие сценарии камера видит надёжно, а какие частично или никак." />;
  const p = passport.data;
  if (!p) return <Loading text="Оцениваем пригодность камеры по последней записи" />;
  // No ready video: every scenario is «Нет обработанного видео»; one empty state instead of a table of the same row.
  if (p.analysis_id === null) return <div className="v5-passport" data-testid="passport">
    <Empty icon="camera" title="Нет обработанной записи" text={`Паспорт считается по последнему обработанному видео камеры: высота людей, темнота, пустые кадры и вердикт по каждому из ${p.scenarios.length} сценариев. Загрузите запись, и после обработки оценка появится здесь.`}>
      <Link className={buttonClass("primary", "sm")} to="?tab=video"><Icon name="file" size={14} />Открыть вкладку «Видео»</Link>
    </Empty>
  </div>;
  const count = (v: Verdict) => p.scenarios.filter(s => s.verdict === v).length;
  const sorted = [...p.scenarios].sort((a, b) => ORDER.indexOf(a.verdict) - ORDER.indexOf(b.verdict));
  const metrics = [
    { label: "Высота человека, медиана", value: px(p.person_height_px_p50), hint: "мелкие люди — хуже поза и СИЗ" },
    { label: "Мелкий предмет (телефон), медиана", value: px(p.small_object_px_p50), hint: p.small_object_px_p50 === null ? "телефонов в записи не было" : "большая сторона рамки cell phone" },
    { label: "Кадров с людьми", value: pct(p.person_frames_share), hint: "доля кадров анализа" },
    { label: "Темно или камера закрыта", value: pct(p.dark_share), hint: "доля длительности" },
    { label: "Пустых кадров", value: pct(p.empty_share), hint: "без единого объекта" },
    { label: "Кадров в оценке", value: String(p.frames), hint: p.analysis_id ? `анализ #${p.analysis_id}` : "обработанного видео нет" },
  ];

  // Same frame as the other setup tabs: panels with a tab-like title, the summary on the right of the head.
  return <div className="v5-passport" data-testid="passport">
    <Panel title="Паспорт пригодности" tools={<IconButton icon="refresh" label="Пересчитать" onClick={passport.reload} disabled={passport.loading} />}>
      <div className="v5-passport-head">
        <p>Что эта камера может видеть надёжно, а что нет — по последней обработанной записи. Пересчитывается при каждом открытии.</p>
        <ul className="v5-verdicts" aria-label="Итог по сценариям">{(["suitable", "partial", "unsuitable", "unknown"] as Verdict[]).map(v => <li key={v} className={count(v) ? `is-${v}` : "is-zero"}><b className="mono">{count(v)}</b><span>{VERDICT[v].title}</span></li>)}</ul>
      </div>
      {p.shift_text && <p className="v5-shift" role="status"><Badge tone={p.shift_px ? "amber" : "neutral"} icon={p.shift_px ? "alert" : "info"}>Положение камеры</Badge>{p.shift_text}</p>}
      <dl className="v5-metrics">{metrics.map(m => <div key={m.label}><dt>{m.label}</dt><dd className="mono">{m.value}</dd><small>{m.hint}</small></div>)}</dl>
    </Panel>
    <Panel title="Сценарии" tools={<span className="v5-muted">{p.scenarios.length}</span>} flush>
      <table className="ds-table v5-passport-table">
        <thead><tr><th>Сценарий</th><th>Вердикт</th><th>Причина</th></tr></thead>
        <tbody>{sorted.map(s => <tr key={s.scenario} data-verdict={s.verdict}>
          <td><b>{s.title}</b><small className="mono">{s.scenario}</small></td>
          <td><Badge tone={VERDICT[s.verdict].tone} icon={VERDICT[s.verdict].icon}>{VERDICT[s.verdict].title}</Badge></td>
          <td>{s.reason}{s.verdict === "partial" && s.reason.startsWith(NO_ZONES) && <Link className="v5-reason-fix" to="?tab=zones">Добавить зоны <Icon name="arrow" size={13} /></Link>}</td>
        </tr>)}</tbody>
      </table>
      <p className="v5-hint">«Частично» — сценарий работает, но с пропусками: проверьте зоны, ракурс и освещение. Плохой свет и ночь лечит модель, а не настройка: система честно пишет «Слишком темно».</p>
    </Panel>
  </div>;
}
