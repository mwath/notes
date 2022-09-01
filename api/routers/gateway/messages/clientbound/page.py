from pydantic import BaseModel

from api.models.page import BlockId

from .register import register

__all__ = ["BlockModified", "BlockDeleted", "BlockAdded"]


@register
class BlockModified(BaseModel):
    block_id: BlockId


@register
class BlockDeleted(BaseModel):
    block_id: BlockId


@register
class BlockAdded(BaseModel):
    block_id: BlockId


@register
class BlockMoved(BaseModel):
    block_id: BlockId
    dest: int
