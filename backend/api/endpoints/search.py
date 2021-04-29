from typing import List
from fastapi import APIRouter

from models import Search
from models.product import ProductDB
from services.products import find_product


router = APIRouter(
    prefix='/search',
    tags=['search']
)


@router.post('/products/', response_model=List[ProductDB])
async def product_search(search_product: Search, skip=0, limit=100):
    return await find_product(search_string=search_product.search_string, skip=skip, limit=limit)
