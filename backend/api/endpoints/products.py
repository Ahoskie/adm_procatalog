from typing import List
from fastapi import APIRouter, Response, Request, HTTPException

from models.product import Product, ProductDB, ProductPartialUpdate
from services.products import (create_product, get_all_products, get_product_by_uuid, update_product_by_uuid,
                               remove_product_by_uuid)
from services.roles import Permissions, user_has_permissions


router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('/', response_model=List[ProductDB])
async def list_products(skip=0, limit=100):
    return await get_all_products(skip, limit)


@router.post('/', response_model=ProductDB)
async def post_product(request: Request, product: Product):
    user = request.scope['user']
    user_has_permissions(user, Permissions.WRITE)
    return await create_product(product)


@router.get('/{product_uuid}/', response_model=ProductDB)
async def read_product_by_uuid(product_uuid: str):
    return await get_product_by_uuid(uuid=product_uuid)


@router.patch('/{product_uuid}/', response_model=ProductDB)
async def patch_product_by_uuid(request: Request, product_uuid: str, product: ProductPartialUpdate):
    user = request.scope['user']
    user_has_permissions(user, Permissions.WRITE)
    return await update_product_by_uuid(uuid=product_uuid, product=product)


@router.delete('/{product_uuid}/', response_model=ProductDB)
async def delete_product_by_uuid(request: Request, product_uuid: str):
    user = request.scope['user']
    user_has_permissions(user, Permissions.WRITE)
    await remove_product_by_uuid(product_uuid)
    return Response(status_code=204)
