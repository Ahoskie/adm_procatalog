from typing import TypeVar

from pydantic import BaseModel
from couchbase.cluster import Bucket
from couchbase.exceptions import DocumentNotFoundException
from fastapi.encoders import jsonable_encoder

from core.config import INT_COUNTER_NAME
from services.exceptions import DocumentNotFound
from db.utils import fulltext_search


PydanticModel = TypeVar('PydanticModel', bound=BaseModel)


def get_next_id(bucket: Bucket):
    next_id = bucket.counter(INT_COUNTER_NAME, delta=1, initial=1).value
    if next_id == 1:
        query_result = bucket.query(
            f'SELECT MAX(META(b).id) FROM {bucket.name} AS b'
        )
        actual_last_id = query_result.get_single_result()['$1']
        if actual_last_id:
            if int(actual_last_id) > 0:
                next_id = int(actual_last_id) + 1
                bucket.upsert(INT_COUNTER_NAME, next_id)
    return str(next_id)


def upsert(bucket: Bucket, value: PydanticModel, key=None):
    if not key:
        key = get_next_id(bucket)
    result = bucket.upsert(key, jsonable_encoder(value))
    if result.success:
        return_value = get(bucket, key)
        return return_value


def update(bucket: Bucket, value: PydanticModel, key):
    result = bucket.upsert(key, jsonable_encoder(value))
    if result.success:
        return_value = get(bucket, key)
        return return_value


def get(bucket: Bucket, key):
    if key != INT_COUNTER_NAME:
        try:
            result = bucket.get(key)
            if result.success:
                result.value['id'] = key
                return result.value
        except DocumentNotFoundException:
            pass
    raise DocumentNotFound(key)


def delete(bucket: Bucket, key):
    get(bucket, key)
    result = bucket.remove(key)
    return result.value


def get_all(bucket: Bucket, skip: int = 0, limit: int = 30):
    query_result = bucket.query(
        f'SELECT META(b).id as id, b.* FROM {bucket.name} AS b WHERE META(b).id != "{INT_COUNTER_NAME}" ' +
        f'LIMIT {limit} OFFSET {skip}'
    )
    result = [row for row in query_result]
    return result


def filter_query(bucket: Bucket, skip: int = 0, limit: int = 30, **kwargs):
    query_string = f'SELECT META(b).id AS id,  b.* FROM {bucket.name} as b WHERE ' + \
                   ' '.join([f'{key}="{kwargs[key]}"' for key in kwargs])
    query_result = bucket.query(query_string + f'LIMIT {limit} OFFSET {skip}')
    return [row for row in query_result]


def custom_query(bucket: Bucket, skip: int = 0, limit: int = 30, query_string=''):
    query_result = bucket.query(query_string + f'LIMIT {limit} OFFSET {skip}')
    return [row for row in query_result]


def fulltext_in_bucket(bucket: Bucket, limit: int = 30, search_string=''):
    index = f'{bucket.name}_index'
    search_result = fulltext_search(index=index, limit=limit, search_string=search_string)
    return search_result
