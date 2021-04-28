from db.buckets import Buckets
from core.config import ATTRIBUTE_BUCKET
from services.exceptions import DocumentAlreadyExists
from services import upsert, get_all, filter_query, update, get, delete
from services.utils import get_document_if_exists


async def get_attribute_by_id(attr_id):
    bucket = await Buckets.get_bucket(ATTRIBUTE_BUCKET)
    return await get(bucket, attr_id)


async def get_all_attributes(skip=0, limit=100):
    bucket = await Buckets.get_bucket(ATTRIBUTE_BUCKET)
    return await get_all(bucket, skip=skip, limit=limit)


async def update_attribute(attr_id, attr):
    bucket = await Buckets.get_bucket(ATTRIBUTE_BUCKET)
    if len(await filter_query(bucket, name=attr.name)) == 0:
        return await update(bucket, attr, attr_id)
    raise DocumentAlreadyExists(attr.name)


async def create_attribute(attr):
    bucket = await Buckets.get_bucket(ATTRIBUTE_BUCKET)
    attributes_results = await get_document_if_exists(bucket, attr)
    if not attributes_results:
        return await upsert(bucket, attr)
    raise DocumentAlreadyExists(attr.name)


async def remove_attribute(attr_id):
    bucket = await Buckets.get_bucket(ATTRIBUTE_BUCKET)
    return await delete(bucket, attr_id)
