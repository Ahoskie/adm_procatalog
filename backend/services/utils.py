from typing import List

from couchbase.cluster import Bucket
from pydantic import BaseModel

from db.buckets import Buckets
from . import filter_query, upsert


def output_pydantic_model(model: BaseModel):
    def generate_model(func):
        def wrapper(*args, **kwargs):
            db_result = func(*args, **kwargs)
            if type(db_result) == list:
                return [model.parse_obj(db_dict) for db_dict in func()]
            return model.parse_obj(db_result)
        return wrapper
    return generate_model


def get_document_if_exists(bucket: Bucket, model: BaseModel):
    data = model.dict()
    result = filter_query(bucket, **data)
    return result[0] if result else None


def get_or_create(bucket: Bucket, model: BaseModel):
    document = get_document_if_exists(bucket, model)
    if not document:
        document = upsert(bucket, model)
    return document
