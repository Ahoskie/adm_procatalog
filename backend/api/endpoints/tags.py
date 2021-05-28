from typing import List
from fastapi import APIRouter, Response, Request, HTTPException

from models.tag import Tag, TagDB, TagPartialUpdate
from services.tags import create_tag, get_all_tags, get_tag_by_id, update_tag_by_id, remove_tag_by_id
from services.roles import Permissions, user_has_permissions


router = APIRouter(
    prefix='/tags',
    tags=['tags']
)


@router.get('/', response_model=List[TagDB])
async def list_tags(skip: int = 0, limit: int = 100):
    return await get_all_tags(skip, limit)


@router.get('/{tag_id}/', response_model=TagDB)
async def read_tag_by_id(tag_id: str):
    return await get_tag_by_id(tag_id=tag_id)


@router.post('/', response_model=TagDB)
async def post_tag(request: Request, tag: Tag):
    user = request.scope['user']
    user_has_permissions(user, Permissions.WRITE)
    tag = await create_tag(tag)
    return tag


@router.patch('/{tag_id}/', response_model=TagDB)
async def patch_tag(request: Request, tag_id: str, tag: TagPartialUpdate):
    user = request.scope['user']
    user_has_permissions(user, Permissions.WRITE)
    tag = await update_tag_by_id(tag_id, tag)
    return tag


@router.delete('/{tag_id}/')
async def delete_tag(request: Request, tag_id: str):
    user = request.scope['user']
    user_has_permissions(user, Permissions.WRITE)
    await remove_tag_by_id(tag_id)
    return Response(status_code=204)
