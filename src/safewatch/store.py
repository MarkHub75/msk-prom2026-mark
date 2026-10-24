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


# --- sectors, cameras ---------------------------------------------------------------------
def sectors() -> list[sqlite3.Row]:
    return all("SELECT * FROM sectors ORDER BY sort_order, name")


def sector(sector_id: int) -> sqlite3.Row | None:
    return one("SELECT * FROM sectors WHERE id = ?", sector_id)


def sector_name_taken(name: str, except_id: int | None = None) -> bool:
    row = one("SELECT 1 FROM sectors WHERE name = ? AND id IS NOT ?", name, except_id)
    return row is not None


def sector_update(sector_id: int, name: str, sort_order: int) -> None:
    run("UPDATE sectors SET name = ?, sort_order = ? WHERE id = ?", name, sort_order, sector_id)


def sector_has_cameras(sector_id: int) -> bool:
    sql = "SELECT 1 FROM cameras WHERE sector_id = ? AND deleted_at IS NULL LIMIT 1"
    return one(sql, sector_id) is not None


def sector_delete(sector_id: int) -> None:
    run("DELETE FROM sectors WHERE id = ?", sector_id)


# Counters of the Camera model in one query: no per-camera round trips.
_CAMERAS = """
SELECT c.*,
    EXISTS (SELECT 1 FROM calibrations k WHERE k.camera_id = c.id) AS has_calibration,
    (SELECT count(*) FROM zones z WHERE z.camera_id = c.id AND z.deleted_at IS NULL)
        AS zones_count,
    (SELECT count(*) FROM videos v WHERE v.camera_id = c.id) AS videos_count
FROM cameras c
WHERE c.deleted_at IS NULL
"""


def cameras(sector_id: int | None = None) -> list[sqlite3.Row]:
    if sector_id is None:
        return all(_CAMERAS + " ORDER BY c.sector_id, c.name, c.id")
    return all(_CAMERAS + " AND c.sector_id = ? ORDER BY c.name, c.id", sector_id)


def camera(camera_id: int) -> sqlite3.Row | None:
    return one(_CAMERAS + " AND c.id = ?", camera_id)


def camera_update(camera_id: int, values: dict[str, Any]) -> None:
    assignments = ", ".join(f"{column} = ?" for column in values)
    run(f"UPDATE cameras SET {assignments} WHERE id = ?", *values.values(), camera_id)


def camera_delete(camera_id: int, at: str) -> None:
    run("UPDATE cameras SET deleted_at = ? WHERE id = ?", at, camera_id)
    sql = "UPDATE broadcasts SET status = 'stopped', stopped_at = ?"
    run(sql + " WHERE camera_id = ? AND status = 'playing'", at, camera_id)


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


# --- videos, jobs, artifacts --------------------------------------------------------------
def video(video_id: int) -> sqlite3.Row | None:
    return one("SELECT * FROM videos WHERE id = ?", video_id)


def video_by_sha(camera_id: int, sha256: str) -> sqlite3.Row | None:
    return one("SELECT * FROM videos WHERE camera_id = ? AND sha256 = ?", camera_id, sha256)


def video_filename(sha256: str) -> str | None:
    row = one("SELECT filename FROM videos WHERE sha256 = ? ORDER BY id LIMIT 1", sha256)
    return None if row is None else str(row["filename"])


def videos(camera_id: int) -> list[sqlite3.Row]:
    return all(
        "SELECT * FROM videos WHERE camera_id = ? ORDER BY created_at DESC, id DESC", camera_id
    )


def video_update(video_id: int, values: dict[str, Any]) -> None:
    assignments = ", ".join(f"{column} = ?" for column in values)
    run(f"UPDATE videos SET {assignments} WHERE id = ?", *values.values(), video_id)


# Metrics of the job's artifacts come in the same row: no per-job round trips.
_JOBS = """
SELECT j.*, v.camera_id,
    d.metrics_json AS det_metrics, d.created_at AS det_created,
    p.metrics_json AS pose_metrics, p.created_at AS pose_created
FROM jobs j
JOIN videos v ON v.id = j.video_id
LEFT JOIN artifacts d ON d.id = j.det_artifact_id
LEFT JOIN artifacts p ON p.id = j.pose_artifact_id
"""


def job(job_id: int) -> sqlite3.Row | None:
    return one(_JOBS + " WHERE j.id = ?", job_id)


def jobs(status: str | None, limit: int) -> list[sqlite3.Row]:
    sql = _JOBS + " WHERE ? IS NULL OR j.status = ? ORDER BY j.created_at DESC, j.id DESC LIMIT ?"
    return all(sql, status, status, limit)


def camera_jobs(camera_id: int) -> list[sqlite3.Row]:
    return all(_JOBS + " WHERE v.camera_id = ? ORDER BY j.created_at DESC, j.id DESC", camera_id)


def video_last_job(video_id: int) -> sqlite3.Row | None:
    return one("SELECT * FROM jobs WHERE video_id = ? ORDER BY id DESC LIMIT 1", video_id)


def next_job(now: str) -> sqlite3.Row | None:
    sql = """SELECT * FROM jobs WHERE status = 'queued'
        OR (status = 'retry_wait' AND next_attempt_at <= ?) ORDER BY created_at, id LIMIT 1"""
    return one(sql, now)


def job_update(job_id: int, values: dict[str, Any]) -> None:
    assignments = ", ".join(f"{column} = ?" for column in values)
    run(f"UPDATE jobs SET {assignments} WHERE id = ?", *values.values(), job_id)


def job_progress(job_id: int, progress: float) -> None:
    run("UPDATE jobs SET progress = max(progress, ?) WHERE id = ?", progress, job_id)


def artifact(cache_key: str) -> sqlite3.Row | None:
    return one("SELECT * FROM artifacts WHERE cache_key = ?", cache_key)


def artifact_update(artifact_id: int, values: dict[str, Any]) -> None:
    assignments = ", ".join(f"{column} = ?" for column in values)
    run(f"UPDATE artifacts SET {assignments} WHERE id = ?", *values.values(), artifact_id)


def queue_jobs() -> list[sqlite3.Row]:
    sql = " WHERE j.status IN ('queued', 'running', 'retry_wait') ORDER BY j.created_at, j.id"
    return all(_JOBS + sql)


def finished_jobs(limit: int) -> list[sqlite3.Row]:
    sql = " WHERE j.status IN ('done', 'failed') ORDER BY j.finished_at DESC, j.id DESC LIMIT ?"
    return all(_JOBS + sql, limit)


def jobs_recover() -> int:
    return run("UPDATE jobs SET status = 'queued' WHERE status = 'running'")
