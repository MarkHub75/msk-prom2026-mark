"""Fail when an app path is stored with CRLF in git (tech.md 3.2, 11).

The research files keep their CRLF; only the paths of the app must be LF in the index.
"""

import argparse
import subprocess
import sys
from pathlib import Path

PATHS = ["src", "tests", "scripts", "config", "contract", "frontend", ".github", "pyproject.toml"]
PATHS += ["uv.lock", "tech.md", "CLAUDE.md", "progress.md", "docs/brief.md"]


def crlf_files(root: Path) -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "--eol", "--", *PATHS],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    ).stdout
    return [line.split("\t", 1)[1] for line in out.splitlines() if line.startswith("i/crlf")]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    found = crlf_files(args.root)
    for name in found:
        print(f"eol: CRLF in git: {name}")
    print(f"eol: {'FAIL' if found else 'ok'}, {len(found)} files with CRLF")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
