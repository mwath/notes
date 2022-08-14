from fastapi import APIRouter, Depends, HTTPException, status

from api.models.page import Page, PageCreation
from api.models.user import User
from api.routers.auth.login import is_connected

router = APIRouter(tags=["page"])


@router.get("s", response_model=list[Page])
async def get_pages(user: User = Depends(is_connected)) -> Page:
    return await Page.get_all(user)


@router.get("/{page_id}", response_model=Page)
async def get_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    if (page := await Page.get(page_id, user)) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This page does not exists")

    return page


@router.put("/{page_id}", response_model=Page)
async def update_page(page_id: int, page: PageCreation, user: User = Depends(is_connected)) -> Page:
    if (page := await Page.update(page_id, page, user)) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This page does not exists")

    return page


@router.put("/{page_id}/archive", response_model=Page)
async def archive_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    if (page := await Page.archive(page_id, user, True)) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This page does not exists")

    return page


@router.put("/{page_id}/unarchive", response_model=Page)
async def unarchive_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    if (page := await Page.archive(page_id, user, False)) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This page does not exists")

    return page


@router.delete("/{page_id}", response_model=Page)
async def delete_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    if (page := await Page.delete(page_id, user)) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This page does not exists")

    return page
