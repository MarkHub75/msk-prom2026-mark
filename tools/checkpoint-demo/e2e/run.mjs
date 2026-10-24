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

async function selectRole(label) {
  const box = page.getByRole("combobox", { name: /роль/i });
  try {
    await box.waitFor({ state: "visible", timeout: STEP_MS });
  } catch {
    throw new StepFail(`переключатель роли (combobox «Роль») с вариантом «${label}»`);
  }
  await box.selectOption({ label });
}

async function noReload(fn) {
  const before = navigations;
  await fn();
  if (navigations !== before) throw new StepFail("без перезагрузки страницы", `перезагрузок: ${navigations - before}`);
}

const STEPS = [
  ["оператор: 4 сектора и «нет наблюдения» в секторе 4", async () => {
    await director("reset");
    await page.goto(`${FRONT_URL}/operator`);
    await selectRole("Оператор");
    for (const name of ["Сектор 1 · Прессовый участок", "Сектор 2 · Склад и погрузка", "Сектор 3 · Сборочный цех", "Сектор 4 · Ремонтная зона"]) {
      await expectUi(page.getByText(name), `плитка «${name}»`);
    }
    const tile = page.locator("a, button, li, article, section, div").filter({ hasText: "Сектор 4 · Ремонтная зона" }).filter({ hasText: /нет наблюдения/i });
    await expectUi(tile, "в плитке сектора 4 текст «Нет наблюдения»");
  }],
  ["demo next → жёлтое в ленте без перезагрузки", async () => {
    await noReload(async () => {
      await director("next");
      await expectUi(page.getByText("Бег 2,4 роста/с"), "в ленте событие «Бег 2,4 роста/с» (жёлтое) без F5");
    });
  }],
  ["карточка жёлтого", async () => {
    await page.getByText("Бег 2,4 роста/с").first().click();
    await expectState(async () => /\/events\/\d+/.test(page.url()), "переход на /events/:id");
    await expectUi(page.getByRole("button", { name: "Подтверждаю" }), "кнопка «Подтверждаю»");
  }],
  ["«Подтверждаю» → жёлтое confirmed", async () => {
    await page.getByRole("button", { name: "Подтверждаю" }).first().click();
    await expectState(async () => (await liveOf("yellow"))?.status === "confirmed", "мок: жёлтое в статусе confirmed");
    await expectUi(page.getByText("Подтверждено"), "статус «Подтверждено» на экране");
  }],
  ["demo next → захват экрана красным сам", async () => {
    await director("next");
    await expectUi(page.getByText("Зафиксировано падение"), "красное «Зафиксировано падение» на экране без клика");
    const red = await liveOf("red");
    await expectState(async () => page.url().includes(`/events/${red.id}`), `экран сам перешёл на /events/${red.id} (захват)`);
    await expectUi(page.getByRole("button", { name: "Подтверждаю" }), "кнопка «Подтверждаю» в захвате");
  }],
  ["«Подтверждаю» → красное мастеру", async () => {
    await page.getByRole("button", { name: "Подтверждаю" }).first().click();
    await expectState(async () => (await liveOf("red"))?.status === "sent_to_master", "мок: красное в sent_to_master");
    await expectUi(page.getByText("Передано мастеру"), "статус «Передано мастеру» на экране");
  }],
  ["мастер: «Принял, иду»", async () => {
    await selectRole("Мастер смены");
    if (!page.url().includes("/master")) await page.goto(`${FRONT_URL}/master`);
    await expectUi(page.getByText("Зафиксировано падение"), "красное во входящих мастера");
    await page.getByText("Зафиксировано падение").first().click();
    await expectUi(page.getByRole("button", { name: "Принял, иду" }), "кнопка «Принял, иду»");
    await page.getByRole("button", { name: "Принял, иду" }).first().click();
    await expectState(async () => (await liveOf("red"))?.status === "master_accepted", "мок: красное в master_accepted");
  }],
  ["мастер: «Решено» с комментарием", async () => {
    await expectUi(page.getByRole("button", { name: "Решено" }), "кнопка «Решено»");
    await page.getByRole("button", { name: "Решено" }).first().click();
    const box = page.getByRole("textbox");
    await expectUi(box, "поле комментария о мерах");
    await box.first().fill(COMMENT);
    const submit = page.getByRole("button", { name: /^(Решено|Отправить|Сохранить|Готово)$/ });
    await submit.last().click();
    await expectState(async () => (await liveOf("red"))?.status === "resolved", "мок: красное в resolved с комментарием");
  }],
  ["охрана труда: событие и история в журнале", async () => {
    await selectRole("Охрана труда");
    const link = page.getByRole("link", { name: "Журнал" });
    await expectUi(link, "пункт меню «Журнал»");
    await link.first().click();
    await expectUi(page.getByText("Зафиксировано падение"), "красное событие в журнале");
    await page.getByText("Зафиксировано падение").first().click();
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
      await expectUi(page.getByText("Бег 2,4 роста/с"), "новое жёлтое в ленте после разрыва WS");
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
