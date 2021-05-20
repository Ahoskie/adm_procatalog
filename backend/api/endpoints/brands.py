from typing import List
from fastapi import APIRouter, Response

from models.brand import Brand, BrandDB, BrandPartialUpdate
from services.brands import get_brand_by_id, get_all_brands, create_brand, update_brand, remove_brand


router = APIRouter(
    prefix='/brands',
    tags=['brands']
)


@router.get('/', response_model=List[BrandDB])
async def list_brands(skip: int = 0, limit: int = 100):
    return await get_all_brands(skip, limit)


@router.get('/{brand_id}/', response_model=BrandDB)
async def read_brand_by_id(brand_id: str):
    return await get_brand_by_id(brand_id=brand_id)


@router.post('/', response_model=BrandDB)
async def post_brand(brand: Brand):
    brand = await create_brand(brand)
    return brand


@router.patch('/{brand_id}/', response_model=BrandDB)
async def patch_brand(brand_id: str, brand: BrandPartialUpdate):
    brand = await update_brand(brand_id, brand)
    return brand


@router.delete('/{brand_id}/')
async def delete_brand(brand_id: str):
    await remove_brand(brand_id)
    return Response(status_code=204)
