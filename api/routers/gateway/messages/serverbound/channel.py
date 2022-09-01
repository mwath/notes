from ...client import Channel, Client
from ..clientbound.channel import ChannelNotFound
from .base import ServerBoundMessage
from .register import register


@register
class RequestJoinChannel(ServerBoundMessage):
    page_id: int

    async def handle(self, client: Client):
        if client.channel is not None:
            # check if this is already the right channel
            if client.channel.page.id == self.page_id:
                return await client.joined_channel(client.channel, client.cid)

            # otherwise remove the client from the channel
            await client.channel.remove_client(client)

        if channel := await Channel.create(client, self.page_id):
            await channel.add_client(client)
        else:
            await client.send(ChannelNotFound(page_id=self.page_id))


@register
class LeaveChannel(ServerBoundMessage):
    async def handle(self, client: Client):
        if client.channel is None:
            return

        await client.channel.remove_client(client)
