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
def list_tags(skip: int = 0, limit: int = 30):
    return get_all_tags(skip, limit)


@router.get('/{tag_id}/', response_model=TagDB)
def read_tag_by_id(tag_id: str):
    try:
        return get_tag_by_id(tag_id=tag_id)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post('/', response_model=TagDB)
def post_tag(tag: Tag):
    try:
        tag = create_tag(tag)
    except DocumentAlreadyExists as e:
        raise HTTPException(status_code=400, detail=e.message)
    return tag


@router.patch('/{tag_id}/', response_model=TagDB)
def patch_tag(tag_id: str, tag: TagPartialUpdate):
    try:
        tag = update_tag_by_id(tag_id, tag)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DocumentAlreadyExists as e:
        raise HTTPException(status_code=400, detail=e.message)
    return tag


@router.delete('/{tag_id}/')
def delete_tag(tag_id: str):
    try:
        tag = remove_tag_by_id(tag_id)
    except DocumentNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return Response(status_code=204)
