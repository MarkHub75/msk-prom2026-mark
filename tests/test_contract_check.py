import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "contract_check.py"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("contract_check", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["contract_check"] = module
    spec.loader.exec_module(module)
    return module


cc = _load()

TECH = """\
# tech.md

### 6.7 Трассировка

| Элемент | Слайс | Потребитель | Файл | Искомая строка | Тест |
| --- | --- | --- | --- | --- | --- |
| `note_create` | 1 | API | `src/app/svc.py` | `def note_create(` | `tests/test_n.py::test_create` |
| `a \\| b` | S2 | CLI | `src/app/cli.py` | `mode = "a\\|b"` | вручную: запустить |
| `later` | 3 | экран | `src/app/later.py` | `def later(` | `tests/test_later.py::test_later` |

## 7. Next
"""

LOG_S1 = "### S1: notes (2026-10-12, PR #2, tech v1)\n- отклонений нет\n"


def make(root: Path, log: str, files: dict[str, str], tech: str = TECH) -> Path:
    (root / "tech.md").write_text(tech, encoding="utf-8")
    progress = f"# progress.md\n\n## open\n\n## log\n\n{log}\n## night\n"
    (root / "progress.md").write_text(progress, encoding="utf-8")
    for name, text in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(text, encoding="utf-8")
    return root


GOOD = {
    "src/app/svc.py": "def note_create(title: str) -> int:\n    return 1\n",
    "tests/test_n.py": "def test_create() -> None:\n    pass\n",
}


def test_closed_slice_with_element_in_code_is_green(tmp_path: Path) -> None:
    assert cc.main(["--root", str(make(tmp_path, LOG_S1, GOOD))]) == 0


def test_closed_slice_element_not_found_is_red(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    files = {**GOOD, "src/app/svc.py": "def note_add(title: str) -> int: ...\n"}
    assert cc.main(["--root", str(make(tmp_path, LOG_S1, files))]) == 1
    assert "def note_create(" in capsys.readouterr().out


def test_closed_slice_without_file_is_red(tmp_path: Path) -> None:
    files = {"tests/test_n.py": GOOD["tests/test_n.py"]}
    found, _, _ = cc.problems(make(tmp_path, LOG_S1, files))
    assert found == ["tech.md:7 S1 «note_create»: no file src/app/svc.py"]


def test_closed_slice_without_its_test_is_red(tmp_path: Path) -> None:
    files = {**GOOD, "tests/test_n.py": "def test_other() -> None: ...\n"}
    found, _, _ = cc.problems(make(tmp_path, LOG_S1, files))
    assert found == ["tech.md:7 S1 «note_create»: no test test_create in tests/test_n.py"]


def test_open_slices_are_skipped(tmp_path: Path) -> None:
    found, checked, closed = cc.problems(make(tmp_path, "", {}))
    assert (found, checked, closed) == ([], 0, set())


def test_rollback_reopens_the_slice(tmp_path: Path) -> None:
    log = LOG_S1 + "\n### S1 откат: broke search (see S1 above)\n"
    assert cc.closed_slices((make(tmp_path, log, {}) / "progress.md").read_text("utf-8")) == set()


def test_entries_in_comments_and_other_sections_do_not_count() -> None:
    progress = (
        "## open\n### S5: not a log\n## log\n<!--\n### S1: example\n-->\n## night\n### S2: x\n"
    )
    assert cc.closed_slices(progress) == set()


def test_escaped_pipe_and_s_prefix_are_read(tmp_path: Path) -> None:
    log = "### S2: cli (2026-10-12, PR #3, tech v1)\n"
    files = {"src/app/cli.py": 'mode = "a|b"\n'}
    found, checked, _ = cc.problems(make(tmp_path, log, files))
    assert (found, checked) == ([], 1)


def test_frontend_rows_are_skipped_when_the_front_end_has_its_own_owner(tmp_path: Path) -> None:
    tech = TECH.replace("`src/app/svc.py`", "`frontend/src/svc.tsx`")
    root = make(tmp_path, LOG_S1, {"tests/test_n.py": GOOD["tests/test_n.py"]}, tech)
    assert cc.problems(root)[0] == ["tech.md:7 S1 «note_create»: no file frontend/src/svc.tsx"]
    (root / "frontend").mkdir()
    (root / "frontend" / "FRONT_OWNER").write_text("Egor\n", encoding="utf-8")
    assert cc.problems(root)[:2] == ([], 0)


def test_row_without_slice_is_a_generation_error(tmp_path: Path) -> None:
    tech = TECH.replace("| `later` | 3 |", "| `later` | — |")
    with pytest.raises(cc.TraceError, match="has no slice"):
        cc.problems(make(tmp_path, "", {}, tech))


def test_missing_trace_table_is_red(tmp_path: Path) -> None:
    assert cc.main(["--root", str(make(tmp_path, "", {}, "# tech.md\n"))]) == 1
