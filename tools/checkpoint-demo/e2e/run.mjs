// Browser e2e of the demo story on the private stack (mock 4110/4111, Vite 5174).
//   node e2e/run.mjs [--front DIR | --fixture] [--no-bugs] [--headed]
// --fixture checks the harness itself on e2e/fixture-front (use with --no-bugs).
// Selectors use visible text and ARIA roles only. A screenshot per step goes to e2e/screens/;
// a failed step adds a line to e2e/FRONT_BUGS.md (the frontend is never fixed from here).
// Prints a JSON summary on the last line. Exit: 0 all steps passed, 1 a step failed, 3 skipped.
import { appendFileSync, copyFileSync, existsSync, mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { chromium } from "playwright";
import { FIXTURE_FRONT, FRONT_URL, HERE, director, ensureMock, ensureVite, pickFront } from "./stack.mjs";

const args = process.argv.slice(2);
const opt = (name, def) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : def;
};
const SCREENS = join(HERE, "e2e", "screens", args.includes("--fixture") ? "fixture" : "");
const BUGS = join(HERE, "e2e", "FRONT_BUGS.md");
const STEP_MS = 10000;
const COMMENT = "Пострадавших нет, рабочее место осмотрено";
const ACTOR = "Иван Петров";
const time = () => new Date().toLocaleTimeString("ru-RU", { timeZone: "Europe/Moscow", hour: "2-digit", minute: "2-digit" });
const stamp = () => new Date().toISOString().replace(/[-:]/g, "").slice(0, 13);

function finish(summary, code) {
  console.log(JSON.stringify(summary));
  process.exit(code);
}

const front = pickFront(args.includes("--fixture") ? FIXTURE_FRONT : opt("--front", undefined));
if (!front.dir) finish({ result: "SKIP", passed: 0, total: 0, reason: front.reason }, 3);
await ensureMock();
await ensureVite(front.dir, front.viteFrom);
mkdirSync(SCREENS, { recursive: true });

const live = async () => (await director("status", "GET")).live;
const liveOf = async (story) => (await live()).find((e) => e.story === story);
class StepFail extends Error {
  constructor(expected, extra = "") {
    super(expected);
    this.extra = extra;
  }
}
const expectUi = async (locator, expected) => {
  try {
    await locator.first().waitFor({ state: "visible", timeout: STEP_MS });
  } catch {
    throw new StepFail(expected);
  }
};
const expectState = async (pred, expected) => {
  const end = Date.now() + STEP_MS;
  while (Date.now() < end) {
    if (await pred()) return;
    await new Promise((r) => setTimeout(r, 300));
  }
  throw new StepFail(expected);
};

const browser = await chromium.launch({ headless: !args.includes("--headed") });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, locale: "ru-RU" });
let navigations = 0;
page.on("framenavigated", (f) => {
  if (f === page.mainFrame()) navigations += 1;
});

// Role switch: a combobox «Роль» (fixture, mobile) or role tabs nav «Выбор роли» (control-room top bar since 8161719d).
async function selectRole(label) {
  const box = page.getByRole("combobox", { name: /роль/i });
  // Tabs use the short title: «Мастер смены» in the combobox is «Мастер» on the tab.
  const short = label.split(" ")[0];
  const tab = page.getByRole("navigation", { name: "Выбор роли" }).getByRole("button", { name: new RegExp(`^(${label}|${short})$`) });
  try {
    await box.or(tab).first().waitFor({ state: "visible", timeout: STEP_MS });
  } catch {
    throw new StepFail(`переключатель роли (combobox «Роль» или вкладки «Выбор роли») с вариантом «${label}»`);
  }
  if (await tab.isVisible()) await tab.click();
  else await box.selectOption({ label });
}

async function noReload(fn) {
  const before = navigations;
  await fn();
  if (navigations !== before) throw new StepFail("без перезагрузки страницы", `перезагрузок: ${navigations - before}`);
}

