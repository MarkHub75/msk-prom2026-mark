"""Credential-free host/network inventory. Does not authenticate or run models."""
from __future__ import annotations
import argparse
import importlib.util
import json
import os
import shutil
import socket
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def check(host: str = "hackathon.lin-q.ru", timeout: float = 3.0) -> dict:
    checks = []
    def add(name, status, **safe_fields):
        checks.append({"name": name, "status": status, **safe_fields})
    add("tun", "pass" if os.path.exists("/dev/net/tun") else "unavailable")
    add("openvpn", "pass" if shutil.which("openvpn") else "unavailable")
    for package in ("tpu_framework", "pytpu"):
        try:
            present = importlib.util.find_spec(package) is not None
        except (ImportError, ValueError):
            present = False
        add(package, "pass" if present else "unavailable")
    try:
        addresses = socket.getaddrinfo(host, 80, type=socket.SOCK_STREAM)
        add("dns", "pass" if addresses else "unavailable")
    except OSError as error:
        add("dns", "unavailable", error_type=type(error).__name__)
    try:
        with socket.create_connection((host, 80), timeout=timeout):
            add("tcp80", "pass")
    except OSError as error:
        add("tcp80", "unavailable", error_type=type(error).__name__)
    # Ignore ambient HTTP proxies: private VPN connectivity must be end-to-end.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect())
    request = urllib.request.Request(f"http://{host}/", method="HEAD")
    try:
        with opener.open(request, timeout=timeout) as response:
            add("jupyter_http", "pass", http_status=response.status)
    except urllib.error.HTTPError as error:
        add("jupyter_http", "pass" if error.code in (301, 302, 303, 307, 308, 401, 403, 405) else "fail", http_status=error.code)
    except Exception as error:
        add("jupyter_http", "unavailable", error_type=type(error).__name__)
    # Login page/HTTP reachability is never reported as successful auth or TPU.
    add("jupyter_authenticated", "not_run")
    add("vendor_resnet50_tpu", "not_run")
    add("own_model_tpu", "not_run")
    return {"checked_at": datetime.now(timezone.utc).isoformat(), "python": sys.version.split()[0],
            "host": host, "checks": checks, "hardware_inference_confirmed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="hackathon.lin-q.ru")
    parser.add_argument("--timeout", type=float, default=3.0)
    args = parser.parse_args()
    if not args.host or any(c in args.host for c in "/:@?#") or args.timeout <= 0:
        parser.error("host must be a bare hostname and timeout must be positive")
    print(json.dumps(check(args.host, args.timeout), indent=2))


if __name__ == "__main__":
    main()
