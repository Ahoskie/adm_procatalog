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
async def list_products(skip=0, limit=30):
    return await get_all_products(skip, limit)


@router.post('/', response_model=ProductDB)
async def post_product(product: Product):
    try:
        return await create_product(product)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get('/{product_uuid}/', response_model=ProductDB)
async def read_product_by_uuid(product_uuid: str):
    try:
        return await get_product_by_uuid(uuid=product_uuid)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.patch('/{product_uuid}/', response_model=ProductDB)
async def patch_product_by_uuid(product_uuid: str, product: ProductPartialUpdate):
    try:
        return await update_product_by_uuid(uuid=product_uuid, product=product)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.delete('/{product_uuid}/', response_model=ProductDB)
async def delete_product_by_uuid(product_uuid: str):
    try:
        await remove_product_by_uuid(product_uuid)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return Response(status_code=204)
