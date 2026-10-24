import { useCallback, useEffect, useState } from "react";
import { apiError } from "./client";

export interface ApiState<T> {
  data: T | undefined;
  error: { code: string; message: string } | undefined;
  loading: boolean;
  reload: () => void;
}

type Call<T> = () => Promise<{ data?: T; error?: unknown }>;

// `fn` returns the result of an `api.GET(...)`: data on success, error with ApiError otherwise.
// The second overload is the untyped form of tech.md 7: data stays `unknown`.
export function useApi<T>(fn: Call<T>, deps: unknown[]): ApiState<T>;
export function useApi(fn: Call<unknown>, deps: unknown[]): ApiState<unknown>;
export function useApi<T>(fn: Call<T>, deps: unknown[]): ApiState<T> {
  const [data, setData] = useState<T>();
  const [error, setError] = useState<{ code: string; message: string }>();
  const [loading, setLoading] = useState(true);
  const [tick, setTick] = useState(0);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const call = useCallback(fn, deps);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    call()
      .then((result) => {
        if (!alive) return;
        setData(result.data);
        setError(result.error === undefined ? undefined : apiError(result.error));
      })
      .catch((e: unknown) => alive && setError(apiError(e)))
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [call, tick]);

  return { data, error, loading, reload: () => setTick((n) => n + 1) };
}
