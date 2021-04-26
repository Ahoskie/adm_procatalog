from typing import List
from fastapi import APIRouter, HTTPException, Response

from models.tag import Tag, TagDB, TagPartialUpdate
from services.exceptions import DocumentNotFound, DocumentAlreadyExists
from services.tags import create_tag, get_all_tags, get_tag_by_id, update_tag_by_id, remove_tag_by_id


router = APIRouter(
    prefix='/tags',
    tags=['tags']
)


@router.get('/', response_model=List[TagDB])
async def list_tags(skip: int = 0, limit: int = 30):
    return await get_all_tags(skip, limit)


@router.get('/{tag_id}/', response_model=TagDB)
async def read_tag_by_id(tag_id: str):
    try:
        return await get_tag_by_id(tag_id=tag_id)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post('/', response_model=TagDB)
async def post_tag(tag: Tag):
    try:
        tag = await create_tag(tag)
    except DocumentAlreadyExists as e:
        raise HTTPException(status_code=400, detail=e.message)
    return tag


@router.patch('/{tag_id}/', response_model=TagDB)
async def patch_tag(tag_id: str, tag: TagPartialUpdate):
    try:
        tag = await update_tag_by_id(tag_id, tag)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DocumentAlreadyExists as e:
        raise HTTPException(status_code=400, detail=e.message)
    return tag


@router.delete('/{tag_id}/')
async def delete_tag(tag_id: str):
    try:
        tag = await remove_tag_by_id(tag_id)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return Response(status_code=204)
