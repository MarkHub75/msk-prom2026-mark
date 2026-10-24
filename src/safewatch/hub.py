"""WebSocket fan-out by role (tech.md 6.5)."""

import asyncio

from pydantic import BaseModel

from safewatch import clock
from safewatch.types import Role, WsMessage, WsType

# A client that leaves this many messages unread is dropped (close 1013); the frontend
# reconnects and rereads its screen over REST.
CLIENT_QUEUE = 1000


class Client:
    def __init__(self, role: Role) -> None:
        self.role = role
        # Unbounded: the limit is checked in publish, so the stop marker always fits.
        self.queue: asyncio.Queue[str | None] = asyncio.Queue()


class Hub:
    def __init__(self) -> None:
        self.clients: set[Client] = set()

    def connect(self, role: Role) -> Client:
        client = Client(role)
        self.clients.add(client)
        return client

    def disconnect(self, client: Client) -> None:
        self.clients.discard(client)

    def publish(self, type: WsType, data: BaseModel, audience: list[Role] | None = None) -> None:
        message = WsMessage.model_validate({"type": type, "at": clock.now(), "data": data})
        payload = message.model_dump_json()
        for client in list(self.clients):
            if audience and client.role not in audience:
                continue
            if client.queue.qsize() >= CLIENT_QUEUE:
                self.disconnect(client)
                client.queue.put_nowait(None)
                continue
            client.queue.put_nowait(payload)


hub = Hub()
