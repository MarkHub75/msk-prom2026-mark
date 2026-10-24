import { useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";

type CameraRule = components["schemas"]["CameraRule"];

// /ohs/rules (tech.md 8.14): cameras × scenarios with switches and the scenario status.
export function RulesScreen() {
  const view = useApi(() => api.GET("/api/ohs/rules"), []);
  const [error, setError] = useState<string>();
  const toggle = async (rule: CameraRule) => {
    setError(undefined);
    const result = await api.PUT("/api/cameras/{camera_id}/rules/{scenario}", {
      params: { path: { camera_id: rule.camera_id, scenario: rule.scenario } },
      body: { enabled: !rule.enabled, params: rule.params },
    });
    if (result.error) setError(result.error.message);
    view.reload();
  };
  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!view.data) return <p>Загрузка…</p>;
  const { scenarios, rows } = view.data;
  return (
    <section>
      <h1>Правила сценариев</h1>
      {error && <p role="alert">{error}</p>}
      {rows.length === 0 ? (
        <p>Камер нет</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Камера</th>
              {scenarios.map((s) => (
                <th key={s.id}>
                  {s.title}
                  {s.status !== "active" && <div>{s.status_text}</div>}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map(({ camera, rules }) => (
              <tr key={camera.id}>
                <td>
                  <Link to={`/admin/cameras/${camera.id}`}>{camera.name}</Link>
                </td>
                {rules.map((rule) => (
                  <td key={rule.scenario}>
                    <label>
                      <input
                        type="checkbox"
                        checked={rule.enabled}
                        disabled={rule.status !== "active"}
                        onChange={() => void toggle(rule)}
                      />{" "}
                      {rule.enabled ? "включён" : "выключен"}
                    </label>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
