from fastapi import APIRouter

from .endpoints.products import router as products_router
from .endpoints.brands import router as brands_router
from .endpoints.tags import router as tags_router


api_router = APIRouter(
    prefix='/api'
)
api_router.include_router(products_router)
api_router.include_router(brands_router)
api_router.include_router(tags_router)
