from pydantic import BaseModel

from .register import register


@register
class Login(BaseModel):
    success: bool
    version: int
    username: str
