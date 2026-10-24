import { act, cleanup, renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { useApi } from "./useApi";

afterEach(cleanup);

describe("API query ownership", () => {
  it("clears stale data immediately for a new query and preserves HTTP errors", async () => {
    const call = (id: number) => id === 1 ? Promise.resolve({data: "camera-one"}) : Promise.resolve({error: {code: "not_implemented", message: "Функция появится в слайсе 6"}, response: new Response(null, {status: 501})});
    const hook = renderHook(({id}) => useApi(() => call(id), [id]), {initialProps: {id: 1}});
    await waitFor(() => expect(hook.result.current.data).toBe("camera-one"));
    hook.rerender({id: 2});
    expect(hook.result.current.data).toBeUndefined();
    await waitFor(() => expect(hook.result.current.error?.status).toBe(501));
    expect(hook.result.current.data).toBeUndefined();
    expect(hook.result.current.error?.code).toBe("not_implemented");
  });

  it("ignores a late response from the previous event", async () => {
    let finishOld: ((value: {data: string}) => void) | undefined;
    const old = new Promise<{data: string}>((resolve) => { finishOld = resolve; });
    const hook = renderHook(({id}) => useApi(() => id === 1 ? old : Promise.resolve({data: "event-two"}), [id]), {initialProps: {id: 1}});
    hook.rerender({id: 2});
    await waitFor(() => expect(hook.result.current.data).toBe("event-two"));
    await act(async () => { finishOld!({data: "event-one"}); await old; });
    expect(hook.result.current.data).toBe("event-two");
  });
});
