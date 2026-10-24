"""Background loops of the server process (tech.md 4): jobs, broadcast tick, escalation tick.

The job loop runs one job at a time and polls the queue while it is empty; the broadcast loop
calls `broadcast_tick` every `broadcast.tick_ms`. Both stop within one period of `stop`.
"""

import asyncio
import logging

from safewatch import config, services

log = logging.getLogger(__name__)


async def _jobs(stop: asyncio.Event, idle_s: float) -> None:
    while not stop.is_set():
        try:
            job = await services.run_next_job()
        except Exception:  # a locked database must not stop the queue for good (R5)
            log.exception("job loop")
            job = None
        if job is None:
            await asyncio.sleep(idle_s)


async def _broadcasts(stop: asyncio.Event, tick_s: float) -> None:
    while not stop.is_set():
        try:
            services.broadcast_tick()
        except Exception:  # one bad tick must not stop the broadcasts for good
            log.exception("broadcast tick")
        await asyncio.sleep(tick_s)


async def run_forever(stop: asyncio.Event) -> None:
    settings = config.get_settings()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(_jobs(stop, settings.jobs.idle_poll_ms / 1000))
        tg.create_task(_broadcasts(stop, settings.broadcast.tick_ms / 1000))
