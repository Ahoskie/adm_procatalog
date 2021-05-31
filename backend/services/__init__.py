from typing import TypeVar, List

from pydantic import BaseModel
from acouchbase.cluster import Bucket
from couchbase.exceptions import DocumentNotFoundException
from fastapi.encoders import jsonable_encoder

from core.config import INT_COUNTER_NAME
from services.exceptions import DocumentNotFound
from db import ClusterHolder
from db.filters import BaseFilter


PydanticModel = TypeVar('PydanticModel', bound=BaseModel)


async def get_next_id(bucket: Bucket):
    value = 1
    try:
        next_id = await bucket.get(INT_COUNTER_NAME)
        value = next_id.value + 1
        await bucket.upsert(INT_COUNTER_NAME, value)
    except DocumentNotFoundException:
        await bucket.upsert(INT_COUNTER_NAME, jsonable_encoder(1))
        query_result = ClusterHolder.cluster.query(
            f'SELECT MAX(TONUMBER(META(b).id)) FROM {bucket.name} AS b'
        )
        actual_last_id = 1
        async for row in query_result:
            actual_last_id = row['$1']
        if actual_last_id:
            if int(actual_last_id) > 0:
                value = int(actual_last_id) + 1
                await bucket.upsert(INT_COUNTER_NAME, value)
    return str(value)


async def upsert(bucket: Bucket, value: PydanticModel, key=None):
    if not key:
        key = await get_next_id(bucket)
    result = await bucket.upsert(key, jsonable_encoder(value))
    if result.success:
        return_value = await get(bucket, key)
        return return_value


async def update(bucket: Bucket, value: PydanticModel, key):
    try:
        db_object = await get(bucket, key)
    except DocumentNotFoundException:
        raise DocumentNotFound(key)

    incoming_data = jsonable_encoder(value)
    for attr in db_object:
        db_attr = db_object[attr]
        if attr != 'id' and not incoming_data[attr]:
            incoming_data[attr] = db_attr

    result = await bucket.upsert(key, incoming_data)
    if result.success:
        return_value = await get(bucket, key)
        return return_value


async def get(bucket: Bucket, key):
    if key != INT_COUNTER_NAME:
        try:
            result = await bucket.get(key)
            if result.success:
                result.value['id'] = key
                return result.value
        except DocumentNotFoundException:
            pass
    raise DocumentNotFound(key)


async def delete(bucket: Bucket, key):
    await get(bucket, key)
    result = await bucket.remove(key)
    return result.value


async def get_all(bucket: Bucket, skip: int = 0, limit: int = 30):
    query_result = ClusterHolder.cluster.query(
        f'SELECT META(b).id as id, b.* FROM {bucket.name} AS b WHERE META(b).id != "{INT_COUNTER_NAME}" ' +
        f'LIMIT {limit} OFFSET {skip}'
    )
    result = [row async for row in query_result]
    return result


async def filter_query(bucket: Bucket, skip: int = 0, limit: int = 30, **kwargs):
    query_string = f'SELECT META(b).id AS id,  b.* FROM {bucket.name} as b WHERE ' + \
                   ' '.join([f'{key}="{kwargs[key]}"' for key in kwargs])
    query_result = ClusterHolder.cluster.query(query_string + f' LIMIT {limit} OFFSET {skip}')
    return [row async for row in query_result]


async def custom_query(skip: int = 0, limit: int = 30, query_string=''):
    query_result = ClusterHolder.cluster.query(query_string + f' LIMIT {limit} OFFSET {skip}')
    return [row async for row in query_result]


async def search_in_bucket(bucket, search_string='', fields=[], filters=List[BaseFilter], skip=0, limit=100):
    cluster = ClusterHolder.cluster
    if len(search_string) < 3:
        return []
    # creating a search string with every word wrapped in %"word"%
    search_string = search_string.strip()
    search_strings = [f'"%{string}%"' for string in search_string.split(' ')]

    satisfactions = ' AND '.join([f'array_element LIKE LOWER({string})' for string in search_strings])
    concatenated_fields = " || \" \" || ".join(["b." + field for field in fields])
    fields_condition = f'ANY array_element IN SUFFIXES(LOWER({concatenated_fields})) SATISFIES {satisfactions}'

    query_string = f'SELECT b.*, META(b).id AS id FROM {bucket.name} AS b WHERE {fields_condition} END '
    filters_conditions = ' AND '.join([filter_obj.get_query_condition() for filter_obj in filters])
    if filters_conditions:
        query_string += 'AND ' + filters_conditions
    query_results = cluster.query(query_string + f'LIMIT {limit} OFFSET {skip}')
    return [row async for row in query_results]
