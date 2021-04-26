from db.buckets import Buckets
from core.config import BRANDS_BUCKET
from .exceptions import DocumentAlreadyExists
from . import upsert, get_all, filter_query, update, get, delete


async def get_all_brands(skip=0, limit=30):
    bucket = await Buckets.get_bucket(BRANDS_BUCKET)
    return await get_all(bucket, skip=skip, limit=limit)


async def get_brand_by_id(brand_id):
    bucket = await Buckets.get_bucket(BRANDS_BUCKET)
    return await get(bucket, brand_id)


async def create_brand(brand):
    bucket = await Buckets.get_bucket(BRANDS_BUCKET)
    brand_results = await filter_query(bucket, name=brand.name)
    if not brand_results:
        return await upsert(bucket, brand)
    raise DocumentAlreadyExists(brand.name)


async def update_brand(brand_id, brand):
    bucket = await Buckets.get_bucket(BRANDS_BUCKET)
    if len(await filter_query(bucket, name=brand.name)) == 0:
        return await update(bucket, brand, brand_id)
    raise DocumentAlreadyExists(brand.name)


async def remove_brand(brand_id):
    bucket = await Buckets.get_bucket(BRANDS_BUCKET)
    return await delete(bucket, brand_id)
