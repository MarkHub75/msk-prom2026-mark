// Demo world of the mock: texts copied from src/safewatch/texts.py and the seed of
// src/safewatch/seed.py (tech.md 8.16), plus the live story of the fake scene `demo`.
// Everything here is synthetic and marked so (is_demo, provenance.fake, why).
import meta from "./meta-main.json";
import evidence from "./evidence.json";
import { PRODUCT } from "../../brand";

export const CONTRACT = "1.0.0";
export const PRODUCT_TITLE = PRODUCT;
export const TIMEZONE = "Europe/Moscow";

export const ROLES = ["operator", "master", "ohs", "management", "admin"];
export const ROLE_TITLES = {
  operator: "Оператор",
  master: "Мастер смены",
  ohs: "Охрана труда",
  management: "Менеджмент",
  admin: "Администратор",
};
export const DEMO_ACTOR = {
  operator: "Оператор смены",
  master: "Мастер смены",
  ohs: "Специалист по охране труда",
  management: "Руководитель",
  admin: "Администратор",
  system: "система",
};
export const LEVEL_TITLES = { yellow: "Жёлтая опасность", red: "Красная опасность" };
// Colors of the theme (tech.md 8.14).
export const LEVEL_COLORS = { yellow: "#FFC400", red: "#FF3B30" };
export const STATUS_TITLES = {
  new: "Новое",
  viewed: "Просмотрено",
  confirmed: "Подтверждено",
  false_alarm: "Ложное срабатывание",
  sent_to_master: "Передано мастеру",
  master_accepted: "Мастер принял",
  resolved: "Решено",
  auto_finished: "Завершилось само",
  superseded: "Пересчитано",
};
export const TERMINAL = new Set(["false_alarm", "resolved", "auto_finished", "superseded"]);
export const HUMAN_ACTIONS = ["view", "confirm", "false_alarm", "send_to_master", "accept", "resolve"];
export const ROLE_ACTIONS = {
  operator: ["view", "confirm", "false_alarm", "send_to_master"],
  master: ["accept", "resolve"],
  ohs: [],
  management: [],
  admin: [],
};
export const NO_OBSERVATION_TEXTS = {
  no_source: "Нет источника видео",
  processing: "Видео обрабатывается",
  failed: "Обработка не удалась",
  ended: "Запись закончилась",
  stale: "Данные анализа устарели",
  dark: "Слишком темно",
  obstructed: "Камера закрыта или не в фокусе",
};
export const SCENARIO_TITLES = {
  running: "Бег и резкие перемещения",
  proximity: "Опасное сближение с техникой",
  phone: "Телефон при работе",
  fall: "Падение и неподвижность",
  fence_crossing: "Перелезание через ограждение",
  restricted_under: "Проход под конвейером или грузом",
  fire_smoking: "Курение и открытый огонь",
  no_harness: "Высота без страховочной привязи",
  suspended_load: "Под подвешенным грузом",
  load_carrying: "Переноска груза с нарушением",
};
// API error texts (texts.py); texts the contract does not name yet are listed in GAPS.md.
export const MSG = {
  requestInvalid: "Неверные данные запроса",
  roleRequired: "Выберите роль",
  actorInvalid: "Имя: до 60 символов",
  notFound: "Не найдено",
  forbidden: "Действие недоступно для этой роли",
  invalidTransition: "Действие недоступно в текущем статусе события",
  commentRequired: "Опишите принятые меры",
  notImplemented: "Функция недоступна в демонстрационном моке",
  internal: "Внутренняя ошибка сервера (инъекция demo fault 500)",
};
export const ACTOR_MAX = 60;

