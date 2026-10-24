import { createContext, useCallback, useContext, useEffect, useRef, useState, type FormEvent, type ReactNode } from "react";
import { useLocation } from "react-router-dom";
import { getActor, setActor as saveActor } from "../api/client";
import { useRole } from "../roles";
import "../styles/actor-identity.css";

interface ActorIdentity {
  actor: string;
  setActor: (value: string) => void;
  ensureActor: () => Promise<boolean>;
}
const ActorContext = createContext<ActorIdentity | undefined>(undefined);
export function useActorIdentity(): ActorIdentity {
  const value = useContext(ActorContext);
  if (!value) throw new Error("Actor identity requires the application shell.");
  return value;
}

export function ActorIdentityProvider({ children }: { children: ReactNode }) {
  const [actor, setActorState] = useState(getActor);
  const [open, setOpen] = useState(false);
  const [draft, setDraft] = useState("");
  const [error, setError] = useState("");
  const dialog = useRef<HTMLDialogElement>(null);
  const pending = useRef<{ promise: Promise<boolean>; resolve: (result: boolean) => void }>();
  const location = useLocation();
  const [role] = useRole();

  const setActor = useCallback((value: string) => {
    saveActor(value);
    setActorState(value);
  }, []);
  const finish = useCallback((accepted: boolean) => {
    pending.current?.resolve(accepted);
    pending.current = undefined;
    setOpen(false);
  }, []);
  const ensureActor = useCallback(() => {
    const name = getActor();
    if (name && [...name].length <= 60) return Promise.resolve(true);
    if (pending.current) return pending.current.promise;
    let resolve!: (result: boolean) => void;
    const promise = new Promise<boolean>(done => { resolve = done; });
    pending.current = { promise, resolve };
    setDraft(""); setError(""); setOpen(true);
    return promise;
  }, []);

  useEffect(() => {
    const element = dialog.current;
    if (open && element && !element.open) element.showModal();
    if (!open && element?.open) element.close();
  }, [open]);
  // A queued action must not follow the user to another event or role.
  useEffect(() => { finish(false); }, [location.pathname, role, finish]);
  useEffect(() => () => { pending.current?.resolve(false); }, []);

  const submit = (event: FormEvent) => {
    event.preventDefault();
    const name = draft.trim();
    if (!name || [...name].length > 60) { setError("Введите имя: от 1 до 60 символов."); return; }
    setActor(name);
    finish(true);
  };
  return <ActorContext.Provider value={{ actor, setActor, ensureActor }}>
    {children}
    <dialog ref={dialog} className="actor-dialog" aria-labelledby="actor-dialog-title" aria-describedby="actor-dialog-description" onCancel={event => { event.preventDefault(); finish(false); }}>
      <form onSubmit={submit}>
        <span className="actor-dialog-kicker">История действий</span>
        <h2 id="actor-dialog-title">Представьтесь для действия</h2>
        <p id="actor-dialog-description">Ваше имя будет записано в историю события. Достаточно указать его один раз на этом устройстве.</p>
        <label>Ваше имя<input autoFocus value={draft} onChange={event => setDraft(event.target.value)} maxLength={60} required autoComplete="name" placeholder="Имя и фамилия" /></label>
        {error && <p className="identity-error" role="alert">{error}</p>}
        <div className="actor-dialog-actions"><button className="button" type="button" onClick={() => finish(false)}>Отмена</button><button className="button button-light" type="submit">Сохранить имя и продолжить</button></div>
      </form>
    </dialog>
  </ActorContext.Provider>;
}
