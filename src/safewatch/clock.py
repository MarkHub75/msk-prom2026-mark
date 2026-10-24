"""Wall clock of the product (tech.md 7). Tests replace `now` with `fake_clock`."""

from datetime import UTC, datetime
from zoneinfo import ZoneInfo


def now() -> datetime:
    return datetime.now(UTC)


def iso(dt: datetime) -> str:
    """UTC ISO 8601 with milliseconds and `Z`, the format of every `*_at` column."""
    return dt.astimezone(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def parse(s: str) -> datetime:
    return datetime.fromisoformat(s).astimezone(UTC)


def local(dt: datetime, tz: str) -> datetime:
    return dt.astimezone(ZoneInfo(tz))