export const DEMO_SECTORS = [
  "Сектор 1 · Прессовый участок",
  "Сектор 2 · Склад и погрузка",
  "Сектор 3 · Сборочный цех",
  "Сектор 4 · Ремонтная зона",
];
export const DEMO_CAMERAS = [
  ["Камера 1.1 · Пресс №2", "Обзор пресса и рабочего места"],
  ["Камера 1.2 · Проход у прессов", "Проход между прессами"],
  ["Камера 2.1 · Погрузочная рампа", "Рампа и зона работы погрузчиков"],
  ["Камера 2.2 · Стеллажи", "Проезд между стеллажами"],
  ["Камера 3.1 · Конвейер", "Сборочный конвейер"],
  ["Камера 3.2 · Ограждение линии", "Ограждение роботизированной линии"],
  ["Камера 4.1 · Ремонтная яма", "Ремонт под вагоном"],
  ["Камера 4.2 · Верстаки", "Верстаки и сварочный пост"],
];
// Zones per camera index, as in seed.ZONES.
const ZONES = [
  [0, "danger", "Пресс"],
  [1, "vehicle_path", "Проезд погрузчика"],
  [2, "vehicle_path", "Проезд погрузчика"],
  [4, "under_load", "Под конвейером"],
  [5, "fence", "Забор у линии"],
  [5, "danger", "Пресс"],
  [6, "lying_allowed", "Ремонтная яма"],
];
// The mock has no broadcast: a camera without one would be "no source" (8.9, rule 3).
// Cameras listed here count as observed (state normal); see GAPS.md.
const UNOBSERVED_CAMERAS = new Set([7]);

const DEMO_REASONS = {
  running: ["Бег 2,4 роста/с", "Бег 3,1 м/с", "Бег 2,0 роста/с рядом с техникой"],
  proximity: ["Сближение с погрузчиком: 0,8 м", "Сближение с грузовиком: 0,4 роста"],
  phone: ["Телефон в руке 12 с", "Телефон в руке 25 с"],
  fall: ["Зафиксировано падение", "Человек лежит неподвижно 15 с"],
  fence_crossing: ["Пересечение ограждения «Забор у линии»"],
  restricted_under: ["Человек в зоне «Под конвейером»"],
};
const DEMO_RESOLVE_COMMENTS = [
  "Провёл инструктаж на месте",
  "Работник отстранён до повторного инструктажа",
  "Пострадавших нет, рабочее место осмотрено",
  "Установлено дополнительное ограждение",
];

export const ZONE_KINDS = [
  ["danger", "Опасная зона / механизм", "#FF453A", "polygon", "Станок, пресс, конвейер, зона работы техники. Вход человека — красное событие."],
  ["fence", "Ограждение", "#FF9F0A", "line", "Линия, которую нельзя пересекать."],
  ["under_load", "Под конвейером / грузом", "#BF5AF2", "polygon", "Проход под конвейером или зона подъёма груза."],
  ["fire_allowed", "Огонь разрешён", "#FF6B00", "polygon", "Печь, сварочный пост. Огонь здесь не нарушение."],
  ["lying_allowed", "Лежать допустимо", "#30D158", "polygon", "Ремонт под станком или вагоном. Тревога только при долгой неподвижности."],
  ["rest", "Зона отдыха", "#64D2FF", "polygon", "Места отдыха. В baseline правила её не используют."],
  ["height", "Работа на высоте", "#FFD60A", "polygon", "Площадки и лестницы, где нужна страховочная привязь."],
  ["vehicle_path", "Пути транспорта", "#98989D", "polygon", "Проезды погрузчиков и машин."],
].map(([id, title, color, geometry, description]) => ({ id, title, color, geometry, description }));

