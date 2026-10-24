// REST aliases are derived only from generated OpenAPI types.
import type { components } from "./schema";
import type { Readable } from "openapi-typescript-helpers";

// openapi-fetch 0.17 derives Readable responses (including array/tuple treatment).
// Share that exact derived view so API results and component props stay compatible.
export type Schemas = {[K in keyof components["schemas"]]: Readable<components["schemas"][K]>};
export type Meta = Schemas["Meta"];
export type Role = Schemas["RoleMeta"]["id"];
export type ApiError = Schemas["ApiError"];
export type OperatorDashboard = Schemas["OperatorDashboard"];
export type Sector = Schemas["Sector"];
export type SectorState = Schemas["SectorState"];
export type SectorView = Schemas["SectorView"];
export type Camera = Schemas["Camera"];
export type CameraState = Schemas["CameraState"];
export type CameraTile = Schemas["CameraTile"];
export type CameraLiveView = Schemas["CameraLiveView"];
export type EventSummary = Schemas["EventSummary"];
export type EventDetail = Schemas["EventDetail"];
export type EventAction = Schemas["EventAction"];
export type ActionIn = Schemas["ActionIn"];
export type HumanAction = ActionIn["action"];
export type MasterInbox = Schemas["MasterInbox"];
export type Evidence = Schemas["Evidence"];
export type HudFrame = Schemas["HudFrame"];
export type HudObject = Schemas["HudObject"];
export type TracksWindow = Schemas["TracksWindow"];
export type Broadcast = Schemas["Broadcast"];
export type Video = Schemas["Video"];
export type DemoPack = Schemas["DemoPack"];
export type Analysis = Schemas["Analysis"];
export type Zone = Schemas["Zone"];
export type Calibration = Schemas["Calibration"];
export type Episode = Schemas["Episode"];
export type Provenance = Schemas["Provenance"];
export type BackendStatus = Schemas["BackendStatus"];
export type Job = Schemas["Job"];
export type OhsStats = Schemas["OhsStats"];
export type CountRow = Schemas["CountRow"];
export type DayRow = Schemas["DayRow"];
// v5 (contract 1.1.0, tech.md 6.11.2)
export type CalcAssumption = Schemas["CalcAssumption"];
export type CalculatorDefaults = Schemas["CalculatorDefaults"];
export type RolloutIn = Schemas["RolloutIn"];
export type RolloutResult = Schemas["RolloutResult"];
export type TierResult = Schemas["TierResult"];
export type ScaleIn = Schemas["ScaleIn"];
export type ScaleResult = Schemas["ScaleResult"];
export type DatasetView = Schemas["DatasetView"];
export type DatasetItem = Schemas["DatasetItem"];
export type IdentityIn = Schemas["IdentityIn"];
export type PeopleStats = Schemas["PeopleStats"];
export type CameraPassport = Schemas["CameraPassport"];
export type PassportScenario = Schemas["PassportScenario"];

// These two payloads are present only in contract/ws.schema.json ($defs).
// Their fields and enums match the real 1.0.0 schema; REST payloads reuse aliases above.
export interface WsHello { server_now: string; contract: string; role: Role }
export interface Notification {
  id: string;
  event_id: number;
  level: EventSummary["level"];
  text: string;
  audience: Role[];
  sound: "siren" | "chime" | "none";
  takeover: boolean;
}
export type WsPayloadMap = {
  hello: WsHello;
  "event.created": EventSummary;
  "event.updated": EventSummary;
  "event.escalated": EventSummary;
  notification: Notification;
  "camera.state": CameraState;
  "sector.state": SectorState;
  "job.progress": Job;
  "broadcast.state": Broadcast;
  "backend.status": BackendStatus;
};
export type WsMessage = { [K in keyof WsPayloadMap]: {type: K; at: string; data: WsPayloadMap[K]} }[keyof WsPayloadMap];
