// Director of the demo mock: the presenter sets the pace, nothing is published by a timer.
//   node bin/demo.mjs next [--force] | reset | status | ws-drop | fault <evidence-404|500|off>
const BASE = process.env.SW_MOCK_URL ?? "http://127.0.0.1:4010";
const [cmd, arg] = process.argv.slice(2);

const USAGE = `Команды:
  next [--force]                 опубликовать следующее событие истории (жёлтое, затем красное)
  reset                          вернуть мир в исходное состояние (рвёт WS: фронт перечитает экран)
  status                         что опубликовано и в каких статусах
  ws-drop                        разорвать все WS-соединения
  fault <evidence-404|500|off>   инъекция ошибок`;

async function call(method, path) {
  let res;
  try {
    res = await fetch(BASE + path, { method });
  } catch {
    console.error(`Мок не отвечает на ${BASE}: запустите mock.cmd (или npm run mock в tools/checkpoint-demo)`);
    process.exit(3);
  }
  return { status: res.status, body: await res.json() };
}

function printStatus(s) {
  console.log(`шаг истории: ${s.step} из ${s.story.length} (${s.story.join(" → ")})`);
  console.log(`автоэскалация: ${s.escalation ? "вкл" : "выкл"}; фолты: evidence-404=${s.faults.evidence404}, 500=${s.faults.error500}`);
  console.log(`открытых событий: ${s.open}; исторических: ${s.history}`);
  for (const e of s.live) console.log(`  #${e.id} ${e.story.padEnd(6)} ${e.status.padEnd(16)} вердикт=${e.verdict}  [${e.actions.join(", ")}]`);
  if (!s.live.length) console.log("  опубликованных событий истории нет: demo next");
}

const commands = {
  async next() {
    const force = process.argv.includes("--force") ? "?force=1" : "";
    const { status, body } = await call("POST", `/__demo/next${force}`);
    if (body.published) console.log(`опубликовано #${body.published.id}: ${body.published.notification_text}`);
    else console.log(body.message);
    return status === 200 ? 0 : 1;
  },
  async reset() {
    const { body } = await call("POST", "/__demo/reset");
    console.log(`мир восстановлен; разорвано WS: ${body.ws_dropped}`);
    printStatus(body.status);
    return 0;
  },
  async status() {
    printStatus((await call("GET", "/__demo/status")).body);
    return 0;
  },
  async "ws-drop"() {
    console.log(`разорвано WS: ${(await call("POST", "/__demo/ws-drop")).body.ws_dropped}`);
    return 0;
  },
  async fault() {
    if (!["evidence-404", "500", "off"].includes(arg)) {
      console.error("fault: evidence-404 | 500 | off");
      return 2;
    }
    const { body } = await call("POST", `/__demo/fault/${arg}`);
    console.log(`фолты: evidence-404=${body.faults.evidence404}, 500=${body.faults.error500}`);
    return 0;
  },
};

if (!commands[cmd]) {
  console.log(USAGE);
  process.exit(cmd ? 2 : 0);
}
process.exit(await commands[cmd]());
