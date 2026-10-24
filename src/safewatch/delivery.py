"""Delivery channels to outside systems (tech.md 6.1, slice 15): lamps, sirens, speakers.

`deliver` blocks on the network: `services.deliveries_flush` calls it in `asyncio.to_thread`
and writes the outcome to the base itself.
"""

from urllib.parse import urlsplit

import httpx

from safewatch import clock, texts
from safewatch.types import DeliveryKind, EventSummary, Level


def target(url: str) -> str:
    """Host and port of a URL: no scheme, path, query or credentials (`Channel.target`)."""
    parts = urlsplit(url)
    host = parts.hostname or ""
    return host if parts.port is None else f"{host}:{parts.port}"


class WebhookChannel:  # DeliveryChannel: POST JSON to delivery.webhooks[i].url, timeout from config
    def __init__(self, name: str, url: str, levels: list[Level], timeout_s: float) -> None:
        self.name = name
        self.url = url
        self.levels = levels
        self.timeout_s = timeout_s

    def deliver(self, event: EventSummary, kind: DeliveryKind) -> tuple[bool, int | None, str]:
        body = {
            "event_id": event.id,
            "kind": kind,
            "level": event.level,
            "scenario": event.scenario,
            "title": event.title,
            "sector": event.sector_name,
            "camera": event.camera_name,
            "zone": event.zone_name,
            "text": event.notification_text,
            "at": clock.iso(clock.now()),
        }
        try:
            response = httpx.post(self.url, json=body, timeout=self.timeout_s)
        except httpx.TimeoutException:
            return False, None, texts.DELIVERY_TIMEOUT
        except httpx.HTTPError as exc:  # the URL may carry credentials: keep only the error type
            return False, None, texts.DELIVERY_UNREACHABLE.format(error=type(exc).__name__)
        if response.is_success:
            return True, response.status_code, ""
        return False, response.status_code, texts.DELIVERY_HTTP.format(status=response.status_code)
