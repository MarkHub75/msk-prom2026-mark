import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { api, getReviewScenario, isReviewMode, mediaUrl, setActor, videoUrl } from "../api/client";
import { setRole } from "../roles";
import { resetReview } from "./review";

beforeEach(() => {
  sessionStorage.clear();
  localStorage.clear();
  history.replaceState({}, "", "/operator?review=critical&reset=1");
  resetReview();
  setRole("operator");
  setActor("Контрактный тест");
});
afterEach(() => {
  history.replaceState({}, "", "/?review=real");
  isReviewMode();
  vi.unstubAllGlobals();
});

describe("explicit contract-shaped review transport", () => {
  it("requires explicit actor identity and provides journal filters/facets from the same state", async () => {
    setActor("");
    const unnamed = await api.POST("/api/events/{event_id}/actions",{params:{path:{event_id:41}},body:{action:"confirm",comment:""}});
    expect(unnamed.response.status).toBe(422);
    setActor("Контрактный тест");
    const page = await api.GET("/api/events",{params:{query:{status:"resolved",limit:1}}});
    expect(page.data?.items.map(item=>item.id)).toEqual([44]);
    expect(page.data?.total).toBe(1);
    expect(page.data?.next_cursor).toBeNull();
    const facets = await api.GET("/api/journal/facets");
    expect(facets.data?.sectors.every(item=>typeof item.id === "string")).toBe(true);
    expect(facets.data?.statuses.some(item=>item.id === "resolved")).toBe(true);
  });
  it("completes operator view/confirm → master accept/report and preserves the same event", async () => {
    setActor("Оператор · проверка");
    const first = await api.GET("/api/events/{event_id}", {params: {path: {event_id: 41}}});
    expect(first.data?.event.status).toBe("new");
    expect(first.data?.allowed_actions).toContain("view");
    const viewed = await api.POST("/api/events/{event_id}/actions", {params: {path: {event_id: 41}}, body: {action: "view", comment: ""}});
    expect(viewed.data?.event.status).toBe("viewed");
    expect(viewed.data?.allowed_actions).not.toContain("view");
    const sent = await api.POST("/api/events/{event_id}/actions", {params: {path: {event_id: 41}}, body: {action: "confirm", comment: ""}});
    expect(sent.data?.event.status).toBe("sent_to_master");
    expect(sent.data?.event.operator_verdict).toBe("confirmed");
    expect(sent.data?.actions.slice(-2).map((item) => item.action)).toEqual(["confirmed", "sent_to_master"]);
    expect(sent.data?.actions.at(-1)?.actor_name).toBe("Оператор · проверка");
    history.pushState({}, "", "/master");
    setRole("master");
    const inbox = await api.GET("/api/master/inbox");
    expect(inbox.data?.active.map((event) => event.id)).toContain(41);
    const accepted = await api.POST("/api/events/{event_id}/actions", {params: {path: {event_id: 41}}, body: {action: "accept", comment: ""}});
    expect(accepted.data?.event.status).toBe("master_accepted");
    expect(accepted.data?.allowed_actions).toEqual(["resolve"]);
    const blank = await api.POST("/api/events/{event_id}/actions", {params: {path: {event_id: 41}}, body: {action: "resolve", comment: "  "}});
    expect(blank.response.status).toBe(422);
    expect(blank.error?.message).toBe("Опишите принятые меры");
    const report = "Проверил участок. Ограждение восстановлено, проход освобождён.";
    const resolved = await api.POST("/api/events/{event_id}/actions", {params: {path: {event_id: 41}}, body: {action: "resolve", comment: report}});
    expect(resolved.data?.event.status).toBe("resolved");
    expect(resolved.data?.actions.at(-1)?.comment).toBe(report);
    const after = await api.GET("/api/master/inbox");
    expect(after.data?.active.some((event) => event.id === 41)).toBe(false);
    expect(after.data?.recent_resolved.some((event) => event.id === 41)).toBe(true);
  });

  it("rejects wrong roles, stale transitions and oversized reports without changing the event", async () => {
    const forbidden = await api.POST("/api/events/{event_id}/actions", {params: {path: {event_id: 43}}, body: {action: "accept", comment: ""}});
    expect(forbidden.response.status).toBe(403);
    setRole("master");
    const conflict = await api.POST("/api/events/{event_id}/actions", {params: {path: {event_id: 43}}, body: {action: "resolve", comment: "Готово"}});
    expect(conflict.response.status).toBe(409);
    await api.POST("/api/events/{event_id}/actions", {params: {path: {event_id: 43}}, body: {action: "accept", comment: ""}});
    const repeated = await api.POST("/api/events/{event_id}/actions", {params: {path: {event_id: 43}}, body: {action: "accept", comment: ""}});
    expect(repeated.response.status).toBe(409);
    const long = await api.POST("/api/events/{event_id}/actions", {params: {path: {event_id: 43}}, body: {action: "resolve", comment: "а".repeat(501)}});
    expect(long.response.status).toBe(422);
    const event = await api.GET("/api/events/{event_id}", {params: {path: {event_id: 43}}});
    expect(event.data?.event.status).toBe("master_accepted");
  });

  it("returns only role/state allowed actions and supports a false alarm without fake handoff", async () => {
    const falseAlarm = await api.POST("/api/events/{event_id}/actions", {params: {path: {event_id: 41}}, body: {action: "false_alarm", comment: ""}});
    expect(falseAlarm.data?.allowed_actions).toEqual([]);
    expect(falseAlarm.data?.event.status).toBe("false_alarm");
    setRole("master");
    const inbox = await api.GET("/api/master/inbox");
    expect(inbox.data?.active.some((event) => event.id === 41)).toBe(false);
    setRole("ohs");
    const readonly = await api.GET("/api/events/{event_id}", {params: {path: {event_id: 42}}});
    expect(readonly.data?.allowed_actions).toEqual([]);
  });

  it("uses the matching synthetic source for evidence, video and per-frame HUD", async () => {
    const event = await api.GET("/api/events/{event_id}", {params: {path: {event_id: 42}}});
    expect(event.data?.provenance.fake).toBe(true);
    expect(event.data?.event.is_demo).toBe(true);
    expect(event.data?.episode?.evidence[0].url).toBe("/fixtures/factory-welding.png");
    expect(videoUrl(3)).toBe("/fixtures/factory-welding-replay.mp4");
    expect(videoUrl(1)).toBe("/fixtures/factory-replay.mp4");
    expect(mediaUrl("/api/evidence/42/image")).toBe("/fixtures/factory-welding.png");
    const tracks = await api.GET("/api/videos/{video_id}/tracks", {params: {path: {video_id: 3}, query: {from_ms: 0, to_ms: 80}}});
    expect(tracks.data?.frames.map((frame) => frame.ts_ms)).toEqual([0, 40, 80]);
    expect(tracks.data?.frames[0].objects[0].bbox).toEqual(event.data?.episode?.evidence[0].objects[0].bbox);
    const invalid = await api.GET("/api/videos/{video_id}/tracks", {params: {path: {video_id: 3}, query: {from_ms: 80, to_ms: 0}}});
    expect(invalid.response.status).toBe(422);
  });

  it("never converts a real API error into synthetic data", async () => {
    history.replaceState({}, "", "/operator?review=real");
    const fetch = vi.fn(async () => new Response(JSON.stringify({code: "not_implemented", message: "Функция появится в слайсе 6"}), {status: 501}));
    vi.stubGlobal("fetch", fetch);
    const result = await api.GET("/api/operator/dashboard");
    expect(getReviewScenario()).toBe("");
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(result.data).toBeUndefined();
    expect(result.error?.code).toBe("not_implemented");
    expect(result.response.status).toBe(501);
  });

  it("provides deterministic empty, unavailable, offline and WS-disconnected states", async () => {
    history.replaceState({}, "", "/operator?review=empty");
    const empty = await api.GET("/api/operator/dashboard");
    expect(empty.data?.sectors).toEqual([]);
    expect(empty.data?.feed).toEqual([]);
    history.replaceState({}, "", "/operator?review=notimplemented");
    expect((await api.GET("/api/operator/dashboard")).response.status).toBe(501);
    history.replaceState({}, "", "/operator?review=error");
    expect((await api.GET("/api/operator/dashboard")).response.status).toBe(503);
    history.replaceState({}, "", "/operator?review=offline");
    await expect(api.GET("/api/operator/dashboard")).rejects.toThrow();
    history.replaceState({}, "", "/operator?review=disconnected");
    expect((await api.GET("/api/operator/dashboard")).data?.sectors.length).toBe(6);
  });
});
