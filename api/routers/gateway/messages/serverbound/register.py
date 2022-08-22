import warnings
from typing import Type

from pydantic import BaseModel

from api.routers.utils import tosnake

serverbound_messages: dict[str, BaseModel] = {}


def register(cls: Type[BaseModel]):
    msgid = tosnake(cls.__name__)
    if msgid in serverbound_messages:
        warnings.warn(f"Message already registered: {msgid}.")
    else:
        serverbound_messages[msgid] = cls

    return cls
