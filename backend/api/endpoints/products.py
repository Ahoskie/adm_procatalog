from typing import List
from fastapi import APIRouter, HTTPException, Response

from models.product import Product, ProductDB, ProductPartialUpdate
from services.products import (create_product, get_all_products, get_product_by_uuid, update_product_by_uuid,
                               remove_product_by_uuid)
from services.exceptions import DocumentNotFound, InvalidVariantAttribute
from db.exceptions import DatabaseException


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
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get('/{product_uuid}/', response_model=ProductDB)
def read_product_by_uuid(product_uuid: str):
    try:
        return get_product_by_uuid(uuid=product_uuid)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.patch('/{product_uuid}/', response_model=ProductDB)
def patch_product_by_uuid(product_uuid: str, product: ProductPartialUpdate):
    try:
        return update_product_by_uuid(uuid=product_uuid, product=product)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.delete('/{product_uuid}/', response_model=ProductDB)
def delete_product_by_uuid(product_uuid: str):
    try:
        remove_product_by_uuid(product_uuid)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return Response(status_code=204)
