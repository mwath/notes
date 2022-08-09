from fastapi import APIRouter, Depends, HTTPException, status

from api.models.page import Page, PageCreation
from api.models.user import User
from api.routers.auth.login import is_connected

router = APIRouter(
    prefix="/page",
    tags=["page"],
)


@router.post("", response_model=Page)
async def create_page(page: PageCreation, user: User = Depends(is_connected)) -> Page:
    return await page.create(user)


@router.get("/{page_id}", response_model=Page)
async def get_page(page_id: int, user: User = Depends(is_connected)) -> Page:
    if (page := await Page.get(page_id, user)) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This page does not exists")

    return page

