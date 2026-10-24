"""Background loops of the server process (tech.md 4): jobs, broadcast tick, escalation tick.

Slice 0 has no loops yet: the task only waits for the server to stop.
"""

import asyncio


async def run_forever(stop: asyncio.Event) -> None:
    await stop.wait()
