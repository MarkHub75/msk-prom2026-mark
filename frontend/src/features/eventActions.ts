import { useCallback, useEffect, useRef, useState } from "react";
import { api, apiError } from "../api/client";
import type { EventDetail, HumanAction } from "../api/types";
import { useActorIdentity } from "../components/ActorIdentity";

export const ACTIONS: Record<HumanAction, string> = {view:"Отметить просмотр",confirm:"Подтвердить",false_alarm:"Ложное срабатывание",send_to_master:"Передать мастеру",accept:"Принять в работу",resolve:"Отправить отчёт и завершить"};

/** POST /api/events/{id}/actions for the shown detail: asks the actor name first, sends only an action the server allows. */
export function useEventActions(id: number, detail: EventDetail | undefined, identity: string) {
  const { ensureActor } = useActorIdentity();
  const [busy, setBusy] = useState<HumanAction>();
  const [actionError, setActionError] = useState<{code:string;message:string}>();
  const guard = useRef(false);
  const currentIdentity = useRef(identity); currentIdentity.current = identity;
  const latestDetail = useRef(detail); latestDetail.current = detail;
  useEffect(() => { setActionError(undefined); }, [identity]);
  // Resolves with the server's new detail (or `saved` without one), `undefined` when nothing was saved.
  const send = useCallback(async (action: HumanAction, comment = ""): Promise<{ saved: EventDetail | true } | undefined> => {
    if (guard.current) return undefined;
    guard.current = true; setBusy(action); setActionError(undefined);
    const sendingIdentity = identity;
    try {
      if (!await ensureActor() || currentIdentity.current !== sendingIdentity) return undefined;
      if (!latestDetail.current?.allowed_actions.includes(action)) {
        setActionError({code:"state_changed",message:"Состояние изменилось. Обновите событие и выберите доступное действие."});
        return undefined;
      }
      const response = await api.POST("/api/events/{event_id}/actions", { params:{path:{event_id:id}},body:{action,comment:comment.trim()} });
      if (currentIdentity.current !== sendingIdentity) return undefined;
      if (response.error) { setActionError(apiError(response.error)); return undefined; }
      return { saved: response.data ?? true };
    } catch (error) { if (currentIdentity.current===sendingIdentity) setActionError(apiError(error)); return undefined; }
    finally { guard.current = false; setBusy(undefined); }
  }, [id,identity,ensureActor]);
  return { busy, actionError, send };
}
