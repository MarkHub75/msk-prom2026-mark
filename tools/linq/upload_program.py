"""Upload a compiled .tpu to the LinQ service: Jupyter Contents API -> /auto/cache/<login>/.

    python tools/linq/upload_program.py models/linq/<tag>/<prog>.tpu [--name mosprom_x.tpu] [--force]

The program name in /auto/cache always starts with 'mosprom_' so we never clash with
programs other people put there; an existing file is only replaced with --force.
Prints the name to pass as `program` to linq_tpu.TpuClient.infer().
"""
from __future__ import annotations

import argparse
import hashlib
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jupyter_remote import JupyterRemote  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("program")
    ap.add_argument("--name")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    src = Path(a.program)
    name = a.name or src.name
    if not name.startswith("mosprom_"):
        name = "mosprom_" + name
    sha = hashlib.sha256(src.read_bytes()).hexdigest()

    jr = JupyterRemote.from_env()
    try:
        jr.upload(src, f"mosprom_work/programs/{name}")
        rc, login, _ = jr.exec("whoami", timeout=30)
        dst = f"/auto/cache/{login.strip()}/{name}"
        cmd = (f"set -e; src=~/work/mosprom_work/programs/{shlex.quote(name)}; dst={shlex.quote(dst)}; "
               f"if [ -e \"$dst\" ] && [ {int(a.force)} = 0 ]; then "
               f"  [ \"$(sha256sum < \"$dst\" | cut -c1-64)\" = {sha} ] && echo SAME || {{ echo EXISTS; exit 3; }}; "
               f"else cp \"$src\" \"$dst\" && echo COPIED; fi; sha256sum < \"$dst\" | cut -c1-64")
        rc, out, err = jr.exec(cmd, timeout=120)
        if rc != 0:
            raise SystemExit(f"copy to {dst} failed ({out.strip()} {err.strip()}); use --force to replace")
        status, remote_sha = out.split()[:2]
        if remote_sha != sha:
            raise SystemExit("sha256 mismatch after upload")
        print(f"{status}: {dst} sha256={sha[:16]}…  -> program name: {name}")
    finally:
        jr.shutdown_kernel()
    return 0


if __name__ == "__main__":
    sys.exit(main())
