import { useCallback, useEffect, useMemo, useState } from "react";
import { apiError, type ApiFailure } from "./client";

export interface ApiState<T> {
  data: T | undefined;
  error: ApiFailure | undefined;
  loading: boolean;
  reload: () => void;
}

export interface ApiOptions {
  // Triggers that refetch the same query (WS update counters, status): while such a refetch runs,
  // the previous data stays on screen instead of flashing a loading state.
  refresh?: unknown[];
}

type Call<T> = () => Promise<{ data?: T; error?: unknown; response?: Response }>;
interface InternalState<T> {owner?: Call<T>; identity?: object; tick: number; data?: T; error?: ApiFailure; loading: boolean}

// `fn` returns the result of an `api.GET(...)`: data on success, error with ApiError otherwise.
// `deps` identify the query (a new id drops old data at once); `options.refresh` only refetch it.
export function useApi<T>(fn: Call<T>, deps: unknown[], options?: ApiOptions): ApiState<T>;
export function useApi(fn: Call<unknown>, deps: unknown[], options?: ApiOptions): ApiState<unknown>;
export function useApi<T>(fn: Call<T>, deps: unknown[], options?: ApiOptions): ApiState<T> {
  const refresh = options?.refresh ?? [];
  const [state, setState] = useState<InternalState<T>>({tick: 0, loading: true});
  const [tick, setTick] = useState(0);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const identity = useMemo(() => ({}), deps);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const call = useCallback(fn, [...deps, ...refresh]);

  useEffect(() => {
    let alive = true;
    setState((prev) => ({owner: call, identity, tick, loading: true, data: prev.identity === identity ? prev.data : undefined}));
    call()
      .then((result) => {
        if (!alive) return;
        if (result.error !== undefined) setState({owner: call, identity, tick, loading: false, error: {...apiError(result.error), ...(result.response ? {status: result.response.status} : {})}});
        else setState({owner: call, identity, tick, data: result.data, loading: false});
      })
      .catch((e: unknown) => { if (alive) setState({owner: call, identity, tick, error: apiError(e), loading: false}); });
    return () => {
      alive = false;
    };
  }, [call, identity, tick]);

  // Never show a previous event/camera, even during the render before its next effect;
  // the same query being refetched keeps its last data.
  const current = state.owner === call && state.tick === tick ? state
    : state.identity === identity ? {loading: true, data: state.data, error: undefined}
    : {loading: true, data: undefined, error: undefined};
  return {data: current.data, error: current.error, loading: current.loading, reload: () => setTick((n) => n + 1)};
}
