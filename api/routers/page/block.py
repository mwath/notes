from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from api.models.page import (
    Block,
    BlockCreation,
    BlockId,
    BlockUpdate,
    Page,
    PageNotFound,
)
from api.routers import utils

router = APIRouter(
    prefix="/{page_id}",
    tags=["block"],
)


@router.get("/blocks", response_model=list[Block])
async def get_page_content(page_id: int, start: BlockId = None):
    return await Block.get_slice(page_id, start, size=-1)


@router.get("/block/{block_id}", response_model=Block)
@utils.exists("This block does not exists")
async def get_block(page_id: int, block_id: BlockId) -> Block:
    return await Block.get(page_id, block_id)


@router.post("/block/{block_id}", response_model=Block)
async def add_block(page_id: int, block_id: BlockId, block: BlockCreation) -> Block:
    if await Page.is_archived(page_id):
        raise HTTPException(status.HTTP_304_NOT_MODIFIED, "Cette page est archivée")

    try:
        return await Block.add(page_id, block_id, block)
    except PageNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    except ForeignKeyViolationError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cette page n'existe pas")


@router.put("/block/{block_id}", response_model=Block)
@utils.exists("This block does not exists")
async def update_block(page_id: int, block_id: BlockId, block: BlockUpdate) -> Block:
    if await Page.is_archived(page_id):
        raise HTTPException(status.HTTP_304_NOT_MODIFIED, "Cette page est archivée")

    return await Block.update(page_id, block_id, block)


@router.delete("/block/{block_id}", response_model=Block)
@utils.exists("This block does not exists")
async def remove_block(page_id: int, block_id: BlockId) -> Block:
    if await Page.is_archived(page_id):
        raise HTTPException(status.HTTP_304_NOT_MODIFIED, "Cette page est archivée")

    return await Block.delete(page_id, block_id)


class BlockMove(BaseModel):
    dest: BlockId | None = None


@router.put("/block/{block_id}/move")
async def move_block(page_id: int, block_id: BlockId, move: BlockMove) -> Block:
    if await Page.is_archived(page_id):
        raise HTTPException(status.HTTP_304_NOT_MODIFIED, "Cette page est archivée")

    await Block.move(page_id, block_id, move.dest)


@router.put("/blocks/swap")
async def swap_blocks(page_id: int, blocks: tuple[BlockId, BlockId]):
    if await Page.is_archived(page_id):
        raise HTTPException(status.HTTP_304_NOT_MODIFIED, "Cette page est archivée")

    try:
        await Block.swap(page_id, blocks[0], blocks[1])
    except ValueError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, str(e))
