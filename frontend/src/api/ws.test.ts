import { act, cleanup, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import schemaText from "./ws.schema.generated.json?raw";
import { setRole } from "../roles";
import { isReviewMode } from "../fixtures/review";
import { parseWsMessage, useWs, wsUrl } from "./ws";
const examplesText = readFileSync(resolve(process.cwd(), "../contract/ws-examples.json"), "utf8");

beforeEach(() => { sessionStorage.clear(); history.replaceState({}, "", "/?review=real"); isReviewMode(); act(() => setRole("operator")); });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.useRealTimers(); });

describe("actual WS schema boundary", () => {
  it("accepts every supplied contract example and rejects malformed or mismatched payloads", () => {
    expect(schemaText).toBe(readFileSync(resolve(process.cwd(), "../contract/ws.schema.json"), "utf8"));
    const examples = JSON.parse(examplesText) as unknown[];
    expect(examples.length).toBeGreaterThan(5);
    for (const example of examples) expect(parseWsMessage(JSON.stringify(example))).not.toBeNull();
    for (const invalid of ["{", "null", "[]", JSON.stringify({type: "unknown", at: "2026-10-24T07:00:00Z", data: {}}),
      JSON.stringify({type: "event.created", at: "2026-10-24T07:00:00Z", data: {server_now: "2026-10-24T07:00:00Z", contract: "1", role: "operator"}})]) expect(parseWsMessage(invalid)).toBeNull();
    expect(wsUrl("master")).toContain("/ws?role=master");
  });

  it("opens no network WebSocket in fixture mode and shows a separate disconnected state", async () => {
    const socket = vi.fn();
    vi.stubGlobal("WebSocket", socket);
    history.replaceState({}, "", "/?review=critical");
    const handler = vi.fn();
    const first = renderHook(() => useWs(handler));
    expect(first.result.current.status).toBe("fixture");
    await act(async () => { await Promise.resolve(); });
    expect(handler.mock.calls[0][0].type).toBe("hello");
    expect(socket).not.toHaveBeenCalled();
    first.unmount();
    history.replaceState({}, "", "/?review=disconnected");
    const disconnected = renderHook(() => useWs(handler));
    expect(disconnected.result.current.status).toBe("disconnected");
    expect(socket).not.toHaveBeenCalled();
  });

  it("reconnects after 1, 2, 4, 8 seconds and cancels retries when unmounted", () => {
    vi.useFakeTimers();
    const sockets: FakeSocket[] = [];
    class FakeSocket {
      onopen: (() => void) | null = null;
      onmessage: ((event: {data: string}) => void) | null = null;
      onclose: ((event: {code: number}) => void) | null = null;
      onerror: (() => void) | null = null;
      constructor() { sockets.push(this); }
      close() {}
    }
    vi.stubGlobal("WebSocket", FakeSocket);
    const hook = renderHook(() => useWs(() => {}));
    expect(sockets.length).toBe(1);
    for (const seconds of [1, 2, 4, 8]) {
      act(() => sockets.at(-1)!.onclose!({code: 1006}));
      const count = sockets.length;
      act(() => vi.advanceTimersByTime(seconds * 1000 - 1));
      expect(sockets.length).toBe(count);
      act(() => vi.advanceTimersByTime(1));
      expect(sockets.length).toBe(count + 1);
    }
    act(() => sockets.at(-1)!.onclose!({code: 1006}));
    hook.unmount();
    const count = sockets.length;
    act(() => vi.advanceTimersByTime(8000));
    expect(sockets.length).toBe(count);
  });
});
