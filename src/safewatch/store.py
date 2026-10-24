"""All SQL of the app besides migrations (tech.md 4). Only the event loop thread calls it."""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from safewatch import config
from safewatch.db import connect, migrate

# Opened lazily once per process; the `conn` fixture in tests puts a fresh in-memory one here.
_conn: sqlite3.Connection | None = None
_depth = 0


def conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        settings = config.get_settings()
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        _conn = connect(settings.data_dir / "safewatch.db")
        migrate(_conn)
    return _conn


@contextmanager
def tx() -> Iterator[sqlite3.Connection]:
    """One transaction; nested calls join the outer one."""
    global _depth
    db = conn()
    if _depth:
        _depth += 1
        try:
            yield db
        finally:
            _depth -= 1
        return
    db.execute("BEGIN IMMEDIATE")
    _depth = 1
    try:
        yield db
    except BaseException:
        db.execute("ROLLBACK")
        raise
    else:
        db.execute("COMMIT")
    finally:
        _depth = 0


def one(sql: str, *args: Any) -> sqlite3.Row | None:
    row: sqlite3.Row | None = conn().execute(sql, args).fetchone()
    return row


def all(sql: str, *args: Any) -> list[sqlite3.Row]:  # noqa: A001 - name from tech.md 7
    return conn().execute(sql, args).fetchall()


def run(sql: str, *args: Any) -> int:
    """Execute a write; return the last row id for INSERT, else the number of changed rows."""
    cur = conn().execute(sql, args)
    if sql.lstrip().upper().startswith("INSERT"):
        return int(cur.lastrowid or 0)
    return cur.rowcount


def insert(table: str, values: dict[str, Any]) -> int:
    columns = ", ".join(values)
    marks = ", ".join("?" for _ in values)
    return run(f"INSERT INTO {table} ({columns}) VALUES ({marks})", *values.values())


# --- seed ---------------------------------------------------------------------------------
def demo_world_exists() -> bool:
    return one("SELECT 1 FROM sectors WHERE is_demo = 1 LIMIT 1") is not None


def demo_counts() -> dict[str, int]:
    tables = ("sectors", "cameras", "zones", "events", "videos")
    counts: dict[str, int] = {}
    for table in tables:
        if table == "videos":
            sql = "SELECT count(*) FROM videos JOIN cameras ON cameras.id = videos.camera_id"
            row = one(sql + " WHERE cameras.is_demo = 1")
        elif table == "zones":
            sql = "SELECT count(*) FROM zones JOIN cameras ON cameras.id = zones.camera_id"
            row = one(sql + " WHERE cameras.is_demo = 1")
        else:
            row = one(f"SELECT count(*) FROM {table} WHERE is_demo = 1")
        counts[table] = int(row[0]) if row else 0
    return counts


def demo_cameras() -> list[sqlite3.Row]:
    return all("SELECT id FROM cameras WHERE is_demo = 1 AND deleted_at IS NULL ORDER BY id")
