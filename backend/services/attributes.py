from db.buckets import Buckets
from core.config import ATTRIBUTE_BUCKET
from services.exceptions import DocumentAlreadyExists
from services import upsert, get_all, filter_query, update, get, delete


def get_attribute_by_id(attr_id):
    bucket = Buckets.get_bucket(ATTRIBUTE_BUCKET)
    return get(bucket, attr_id)


def get_all_attributes(skip=0, limit=30):
    bucket = Buckets.get_bucket(ATTRIBUTE_BUCKET)
    return get_all(bucket, skip=skip, limit=limit)


def update_attribute(attr_id, attr):
    bucket = Buckets.get_bucket(ATTRIBUTE_BUCKET)
    if len(filter_query(bucket, name=attr.name)) == 0:
        return update(bucket, attr, attr_id)
    raise DocumentAlreadyExists(attr.name)


def create_attribute(attr):
    bucket = Buckets.get_bucket(ATTRIBUTE_BUCKET)
    attributes_results = filter_query(bucket, name=attr.name)
    if not attributes_results:
        return upsert(bucket, attr)
    raise DocumentAlreadyExists(attr.name)


def remove_attribute(attr_id):
    bucket = Buckets.get_bucket(ATTRIBUTE_BUCKET)
    return delete(bucket, attr_id)
