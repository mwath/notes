from pydantic import BaseModel

from ...version import GATEWAY_VERSION
from .register import register


@register
class Handshake(BaseModel):
    version: int

    def supported(self) -> bool:
        return self.version == GATEWAY_VERSION
