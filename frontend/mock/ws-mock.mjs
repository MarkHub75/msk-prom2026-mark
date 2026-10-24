// WebSocket mock for frontend work without the backend: every 3 s the next example message
// of contract/ws-examples.json goes to every client, `hello` first on connect.
import { readFileSync } from "node:fs";
import { WebSocketServer } from "ws";

const PORT = 4011;
const EVERY_MS = 3000;
const examples = JSON.parse(
  readFileSync(new URL("../../contract/ws-examples.json", import.meta.url), "utf8"),
);
const hello = examples.find((m) => m.type === "hello");
const rest = examples.filter((m) => m.type !== "hello");
const server = new WebSocketServer({ port: PORT, path: "/ws" });

server.on("connection", (socket, request) => {
  const role = new URL(request.url ?? "/ws", "http://localhost").searchParams.get("role");
  const now = new Date().toISOString();
  socket.send(JSON.stringify({ ...hello, at: now, data: { ...hello.data, role, server_now: now } }));
});

let next = 0;
setInterval(() => {
  const message = { ...rest[next % rest.length], at: new Date().toISOString() };
  next += 1;
  for (const client of server.clients) client.send(JSON.stringify(message));
}, EVERY_MS);

console.log(`ws mock on ws://127.0.0.1:${PORT}/ws`);
