from uuid import uuid4

from couchbase.exceptions import DocumentNotFoundException

from db.buckets import Buckets
from core.config import PRODUCTS_BUCKET, BRANDS_BUCKET, TAGS_BUCKET
from services import upsert, get, get_all, filter_query, update, delete
from services.utils import get_or_create
from services.exceptions import DocumentNotFound, DocumentAlreadyExists


def create_product(product):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    brand = get_or_create(Buckets.get_bucket(BRANDS_BUCKET), product.brand)
    product.brand = brand

    tags = list()
    for tag in product.tags:
        tags.append(get_or_create(Buckets.get_bucket(TAGS_BUCKET), tag))
    product.tags = tags

    result_product = upsert(bucket, product, key=str(uuid4()))
    return result_product


def get_all_products():
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    return get_all(bucket)


def get_product_by_uuid(uuid):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    try:
        product = get(bucket, uuid)
    except DocumentNotFoundException:
        raise DocumentNotFound(uuid)
    return product


def update_product_by_uuid(uuid, product):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    return update(bucket, product, uuid)


def remove_product_by_uuid(uuid):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    try:
        return delete(bucket, uuid)
    except DocumentNotFoundException:
        raise DocumentNotFound(uuid)
