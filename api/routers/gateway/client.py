from __future__ import annotations

import random
from typing import Awaitable, TypedDict

from pydantic import BaseModel
from starlette.websockets import WebSocket

from api.models.page import Page
from api.routers.auth.login import User
from api.routers.utils import tosnake

from .messages.clientbound.channel import (
    JoinedChannel,
    LeftChannel,
    UserJoinedChannel,
    UserLeftChannel,
)

channels: dict[int, Channel] = {}


class Channel:
    def __init__(self, page: Page):
        self.page = page
        self.clients: dict[int, Client] = {}

    @classmethod
    async def create(cls, client: Client, page_id: int) -> Channel | None:
        channel = channels.get(page_id)
        if channel is None and (page := await Page.get(page_id, client.user)):
            channels[page_id] = channel = Channel(page)

        return channel

    async def add_client(self, client: Client):
        # generate new random id that does not exists
        while (cid := random.randint(0, 1_000_000)) in self.clients:
            pass

        self.clients[cid] = client
        client.cid = cid
        client.channel = self

        msg = UserJoinedChannel(cid=cid, uid=client.user.id, username=client.user.username)
        await client.joined_channel(self, cid)
        await self.broadcast(msg, except_=cid)

    async def remove_client(self, client: Client):
        client = self.clients.pop(client.cid)
        await client.left_channel(self)
        await self.broadcast(UserLeftChannel(cid=client.cid))

    async def broadcast(self, message: BaseModel, except_: int | set[int] = None):
        """Send a message to all connecetd websocket clients.
        Will not send the message the client's id specified in `except_`."""

        ids = set(self.clients.keys())
        if except_ is not None:
            ids.difference_update(except_ if isinstance(except_, set) else [except_])

        for cid in ids:
            await self.clients[cid].send(message)

    async def close(self):
        for client in self.clients.values():
            await client.close()


class Message(TypedDict):
    id: str
    data: dict


class MessageModel(BaseModel):
    id: str
    data: dict


class Client:
    def __init__(self, ws: WebSocket, user: User, cid: int = 0, channel: Channel | None = None):
        self.ws = ws
        self.cid = cid
        self.user = user
        self.channel = channel

    def send(self, msg: BaseModel) -> Awaitable[None]:
        name = tosnake(msg.__class__.__name__)
        return self.ws.send_text(MessageModel(id=name, data=msg.dict()).json())

    async def disconnected(self):
        if self.channel is not None:
            await self.channel.remove_client(self)

    async def joined_channel(self, channel: Channel, cid: int):
        await self.send(JoinedChannel(cid=cid, page=channel.page))

    async def left_channel(self, channel: Channel):
        if self.channel is not None and self.channel != channel:
            return

        self.channel = None
        await self.send(LeftChannel())

    async def handle_message(self, msg: Message):
        if "id" not in msg or "data" not in msg:
            raise ValueError("Message is missing id or data")

        msgid = msg["id"]
        cls = serverbound_messages.get(msgid)
        if cls is None:
            raise ValueError(f"Invalid serverbound message: {msgid}")

        msg = cls(**msg["data"])
        await msg.handle(self)


from .messages.serverbound.register import serverbound_messages
