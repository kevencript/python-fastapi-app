from fastapi import APIRouter

from embed.routers.v1.auth import router as auth_api
from embed.routers.v1.posts import router as posts_api

router = APIRouter()

router.include_router(auth_api, prefix="/auth", tags=["Auth"])
router.include_router(posts_api, prefix="/post", tags=["Posts"])
