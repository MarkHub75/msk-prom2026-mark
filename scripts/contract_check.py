"""Check that every contract element of a closed slice is in the code (tech.md 11).

Reads the "Трассировка" table of tech.md and the closed slices in `## log` of progress.md.
For each table row whose slice is closed, the file must exist and contain the searched
string; a test given as `path::name` must exist too. Any miss makes the gate red.

Knows nothing about the project's language: it only looks for literal strings in files,
so the same script runs for any stack (`python scripts/contract_check.py`).
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

COLUMNS = ("Элемент", "Слайс", "Потребитель", "Файл", "Искомая строка", "Тест")
TRACE_HEADING = re.compile(r"^#{2,6}\s.*Трассировка")
CLOSED = re.compile(r"^###\s+S(\d+)\b(.*)$")
ROLLBACK = ("откат", "rollback", "revert")
SLICE = re.compile(r"^S?(\d+)$")
TEST_REF = re.compile(r"^(?P<path>[^\s:`]+)::(?P<name>\w+)")
CELL_SPLIT = re.compile(r"(?<!\\)\|")
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


class TraceError(Exception):
    """tech.md or progress.md is not in the format the gate reads."""


@dataclass(frozen=True)
class Row:
    line: int
    element: str
    slice: int
    file: str
    needle: str
    test: str


def unquote(cell: str) -> str:
    cell = cell.strip()
    if len(cell) >= 2 and cell.startswith("`") and cell.endswith("`"):
        cell = cell[1:-1]
    return cell.replace("\\|", "|")


def cells(line: str) -> list[str]:
    parts = CELL_SPLIT.split(line.strip())
    # A row "| a | b |" splits into ["", " a ", " b ", ""].
    return [part.strip() for part in parts[1:-1]]


def trace_rows(tech: str) -> list[Row]:
    lines = COMMENT.sub("", tech).splitlines()
    start = next((i for i, line in enumerate(lines) if TRACE_HEADING.match(line)), None)
    if start is None:
        raise TraceError("tech.md: no heading with «Трассировка»")
    head = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("|")), None)
    if head is None:
        raise TraceError("tech.md: no table under «Трассировка»")
    names = cells(lines[head])
    missing = [name for name in COLUMNS if name not in names]
    if missing:
        raise TraceError(f"tech.md: trace table lacks columns {', '.join(missing)}")
    col = {name: names.index(name) for name in COLUMNS}
    rows = []
    for i in range(head + 2, len(lines)):
        if not lines[i].startswith("|"):
            break
        row = cells(lines[i])
        if len(row) != len(names):
            raise TraceError(f"tech.md:{i + 1}: {len(row)} cells, header has {len(names)}")
        element = unquote(row[col["Элемент"]])
        number = SLICE.match(unquote(row[col["Слайс"]]))
        if number is None:
            raise TraceError(f"tech.md:{i + 1}: «{element}» has no slice")
        rows.append(
            Row(
                line=i + 1,
                element=element,
                slice=int(number.group(1)),
                file=unquote(row[col["Файл"]]),
                needle=unquote(row[col["Искомая строка"]]),
                test=unquote(row[col["Тест"]]),
            )
        )
    if not rows:
        raise TraceError("tech.md: trace table is empty")
    return rows


def closed_slices(progress: str) -> set[int]:
    closed: set[int] = set()
    in_log = False
    for line in COMMENT.sub("", progress).splitlines():
        if line.startswith("## "):
            in_log = line.strip() == "## log"
            continue
        match = CLOSED.match(line) if in_log else None
        if match is None:
            continue
        number = int(match.group(1))
        if any(word in match.group(2).lower() for word in ROLLBACK):
            closed.discard(number)
        else:
            closed.add(number)
    return closed


FRONT_OWNER = "frontend/FRONT_OWNER"


def problems(root: Path) -> tuple[list[str], int, set[int]]:
    rows = trace_rows((root / "tech.md").read_text(encoding="utf-8"))
    closed = closed_slices((root / "progress.md").read_text(encoding="utf-8"))
    # Egor's front end replaces the minimal one of the trace table: its own layout and tests
    # (npm run gate) own frontend/, so the table's frontend files are not looked for there.
    own_front = (root / FRONT_OWNER).is_file()
    found: list[str] = []
    checked = 0
    for row in rows:
        if row.slice not in closed:
            continue
        if own_front and row.file.startswith("frontend/"):
            continue
        checked += 1
        where = f"tech.md:{row.line} S{row.slice} «{row.element}»"
        path = root / row.file
        if not path.is_file():
            found.append(f"{where}: no file {row.file}")
        elif row.needle not in path.read_text(encoding="utf-8"):
            found.append(f"{where}: «{row.needle}» not in {row.file}")
        test = TEST_REF.match(row.test)
        if test:
            test_path = root / test.group("path")
            if not test_path.is_file():
                found.append(f"{where}: no test file {test.group('path')}")
            elif test.group("name") not in test_path.read_text(encoding="utf-8"):
                found.append(f"{where}: no test {test.group('name')} in {test.group('path')}")
    return found, checked, closed


def main(argv: list[str] | None = None) -> int:
    # Windows consoles and pipes default to cp1252; the messages carry Cyrillic.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        found, checked, closed = problems(args.root)
    except (TraceError, FileNotFoundError) as error:
        print(f"contract: {error}")
        return 1
    for line in found:
        print(f"contract: {line}")
    slices = ", ".join(f"S{n}" for n in sorted(closed)) or "none"
    status = "FAIL" if found else "ok"
    print(f"contract: {status}, {checked} elements checked, closed slices: {slices}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
