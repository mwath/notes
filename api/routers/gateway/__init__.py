from __future__ import annotations

from json import JSONDecodeError

from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket, WebSocketDisconnect

from api.routers.auth.login import User, is_connected_pass, oauth2_scheme

from .client import Client
from .export import export_messages
from .messages.clientbound.login import Login
from .messages.serverbound import Handshake
from .version import GATEWAY_VERSION

__all__ = ["export_messages", "router"]

router = APIRouter(
    prefix="/gateway",
    tags=["gateway"],
)


async def is_connected(ws: WebSocket):
    token = await oauth2_scheme(ws)
    userpass = await is_connected_pass(token)
    return User(**userpass.dict())


@router.websocket("")
async def websocket_gateway(ws: WebSocket, user: User = Depends(is_connected)):
    client: Client = None
    await ws.accept()
    try:
        msg = await ws.receive_json()
        if msg.get("id") == "handshake" and "data" in msg:
            handshake = Handshake(**msg["data"])
            supported = handshake.supported()
            client = Client(ws, user, 0, None)

            await client.send(Login(success=supported, version=GATEWAY_VERSION, username=user.username))
            if supported:
                async for msg in ws.iter_json():
                    await client.handle_message(msg)

    except JSONDecodeError:
        print("Disconnect client due to decode error")
    except ValueError as e:
        print(f"Disconnect client due to {e}")
    except WebSocketDisconnect:
        pass

    if client is not None:
        await client.disconnected()
