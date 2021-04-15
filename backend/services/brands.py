from couchbase.exceptions import DocumentNotFoundException

from db.buckets import Buckets
from core.config import BRANDS_BUCKET
from .exceptions import DocumentAlreadyExists, DocumentNotFound
from . import upsert, get_all, filter_query, update, get, delete


def get_all_brands():
    bucket = Buckets.get_bucket(BRANDS_BUCKET)
    return get_all(bucket)


def get_brand_by_id(brand_id):
    bucket = Buckets.get_bucket(BRANDS_BUCKET)
    try:
        return get(bucket, brand_id)
    except DocumentNotFoundException:
        raise DocumentNotFound(brand_id)


def create_brand(brand):
    bucket = Buckets.get_bucket(BRANDS_BUCKET)
    brand_results = filter_query(bucket, name=brand.name)
    if not brand_results:
        return upsert(bucket, brand)
    raise DocumentAlreadyExists(brand.name)


def update_brand(brand_id, brand):
    bucket = Buckets.get_bucket(BRANDS_BUCKET)
    if len(filter_query(bucket, name=brand.name)) == 0:
        return update(bucket, brand, brand_id)
    raise DocumentAlreadyExists(brand.name)


def remove_brand(brand_id):
    bucket = Buckets.get_bucket(BRANDS_BUCKET)
    try:
        return delete(bucket, brand_id)
    except DocumentNotFoundException:
        raise DocumentNotFound(brand_id)
