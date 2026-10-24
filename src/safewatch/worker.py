"""Background loops of the server process (tech.md 4): jobs, broadcast tick, escalation tick.

Slice 2 brings the job loop: one job at a time, idle polling between jobs.
"""

import asyncio
import contextlib

from safewatch import config, services


async def run_forever(stop: asyncio.Event) -> None:
    idle_s = config.get_settings().jobs.idle_poll_ms / 1000
    while not stop.is_set():
        if await services.run_next_job() is None:
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(stop.wait(), idle_s)
