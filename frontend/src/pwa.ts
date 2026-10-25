import { useCallback, useEffect, useState, useSyncExternalStore } from "react";

/** Installable app: service worker, the install prompt, system notifications (public/sw.js). */

type InstallPrompt = Event & { prompt: () => Promise<void>; userChoice: Promise<{ outcome: "accepted" | "dismissed" }> };
let deferred: InstallPrompt | undefined;
const listeners = new Set<() => void>();
const emit = () => listeners.forEach(listener => listener());
const subscribe = (listener: () => void) => { listeners.add(listener); return () => { listeners.delete(listener); }; };

if (typeof window !== "undefined") {
  // Chrome fires it once, early: keep it until the profile sheet offers «Установить на телефон».
  window.addEventListener("beforeinstallprompt", event => { event.preventDefault(); deferred = event as InstallPrompt; emit(); });
  window.addEventListener("appinstalled", () => { deferred = undefined; emit(); });
}

/** Production only: in dev the worker would cache Vite modules and fight HMR. */
export function registerServiceWorker() {
  if (!import.meta.env.PROD || typeof navigator === "undefined" || !("serviceWorker" in navigator)) return;
  window.addEventListener("load", () => { navigator.serviceWorker.register("/sw.js").catch(() => undefined); });
}

export const isStandalone = () => Boolean(window.matchMedia?.("(display-mode: standalone)")?.matches || (navigator as Navigator & { standalone?: boolean }).standalone);
const isIos = () => /iphone|ipad|ipod/i.test(navigator.userAgent) || (/macintosh/i.test(navigator.userAgent) && navigator.maxTouchPoints > 1);

export type InstallState = "installed" | "available" | "ios" | "unavailable";
function installState(): InstallState {
  if (isStandalone()) return "installed";
  if (deferred) return "available";
  return isIos() ? "ios" : "unavailable";
}
export function useInstall() {
  const state = useSyncExternalStore(subscribe, installState, () => "unavailable" as const);
  const install = useCallback(async () => {
    const prompt = deferred; if (!prompt) return;
    deferred = undefined;
    try { await prompt.prompt(); await prompt.userChoice; } catch { /* the browser refused to show it */ }
    emit();
  }, []);
  return { state, install };
}

/** Vibration only after the first tap: before it Chrome blocks the call and logs an error on every alarm. */
export function vibrate(pattern: number | number[]) {
  if (typeof navigator === "undefined" || typeof navigator.vibrate !== "function") return;
  const activation = (navigator as Navigator & { userActivation?: { hasBeenActive: boolean } }).userActivation;
  if (activation && !activation.hasBeenActive) return;
  navigator.vibrate(pattern);
}

export type NotifyPermission = NotificationPermission | "unsupported";
const permission = (): NotifyPermission => typeof Notification === "undefined" ? "unsupported" : Notification.permission;
/** Asks once from a tap (sound toggle, profile sheet); a later answer is the browser's setting. */
export async function askNotifications(): Promise<NotifyPermission> {
  if (permission() !== "default") return permission();
  try { return await Notification.requestPermission(); } catch { return permission(); }
}
export function useNotifyPermission() {
  const [state, setState] = useState(permission);
  useEffect(() => { const sync = () => setState(permission()); document.addEventListener("visibilitychange", sync); return () => document.removeEventListener("visibilitychange", sync); }, []);
  return { state, ask: async () => setState(await askNotifications()) };
}

/**
 * System notification with sound and vibration of the OS. Through the service worker registration:
 * on Android Chrome `new Notification()` throws, only `registration.showNotification` works.
 * The same tag replaces the previous notification of the event and alerts again (renotify).
 */
export async function systemNotify(title: string, body: string, { tag, url, urgent = false }: { tag: string; url: string; urgent?: boolean }) {
  if (permission() !== "granted") return false;
  const options: NotificationOptions & { vibrate?: number[]; renotify?: boolean } = {
    body, tag, data: { url }, icon: "/icons/icon-192.png", badge: "/icons/badge-96.png", lang: "ru",
    renotify: true, requireInteraction: urgent, silent: false, vibrate: urgent ? [300, 120, 300, 120, 300] : [200, 100, 200],
  };
  try {
    const registration = await navigator.serviceWorker?.getRegistration();
    if (registration) { await registration.showNotification(title, options); return true; }
  } catch { /* no worker (dev, old browser): try the page constructor */ }
  try { new Notification(title, options); return true; } catch { return false; }
}
