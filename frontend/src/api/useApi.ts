import { useCallback, useEffect, useState } from "react";
import { apiError, type ApiFailure } from "./client";

export interface ApiState<T> {
  data: T | undefined;
  error: ApiFailure | undefined;
  loading: boolean;
  reload: () => void;
}

type Call<T> = () => Promise<{ data?: T; error?: unknown; response?: Response }>;
interface InternalState<T> {owner?: Call<T>; tick: number; data?: T; error?: ApiFailure; loading: boolean}

// `fn` returns the result of an `api.GET(...)`: data on success, error with ApiError otherwise.
// The second overload is the untyped form of tech.md 7: data stays `unknown`.
export function useApi<T>(fn: Call<T>, deps: unknown[]): ApiState<T>;
export function useApi(fn: Call<unknown>, deps: unknown[]): ApiState<unknown>;
export function useApi<T>(fn: Call<T>, deps: unknown[]): ApiState<T> {
  const [state, setState] = useState<InternalState<T>>({tick: 0, loading: true});
  const [tick, setTick] = useState(0);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const call = useCallback(fn, deps);

  useEffect(() => {
    let alive = true;
    setState({owner: call, tick, loading: true});
    call()
      .then((result) => {
        if (!alive) return;
        if (result.error !== undefined) setState({owner: call, tick, loading: false, error: {...apiError(result.error), ...(result.response ? {status: result.response.status} : {})}});
        else setState({owner: call, tick, data: result.data, loading: false});
      })
      .catch((e: unknown) => { if (alive) setState({owner: call, tick, error: apiError(e), loading: false}); });
    return () => {
      alive = false;
    };
  }, [call, tick]);

  // Do not show a previous event/camera even during the render before its next effect.
  const current = state.owner === call && state.tick === tick ? state : {loading: true, data: undefined, error: undefined};
  return {data: current.data, error: current.error, loading: current.loading, reload: () => setTick((n) => n + 1)};
}
