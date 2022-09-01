from api.models.page import BlockId

from ...client import Client
from ..clientbound import page as cmsg
from .base import ServerBoundMessage
from .register import register

__all__ = ["BlockModified"]


@register
class BlockModified(ServerBoundMessage):
    block_id: BlockId

    async def handle(self, client: Client):
        if client.channel is not None:
            await client.channel.broadcast(cmsg.BlockModified(block_id=self.block_id), client.cid)


@register
class BlockDeleted(ServerBoundMessage):
    block_id: BlockId

    async def handle(self, client: Client):
        if client.channel is not None:
            await client.channel.broadcast(cmsg.BlockDeleted(block_id=self.block_id), client.cid)


@register
class BlockAdded(ServerBoundMessage):
    block_id: BlockId

    async def handle(self, client: Client):
        if client.channel is not None:
            await client.channel.broadcast(cmsg.BlockAdded(block_id=self.block_id), client.cid)


@register
class BlockMoved(ServerBoundMessage):
    block_id: BlockId
    dest: int

    async def handle(self, client: Client):
        if client.channel is not None:
            await client.channel.broadcast(cmsg.BlockMoved(block_id=self.block_id, dest=self.dest), client.cid)
