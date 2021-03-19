from typing import TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel
from couchbase.cluster import Bucket
from fastapi.encoders import jsonable_encoder


PydanticModel = TypeVar('PydanticModel', bound=BaseModel)


def get_next_id(bucket: Bucket):
    query_result = bucket.query(
        f'SELECT MAX(META(b).id) FROM {bucket.name} AS b'
    )
    next_id = int(query_result.get_single_result()['$1']) + 1
    return str(next_id)


def upsert(bucket: Bucket, value: PydanticModel, key=None):
    if not key:
        key = get_next_id(bucket)
    result = bucket.upsert(key, jsonable_encoder(value))
    if result.success:
        return_value = get(bucket, key).value
        return_value['id'] = key
        return return_value


def get(bucket: Bucket, key: UUID):
    result = bucket.get(key)
    if result.success:
        return result


def get_all(bucket: Bucket, skip: int = 0, limit: int = 100):
    query_result = bucket.query(
        f'SELECT META(b).id as id, b.* FROM {bucket.name} AS b', limit=limit, skip=skip
    )
    result = [row for row in query_result]
    return result


def filter_query(bucket: Bucket, skip: int = 0, limit: int = 100, **kwargs):
    query_string = f'SELECT META(b).id AS id,  b.* FROM {bucket.name} as b WHERE ' + \
                   ' '.join([f'{key}="{kwargs[key]}"' for key in kwargs])
    query_result = bucket.query(query_string, limit=limit, skip=skip)
    return [row for row in query_result]
