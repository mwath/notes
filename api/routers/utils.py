import functools
from typing import Any, Awaitable, Callable, Iterator

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


def tosnake_iter(name: str) -> Iterator[str]:
    lasti = 0
    for i, char in enumerate(name):
        if char.isupper() and lasti != i:
            yield name[lasti:i].lower()
            lasti = i

    yield name[lasti:].lower()


def tosnake(name: str) -> str:
    return "_".join(tosnake_iter(name))
