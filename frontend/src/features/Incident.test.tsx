import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../App";
import { subjectTitle } from "./Incident";
import { createFixtureEvents, fixtureMeta } from "../fixtures/data";
import { setRole } from "../roles";
import type { EventDetail, HumanAction } from "../api/types";

class QuietSocket { onopen = null; onmessage = null; onclose = null; onerror = null; close() {} }
beforeEach(() => {
  localStorage.clear(); sessionStorage.clear();
  history.replaceState({}, "", "/?review=real");
  vi.stubGlobal("WebSocket", QuietSocket);
  // jsdom omits native dialog methods; real focus/cancel behavior is browser-tested.
  Object.defineProperties(HTMLDialogElement.prototype, {
    showModal:{configurable:true,value:function(this:HTMLDialogElement) { this.setAttribute("open", ""); }},
    close:{configurable:true,value:function(this:HTMLDialogElement) { this.removeAttribute("open"); }},
  });
  act(() => setRole("operator"));
});
afterEach(() => { cleanup(); Reflect.deleteProperty(HTMLDialogElement.prototype,"showModal"); Reflect.deleteProperty(HTMLDialogElement.prototype,"close"); vi.restoreAllMocks(); vi.unstubAllGlobals(); });

function transport() {
  let detail: EventDetail = {...createFixtureEvents()[0],video_id:null,broadcast:null,allowed_actions:["view","confirm","false_alarm","send_to_master"]};
  let missing = false;
  const posts: Request[] = [];
  vi.stubGlobal("fetch", async (request:Request) => {
    const path = new URL(request.url).pathname;
    if (path === "/api/meta") return Response.json(fixtureMeta);
    if (request.method === "POST") {
      posts.push(request.clone());
      const { action } = await request.json() as {action:HumanAction};
      detail = {...detail,event:{...detail.event,status:action === "view"?"viewed":"sent_to_master",status_title:action === "view"?"Просмотрено":"Передано мастеру"},allowed_actions:action === "view"?["confirm","false_alarm","send_to_master"]:[]};
      return Response.json(detail);
    }
    if (missing) return Response.json({code:"not_found",message:"Событие не найдено",details:{}},{status:404});
    return Response.json(detail);
  });
  return {posts,remove:() => {missing=true;}};
}
function openIncident() { return render(<MemoryRouter initialEntries={["/events/41"]}><App /></MemoryRouter>); }

describe("incident identity and authoritative refresh", () => {
  it("does not invent an actor or post automatic view before explicit identity; resumes the requested action", async () => {
    const server = transport(); openIncident();
    const confirm = await screen.findByRole("button",{name:/Подтвердить/});
    expect(server.posts).toHaveLength(0);
    fireEvent.click(confirm);
    let dialog = screen.getByRole("dialog",{name:"Представьтесь для действия"});
    fireEvent.click(within(dialog).getByRole("button",{name:"Отмена"}));
    await waitFor(() => expect(confirm.hasAttribute("disabled")).toBe(false));
    expect(server.posts).toHaveLength(0);
    fireEvent.click(confirm);
    dialog = screen.getByRole("dialog",{name:"Представьтесь для действия"});
    fireEvent.change(within(dialog).getByLabelText("Ваше имя"),{target:{value:"   "}});
    fireEvent.submit(dialog.querySelector("form")!);
    expect(server.posts).toHaveLength(0);
    expect(within(dialog).getByRole("alert").textContent).toContain("Введите имя");
    fireEvent.change(within(dialog).getByLabelText("Ваше имя"),{target:{value:"Иван Петров"}});
    fireEvent.submit(dialog.querySelector("form")!);
    await waitFor(() => expect(server.posts).toHaveLength(1));
    expect(server.posts[0].headers.get("X-Actor")).toBe(encodeURIComponent("Иван Петров"));
    expect((await server.posts[0].json()).action).toBe("confirm");
    expect(localStorage.getItem("safewatch.actor")).toBe("Иван Петров");
  });

  it("removes prior event details and actions when a fresh REST read returns 404 after an action", async () => {
    const server = transport();
    localStorage.setItem("safewatch.actor","Иван Петров");
    const view = openIncident();
    await waitFor(() => expect(server.posts).toHaveLength(1));
    await screen.findByText("Просмотрено");
    expect(view.container.querySelectorAll("button[data-action]").length).toBeGreaterThan(0);
    server.remove();
    fireEvent.click(screen.getByRole("button",{name:"Обновить"}));
    await screen.findByText("Событие не найдено");
    expect(view.container.querySelectorAll("button[data-action]")).toHaveLength(0);
    expect(screen.queryByText("Просмотрено")).toBeNull();
  });
});

describe("episode codes in words", () => {
  it("names the subject like the HUD does, never a raw code", () => {
    expect(subjectTitle("track:3")).toBe("человек #3");
    expect(subjectTitle("pair:3-7")).toBe("человек #3 и техника #7");
    expect(subjectTitle("zone:3-2")).toBe("человек #3 в зоне #2");
    expect(subjectTitle("fire")).toBe("огонь");
  });
});
