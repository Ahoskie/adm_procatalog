from typing import List
from fastapi import APIRouter, HTTPException

from models.product import Product, ProductDB
from services.products import (create_product, get_all_products, get_product_by_uuid, update_product_by_uuid,
                               remove_product_by_uuid)
from services.exceptions import DocumentNotFound, DocumentAlreadyExists


router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('/', response_model=List[ProductDB])
def list_products():
    return get_all_products()


@router.post('/')
def post_product(product: Product):
    try:
        return create_product(product)
    except DocumentAlreadyExists as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get('/{product_uuid}/', response_model=ProductDB)
def read_product_by_uuid(product_uuid: str):
    try:
        return get_product_by_uuid(uuid=product_uuid)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.patch('/{product_uuid}/', response_model=ProductDB)
def patch_product_by_uuid(product_uuid: str, product: Product):
    try:
        print(get_product_by_uuid(product_uuid))
        stored_product = get_product_by_uuid(product_uuid)
        update_data = product.dict(exclude_unset=True)
        print(update_data)
        updated_product = Product(**stored_product).copy(update=update_data)
        return update_product_by_uuid(uuid=product_uuid, product=updated_product)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.delete('/{product_uuid}/', response_model=ProductDB)
def delete_product_by_uuid(product_uuid: str):
    try:
        return delete_product_by_uuid(uuid=product_uuid)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
