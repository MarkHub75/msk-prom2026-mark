import { useSyncExternalStore } from "react";
import type { components } from "./api/schema";

export type Role = components["schemas"]["RoleMeta"]["id"];

// Order of the switcher; titles come from /api/meta.
export const ROLES: Role[] = ["operator", "master", "ohs", "management", "admin"];
const KEY = "safewatch.role";
const listeners = new Set<() => void>();

function load(): Role {
  try {
    const saved = localStorage.getItem(KEY);
    if (saved && (ROLES as string[]).includes(saved)) return saved as Role;
  } catch {
    // storage blocked (private window): the default role is enough
  }
  return "operator";
}

let current: Role = load();

export function getRole(): Role {
  return current;
}

export function setRole(role: Role): void {
  current = role;
  try {
    localStorage.setItem(KEY, role);
  } catch {
    // storage blocked: the role lives until reload
  }
  listeners.forEach((listener) => listener());
}

function subscribe(listener: () => void): () => void {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useRole(): [Role, (role: Role) => void] {
  return [useSyncExternalStore(subscribe, getRole), setRole];
}
