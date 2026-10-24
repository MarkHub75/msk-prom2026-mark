import { useState } from "react";
import { api, apiError } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { DataTable } from "../../components/DataTable";
import { ConfirmDialog, FormField, FormModal } from "../../components/Form";

type Sector = components["schemas"]["Sector"];
type Camera = components["schemas"]["Camera"];

type Dialog =
  | { kind: "sector"; sector?: Sector }
  | { kind: "camera"; camera?: Camera }
  | { kind: "delete-sector"; sector: Sector }
  | { kind: "delete-camera"; camera: Camera };

type Result = { error?: unknown };

function SectorForm({ sector, onDone }: { sector?: Sector; onDone: (r?: Result) => Promise<string | undefined> }) {
  const [name, setName] = useState(sector?.name ?? "");
  const [order, setOrder] = useState(String(sector?.sort_order ?? 0));
  const [error, setError] = useState<string>();
  const submit = async () => {
    const body = { name, sort_order: Number(order) || 0 };
    const result = sector
      ? await api.PUT("/api/sectors/{sector_id}", { params: { path: { sector_id: sector.id } }, body })
      : await api.POST("/api/sectors", { body });
    setError(await onDone(result));
  };
  return (
    <FormModal
      title={sector ? "Переименовать сектор" : "Новый сектор"}
      error={error}
      submitText="Сохранить"
      onSubmit={() => void submit()}
      onClose={() => void onDone()}
    >
      <FormField label="Название">
        <input value={name} onChange={(e) => setName(e.target.value)} />
      </FormField>
      <FormField label="Порядок">
        <input type="number" value={order} onChange={(e) => setOrder(e.target.value)} />
      </FormField>
    </FormModal>
  );
}

function CameraForm({
  camera,
  sectors,
  onDone,
}: {
  camera?: Camera;
  sectors: Sector[];
  onDone: (r?: Result) => Promise<string | undefined>;
}) {
  const [name, setName] = useState(camera?.name ?? "");
  const [description, setDescription] = useState(camera?.description ?? "");
  const [sectorId, setSectorId] = useState(camera?.sector_id ?? sectors[0]?.id ?? 0);
  const [error, setError] = useState<string>();
  const submit = async () => {
    const body = { name, description, sector_id: sectorId };
    const result = camera
      ? await api.PATCH("/api/cameras/{camera_id}", { params: { path: { camera_id: camera.id } }, body })
      : await api.POST("/api/cameras", { body });
    setError(await onDone(result));
  };
  return (
    <FormModal
      title={camera ? "Изменить камеру" : "Новая камера"}
      error={error}
      submitText="Сохранить"
      onSubmit={() => void submit()}
      onClose={() => void onDone()}
    >
      <FormField label="Название">
        <input value={name} onChange={(e) => setName(e.target.value)} />
      </FormField>
      <FormField label="Описание">
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} />
      </FormField>
      <FormField label="Сектор">
        <select value={sectorId} onChange={(e) => setSectorId(Number(e.target.value))}>
          {sectors.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
      </FormField>
    </FormModal>
  );
}

function DeleteDialog({ dialog, onDone }: { dialog: Dialog; onDone: (r?: Result) => Promise<string | undefined> }) {
  const [error, setError] = useState<string>();
  if (dialog.kind === "delete-sector") {
    const remove = async () =>
      setError(await onDone(await api.DELETE("/api/sectors/{sector_id}", { params: { path: { sector_id: dialog.sector.id } } })));
    return (
      <ConfirmDialog
        text={`Удалить сектор «${dialog.sector.name}»?`}
        error={error}
        onConfirm={() => void remove()}
        onClose={() => void onDone()}
      />
    );
  }
  if (dialog.kind !== "delete-camera") return null;
  const remove = async () =>
    setError(await onDone(await api.DELETE("/api/cameras/{camera_id}", { params: { path: { camera_id: dialog.camera.id } } })));
  return (
    <ConfirmDialog
      text={`Удалить камеру «${dialog.camera.name}»? События камеры останутся в журнале.`}
      error={error}
      onConfirm={() => void remove()}
      onClose={() => void onDone()}
    />
  );
}

export function CamerasScreen() {
  const view = useApi(() => api.GET("/api/admin/cameras"), []);
  const [dialog, setDialog] = useState<Dialog>();

  // Closes the dialog and reloads on success; returns the API error text for the form otherwise.
  const done = async (result?: Result): Promise<string | undefined> => {
    if (result?.error !== undefined) return apiError(result.error).message;
    setDialog(undefined);
    if (result) view.reload();
    return undefined;
  };

  if (view.loading && !view.data) return <p>Загрузка…</p>;
  if (view.error) return <p role="alert">{view.error.message}</p>;
  const sectors = view.data?.sectors ?? [];
  const cameras = view.data?.cameras ?? [];
  const sectorName = (id: number) => sectors.find((s) => s.id === id)?.name ?? "—";

  return (
    <section>
      <h1>Секторы и камеры</h1>
      <h2>Секторы</h2>
      <button type="button" onClick={() => setDialog({ kind: "sector" })}>
        Новый сектор
      </button>
      <DataTable
        empty="Секторов нет"
        rows={sectors}
        columns={[
          { title: "Название", cell: (s) => s.name },
          { title: "Порядок", cell: (s) => s.sort_order },
          { title: "Камер", cell: (s) => cameras.filter((c) => c.sector_id === s.id).length },
          {
            title: "Действия",
            cell: (s) => (
              <>
                <button type="button" onClick={() => setDialog({ kind: "sector", sector: s })}>
                  Переименовать
                </button>
                <button type="button" onClick={() => setDialog({ kind: "delete-sector", sector: s })}>
                  Удалить
                </button>
              </>
            ),
          },
        ]}
      />
      <h2>Камеры</h2>
      <button type="button" disabled={sectors.length === 0} onClick={() => setDialog({ kind: "camera" })}>
        Новая камера
      </button>
      <DataTable
        empty="Камер нет"
        rows={cameras}
        columns={[
          { title: "Название", cell: (c) => c.name },
          { title: "Сектор", cell: (c) => sectorName(c.sector_id) },
          { title: "Описание", cell: (c) => c.description },
          { title: "Калибровка", cell: (c) => (c.has_calibration ? "есть" : "нет") },
          { title: "Зон", cell: (c) => c.zones_count },
          { title: "Видео", cell: (c) => c.videos_count },
          {
            title: "Действия",
            cell: (c) => (
              <>
                <button type="button" onClick={() => setDialog({ kind: "camera", camera: c })}>
                  Изменить
                </button>
                <button type="button" onClick={() => setDialog({ kind: "delete-camera", camera: c })}>
                  Удалить
                </button>
              </>
            ),
          },
        ]}
      />
      {dialog?.kind === "sector" && <SectorForm sector={dialog.sector} onDone={done} />}
      {dialog?.kind === "camera" && <CameraForm camera={dialog.camera} sectors={sectors} onDone={done} />}
      {dialog && dialog.kind.startsWith("delete") && <DeleteDialog dialog={dialog} onDone={done} />}
    </section>
  );
}