// Texts of the control-room frontend (origin/front/control-room): «Диспетчерская», «Очередь тревог»,
// «Открыть событие», «Подтвердить», «Принять в работу», «Решено» / «Принятые меры».
const CONFIRM = /^(Подтвердить|Подтверждаю)(\s|$)/;
const queue = () => page.getByRole("complementary", { name: "Очередь тревог" });
async function click(locator, expected) {
  await expectUi(locator, expected);
  try {
    await locator.first().click({ timeout: 3000 });
  } catch {
    throw new StepFail(`${expected}: элемент виден, но клик не проходит (перекрыт или неактивен)`);
  }
  // The control-room front asks for a name before the first action (it goes to the history).
  const intro = page.getByRole("dialog").filter({ hasText: "Представьтесь для действия" });
  if (await intro.first().waitFor({ state: "visible", timeout: 1000 }).then(() => true, () => false)) {
    await intro.getByRole("textbox").first().fill(ACTOR);
    await intro.getByRole("button", { name: /Сохранить имя/ }).first().click();
  }
}

const STEPS = [
  ["оператор: 4 сектора и «нет наблюдения» в секторе 4", async () => {
    await director("reset");
    await page.goto(`${FRONT_URL}/operator`);
    await selectRole("Оператор");
    await expectUi(page.getByRole("heading", { name: "Диспетчерская" }), "заголовок «Диспетчерская»");
    const sectors = page.getByRole("region", { name: "Секторы производства" });
    for (const name of ["Прессовый участок", "Склад и погрузка", "Сборочный цех", "Ремонтная зона"]) {
      await expectUi(sectors.getByRole("button", { name: new RegExp(name) }), `плитка сектора «${name}» в «Секторы производства»`);
    }
    await expectUi(sectors.getByRole("button", { name: /Ремонтная зона.*Нет наблюдения/i }), "у сектора 4 «Нет наблюдения»");
    await expectUi(queue(), "панель «Очередь тревог»");
  }],
  ["demo next → жёлтое в «Очереди тревог» без перезагрузки", async () => {
    await noReload(async () => {
      await director("next");
      await expectUi(queue().getByRole("button", { name: /Бег и резкие перемещения/ }), "в «Очереди тревог» событие «Бег и резкие перемещения» без F5");
    });
  }],
  ["«Открыть событие» → карточка жёлтого", async () => {
    await click(queue().getByRole("button", { name: /Бег и резкие перемещения/ }), "событие в очереди");
    await click(page.getByRole("link", { name: "Открыть событие" }), "ссылка «Открыть событие»");
    const yellow = await liveOf("yellow");
    await expectState(async () => page.url().includes(`/events/${yellow.id}`), `переход на /events/${yellow.id}`);
    await expectUi(page.getByRole("button", { name: CONFIRM }), "кнопка «Подтвердить»");
  }],
  ["«Подтвердить» → жёлтое confirmed", async () => {
    await click(page.getByRole("button", { name: CONFIRM }), "кнопка «Подтвердить»");
    await expectState(async () => (await liveOf("yellow"))?.status === "confirmed", "мок: жёлтое в статусе confirmed");
    await expectUi(page.getByText("Подтверждено"), "статус «Подтверждено» на экране");
  }],
  ["demo next → захват экрана красным сам", async () => {
    await director("next");
    const red = await liveOf("red");
    const dialog = page.getByRole("alertdialog").filter({ hasText: "Зафиксировано падение" });
    try {
      await dialog.first().waitFor({ state: "visible", timeout: STEP_MS });
    } catch {
      if (!page.url().includes(`/events/${red.id}`)) throw new StepFail("сам открылся захват экрана (alertdialog с «Зафиксировано падение» или /events/:id красного)");
    }
  }],
  ["«Подтвердить» → красное мастеру", async () => {
    await click(page.getByRole("button", { name: CONFIRM }), "кнопка «Подтвердить» в захвате");
    await expectState(async () => (await liveOf("red"))?.status === "sent_to_master", "мок: красное в sent_to_master");
    await expectUi(page.getByText("Передано мастеру"), "статус «Передано мастеру» на экране");
  }],
  ["мастер: «Принять в работу»", async () => {
    await selectRole("Мастер смены");
    const red = await liveOf("red");
    await page.waitForTimeout(1000);
    // The control-room front may open the card of the new task by itself after the role switch.
    if (!new RegExp(`/events/${red.id}(\\?|$)`).test(page.url())) {
      if (!page.url().includes("/master")) await page.goto(`${FRONT_URL}/master`);
      await click(page.getByRole("link", { name: /Зафиксировано падение/ }), "красное во входящих мастера");
    }
    await click(page.getByRole("button", { name: /^Принять в работу|^Принял, иду/ }), "кнопка «Принять в работу»");
    await expectState(async () => (await liveOf("red"))?.status === "master_accepted", "мок: красное в master_accepted");
  }],
  ["мастер: «Решено» с «Принятые меры»", async () => {
    let box = page.getByRole("textbox", { name: /Принятые меры/ });
    if (!(await box.first().isVisible().catch(() => false))) {
      await click(page.getByRole("button", { name: /^Решено/ }), "кнопка «Решено»");
      box = page.getByRole("textbox", { name: /Принятые меры/ });
    }
    await expectUi(box, "поле «Принятые меры»");
    await box.first().fill(COMMENT);
    await click(page.getByRole("button", { name: /^(Решено|Отправить|Сохранить|Готово)(\s|$)/ }).last(), "кнопка отправки «Решено»");
    await expectState(async () => (await liveOf("red"))?.status === "resolved", "мок: красное в resolved с комментарием");
  }],
  ["охрана труда: событие и история в журнале", async () => {
    await selectRole("Охрана труда");
    await click(page.getByRole("link", { name: "Журнал" }), "пункт меню «Журнал»");
    const red = await liveOf("red");
    await click(page.getByRole("link", { name: new RegExp(`Открыть историю события ${red.id}$`) }), `в журнале «Открыть историю события ${red.id}»`);
    await expectUi(page.getByText(COMMENT), `комментарий мастера «${COMMENT}» в истории`);
    await expectUi(page.getByText(/Решено/), "запись «Решено» в истории");
  }],
  ["demo ws-drop → события снова приходят", async () => {
    await director("reset?keep_ws=1");
    await selectRole("Оператор");
    await page.goto(`${FRONT_URL}/operator`);
    await expectState(async () => (await director("status", "GET")).ws_clients?.operator > 0, "оператор подключён к WS");
    await director("ws-drop");
    await expectState(async () => (await director("status", "GET")).ws_clients?.operator > 0, "оператор переподключился к WS после разрыва");
    await noReload(async () => {
      await director("next");
      await expectUi(queue().getByRole("button", { name: /Бег и резкие перемещения/ }), "новое жёлтое в «Очереди тревог» после разрыва WS");
    });
  }],
];

