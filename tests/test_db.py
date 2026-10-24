import sqlite3

import pytest

from safewatch.db import migrate

TABLES = {
    "sectors", "cameras", "videos", "jobs", "artifacts", "analyses", "episodes", "evidence",
    "broadcasts", "zones", "calibrations", "camera_rules", "events", "event_actions", "deliveries",
}  # fmt: skip
AT = "2026-10-24T09:00:00.000Z"


def _world(conn: sqlite3.Connection) -> None:
    conn.execute("INSERT INTO sectors (id, name, created_at) VALUES (1, 'S', ?)", (AT,))
    conn.execute(
        "INSERT INTO cameras (id, sector_id, name, created_at) VALUES (1, 1, 'C', ?)", (AT,)
    )


def test_migrate_creates_tables(conn: sqlite3.Connection) -> None:
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert tables == TABLES
    assert conn.execute("PRAGMA user_version").fetchone()[0] == 1


def test_second_migrate_changes_nothing(conn: sqlite3.Connection) -> None:
    before = conn.execute("SELECT sql FROM sqlite_master ORDER BY name").fetchall()
    assert migrate(conn) == 0
    assert conn.execute("SELECT sql FROM sqlite_master ORDER BY name").fetchall() == before


def test_event_actions_are_append_only(conn: sqlite3.Connection) -> None:
    _world(conn)
    conn.execute(
        "INSERT INTO events (id, pub_key, camera_id, sector_id, scenario, title, reason_text,"
        " level, status, started_at, published_at) VALUES"
        " (1, 'demo:1', 1, 1, 'fall', 'T', 'R', 'red', 'new', ?, ?)",
        (AT, AT),
    )
    conn.execute(
        "INSERT INTO event_actions (event_id, at, actor_role, actor_name, action, to_status)"
        " VALUES (1, ?, 'system', 'система', 'published', 'new')",
        (AT,),
    )
    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        conn.execute("UPDATE event_actions SET comment = 'x'")
    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        conn.execute("DELETE FROM event_actions")
    assert conn.execute("SELECT count(*) FROM event_actions").fetchone()[0] == 1


def test_one_playing_broadcast_per_camera(conn: sqlite3.Connection) -> None:
    _world(conn)
    conn.execute(
        "INSERT INTO videos (id, camera_id, filename, sha256, path, size_bytes, width, height,"
        " fps, frame_count, duration_ms, codec, browser_playable, status, created_at) VALUES"
        " (1, 1, 'a.mp4', 'h', 'uploads/h.mp4', 1, 2, 2, 25, 1, 40, 'avc1', 1, 'ready', ?)",
        (AT,),
    )
    conn.execute(
        "INSERT INTO artifacts (id, cache_key, video_sha256, model_id, model_version, task,"
        " input_size, step, backend, fake, path, frames, metrics_json, created_at) VALUES"
        " (1, 'k', 'h', 'm', 'v', 'detect', 640, 2, 'linq', 1, 'p', 1, '{}', ?)",
        (AT,),
    )
    conn.execute(
        "INSERT INTO analyses (id, video_id, version, det_artifact_id, config_json, hud_path,"
        " gaps_json, duration_ms, created_at) VALUES (1, 1, 1, 1, '{}', 'h', '[]', 40, ?)",
        (AT,),
    )
    insert = (
        "INSERT INTO broadcasts (camera_id, video_id, analysis_id, started_at, loop, status)"
        " VALUES (1, 1, 1, ?, 1, ?)"
    )
    conn.execute(insert, (AT, "stopped"))
    conn.execute(insert, (AT, "playing"))
    conn.execute(insert, (AT, "ended"))
    with pytest.raises(sqlite3.IntegrityError, match="UNIQUE"):
        conn.execute(insert, (AT, "playing"))


def test_connect_registers_casefold(conn: sqlite3.Connection) -> None:
    row = conn.execute("SELECT casefold('ПРЕСС Пресс'), casefold(NULL)").fetchone()
    assert tuple(row) == ("пресс пресс", None)
