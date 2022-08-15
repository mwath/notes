from fastapi import APIRouter, Depends

from api.models.page import Page, PageCreation
from api.models.user import User
from api.routers import utils
from api.routers.auth.login import is_connected

router = APIRouter(tags=["page"])


@router.get("s", response_model=list[Page])
async def get_pages(user: User = Depends(is_connected)) -> Page:
    return await Page.get_all(user)


@router.get("/{page_id}", response_model=Page)
@utils.exists("This page does not exists")
async def get_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    return await Page.get(page_id, user)


@router.put("/{page_id}", response_model=Page)
@utils.exists("This page does not exists")
async def update_page(page_id: int, page: PageCreation, user: User = Depends(is_connected)) -> Page:
    return await Page.update(page_id, page, user)


@router.put("/{page_id}/archive", response_model=Page)
@utils.exists("This page does not exists")
async def archive_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    return await Page.archive(page_id, user, True)


@router.put("/{page_id}/unarchive", response_model=Page)
@utils.exists("This page does not exists")
async def unarchive_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    return await Page.archive(page_id, user, False)


@router.delete("/{page_id}", response_model=Page)
@utils.exists("This page does not exists")
async def delete_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    return await Page.delete(page_id, user)