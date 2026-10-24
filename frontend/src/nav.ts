import type { Role } from "./roles";

export interface NavItem {
  path: string;
  title: string;
  roles: Role[];
  slice: number;
  menu: boolean; // shown in the navigation of its roles; routes with ids are reached by links
}

// Routes of tech.md 8.14; a route of an unbuilt slice renders StubNotice.
export const NAV: NavItem[] = [
  { path: "/operator", title: "Диспетчерская", roles: ["operator"], slice: 6, menu: true },
  { path: "/operator/sectors/:sectorId", title: "Сектор", roles: ["operator"], slice: 6, menu: false },
  { path: "/operator/cameras/:cameraId", title: "Камера", roles: ["operator"], slice: 6, menu: false },
  { path: "/events/:eventId", title: "Событие", roles: ["operator", "master", "ohs", "management", "admin"], slice: 7, menu: false },
  { path: "/master", title: "Мои события", roles: ["master"], slice: 8, menu: true },
  { path: "/master/events/:eventId", title: "Событие", roles: ["master"], slice: 8, menu: false },
  { path: "/master/shift", title: "Смена", roles: ["master"], slice: 8, menu: true },
  { path: "/ohs/journal", title: "Журнал", roles: ["ohs"], slice: 12, menu: true },
  { path: "/ohs/rules", title: "Правила", roles: ["ohs"], slice: 9, menu: true },
  { path: "/ohs/stats", title: "Аналитика", roles: ["ohs"], slice: 13, menu: true },
  { path: "/management", title: "Аналитика", roles: ["management"], slice: 13, menu: true },
  { path: "/admin/cameras", title: "Камеры", roles: ["admin"], slice: 1, menu: true },
  { path: "/admin/cameras/:cameraId", title: "Настройка камеры", roles: ["admin", "ohs"], slice: 2, menu: false },
  { path: "/admin/system", title: "Система", roles: ["admin"], slice: 3, menu: true },
  { path: "/admin/demo", title: "Демо", roles: ["admin"], slice: 6, menu: true },
];

export function menuFor(role: Role): NavItem[] {
  return NAV.filter((item) => item.menu && item.roles.includes(role));
}
