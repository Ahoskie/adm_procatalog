from typing import List
from fastapi import APIRouter, HTTPException, Response

from models.attribute import Attribute, AttributeDB, AttributePartialUpdate
from services.exceptions import DocumentNotFound, DocumentAlreadyExists
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
    try:
        return await get_attribute_by_id(attr_id=attr_id)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post('/', response_model=AttributeDB)
async def post_attr(attr: Attribute):
    try:
        attr = await create_attribute(attr)
    except DocumentAlreadyExists as e:
        raise HTTPException(status_code=400, detail=e.message)
    return attr


@router.patch('/{attr_id}/', response_model=AttributeDB)
async def patch_attr(attr_id: str, attr: AttributePartialUpdate):
    try:
        attr = await update_attribute(attr_id, attr)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DocumentAlreadyExists as e:
        raise HTTPException(status_code=400, detail=e.message)
    return attr


@router.delete('/{attr_id}/')
async def delete_attr(attr_id: str):
    try:
        attr = await remove_attribute(attr_id)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return Response(status_code=204)
