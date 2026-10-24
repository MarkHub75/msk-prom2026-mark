import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { StubNotice } from "./components/StubNotice";
import { menuFor } from "./nav";
import { OperatorPage, SectorPage, CameraPage } from "./features/Operator";
import { IncidentPage } from "./features/Incident";
import { MasterPage, ShiftPage } from "./features/Master";
import { JournalPage } from "./features/Journal";
import { ReportPage } from "./features/Report";
import { StatsPage } from "./features/Stats";
import { AdminCamerasPage } from "./features/AdminCameras";
import { CameraSetupPage } from "./features/CameraSetup";
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
        <Route path="/ohs/journal" element={<JournalPage />} />
        <Route path="/ohs/report" element={<ReportPage />} />
        <Route path="/ohs/rules" element={<StubNotice slice={9} title="Правила наблюдения" />} />
        <Route path="/ohs/stats" element={<StatsPage />} />
        <Route path="/management" element={<StatsPage management />} />
        <Route path="/admin/cameras" element={<AdminCamerasPage />} />
        <Route path="/admin/cameras/:cameraId" element={<CameraSetupPage />} />
        <Route path="/admin/system" element={<StubNotice slice={3} title="Состояние системы" />} />
        <Route path="*" element={<Navigate to={menuFor(role)[0]?.path ?? "/operator"} replace />} />
      </Routes>
    </AppShell>
  );
}
