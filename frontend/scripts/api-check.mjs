// Fails when src/api/schema.d.ts differs from what `npm run api:gen` makes of the contract.
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("..", import.meta.url));
const cli = join(root, "node_modules", "openapi-typescript", "bin", "cli.js");
const dir = mkdtempSync(join(tmpdir(), "api-check-"));
const fresh = join(dir, "schema.d.ts");
try {
  execFileSync(process.execPath, [cli, "../contract/openapi.json", "-o", fresh], {
    cwd: root,
    stdio: "ignore",
  });
  const normalize = (text) => text.replace(/\r\n/g, "\n");
  const want = normalize(readFileSync(fresh, "utf8"));
  const have = normalize(readFileSync(join(root, "src", "api", "schema.d.ts"), "utf8"));
  if (want !== have) {
    console.error("api:check: src/api/schema.d.ts is stale, run `npm run api:gen`");
    process.exit(1);
  }
  console.log("api:check: ok");
} finally {
  rmSync(dir, { recursive: true, force: true });
}
