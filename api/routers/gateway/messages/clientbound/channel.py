from pydantic import BaseModel

from api.models.page import Page

from .register import register


@register
class JoinedChannel(BaseModel):
    cid: int
    page: Page


@register
class LeftChannel(BaseModel):
    pass


@register
class UserJoinedChannel(BaseModel):
    cid: int
    uid: int
    username: str


@register
class UserLeftChannel(BaseModel):
    cid: int


@register
class ChannelNotFound(BaseModel):
    page_id: int
