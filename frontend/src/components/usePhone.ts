import { useSyncExternalStore } from "react";

/** Phone layout of the operator and master apps (tech.md 8.14: works from 360 px). */
export const PHONE_QUERY = "(max-width: 760px)";

function media() { return typeof window !== "undefined" && typeof window.matchMedia === "function" ? window.matchMedia(PHONE_QUERY) : undefined; }
function subscribe(listener: () => void) {
  const query = media();
  query?.addEventListener("change", listener);
  return () => query?.removeEventListener("change", listener);
}

export function usePhone() { return useSyncExternalStore(subscribe, () => media()?.matches ?? false, () => false); }
