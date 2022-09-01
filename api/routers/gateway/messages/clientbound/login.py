from pydantic import BaseModel

from .register import register

__all__ = ["Login"]


@register
class Login(BaseModel):
    success: bool
    version: int
    username: str
