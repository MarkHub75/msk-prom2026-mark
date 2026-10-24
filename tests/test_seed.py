import json
import sqlite3
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import pytest

from safewatch import cli, seed, services
from safewatch.config import Settings
from safewatch.errors import NotFound
from safewatch.types import SeedReport


def _counts(conn: sqlite3.Connection) -> dict[str, int]:
    tables = ("sectors", "cameras", "zones", "events", "event_actions")
    return {t: conn.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in tables}


def test_seed_creates_demo_world_once(core: Settings, conn: sqlite3.Connection, fake_clock) -> None:
    report = services.seed_demo()
    assert report == SeedReport(
        skipped=False, sectors=4, cameras=8, zones=7, events=seed.EVENTS, videos=0
    )
    for table in ("sectors", "cameras", "events"):
        assert conn.execute(f"SELECT count(*) FROM {table} WHERE is_demo = 0").fetchone()[0] == 0
    events = conn.execute("SELECT * FROM events ORDER BY id").fetchall()
    assert all(e["pub_key"] == f"demo:{n}" for n, e in enumerate(events, start=1))
    levels = Counter(e["level"] for e in events)
    assert levels == {"yellow": 192, "red": 48}
    statuses = Counter((e["level"], e["status"]) for e in events)
    assert statuses[("yellow", "confirmed")] == 96
    assert statuses[("yellow", "false_alarm")] == 29
    assert statuses[("red", "resolved")] == 34 + 4
    assert sum(e["escalated_by_timeout"] for e in events) == 4
    yesterday_end = "2026-10-23T21:00:00.000Z"  # Moscow midnight of 24.10
    assert max(e["started_at"] for e in events) < yesterday_end
    for e in events:
        actions = conn.execute(
            "SELECT * FROM event_actions WHERE event_id = ? ORDER BY id", (e["id"],)
        ).fetchall()
        assert (actions[0]["action"], actions[0]["actor_role"]) == ("published", "system")
        assert actions[-1]["to_status"] == e["status"]
        if e["status"] == "resolved":
            assert actions[-1]["comment"] != ""
    before = _counts(conn)
    again = services.seed_demo()
    assert again == report.model_copy(update={"skipped": True})
    assert _counts(conn) == before


def test_yellow_events_drop_week_by_week(fake_clock) -> None:
    world = seed.build_demo(fake_clock.now(), "Europe/Moscow")
    last = datetime(2026, 10, 23, 21, 0, tzinfo=UTC)  # end of yesterday in Moscow
    weeks = Counter((last - e.started_at).days // 7 for e in world.events if e.level == "yellow")
    per_week = [weeks[w] for w in range(5, -1, -1)]  # oldest week first
    assert per_week == sorted(per_week, reverse=True)
    assert per_week[0] > per_week[-1]
    assert seed.build_demo(fake_clock.now(), "Europe/Moscow").events[0] == world.events[0]


def test_seed_cli_reports_counts(
    core: Settings, conn: sqlite3.Connection, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    assert cli.main(["seed"]) == 0
    report = SeedReport.model_validate(json.loads(capsys.readouterr().out))
    assert (report.skipped, report.sectors, report.events) == (False, 4, seed.EVENTS)
    assert cli.main(["seed", "--videos", str(tmp_path / "missing")]) == 3
    with pytest.raises(NotFound):
        services.seed_demo(tmp_path / "missing")
