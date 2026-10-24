// Stateful core of the mock: one world in memory, transitions of tech.md 8.6, camera and
// sector states of 8.9, feed and notifications of 8.8. Every change goes out through `emit`.
import {
  CONTRACT, DEMO_ACTOR, LEVEL_TITLES, NO_OBSERVATION_TEXTS, RULE_PARAMS, ROLE_ACTIONS, SCENARIO_TITLES,
  SOURCE_HISTORY, SOURCE_SYNTHETIC, STATUS_TITLES, STORY, TERMINAL, buildWorld, loadEvidence,
} from "./world.mjs";

// Static assets copied from the checkpoint mock; camera 8 has no observation.
export function previewBytes(id) { return id >= 1 && id <= 7; }
const FEED_LIMIT = 100;
const RECENT_CLOSED_MS = 30 * 60 * 1000;
const ESCALATION_TIMEOUT_MS = 45 * 1000;
const iso = (ms) => (ms == null ? null : new Date(ms).toISOString());

export class AppError extends Error {
  constructor(status, code, message, details = {}) {
    super(message);
    Object.assign(this, { status, code, details });
  }
}

export class Mock {
  constructor({ emit, escalation = false, withEpisode = true, clock = () => Date.now() }) {
    this.emit = emit; // (type, data, audience|null) => void
    this.escalation = escalation;
    this.withEpisode = withEpisode;
    this.now = clock;
    this.reset();
  }

  reset() {
    const now = this.now();
    Object.assign(this, buildWorld(now));
    // Live ids keep growing across resets: a frontend must not take a new event for an old one.
    this.nextEventId = Math.max(this.nextEventId ?? 0, this.events.length + 1);
    this.nextActionId = 1;
    for (const e of this.events) for (const a of e.actions) a.id = this.nextActionId++;
    this.step = 0;
    this.faults = { evidence404: false, error500: false };
    this.evidence = this.loadEvidence();
    decorateHistory(this);
    this.lastStates = this.statesSnapshot();
  }

  loadEvidence() {
    const conf = loadEvidence();
    const out = {};
    STORY.forEach((s, i) => {
      const c = conf[s.key];
      const path = c.file;
      out[s.key] = {
        id: i + 1, path, frame_idx: c.frame_idx, ts_ms: c.ts_ms, objects: c.objects,
        sha256: c.sha256,
      };
    });
    return out;
  }

  evidenceById(id) {
    return Object.values(this.evidence).find((e) => e.id === id) ?? null;
  }

  // --- lookups -------------------------------------------------------------------------
  sector(id) { return this.sectors.find((s) => s.id === id); }
  camera(id) { return this.cameras.find((c) => c.id === id); }
  zone(id) { return id == null ? null : this.zones.find((z) => z.id === id); }
  event(id) {
    const e = this.events.find((x) => x.id === id);
    if (!e) throw new AppError(404, "not_found", "Событие не найдено", { event_id: id });
    return e;
  }

  // --- summaries -----------------------------------------------------------------------
  priority(e) {
    if (TERMINAL.has(e.status)) return 0;
    if (e.status === "new" || e.status === "viewed") return e.level === "red" ? 3 : 2;
    return 1;
  }

  summary(e) {
    const now = this.now();
    const sector = this.sector(e.sector_id);
    const camera = this.camera(e.camera_id);
    const zone = this.zone(e.zone_id);
    let text = `${LEVEL_TITLES[e.level]} · ${sector.name.split(" · ")[0]} · ${e.reason_text}`;
    if (e.escalated_by_timeout) text += " · Не подтверждено оператором";
    return {
      id: e.id, scenario: e.scenario, title: SCENARIO_TITLES[e.scenario], level: e.level,
      status: e.status, status_title: STATUS_TITLES[e.status], operator_verdict: e.operator_verdict,
      escalated_by_timeout: e.escalated_by_timeout, mode: e.mode, camera_id: camera.id,
      camera_name: camera.name, sector_id: sector.id, sector_name: sector.name,
      zone_id: zone?.id ?? null, zone_name: zone?.name ?? null, reason_text: e.reason_text,
      notification_text: text, started_at: iso(e.started_at), published_at: iso(e.published_at),
      red_at: iso(e.red_at), ended_at: iso(e.ended_at),
      duration_s: Math.round(((e.ended_at ?? now) - e.started_at) / 100) / 10,
      priority: this.priority(e), is_demo: e.is_demo,
      person_name: "", person_position: "", crew: "", clip: null,
      // Contract main 62161986 (slice 12): confirm frame of the episode, null without one.
      evidence_url: e.episode?.evidence?.[0]?.url ?? null,
    };
  }

  // Lifecycle time of an event: the last action (terminal events leave the feed 30 min after it).
  closedAt(e) { return e.actions.at(-1)?.at ?? e.published_at; }