// running and fall are taken as is from GET /api/meta of main (src/meta-main.json); the others are
// the mock's until slice 10 brings them (GAPS A2).
const FROM_MAIN = meta.scenarios;
// Scenario params: defaults of config/default.yaml; titles, units and ranges are the mock's (GAPS.md).
const P = (key, title, unit, def, min, max) => ({ key, title, unit, default: def, min, max });
const MODEL_MISSING = "Модель не подключена";
const NOT_IN_DEMO = "Не включён в демонстрационный контур";
export const SCENARIOS = [
  ["running", "Бег и резкие перемещения: скорость человека выше порога.", "run", "yellow", "active", "", ["person"], ["danger", "vehicle_path"], [
    P("speed_bh_s", "Порог скорости", "роста/с", 1.5, 0.5, 5), P("speed_m_s", "Порог скорости", "м/с", 2.5, 1, 8),
    P("hold_s", "Удержание", "с", 1, 0, 10), P("red_hold_s", "Удержание красного", "с", 0.5, 0, 10),
    P("near_vehicle_bh", "Рядом с техникой", "роста", 3, 0.5, 10), P("near_vehicle_m", "Рядом с техникой", "м", 3, 0.5, 20)]],
  ["proximity", "Человек слишком близко к движущейся технике.", "truck", "yellow", "skeleton", NOT_IN_DEMO, ["person", "car", "bus", "truck", "train"], ["danger"], []],
  ["phone", "Телефон в руке у работника.", "phone", "yellow", "skeleton", NOT_IN_DEMO, ["person", "cell phone"], ["danger", "vehicle_path"], []],
  ["fall", "Падение человека и неподвижность лёжа.", "fall", "red", "active", "", ["person"], ["lying_allowed"], [
    P("transition_s", "Переход в позу «лёжа»", "с", 2, 0.5, 10), P("confirm_s", "Удержание", "с", 2, 0, 10),
    P("still_s", "Неподвижность", "с", 10, 1, 120), P("allowed_still_s", "Неподвижность в разрешённой зоне", "с", 60, 5, 600)]],
  ["fence_crossing", "Пересечение линии ограждения.", "fence", "red", "skeleton", NOT_IN_DEMO, ["person"], ["fence"], []],
  ["restricted_under", "Человек под конвейером или грузом.", "conveyor", "red", "skeleton", NOT_IN_DEMO, ["person"], ["under_load"], []],
  ["fire_smoking", "Огонь или дым вне разрешённой зоны, курение.", "fire", "red", "model_missing", MODEL_MISSING, ["fire", "smoke", "cigarette"], ["fire_allowed", "danger"], []],
  ["no_harness", "Работа на высоте без страховочной привязи.", "harness", "yellow", "model_missing", MODEL_MISSING, ["no_harness"], ["height"], []],
  ["suspended_load", "Человек под подвешенным грузом.", "crane", "red", "model_missing", MODEL_MISSING, ["suspended_load"], [], []],
  ["load_carrying", "Переноска груза с нарушением.", "box", "yellow", "skeleton", "Сценарий уточняется: правила переноски не определены", [], [], []],
].map(([id, description, icon, default_level, status, status_text, required_classes, zone_kinds, params]) => ({
  id, title: SCENARIO_TITLES[id], description, icon, default_level, status, status_text, required_classes, zone_kinds, params,
})).map((s) => FROM_MAIN.find((m) => m.id === s.id) ?? s);
export const RULE_PARAMS = Object.fromEntries(
  SCENARIOS.map((s) => [s.id, Object.fromEntries(s.params.map((p) => [p.key, p.default]))]),
);

export const SOURCE_SYNTHETIC = "Синтетическое демо-событие, не результат нейросети";
export const SOURCE_HISTORY = "Демо-история (сид), не результат нейросети";

// Live story = fake scene `demo` (tech.md 6.1): walks 3 s, runs 3 s, walks 2 s, falls and lies 12 s.
// Both alarms: Сектор 1, «Камера 1.1 · Пресс №2». Reason texts are from table 8.3.
export const STORY = [
  {
    key: "yellow", scenario: "running", level: "yellow", camera: 0, reason_text: "Бег 2,4 роста/с",
    start_ms: 3000, confirm_ms: 4000, end_ms: 6000, reason_code: "speed_bh",
    why: [["Правило", "Бег: скорость выше 1,5 роста/с дольше 1 с"], ["Измерено", "2,4 роста/с"], ["Метод", "в ростах человека, без калибровки"]],
  },
  {
    key: "red", scenario: "fall", level: "red", camera: 0, reason_text: "Зафиксировано падение",
    start_ms: 8000, confirm_ms: 10000, end_ms: 20000, reason_code: "fall_transition",
    why: [["Правило", "Падение: поза «лёжа» не позже 2 с после позы «стоя», удержание 2 с"], ["Метод", "поза"]],
  },
];

// Small deterministic PRNG (mulberry32): the history is the same after every reset.
function rng(seed) {
  let a = seed >>> 0;
  const next = () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  return {
    next,
    int: (lo, hi) => lo + Math.floor(next() * (hi - lo + 1)),
    pick: (list) => list[Math.floor(next() * list.length)],
  };
}

const SEC = 1000;
const HISTORY = [
  // [level, scenario, outcome]: the outcome mix of seed_demo (8.16), all terminal (GAPS.md)
  ["yellow", "running", "resolved"], ["yellow", "phone", "resolved"], ["yellow", "proximity", "auto_finished"],
  ["yellow", "running", "false_alarm"], ["yellow", "running", "auto_finished"], ["yellow", "phone", "resolved"],
  ["yellow", "proximity", "resolved"], ["yellow", "running", "auto_finished"], ["yellow", "running", "resolved"],
  ["yellow", "phone", "false_alarm"], ["yellow", "proximity", "resolved"], ["yellow", "running", "auto_finished"],
  ["red", "fall", "resolved"], ["red", "fence_crossing", "resolved"], ["red", "restricted_under", "false_alarm"],
  ["red", "fall", "timeout"], ["red", "running", "resolved"], ["red", "proximity", "resolved"],
];

