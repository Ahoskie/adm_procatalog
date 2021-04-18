from typing import List
from fastapi import APIRouter, HTTPException

from models.product import Product, ProductDB
from services.products import (create_product, get_all_products, get_product_by_uuid, update_product_by_uuid,
                               remove_product_by_uuid)
from services.exceptions import DocumentNotFound, InvalidVariantAttribute


router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('/', response_model=List[ProductDB])
def list_products(skip=0, limit=30):
    return get_all_products(skip, limit)


@router.post('/', response_model=ProductDB)
def post_product(product: Product):
    try:
        return create_product(product)
    except InvalidVariantAttribute as e:
        raise HTTPException(status_code=400, detail=e.message)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get('/{product_uuid}/', response_model=ProductDB)
def read_product_by_uuid(product_uuid: str):
    try:
        return get_product_by_uuid(uuid=product_uuid)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.put('/{product_uuid}/', response_model=ProductDB)
def put_product_by_uuid(product_uuid: str, product: Product):
    try:
        return update_product_by_uuid(uuid=product_uuid, product=product)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except InvalidVariantAttribute as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.delete('/{product_uuid}/', response_model=ProductDB)
def delete_product_by_uuid(product_uuid: str):
    try:
        return remove_product_by_uuid(product_uuid)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
