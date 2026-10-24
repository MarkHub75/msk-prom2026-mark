import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { ArrowDown, ArrowUp, Camera as CameraIcon, FolderTree, ImageOff, Layers, Pencil, Plus, Radio, Settings2, Trash2 } from "lucide-react";
import { api, apiError, mediaUrl, type ApiFailure } from "../api/client";
import type { Camera, CameraTile, Sector, SectorState } from "../api/types";
import { useApi } from "../api/useApi";
import { useWs } from "../api/ws";
import { ErrorNotice, Loading, PageHeading } from "../components/ui";
import { Field, Modal, StateBadge } from "../components/admin/AdminUi";
import "../styles/admin.css";

const I = { size: 15, strokeWidth: 1.75 } as const;
const LIVE_THROTTLE_MS = 1500;

type Dialog =
  | { kind: "sector"; sector?: Sector }
  | { kind: "camera"; camera?: Camera; sectorId?: number }
  | { kind: "delete-sector"; sector: Sector; cameras: number }
  | { kind: "delete-camera"; camera: Camera };

type Done = (result: { error?: unknown; response?: Response }) => ApiFailure | undefined;

function failure(result: { error?: unknown; response?: Response }): ApiFailure | undefined {
  if (result.error === undefined) return undefined;
  return { ...apiError(result.error), ...(result.response ? { status: result.response.status } : {}) };
}

function SectorForm({ sector, nextOrder, onClose, done }: { sector?: Sector; nextOrder: number; onClose: () => void; done: Done }) {
  const [name, setName] = useState(sector?.name ?? "");
  const [order, setOrder] = useState(String(sector?.sort_order ?? nextOrder));
  const [error, setError] = useState<ApiFailure>();
  const [busy, setBusy] = useState(false);
  const submit = async () => {
    setBusy(true);
    const body = { name: name.trim(), sort_order: Number(order) || 0 };
    const result = sector
      ? await api.PUT("/api/sectors/{sector_id}", { params: { path: { sector_id: sector.id } }, body })
      : await api.POST("/api/sectors", { body });
    setBusy(false);
    setError(done(result));
  };
  const shown = error && ["name", "sort_order"].includes(String(error.details?.field ?? "").split(".").pop() ?? "");
  return <Modal title={sector ? "Переименовать сектор" : "Новый сектор"} submitText={sector ? "Сохранить" : "Создать сектор"} onClose={onClose} onSubmit={() => void submit()} busy={busy} error={error} errorShown={shown}>
    <Field label="Название" name="name" error={error} hint="До 80 символов. Его видят оператор и мастер."><input value={name} onChange={(e) => setName(e.target.value)} placeholder="Сектор 5 · Покрасочный участок" /></Field>
    <Field label="Порядок в списке" name="sort_order" error={error} hint="Меньше — выше в списке и на пульте."><input type="number" value={order} onChange={(e) => setOrder(e.target.value)} /></Field>
  </Modal>;
}

function CameraForm({ camera, sectorId, sectors, onClose, done }: { camera?: Camera; sectorId?: number; sectors: Sector[]; onClose: () => void; done: Done }) {
  const [name, setName] = useState(camera?.name ?? "");
  const [description, setDescription] = useState(camera?.description ?? "");
  const [sector, setSector] = useState(camera?.sector_id ?? sectorId ?? sectors[0]?.id ?? 0);
  const [error, setError] = useState<ApiFailure>();
  const [busy, setBusy] = useState(false);
  const submit = async () => {
    setBusy(true);
    const body = { name: name.trim(), description: description.trim(), sector_id: sector };
    const result = camera
      ? await api.PATCH("/api/cameras/{camera_id}", { params: { path: { camera_id: camera.id } }, body })
      : await api.POST("/api/cameras", { body });
    setBusy(false);
    setError(done(result));
  };
  const shown = error && ["name", "description", "sector_id"].includes(String(error.details?.field ?? "").split(".").pop() ?? "");
  return <Modal title={camera ? "Изменить камеру" : "Новая камера"} submitText={camera ? "Сохранить" : "Добавить камеру"} onClose={onClose} onSubmit={() => void submit()} busy={busy} error={error} errorShown={shown}>
    <Field label="Название" name="name" error={error} hint="Например, «Камера 5.1 · Окрасочная камера»."><input value={name} onChange={(e) => setName(e.target.value)} /></Field>
    <Field label="Что видит камера" name="description" error={error}><textarea rows={3} value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Проход у линии, вид сверху" /></Field>
    <Field label="Сектор" name="sector_id" error={error} hint={camera ? "Перенос в другой сектор меняет его счётчики на пульте." : undefined}>
      <select value={sector} onChange={(e) => setSector(Number(e.target.value))}>{sectors.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}</select>
    </Field>
  </Modal>;
}

