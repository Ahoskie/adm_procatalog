from typing import List
from fastapi import APIRouter, Response

from models.attribute import Attribute, AttributeDB, AttributePartialUpdate
from services.attributes import (create_attribute, get_all_attributes, get_attribute_by_id, update_attribute,
                                 remove_attribute)


router = APIRouter(
    prefix='/attributes',
    tags=['attributes']
)


@router.get('/', response_model=List[AttributeDB])
async def list_attrs(skip: int = 0, limit: int = 100):
    return await get_all_attributes(skip, limit)


@router.get('/{attr_id}/', response_model=AttributeDB)
async def read_attr_by_id(attr_id: str):
    return await get_attribute_by_id(attr_id=attr_id)


@router.post('/', response_model=AttributeDB)
async def post_attr(attr: Attribute):
    attr = await create_attribute(attr)
    return attr


@router.patch('/{attr_id}/', response_model=AttributeDB)
async def patch_attr(attr_id: str, attr: AttributePartialUpdate):
    attr = await update_attribute(attr_id, attr)
    return attr


@router.delete('/{attr_id}/')
async def delete_attr(attr_id: str):
    await remove_attribute(attr_id)
    return Response(status_code=204)
