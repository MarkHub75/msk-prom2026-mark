import type { components } from "../api/schema";

type Sound = components["schemas"]["Notification"]["sound"];

let context: AudioContext | undefined;

function audio(): AudioContext | undefined {
  if (typeof AudioContext === "undefined") return undefined;
  context ??= new AudioContext();
  return context;
}

// The browser keeps audio suspended until the first click: the header offers «Включить звук».
export function soundBlocked(): boolean {
  return audio()?.state === "suspended";
}

export function unlockSound(): void {
  void audio()?.resume();
}

// WebAudio without files (tech.md 2): a chime is one short tone, a siren sweeps until stopped.
// Returns the function that stops the sound.
export function playSound(kind: Sound): () => void {
  const ctx = audio();
  if (!ctx || kind === "none") return () => undefined;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  gain.gain.value = 0.2;
  osc.connect(gain).connect(ctx.destination);
  const t = ctx.currentTime;
  if (kind === "chime") {
    osc.frequency.setValueAtTime(880, t);
    osc.start(t);
    osc.stop(t + 0.4);
    return () => undefined;
  }
  for (let i = 0; i < 600; i += 1) {
    osc.frequency.setValueAtTime(i % 2 ? 600 : 1000, t + i * 0.5); // up to 5 minutes of siren
  }
  osc.start(t);
  return () => osc.stop();
}
