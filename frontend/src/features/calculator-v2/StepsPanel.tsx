import type { CSSProperties } from "react";
import type { ResultV2, StepV2 } from "../../api/calcV2";
import { Badge, Panel } from "../../components/ui";
import { boards, num, one, rub } from "./format";

// К6 «Ступеньки»: the same cameras, catalogue and CPU/slot limits, five ways to count the load.
// The headline is the server's own numbers: the naive step against the last step that is available.
const UNIT = "эквивалентных запусков опорной модели в секунду";

// К10 п.7: the tracker step is «недоступен» while defaults.v2.features.tracker.available=false, whatever a step says.
const usable = (s: StepV2, tracker: boolean) => s.available && (s.id !== "tracker" || tracker);

function lastAvailable(steps: StepV2[], tracker: boolean): StepV2 | undefined {
  return [...steps].reverse().find(s => usable(s, tracker) && s.chips !== null);
}

export function StepsPanel({ result, trackerAvailable }: { result: ResultV2; trackerAvailable: boolean }) {
  const steps = result.steps;
  const first = steps.find(s => s.id === "naive");
  const best = lastAvailable(steps, trackerAvailable);
  const max = Math.max(1, ...steps.map(s => s.chips ?? 0));
  const input = result.resolved.input.load;
  const cameras = result.resolved.total.cameras;
  const headline = first?.chips != null && best?.chips != null ? <><b className="mono">{first.chips}</b><span className="cv2-arrow" aria-hidden>→</span><b className="mono">{boards(best.chips)}</b></> : null;

  return <Panel title="Сколько плат LinQ нужно" data-testid="steps" tools={<Badge tone="grey">модель нагрузки, не замер</Badge>}>
    <div className="cv2-steps-head">
      {headline ? <p className="cv2-steps-headline" aria-label={`${first?.chips} → ${best?.chips} плат`}>{headline}</p> : <p className="cv2-steps-headline is-none">Число плат не определено</p>}
      <p className="cv2-steps-sub">{cameras ? `${cameras} камер, одинаковые камеры и каталог на каждой ступени.` : "Камер в расчёте нет."} Ступенька может и не уменьшить число плат; стоимость — только оборудование, без пусконаладки.</p>
    </div>
    <ol className="cv2-steps">
      {steps.map((s, i) => {
        const on = usable(s, trackerAvailable);
        const prev = i > 0 ? steps[i - 1].chips : null;
        const delta = on && s.chips !== null && prev !== null ? s.chips - prev : null;
        const style = { "--share": !on || s.chips === null ? 0 : s.chips / max } as CSSProperties;
        return <li key={s.id} className={`cv2-step${on ? "" : " is-off"}${s === best ? " is-best" : ""}`} data-step={s.id} style={style}>
          <div className="cv2-step-bar" aria-hidden><i /></div>
          <div className="cv2-step-body">
            <span className="cv2-step-n mono">{on ? num(s.chips) : "—"}</span>
            <b className="cv2-step-title">{s.title}</b>
            {on
              ? <small className="mono">{s.servers === null ? "серверы: нет данных" : `серверов ${s.servers}`} · {rub(s.equipment_capex_rub)}</small>
              : <small><Badge tone="grey">недоступен</Badge></small>}
            {delta !== null && delta !== 0 && <small className="cv2-step-delta mono">{delta < 0 ? "−" : "+"}{Math.abs(delta)} к предыдущей</small>}
            <small className="cv2-step-reason">{s.reason}</small>
          </div>
        </li>;
      })}
    </ol>
    <ul className="cv2-captions">
      <li><b>Модель нагрузки, не замер.</b> Нагрузка в {UNIT}: пик {num(result.load.peak_units_s)}, всплеск {num(result.load.surge_units_s)}, активных камер в пике (p95) {result.load.active_p95} из {result.load.cameras}.</li>
      <li><b>Ёмкость платы — заявление производителя.</b> {one(input.reference_chip_fps)} кадр/с на чип × запас {one(input.capacity_derate)} = {num(result.load.effective_chip_units_s)} ед./с; это не замер Argus и не гарантия для любых моделей.</li>
      <li><b>«Как считалось раньше»</b> делит всю нагрузку на пропускную способность общей очереди площадки: это сравнение старого подхода, а не паспорт чипа.</li>
      <li><b>Трекер</b> {steps.some(s => s.id === "tracker" && usable(s, trackerAvailable)) ? "учтён: сохранность событий подтверждена отчётом." : "недоступен, пока нет отчёта о сохранности событий; ступень не изображается достигнутой."}</li>
    </ul>
  </Panel>;
}
