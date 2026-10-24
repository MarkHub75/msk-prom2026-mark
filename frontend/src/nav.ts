import type { ComponentType } from "react";
import type { Role } from "./roles";
import { CameraSetup } from "./screens/admin/CameraSetup";
import { CamerasScreen } from "./screens/admin/CamerasScreen";
import { SystemScreen } from "./screens/admin/SystemScreen";
import { EventScreen } from "./screens/events/EventScreen";
import { MasterEvent } from "./screens/master/MasterEvent";
import { MasterInbox } from "./screens/master/MasterInbox";
import { ShiftSummaryScreen } from "./screens/master/ShiftSummaryScreen";
import { CameraScreen } from "./screens/operator/CameraScreen";
import { OperatorDashboard } from "./screens/operator/OperatorDashboard";
import { SectorScreen } from "./screens/operator/SectorScreen";
import { ManagementDashboard } from "./screens/management/ManagementDashboard";
import { Journal } from "./screens/ohs/Journal";
import { OhsStats } from "./screens/ohs/OhsStats";
import { RulesScreen } from "./screens/ohs/RulesScreen";

export interface NavItem {
  path: string;
  title: string;
  roles: Role[];
  slice: number;
  menu: boolean; // shown in the navigation of its roles; routes with ids are reached by links
  screen?: ComponentType; // the built screen; without it the route renders StubNotice
}

// Routes of tech.md 8.14; a route of an unbuilt slice has no screen and renders StubNotice.
export const NAV: NavItem[] = [
  { path: "/operator", title: "Секторы", roles: ["operator"], slice: 6, menu: true, screen: OperatorDashboard },
  { path: "/operator/sectors/:sectorId", title: "Сектор", roles: ["operator"], slice: 6, menu: false, screen: SectorScreen },
  { path: "/operator/cameras/:cameraId", title: "Камера", roles: ["operator"], slice: 6, menu: false, screen: CameraScreen },
  { path: "/events/:eventId", title: "Событие", roles: ["operator", "master", "ohs", "management", "admin"], slice: 7, menu: false, screen: EventScreen },
  { path: "/master", title: "Мои события", roles: ["master"], slice: 8, menu: true, screen: MasterInbox },
  { path: "/master/events/:eventId", title: "Событие", roles: ["master"], slice: 8, menu: false, screen: MasterEvent },
  { path: "/master/shift", title: "Смена", roles: ["master"], slice: 8, menu: true, screen: ShiftSummaryScreen },
  { path: "/ohs/journal", title: "Журнал", roles: ["ohs"], slice: 12, menu: true, screen: Journal },
  { path: "/ohs/rules", title: "Правила", roles: ["ohs"], slice: 9, menu: true, screen: RulesScreen },
  { path: "/ohs/stats", title: "Статистика", roles: ["ohs"], slice: 13, menu: true, screen: OhsStats },
  { path: "/management", title: "Тренды", roles: ["management"], slice: 13, menu: true, screen: ManagementDashboard },
  { path: "/admin/cameras", title: "Камеры", roles: ["admin"], slice: 1, menu: true, screen: CamerasScreen },
  { path: "/admin/cameras/:cameraId", title: "Настройка камеры", roles: ["admin", "ohs"], slice: 2, menu: false, screen: CameraSetup },
  { path: "/admin/system", title: "Система", roles: ["admin"], slice: 3, menu: true, screen: SystemScreen },
];

export function menuFor(role: Role): NavItem[] {
  return NAV.filter((item) => item.menu && item.roles.includes(role));
}
