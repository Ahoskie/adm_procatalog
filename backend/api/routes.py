from fastapi import APIRouter

from .endpoints.products import router as products_router
from .endpoints.attributes import router as attrs_router
from .endpoints.brands import router as brands_router
from .endpoints.tags import router as tags_router
from .endpoints.search import router as search_router
from .endpoints.internal import router as internal_router


api_router = APIRouter(
    prefix='/api'
)
api_router.include_router(products_router)
api_router.include_router(internal_router)
api_router.include_router(brands_router)
api_router.include_router(search_router)
api_router.include_router(attrs_router)
api_router.include_router(tags_router)