  feed(filter = () => true) {
    const now = this.now();
    return this.events
      .filter((e) => e.status !== "superseded" && filter(e))
      .filter((e) => !TERMINAL.has(e.status) || now - this.closedAt(e) <= RECENT_CLOSED_MS)
      .sort((a, b) => this.priority(b) - this.priority(a) || b.published_at - a.published_at)
      .slice(0, FEED_LIMIT)
      .map((e) => this.summary(e));
  }

  // --- states (8.9) --------------------------------------------------------------------
  cameraState(c) {
    const open = this.events.filter((e) => e.camera_id === c.id && !TERMINAL.has(e.status));
    const open_red = open.filter((e) => e.level === "red").length;
    const open_yellow = open.filter((e) => e.level === "yellow").length;
    let state = "normal";
    let reason = null;
    if (open_red) state = "red";
    else if (open.some((e) => e.level === "yellow" && e.ended_at == null)) state = "yellow";
    else if (!c.observed) [state, reason] = ["no_observation", "no_source"];
    return {
      camera_id: c.id, sector_id: c.sector_id, state, reason,
      reason_text: reason ? NO_OBSERVATION_TEXTS[reason] : "", freshness_ms: null, open_yellow, open_red,
    };
  }

  sectorState(s) {
    const states = this.cameras.filter((c) => c.sector_id === s.id).map((c) => this.cameraState(c));
    const noObs = states.filter((x) => x.state === "no_observation").length;
    let state = "normal";
    let reason_text = "";
    if (states.some((x) => x.state === "red")) state = "red";
    else if (states.some((x) => x.state === "yellow")) state = "yellow";
    else if (noObs || !states.length) {
      state = "no_observation";
      reason_text = `Нет наблюдения: ${noObs} из ${states.length} камер`;
    }
    const sum = (k) => states.reduce((n, x) => n + x[k], 0);
    return {
      sector_id: s.id, name: s.name, state, reason_text, cameras_total: states.length,
      cameras_no_observation: noObs, open_yellow: sum("open_yellow"), open_red: sum("open_red"),
    };
  }

  statesSnapshot() {
    return {
      cameras: new Map(this.cameras.map((c) => [c.id, JSON.stringify(this.cameraState(c))])),
      sectors: new Map(this.sectors.map((s) => [s.id, JSON.stringify(this.sectorState(s))])),
    };
  }

  // camera.state and sector.state for whatever changed since the last call.
  emitStates() {
    const next = this.statesSnapshot();
    for (const c of this.cameras) {
      if (next.cameras.get(c.id) !== this.lastStates.cameras.get(c.id)) this.emit("camera.state", this.cameraState(c));
    }
    for (const s of this.sectors) {
      if (next.sectors.get(s.id) !== this.lastStates.sectors.get(s.id)) this.emit("sector.state", this.sectorState(s));
    }
    this.lastStates = next;
  }

  // --- screens -------------------------------------------------------------------------
  dashboard() {
    return { sectors: this.sectors.map((s) => this.sectorState(s)), feed: this.feed(), server_now: iso(this.now()) };
  }

  sectorView(id) {
    const s = this.sector(id);
    if (!s) throw new AppError(404, "not_found", "Сектор не найден", { sector_id: id });
    const cams = this.cameras.filter((c) => c.sector_id === id);
    return {
      sector: this.sectorState(s),
      cameras: cams.map((c) => ({ camera: publicCamera(c), state: this.cameraState(c), broadcast: null, preview_url: c.observed && previewBytes(c.id) ? `/api/cameras/${c.id}/preview` : null })),
      feed: this.feed((e) => e.sector_id === id),
    };
  }

  detail(id, role) {
    const e = this.event(id);
    return {
      event: this.summary(e),
      episode: e.episode,
      why: e.why,
      actions: e.actions.map(publicAction),
      allowed_actions: role ? this.allowed(e, role) : [],
      provenance: e.provenance,
      deliveries: [],
      can_identify: false,
      video_id: null, video_start_ms: null, video_end_ms: null, broadcast: null,
    };
  }

  masterInbox() {
    const shown = (st) => this.events.filter((e) => e.status === st);
    const active = [...shown("sent_to_master"), ...shown("master_accepted")]
      .sort((a, b) => this.priority(b) - this.priority(a) || b.published_at - a.published_at);
    const resolved = shown("resolved").sort((a, b) => this.closedAt(b) - this.closedAt(a)).slice(0, 10);
    return { active: active.map((e) => this.summary(e)), recent_resolved: resolved.map((e) => this.summary(e)), server_now: iso(this.now()) };
  }

