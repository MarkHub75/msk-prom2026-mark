"""Connection and migrations (tech.md 5.1). SQL of the app lives here and in store.py."""

import sqlite3
from pathlib import Path

MIGRATIONS = Path(__file__).parent / "migrations"


def _casefold(value: str | None) -> str | None:
    # SQLite lower() folds ASCII only; the journal searches Cyrillic text.
    return value.casefold() if value is not None else None


def connect(path: Path | str) -> sqlite3.Connection:
    """Open the database; `":memory:"` gives tests a fresh one. Autocommit: store.tx() opens
    transactions explicitly."""
    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    if str(path) != ":memory:":
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = FULL")
        conn.execute("PRAGMA busy_timeout = 1000")
    conn.create_function("casefold", 1, _casefold, deterministic=True)
    return conn


def migrate(conn: sqlite3.Connection) -> int:
    """Apply numbered `NNNN_*.sql` files newer than `user_version`; return how many ran."""
    version: int = conn.execute("PRAGMA user_version").fetchone()[0]
    applied = 0
    for path in sorted(MIGRATIONS.glob("*.sql")):
        number = int(path.name[:4])
        if number <= version:
            continue
        sql = path.read_text(encoding="utf-8")
        conn.executescript(f"BEGIN;\n{sql}\nPRAGMA user_version = {number};\nCOMMIT;")
        applied += 1
    return applied
