from fastapi import APIRouter, HTTPException

from models.product import Tag, TagDB
from services.exceptions import DocumentNotFound, DocumentAlreadyExists
from services.tags import create_tag, get_all_tags, get_tag_by_id, update_tag_by_id, remove_tag_by_id


router = APIRouter(
    prefix='/tags',
    tags=['tags']
)


@router.get('/')
def list_tags():
    return get_all_tags()


@router.get('/{tag_id}/')
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


@router.patch('/{tag_id}/')
def patch_tag(tag_id: str, tag: Tag):
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
    return tag
