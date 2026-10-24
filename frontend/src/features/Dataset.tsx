import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { api, mediaUrl } from "../api/client";
import { useApi } from "../api/useApi";
import { useMeta } from "../components/AppShell";
import { Button, buttonClass, Empty, ErrorNotice, Icon, IconButton, isPending, Kpi, Loading, PageHeading, Panel } from "../components/ui";
import "../styles/v5.css";

// tech.md 8.26: every event with the «false alarm» verdict lands in the dataset once (worker datasets_flush):
// frames of the clip window, detections, pose, HUD and label.json; the ZIP adds manifest.json.
const FILES = [
  { name: "frames/<кадр>.jpg", text: "проанализированные кадры окна клипа" },
  { name: "detections.jsonl", text: "детекции моделей по кадрам (формат — docs/ML_INTEGRATION.md, раздел 4)" },
  { name: "pose.jsonl", text: "точки позы, если pose был в анализе" },
  { name: "hud.jsonl", text: "кадры HUD с треками и тегами" },
  { name: "label.json", text: "метка «ложное срабатывание», сценарий, причина, видео, модели, комментарий оператора" },
];

// The worker adds an item a couple of seconds after the verdict and sends no WS message for it.
const POLL_MS = 10_000;
const EXPORT = "/api/datasets/false-alarms/export.zip";

const stamp = new Intl.DateTimeFormat("ru-RU", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit", timeZone: "Europe/Moscow" });

export function DatasetPage() {
  const meta = useMeta();
  const view = useApi(() => api.GET("/api/datasets/false-alarms"), []);
  const reload = useRef(view.reload); reload.current = view.reload;
  useEffect(() => { const timer = setInterval(() => reload.current(), POLL_MS); return () => clearInterval(timer); }, []);
  const scenario = (id: string) => meta?.scenarios.find(s => s.id === id)?.title ?? id;

  const data = view.data;
  const byScenario = new Map<string, number>();
  for (const item of data?.items ?? []) byScenario.set(item.scenario, (byScenario.get(item.scenario) ?? 0) + 1);

  // A server without the dataset has nothing to refresh or download: no actions next to the pending notice.
  const heading = <PageHeading title="Датасет ложных срабатываний" meta={<span>Каждое событие с вердиктом «Ложное срабатывание» один раз сохраняется для дообучения моделей</span>}>
    {!isPending(view.error) && <>
    <IconButton icon="refresh" label="Обновить" onClick={view.reload} disabled={view.loading} />
    {/* The list answered, so the export route exists: a plain download lets the browser stream an archive of
        hundreds of MB (about 13 MB per event at 40 frames) to disk instead of holding it in memory as a blob. */}
    {data?.total ? <a className={buttonClass("primary")} href={mediaUrl(EXPORT)} download data-testid="export-zip"><Icon name="download" />Скачать ZIP</a>
      : <Button variant="primary" icon="download" disabled data-testid="export-zip">Скачать ZIP</Button>}
    </>}
  </PageHeading>;

  if (view.error) return <div className="v5-page">{heading}<ErrorNotice error={view.error} retry={view.reload} pending="Соберёт события с вердиктом «Ложное срабатывание» в датасет для дообучения: кадры, детекции, HUD и метку." /></div>;
  if (!data) return <div className="v5-page">{heading}<Loading text="Получаем состав датасета" /></div>;

  return <div className="v5-page" data-testid="dataset">
    {heading}
    <div className="v5-kpis">
      <Kpi label="Событий в датасете" value={data.total} />
      <Kpi label="Кадров" value={data.frames} hint="JPEG, на событие — не больше лимита кадров из настроек сервера" />
      <Kpi label="Сценариев" value={byScenario.size} hint={[...byScenario].sort((a, b) => b[1] - a[1]).map(([id, n]) => `${scenario(id)} ${n}`).join(" · ") || undefined} />
    </div>
    <div className="v5-split">
      <Panel title="Элементы" tools={<span className="v5-muted">{data.items.length} из {data.total}</span>} flush>
        {data.items.length ? <table className="ds-table" data-testid="dataset-items">
          <thead><tr><th>Событие</th><th>Сценарий</th><th className="num">Кадров</th><th>Добавлено, МСК</th><th>Папка</th></tr></thead>
          <tbody>{data.items.map(item => <tr key={item.event_id}>
            <td><Link to={`/events/${item.event_id}`} className="mono">#{item.event_id}</Link></td>
            <td>{scenario(item.scenario)}</td>
            <td className="num">{item.frames}</td>
            <td className="mono">{stamp.format(new Date(item.created_at))}</td>
            <td className="mono v5-path" title={item.path}>{item.path}</td>
          </tr>)}</tbody>
        </table> : <Empty icon="database" title="Ложных срабатываний пока нет" text="Отметьте событие «Ложное срабатывание» в карточке: оно появится здесь после следующего прохода воркера. Демо-события сида без эпизода не попадают." />}
      </Panel>
      <Panel title="Что внутри элемента">
        <ul className="v5-files">{FILES.map(f => <li key={f.name}><code>{f.name}</code><span>{f.text}</span></li>)}</ul>
        <p className="v5-hint">ZIP содержит все элементы и <code>manifest.json</code> со списком. То же из консоли: <code>safewatch dataset export --out DIR</code>.</p>
      </Panel>
    </div>
  </div>;
}
