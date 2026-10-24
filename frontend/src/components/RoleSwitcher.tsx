import { ROLES, useRole, type Role } from "../roles";
import { useMeta } from "./AppShell";

export function RoleSwitcher() {
  const [role, setRole] = useRole();
  const meta = useMeta();
  const title = (id: Role) => meta?.roles.find((r) => r.id === id)?.title ?? id;
  return (
    <label>
      Роль{" "}
      <select aria-label="Роль" value={role} onChange={(e) => setRole(e.target.value as Role)}>
        {ROLES.map((id) => (
          <option key={id} value={id}>
            {title(id)}
          </option>
        ))}
      </select>
    </label>
  );
}
