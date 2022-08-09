from api.routers.auth.login import is_connected
from .page import router as page_router

from fastapi import APIRouter, Depends

router = APIRouter(dependencies=[Depends(is_connected)])
router.include_router(page_router)

