"""Client for the LinQ TPU inference API (RabbitMQ + tpu_pycloud_format).

Works both inside the LinQ Jupyter (broker 10.0.114.30) and on our machine through the
SSH tunnel (broker 127.0.0.1:5672, see tools/linq/tunnel). The .tpu program itself must
already sit in /auto/cache/<jupyter login>/ on the LinQ side (upload via jupyter_remote.py).

Wire contract (from the vendor example, verified on the service):
  publish  exchange='tpu.direct', routing_key='input', body=serialize(PyTask({name: ndarray}))
  headers  uri='file:///auto/cache/<login>/<prog>.tpu?raw=False'
           response_routing_keys='["<our reply queue>"]'
           tpu_pycloud_message_id='<our id>'   (echoed back)
  reply    body -> deserialize() -> (outputs {name: ndarray}, metadata, worker info)
           worker info: worker_pid, inference_time, status_code, error_message

CLI:
  python tools/linq/linq_tpu.py ping
  python tools/linq/linq_tpu.py run PROGRAM.tpu --input NAME:1x3x224x224 [--n 10]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass

import numpy as np
import pika
from tpu_pycloud_format import (MESSAGE_ID_ATTR_NAME, RESPONSE_ROUTING_KEYS_ATTR_NAME,
                                TARGET_URI_ATTR_NAME, PyTask, deserialize, serialize)

EXCHANGE = "tpu.direct"
INPUT_QUEUE = "input"
CACHE_ROOT = "/auto/cache"


def default_host() -> str:
    if os.environ.get("LINQ_AMQP_HOST"):
        return os.environ["LINQ_AMQP_HOST"]
    # inside the LinQ Jupyter the broker is reachable directly; elsewhere use the tunnel
    return "10.0.114.30" if os.environ.get("JUPYTERHUB_USER") else "127.0.0.1"


def default_login() -> str:
    if not (os.environ.get("JUPYTERHUB_USER") or os.environ.get("LINQ_JUPYTER_USER")):
        try:  # outside Jupyter: take the login from the repo .env
            from pathlib import Path
            from dotenv import load_dotenv
            load_dotenv(Path(__file__).resolve().parents[2] / ".env")
        except ImportError:
            pass
    login = os.environ.get("JUPYTERHUB_USER") or os.environ.get("LINQ_JUPYTER_USER", "").lower()
    if not login:
        raise RuntimeError("Jupyter login unknown: set LINQ_JUPYTER_USER in .env")
    return login


def program_uri(program: str, login: str | None = None) -> str:
    """'net.tpu' -> file:///auto/cache/<login>/net.tpu?raw=False; absolute paths kept."""
    if program.startswith("file://"):
        return program
    path = program if program.startswith("/") else f"{CACHE_ROOT}/{login or default_login()}/{program}"
    return f"file://{path}?raw=False"


@dataclass
class TpuResult:
    outputs: dict[str, np.ndarray]
    worker: dict
    rtt_s: float  # publish -> reply received, as seen by the client

    @property
    def ok(self) -> bool:
        return bool(self.outputs) and int(self.worker.get("status_code", 0)) == 0


class TpuClient:
    def __init__(self, host: str | None = None, port: int = 5672,
                 user: str | None = None, password: str | None = None):
        params = pika.ConnectionParameters(
            host or default_host(), int(os.environ.get("LINQ_AMQP_PORT", port)),
            credentials=pika.PlainCredentials(user or os.environ.get("LINQ_AMQP_USER", "guest"),
                                              password or os.environ.get("LINQ_AMQP_PASSWORD", "guest")),
            heartbeat=60, blocked_connection_timeout=30, connection_attempts=2, retry_delay=1,
            socket_timeout=10)
        self.conn = pika.BlockingConnection(params)
        self.ch = self.conn.channel()
        self.reply_queue = f"mosprom_{uuid.uuid4().hex[:12]}"
        self.ch.queue_declare(queue=self.reply_queue, exclusive=True, auto_delete=True)
        self.ch.queue_bind(exchange=EXCHANGE, queue=self.reply_queue, routing_key=self.reply_queue)
        self._pending: dict[str, float] = {}
        self._done: dict[str, TpuResult] = {}
        self.unmatched = 0  # replies without a known message id
        self.ch.basic_consume(self.reply_queue, self._on_reply, auto_ack=True)

    # -- low level -------------------------------------------------------
    def _on_reply(self, ch, method, props, body) -> None:
        mid = (props.headers or {}).get(MESSAGE_ID_ATTR_NAME)
        t0 = self._pending.pop(mid, None)
        if t0 is None:
            self.unmatched += 1
            return
        data, _meta, worker = deserialize(body)
        self._done[mid] = TpuResult(data if isinstance(data, dict) else {}, worker, time.monotonic() - t0)

    def submit(self, program: str, tensors: dict[str, np.ndarray], login: str | None = None) -> str:
        mid = uuid.uuid4().hex
        self._pending[mid] = time.monotonic()
        self.ch.basic_publish(
            exchange=EXCHANGE, routing_key=INPUT_QUEUE,
            body=serialize(PyTask({k: np.ascontiguousarray(v) for k, v in tensors.items()})),
            properties=pika.BasicProperties(headers={
                TARGET_URI_ATTR_NAME: program_uri(program, login),
                RESPONSE_ROUTING_KEYS_ATTR_NAME: json.dumps([self.reply_queue]),
                MESSAGE_ID_ATTR_NAME: mid,
            }))
        return mid

    def collect(self, ids: list[str], timeout: float = 60) -> list[TpuResult]:
        deadline = time.monotonic() + timeout
        while any(i not in self._done for i in ids):
            left = deadline - time.monotonic()
            if left <= 0:
                missing = [i for i in ids if i not in self._done]
                raise TimeoutError(f"no TPU reply for {len(missing)} task(s) in {timeout} s, "
                                   f"unmatched replies {self.unmatched}")
            self.conn.process_data_events(time_limit=min(left, 1.0))
        return [self._done.pop(i) for i in ids]

    # -- convenience -----------------------------------------------------
    def infer(self, program: str, tensors: dict[str, np.ndarray], timeout: float = 60,
              login: str | None = None) -> TpuResult:
        r = self.collect([self.submit(program, tensors, login)], timeout)[0]
        if not r.ok:
            raise RuntimeError(f"TPU worker error status={r.worker.get('status_code')}: "
                               f"{r.worker.get('error_message')}")
        return r

    def input_queue_info(self) -> dict:
        q = self.ch.queue_declare(queue=INPUT_QUEUE, passive=True)
        return {"messages": q.method.message_count, "consumers": q.method.consumer_count}

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ping")
    p = sub.add_parser("run")
    p.add_argument("program")
    p.add_argument("--input", required=True, help="NAME:1x3x224x224 (random float32)")
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--login")
    a = ap.parse_args()

    with TpuClient(a.host) as c:
        if a.cmd == "ping":
            print(json.dumps({"host": c.conn._impl.params.host, "input_queue": c.input_queue_info()}))
            return 0
        name, shape = a.input.split(":")
        x = np.random.rand(*[int(s) for s in shape.split("x")]).astype(np.float32)
        for i in range(a.n):
            r = c.infer(a.program, {name: x}, login=a.login)
            outs = {k: (list(v.shape), str(v.dtype)) for k, v in r.outputs.items()}
            print(f"#{i} rtt={r.rtt_s * 1000:.1f} ms worker_inference={r.worker['inference_time'] * 1000:.1f} ms "
                  f"pid={r.worker['worker_pid']} outputs={outs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