function DeleteForm({ dialog, onClose, done }: { dialog: Extract<Dialog, { kind: "delete-sector" | "delete-camera" }>; onClose: () => void; done: Done }) {
  const [error, setError] = useState<ApiFailure>();
  const [busy, setBusy] = useState(false);
  const remove = async () => {
    setBusy(true);
    const result = dialog.kind === "delete-sector"
      ? await api.DELETE("/api/sectors/{sector_id}", { params: { path: { sector_id: dialog.sector.id } } })
      : await api.DELETE("/api/cameras/{camera_id}", { params: { path: { camera_id: dialog.camera.id } } });
    setBusy(false);
    setError(done(result));
  };
  const name = dialog.kind === "delete-sector" ? dialog.sector.name : dialog.camera.name;
  return <Modal title={dialog.kind === "delete-sector" ? "Удалить сектор" : "Удалить камеру"} submitText="Удалить" danger onClose={onClose} onSubmit={() => void remove()} busy={busy} error={error}>
    <p className="adm-confirm">Удалить <b>«{name}»</b>?</p>
    {dialog.kind === "delete-sector"
      ? <p className="adm-muted">{dialog.cameras ? `В секторе ${dialog.cameras} камер. Сервер не удалит сектор, пока их не перенесут или не удалят.` : "Сектор пуст. События прошлых смен останутся в журнале."}</p>
      : <p className="adm-muted">Видео, зоны и калибровка камеры удаляются. События камеры остаются в журнале.</p>}
  </Modal>;
}

function Preview({ tile }: { tile?: CameraTile }) {
  const [failed, setFailed] = useState(false);
  if (!tile?.preview_url || failed) return <span className="adm-thumb adm-thumb-empty"><ImageOff {...I} /><small>нет кадра</small></span>;
  return <span className="adm-thumb"><img src={mediaUrl(tile.preview_url)} alt={`Кадр: ${tile.camera.name}`} loading="lazy" onError={() => setFailed(true)} /></span>;
}

function Source({ camera, tile }: { camera: Camera; tile?: CameraTile }) {
  const b = tile?.broadcast;
  if (b?.status === "playing") return <span className="adm-source adm-source-live"><Radio {...I} /><b>Эфир</b><em>повтор записи{b.loop ? " по кругу" : ""}</em></span>;
  if (camera.videos_count) return <span className="adm-source"><Layers {...I} /><b>{camera.videos_count} видео</b><em>{b ? "эфир остановлен" : "эфир не запущен"}</em></span>;
  return <span className="adm-source adm-source-none"><CameraIcon {...I} /><b>Нет источника</b><em>загрузите запись</em></span>;
}

async function loadViews(sectors: Sector[]) {
  const views = await Promise.all(sectors.map((s) => api.GET("/api/sectors/{sector_id}/view", { params: { path: { sector_id: s.id } } })));
  const failed = views.find((v) => v.error !== undefined);
  if (failed) return { error: failed.error, response: failed.response };
  return { data: views.map((v) => v.data!) };
}

