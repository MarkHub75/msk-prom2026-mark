"""Small, dependency-light client for the LinQ JupyterHub.

Credentials come from .env (LINQ_JUPYTER_URL / _USER / _PASSWORD, optional
LINQ_JUPYTER_TOKEN) and are never printed.

CLI:
    python tools/linq/jupyter_remote.py info
    python tools/linq/jupyter_remote.py exec "uname -a" [--timeout 600] [--cwd DIR]
    python tools/linq/jupyter_remote.py exec @local_script.sh
    python tools/linq/jupyter_remote.py py "print(1+1)" [--timeout 600]
    python tools/linq/jupyter_remote.py pyfile local_script.py [--timeout 600]
    python tools/linq/jupyter_remote.py upload LOCAL REMOTE
    python tools/linq/jupyter_remote.py download REMOTE LOCAL
    python tools/linq/jupyter_remote.py ls [REMOTE_DIR]

Library:
    from jupyter_remote import JupyterRemote
    jr = JupyterRemote.from_env()
    rc, out, err = jr.exec("nproc")
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import websocket

REPO = Path(__file__).resolve().parents[2]
CHUNK = 4 * 1024 * 1024  # Contents API chunk size (raw bytes before base64)


class JupyterError(RuntimeError):
    pass


def _load_env() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:  # pragma: no cover
        return
    load_dotenv(REPO / ".env")


class JupyterRemote:
    def __init__(self, base_url: str, user: str | None, password: str | None,
                 token: str | None = None, verbose: bool = False):
        self.base = base_url.rstrip("/") + "/"
        self.user = user
        self.password = password
        self.verbose = verbose
        self.s = requests.Session()
        self.s.headers["User-Agent"] = "mosprom-linq-client/1"
        self.server: str | None = None  # e.g. http://host/user/<name>/
        self.kind = "unknown"
        self._kernel_id: str | None = None
        if token:
            self.s.headers["Authorization"] = f"token {token}"
        self._login()

    # ------------------------------------------------------------------ auth
    @classmethod
    def from_env(cls, verbose: bool = False) -> "JupyterRemote":
        _load_env()
        url = os.environ.get("LINQ_JUPYTER_URL")
        if not url:
            raise JupyterError("LINQ_JUPYTER_URL is not set in .env")
        return cls(url, os.environ.get("LINQ_JUPYTER_USER"),
                   os.environ.get("LINQ_JUPYTER_PASSWORD"),
                   os.environ.get("LINQ_JUPYTER_TOKEN") or None, verbose)

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(f"[jr] {msg}", file=sys.stderr)

    def _xsrf(self, path: str | None = None) -> str | None:
        # Hub and single-user server each set their own _xsrf cookie; pick the
        # one with the longest path that prefixes the target path.
        target = path if path is not None else (urlparse(self.server).path if self.server else "/hub/")
        best, best_len = None, -1
        for c in self.s.cookies:
            if c.name == "_xsrf" and target.startswith(c.path or "/") and len(c.path or "/") > best_len:
                best, best_len = c.value, len(c.path or "/")
        return best

    def _login(self) -> None:
        r = self.s.get(self.base, timeout=30)
        r.raise_for_status()
        if "/hub/" in r.url or "jupyterhub" in r.text.lower():
            self.kind = "jupyterhub"
            self._hub_login()
        else:
            self.kind = "jupyter-server"
            self.server = self.base
            if "login" in r.url and self.password:
                self._server_login(r)
        # warm-up: obtain _xsrf for the single-user server and check API
        r = self.s.get(urljoin(self.server, "api/status"), timeout=30)
        if r.status_code != 200:
            raise JupyterError(f"API not reachable after login: HTTP {r.status_code}")
        self.s.get(urljoin(self.server, "lab"), timeout=30)
        self._log(f"kind={self.kind} server={self.server}")

    def _hub_login(self) -> None:
        login_url = urljoin(self.base, "hub/login")
        r = self.s.get(login_url, timeout=30)
        m = re.search(r'name="_xsrf"\s+value="([^"]+)"', r.text)
        data = {"username": self.user or "", "password": self.password or ""}
        if m:
            data["_xsrf"] = m.group(1)
        r = self.s.post(login_url, data=data, timeout=60, allow_redirects=True)
        if "hub/login" in urlparse(r.url).path and r.status_code in (200, 403):
            raise JupyterError("JupyterHub login rejected (check LINQ_JUPYTER_USER/PASSWORD)")
        # who am I
        hdr = {"X-XSRFToken": self._xsrf("/hub/") or ""}
        me = self.s.get(urljoin(self.base, "hub/api/user"), headers=hdr, timeout=30)
        name = me.json().get("name") if me.ok else self.user
        self.server = urljoin(self.base, f"user/{name}/")
        # make sure the single-user server is running
        st = self.s.get(urljoin(self.server, "api/status"), timeout=30)
        if st.status_code != 200:
            self._log("starting single-user server")
            self.s.post(urljoin(self.base, f"hub/api/users/{name}/server"),
                        headers=hdr, timeout=60)
            for _ in range(60):
                time.sleep(2)
                if self.s.get(urljoin(self.server, "api/status"), timeout=30).status_code == 200:
                    break
            else:
                raise JupyterError("single-user server did not start in 120 s")
        # spawn page sets the per-server _xsrf cookie
        self.s.get(self.server, timeout=30)

    def _server_login(self, r: requests.Response) -> None:
        m = re.search(r'name="_xsrf"\s+value="([^"]+)"', r.text)
        data = {"password": self.password}
        if m:
            data["_xsrf"] = m.group(1)
        self.s.post(urljoin(self.base, "login"), data=data, timeout=30)

    # --------------------------------------------------------------- helpers
    def _api(self, method: str, path: str, **kw) -> requests.Response:
        headers = kw.pop("headers", {})
        x = self._xsrf()
        if x:
            headers["X-XSRFToken"] = x
        kw.setdefault("timeout", 120)
        r = self.s.request(method, urljoin(self.server, path.lstrip("/")), headers=headers, **kw)
        if r.status_code >= 400:
            raise JupyterError(f"{method} {path}: HTTP {r.status_code} {r.text[:300]}")
        return r

    # ---------------------------------------------------------------- kernel
    def kernel(self) -> str:
        if self._kernel_id:
            return self._kernel_id
        r = self._api("POST", "api/kernels", json={"name": "python3"})
        self._kernel_id = r.json()["id"]
        self._log(f"kernel {self._kernel_id}")
        return self._kernel_id

    def shutdown_kernel(self) -> None:
        if self._kernel_id:
            try:
                self._api("DELETE", f"api/kernels/{self._kernel_id}")
            except JupyterError:
                pass
            self._kernel_id = None

    def _ws(self) -> websocket.WebSocket:
        kid = self.kernel()
        u = urlparse(self.server)
        scheme = "wss" if u.scheme == "https" else "ws"
        url = f"{scheme}://{u.netloc}{u.path}api/kernels/{kid}/channels"
        cookie = "; ".join(f"{c.name}={c.value}" for c in self.s.cookies)
        headers = [f"Cookie: {cookie}"]
        if "Authorization" in self.s.headers:
            headers.append(f"Authorization: {self.s.headers['Authorization']}")
        x = self._xsrf()
        if x:
            headers.append(f"X-XSRFToken: {x}")
        # No Origin header: behind the tunnel nginx rewrites Host (drops the port),
        # so any Origin we send fails Jupyter's same-origin check.
        return websocket.create_connection(url, header=headers, timeout=30, suppress_origin=True)

    def py(self, code: str, timeout: float = 600, stream: bool = False) -> tuple[bool, str, str]:
        """Execute code in the remote kernel. Returns (ok, stdout, stderr/traceback)."""
        ws = self._ws()
        msg_id = uuid.uuid4().hex
        ws.send(json.dumps({
            "header": {"msg_id": msg_id, "username": "client", "session": uuid.uuid4().hex,
                       "msg_type": "execute_request", "version": "5.3"},
            "parent_header": {}, "metadata": {}, "channel": "shell",
            "content": {"code": code, "silent": False, "store_history": False,
                        "user_expressions": {}, "allow_stdin": False, "stop_on_error": True},
        }))
        out, err, ok = [], [], True
        deadline = time.time() + timeout
        done_iopub = done_shell = False
        try:
            while not (done_iopub and done_shell):
                left = deadline - time.time()
                if left <= 0:
                    self._api("POST", f"api/kernels/{self._kernel_id}/interrupt")
                    raise JupyterError(f"timeout after {timeout} s (kernel interrupted)")
                ws.settimeout(min(left, 30))
                try:
                    raw = ws.recv()
                except websocket.WebSocketTimeoutException:
                    continue
                m = json.loads(raw)
                if m.get("parent_header", {}).get("msg_id") != msg_id:
                    continue
                t, c = m["msg_type"], m["content"]
                if t == "stream":
                    (out if c["name"] == "stdout" else err).append(c["text"])
                    if stream:
                        print(c["text"], end="", file=sys.stdout if c["name"] == "stdout" else sys.stderr, flush=True)
                elif t in ("execute_result", "display_data"):
                    txt = c.get("data", {}).get("text/plain", "")
                    out.append(txt + "\n")
                    if stream:
                        print(txt, flush=True)
                elif t == "error":
                    ok = False
                    tb = re.sub(r"\x1b\[[0-9;]*m", "", "\n".join(c.get("traceback", [])))
                    err.append(tb or f"{c.get('ename')}: {c.get('evalue')}")
                elif t == "status" and c.get("execution_state") == "idle":
                    done_iopub = True
                elif t == "execute_reply":
                    done_shell = True
                    if c.get("status") != "ok":
                        ok = False
        finally:
            ws.close()
        return ok, "".join(out), "".join(err)

    def exec(self, cmd: str, timeout: float = 600, cwd: str | None = None) -> tuple[int, str, str]:
        """Run a shell command remotely. Returns (returncode, stdout, stderr)."""
        code = (
            "import subprocess, json, os\n"
            f"_p = subprocess.run({cmd!r}, shell=True, capture_output=True, text=True, "
            f"timeout={timeout!r}, cwd={cwd!r} and os.path.expanduser({cwd!r}), executable='/bin/bash')\n"
            "print('__JR__' + json.dumps({'rc': _p.returncode, 'out': _p.stdout, 'err': _p.stderr}))\n"
        )
        ok, out, err = self.py(code, timeout=timeout + 30)
        m = re.search(r"__JR__(\{.*\})\s*$", out, re.S)
        if not ok or not m:
            return 255, out, err or "remote exec failed"
        d = json.loads(m.group(1))
        return d["rc"], d["out"], d["err"]

    # -------------------------------------------------------------- contents
    def ls(self, path: str = "") -> list[dict]:
        r = self._api("GET", f"api/contents/{path.strip('/')}", params={"content": 1})
        d = r.json()
        return d["content"] if d["type"] == "directory" else [d]

    def mkdir(self, path: str) -> None:
        parts = [p for p in path.strip("/").split("/") if p]
        cur = ""
        for p in parts:
            cur = f"{cur}/{p}" if cur else p
            try:
                self._api("GET", f"api/contents/{cur}", params={"content": 0})
            except JupyterError:
                self._api("PUT", f"api/contents/{cur}", json={"type": "directory"})

    def upload(self, local: str | Path, remote: str, progress: bool = True) -> None:
        local = Path(local)
        remote = remote.strip("/")
        if "/" in remote:
            self.mkdir(remote.rsplit("/", 1)[0])
        size = local.stat().st_size
        with local.open("rb") as f:
            if size <= CHUNK:
                self._api("PUT", f"api/contents/{remote}", json={
                    "type": "file", "format": "base64", "name": remote.rsplit("/", 1)[-1],
                    "content": base64.b64encode(f.read()).decode()}, timeout=600)
                return
            n, sent = 1, 0
            while True:
                buf = f.read(CHUNK)
                sent += len(buf)
                last = sent >= size
                self._api("PUT", f"api/contents/{remote}", json={
                    "type": "file", "format": "base64", "name": remote.rsplit("/", 1)[-1],
                    "chunk": -1 if last else n, "content": base64.b64encode(buf).decode()},
                    timeout=600)
                if progress:
                    print(f"\r[upload] {remote}: {sent / size:6.1%}", end="", file=sys.stderr)
                if last:
                    break
                n += 1
        if progress:
            print(file=sys.stderr)

    def download(self, remote: str, local: str | Path) -> int:
        local = Path(local)
        local.parent.mkdir(parents=True, exist_ok=True)
        r = self.s.get(urljoin(self.server, f"files/{remote.strip('/')}"), stream=True, timeout=600)
        if r.status_code >= 400:
            raise JupyterError(f"download {remote}: HTTP {r.status_code}")
        n = 0
        with local.open("wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
                n += len(chunk)
        return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-v", "--verbose", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("info")
    p = sub.add_parser("exec"); p.add_argument("command"); p.add_argument("--timeout", type=float, default=600); p.add_argument("--cwd")
    p = sub.add_parser("py"); p.add_argument("code"); p.add_argument("--timeout", type=float, default=600)
    p = sub.add_parser("pyfile"); p.add_argument("file"); p.add_argument("--timeout", type=float, default=3600)
    p = sub.add_parser("upload"); p.add_argument("local"); p.add_argument("remote")
    p = sub.add_parser("download"); p.add_argument("remote"); p.add_argument("local")
    p = sub.add_parser("ls"); p.add_argument("path", nargs="?", default="")
    a = ap.parse_args()

    jr = JupyterRemote.from_env(verbose=a.verbose)
    try:
        if a.cmd == "info":
            print(json.dumps({"kind": jr.kind, "server": jr.server}, ensure_ascii=False))
        elif a.cmd == "exec":
            # "@file.sh" reads the command from a local file (avoids shell-quoting hell on Windows)
            cmd = Path(a.command[1:]).read_text(encoding="utf-8") if a.command.startswith("@") else a.command
            rc, out, err = jr.exec(cmd, timeout=a.timeout, cwd=a.cwd)
            sys.stdout.write(out)
            sys.stderr.write(err)
            return rc
        elif a.cmd in ("py", "pyfile"):
            code = a.code if a.cmd == "py" else Path(a.file).read_text(encoding="utf-8")
            ok, out, err = jr.py(code, timeout=a.timeout, stream=True)
            if err and not ok:
                sys.stderr.write(err)
            return 0 if ok else 1
        elif a.cmd == "upload":
            jr.upload(a.local, a.remote)
            print(f"uploaded {a.local} -> {a.remote}")
        elif a.cmd == "download":
            n = jr.download(a.remote, a.local)
            print(f"downloaded {a.remote} -> {a.local} ({n} bytes)")
        elif a.cmd == "ls":
            for e in sorted(jr.ls(a.path), key=lambda e: (e["type"] != "directory", e["name"])):
                size = e.get("size") or ""
                print(f"{e['type'][:3]:3} {str(size):>12} {e.get('last_modified', '')[:19]}  {e['path']}")
    finally:
        jr.shutdown_kernel()
    return 0


if __name__ == "__main__":
    sys.exit(main())
