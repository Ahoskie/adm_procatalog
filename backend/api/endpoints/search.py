from fastapi import APIRouter

from models.product import Product
from services.products import fulltext_find_product


router = APIRouter(
    prefix='/search',
    tags=['search']
)


@router.post('/')
def post_product(product: Product, limit=30):
    return fulltext_find_product(limit=limit, search_string=product.name)
