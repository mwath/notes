import functools
from typing import Any, Awaitable, Callable

from fastapi import HTTPException, status


def exists(message: str):
    def deco(coro: Callable[..., Awaitable[Any]]):
        @functools.wraps(coro)
        async def wrapper(*a, **kw):
            if (block := await coro(*a, **kw)) is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, message)

            return block

        return wrapper

    return deco
