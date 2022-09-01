from fastapi import APIRouter, Depends, HTTPException, status

from api.models.page import Page, PageCreation
from api.models.user import User
from api.routers import utils
from api.routers.auth.login import is_connected

PAGE_DOES_NOT_EXISTS = "Cette page n'existe pas"


router = APIRouter(tags=["page"])


@router.get("s", response_model=list[Page])
async def get_pages(only_me: bool = False, user: User = Depends(is_connected)) -> Page:
    return await Page.get_all(user if only_me else None)


@router.get("/{page_id}", response_model=Page)
@utils.exists(PAGE_DOES_NOT_EXISTS)
async def get_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    return await Page.get(page_id, user)


@router.put("/{page_id}", response_model=Page)
@utils.exists(PAGE_DOES_NOT_EXISTS)
async def update_page(page_id: int, page: PageCreation, user: User = Depends(is_connected)) -> Page:
    result = await Page.update(page_id, page, user)
    if not result.active:
        raise HTTPException(status.HTTP_304_NOT_MODIFIED, "Cette page est archivée")

    return result


@router.put("/{page_id}/archive", response_model=Page)
@utils.exists(PAGE_DOES_NOT_EXISTS)
async def archive_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    return await Page.archive(page_id, user, True)


@router.put("/{page_id}/unarchive", response_model=Page)
@utils.exists(PAGE_DOES_NOT_EXISTS)
async def unarchive_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    return await Page.archive(page_id, user, False)


@router.delete("/{page_id}", response_model=Page)
@utils.exists(PAGE_DOES_NOT_EXISTS)
async def delete_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    result = await Page.delete(page_id, user)
    if not result.active:
        raise HTTPException(status.HTTP_304_NOT_MODIFIED, "Cette page est archivée")

    return result
