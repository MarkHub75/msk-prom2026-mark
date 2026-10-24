"""`safewatch` command (tech.md 6.3)."""

import argparse
import asyncio
import json
import socket
import sys
import time
from pathlib import Path

import psutil
from pydantic import TypeAdapter

from safewatch import config, doctor, services
from safewatch.config import ROOT
from safewatch.errors import NotFound
from safewatch.types import WsMessage

CONTRACT_DIR = ROOT / "contract"
STOP_WAIT_S = 10
STOP_POLL_S = 0.1


def _pid_file() -> Path:
    return config.get_settings().data_dir / "server.pid"


def _port_free(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((host, port))
        except OSError:
            return False
    return True


def serve(host: str | None, port: int | None, seed: bool) -> int:
    import uvicorn

    from safewatch.api import create_app

    settings = config.get_settings()
    host = host or settings.server.host
    port = port or settings.server.port
    if not _port_free(host, port):
        print(f"port {port} on {host} is busy", file=sys.stderr)
        return 2
    app = create_app(settings)
    if seed:
        print(services.seed_demo().model_dump_json())
    pid_file = _pid_file()
    pid_file.parent.mkdir(parents=True, exist_ok=True)
    me = psutil.Process()
    record = {"pid": me.pid, "create_time": me.create_time()}
    pid_file.write_text(json.dumps(record), encoding="utf-8", newline="\n")
    try:
        server = uvicorn.Server(uvicorn.Config(app, host=host, port=port, log_level="info"))
        # asyncio.run uses the ProactorEventLoop on Windows (tech.md 3.2), no reload.
        asyncio.run(server.serve())
    finally:
        pid_file.unlink(missing_ok=True)
    return 0


def _exited(proc: psutil.Process) -> bool:
    try:
        # On POSIX an exited child of another process stays a zombie until its parent reaps
        # it; psutil.wait() from here would wait for that.
        return proc.status() == psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return True


def _wait_exit(proc: psutil.Process) -> None:
    deadline = time.perf_counter() + STOP_WAIT_S
    while not _exited(proc):
        if time.perf_counter() > deadline:
            raise psutil.TimeoutExpired(STOP_WAIT_S, proc.pid)
        time.sleep(STOP_POLL_S)


def stop() -> int:
    pid_file = _pid_file()
    if not pid_file.exists():
        print("not running")
        return 0
    record = json.loads(pid_file.read_text(encoding="utf-8"))
    try:
        proc = psutil.Process(record["pid"])
        ours = proc.create_time() == record["create_time"]
    except psutil.NoSuchProcess:
        ours = False
    if not ours:
        # The pid now belongs to another process (or none): leave it alone, drop the file.
        pid_file.unlink(missing_ok=True)
        print(f"pid {record['pid']} is not the server; removed {pid_file.name}")
        return 1
    proc.terminate()
    _wait_exit(proc)
    pid_file.unlink(missing_ok=True)
    print(f"stopped {record['pid']}")
    return 0


def seed(videos: Path | None) -> int:
    try:
        report = services.seed_demo(videos)
    except NotFound as exc:
        print(exc.message, file=sys.stderr)
        return 3
    print(report.model_dump_json())
    return 0


def contract_texts() -> dict[str, str]:
    from safewatch.api import create_app

    def dump(data: object) -> str:
        return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"

    openapi = create_app(config.get_settings()).openapi()
    return {
        "openapi.json": dump(openapi),
        "ws.schema.json": dump(TypeAdapter(WsMessage).json_schema()),
    }


def contract(check: bool) -> int:
    drift = []
    for name, text in contract_texts().items():
        path = CONTRACT_DIR / name
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                drift.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
    for name in drift:
        print(f"contract/{name} differs from the app: run `safewatch contract`")
    return 1 if drift else 0


def main(argv: list[str] | None = None) -> int:
    # Windows consoles and pipes default to cp1252; the output carries Cyrillic.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(prog="safewatch")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("serve", help="run the server")
    p.add_argument("--host")
    p.add_argument("--port", type=int)
    p.add_argument("--seed", action="store_true", help="create the demo world if it is missing")
    sub.add_parser("stop", help="stop the server of server.pid")
    p = sub.add_parser("seed", help="create the demo world")
    p.add_argument("--videos", type=Path)
    sub.add_parser("doctor", help="check keys, models, LinQ tools and the database")
    p = sub.add_parser("contract", help="write or check contract/*.json")
    p.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "serve":
        return serve(args.host, args.port, args.seed)
    if args.command == "stop":
        return stop()
    if args.command == "seed":
        return seed(args.videos)
    if args.command == "doctor":
        return doctor.run(config.get_settings())
    return contract(args.check)
