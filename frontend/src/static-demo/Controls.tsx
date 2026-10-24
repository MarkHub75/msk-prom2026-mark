import { useState } from "react";
import { PRODUCT } from "../brand";
import { Button } from "../components/ui";
import { nextStep, resetDemo } from "./index.mjs";
import "./demo.css";

export function DemoControls() {
  const [step, setStep] = useState(0);
  const [message, setMessage] = useState("Шаг 1: жёлтое событие — бег. Шаг 2: красное — падение.");
  const advance = () => {
    const result = nextStep();
    if (result.published) {
      setStep(value => value + 1);
      setMessage(result.published.level === "yellow" ? "Жёлтое событие опубликовано. Можно подтвердить или перейти к падению." : "Красное событие опубликовано. Подтвердите его и переключитесь на роль «Мастер».");
    }
  };
  const reset = () => {
    resetDemo(); setStep(0);
    setMessage("Мир восстановлен. Следующий шаг опубликует жёлтое событие.");
  };
  return <>
    <div className="static-demo-banner" role="note"><strong>{PRODUCT}</strong><span>Статическое демо: данные и кадры синтетические, сервера нет</span></div>
    <aside className="static-demo-director" aria-label="Режиссёр демо">
      <p role="status" aria-live="polite">{message}</p>
      <div><Button variant="primary" size="sm" icon="play" disabled={step >= 2} onClick={advance}>Следующий шаг демо</Button><Button size="sm" icon="refresh" onClick={reset}>Сбросить</Button></div>
    </aside>
  </>;
}