  // --- transitions (8.6) ---------------------------------------------------------------
  // Returns {to, verdict, logs} or null when the pair (action, status) is not in the table.
  transition(e, action) {
    const st = e.status;
    const early = ["new", "viewed", "confirmed"].includes(st);
    const timedOut = st === "sent_to_master" && e.escalated_by_timeout && e.operator_verdict === "none";
    switch (action) {
      case "view":
        return st === "new" ? { to: "viewed", logs: [["viewed", st, "viewed"]] } : null;
      case "confirm":
        if (e.level === "yellow") {
          return ["new", "viewed"].includes(st) ? { to: "confirmed", verdict: "confirmed", logs: [["confirmed", st, "confirmed"]] } : null;
        }
        if (early) {
          return { to: "sent_to_master", verdict: "confirmed", logs: [["confirmed", st, "confirmed"], ["sent_to_master", "confirmed", "sent_to_master"]] };
        }
        return timedOut ? { to: st, verdict: "confirmed", logs: [["confirmed", st, st]] } : null;
      case "false_alarm":
        return early || timedOut ? { to: "false_alarm", verdict: "false_alarm", logs: [["false_alarm", st, "false_alarm"]] } : null;
      case "send_to_master":
        return early
          ? { to: "sent_to_master", verdict: e.operator_verdict === "none" ? "confirmed" : undefined, logs: [["sent_to_master", st, "sent_to_master"]] }
          : null;
      case "accept":
        return st === "sent_to_master" ? { to: "master_accepted", logs: [["master_accepted", st, "master_accepted"]] } : null;
      case "resolve":
        return st === "master_accepted" ? { to: "resolved", logs: [["resolved", st, "resolved"]] } : null;
      default:
        return null;
    }
  }

  allowed(e, role) {
    return (ROLE_ACTIONS[role] ?? []).filter((a) => this.transition(e, a));
  }

  act(id, { action, comment = "" }, role, actor) {
    if (!role) throw new AppError(400, "role_required", "Выберите роль");
    const e = this.event(id);
    if (!(ROLE_ACTIONS[role] ?? []).includes(action)) {
      throw new AppError(403, "forbidden_role", "Действие недоступно для этой роли", { role, action });
    }
    const t = this.transition(e, action);
    if (!t) {
      throw new AppError(409, "invalid_transition", "Действие недоступно в текущем статусе события", { action, status: e.status });
    }
    if (action === "resolve" && !comment.trim()) {
      throw new AppError(422, "validation", "Опишите принятые меры", { field: "comment" });
    }
    const at = this.now();
    const before = e.status;
    for (const [log, from, to] of t.logs) {
      e.actions.push({ id: this.nextActionId++, at, actor_role: role, actor_name: actor || DEMO_ACTOR[role], action: log, from_status: from, to_status: to, comment });
    }
    e.status = t.to;
    if (t.verdict) e.operator_verdict = t.verdict;
    this.emit("event.updated", this.summary(e));
    if (t.to === "sent_to_master" && before !== "sent_to_master") this.notifyMaster(e);
    this.emitStates();
    return this.detail(id, role);
  }

  notifyMaster(e) {
    const s = this.summary(e);
    this.emit("notification", { id: `${e.id}-master`, event_id: e.id, level: e.level, text: s.notification_text, audience: ["master"], sound: "chime", takeover: false }, ["master"]);
  }

  // 8.7, behind a flag: red without an operator decision for 45 s goes to the master.
  escalationTick() {
    if (!this.escalation) return 0;
    const now = this.now();
    let n = 0;
    for (const e of this.events) {
      if (e.level !== "red" || !["new", "viewed", "confirmed"].includes(e.status) || e.red_at == null) continue;
      const reacted = e.actions.some((a) => a.at >= e.red_at && a.actor_role === "operator" && ["confirmed", "false_alarm", "sent_to_master"].includes(a.action));
      if (reacted || now - e.red_at < ESCALATION_TIMEOUT_MS) continue;
      e.actions.push({ id: this.nextActionId++, at: now, actor_role: "system", actor_name: DEMO_ACTOR.system, action: "timeout_escalated", from_status: e.status, to_status: "sent_to_master", comment: "" });
      e.status = "sent_to_master";
      e.escalated_by_timeout = true;
      this.emit("event.updated", this.summary(e));
      this.notifyMaster(e);
      n += 1;
    }
    if (n) this.emitStates();
    return n;
  }

