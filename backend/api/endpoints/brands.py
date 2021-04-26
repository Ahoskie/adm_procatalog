from typing import List
from fastapi import APIRouter, HTTPException, Response

from models.brand import Brand, BrandDB, BrandPartialUpdate
from services.exceptions import DocumentNotFound, DocumentAlreadyExists
from services.brands import get_brand_by_id, get_all_brands, create_brand, update_brand, remove_brand


router = APIRouter(
    prefix='/brands',
    tags=['brands']
)


@router.get('/', response_model=List[BrandDB])
async def list_brands(skip: int = 0, limit: int = 30):
    return await get_all_brands(skip, limit)


@router.get('/{brand_id}/', response_model=BrandDB)
async def read_brand_by_id(brand_id: str):
    try:
        return await get_brand_by_id(brand_id=brand_id)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post('/', response_model=BrandDB)
async def post_brand(brand: Brand):
    try:
        brand = await create_brand(brand)
    except DocumentAlreadyExists as e:
        raise HTTPException(status_code=400, detail=e.message)
    return brand


@router.patch('/{brand_id}/', response_model=BrandDB)
async def patch_brand(brand_id: str, brand: BrandPartialUpdate):
    try:
        brand = await update_brand(brand_id, brand)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DocumentAlreadyExists as e:
        raise HTTPException(status_code=400, detail=e.message)
    return brand


@router.delete('/{brand_id}/')
async def delete_brand(brand_id: str):
    try:
        brand = await remove_brand(brand_id)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return Response(status_code=204)
