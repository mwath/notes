from pydantic import BaseModel

from ...client import Client


class ServerBoundMessage(BaseModel):
    async def handle(self, client: Client):
        raise NotImplementedError()
