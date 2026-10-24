from safewatch.hub import CLIENT_QUEUE, Hub
from safewatch.types import CameraState, WsMessage

STATE = CameraState(
    camera_id=1, sector_id=1, state="normal", reason=None, reason_text="", freshness_ms=None,
    open_yellow=0, open_red=0,
)  # fmt: skip


async def test_audience_filtering() -> None:
    hub = Hub()
    operator, master = hub.connect("operator"), hub.connect("master")
    hub.publish("camera.state", STATE, audience=["master"])
    hub.publish("camera.state", STATE)
    assert operator.queue.qsize() == 1
    assert master.queue.qsize() == 2
    message = WsMessage.model_validate_json(master.queue.get_nowait() or "")
    assert (message.type, message.data) == ("camera.state", STATE)


async def test_queue_overflow_drops_client() -> None:
    hub = Hub()
    slow = hub.connect("operator")
    for _ in range(CLIENT_QUEUE):
        hub.publish("camera.state", STATE)
    assert slow in hub.clients and not slow.dropped
    hub.publish("camera.state", STATE)
    assert slow not in hub.clients and slow.dropped
    assert slow.queue.qsize() == CLIENT_QUEUE + 1  # the last item is the stop marker
