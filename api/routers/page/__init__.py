from fastapi import APIRouter, Depends

from api.models.page import Page, PageCreation
from api.models.user import User
from api.routers.auth.login import is_connected

from .block import router as block_router
from .page import router as page_router

router = APIRouter(prefix="/page", dependencies=[Depends(is_connected)])


@router.post("", response_model=Page, tags=page_router.tags)
async def create_page(page: PageCreation, user: User = Depends(is_connected)) -> Page:
    return await page.create(user)


router.include_router(page_router)
router.include_router(block_router)
