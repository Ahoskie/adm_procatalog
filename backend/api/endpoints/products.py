from typing import List
from fastapi import APIRouter

from models.product import Product, ProductDB, Brand, BrandDB
from crud.products import get_product, create_product, get_all_products, get_product_by_name


router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('/')
def list_products():
    return get_all_products()


@router.post('/')
def post_product(product: Product):
    return create_product(product)


@router.get('/{product_name}/')
def read_product_by_name(product_name: str):
    return get_product_by_name(name=product_name)

