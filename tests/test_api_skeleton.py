import re
from pathlib import Path

import httpx
import pytest
from fastapi import APIRouter
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from safewatch import api, services
from safewatch.api import create_app
from safewatch.config import Settings
from safewatch.errors import (
    AppError,
    Conflict,
    Forbidden,
    NotFound,
    RoleRequired,
    TooLarge,
    UnsupportedVideo,
    ValidationFailed,
)
from safewatch.types import ApiError

ROOT = Path(__file__).resolve().parents[1]
ROUTE_ROW = re.compile(
    r"^\| `@router\.(\w+)\(\"([^\"]+)\"(?:, status_code=\d+)?\)` "
    r"\| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \| (\d+) \|",
    re.M,
)


def _contract_routes() -> list[tuple[str, str, int]]:
    tech = (ROOT / "tech.md").read_text(encoding="utf-8")
    section = tech.split("### 6.4", 1)[1].split("### 6.5", 1)[0]
    return [(m.group(1), m.group(2), int(m.group(3))) for m in ROUTE_ROW.finditer(section)]


async def test_health_ok(client: httpx.AsyncClient) -> None:
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "contract": "1.0.0"}


def test_every_contract_route_is_declared(settings: Settings) -> None:
    routes = _contract_routes()
    assert len(routes) == 55
    openapi = create_app(settings).openapi()["paths"]
    declared = {
        (method.lower(), route.path)
        for route in api.router.routes
        for method in getattr(route, "methods", None) or {"websocket"}
    }
    assert {p for m, p in declared if m != "websocket"} == set(openapi)
    missing = [(m, p) for m, p, _ in routes if (m, p) not in declared]
    assert missing == []


async def test_unbuilt_route_returns_501(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Every route is built since slice 13: an unfinished slice is a facade raising the stub.
    def unbuilt(*_: object) -> None:
        raise NotImplementedError("slice 13")

    monkeypatch.setattr(services, "management_view", unbuilt)
    response = await client.get("/api/stats/management")
    assert response.status_code == 501
    body = ApiError.model_validate(response.json())
    assert body.code == "not_implemented"
    assert body.message.startswith("Функция появится в слайсе")


async def test_request_errors_are_api_errors(client: httpx.AsyncClient) -> None:
    bad_role = await client.post("/api/sectors", json={"name": "A"}, headers={"X-Role": "boss"})
    assert (bad_role.status_code, bad_role.json()["code"]) == (400, "role_required")
    bad_form = await client.post("/api/sectors", json={"name": 5}, headers={"X-Role": "admin"})
    assert bad_form.status_code == 422
    assert ApiError.model_validate(bad_form.json()).code == "validation"
    assert bad_form.json()["details"]["field"] == "body.name"
    long_actor = {"X-Role": "operator", "X-Actor": "%D0%AF" * 61}
    actor = await client.post("/api/events/1/actions", json={"action": "view"}, headers=long_actor)
    assert (actor.status_code, actor.json()["code"]) == (422, "validation")
    ok_actor = {"X-Role": "operator", "X-Actor": "%D0%AF" * 60}
    actor = await client.post("/api/events/1/actions", json={"action": "view"}, headers=ok_actor)
    assert actor.status_code == 404  # the name passed, the event is missing


ERRORS: list[tuple[AppError, int, str]] = [
    (NotFound("нет"), 404, "not_found"),
    (ValidationFailed("плохо", field="name"), 422, "validation"),
    (Conflict("name_taken", "занято"), 409, "name_taken"),
    (Forbidden("нельзя"), 403, "forbidden_role"),
    (RoleRequired("роль"), 400, "role_required"),
    (TooLarge("большой"), 413, "too_large"),
    (UnsupportedVideo("формат"), 415, "unsupported_video"),
]


@pytest.mark.parametrize(("error", "status", "code"), ERRORS)
def test_app_errors_map_to_status_codes(
    settings: Settings, error: AppError, status: int, code: str, tmp_path: Path
) -> None:
    bare = settings.model_copy(deep=True)
    bare.server.static_dir = tmp_path / "no-frontend"  # the temp route goes after the mount
    app = create_app(bare)
    temp = APIRouter()

    @temp.get("/api/test-error")
    async def fail() -> None:
        raise error

    app.include_router(temp)
    response = TestClient(app).get("/api/test-error")
    assert response.status_code == status
    body = ApiError.model_validate(response.json())
    assert (body.code, body.message) == (code, error.message)
    assert body.details == error.details


def test_ws_hello_and_unknown_role(settings: Settings, conn: object) -> None:
    client = TestClient(create_app(settings))
    with client.websocket_connect("/ws?role=operator") as ws:
        hello = ws.receive_json()
        assert hello["type"] == "hello"
        assert hello["data"]["role"] == "operator"
        assert hello["data"]["contract"] == api.CONTRACT_VERSION
    with pytest.raises(WebSocketDisconnect) as closed:
        with client.websocket_connect("/ws?role=boss") as ws:
            ws.receive_json()
    assert closed.value.code == 4400


async def test_frontend_is_served_with_spa_fallback(core: Settings, tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<p>SafeWatch</p>", encoding="utf-8")
    app_settings = core.model_copy(deep=True)
    app_settings.server.static_dir = dist
    transport = httpx.ASGITransport(app=create_app(app_settings))
    async with httpx.AsyncClient(transport=transport, base_url="http://127.0.0.1") as c:
        assert (await c.get("/operator/cameras/3")).text == "<p>SafeWatch</p>"
        assert (await c.get("/api/health")).json()["status"] == "ok"
        assert (await c.get("/api/no-such-route")).status_code == 404