  // --- director ------------------------------------------------------------------------
  // Publishes the next event of the story. Refuses the red one while the yellow one still waits
  // for the operator: on the backend the running episode would end and auto-finish it (8.5).
  publishNext({ force = false } = {}) {
    const s = STORY[this.step];
    if (!s) return { done: true, message: "История закончилась: demo reset" };
    const prev = this.events.find((e) => e.story === STORY[this.step - 1]?.key);
    if (prev && ["new", "viewed"].includes(prev.status) && !force) {
      return { refused: true, message: `Событие ${prev.id} (жёлтое) ещё ждёт оператора. На бэкенде оно завершилось бы само. Подтвердите его или demo next --force` };
    }
    const now = this.now();
    if (prev && prev.ended_at == null) {
      prev.ended_at = now;
      if (["new", "viewed"].includes(prev.status)) {
        prev.actions.push({ id: this.nextActionId++, at: now, actor_role: "system", actor_name: DEMO_ACTOR.system, action: "auto_finished", from_status: prev.status, to_status: "auto_finished", comment: "" });
        prev.status = "auto_finished";
      }
      this.emit("event.updated", this.summary(prev));
    }
    const camera = this.cameras[s.camera];
    const ev = this.evidence[s.key];
    const e = {
      id: this.nextEventId++, scenario: s.scenario, level: s.level, camera_id: camera.id, sector_id: camera.sector_id,
      zone_id: null, reason_text: s.reason_text, status: "new", operator_verdict: "none", escalated_by_timeout: false,
      mode: "demo", is_demo: true, started_at: now - (s.confirm_ms - s.start_ms), published_at: now,
      red_at: s.level === "red" ? now : null, ended_at: null, story: s.key,
      actions: [],
      why: [{ label: "Источник", value: SOURCE_SYNTHETIC }, ...s.why.map(([label, value]) => ({ label, value })), { label: "Рамка на кадре", value: "ручная разметка, не детекция модели" }],
      provenance: { backend: null, fake: true, det_model: null, pose_model: null, job_id: null, video_sha256: null, analysis_version: null, rule_params: RULE_PARAMS[s.scenario], evidence_sha256: ev.sha256 || null },
      episode: this.syntheticEpisode(s, ev),
    };
    e.actions.push({ id: this.nextActionId++, at: now, actor_role: "system", actor_name: DEMO_ACTOR.system, action: "published", from_status: null, to_status: "new", comment: "" });
    this.events.push(e);
    this.step += 1;
    const summary = this.summary(e);
    this.emit("event.created", summary);
    const red = s.level === "red";
    this.emit("notification", { id: `${e.id}-${s.level}`, event_id: e.id, level: s.level, text: summary.notification_text, audience: ["operator"], sound: red ? "siren" : "chime", takeover: red }, ["operator"]);
    this.emitStates();
    return { published: summary };
  }

  // The contract keeps `episode: null` for demo events, but the evidence frame is reachable only
  // through `episode.evidence` (GAPS.md): the live events carry a synthetic episode.
  syntheticEpisode(s, ev) {
    if (!this.withEpisode) return null;
    return {
      id: ev.id, analysis_id: 0, scenario: s.scenario, scenario_title: SCENARIO_TITLES[s.scenario], subject: "synthetic:1",
      zone_id: null, level_initial: s.level, level_max: s.level, start_ms: s.start_ms, confirm_ms: s.confirm_ms,
      escalate_ms: null, end_ms: s.end_ms, end_reason: "video_end", reason_code: s.reason_code, reason_text: s.reason_text,
      method: "синтетика: ручная разметка", confidence: 1, metrics: {}, uncertain_ms: 0,
      evidence: [{ id: ev.id, kind: "confirm", frame_idx: ev.frame_idx, ts_ms: ev.ts_ms, url: `/api/evidence/${ev.id}/image`, sha256: ev.sha256, objects: ev.objects }],
    };
  }

  status() {
    return {
      step: this.step, story: STORY.map((s) => s.key), escalation: this.escalation, with_episode: this.withEpisode, faults: this.faults,
      live: this.events.filter((e) => e.story).map((e) => ({ id: e.id, story: e.story, level: e.level, status: e.status, verdict: e.operator_verdict, actions: e.actions.map((a) => a.action) })),
      open: this.events.filter((e) => !TERMINAL.has(e.status)).length,
      history: this.events.filter((e) => !e.story).length,
    };
  }
}

export function publicCamera(c) {
  const { observed: _observed, ...rest } = c;
  return rest;
}

function publicAction(a) {
  return { id: a.id, at: iso(a.at), actor_role: a.actor_role, actor_name: a.actor_name, action: a.action, from_status: a.from_status, to_status: a.to_status, comment: a.comment };
}

// History events: episode null (as the seed), honest provenance.
export function decorateHistory(mock) {
  for (const e of mock.events) {
    if (e.story) continue;
    e.why ??= [{ label: "Источник", value: SOURCE_HISTORY }];
    e.provenance ??= { backend: null, fake: true, det_model: null, pose_model: null, job_id: null, video_sha256: null, analysis_version: null, rule_params: RULE_PARAMS[e.scenario] ?? {}, evidence_sha256: null };
  }
}

export { CONTRACT };
