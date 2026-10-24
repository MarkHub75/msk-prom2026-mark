import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { StubNotice } from "./components/StubNotice";
import { menuFor } from "./nav";
import { OperatorPage, SectorPage, CameraPage } from "./features/Operator";
import { IncidentPage } from "./features/Incident";
import { MasterPage, ShiftPage } from "./features/Master";
import { useRole } from "./roles";

export function App() {
  const [role] = useRole();
  return (
    <AppShell>
      <Routes>
        <Route path="/operator" element={<OperatorPage />} />
        <Route path="/operator/sectors/:sectorId" element={<SectorPage />} />
        <Route path="/operator/cameras/:cameraId" element={<CameraPage />} />
        <Route path="/events/:eventId" element={<IncidentPage />} />
        <Route path="/master" element={<MasterPage />} />
        <Route path="/master/events/:eventId" element={<IncidentPage master />} />
        <Route path="/master/shift" element={<ShiftPage />} />
        <Route path="/ohs/journal" element={<StubNotice slice={12} title="Журнал охраны труда" />} />
        <Route path="/ohs/rules" element={<StubNotice slice={9} title="Правила наблюдения" />} />
        <Route path="/ohs/stats" element={<StubNotice slice={13} title="Статистика охраны труда" />} />
        <Route path="/management" element={<StubNotice slice={13} title="Производственные тренды" />} />
        <Route path="/admin/cameras" element={<StubNotice slice={1} title="Управление камерами" />} />
        <Route path="/admin/cameras/:cameraId" element={<StubNotice slice={2} title="Настройка камеры" />} />
        <Route path="/admin/system" element={<StubNotice slice={3} title="Состояние системы" />} />
        <Route path="*" element={<Navigate to={menuFor(role)[0]?.path ?? "/operator"} replace />} />
      </Routes>
    </AppShell>
  );
}
