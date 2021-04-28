from db.buckets import Buckets
from core.config import TAGS_BUCKET, ATTRIBUTE_BUCKET
from services import upsert, get, get_all, update, delete, filter_query
from services.utils import bulk_create, get_or_bulk_create, get_document_if_exists
from services.exceptions import DocumentAlreadyExists, DocumentNotFound


async def create_tag(tag):
    bucket = await Buckets.get_bucket(TAGS_BUCKET)
    tag_for_search = tag.copy()
    delattr(tag_for_search, 'attrs')
    tags = await get_document_if_exists(bucket, tag_for_search)
    if tags:
        raise DocumentAlreadyExists(tag.name)
    tag.attrs = await get_or_bulk_create(await Buckets.get_bucket(ATTRIBUTE_BUCKET), tag.attrs)
    return await upsert(bucket, tag)


async def get_all_tags(skip=0, limit=100):
    bucket = await Buckets.get_bucket(TAGS_BUCKET)
    documents = await get_all(bucket, skip=skip, limit=limit)
    return documents


async def get_tag_by_id(tag_id):
    bucket = await Buckets.get_bucket(TAGS_BUCKET)
    document = await get(bucket, tag_id)
    return document


async def update_tag_by_id(tag_id, tag):
    bucket = await Buckets.get_bucket(TAGS_BUCKET)
    if tag.attrs:
        tag.attrs = await get_or_bulk_create(await Buckets.get_bucket(ATTRIBUTE_BUCKET), tag.attrs)
    updated_tag = await update(bucket, tag, tag_id)
    if not updated_tag:
        raise DocumentNotFound(tag_id)
    return updated_tag


async def remove_tag_by_id(tag_id):
    bucket = await Buckets.get_bucket(TAGS_BUCKET)
    return await delete(bucket, tag_id)