let passed = 0;
let failed = null;
for (const [i, [name, fn]] of STEPS.entries()) {
  const shot = join(SCREENS, `${String(i + 1).padStart(2, "0")}.jpg`);
  try {
    await fn();
    await page.screenshot({ path: shot, type: "jpeg", quality: 60 });
    passed += 1;
    console.log(`PASS ${i + 1}. ${name}`);
  } catch (e) {
    await page.screenshot({ path: shot, type: "jpeg", quality: 60 }).catch(() => {});
    const failShot = `fail-${stamp()}-${String(i + 1).padStart(2, "0")}.jpg`;
    if (existsSync(shot)) copyFileSync(shot, join(SCREENS, failShot));
    const seen = (await page.locator("body").innerText().catch(() => "")).replace(/\s+/g, " ").trim().slice(0, 200);
    const expected = e instanceof StepFail ? e.message : `${e.name}: ${e.message.split("\n")[0]}`;
    failed = { step: i + 1, name, expected, seen: `${page.url().replace(FRONT_URL, "")} | ${e.extra ?? ""}${seen}`, shot: `screens/${args.includes("--fixture") ? "fixture/" : ""}${failShot}` };
    console.log(`FAIL ${i + 1}. ${name}: ожидалось ${expected}`);
    break;
  }
}
await browser.close();

const summary = { result: failed ? "FAIL" : "PASS", passed, total: STEPS.length, front: front.dir, failed };
if (failed && !args.includes("--no-bugs")) {
  if (!existsSync(BUGS)) writeFileSync(BUGS, "# FRONT_BUGS: провалы e2e фронта против мока 4110/4111\n\nСтрока на провал: время МСК · шаг · ожидалось · видно (путь | текст страницы) · скриншот. Фронт отсюда не чиним. Шаги после провала не проверялись.\n\n");
  appendFileSync(BUGS, `- ${time()} · шаг ${failed.step} «${failed.name}» · ожидалось: ${failed.expected} · видно: ${failed.seen} · скриншот: ${failed.shot}\n`);
}
finish(summary, failed ? 1 : 0);
