// Hash routing keeps navigation/reloads on Pages independent of server rewrites.
import { writeFile } from "node:fs/promises";
const base = process.env.PAGES_BASE;
if (!base?.startsWith("/") || !base.endsWith("/")) throw new Error("PAGES_BASE must be /repository/");
const encoded = JSON.stringify(base).replaceAll("<", "\\u003c");
await writeFile("dist/404.html", `<!doctype html><html lang="ru"><meta charset="UTF-8"><title>Демо</title><script>
const base=${encoded};
const route=location.pathname.startsWith(base)?location.pathname.slice(base.length):"operator";
location.replace(base+"#/"+route+location.search);
</script><p>Открываем статическое демо…</p></html>\n`);
await writeFile("dist/.nojekyll", "");