export function AdminCamerasPage() {
  const fresh = useApi(() => api.GET("/api/admin/cameras"), []);
  // A reload after a save keeps the previous list on screen instead of a loading flash.
  const last = useRef(fresh.data);
  if (fresh.data) last.current = fresh.data;
  const view = { ...fresh, data: fresh.data ?? last.current };
  const sectors = [...(view.data?.sectors ?? [])].sort((a, b) => a.sort_order - b.sort_order || a.id - b.id);
  const cameras = view.data?.cameras ?? [];
  const liveFresh = useApi(() => fresh.data ? loadViews(fresh.data.sectors) : Promise.resolve({ data: undefined }), [fresh.data]);
  const lastLive = useRef(liveFresh.data);
  if (liveFresh.data) lastLive.current = liveFresh.data;
  const live = { ...liveFresh, data: liveFresh.data ?? lastLive.current };
  const [params, setParams] = useSearchParams();
  const [dialog, setDialog] = useState<Dialog>();
  const [orderError, setOrderError] = useState<ApiFailure>();
  const reloadView = view.reload;
  const reloadLive = live.reload;
  // State messages come in bursts (every camera of a looping broadcast): one batched reload at most every 1.5 s.
  const pending = useRef<ReturnType<typeof setTimeout>>();
  const latestReload = useRef(reloadLive);
  latestReload.current = reloadLive;
  useEffect(() => () => clearTimeout(pending.current), []);
  useWs(useCallback((m) => {
    if ((m.type !== "camera.state" && m.type !== "broadcast.state") || pending.current) return;
    pending.current = setTimeout(() => { pending.current = undefined; latestReload.current(); }, LIVE_THROTTLE_MS);
  }, []));

  const close = useCallback(() => setDialog(undefined), []);
  const done: Done = (result) => {
    const error = failure(result);
    if (!error) { setDialog(undefined); reloadView(); }
    return error;
  };

  if (view.error && !view.data) return <><PageHeading title="Камеры и секторы" /><ErrorNotice error={view.error} retry={view.reload} /></>;
  if (!view.data) return <><PageHeading title="Камеры и секторы" /><Loading text="Загружаем секторы и камеры" /></>;

  const tiles = new Map<number, CameraTile>((live.data ?? []).flatMap((v) => v.cameras.map((t) => [t.camera.id, t] as const)));
  const states = new Map<number, SectorState>((live.data ?? []).map((v) => [v.sector.sector_id, v.sector]));
  const picked = params.get("sector");
  const selected = picked === "all" ? undefined : sectors.find((s) => String(s.id) === picked) ?? sectors[0];
  const shown = cameras.filter((c) => !selected || c.sector_id === selected.id);
  const sectorName = (id: number) => sectors.find((s) => s.id === id)?.name ?? "—";
  const select = (id: number | "all") => setParams((p) => { p.set("sector", String(id)); return p; }, { replace: true });

  const move = async (index: number, delta: -1 | 1) => {
    const order = [...sectors];
    const [item] = order.splice(index, 1);
    order.splice(index + delta, 0, item);
    setOrderError(undefined);
    for (const [i, s] of order.entries()) {
      if (s.sort_order === i + 1) continue;
      const result = await api.PUT("/api/sectors/{sector_id}", { params: { path: { sector_id: s.id } }, body: { name: s.name, sort_order: i + 1 } });
      const error = failure(result);
      if (error) { setOrderError(error); break; }
    }
    reloadView();
  };

  return <div className="adm-page">
    <PageHeading title="Камеры и секторы" meta={<span className="adm-muted">{sectors.length} секторов · {cameras.length} камер{cameras.some((c) => c.is_demo) ? " · есть демо-данные" : ""}</span>}>
      <button className="button" onClick={() => setDialog({ kind: "sector" })}><FolderTree {...I} />Новый сектор</button>
      <button className="button button-primary" disabled={!sectors.length} title={sectors.length ? undefined : "Сначала создайте сектор"} onClick={() => setDialog({ kind: "camera", sectorId: selected?.id })}><Plus {...I} />Новая камера</button>
    </PageHeading>
    <div className="adm-split">
      <aside className="adm-tree" data-panel="Секторы" aria-label="Секторы">
        <button className={`adm-tree-row adm-tree-all ${!selected ? "selected" : ""}`} onClick={() => select("all")}>
          <Layers {...I} /><span className="adm-tree-name">Все камеры</span><span className="adm-count">{cameras.length}</span>
        </button>
        {!sectors.length && <div className="adm-empty-small"><b>Секторов нет</b><p>Создайте первый сектор, затем добавьте в него камеры.</p></div>}
        <ol>
          {sectors.map((s, i) => {
            const count = cameras.filter((c) => c.sector_id === s.id).length;
            const state = states.get(s.id);
            return <li key={s.id} className={`adm-tree-item ${selected?.id === s.id ? "selected" : ""}`}>
              <button className="adm-tree-row" onClick={() => select(s.id)} aria-current={selected?.id === s.id}>
                <FolderTree {...I} />
                <span className="adm-tree-name">{s.name}{s.is_demo && <i className="adm-demo">демо</i>}</span>
                <span className="adm-count" title="Камер в секторе">{count}</span>
              </button>
              <div className="adm-tree-meta">
                {state ? <StateBadge state={state.state} /> : <span className="adm-muted">состояние…</span>}
                {state && (state.open_red + state.open_yellow) > 0 && <span className="adm-open" title="Открытые события">открыто: {state.open_red ? <b className="adm-red">{state.open_red} кр.</b> : null} {state.open_yellow} жёлт.</span>}
              </div>
              <div className="adm-tree-tools">
                <button className="adm-icon" aria-label={`Выше: ${s.name}`} disabled={i === 0} onClick={() => void move(i, -1)}><ArrowUp {...I} /></button>
                <button className="adm-icon" aria-label={`Ниже: ${s.name}`} disabled={i === sectors.length - 1} onClick={() => void move(i, 1)}><ArrowDown {...I} /></button>
                <button className="adm-icon" aria-label={`Переименовать сектор ${s.name}`} onClick={() => setDialog({ kind: "sector", sector: s })}><Pencil {...I} /></button>
                <button className="adm-icon adm-icon-danger" aria-label={`Удалить сектор ${s.name}`} onClick={() => setDialog({ kind: "delete-sector", sector: s, cameras: count })}><Trash2 {...I} /></button>
              </div>
            </li>;
          })}
        </ol>
        {orderError && <div className="adm-pad"><ErrorNotice error={orderError} compact /></div>}
      </aside>
      <section className="adm-cams" data-panel={selected ? `Камеры · ${selected.name}` : "Камеры · все секторы"} aria-label="Камеры">
        <div className="adm-cams-bar">
          <span>{selected ? <>Сектор <b>{selected.name}</b>, порядок {selected.sort_order}</> : <>Все секторы</>}</span>
          <span className="adm-muted">{shown.length} камер · превью и состояние из сервера{live.loading ? " · обновляем…" : ""}</span>
        </div>
        {live.error && <div className="adm-pad"><ErrorNotice error={live.error} compact retry={live.reload} /></div>}
        {!shown.length ? <div className="adm-empty">
          <CameraIcon size={28} strokeWidth={1.5} />
          <h3>{selected ? "В секторе нет камер" : "Камер нет"}</h3>
          <p>Пока в секторе нет камер, пульт показывает его без наблюдения. Добавьте камеру и загрузите для неё запись.</p>
          {sectors.length > 0 && <button className="button button-primary" onClick={() => setDialog({ kind: "camera", sectorId: selected?.id })}><Plus {...I} />Добавить камеру</button>}
        </div> : <table className="adm-table">
          <thead><tr><th>Превью</th><th>Камера</th>{!selected && <th>Сектор</th>}<th>Состояние</th><th>Источник</th><th>Настройка</th><th aria-label="Действия" /></tr></thead>
          <tbody>{shown.map((c) => {
            const tile = tiles.get(c.id);
            return <tr key={c.id}>
              <td><Link to={`/admin/cameras/${c.id}`} aria-label={`Настроить ${c.name}`}><Preview tile={tile} /></Link></td>
              <td className="adm-cam-name"><Link to={`/admin/cameras/${c.id}`}>{c.name}</Link>{c.is_demo && <i className="adm-demo">демо</i>}<small>{c.description || "без описания"}</small><code>id {c.id}</code></td>
              {!selected && <td className="adm-muted">{sectorName(c.sector_id)}</td>}
              <td>{tile ? <StateBadge state={tile.state.state} reason={tile.state.reason_text} /> : <span className="adm-muted">—</span>}</td>
              <td><Source camera={c} tile={tile} /></td>
              <td className="adm-setup-cell"><span className={c.has_calibration ? "adm-ok" : "adm-muted"}>{c.has_calibration ? "Калибровка есть" : "Без калибровки"}</span><span className="adm-muted">Зон: {c.zones_count}</span></td>
              <td className="adm-row-tools">
                <Link className="button button-small" to={`/admin/cameras/${c.id}`}><Settings2 {...I} /><span>Настроить</span></Link>
                <button className="adm-icon" aria-label={`Изменить камеру ${c.name}`} onClick={() => setDialog({ kind: "camera", camera: c })}><Pencil {...I} /></button>
                <button className="adm-icon adm-icon-danger" aria-label={`Удалить камеру ${c.name}`} onClick={() => setDialog({ kind: "delete-camera", camera: c })}><Trash2 {...I} /></button>
              </td>
            </tr>;
          })}</tbody>
        </table>}
      </section>
    </div>
    {dialog?.kind === "sector" && <SectorForm sector={dialog.sector} nextOrder={(sectors.at(-1)?.sort_order ?? 0) + 1} onClose={close} done={done} />}
    {dialog?.kind === "camera" && <CameraForm camera={dialog.camera} sectorId={dialog.sectorId} sectors={sectors} onClose={close} done={done} />}
    {(dialog?.kind === "delete-sector" || dialog?.kind === "delete-camera") && <DeleteForm dialog={dialog} onClose={close} done={done} />}
  </div>;
}
