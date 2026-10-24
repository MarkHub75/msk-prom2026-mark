// Reference frontend for checking the e2e harness itself (not a product screen): the smallest
// UI that walks the demo story through the contract. Plain JS, served by Vite.
const API = import.meta.env.VITE_API_BASE;
const WS_URL = import.meta.env.VITE_WS_URL;
const HOME = { operator: "/operator", master: "/master", ohs: "/ohs/journal", management: "/operator", admin: "/operator" };
const MENU = { operator: [["/operator", "Диспетчерская"]], master: [["/master", "Мои события"]], ohs: [["/ohs/journal", "Журнал"]] };
const BUTTONS = { view: null, confirm: "Подтвердить", false_alarm: "Ложное срабатывание", send_to_master: "Передать мастеру", accept: "Принять в работу", resolve: "Решено" };
let role = localStorage.getItem("fixture.role") || "operator";
let socket;

const el = (tag, attrs = {}, ...kids) => {
  const n = document.createElement(tag);
  Object.assign(n, attrs);
  n.append(...kids.flat().filter((k) => k != null));
  return n;
};
const api = async (path, init = {}) => {
  const r = await fetch(API + path, { ...init, headers: { "X-Role": role, "Content-Type": "application/json", ...(init.headers ?? {}) } });
  return r.json();
};
const go = (path) => {
  history.pushState(null, "", path);
  render();
};

function connect() {
  socket?.close();
  const s = new WebSocket(`${WS_URL}?role=${role}`);
  socket = s;
  s.onmessage = (e) => {
    const m = JSON.parse(e.data);
    if (m.type === "notification" && m.data.takeover && role === "operator") {
      history.pushState(null, "", `/events/${m.data.event_id}?takeover=1`);
      render().then(() => document.body.append(el("div", { role: "alertdialog", ariaLabel: "Критическое событие", textContent: m.data.text })));
    }
    else if (m.type.startsWith("event.") || m.type.endsWith(".state")) render();
  };
  s.onclose = () => {
    if (socket === s) setTimeout(connect, 1000);
  };
}

async function header(meta) {
  const select = el("select", { id: "role", onchange: (e) => {
    role = e.target.value;
    localStorage.setItem("fixture.role", role);
    connect();
    go(HOME[role]);
  } }, meta.roles.map((r) => el("option", { value: r.id, selected: r.id === role, textContent: r.title })));
  const nav = el("nav", {}, (MENU[role] ?? []).map(([href, title]) => el("a", { href, textContent: title, onclick: (e) => (e.preventDefault(), go(href)) })));
  return el("header", {}, el("strong", { textContent: "SafeWatch (фикстура e2e)" }), nav, el("label", { htmlFor: "role", textContent: "Роль" }), select);
}

const eventLink = (e) => el("li", {}, el("a", { href: `/events/${e.id}`, textContent: `${e.reason_text} · ${e.status_title}`, onclick: (ev) => (ev.preventDefault(), go(`/events/${e.id}`)) }));

async function screen() {
  const path = location.pathname;
  if (path === "/operator") {
    const d = await api("/api/operator/dashboard");
    const queue = el("aside", { ariaLabel: "Очередь тревог" }, el("h2", { textContent: "Очередь тревог" }),
      d.feed.map((e) => el("button", { textContent: `${e.title} ${e.reason_text}`, onclick: () => queue.append(el("a", { href: `/events/${e.id}`, textContent: "Открыть событие", onclick: (ev) => (ev.preventDefault(), go(`/events/${e.id}`)) })) })));
    return el("main", {}, el("h1", { textContent: "Диспетчерская" }),
      el("section", { ariaLabel: "Секторы производства" }, d.sectors.map((s) => el("button", { textContent: `${s.name} ${s.reason_text || s.state}` }))),
      queue);
  }
  if (path === "/master") {
    const d = await api("/api/master/inbox");
    return el("main", {}, el("ul", {}, [...d.active, ...d.recent_resolved].map(eventLink)));
  }
  if (path === "/ohs/journal") {
    const d = await api("/api/events?limit=50");
    return el("main", {}, el("ul", {}, d.items.map((e) => el("li", {}, e.reason_text, " ", el("a", { href: `/events/${e.id}`, textContent: `Открыть историю события ${e.id}`, onclick: (ev) => (ev.preventDefault(), go(`/events/${e.id}`)) })))));
  }
  const m = path.match(/^\/events\/(\d+)$/);
  if (m) {
    const d = await api(`/api/events/${m[1]}`);
    const act = async (action, comment = "") => {
      await api(`/api/events/${m[1]}/actions`, { method: "POST", body: JSON.stringify({ action, comment }) });
      render();
    };
    const buttons = d.allowed_actions.filter((a) => BUTTONS[a]).map((a) => el("button", { textContent: BUTTONS[a], onclick: () => {
      if (a !== "resolve") return act(a);
      const box = el("textarea", { ariaLabel: "Принятые меры" });
      document.querySelector("main").append(box, el("button", { textContent: "Отправить", onclick: () => act("resolve", box.value) }));
    } }));
    return el("main", {},
      el("h2", { textContent: d.event.notification_text }),
      el("p", { textContent: d.event.status_title }),
      el("ol", {}, d.actions.map((a) => el("li", { textContent: `${a.action} · ${a.to_status ?? ""} ${a.comment}` }))),
      buttons);
  }
  return el("main", {}, el("p", { textContent: "нет экрана" }));
}

async function render() {
  const meta = await api("/api/meta");
  document.body.replaceChildren(await header(meta), await screen());
}

window.onpopstate = render;
connect();
render();
