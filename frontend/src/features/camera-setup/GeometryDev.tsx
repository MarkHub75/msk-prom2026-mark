// Temporary dev route of the geometry stream: the three tabs in a row. Removed on merge.
import { useState } from "react";
import { useParams } from "react-router-dom";
import { CalibrationTab } from "./CalibrationTab";
import { CameraRulesTab } from "./CameraRulesTab";
import { ZonesTab } from "./ZonesTab";

const TABS = [["zones", "Зоны"], ["calibration", "Калибровка"], ["rules", "Правила"]] as const;

export function GeometryDev() {
  const cameraId = Number(useParams().cameraId);
  const [tab, setTab] = useState<(typeof TABS)[number][0]>(() => (new URLSearchParams(location.search).get("tab") as "zones") || "zones");
  return (
    <div className="geo-dev">
      <nav className="geo-dev-tabs">
        {TABS.map(([id, title]) => <button key={id} type="button" className={tab === id ? "is-active" : ""} onClick={() => setTab(id)}>{title}</button>)}
      </nav>
      {tab === "zones" && <ZonesTab cameraId={cameraId} />}
      {tab === "calibration" && <CalibrationTab cameraId={cameraId} />}
      {tab === "rules" && <CameraRulesTab cameraId={cameraId} />}
    </div>
  );
}
