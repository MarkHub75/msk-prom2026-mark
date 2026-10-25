import { PRODUCT } from "../brand";
import type { CalcAssumption, RolloutIn, RolloutResult, ScaleIn, ScaleResult, TierResult } from "../api/types";

// Shown only while the server answers 501: the demo plant of calculator_defaults and the assumptions of
// config `calculator.assumptions` (tech.md 6.11.8), counted by the formulas of tech.md 8.25.
// The screen labels it «пример, сервер ещё не подключён»; once the server answers, its numbers replace these.
const A = (key: string, title: string, value: number, unit: string, source: string): CalcAssumption => ({ key, title, value, unit, source, editable: false });
export const EXAMPLE_ASSUMPTIONS: CalcAssumption[] = [
  A("accelerator.capacity_fps", "Пропускная способность одного ускорителя LinQ", 12.4, "кадр/с", "замер LinQ 24.10 14:52: детектор 640, 4 запроса одновременно, общая очередь площадки"),
  A("models_per_frame", "Запросов к TPU на кадр", 2, "шт.", `конвейер ${PRODUCT}: детектор людей и поза`),
  A("accelerators_per_server", "Ускорителей в одном сервере", 4, "шт.", "допущение команды, уточнить у ХайТэк"),
  A("accelerator.price_rub", "Цена ускорителя LinQ", 500000, "₽", "допущение команды: цена не опубликована, заменить ценой поставщика"),
  A("server.price_rub", "Цена сервера под ускорители", 350000, "₽", "допущение команды, уточнить у поставщика"),
  A("integration_rub", "Пусконаладка и подключение камер", 300000, "₽", "допущение команды"),
  A("support_share_year", "Поддержка в год, доля от вложений", 0.15, "доля", "допущение команды"),
  A("light_sound_rub", "Световой и звуковой сигнал у зоны", 25000, "₽ за зону", "допущение команды, уточнить у поставщика"),
  A("zones_per_camera", "Сигнальных зон на камеру", 1, "шт.", "допущение команды"),
  A("speaker_rub", "Громкоговоритель в цех", 40000, "₽ за цех", "допущение команды, уточнить у поставщика"),
  A("new_camera_rub", "Новая IP-камера с монтажом", 30000, "₽", "допущение команды, уточнить у поставщика"),
  A("new_cameras_share", "Доля новых камер на максимальном уровне", 0.2, "доля", "допущение команды"),
  A("reduction.base", "Снижение инцидентов: базовый уровень", 0.2, "доля", "гипотеза команды, проверяется пилотом; доказанного эффекта нет"),
  A("reduction.extended", "Снижение инцидентов: расширенный уровень", 0.3, "доля", "гипотеза команды, проверяется пилотом; доказанного эффекта нет"),
  A("reduction.max", "Снижение инцидентов: максимальный уровень", 0.4, "доля", "гипотеза команды, проверяется пилотом; доказанного эффекта нет"),
];
export const EXAMPLE_ROLLOUT: RolloutIn = { workshops: 2, cameras: 8, shifts_per_day: 2, workers: 200, operators: 2, incidents_per_year: 4, downtime_cost_rub: 500000, fine_cost_rub: 200000, treatment_cost_rub: 300000, lawsuit_cost_rub: 500000, overrides: {} };
export const EXAMPLE_SCALE: ScaleIn = { cameras_now: 8, new_cameras: 8, overrides: {} };
/** config `pipeline.target_analysis_fps` (tech.md 6.6). */
export const EXAMPLE_FPS = 12;

const v = (key: string) => EXAMPLE_ASSUMPTIONS.find(a => a.key === key)!.value;
const rub = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });
const times = (label: string, n: number, price: number) => ({ label, value: `${rub.format(n)} × ${rub.format(price)} ₽` });

export const accelerators = (cameras: number) => Math.ceil(cameras * EXAMPLE_FPS * v("models_per_frame") / v("accelerator.capacity_fps"));
export const servers = (acc: number) => Math.ceil(acc / v("accelerators_per_server"));

export function exampleRollout(input: RolloutIn = EXAMPLE_ROLLOUT): RolloutResult {
  const cost = input.downtime_cost_rub + input.fine_cost_rub + input.treatment_cost_rub + input.lawsuit_cost_rub;
  const acc = accelerators(input.cameras), srv = servers(acc);
  const zones = input.cameras * v("zones_per_camera"), newCameras = Math.ceil(input.cameras * v("new_cameras_share"));
  const baseItems = [times("Ускорители LinQ", acc, v("accelerator.price_rub")), times("Серверы", srv, v("server.price_rub")), { label: "Пусконаладка", value: `${rub.format(v("integration_rub"))} ₽` }];
  const lightItem = times("Свет и звук у зон", zones, v("light_sound_rub"));
  const base = acc * v("accelerator.price_rub") + srv * v("server.price_rub") + v("integration_rub");
  const extended = base + zones * v("light_sound_rub");
  const max = extended + input.workshops * v("speaker_rub") + newCameras * v("new_camera_rub");
  const tier = (id: TierResult["tier"], title: string, capex: number, items: TierResult["items"]): TierResult => {
    const opex = capex * v("support_share_year"), savings = input.incidents_per_year * cost * v(`reduction.${id}`);
    return { tier: id, title, capex_rub: capex, opex_rub_year: opex, savings_rub_year: savings, payback_months: savings > opex ? capex / (savings - opex) * 12 : null, accelerators: acc, servers: srv, items };
  };
  return {
    incident_cost_rub: cost,
    incidents_per_1000_workers: input.workers ? input.incidents_per_year / input.workers * 1000 : null,
    // Needs live events of the server: no server, no figure.
    events_per_operator_shift: null,
    assumptions: EXAMPLE_ASSUMPTIONS,
    tiers: [
      tier("base", "Базовый", base, baseItems),
      tier("extended", "Расширенный", extended, [...baseItems, lightItem]),
      tier("max", "Максимальный", max, [...baseItems, lightItem, times("Громкоговорители", input.workshops, v("speaker_rub")), times("Новые камеры", newCameras, v("new_camera_rub"))]),
    ],
  };
}

export function exampleScale(input: ScaleIn = EXAMPLE_SCALE): ScaleResult {
  const now = accelerators(input.cameras_now), total = accelerators(input.cameras_now + input.new_cameras);
  const srvNow = servers(now), srvTotal = servers(total);
  return {
    cameras_total: input.cameras_now + input.new_cameras, accelerators_now: now, accelerators_total: total, servers_total: srvTotal,
    analysis_fps: EXAMPLE_FPS, capacity_fps: v("accelerator.capacity_fps"), capacity_source: EXAMPLE_ASSUMPTIONS[0].source,
    capex_rub: (total - now) * v("accelerator.price_rub") + (srvTotal - srvNow) * v("server.price_rub") + input.new_cameras * v("new_camera_rub"),
    assumptions: EXAMPLE_ASSUMPTIONS,
    items: [times("Ускорители LinQ", total - now, v("accelerator.price_rub")), times("Серверы", srvTotal - srvNow, v("server.price_rub")), times("Новые камеры", input.new_cameras, v("new_camera_rub"))],
  };
}
