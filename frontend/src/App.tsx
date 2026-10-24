import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { StubNotice } from "./components/StubNotice";
import { NAV, menuFor } from "./nav";
import { useRole } from "./roles";

export function App() {
  const [role] = useRole();
  return (
    <AppShell>
      <Routes>
        {NAV.map((item) => (
          <Route
            key={item.path}
            path={item.path}
            element={item.screen ? <item.screen /> : <StubNotice slice={item.slice} title={item.title} />}
          />
        ))}
        <Route path="*" element={<Navigate to={menuFor(role)[0]?.path ?? "/operator"} replace />} />
      </Routes>
    </AppShell>
  );
}