function history(e, outcome, r) {
  const act = (at, actor_role, action, from_status, to_status, comment = "") =>
    e.actions.push({ at, actor_role, actor_name: DEMO_ACTOR[actor_role], action, from_status, to_status, comment });
  let t = e.published_at;
  act(t, "system", "published", null, "new");
  if (outcome === "auto_finished") {
    act(e.ended_at, "system", "auto_finished", "new", "auto_finished");
    e.status = "auto_finished";
    return;
  }
  let prev;
  if (outcome === "timeout") {
    t += 45 * SEC;
    act(t, "system", "timeout_escalated", "new", "sent_to_master");
    e.escalated_by_timeout = true;
    prev = "sent_to_master";
  } else {
    t += r.int(5, 30) * SEC;
    act(t, "operator", "viewed", "new", "viewed");
    t += r.int(3, 40) * SEC;
    if (outcome === "false_alarm") {
      act(t, "operator", "false_alarm", "viewed", "false_alarm");
      e.operator_verdict = "false_alarm";
      e.status = "false_alarm";
      return;
    }
    act(t, "operator", "confirmed", "viewed", "confirmed");
    e.operator_verdict = "confirmed";
    // A confirmed yellow stays open (8.6); the history is terminal, so it goes on to the master.
    act(t + 5 * SEC, "operator", "sent_to_master", "confirmed", "sent_to_master");
    prev = "sent_to_master";
  }
  t += r.int(60, 300) * SEC;
  act(t, "master", "master_accepted", prev, "master_accepted");
  t += r.int(300, 1800) * SEC;
  act(t, "master", "resolved", "master_accepted", "resolved", r.pick(DEMO_RESOLVE_COMMENTS));
  e.status = "resolved";
}

export function loadEvidence() {
  return structuredClone(evidence);
}

// Fresh world: ids are stable across resets (sectors 1..4, cameras 1..8, history events 1..18).
export function buildWorld(now) {
  const sectors = DEMO_SECTORS.map((name, i) => ({ id: i + 1, name, sort_order: i + 1, is_demo: true }));
  const zones = ZONES.map(([cam, kind, name], i) => ({ id: i + 1, camera_id: cam + 1, kind, name }));
  const cameras = DEMO_CAMERAS.map(([name, description], i) => ({
    id: i + 1,
    sector_id: Math.floor(i / 2) + 1,
    name,
    description,
    is_demo: true,
    has_calibration: false,
    zones_count: zones.filter((z) => z.camera_id === i + 1).length,
    videos_count: 0,
    observed: !UNOBSERVED_CAMERAS.has(i),
  }));
  const r = rng(2026);
  const midnight = new Date(now);
  midnight.setUTCHours(21, 0, 0, 0); // 00:00 MSK (UTC+3) of the next or the current day
  if (midnight.getTime() > now) midnight.setUTCDate(midnight.getUTCDate() - 1);
  const yesterday = midnight.getTime() - 86400 * SEC;
  const events = HISTORY.map(([level, scenario, outcome]) => {
    const camera = cameras[r.int(0, cameras.length - 1)];
    const own = zones.filter((z) => z.camera_id === camera.id);
    const started_at = yesterday - r.int(0, 6) * 86400 * SEC + r.int(0, 86399) * SEC;
    const published_at = started_at + r.int(2, 8) * SEC;
    const e = {
      id: 0, scenario, level, camera_id: camera.id, sector_id: camera.sector_id,
      zone_id: own.length && r.next() < 0.5 ? own[0].id : null,
      reason_text: r.pick(DEMO_REASONS[scenario]),
      status: "new", operator_verdict: "none", escalated_by_timeout: false, mode: "demo", is_demo: true,
      started_at, published_at, red_at: level === "red" ? published_at : null,
      ended_at: published_at + r.int(5, 120) * SEC,
      actions: [], episode: null, story: null,
    };
    history(e, outcome, r);
    return e;
  });
  events.sort((a, b) => a.started_at - b.started_at);
  events.forEach((e, i) => (e.id = i + 1));
  return { sectors, cameras, zones, events };
}
