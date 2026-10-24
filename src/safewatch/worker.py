"""Background loops of the server process (tech.md 4): jobs, broadcast tick, escalation tick.

Slice 2 brings the job loop: one job at a time, idle polling between jobs.
"""

import asyncio
import contextlib
import logging

from safewatch import config, services

log = logging.getLogger(__name__)


async def run_forever(stop: asyncio.Event) -> None:
    idle_s = config.get_settings().jobs.idle_poll_ms / 1000
    while not stop.is_set():
        try:
            job = await services.run_next_job()
        except Exception:  # a locked database must not stop the queue for good (R5)
            log.exception("job loop")
            job = None
        if job is None:
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(stop.wait(), idle_s)
